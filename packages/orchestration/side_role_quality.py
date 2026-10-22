"""F113 T003b — the quality gate of a side role on a local endpoint: a frozen spot-check set of seeded
facts, the flip to the role's own model when the endpoint loses, and the explicit re-check that flips
it back after a dwell (DECISION F113 D3).

A spot check runs only when an operator asks for it, with `remedy doctor side-roles --check`, never
inside a job. Each case of the summary role's set hands the endpoint's model a small diff whose facts
are seeded, and passes when the summary names every one of them within `SPOT_CHECK_MAX_SECONDS`: a
chore that takes too long fails like one that is wrong. Remedy deliberately does not ask a model to
judge the answer; the checks are the seeded facts.

A failed check flips the role to its own model for that endpoint and model, with the check named. A
passing check flips it back only when it is a re-check made at least `SPOT_CHECK_DWELL_S` after the
flip, so one lucky answer cannot undo a failure at once and the route never flaps. A check against an
endpoint that does not answer changes nothing: the probe already falls the role back on every call.
The checks are appended to `spot_checks.jsonl` and the flips kept in `quality_state.json`, under the
data root's `side_roles/`, because an endpoint and its model belong to the machine, not to a project.
"""

from __future__ import annotations

import json
import time
import uuid
from collections.abc import Callable, Mapping
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from packages.orchestration.local_endpoints import LocalEndpoint, LocalEndpointProbes

#: The version of the frozen set below; a record names the set it was checked against.
SPOT_CHECK_SET_VERSION = "summary-spot-check-v1"
#: The longest one case may take before it fails for slowness.
SPOT_CHECK_MAX_SECONDS: float = 60.0
#: How long a flip stands before a passing re-check may undo it.
SPOT_CHECK_DWELL_S: float = 3600.0

OUTCOME_PASSED = "passed"
OUTCOME_FAILED = "failed"
OUTCOME_UNAVAILABLE = "unavailable"
STATE_FLIPPED = "flipped"
STATE_LOCAL = "local"


@dataclass(frozen=True)
class SpotCheckCase:
    """One case: the diff sections the summary role is given, and the facts its summary must name."""

    name: str
    sections: tuple[tuple[str, str], ...]
    facts: tuple[str, ...]


def _diff(path: str, body: str) -> tuple[str, str]:
    return path, f"diff --git a/{path} b/{path}\n--- a/{path}\n+++ b/{path}\n{body}"


#: The summary role's frozen set: each case seeds facts a correct summary of its diff must name.
SUMMARY_SPOT_CHECKS: tuple[SpotCheckCase, ...] = (
    SpotCheckCase("new-function", (_diff("billing/invoice.py", (
        "@@ -1,2 +1,5 @@\n import decimal\n+\n+def compute_invoice_total(lines):\n"
        "+    return sum(line.amount for line in lines)\n")),), ("compute_invoice_total",)),
    SpotCheckCase("removed-setting", (_diff("config/settings.toml", (
        "@@ -3,3 +3,2 @@\n [network]\n-retry_limit = 5\n timeout_seconds = 30\n")),), ("retry_limit",)),
    SpotCheckCase("new-flag", (
        _diff("cli/main.py", "@@ -9,1 +9,2 @@\n parser.add_argument('--verbose')\n+parser.add_argument('--dry-run')\n"),
        _diff("README.md", "@@ -1,1 +1,2 @@\n # Tool\n+Pass --dry-run to print the plan without writing.\n"),
    ), ("--dry-run",)),
)

#: The roles that have a set; a mapped role without one is never checked and never flipped.
SPOT_CHECK_SETS: dict[str, tuple[SpotCheckCase, ...]] = {"summary": SUMMARY_SPOT_CHECKS}


@dataclass(frozen=True)
class SpotCheckCaseResult:
    """How one case went: passed, the facts the summary missed, its seconds, and why it failed."""

    name: str
    passed: bool
    missing_facts: tuple[str, ...]
    seconds: float
    reason: str


@dataclass(frozen=True)
class SpotCheckRecord:
    """One spot check of one role on one endpoint and model, as `spot_checks.jsonl` keeps it."""

    record_id: str
    role: str
    endpoint: str
    base_url: str
    model: str
    set_version: str
    checked_at: str
    outcome: str
    reason: str
    cases: tuple[SpotCheckCaseResult, ...]


def _run_case(case: SpotCheckCase, call_fn: Callable[[str, int], str], clock: Callable[[], float]) -> SpotCheckCaseResult:
    from packages.orchestration.artifact_summary import generate_artifact_summary

    sections = [{"section": path, "span_ref": f"file:{path}", "text": text} for path, text in case.sections]
    started = clock()
    summary = generate_artifact_summary(sections, f"spot-check:{case.name}", case.name, call_fn)
    seconds = round(clock() - started, 3)
    if summary.generator.startswith("fallback:"):
        return SpotCheckCaseResult(case.name, False, case.facts, seconds, f"no summary: {summary.generator}")
    said = "\n".join([summary.l1, *(section.summary for section in summary.l2)]).lower()
    missing = tuple(fact for fact in case.facts if fact.lower() not in said)
    if missing:
        return SpotCheckCaseResult(case.name, False, missing, seconds, f"missing facts: {', '.join(missing)}")
    if seconds > SPOT_CHECK_MAX_SECONDS:
        return SpotCheckCaseResult(case.name, False, (), seconds,
                                   f"took {seconds} seconds, more than {SPOT_CHECK_MAX_SECONDS:g}")
    return SpotCheckCaseResult(case.name, True, (), seconds, "")


def run_spot_check(
    role: str, endpoint: LocalEndpoint, *, probes: LocalEndpointProbes,
    call_fn: Callable[[str, int], str] | None = None, clock: Callable[[], float] = time.monotonic,
    now: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
) -> SpotCheckRecord:
    """Check `role` on `endpoint` against its frozen set; an endpoint that does not answer is not checked."""
    from packages.orchestration.artifact_summary import GeneratedSummaryContent
    from packages.orchestration.local_endpoints import make_local_call_fn

    cases = SPOT_CHECK_SETS[role]
    record = {"record_id": uuid.uuid4().hex[:12], "role": role, "endpoint": endpoint.name,
              "base_url": endpoint.base_url, "model": endpoint.model, "set_version": SPOT_CHECK_SET_VERSION,
              "checked_at": now().isoformat(timespec="seconds")}
    health = probes.health(endpoint)
    if not health.available:
        return SpotCheckRecord(**record, outcome=OUTCOME_UNAVAILABLE, reason=health.reason, cases=())
    serve = call_fn or make_local_call_fn(endpoint, GeneratedSummaryContent)
    results = tuple(_run_case(case, serve, clock) for case in cases)
    failed = [result.name for result in results if not result.passed]
    return SpotCheckRecord(**record, outcome=OUTCOME_FAILED if failed else OUTCOME_PASSED,
                           reason=f"failed cases: {', '.join(failed)}" if failed else "", cases=results)


def side_roles_dir(root: Path | None = None) -> Path:
    """Where the spot checks and the flips live: `side_roles/` under the data root."""
    from packages.orchestration.data_paths import resolve_data_root

    return (root or resolve_data_root()) / "side_roles"


def _state_path(root: Path | None) -> Path:
    return side_roles_dir(root) / "quality_state.json"


class QualityStateUnreadable(ValueError):
    """`quality_state.json` exists but does not read as the state of the checked roles."""


def read_quality_state(root: Path | None = None) -> dict[str, dict[str, Any]]:
    """Each checked role's state: its endpoint and model, `flipped` or `local`, since when, by which check."""
    path = _state_path(root)
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        raise QualityStateUnreadable(f"the side-role quality state {path.name} cannot be read: {exc}") from exc
    if not isinstance(data, dict):
        raise QualityStateUnreadable(f"the side-role quality state {path.name} is not a table of roles")
    return data


def _same_target(entry: Mapping[str, Any], endpoint: LocalEndpoint) -> bool:
    return (entry.get("endpoint"), entry.get("base_url"), entry.get("model")) == (
        endpoint.name, endpoint.base_url, endpoint.model)


def flip_reason(role: str, endpoint: LocalEndpoint, root: Path | None = None) -> str:
    """Why `role` runs on its own model instead of `endpoint`, or "" when no flip stands for this endpoint and model.

    A state that cannot be read keeps the role off the endpoint: Remedy does not run a role locally
    while it cannot tell whether that role failed its check.
    """
    try:
        entry = read_quality_state(root).get(role)
    except QualityStateUnreadable as exc:
        return f"quality_gate: {exc}"
    if not entry or entry.get("state") != STATE_FLIPPED or not _same_target(entry, endpoint):
        return ""
    return (f"quality_gate: {role} on {endpoint.name} ({endpoint.model}) failed spot check "
            f"{entry.get('record_id')} at {entry.get('since')}")


def dwell_ends(since: str) -> datetime:
    """When a flip made at `since` may be undone by a passing re-check."""
    return datetime.fromisoformat(since) + timedelta(seconds=SPOT_CHECK_DWELL_S)


def record_spot_check(record: SpotCheckRecord, root: Path | None = None) -> dict[str, Any]:
    """Append `record` to the history and apply it to the role's state; answer the state it leaves.

    A failure flips the role; a pass flips a standing flip back only once its dwell has passed; a
    check that found the endpoint unavailable leaves the state as it was.
    """
    folder = side_roles_dir(root)
    folder.mkdir(parents=True, exist_ok=True)
    with (folder / "spot_checks.jsonl").open("a", encoding="utf-8") as history:
        history.write(json.dumps(asdict(record), sort_keys=True) + "\n")
    state = read_quality_state(root)
    entry = state.get(record.role) or {}
    target = LocalEndpoint(record.endpoint, record.base_url, record.model)
    standing = entry.get("state") == STATE_FLIPPED and _same_target(entry, target)
    held = standing and datetime.fromisoformat(record.checked_at) < dwell_ends(entry["since"])
    if record.outcome == OUTCOME_UNAVAILABLE or (record.outcome == OUTCOME_PASSED and held):
        return entry
    new_state = STATE_FLIPPED if record.outcome == OUTCOME_FAILED else STATE_LOCAL
    entry = {"endpoint": record.endpoint, "base_url": record.base_url, "model": record.model, "state": new_state,
             "since": record.checked_at, "record_id": record.record_id, "set_version": record.set_version}
    state[record.role] = entry
    _state_path(root).write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return entry


def side_role_status_lines(routes: Mapping[str, LocalEndpoint], root: Path | None = None) -> list[str]:
    """One plain line per mapped role: where it runs and why, for `remedy status` and the doctor command."""
    try:
        state = read_quality_state(root)
    except QualityStateUnreadable as exc:
        return [f"every mapped side role runs on its own model: {exc}"] if routes else []
    lines = []
    for role, endpoint in routes.items():
        where = f"{role} on {endpoint.name} ({endpoint.model})"
        entry = state.get(role) or {}
        if role not in SPOT_CHECK_SETS:
            lines.append(f"{where}: no spot-check set exists for this role, so it is never checked")
        elif not entry or not _same_target(entry, endpoint):
            lines.append(f"{where}: not spot-checked for this endpoint and model yet")
        elif entry.get("state") == STATE_FLIPPED:
            lines.append(f"{where}: FLIPPED to its own model since {entry['since']} by failed spot check "
                         f"{entry['record_id']}; a passing re-check after {dwell_ends(entry['since']).isoformat()} "
                         "flips it back")
        else:
            lines.append(f"{where}: passing since spot check {entry['record_id']} at {entry['since']}")
    return lines
