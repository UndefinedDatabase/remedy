"""Decision group command handlers (human decision queue)."""

from __future__ import annotations

import json as _json
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from packages.orchestration.data_paths import resolve_job_id

if TYPE_CHECKING:
    import argparse

#: F051 task-decision namespace.  Mirrors escalation.DECISION_ID_PREFIX, kept
#: as a literal here so this module's dispatch reads like the ``sr:``/``fp:``
#: branches next to it.
_ESCALATION_PREFIX = "td:"


def _load_job_events(job_id_str: str):
    """Load job and events. Returns (job, events, job_id_str)."""
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.storage import JobNotFoundError, load_job
    from packages.orchestration.timeline import load_run_events

    job_id = resolve_job_id(job_id_str)
    try:
        job = load_job(job_id)
    except JobNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    data_dir = resolve_data_root()
    events = load_run_events(data_dir, job_id)
    return job, events, job_id_str


def _cmd_decision_list(
    job_id_str: str,
    *,
    json_output: bool = False,
    sort: str | None = None,
    desc: bool = False,
    since: str | None = None,
    until: str | None = None,
    limit: str | None = None,
) -> None:
    from packages.orchestration.decision_queue import export_decision_json, list_decisions
    from packages.orchestration.list_options import ListOptionError, apply_list_options

    job, events, jid = _load_job_events(job_id_str)
    decisions = list_decisions(job, events)
    try:
        decisions = apply_list_options(
            decisions,
            sort=sort, desc=desc, since=since, until=until, limit=limit,
            sort_fields={
                "created_at": lambda d: d.created_at,
                "status": lambda d: d.status,
                "severity": lambda d: d.severity,
            },
            default_sort_field="created_at",
            date_getter=lambda d: d.created_at or None,
        )
    except ListOptionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if json_output:
        print(_json.dumps({
            "version": 1,
            "job_id": jid,
            "decisions": [export_decision_json(d) for d in decisions],
        }, sort_keys=True))
    else:
        if not decisions:
            print(f"No pending decisions for job {jid[:8]}.")
            return
        for d in decisions:
            status_mark = "[open]" if d.status == "open" else "[resolved]"
            resolved_str = f", resolved={d.resolved_at}" if d.resolved_at else ""
            print(f"  {d.type} {status_mark} ({d.severity}): {d.safe_summary}  (id={d.id}, created={d.created_at}{resolved_str})")


def _cmd_decision_show(job_id_str: str, decision_id: str, *, json_output: bool = False) -> None:
    from packages.orchestration.decision_queue import export_decision_json, get_decision

    job, events, jid = _load_job_events(job_id_str)
    d = get_decision(job, events, decision_id)

    if d is None:
        print(f"Error: decision not found: {decision_id}", file=sys.stderr)
        sys.exit(1)

    if json_output:
        print(_json.dumps({
            "version": 1,
            "job_id": jid,
            "decision": export_decision_json(d),
        }, sort_keys=True))
    else:
        print(f"Decision: {d.id}")
        print(f"  Type: {d.type}")
        print(f"  Status: {d.status}")
        print(f"  Severity: {d.severity}")
        print(f"  Summary: {d.safe_summary}")
        for q in d.payload.get("clarifications", []):
            print(f"  Question {q.get('id', '')}: {q.get('question', '')}")
            print(f"    Default: {q.get('default_answer', '')}")
            print(f"    Impact: {q.get('impact', '')}")
        offer = d.payload.get("mission_offer")
        if offer:
            # F056: the default is printed because it is what happens when the
            # operator says nothing — silence must never read as consent.
            print(f"  Question mission: {offer.get('question', '')}")
            print(f"    Default: {offer.get('default', 'no')} "
                  f"(add --as-mission to opt in)")
        if d.next_actions:
            print("  Next actions:")
            for a in d.next_actions:
                print(f"    - {a}")


class AnswerParseError(ValueError):
    """A ``--answer`` option could not be applied to the bundled questions."""


def parse_answer_options(
    raw: list[str] | None,
    questions: list[dict[str, str]],
) -> dict[str, str]:
    """Parse repeatable ``--answer q1=text`` options against open questions.

    Answering a subset is valid — every unanswered question falls back to
    its documented default at approval time. An unknown or duplicated id,
    or a malformed pair, is a spec error and raises AnswerParseError.
    """
    known = [str(q.get("id", "")) for q in questions]
    answers: dict[str, str] = {}
    for item in raw or []:
        text = str(item)
        if "=" not in text:
            raise AnswerParseError(
                f"malformed --answer {text!r}: expected <question-id>=<answer>, "
                'e.g. --answer q1="use PostgreSQL"')
        qid, _, value = text.partition("=")
        qid = qid.strip()
        if not qid:
            raise AnswerParseError(
                f"malformed --answer {text!r}: missing question id before '='")
        if qid not in known:
            listed = ", ".join(known) if known else "(none — the plan has no open questions)"
            raise AnswerParseError(
                f"unknown question id {qid!r}. Open questions: {listed}")
        if qid in answers:
            raise AnswerParseError(f"duplicate --answer for question id {qid!r}")
        answers[qid] = value
    return answers


def _create_mission_for_job(job: Any) -> None:
    """F056: the plan-approval opt-in, taken.  Only ever reached via --as-mission.

    Creates the mission and links this job as its ``initial`` job.  A failure
    here is reported and exits non-zero rather than leaving an approved plan
    with a half-built mission behind it.
    """
    from packages.orchestration.mission_state import (
        MISSION_ROLE_INITIAL,
        MissionError,
        create_mission,
        link_job_to_mission,
        mission_for_job,
    )

    project_id = str(getattr(job, "project_id", "") or "")
    if not project_id:
        print("Error: this job has no project, so it cannot start a mission.\n"
              "  Register one with: remedy init", file=sys.stderr)
        sys.exit(1)

    existing = mission_for_job(str(job.id))
    if existing is not None:
        print(f"Error: job {str(job.id)[:8]} already belongs to mission "
              f"{existing.id[:12]} — one job, one mission.", file=sys.stderr)
        sys.exit(1)

    intake = getattr(job, "intake", None)
    goal = ""
    if isinstance(intake, dict):
        goal = str(intake.get("goal", "") or "")
    goal = goal or str(getattr(job, "mission", "") or "") or str(job.name)

    try:
        mission = create_mission(project_id, goal)
        link_job_to_mission(project_id, mission.id, str(job.id),
                            MISSION_ROLE_INITIAL)
    except MissionError as exc:
        print(f"Error: could not start the mission: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Mission {mission.id} started for this goal.")
    print(f"  Goal:  {mission.goal}")
    print(f"  Chain: remedy mission show {mission.id[:12]}")


def _cmd_decision_resolve(
    job_id_str: str,
    decision_id: str,
    *,
    reason: str | None = None,
    answer: list[str] | None = None,
    as_mission: bool = False,
) -> None:
    # ``--answer`` bundles the flight plan's clarification questions; a task
    # decision carries exactly one question, answered through --reason.
    if answer and not decision_id.startswith("fp:"):
        print(
            f"Error: --answer is only valid for the flight-plan approval "
            f"decision, not {decision_id!r}.",
            file=sys.stderr)
        sys.exit(1)
    # F056: same rule for the mission opt-in — it belongs to the plan approval.
    if as_mission and not decision_id.startswith("fp:"):
        print(
            f"Error: --as-mission is only valid for the flight-plan approval "
            f"decision, not {decision_id!r}.",
            file=sys.stderr)
        sys.exit(1)

    # Decisions are derived — resolve the underlying record if possible
    if decision_id.startswith("sr:"):
        from packages.orchestration.stop_reasons import resolve_stop_reason
        stop_id = decision_id[3:]
        sr = resolve_stop_reason(job_id_str, stop_id, reason or "manually resolved")
        if sr is None:
            print(f"Error: stop reason not found: {stop_id}", file=sys.stderr)
            sys.exit(1)
        print(f"Resolved stop reason: {sr.id[:8]} ({sr.reason_code})")
    elif decision_id.startswith(_ESCALATION_PREFIX):
        # F051: a task asked a question mid-run.  ``--reason`` carries the
        # ANSWER, and the same command that the status/report views print is the
        # one that lands here — no separate answer command exists.
        from datetime import datetime, timezone

        from packages.orchestration.data_paths import resolve_job_id as _rji
        from packages.orchestration.escalation import (
            answer_task_decision,
            find_task_decision,
        )
        from packages.orchestration.storage import JobNotFoundError, load_job, save_job

        job_id = _rji(job_id_str)
        try:
            job = load_job(job_id)
        except JobNotFoundError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)

        record = find_task_decision(job, decision_id)
        if record is None:
            print(f"Error: decision not found: {decision_id}", file=sys.stderr)
            sys.exit(1)

        answer_text = (reason or "").strip() or str(record.get("safe_default", ""))
        if not answer_text:
            print(
                "Error: --reason carries the answer for a task decision, and "
                "this one has no safe default to fall back on.\n"
                f"  remedy decision resolve {job_id_str} {decision_id} "
                '--reason "<your answer>"',
                file=sys.stderr,
            )
            sys.exit(1)

        answered = answer_task_decision(
            job, decision_id, answer=answer_text,
            now=datetime.now(timezone.utc))
        if answered is None:
            # Answers are written once — say which answer already stands.
            print(
                f"Error: decision {decision_id} is already answered "
                f"({record.get('answer_source', '')}): {record.get('answer', '')}",
                file=sys.stderr)
            sys.exit(1)

        save_job(job)
        print(f"Answered {decision_id} for job {job_id_str}: {answered['answer']}")
        for ref in answered.get("cross_references", []):
            print(f"  Same question also asked as: {ref}")
        print(f"Resume the run: remedy job run-loop {job_id_str} --json")
    elif decision_id.startswith("fp:"):
        from packages.orchestration.data_paths import resolve_job_id as _rji
        from packages.orchestration.storage import JobNotFoundError, load_job

        job_id = _rji(job_id_str)
        try:
            job = load_job(job_id)
        except JobNotFoundError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)

        from packages.orchestration.flight_plan import (
            clarifications_already_resolved,
            open_clarification_questions,
            resolve_flight_plan_approval,
        )

        fp = getattr(job, "flight_plan", None)
        if not isinstance(fp, dict) or fp.get("_approval") != "pending":
            # Answers are asked once and written once. A late one is a
            # mistake worth naming, not a generic "nothing pending".
            if answer and isinstance(fp, dict) and clarifications_already_resolved(
                    fp.get("clarifications_resolved")):
                print(
                    "Error: clarifications already resolved for this job — "
                    "answers are immutable. Replan to ask again: "
                    f"remedy do replan {job_id_str}",
                    file=sys.stderr)
                sys.exit(1)
            print("Error: no pending flight plan approval for this job.", file=sys.stderr)
            sys.exit(1)

        if reason not in ("approve", "reject"):
            print(
                "Error: --reason must be 'approve' or 'reject'.\n"
                f"  remedy decision resolve {job_id_str} fp:approval --reason approve\n"
                f"  remedy decision resolve {job_id_str} fp:approval --reason reject",
                file=sys.stderr,
            )
            sys.exit(1)

        questions = open_clarification_questions(fp.get("clarifications_resolved"))
        if answer and reason != "approve":
            print(
                "Error: --answer applies only when approving the plan.",
                file=sys.stderr)
            sys.exit(1)
        if as_mission and reason != "approve":
            print(
                "Error: --as-mission applies only when approving the plan.",
                file=sys.stderr)
            sys.exit(1)
        try:
            answers = parse_answer_options(answer, questions)
        except AnswerParseError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)

        if reason == "approve":
            log_path = resolve_flight_plan_approval(
                job, reason="approve", answers=answers, questions=questions)
            print(f"Flight plan approved for job {job_id_str}.")
            for q in questions:
                qid = q["id"]
                source = "human" if qid in answers else "default"
                print(f"  {qid} ({source}): "
                      f"{answers.get(qid, q['default_answer'])}")
            print(f"Assumption log: {log_path}")
            # F056: last, and only on an explicit --as-mission. An approval
            # without the flag leaves no mission behind — the default is NO.
            if as_mission:
                _create_mission_for_job(job)
        else:
            resolve_flight_plan_approval(
                job, reason="reject", answers=answers, questions=questions)
            print(f"Flight plan rejected for job {job_id_str}.")
            print(f"Run: remedy do replan {job_id_str}")
    else:
        print(f"Decision '{decision_id}' is derived and cannot be directly resolved.", file=sys.stderr)
        print("Resolve the underlying record (patch intent, test, etc.) instead.", file=sys.stderr)
        sys.exit(1)


def _cmd_decision_explain(job_id_str: str) -> None:
    from packages.orchestration.decision_queue import explain_decisions

    job, events, _jid = _load_job_events(job_id_str)
    print(explain_decisions(job, events))


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "decision.list": lambda args: _cmd_decision_list(
        args.job_id,
        json_output=getattr(args, "json", False),
        sort=getattr(args, "sort", None),
        desc=getattr(args, "desc", False),
        since=getattr(args, "since", None),
        until=getattr(args, "until", None),
        limit=getattr(args, "limit", None),
    ),
    "decision.show": lambda args: _cmd_decision_show(
        args.job_id,
        args.decision_id,
        json_output=getattr(args, "json", False),
    ),
    "decision.resolve": lambda args: _cmd_decision_resolve(
        args.job_id,
        args.decision_id,
        reason=getattr(args, "reason", None),
        answer=getattr(args, "answer", None),
        as_mission=getattr(args, "as_mission", False),
    ),
    "decision.explain": lambda args: _cmd_decision_explain(args.job_id),
}
