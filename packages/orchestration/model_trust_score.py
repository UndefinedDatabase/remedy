"""F133 T002 — model trust score: the one trust home (DECISION F133 D1, D2).

Remedy's provider-trust pair (`provider_trust.py`, `provider_trust_verification.py`) was deleted at
`0242c0a3b`; it gated an externally produced patch candidate and computed no metric of a model's own
record. This module is the replacement home: for every model and role a project's jobs have used
inside a rolling window, it measures four things from the records that already exist — the cost
ledger's `calls` table, a job's own record, and a task run's `provider_evidence.json` and its
call-level post-mortems — and never a second time the same way `tier_outcomes.py` already keeps a
per-tier record.

The model of a call. A ledger row's `calls.model` column is set only when the job path verified the
model that actually answered, which in practice is almost never — the job path never sets
`actual_model_verified` (`pingpong_loop.py:4293`), so that column is empty on every real row today.
Where it is empty, the call joins to the `provider_attempts` entry of the same `seq` its own
`call_id` names (`<job_id>:<task_id>:<seq>`), read from the task run's `provider_evidence.json`, and
takes that entry's own `model`. A call that cannot be joined to an attempt with a non-empty model — an
old one-row-per-task-run row, or a missing evidence file — is counted as UNATTRIBUTED and never
guessed at.

The four metrics, each a :class:`TrustMetric` of its value and the sample count `n` it rests on:
`pass_quota` (passes over settled served tasks), `repair_need` (mean repair rounds over the same
tasks), `format_error_rate` (format errors over EVERY call of that model and role in the window's
tasks, keyed by each call's own model, settled or not) and `cost_per_pass` (that role's call cost over
its settled served tasks, divided by passes, read from the ledger's own `cost_basis` column: a call is
priced only when it has a figure and a basis other than `unknown`; the label is the one basis every
priced call of the sum shares, `provider_reported` or `price_table`, and `mixed` when they share none;
`tokens` when every call reported its tokens but none of them is priced, else `unknown` with no value
— a basis label that never claims a figure nothing reported). A task is SETTLED when its job record
gives it a passing or a failing terminal status; every other status, and a task whose record is gone,
is UNSETTLED and kept out of the outcome metrics. A row below the sample floor is marked THIN and is
never a leader. Among a role's rows that are not thin and have a pass quota, `trust_leader` names the
clear leader, when one leads the second-highest by at least `TRUST_LEADER_MARGIN` (DECISION F133 D3
(1)) — trust is a RECOMMENDATION read by a human; it never changes a route by itself.

Remedy deliberately does not guess a model for an unjoinable call, count an unsettled task toward an
outcome, invent a cost basis nothing reported, or read `tier_outcomes.query_tier_outcomes` here: that
function writes to the ledger on every call and keeps no window, so the per-tier record stays
`tier_outcomes.py`'s own and this module computes nothing per tier (DECISION F133 D3 (3)).

The measurement is read-only on the ledger, the job store and the evidence tree: it opens the ledger
the way `token_ledger` opens every query, with `mode=rw` and `PRAGMA query_only=1`. The table is
cached as `model_trust_snapshot.json` beside the ledger and rebuilt once it is older than its limit,
or was built with another window or floor; nothing refreshes it in the background.
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

#: Model-of-a-call cost bases this module itself reports: the ledger's own two labels, kept equal to
#: `token_ledger`'s own by `test_cost_basis_constants_match_the_ledgers_own_vocabulary` (AGENTS.md,
#: "One spelling per concept"), plus two this module adds: `tokens` when every call reported its
#: tokens but none is priced, and `mixed` when a cost-per-pass sum's priced calls do not all share
#: one basis.
COST_BASIS_PROVIDER_REPORTED = "provider_reported"
COST_BASIS_UNKNOWN = "unknown"
TRUST_COST_BASIS_PRICE_TABLE = "price_table"
TRUST_COST_BASIS_TOKENS = "tokens"
TRUST_COST_BASIS_MIXED = "mixed"

#: The snapshot file, beside the project's ledger, and the schema generation of its JSON.
MODEL_TRUST_SNAPSHOT_FILENAME = "model_trust_snapshot.json"
MODEL_TRUST_SNAPSHOT_SCHEMA = 1

#: DECISION F133 D3 (1): the minimum lead, in pass-quota points, the top eligible row of a role
#: needs over the second-highest one to be that role's clear leader.
TRUST_LEADER_MARGIN = 0.10

#: `trust_leader`'s `reason` (DECISION F133 D3 (1)): a clear leader was found, too few of the
#: role's rows are eligible (not thin, with a pass quota) to compare, or the top two rows exist but
#: the lead between them is below `TRUST_LEADER_MARGIN`.
TRUST_RECOMMENDATION_LEADER = "leader"
TRUST_RECOMMENDATION_TOO_FEW_ELIGIBLE = "too_few_eligible"
TRUST_RECOMMENDATION_NO_MARGIN = "no_margin"

#: The defaults of `model_routing.trust_window_days`, `model_routing.trust_sample_floor` and
#: `model_routing.trust_snapshot_max_age_seconds` (DECISION F133 D2 (1)).
DEFAULT_TRUST_WINDOW_DAYS = 90
DEFAULT_TRUST_SAMPLE_FLOOR = 20
DEFAULT_TRUST_SNAPSHOT_MAX_AGE_SECONDS = 3600

# A job id or task id is a path segment of the job store; anything else is not looked up on disk.
_SAFE_ID_RE = re.compile(r"^[A-Za-z0-9_-]+$")

_CALL_QUERY = """
SELECT job_id, task_id, call_id, role, model, tokens_in, tokens_out, cost_usd, ts_utc, cost_basis
FROM calls
WHERE job_id IS NOT NULL AND job_id != '' AND task_id IS NOT NULL AND task_id != ''
"""


class TrustConfigError(ValueError):
    """A `model_routing.trust_*` setting could not be parsed; the command exits 2 on it."""


@dataclass(frozen=True)
class TrustMetric:
    """One measured figure and the sample count it rests on; ``value`` is None when ``n`` is 0."""

    value: float | None
    n: int

    def to_json(self) -> dict[str, Any]:
        return {"value": self.value, "n": self.n}


@dataclass(frozen=True)
class ModelTrustRow:
    """One model's record of one role, inside the window."""

    role: str
    model: str
    pass_quota: TrustMetric
    repair_need: TrustMetric
    format_error_rate: TrustMetric
    cost_per_pass: TrustMetric
    cost_basis: str
    settled_tasks: int
    thin: bool

    def to_json(self) -> dict[str, Any]:
        return {
            "role": self.role,
            "model": self.model,
            "pass_quota": self.pass_quota.to_json(),
            "repair_need": self.repair_need.to_json(),
            "format_error_rate": self.format_error_rate.to_json(),
            "cost_per_pass": self.cost_per_pass.to_json(),
            "cost_basis": self.cost_basis,
            "settled_tasks": self.settled_tasks,
            "thin": self.thin,
        }


@dataclass(frozen=True)
class ModelTrustTable:
    """A project's trust matrix: every model and role seen inside the window, and what was not."""

    project_id: str
    updated_at: str
    window_days: int
    sample_floor: int
    window_start: str
    ledger_present: bool
    rows: tuple[ModelTrustRow, ...]
    unattributed_calls: int
    unsettled_tasks: int

    def lookup(self, model: str, role: str) -> ModelTrustRow | None:
        """The row of ``model`` and ``role``, or None when neither was seen in the window."""
        for row in self.rows:
            if row.model == model and row.role == role:
                return row
        return None

    def to_json(self) -> dict[str, Any]:
        return {
            "schema": MODEL_TRUST_SNAPSHOT_SCHEMA,
            "project_id": self.project_id,
            "updated_at": self.updated_at,
            "window_days": self.window_days,
            "sample_floor": self.sample_floor,
            "window_start": self.window_start,
            "ledger_present": self.ledger_present,
            "rows": [row.to_json() for row in self.rows],
            "unattributed_calls": self.unattributed_calls,
            "unsettled_tasks": self.unsettled_tasks,
        }


@dataclass(frozen=True)
class TrustRecommendation:
    """DECISION F133 D3 (1): one role's clear-leader recommendation, or why there is none.

    ``leader``, ``runner_up`` and the two pass quotas are ``None`` unless ``reason`` is
    :data:`TRUST_RECOMMENDATION_LEADER` — when there is no recommendation, no model is named.
    """

    role: str
    leader: str | None
    leader_pass_quota: float | None
    leader_settled_tasks: int | None
    runner_up: str | None
    runner_up_pass_quota: float | None
    reason: str

    def to_json(self) -> dict[str, Any]:
        return {
            "role": self.role,
            "leader": self.leader,
            "leader_pass_quota": self.leader_pass_quota,
            "leader_settled_tasks": self.leader_settled_tasks,
            "runner_up": self.runner_up,
            "runner_up_pass_quota": self.runner_up_pass_quota,
            "reason": self.reason,
        }


@dataclass
class _RowAccumulator:
    """Mutable running totals for one (model, role) bucket while the ledger is walked once."""

    calls_total: int = 0
    calls_error: int = 0
    settled_tasks: int = 0
    passes: int = 0
    repair_sum: int = 0
    cost_sum: float = 0.0
    tokens_sum: int = 0
    # DECISION F133 D3 (2): a call is PRICED only when it has a cost figure and a basis other than
    # `unknown`; `all_priced` is False once any call of any settled task added here was not, and
    # `priced_bases` holds every distinct basis a priced call carried.
    all_priced: bool = True
    priced_bases: set[str] = field(default_factory=set)
    tokens_known: bool = True

    def add_call(self, *, is_error: bool) -> None:
        self.calls_total += 1
        if is_error:
            self.calls_error += 1

    def add_settled_task(self, *, passed: bool, repair_rounds_used: int,
                          role_calls: list[tuple[Any, ...]]) -> None:
        self.settled_tasks += 1
        if passed:
            self.passes += 1
        self.repair_sum += repair_rounds_used
        task_cost = 0.0
        task_tokens = 0
        for _call_id, _role, _model, tok_in, tok_out, cost, _ts, basis in role_calls:
            if cost is not None and basis != COST_BASIS_UNKNOWN:
                self.priced_bases.add(basis)
                task_cost += float(cost)
            else:
                self.all_priced = False
            if tok_in is None or tok_out is None:
                self.tokens_known = False
            else:
                task_tokens += int(tok_in) + int(tok_out)
        self.cost_sum += task_cost
        self.tokens_sum += task_tokens


def resolve_trust_settings(*, project_root: str | None = None) -> dict[str, int]:
    """F133's three settings from the config authority: env > `remedy.toml` > default.

    Keys ``window_days``, ``sample_floor`` and ``max_age_seconds``; raises
    :class:`TrustConfigError` for a malformed value, as ``resolve_calibration_settings`` does for
    its own three.
    """
    from packages.orchestration.config import ConfigSource, load_config
    from packages.orchestration.config_keys_model_routing import (
        TRUST_SAMPLE_FLOOR_CONFIG_KEY,
        TRUST_SNAPSHOT_MAX_AGE_SECONDS_CONFIG_KEY,
        TRUST_WINDOW_DAYS_CONFIG_KEY,
    )

    cfg = load_config(project_path=Path(project_root) / "remedy.toml") if project_root else load_config()
    fallbacks = {
        "window_days": DEFAULT_TRUST_WINDOW_DAYS,
        "sample_floor": DEFAULT_TRUST_SAMPLE_FLOOR,
        "max_age_seconds": DEFAULT_TRUST_SNAPSHOT_MAX_AGE_SECONDS,
    }
    keys = {
        "window_days": TRUST_WINDOW_DAYS_CONFIG_KEY,
        "sample_floor": TRUST_SAMPLE_FLOOR_CONFIG_KEY,
        "max_age_seconds": TRUST_SNAPSHOT_MAX_AGE_SECONDS_CONFIG_KEY,
    }
    settings: dict[str, int] = {}
    for name, key in keys.items():
        cv = cfg.get_value(key)
        raw = cv.value if cv is not None and cv.source != ConfigSource.DEFAULT else None
        resolved = _pos_int(key, raw)
        settings[name] = fallbacks[name] if resolved is None else resolved
    return settings


def _pos_int(name: str, raw: Any) -> int | None:
    if raw is None:
        return None
    if isinstance(raw, bool):
        raise TrustConfigError(f"{name} must be an integer, got bool")
    if isinstance(raw, str):
        raw = raw.strip()
        if not raw:
            return None
        try:
            raw = int(raw)
        except ValueError:
            raise TrustConfigError(f"{name} is not a valid integer: {raw!r}") from None
    if isinstance(raw, float):
        if raw != int(raw):
            raise TrustConfigError(f"{name} must be an integer, got float {raw}")
        raw = int(raw)
    if not isinstance(raw, int):
        raise TrustConfigError(f"{name} must be an integer, got {type(raw).__name__}")
    if raw <= 0:
        raise TrustConfigError(f"{name} must be strictly positive, got {raw}")
    return raw


def _parse_utc(text: str) -> datetime | None:
    try:
        moment = datetime.fromisoformat(str(text).replace("Z", "+00:00"))
    except ValueError:
        return None
    return moment if moment.tzinfo is not None else moment.replace(tzinfo=timezone.utc)


def _connect_ledger_readonly(path: Path) -> Any:
    from packages.orchestration.token_ledger import _connect_readonly

    return _connect_readonly(path)


def _call_seq(call_id: str, job_id: str, task_id: str) -> int | None:
    """The attempt's 1-based position, parsed from ``call_id`` (DECISION F133 D2 (2)).

    A per-call row's ``call_id`` is ``"<job_id>:<task_id>:<seq>"``; the older one-row-per-task-run
    shape has no trailing ``:<seq>`` at all, and returns None.
    """
    prefix = f"{job_id}:{task_id}:"
    if not call_id.startswith(prefix):
        return None
    remainder = call_id[len(prefix):]
    return int(remainder) if remainder.isdigit() else None


def _task_run_attempts(job_id: str, task_id: str, root: Path | None,
                        cache: dict[tuple[str, str], list[dict[str, Any]]]) -> list[dict[str, Any]]:
    """``provider_attempts`` of one task run, cached; ``[]`` when it cannot be read."""
    key = (job_id, task_id)
    if key in cache:
        return cache[key]
    attempts: list[dict[str, Any]] = []
    if _SAFE_ID_RE.match(job_id) and _SAFE_ID_RE.match(task_id):
        from packages.orchestration.data_paths import job_evidence_dir

        path = job_evidence_dir(job_id, root) / "task_runs" / task_id / "provider_evidence.json"
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            data = None
        raw = data.get("provider_attempts") if isinstance(data, dict) else None
        if isinstance(raw, list):
            attempts = [a for a in raw if isinstance(a, dict)]
    cache[key] = attempts
    return attempts


def _own_model(call: tuple[Any, ...], job_id: str, task_id: str, root: Path | None,
                attempts_cache: dict[tuple[str, str], list[dict[str, Any]]]) -> str | None:
    """The call's own model: the ledger's, when the job path verified one, else the attempt's."""
    call_id, _role, model_col, *_rest = call
    if model_col:
        return str(model_col)
    seq = _call_seq(call_id, job_id, task_id)
    if seq is None:
        return None
    for attempt in _task_run_attempts(job_id, task_id, root, attempts_cache):
        if attempt.get("seq") == seq:
            model = attempt.get("model")
            return str(model) if model else None
    return None


def _parse_postmortem_roles(job_id: str, task_id: str, root: Path | None) -> set[str]:
    """Roles whose task run carries a call-scope post-mortem of class ``parse``."""
    if not (_SAFE_ID_RE.match(job_id) and _SAFE_ID_RE.match(task_id)):
        return set()
    from packages.orchestration.data_paths import job_evidence_dir
    from packages.orchestration.failure_postmortem import FailureClass, collect_task_call_postmortems

    stream_dir = job_evidence_dir(job_id, root) / "task_runs" / task_id / "streams"
    roles: set[str] = set()
    for _label, path in collect_task_call_postmortems(task_stream_dir=stream_dir):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(data, dict) and data.get("failure_class") == FailureClass.PARSE.value and data.get("role"):
            roles.add(str(data["role"]))
    return roles


def _format_error_seqs(attempts: list[dict[str, Any]], parse_roles: set[str]) -> set[int]:
    """Seqs that are format errors (DECISION F133 D2 (4)): a later same-role-and-round parse retry,
    or the role's last call where a parse post-mortem exists for that role. Counted once per call."""
    by_role: dict[str, list[dict[str, Any]]] = {}
    for attempt in attempts:
        by_role.setdefault(str(attempt.get("role") or ""), []).append(attempt)
    errors: set[int] = set()
    for role, alist in by_role.items():
        seqs = [a.get("seq") for a in alist if isinstance(a.get("seq"), int)]
        if not seqs:
            continue
        max_seq = max(seqs)
        for attempt in alist:
            seq = attempt.get("seq")
            if not isinstance(seq, int):
                continue
            rnd = attempt.get("round")
            later_retry = any(
                other.get("role") == role and other.get("round") == rnd
                and isinstance(other.get("seq"), int) and other["seq"] > seq
                and other.get("is_parse_retry") is True
                for other in alist
            )
            if later_retry:
                errors.add(seq)
            elif seq == max_seq and role in parse_roles:
                errors.add(seq)
    return errors


def _error_seqs(job_id: str, task_id: str, root: Path | None,
                 attempts_cache: dict[tuple[str, str], list[dict[str, Any]]],
                 error_cache: dict[tuple[str, str], set[int]]) -> set[int]:
    key = (job_id, task_id)
    if key in error_cache:
        return error_cache[key]
    attempts = _task_run_attempts(job_id, task_id, root, attempts_cache)
    parse_roles = _parse_postmortem_roles(job_id, task_id, root)
    errors = _format_error_seqs(attempts, parse_roles)
    error_cache[key] = errors
    return errors


def _job_task_status(job_id: str, root: Path | None,
                      cache: dict[str, dict[str, dict[str, Any]]]) -> dict[str, dict[str, Any]]:
    """``{task_id: {"status":, "repair_rounds_used":}}`` from the job's own record."""
    if job_id in cache:
        return cache[job_id]
    info: dict[str, dict[str, Any]] = {}
    if _SAFE_ID_RE.match(job_id):
        from packages.orchestration.data_paths import job_record_path

        try:
            record = json.loads(job_record_path(job_id, root).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            record = None
        tasks = record.get("tasks") if isinstance(record, dict) else None
        for task in tasks if isinstance(tasks, list) else ():
            if isinstance(task, dict) and task.get("task_id"):
                info[str(task["task_id"])] = {
                    "status": task.get("status"),
                    "repair_rounds_used": task.get("repair_rounds_used", 0),
                }
    cache[job_id] = info
    return info


def _settlement(task_info: dict[str, Any] | None) -> str | None:
    """"pass", "fail" or None (unsettled — kept out of the outcome metrics)."""
    from packages.orchestration.pingpong_job import TASK_BLOCKED, TASK_DONE_STATUSES, TASK_FAILED

    if task_info is None:
        return None
    status = task_info.get("status")
    if status in TASK_DONE_STATUSES:
        return "pass"
    if status in (TASK_FAILED, TASK_BLOCKED):
        return "fail"
    return None


def _finalize_row(role: str, model: str, acc: _RowAccumulator, sample_floor: int) -> ModelTrustRow:
    pass_quota = TrustMetric(
        value=(acc.passes / acc.settled_tasks) if acc.settled_tasks else None, n=acc.settled_tasks)
    repair_need = TrustMetric(
        value=(acc.repair_sum / acc.settled_tasks) if acc.settled_tasks else None, n=acc.settled_tasks)
    format_error_rate = TrustMetric(
        value=(acc.calls_error / acc.calls_total) if acc.calls_total else None, n=acc.calls_total)
    if acc.passes == 0:
        cost_basis, cost_value = COST_BASIS_UNKNOWN, None
    elif acc.all_priced and acc.priced_bases:
        cost_basis = (next(iter(acc.priced_bases)) if len(acc.priced_bases) == 1
                      else TRUST_COST_BASIS_MIXED)
        cost_value = acc.cost_sum / acc.passes
    elif acc.tokens_known:
        cost_basis, cost_value = TRUST_COST_BASIS_TOKENS, acc.tokens_sum / acc.passes
    else:
        cost_basis, cost_value = COST_BASIS_UNKNOWN, None
    cost_per_pass = TrustMetric(value=cost_value, n=acc.passes)
    return ModelTrustRow(
        role=role, model=model, pass_quota=pass_quota, repair_need=repair_need,
        format_error_rate=format_error_rate, cost_per_pass=cost_per_pass, cost_basis=cost_basis,
        settled_tasks=acc.settled_tasks, thin=acc.settled_tasks < sample_floor)


def build_model_trust_table(
    project_id: str,
    *,
    now: datetime,
    window_days: int = DEFAULT_TRUST_WINDOW_DAYS,
    sample_floor: int = DEFAULT_TRUST_SAMPLE_FLOOR,
    root: Path | None = None,
    window_end: datetime | None = None,
) -> ModelTrustTable:
    """Measure ``project_id``'s ledger: one row per model and role seen inside the window.

    A task is in the window when its latest call is no older than ``window_days`` before ``now``
    and, when ``window_end`` is given, no newer than it — the trust view's one addition over the
    estimate calibration's own window test, needed to measure a PRIOR window that does not overlap
    the current one; ``window_end=None`` (every other caller) measures exactly as calibration does,
    with no upper bound. Read-only on the ledger; raises ``sqlite3.Error`` when it cannot be read.
    """
    from packages.orchestration.token_ledger import token_ledger_path_for

    window_start = now - timedelta(days=window_days)
    ledger_path = token_ledger_path_for(project_id, root)
    if not ledger_path.is_file():
        return ModelTrustTable(
            project_id=str(project_id), updated_at=now.isoformat(), window_days=window_days,
            sample_floor=sample_floor, window_start=window_start.isoformat(), ledger_present=False,
            rows=(), unattributed_calls=0, unsettled_tasks=0)
    conn = _connect_ledger_readonly(ledger_path)
    try:
        call_rows = conn.execute(_CALL_QUERY).fetchall()
    finally:
        conn.close()

    tasks_latest: dict[tuple[str, str], datetime] = {}
    by_task: dict[tuple[str, str], list[tuple[Any, ...]]] = {}
    for job_id, task_id, call_id, role, model, tok_in, tok_out, cost, ts, cost_basis in call_rows:
        key = (str(job_id), str(task_id))
        by_task.setdefault(key, []).append(
            (str(call_id), str(role or ""), model, tok_in, tok_out, cost, ts, str(cost_basis)))
        moment = _parse_utc(ts)
        if moment is not None and (key not in tasks_latest or moment > tasks_latest[key]):
            tasks_latest[key] = moment

    status_cache: dict[str, dict[str, dict[str, Any]]] = {}
    attempts_cache: dict[tuple[str, str], list[dict[str, Any]]] = {}
    error_cache: dict[tuple[str, str], set[int]] = {}
    buckets: dict[tuple[str, str], _RowAccumulator] = {}
    unattributed_calls = 0
    unsettled_tasks = 0

    for (job_id, task_id), calls in sorted(by_task.items()):
        latest = tasks_latest.get((job_id, task_id))
        if latest is None or latest < window_start or (window_end is not None and latest > window_end):
            continue
        task_info = _job_task_status(job_id, root, status_cache).get(task_id)
        settled = _settlement(task_info)
        if settled is None:
            unsettled_tasks += 1

        by_role: dict[str, list[tuple[Any, ...]]] = {}
        for call in calls:
            by_role.setdefault(call[1], []).append(call)

        for role, role_calls in by_role.items():
            role_calls_sorted = sorted(role_calls, key=lambda c: _call_seq(c[0], job_id, task_id) or 0)
            own_models = [_own_model(c, job_id, task_id, root, attempts_cache) for c in role_calls_sorted]
            for call, own_model in zip(role_calls_sorted, own_models):
                if own_model is None:
                    unattributed_calls += 1
                    continue
                seq = _call_seq(call[0], job_id, task_id)
                is_error = seq is not None and seq in _error_seqs(
                    job_id, task_id, root, attempts_cache, error_cache)
                buckets.setdefault((role, own_model), _RowAccumulator()).add_call(is_error=is_error)

            serving_model = own_models[-1] if own_models else None
            if settled is not None and serving_model is not None:
                buckets.setdefault((role, serving_model), _RowAccumulator()).add_settled_task(
                    passed=(settled == "pass"),
                    repair_rounds_used=int((task_info or {}).get("repair_rounds_used", 0) or 0),
                    role_calls=role_calls_sorted)

    rows = tuple(
        _finalize_row(role, model, acc, sample_floor)
        for (role, model), acc in sorted(buckets.items())
    )
    return ModelTrustTable(
        project_id=str(project_id), updated_at=now.isoformat(), window_days=window_days,
        sample_floor=sample_floor, window_start=window_start.isoformat(), ledger_present=True,
        rows=rows, unattributed_calls=unattributed_calls, unsettled_tasks=unsettled_tasks)


#: R-1432: the lead and the margin are compared in whole hundredths of a POINT (a point being one
#: pass-quota percentage point, 0.01) rather than in raw floating point, so a lead that is
#: mathematically exactly `TRUST_LEADER_MARGIN` — such as 17 of 20 tasks against 15 of 20, whose
#: `float` difference is `0.09999999999999998` — is never refused by rounding noise many orders
#: below one task in a thousand.
_HUNDREDTHS_OF_A_POINT_PER_UNIT = 10_000


def _hundredths_of_a_point(value: float) -> int:
    return round(value * _HUNDREDTHS_OF_A_POINT_PER_UNIT)


def trust_leader(table: ModelTrustTable, role: str) -> TrustRecommendation:
    """DECISION F133 D3 (1): ``role``'s clear leader among its eligible rows, or why there is none.

    Eligible: not thin and has a pass quota. With at least two eligible rows, the highest pass
    quota is the clear leader only when it leads the second-highest by at least
    :data:`TRUST_LEADER_MARGIN`; a tie, a lead below the margin, or fewer than two eligible rows
    means no leader.
    """
    eligible = sorted(
        (row for row in table.rows if row.role == role and not row.thin
         and row.pass_quota.value is not None),
        key=lambda row: row.pass_quota.value, reverse=True)
    if len(eligible) < 2:
        return TrustRecommendation(
            role=role, leader=None, leader_pass_quota=None, leader_settled_tasks=None,
            runner_up=None, runner_up_pass_quota=None, reason=TRUST_RECOMMENDATION_TOO_FEW_ELIGIBLE)
    top, second = eligible[0], eligible[1]
    lead = top.pass_quota.value - second.pass_quota.value
    if _hundredths_of_a_point(lead) < _hundredths_of_a_point(TRUST_LEADER_MARGIN):
        return TrustRecommendation(
            role=role, leader=None, leader_pass_quota=None, leader_settled_tasks=None,
            runner_up=None, runner_up_pass_quota=None, reason=TRUST_RECOMMENDATION_NO_MARGIN)
    return TrustRecommendation(
        role=role, leader=top.model, leader_pass_quota=top.pass_quota.value,
        leader_settled_tasks=top.settled_tasks, runner_up=second.model,
        runner_up_pass_quota=second.pass_quota.value, reason=TRUST_RECOMMENDATION_LEADER)


def _metric_from_json(raw: Any) -> TrustMetric:
    return TrustMetric(value=None if raw["value"] is None else float(raw["value"]), n=int(raw["n"]))


def _row_from_json(raw: dict[str, Any]) -> ModelTrustRow:
    return ModelTrustRow(
        role=str(raw["role"]), model=str(raw["model"]),
        pass_quota=_metric_from_json(raw["pass_quota"]),
        repair_need=_metric_from_json(raw["repair_need"]),
        format_error_rate=_metric_from_json(raw["format_error_rate"]),
        cost_per_pass=_metric_from_json(raw["cost_per_pass"]),
        cost_basis=str(raw["cost_basis"]), settled_tasks=int(raw["settled_tasks"]), thin=bool(raw["thin"]))


def model_trust_table_from_json(raw: dict[str, Any]) -> ModelTrustTable:
    """The table a snapshot holds; raises ``KeyError``, ``TypeError`` or ``ValueError`` on a bad one."""
    if raw.get("schema") != MODEL_TRUST_SNAPSHOT_SCHEMA:
        raise ValueError(f"model trust snapshot schema {raw.get('schema')!r} is not {MODEL_TRUST_SNAPSHOT_SCHEMA}")
    rows = tuple(_row_from_json(item) for item in raw["rows"])
    return ModelTrustTable(
        project_id=str(raw["project_id"]), updated_at=str(raw["updated_at"]),
        window_days=int(raw["window_days"]), sample_floor=int(raw["sample_floor"]),
        window_start=str(raw["window_start"]), ledger_present=bool(raw["ledger_present"]),
        rows=rows, unattributed_calls=int(raw["unattributed_calls"]),
        unsettled_tasks=int(raw["unsettled_tasks"]))


def model_trust_snapshot_path(project_id: str, root: Path | None = None) -> Path:
    """``<data_root>/projects/<project_id>/model_trust_snapshot.json``, beside the project's ledger."""
    from packages.orchestration.token_ledger import token_ledger_path_for

    return token_ledger_path_for(project_id, root).with_name(MODEL_TRUST_SNAPSHOT_FILENAME)


def load_model_trust_table(
    project_id: str,
    *,
    now: datetime | None = None,
    window_days: int = DEFAULT_TRUST_WINDOW_DAYS,
    sample_floor: int = DEFAULT_TRUST_SAMPLE_FLOOR,
    max_age_seconds: int = DEFAULT_TRUST_SNAPSHOT_MAX_AGE_SECONDS,
    root: Path | None = None,
) -> ModelTrustTable:
    """The project's trust table: the snapshot while it is fresh, otherwise a new measurement.

    A snapshot is used only when it parses, was built with this window and floor, and is no older
    than ``max_age_seconds``; otherwise the ledger is measured again and, when a ledger exists, the
    new table replaces the snapshot. A snapshot that cannot be written leaves the measurement in use.
    """
    from packages.common.secure_fs import durable_write_json

    moment = now or datetime.now(timezone.utc)
    path = model_trust_snapshot_path(project_id, root)
    try:
        cached = model_trust_table_from_json(json.loads(path.read_text(encoding="utf-8")))
    except (OSError, ValueError, KeyError, TypeError):
        cached = None
    if cached is not None and cached.window_days == window_days and cached.sample_floor == sample_floor:
        built = _parse_utc(cached.updated_at)
        if built is not None and timedelta(0) <= moment - built <= timedelta(seconds=max_age_seconds):
            return cached
    table = build_model_trust_table(
        project_id, now=moment, window_days=window_days, sample_floor=sample_floor, root=root)
    if table.ledger_present:
        try:
            durable_write_json(path, table.to_json())
        except OSError:
            logger.warning(
                "model trust snapshot %s could not be written; the measurement is used unsaved",
                path, exc_info=True)
    return table
