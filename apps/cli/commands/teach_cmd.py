"""`remedy teach narrate` and `remedy teach ask` — the teacher role's CLI (F255 T002-T004).

`narrate` is Stage 1: the FIRST caller of
``packages.orchestration.teacher_narration`` outside its own tests. It reads ONE
job's run log through the production reader
``packages.orchestration.timeline.load_run_events`` and prints one plain sentence
per event.

`ask` is Stage 2: the FIRST caller of ``packages.orchestration.teacher_model``,
which answers one question through the teacher's own model and records the one
ledger row that answer cost.

`ask --file` is the production caller of GROUNDING SOURCE (2), the workspace
code the ruled Design puts in a Stage 2 context (finding R-0610: the source
accepted `code` from the day it was built and nothing outside the tests ever
passed it). The option reads exactly ONE named file, for reading only, and hands
its text to ``ask_teacher`` as `code` with the path as `code_path`. Without it
both stay None and the answer is grounded exactly as it was before.

THE TWO COMMANDS DECLARE DIFFERENT ACTION CLASSES, and that difference is the
truth rather than an oversight (DECISION F255 D10). `narrate` is `read_only`:
it opens the run log for reading only, holds no lock, and writes nothing — no
run-log entry, no job record, no cache, no export. `ask` is `write_metadata`,
because it writes EXACTLY one token-ledger row for the model call it made. Both
claims are proven behaviourally in ``tests/cli/test_teach_cmd.py`` by hashing
every file under the data root before and after the call — for `ask`, with the
ledger file and its sqlite sidecars excluded BY NAME, so any other write still
fails the test.

Remedy deliberately does NOT emit a run-log event for a teach command. A teacher
that logged its own observation would change what the next observer sees, which
is exactly the influence this role is forbidden
(docs/agents/teacher_conventions.md, "Stance").

Zero tokens for Stage 1: narration is a template lookup, so it reaches no model
and spends nothing. The teacher's own model key (``teacher.model``) belongs to
`ask` alone and is deliberately not read by `narrate`.

Exit codes:
* 0 — narrated, answered, OR REFUSED; an absent or empty run log narrates to
  nothing and is still 0, and a refusal is still 0 because a teacher that could
  fail a run would not be passive;
* 1 or 2 — raised by ``resolve_any_job_id`` itself: an unusable id, or a short
  prefix matching more than one job. These commands add no exit path of their
  own. Both job stores are searched — the classic ``jobs/<uuid>.json`` one and
  the ``jobs/<16hex>/`` one `remedy do job-run` writes — so a job-based
  run is narratable; the exit codes and messages are unchanged.
"""
from __future__ import annotations


def _cmd_teach_narrate(job_id_str: str, *, json_output: bool = False) -> None:
    """Narrate one job's run log. READ-ONLY: nothing on this path writes."""
    import json as _json

    from packages.orchestration.data_paths import resolve_any_job_id, resolve_data_root
    from packages.orchestration.teacher_narration import narrate_run_events
    from packages.orchestration.timeline import load_run_events

    # BOTH job stores, not just the classic one: `remedy do job-run` files its
    # jobs under `jobs/<16hex>/` with 16-hex ids, and `resolve_job_id`
    # searches `jobs/*.json` and returns a UUID. The teacher answered "no job
    # matches prefix" for every job-based run, whose run log was on disk the
    # whole time (operator dogfooding, 2026-08-25). Still read-only: the
    # resolver opens directories and writes nothing.
    job_id = resolve_any_job_id(job_id_str)
    events = load_run_events(resolve_data_root(), job_id)
    sentences = narrate_run_events(events)

    if json_output:
        print(_json.dumps({
            "job_id": str(job_id),
            "event_count": len(events),
            "narration": sentences,
        }, indent=2))
        return

    print(f"Teacher narration for job {str(job_id)[:8]} ({len(events)} events)")
    if not sentences:
        print("  no events yet")
    for sentence in sentences:
        print(f"  {sentence}")


#: The one line printed when an answer produced NO ledger row — a refusal, or a
#: ledger write that missed. Said out loud rather than left to silence: a cost
#: that was not recorded is a cost `remedy stats cost` will never show.
_UNBILLED_NOTE = "No spend row was recorded for this question."


#: The one line printed when `--file` named a path that could not be read. Said
#: OUT LOUD rather than swallowed: an operator never told would believe the
#: answer read code it never opened, which is the invention this role refuses.
_UNREADABLE_FILE_NOTE = "Could not read {path} ({reason}); answering without it."


def _read_grounding_file(path: str) -> str | None:
    """The text of ONE workspace file, or None after saying why out loud.

    READ-ONLY toward the workspace: opening a file for reading writes nothing,
    so `teach.ask` keeps its `write_metadata` class and the ledger row stays its
    only write (DECISION F255 D10). An unreadable path NEVER fails the command —
    a teacher that could fail a run would not be the passive role — so this
    returns None and the answer is given from the sources that did resolve.
    """
    from pathlib import Path

    try:
        return Path(path).read_text(encoding="utf-8")
    except (OSError, ValueError) as exc:
        reason = getattr(exc, "strerror", None) or str(exc) or type(exc).__name__
        print(_UNREADABLE_FILE_NOTE.format(path=path, reason=reason))
        return None


def _grounding_sources(context) -> tuple[str, ...]:
    """The sources this answer may speak from, in the order the prompt lists them.

    Mirrors ``teacher_qa.render_prompt``'s own emission rule: a source appears
    when it has facts, and ``concept`` always appears because general knowledge
    is always permitted — explicitly labelled as not a claim about this project.
    """
    from packages.orchestration.teacher_qa import GROUNDING_SOURCES, SOURCE_CONCEPT

    present = {fact.source for fact in context.facts}
    return tuple(s for s in GROUNDING_SOURCES if s in present or s == SOURCE_CONCEPT)


def _cmd_teach_ask(
    question: str,
    *,
    job_id: str | None = None,
    file: str | None = None,
    level: str | None = None,
    project: str | None = None,
    json_output: bool = False,
    call=None,
) -> None:
    """Answer one question about a run or the operator's code. Writes ONE ledger row.

    ``file`` is grounding source (2): one workspace file, read for reading only,
    passed on as `code` with its path as `code_path`. Absent — or present but
    unreadable — both stay None and the answer is grounded as it was before.

    ``call`` is the transport seam of ``teacher_model.ask_teacher``; it is NOT a
    CLI flag and stays None in every real invocation. It exists so the tests can
    prove this command's behaviour without a running Ollama (DECISION F255 D8).
    """
    import json as _json

    from packages.orchestration.data_paths import resolve_any_job_id, resolve_data_root
    from packages.orchestration.project_scope import resolve_scope
    from packages.orchestration.teacher_model import ask_teacher
    from packages.orchestration.teacher_qa import DEFAULT_LEVEL, build_teacher_context
    from packages.orchestration.timeline import load_run_events

    resolved_level = level or DEFAULT_LEVEL
    # The same scope resolution `remedy stats cost` uses, so the row this writes
    # lands in the ledger that command reads.
    scope = resolve_scope(project_flag=project, all_projects=False)

    resolved_job: str | None = None
    events: list[dict] = []
    if job_id:
        # Both job stores, for the reason `narrate` states above.
        resolved_job = resolve_any_job_id(job_id)
        events = load_run_events(resolve_data_root(), resolved_job)

    code: str | None = None
    code_path: str | None = None
    if file:
        code = _read_grounding_file(file)
        code_path = file if code is not None else None

    # The SAME `code` and `code_path` reach both contexts. The printed source
    # list is derived from the context it describes, so the two cannot disagree.
    sources = _grounding_sources(
        build_teacher_context(
            question,
            events=events,
            code=code,
            code_path=code_path,
            level=resolved_level,
        )
    )
    answer = ask_teacher(
        question,
        events=events,
        code=code,
        code_path=code_path,
        level=resolved_level,
        call=call,
        job_id=resolved_job,
        project_id=scope.project_id,
    )

    if json_output:
        print(_json.dumps({
            "question": question,
            "job_id": resolved_job or "",
            "level": resolved_level,
            "model": answer.model,
            "refused": answer.refused,
            "answer": answer.text,
            "grounding_sources": list(sources),
            "call_id": answer.call_id,
            "billed": answer.billed,
        }, indent=2))
        return

    print(f"Teacher answer ({answer.model})")
    print(answer.text)
    print(f"Grounding sources: {', '.join(sources)}")
    if not answer.billed:
        print(_UNBILLED_NOTE)


COMMAND_HANDLERS = {
    "teach.narrate": lambda args: _cmd_teach_narrate(
        getattr(args, "job_id", "") or "",
        json_output=bool(getattr(args, "json", False)),
    ),
    "teach.ask": lambda args: _cmd_teach_ask(
        getattr(args, "question", "") or "",
        job_id=getattr(args, "job_id", None),
        file=getattr(args, "file", None),
        level=getattr(args, "level", None),
        project=getattr(args, "project", None),
        json_output=bool(getattr(args, "json", False)),
    ),
}
