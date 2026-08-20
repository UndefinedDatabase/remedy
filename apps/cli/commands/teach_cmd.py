"""`remedy teach narrate <job_id>` — Stage 1 of the teacher role (F255 T002/T003).

The FIRST caller of ``packages.orchestration.teacher_narration`` outside its own
tests. It reads ONE job's run log through the production reader
``packages.orchestration.timeline.load_run_events`` and prints one plain sentence
per event.

READ-ONLY by construction AND by test: this command opens the run log for
reading only, holds no lock, and writes nothing — no run-log entry, no job
record, no cache, no export. ``tests/cli/test_teach_cmd.py`` proves that
behaviourally, by hashing every file under the data root before and after the
call and comparing the two maps.

Remedy deliberately does NOT emit a run-log event for a teach command. A teacher
that logged its own observation would change what the next observer sees, which
is exactly the influence this role is forbidden
(docs/agents/teacher_conventions.md, "Stance").

Zero tokens: narration is a template lookup, so Stage 1 reaches no model and
spends nothing. The teacher's own model key (``teacher.model``) belongs to the
Stage 2 question path and is deliberately not read here.

Exit codes:
* 0 — narrated; an absent or empty run log narrates to nothing and is still 0;
* 1 or 2 — raised by ``resolve_job_id`` itself: an unusable id, or a short
  prefix matching more than one job. This command adds no exit path of its own,
  because a teacher that could fail a run in a new way would not be passive.
"""
from __future__ import annotations


def _cmd_teach_narrate(job_id_str: str, *, json_output: bool = False) -> None:
    """Narrate one job's run log. READ-ONLY: nothing on this path writes."""
    import json as _json

    from packages.orchestration.data_paths import resolve_data_root, resolve_job_id
    from packages.orchestration.teacher_narration import narrate_run_events
    from packages.orchestration.timeline import load_run_events

    job_id = resolve_job_id(job_id_str)
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


COMMAND_HANDLERS = {
    "teach.narrate": lambda args: _cmd_teach_narrate(
        getattr(args, "job_id", "") or "",
        json_output=bool(getattr(args, "json", False)),
    ),
}
