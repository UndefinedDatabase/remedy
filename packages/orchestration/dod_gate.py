"""F061 T004 — the job-end gate: a job ends green only when its DoD does.

The rule, in one sentence: **any red BLOCKING check keeps the job open.**

  * every blocking check green  → the gate RELEASES and the job may end green;
  * one or more blocking reds   → the gate HOLDS, the job stays open with
    status blocked, and the matrix says which checks and why;
  * non-blocking reds           → REPORTED, never gating. They appear in the
    matrix with their reason and change no outcome.

A job with no stored DoD is not gated: :func:`run_job_gate` returns ``None``,
and the caller's behaviour is exactly what it was before this feature existed.
That is deliberate — the gate can only ever make a green job blocked, never the
reverse, and a job nobody compiled a DoD for is not silently held.

Storage lives in the job's evidence area (data root), beside the report and the
cycle records — never in the user's repository:

    <job evidence>/dod.json         the compiled DoD (written by the compiler)
    <job evidence>/dod_result.json  the last gate run (written by this module)

Running the checks is :mod:`dod_runners`' job; deciding what their results MEAN
is this module's, and only this module's. That split is why the runners could
be proven red and green without a job anywhere near them.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from packages.orchestration.dod_runners import (
    CHECK_TIMEOUT_DEFAULT_SEC,
    STATUS_PASSED,
    CheckEvidence,
    UnsupportedCheckKindError,
    run_check,
)
from packages.orchestration.dod_schema import DoD

#: Filenames inside the job's evidence area.
DOD_FILENAME = "dod.json"
DOD_RESULT_FILENAME = "dod_result.json"

#: The blocker string the gate contributes to a fulfillment record, so a reader
#: can tell a DoD hold apart from any other contract blocker at a glance.
BLOCKER_PREFIX = "dod_blocking_red"

#: Reason recorded when a check kind has no runner at all. The gate does NOT
#: crash the job on it, but it never counts as green either: an unrunnable
#: blocking check holds the job exactly like a failed one.
REASON_NO_RUNNER = "no_runner"


def job_evidence_dir(job_id: str) -> Path:
    """The job's evidence area — the same one the report and cycles use."""
    from packages.orchestration.pingpong_job import job_evidence_dir as _dir
    return Path(_dir(job_id))


def dod_path(job_id: str) -> Path:
    return job_evidence_dir(job_id) / DOD_FILENAME


def result_path(job_id: str) -> Path:
    return job_evidence_dir(job_id) / DOD_RESULT_FILENAME


def store_dod(job_id: str, dod: DoD) -> Path:
    """Persist a job's compiled DoD into its evidence area."""
    path = dod_path(job_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(dod.model_dump(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    return path


def load_dod(job_id: str) -> DoD | None:
    """The job's DoD, or None when there is none / it will not parse.

    An unparseable DoD reads as absent rather than raising: the gate must not
    be the thing that crashes a finished job. It is not silently green either —
    :func:`run_job_gate` records the read failure in its result.
    """
    path = dod_path(job_id)
    if not path.is_file():
        return None
    try:
        return DoD.model_validate(json.loads(path.read_text(encoding="utf-8")))
    except Exception:  # noqa: BLE001 — a corrupt DoD is "no usable DoD"
        return None


# ---------------------------------------------------------------------------
# The verdict
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class GateResult:
    """What the gate decided, and everything it decided it from."""

    #: True when the job may end green.
    released: bool
    evidence: tuple[CheckEvidence, ...] = ()
    #: Check ids of RED blocking checks — the reason the gate holds.
    blocking_red: tuple[str, ...] = ()
    #: Check ids of red NON-blocking checks: reported, never gating.
    reported_red: tuple[str, ...] = ()
    #: Non-empty when the gate could not evaluate the DoD it was given.
    error: str = ""

    @property
    def blocked(self) -> bool:
        return not self.released

    def to_json(self) -> dict[str, Any]:
        return {
            "released": self.released,
            "blocking_red": list(self.blocking_red),
            "reported_red": list(self.reported_red),
            "error": self.error,
            "checks": [_evidence_json(e) for e in self.evidence],
        }


def _evidence_json(ev: CheckEvidence) -> dict[str, Any]:
    return {
        "check_id": ev.check_id,
        "kind": ev.kind,
        "source": ev.source,
        "blocking": ev.blocking,
        "status": ev.status,
        "reason": ev.reason,
        "command": ev.command,
        "exit_code": ev.exit_code,
        "duration_ms": ev.duration_ms,
        "output_tail": ev.output_tail,
    }


@dataclass
class _Tally:
    blocking_red: list[str] = field(default_factory=list)
    reported_red: list[str] = field(default_factory=list)


def evaluate_dod(
    dod: DoD,
    worktree_root: Path | str,
    *,
    timeout_sec: int = CHECK_TIMEOUT_DEFAULT_SEC,
    allowed_executables: frozenset[str] | set[str] | None = None,
) -> GateResult:
    """Run every check and apply the gate rule to the results.

    A check kind with no runner does not crash the gate — but it does not pass
    either. It is recorded as red with reason ``no_runner`` and, if it is
    blocking, it holds the job. Silence is the one thing this must never do.
    """
    evidence: list[CheckEvidence] = []
    tally = _Tally()

    for check in dod.checks:
        try:
            ev = run_check(check, worktree_root, timeout_sec=timeout_sec,
                           allowed_executables=allowed_executables)
        except UnsupportedCheckKindError as exc:
            ev = CheckEvidence(
                check_id=check.id, kind=check.kind, source=check.source,
                blocking=check.blocking, status="failed", reason=REASON_NO_RUNNER,
                command="", argv=(), cwd="", exit_code=None, duration_ms=0,
                output_tail=str(exc),
            )
        evidence.append(ev)
        if ev.status != STATUS_PASSED:
            (tally.blocking_red if ev.blocking else tally.reported_red).append(
                ev.check_id)

    return GateResult(
        released=not tally.blocking_red,
        evidence=tuple(evidence),
        blocking_red=tuple(tally.blocking_red),
        reported_red=tuple(tally.reported_red),
    )


def run_job_gate(
    job_id: str,
    worktree_root: Path | str,
    *,
    timeout_sec: int = CHECK_TIMEOUT_DEFAULT_SEC,
    allowed_executables: frozenset[str] | set[str] | None = None,
) -> GateResult | None:
    """Evaluate the gate for one job, persisting the result. None = no DoD.

    Returning None is what keeps this feature additive: a job without a stored
    DoD is not gated at all, and every caller behaves exactly as it did before.
    """
    if not dod_path(job_id).is_file():
        return None

    dod = load_dod(job_id)
    if dod is None:
        result = GateResult(
            released=False,
            error=f"the stored DoD at {DOD_FILENAME} could not be read; "
                  "a job is not released on an unreadable definition of done",
        )
    else:
        result = evaluate_dod(
            dod, worktree_root, timeout_sec=timeout_sec,
            allowed_executables=allowed_executables)

    save_gate_result(job_id, result)
    return result


def save_gate_result(job_id: str, result: GateResult) -> Path:
    path = result_path(job_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(result.to_json(), indent=2) + "\n", encoding="utf-8")
    return path


def load_gate_result(job_id: str) -> dict[str, Any] | None:
    """The last recorded gate run as plain data, or None.

    Plain data on purpose: the report and the CLI render the matrix, and
    neither needs to re-hydrate CheckEvidence objects to do it.
    """
    path = result_path(job_id)
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def gate_blocker(result: GateResult | None) -> str:
    """The single blocker line a held job carries, or "" when released."""
    if result is None or result.released:
        return ""
    if result.error:
        return f"{BLOCKER_PREFIX}:{result.error}"
    return f"{BLOCKER_PREFIX}:{','.join(result.blocking_red)}"


# ---------------------------------------------------------------------------
# The check matrix
# ---------------------------------------------------------------------------

MATRIX_HEADER = ("check", "kind", "blocking", "status", "reason", "duration")


def matrix_rows(result: GateResult | dict[str, Any] | None) -> list[tuple[str, ...]]:
    """The matrix as rows of strings, from a GateResult or its stored JSON."""
    if result is None:
        return []
    checks = (result.to_json() if isinstance(result, GateResult) else result).get(
        "checks") or []
    rows: list[tuple[str, ...]] = []
    for check in checks:
        if not isinstance(check, dict):
            continue
        rows.append((
            str(check.get("check_id", "")),
            str(check.get("kind", "")),
            "yes" if check.get("blocking") else "no",
            str(check.get("status", "")),
            str(check.get("reason", "") or "-"),
            f"{int(check.get('duration_ms', 0) or 0)}ms",
        ))
    return rows


def render_matrix(result: GateResult | dict[str, Any] | None) -> str:
    """The matrix as a markdown table — the same rows the CLI prints."""
    rows = matrix_rows(result)
    if not rows:
        return "No Definition of Done was run for this job."
    lines = ["| " + " | ".join(MATRIX_HEADER) + " |",
             "| " + " | ".join("---" for _ in MATRIX_HEADER) + " |"]
    lines += ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join(lines)
