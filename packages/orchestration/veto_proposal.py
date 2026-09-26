"""F027 T002 — the `replan_proposal` decision, its answer and the follow-up job a replan
creates (DECISION F027 D4).

Every veto files ONE `replan_proposal` decision, derived straight from the veto's own
control files and the answer files `task_veto` now also keeps (D4 (1)) — nothing here is
stored in `job.json`, and nothing here plans, approves or runs a job. The card offers a
two-option menu, `replan_follow_up` or `accept_reduced_scope`; `answer_replan_proposal`
is the one function that answers it, shared today by the CLI route and, from the next
round, the write door. An answer is itself a create-only control fact (D4 (3)) and a
replan mints an UNPLANNED follow-up `JobPlan` before it publishes that answer, then saves
the job after (D4 (4)) — so a repeated answer of the same option repairs a follow-up job
whose earlier save failed, exactly as a repeated veto repairs its own missing event.

Public API::

    DECISION_TYPE_REPLAN_PROPOSAL — str, the decision type this module derives
    replan_proposal_decisions(job, *, control_root_path=None) -> list[HumanDecision]
    answer_replan_proposal(job, decision_id, option, *, actor, control_root_path=None,
                           root=None) -> dict
    build_follow_up_job(job, entry, unreachable_ids, *, job_id) -> JobPlan
"""
from __future__ import annotations

import json as _json
from typing import Any

from packages.core.models import RunState
from packages.orchestration import task_veto as _tv
from packages.orchestration.decision_evidence import (
    DecisionEvidenceRef,
    DecisionEvidenceTriple,
    DecisionOptionOutcome,
)
from packages.orchestration.decision_queue import HumanDecision

__all__ = [
    "DECISION_TYPE_REPLAN_PROPOSAL",
    "replan_proposal_decisions",
    "answer_replan_proposal",
    "build_follow_up_job",
]

DECISION_TYPE_REPLAN_PROPOSAL = "replan_proposal"

#: The id namespace: `veto:<request id>` — the request id is the same one the veto's own
#: control file and `task_vetoed` event already carry, so the three never drift apart.
_ID_PREFIX = "veto:"


def _decision_id(request_id: str) -> str:
    return f"{_ID_PREFIX}{request_id}"


def _task_status_str(task: Any) -> str:
    status = getattr(task, "status", "")
    return status.value if hasattr(status, "value") else str(status)


def _qualifying_entries(job: Any, control_root_path: Any) -> list[Any]:
    """D4 (1)'s filter: one `vetoed_tasks` entry per card, whose task is still in the job
    with a status in `VETOABLE_TASK_STATUSES` or `vetoed`, and whose request id has no
    answer yet. Every other entry is either inert (the task moved on to some other status,
    or no longer exists) or already answered, and neither files a card."""
    entries = _tv.vetoed_tasks(job.job_id, control_root_path=control_root_path)
    answers = _tv.veto_answers(job.job_id, control_root_path=control_root_path)
    tasks_by_id = {t.task_id: t for t in job.tasks}
    out: list[Any] = []
    for entry in entries:
        if entry.request_id in answers:
            continue
        task = tasks_by_id.get(entry.task_id)
        if task is None:
            continue
        status = _task_status_str(task)
        if status not in _tv.VETOABLE_TASK_STATUSES and status != "vetoed":
            continue
        out.append(entry)
    return out


def _proposal_unreachable(job: Any, entry: Any, all_entries: list[Any]) -> list[str]:
    """`veto_unreachable` over this veto alone, without every task another entry of
    `vetoed_tasks` already holds — mirrors `task_veto._event_unreachable` exactly."""
    other_ids = {e.task_id for e in all_entries if e.task_id != entry.task_id}
    return [tid for tid in _tv.veto_unreachable(job.tasks, [entry.task_id])
            if tid not in other_ids]


def replan_proposal_decisions(job: Any, *, control_root_path: Any = None) -> list[HumanDecision]:
    """DECISION F027 D4 (1): one `replan_proposal` decision per qualifying veto entry."""
    all_entries = _tv.vetoed_tasks(job.job_id, control_root_path=control_root_path)
    qualifying = _qualifying_entries(job, control_root_path)
    job_id = str(getattr(job, "job_id", ""))
    tasks_by_id = {t.task_id: t for t in job.tasks}
    decisions: list[HumanDecision] = []

    for entry in qualifying:
        task = tasks_by_id.get(entry.task_id)
        title = task.title if task is not None else entry.task_id
        unreachable = _proposal_unreachable(job, entry, all_entries)
        count = len(unreachable)
        tail = (f" {count} downstream task{'s' if count != 1 else ''} cannot run."
                if count else "")
        summary = (
            f"You vetoed {title} — reason: {entry.reason}.{tail} "
            "Replan the remaining work as a follow-up job, or accept the reduced scope."
        )
        decision_id = _decision_id(entry.request_id)

        decisions.append(HumanDecision(
            id=decision_id,
            type=DECISION_TYPE_REPLAN_PROPOSAL,
            status="open",
            severity="blocker",
            source="task_veto",
            related_node_id=f"task:{entry.task_id[:8]}",
            related_intent_id="",
            related_file="",
            safe_summary=summary,
            next_actions=(
                f"remedy decision resolve {job_id[:8]} {decision_id} "
                f"--reason {_tv.REPLAN_FOLLOW_UP}",
                f"remedy decision resolve {job_id[:8]} {decision_id} "
                f"--reason {_tv.ACCEPT_REDUCED_SCOPE}",
            ),
            created_at=entry.requested_at,
            resolved_at=None,
            payload={
                "options": list(_tv.REPLAN_PROPOSAL_OPTIONS),
                "task_id": entry.task_id,
                "request_id": entry.request_id,
                "task_title": title,
                "reason": entry.reason,
                "actor": entry.actor,
                "requested_at": entry.requested_at,
                "unreachable_task_ids": unreachable,
            },
            evidence=DecisionEvidenceTriple(
                refs=(
                    DecisionEvidenceRef(
                        kind="decision",
                        target=entry.request_id,
                        label="the veto this proposal was filed for",
                    ),
                ),
                outcomes=(
                    DecisionOptionOutcome(
                        option=_tv.REPLAN_FOLLOW_UP,
                        expected_outcome=(
                            "An unplanned follow-up job is created carrying the vetoed "
                            "task's goal, the reason and the unreachable work forward, for "
                            "the operator to plan and run without the vetoed approach."
                        ),
                        downside=(
                            "Nothing in the follow-up job runs on its own: planning, "
                            "approving and launching it are still the operator's own steps."
                        ),
                    ),
                    DecisionOptionOutcome(
                        option=_tv.ACCEPT_REDUCED_SCOPE,
                        expected_outcome=(
                            "The job completes with the vetoed task and its unreachable "
                            "work left undone, and nothing further is created."
                        ),
                        downside=(
                            "The work the veto struck stays undone, and no follow-up exists "
                            "unless one is proposed separately."
                        ),
                    ),
                ),
            ),
        ))
    return decisions


# ---------------------------------------------------------------------------
# D4 (2) — the answer, shared by the CLI and (next round) the write door
# ---------------------------------------------------------------------------


def _refuse(code: str, detail: str, decision_id: str) -> dict[str, Any]:
    return {"outcome": "refused", "code": code, "detail": detail, "decision_id": decision_id}


def _ensure_follow_up_job(job: Any, entry: Any, unreachable: list[str], answer: Any,
                          root: Any) -> None:
    """D4 (4)'s repair half: build and save the follow-up job named by `answer` when it does
    not exist yet. A no-op for an accept, or for a replan whose follow-up is already saved."""
    if answer.option != _tv.REPLAN_FOLLOW_UP or not answer.follow_up_job_id:
        return
    from packages.orchestration.pingpong_job import load_job_plan, save_job_plan

    if load_job_plan(answer.follow_up_job_id, root) is not None:
        return
    follow_up = build_follow_up_job(job, entry, unreachable, job_id=answer.follow_up_job_id)
    save_job_plan(follow_up, root)


def _veto_proposal_answered_event_exists(job_id: str, request_id: str) -> bool | None:
    """Mirrors `task_veto._task_vetoed_event_exists` exactly: True/False, or None when the
    ledger could not be read at all — never mistaken for "no event"."""
    try:
        from packages.orchestration.data_paths import run_log_dir

        job_runs = run_log_dir(job_id)
        if not job_runs.is_dir():
            return False
        for jsonl in sorted(job_runs.glob("*.jsonl")):
            for line in jsonl.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                try:
                    raw = _json.loads(line)
                except ValueError:
                    continue
                if (raw.get("event") == "veto_proposal_answered"
                        and str(raw.get("job_id")) == job_id
                        and str((raw.get("metadata") or {}).get("request_id")) == request_id):
                    return True
        return False
    except OSError:
        return None


def _write_veto_proposal_answered_event(job: Any, entry: Any, answer: Any) -> None:
    from packages.orchestration.run_log import RunLogWriter

    writer = RunLogWriter(job.job_id)
    writer.log(
        "veto_proposal_answered",
        outcome=answer.option,
        scope="task",
        task_id=entry.task_id,
        request_id=entry.request_id,
        option=answer.option,
        actor=answer.actor,
        answered_at=answer.answered_at,
        follow_up_job_id=answer.follow_up_job_id,
    )


def _maybe_repair_veto_proposal_answered_event(job: Any, entry: Any, answer: Any) -> None:
    already = _veto_proposal_answered_event_exists(job.job_id, entry.request_id)
    if already is not None and not already:
        _write_veto_proposal_answered_event(job, entry, answer)


def answer_replan_proposal(job: Any, decision_id: str, option: str, *, actor: str,
                           control_root_path: Any = None, root: Any = None) -> dict[str, Any]:
    """D4 (2) to (4): answer one `replan_proposal` decision of `job`. Never raises for a
    refusal: checks in order the id, the option and an existing answer, and answers
    `{"outcome": "refused", "code", "detail", "decision_id"}` for any of the three —
    `already_answered` also carries the recorded `option` and `follow_up_job_id`. On
    success it answers `{"outcome": "answered", "decision_id", "option",
    "follow_up_job_id"}`, the last "" for an accept.
    """
    if not str(decision_id).startswith(_ID_PREFIX):
        return _refuse("unknown_decision",
                       f"{decision_id!r} does not name a veto of this job", decision_id)
    request_id = str(decision_id)[len(_ID_PREFIX):]

    all_entries = _tv.vetoed_tasks(job.job_id, control_root_path=control_root_path)
    entry = next((e for e in all_entries if e.request_id == request_id), None)
    if entry is None:
        return _refuse("unknown_decision",
                       f"{decision_id!r} does not name a veto of this job", decision_id)

    if option not in _tv.REPLAN_PROPOSAL_OPTIONS:
        return _refuse(
            "invalid_option",
            f"option must be one of {', '.join(_tv.REPLAN_PROPOSAL_OPTIONS)}", decision_id)

    unreachable = _proposal_unreachable(job, entry, all_entries)
    existing = _tv.veto_answers(job.job_id, control_root_path=control_root_path).get(request_id)

    if existing is None:
        # D4 (4): the follow-up id is minted and RECORDED IN THE ANSWER before the job
        # carrying it is ever saved — see `_ensure_follow_up_job` below.
        follow_up_job_id = ""
        if option == _tv.REPLAN_FOLLOW_UP:
            from packages.orchestration.data_paths import mint_job_id
            follow_up_job_id = mint_job_id()
        answer, _created = _tv.record_veto_answer(
            job.job_id, request_id, entry.task_id, option, actor, follow_up_job_id,
            control_root_path=control_root_path)
    else:
        answer = existing

    _ensure_follow_up_job(job, entry, unreachable, answer, root)
    _maybe_repair_veto_proposal_answered_event(job, entry, answer)

    if existing is not None:
        return {
            "outcome": "refused", "code": "already_answered", "decision_id": decision_id,
            "option": answer.option, "follow_up_job_id": answer.follow_up_job_id,
        }
    return {
        "outcome": "answered", "decision_id": decision_id, "option": answer.option,
        "follow_up_job_id": answer.follow_up_job_id,
    }


# ---------------------------------------------------------------------------
# D4 (4) — the follow-up job: unplanned, no tasks, never run by this module
# ---------------------------------------------------------------------------


def build_follow_up_job(job: Any, entry: Any, unreachable_ids: list[str], *,
                        job_id: str) -> Any:
    """The D4 (4) follow-up `JobPlan`: copies the original's repository and project, has no
    tasks and the state `pending`, and its goal names the original job, the vetoed task's
    title (which already carries its goal — `job_plan.map_task_plan_to_tasks` titles a task
    `"<title>: <goal>"`), the reason verbatim and each unreachable task's title. Nothing here
    plans, approves, runs or saves the ORIGINAL job's record — only the returned follow-up.
    """
    from packages.orchestration.pingpong_job import JobPlan

    tasks_by_id = {t.task_id: t for t in job.tasks}
    vetoed_task = tasks_by_id.get(entry.task_id)
    vetoed_title = vetoed_task.title if vetoed_task is not None else entry.task_id

    lines = [
        f"Replan the work vetoed on job {job.job_id[:8]}.",
        f"Vetoed task: {vetoed_title}",
        f"Reason: {entry.reason}",
    ]
    if unreachable_ids:
        lines.append("Also replan the following work, unreachable behind that veto:")
        for tid in unreachable_ids:
            other = tasks_by_id.get(tid)
            lines.append(f"- {other.title if other is not None else tid}")
    lines.append("Plan this work again without the vetoed approach.")
    goal = "\n".join(lines)

    return JobPlan(
        job_id=job_id,
        repo_path=job.repo_path,
        project_id=job.project_id,
        state=RunState.PENDING,
        tasks=[],
        job_title=f"Replan after veto of {vetoed_title}",
        user_prompt=goal,
        mission=goal,
        metadata={
            "replan_of": {
                "job_id": job.job_id,
                "task_id": entry.task_id,
                "request_id": entry.request_id,
            },
        },
    )
