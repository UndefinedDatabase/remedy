"""Operator amendment amend1024-one-real-order, Part B — the scope decision: one job, or several?

Before any milestone is planned, the planner (claude-cli unless the walk names another) reads the
order, the repository's tracked paths (at most `SCOPE_DECISION_MAX_PATHS` lines, paths only) and
one question, and answers one fixed JSON object: `single_job` (true or false), `files` (the files
the order likely touches) and `reason` (one German sentence). ONE JOB IS THE DEFAULT: several jobs
only when the planner answers `single_job: false` WITH a reason, and an order whose header says
`shape: single-job` is one job without asking. The answer is kept as evidence
(`SCOPE_DECISION_FILENAME` in each job's evidence folder).

The regex lanes of `do_lane.py` decide only when there is no answer: the planner is not reachable,
its call fails, or what it wrote is not the object after one parse retry. Remedy deliberately does
not guess a size from an unusable answer.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any, ClassVar

from pydantic import Field

from packages.orchestration.structured_base import _Strict

#: The most tracked paths the scope question shows; a larger repository is cut and says so.
SCOPE_DECISION_MAX_PATHS = 2000
#: The evidence file each job of a walk keeps the scope decision in.
SCOPE_DECISION_FILENAME = "scope_decision.json"

#: What the decision came to: the planner's one job, its several jobs, or the regex fallback.
SCOPE_ONE_JOB = "one_job"
SCOPE_SEVERAL_JOBS = "several_jobs"
SCOPE_REGEX_FALLBACK = "regex_fallback"


class OrderScopeDecision(_Strict):
    """The planner's answer to the scope question: exactly these three fields."""

    SCHEMA_V: ClassVar[str] = "order_scope_decision_v1"
    single_job: bool
    files: list[str] = Field(default_factory=list)
    reason: str = ""


# WHY: the question is the whole contract with the planner, so it is spelled once, in English
# like every planner prompt, and asks for the reason in German as the operator ordered.
_SCOPE_QUESTION = (
    "You decide the SIZE of a software change before anyone plans it. Read the order and the "
    "repository's file list. Is this ONE job (one coherent change a single developer makes in one "
    "sitting, even across several files), or does it really need SEVERAL separate jobs that must "
    "land one after another? Prefer one job: answer several only when the order names independent "
    "deliverables that cannot be built and reviewed together. Answer with one JSON object: "
    "single_job (true or false), files (the repository paths the change most likely touches), "
    "reason (exactly one sentence in German saying why)."
)


def scope_decision_prompt(order: str, tracked_files: list[str]) -> str:
    """The scope question over ORDER and at most `SCOPE_DECISION_MAX_PATHS` of TRACKED_FILES."""
    shown = tracked_files[:SCOPE_DECISION_MAX_PATHS]
    cut = len(tracked_files) - len(shown)
    listing = "\n".join(shown) if shown else "(the repository tracks no file yet)"
    if cut:
        listing += f"\n... and {cut} more paths not shown"
    return f"{_SCOPE_QUESTION}\n\nORDER:\n{order.strip()}\n\nREPOSITORY FILES:\n{listing}"


def decide_order_scope(
    order: str, tracked_files: list[str], *,
    provider: str | None = None, model: str | None = None,
    call_fn: Callable[[str, int], str] | None = None,
) -> dict[str, Any]:
    """Ask the planner the scope question and return the decision record kept as evidence.

    CALL_FN defaults to the planner `make_structured_call_fn` builds for PROVIDER and MODEL. The
    record's `decided` is `SCOPE_ONE_JOB` unless the planner answered `single_job: false` with a
    non-empty reason (`SCOPE_SEVERAL_JOBS`); without an answer it is `SCOPE_REGEX_FALLBACK` and
    `outcome` says why (`planner_unreachable`, `planner_failed`, `answer_invalid`).
    """
    from packages.orchestration.intake import make_structured_call_fn, resolve_planner_target
    from packages.orchestration.structured_outputs import run_structured_call

    planner, _model = resolve_planner_target(provider, model)
    record: dict[str, Any] = {
        "schema_v": OrderScopeDecision.SCHEMA_V, "planner": planner,
        "paths_shown": min(len(tracked_files), SCOPE_DECISION_MAX_PATHS),
        "paths_total": len(tracked_files),
        "single_job": None, "files": [], "reason": "", "detail": "",
    }
    if call_fn is None:
        call_fn = make_structured_call_fn(OrderScopeDecision, provider=provider, model=model)
    if call_fn is None:
        return {**record, "outcome": "planner_unreachable", "decided": SCOPE_REGEX_FALLBACK,
                "detail": f"the planner {planner} is not reachable"}
    record["model"] = getattr(call_fn, "resolved_model", None)
    try:
        outcome = run_structured_call(OrderScopeDecision, scope_decision_prompt(order, tracked_files),
                                      call_fn, allow_parse_retry=True)
    except (RuntimeError, OSError, ValueError, ImportError) as exc:   # no answer; the regex lanes decide
        return {**record, "outcome": "planner_failed", "decided": SCOPE_REGEX_FALLBACK,
                "detail": f"{type(exc).__name__}: {exc}"[:500]}
    record["calls"] = outcome.calls
    if not outcome.ok or not isinstance(outcome.value, OrderScopeDecision):
        return {**record, "outcome": "answer_invalid", "decided": SCOPE_REGEX_FALLBACK,
                "detail": outcome.hint[:500]}
    answer = outcome.value
    reason = answer.reason.strip()
    several = not answer.single_job and bool(reason)
    return {**record, "outcome": "answered", "single_job": answer.single_job,
            "files": [str(path) for path in answer.files], "reason": reason,
            "decided": SCOPE_SEVERAL_JOBS if several else SCOPE_ONE_JOB,
            "detail": "" if several or answer.single_job else
            "single_job false without a reason, so the default, one job, holds"}


def record_scope_decision(record: dict[str, Any] | None, job_id: str) -> None:
    """Write RECORD as `SCOPE_DECISION_FILENAME` into JOB_ID's evidence folder; nothing for None."""
    if not record:
        return
    from packages.orchestration.data_paths import job_evidence_dir

    folder = Path(job_evidence_dir(job_id))
    folder.mkdir(parents=True, exist_ok=True)
    (folder / SCOPE_DECISION_FILENAME).write_text(
        json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")



# WHY: a client shows why an order became one job or several without reading the evidence folder.
def story_scope(job_id: str) -> dict[str, Any] | None:
    """JOB_ID's scope decision as a story carries it: `single_job` (null when the regex lanes
    decided), `files`, `reason` and `decided`; None when the job keeps no readable decision."""
    from packages.orchestration.data_paths import job_evidence_dir

    try:
        record = json.loads((Path(job_evidence_dir(job_id)) / SCOPE_DECISION_FILENAME).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(record, dict):
        return None
    single = record.get("single_job")
    files = record.get("files")
    return {"single_job": single if isinstance(single, bool) else None,
            "files": [str(path) for path in files] if isinstance(files, list) else [],
            "reason": str(record.get("reason") or ""), "decided": str(record.get("decided") or "") or None}
