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
its settled served tasks, divided by passes, with a basis label that never claims a figure nothing
reported). A task is SETTLED when its job record gives it a passing or a failing terminal status;
every other status, and a task whose record is gone, is UNSETTLED and kept out of the outcome
metrics. A row below the sample floor is marked THIN and is never a leader.

Remedy deliberately does not guess a model for an unjoinable call, count an unsettled task toward an
outcome, invent a cost basis nothing reported, or read `tier_outcomes.query_tier_outcomes` here — that
join is round 3's, beside this module's own matrix (DECISION F133 D2 (6)).

The measurement is read-only on the ledger, the job store and the evidence tree: it opens the ledger
the way `token_ledger` opens every query, with `mode=rw` and `PRAGMA query_only=1`. The table is
cached as `model_trust_snapshot.json` beside the ledger and rebuilt once it is older than its limit,
or was built with another window or floor; nothing refreshes it in the background.
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

#: Model-of-a-call cost bases this module itself reports: the ledger's own two labels, plus a third
#: this module adds when every call reported its tokens but not its cost.
COST_BASIS_PROVIDER_REPORTED = "provider_reported"
COST_BASIS_UNKNOWN = "unknown"
TRUST_COST_BASIS_TOKENS = "tokens"

#: The snapshot file, beside the project's ledger, and the schema generation of its JSON.
MODEL_TRUST_SNAPSHOT_FILENAME = "model_trust_snapshot.json"
MODEL_TRUST_SNAPSHOT_SCHEMA = 1

#: The defaults of `model_routing.trust_window_days`, `model_routing.trust_sample_floor` and
#: `model_routing.trust_snapshot_max_age_seconds` (DECISION F133 D2 (1)).
DEFAULT_TRUST_WINDOW_DAYS = 90
DEFAULT_TRUST_SAMPLE_FLOOR = 20
DEFAULT_TRUST_SNAPSHOT_MAX_AGE_SECONDS = 3600

# A job id or task id is a path segment of the job store; anything else is not looked up on disk.
_SAFE_ID_RE = re.compile(r"^[A-Za-z0-9_-]+$")

_CALL_QUERY = """
SELECT job_id, task_id, call_id, role, model, tokens_in, tokens_out, cost_usd, ts_utc
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
    cost_known: bool = True
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
        for _call_id, _role, _model, tok_in, tok_out, cost, _ts in role_calls:
            if cost is None:
                self.cost_known = False
            else:
                task_cost += float(cost)
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

    cfg = load_config(project_path=Path(project_root) / "remedy.toml") if project_root else load_config()
    fallbacks = {
        "window_days": DEFAULT_TRUST_WINDOW_DAYS,
        "sample_floor": DEFAULT_TRUST_SAMPLE_FLOOR,
        "max_age_seconds": DEFAULT_TRUST_SNAPSHOT_MAX_AGE_SECONDS,
    }
    keys = {
        "window_days": "model_routing.trust_window_days",
        "sample_floor": "model_routing.trust_sample_floor",
        "max_age_seconds": "model_routing.trust_snapshot_max_age_seconds",
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


