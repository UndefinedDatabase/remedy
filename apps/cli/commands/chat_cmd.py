"""Handler for ``remedy chat`` — send a steering message to a running job (F264 T001).

`remedy chat <job_id> "<message>"` hands one free-form sentence to the job. Nothing reaches
into a model call in flight: the message is written as a sealed record under the job's
evidence and certified into its run log, and the run reads it at its next safe point (T002).
The command goes through `steering.record_steering_message`, the one place a message is
accepted, which the cockpit's input field uses too. It writes no file in the repository.

`remedy chat show <job_id>` (T003) lists the job's messages with each acknowledgement — the task
round that took it in and what was understood — read from the same run-log events the cockpit's
stream carries, and says plainly when a message is still waiting or was never taken in.

`remedy chat ask <job_id> "<text>" [--task <task id>] [--yes] [--json]` (F038 T003, DECISION
F038 D10) is one line of the chat: `text` runs through `run_chat_turn`, and a question answers
with its scope, its checked answer and its numbered evidence, while an action prints a card and
sends it through the job's running cockpit only once it is confirmable and confirmed, by `--yes`
or a `y` typed at a terminal prompt. Nothing is sent otherwise, and the exit code stays 0 either
way; only a task id naming no task of the job, an absent or unreachable cockpit, or a cockpit
that refuses the card answer above the floor.
"""
from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from apps.cli.json_envelope import emit_ok, fail

if TYPE_CHECKING:
    import argparse
    from collections.abc import Callable

#: The contract's exit code for a job whose record is unreadable or which has ended
#: (DECISION F283 D12): the invocation is well formed, the job cannot take a message.
EXIT_NOT_READY = 3


def _cmd_chat_send(job_id: str, message: str, *, json_output: bool = False) -> None:
    """Record ``message`` for the job. Exits 2 on an unusable message, 3 on an ended job."""
    from apps.cli.job_id_arg import resolve_job_id_or_fail
    from packages.orchestration.pingpong_job import load_job_plan
    from packages.orchestration.steering import (
        SteeringError,
        SteeringWriteError,
        normalize_steering_text,
        record_steering_message,
    )

    try:
        normalize_steering_text(message)
    except SteeringError as exc:
        fail("invalid_message", f"The message was not sent: {exc}.", json_output=json_output,
             exit_code=2)
    full_id = resolve_job_id_or_fail((job_id or "").strip(), json_output=json_output,
                                     job_id=job_id)
    job = load_job_plan(full_id)
    if job is None:
        fail("job_not_found", f"The record of job {full_id} cannot be read.",
             json_output=json_output, exit_code=EXIT_NOT_READY, job_id=full_id)
    state = job.state.value if hasattr(job.state, "value") else str(job.state)
    try:
        record = record_steering_message(job.job_id, message, job_state=state, channel="cli")
    except SteeringWriteError as exc:
        fail("steering_write_failed", f"The message could not be recorded: {exc}.",
             json_output=json_output, job_id=job.job_id)
    except SteeringError as exc:
        fail("job_not_steerable", f"The message was not sent: {exc}.",
             json_output=json_output, exit_code=EXIT_NOT_READY, job_id=job.job_id)

    if json_output:
        emit_ok(job_id=job.job_id, message_id=record["message_id"],
                received_at=record["received_at"], record_sha256=record["record_sha256"])
        return
    print(f"Message {record['message_id']} recorded for job {job.job_id}.")
    print("The job reads it at its next safe point; nothing interrupts a model call in flight.")


#: What each status says to the operator, in plain words (T003, DECISION F264 D6).
_STATUS_WORDS = {
    "waiting": "waiting — the job has not reached a safe point since it arrived",
    "not_taken_in": "not taken in — the job ended before it reached another round",
}


def _cmd_chat_show(job_id: str, *, json_output: bool = False) -> None:
    """List the job's steering messages with each acknowledgement. Exits 3 on an unreadable job."""
    from apps.cli.job_id_arg import resolve_job_id_or_fail
    from packages.orchestration.pingpong_job import load_job_plan
    from packages.orchestration.steering import SteeringError, steering_overview

    full_id = resolve_job_id_or_fail((job_id or "").strip(), json_output=json_output,
                                     job_id=job_id)
    job = load_job_plan(full_id)
    if job is None:
        fail("job_not_found", f"The record of job {full_id} cannot be read.",
             json_output=json_output, exit_code=EXIT_NOT_READY, job_id=full_id)
    state = job.state.value if hasattr(job.state, "value") else str(job.state)
    # F030 T002, DECISION F030 D2 (6): the job's own task statuses, so the overview can tell
    # a note whose task has finished from one still waiting for its next round.
    task_statuses = {
        str(t.task_id): (t.status.value if hasattr(t.status, "value") else str(t.status))
        for t in job.tasks
    }
    try:
        rows = steering_overview(job.job_id, state, task_statuses=task_statuses)
    except SteeringError as exc:
        fail("steering_record_damaged", f"The job's steering records cannot be trusted: {exc}.",
             json_output=json_output, job_id=job.job_id)

    if json_output:
        emit_ok(job_id=job.job_id, job_status=state, messages=rows)
        return
    if not rows:
        print(f"Job {job.job_id} has no steering messages.")
        return
    print(f"Job {job.job_id} — {state}")
    for row in rows:
        addressed_to = row.get("addressed_to", "")
        if addressed_to:
            print(f"{row['message_id']}  {row['received_at']}  via {row['channel']} to task "
                  f"{addressed_to}: {row['text']}")
        else:
            print(f"{row['message_id']}  {row['received_at']}  via {row['channel']}: "
                  f"{row['text']}")
        if row["status"] == "acknowledged":
            print(f"  taken in at round {row['round_number']} of task {row['task_id']}: "
                  f"{row['understood']}")
        elif addressed_to and row["status"] == "waiting":
            print(f"  waiting — task {addressed_to} has not started a round since it arrived")
        elif addressed_to and row["status"] == "not_taken_in":
            print(f"  not taken in — task {addressed_to} finished without starting another round")
        else:
            print(f"  {_STATUS_WORDS[row['status']]}")


def _chat_stdin_is_a_tty() -> bool:
    """Whether there is an operator on the other end who could answer the card's confirm
    prompt. A module-level function, mirroring `cost_preview_confirm._stdin_is_a_tty`, so a
    test can replace it rather than faking a real terminal."""
    return sys.stdin.isatty()


def _render_chat_answer_turn(job_id: str, turn: object, *, json_output: bool) -> None:
    """Print or emit a QUESTION turn's checked answer and its numbered evidence (S5)."""
    from packages.orchestration.chat_answer import render_chat_answer

    answer = turn.answer
    evidence = turn.evidence
    if json_output:
        emit_ok(
            job_id=job_id, kind="answer", scope=answer.scope, subject=answer.subject,
            generator=answer.generator,
            sentences=[
                {"text": sentence.text, "citations": list(sentence.citations),
                 "supported": sentence.supported}
                for sentence in answer.sentences
            ],
            evidence=[
                {"number": number, "kind": item.kind, "ref": item.ref}
                for number, item in enumerate(evidence.items, start=1)
            ],
            omitted=evidence.omitted,
        )
        return
    subject = answer.subject or "no registered project"
    print(f"Scope: {answer.scope} {subject}")
    print(render_chat_answer(answer))
    for number, item in enumerate(evidence.items, start=1):
        print(f"[{number}] {item.kind} {item.ref}")


def _send_chat_card(job: object, card: object, *, yes: bool, json_output: bool) -> None:
    """Print a CARD turn's title and lines (S6), and send it through the job's running
    cockpit only once it is confirmable and confirmed by `--yes` or a typed `y`."""
    import secrets

    human = sys.stderr if json_output else sys.stdout
    print(card.title, file=human)
    for line in card.lines:
        print(f"  {line}", file=human)

    sent = False
    door_body: dict = {}
    not_sent_reason = ""
    outcome = ""

    if not card.confirmable:
        not_sent_reason = "the card is not confirmable"
    elif not yes and not _chat_stdin_is_a_tty():
        not_sent_reason = (
            "standard input is not a terminal, so there is nobody to confirm; "
            "pass --yes to send it without a prompt"
        )
    else:
        confirmed = yes
        if not confirmed:
            answer = input("Send it? [y/N] ")
            confirmed = answer.strip().lower() in ("y", "yes")
        if not confirmed:
            not_sent_reason = "not confirmed"
        else:
            from apps.cli.commands.ui import live_ui_session_for_job
            from packages.orchestration.chat_door import send_card_through_door

            session = live_ui_session_for_job(job.job_id)
            if session is None:
                fail(
                    "cockpit_not_running",
                    f"No cockpit is running for job {job.job_id}. Start one with: "
                    f"remedy ui start {job.job_id}.",
                    json_output=json_output, exit_code=3, job_id=job.job_id,
                )
            try:
                door_answer = send_card_through_door(
                    card, job_id=job.job_id, client_nonce="chat-" + secrets.token_hex(8),
                    port=int(session["port"]), token=str(session["token"]),
                )
            except OSError as exc:
                fail(
                    "cockpit_unreachable", f"The cockpit could not be reached: {exc}.",
                    json_output=json_output, exit_code=3, job_id=job.job_id,
                )
            if not door_answer.accepted:
                fail(
                    "door_refused",
                    f"The cockpit refused the card (status {door_answer.status}): "
                    f"{door_answer.body.get('error', '')}.",
                    json_output=json_output, exit_code=1, job_id=job.job_id,
                )
            sent = True
            door_body = door_answer.body
            outcome = door_body.get("outcome", "")

    if json_output:
        emit_ok(
            job_id=job.job_id, kind="card", verb=card.verb, title=card.title,
            lines=list(card.lines), confirmable=card.confirmable, sent=sent,
            door=door_body, not_sent_reason=not_sent_reason,
        )
        return
    if sent:
        print(f"Sent: {card.verb}. The cockpit answered: {outcome}.")
    else:
        print(f"Not sent: {not_sent_reason}.")


def _cmd_chat_ask(
    job_id: str, text: str, *, task_id: str = "", yes: bool = False, json_output: bool = False,
) -> None:
    """Run one chat turn for `job_id`: a question is answered from its evidence, an action
    becomes a card sent through the job's running cockpit once confirmed (DECISION F038 D10).

    Resolves the job exactly as `_cmd_chat_send` does — an unreadable record exits
    `EXIT_NOT_READY` — then runs `run_chat_turn`; a `task_id` naming no task of the job raises
    `ChatTurnError` before anything else is read, and exits 2 (`invalid_task`).
    """
    from apps.cli.job_id_arg import resolve_job_id_or_fail
    from packages.orchestration.chat_turn import CHAT_TURN_ANSWER, ChatTurnError, run_chat_turn
    from packages.orchestration.pingpong_job import load_job_plan

    full_id = resolve_job_id_or_fail((job_id or "").strip(), json_output=json_output,
                                     job_id=job_id)
    job = load_job_plan(full_id)
    if job is None:
        fail("job_not_found", f"The record of job {full_id} cannot be read.",
             json_output=json_output, exit_code=EXIT_NOT_READY, job_id=full_id)

    try:
        turn = run_chat_turn(job, text, task_id=(task_id or "").strip())
    except ChatTurnError as exc:
        fail("invalid_task", f"The turn was not run: {exc}.", json_output=json_output,
             exit_code=2, job_id=job.job_id)

    if turn.kind == CHAT_TURN_ANSWER:
        _render_chat_answer_turn(job.job_id, turn, json_output=json_output)
        return
    _send_chat_card(job, turn.card, yes=yes, json_output=json_output)


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "chat.send": lambda args: _cmd_chat_send(
        getattr(args, "job_id", ""), getattr(args, "message", ""),
        json_output=getattr(args, "json", False)),
    "chat.show": lambda args: _cmd_chat_show(
        getattr(args, "job_id", ""), json_output=getattr(args, "json", False)),
    "chat.ask": lambda args: _cmd_chat_ask(
        getattr(args, "job_id", ""), getattr(args, "text", ""),
        task_id=getattr(args, "task", None) or "",
        yes=getattr(args, "yes", False),
        json_output=getattr(args, "json", False)),
}
