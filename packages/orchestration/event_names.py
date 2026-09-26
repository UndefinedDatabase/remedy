"""F277 T001 — the one table of run-ledger event names.

``RunEvent.event`` is a bare ``str``.  Roughly forty modules read the ledger
back by literal comparison, so a reader comparing against a name nothing writes
is indistinguishable from one that works: it simply never matches, and the
dimension it feeds scores absent forever.  Six such readers existed when F277
measured the tree.  Four were accidents and are gone — two readers deleted with
what they fed, two names given the writer their readers had always named — and
the two that remain are not accidents at all: they are RETIRED names, whose
writers a dated decision removed and whose readers the same decision kept, so
that run logs already on disk still render.  This module is the declaration all
those comparisons can be checked against, and
``tests/orchestration/test_event_names.py`` is what checks them — by reading the
code, not this docstring.

Dependency-free on purpose: it imports nothing from ``packages.orchestration``,
so any module in the package can validate a name through it without risking an
import cycle.  This mirrors ``model_aliases.py``, the table F254 built for the
same reason.

Public API::

    EVENT_NAMES: frozenset[str]          # every name some code path WRITES
    RETIRED_EVENT_NAMES: frozenset[str]  # names only READ, by ruling — see below
    is_declared_event(name) -> bool
    assert_declared_event(name) -> None    # raises ValueError on an unknown name
    known_event_names() -> tuple[str, ...]

Deliberate absences:
  * Remedy deliberately does not RENAME any event name here.  F277 declares the
    vocabulary that exists; the names themselves are the feature's explicit
    "Do not touch" (docs/roadmap/features/T2_F277.md).  That is why two spelling
    conventions survive below — ``budget.tick`` and ``command.accepted`` use a
    dot where every other name uses an underscore.
  * Remedy deliberately does not validate event names on every write.  The check
    is opt-in through ``REMEDY_STRICT_EVENT_NAMES`` (see ``run_log.py``), because
    a ledger write must never break a running job — the same reason
    ``long_run_executor._emit`` swallows its own exceptions.
  * Remedy deliberately does not group these names by producer.  A name is
    written in one place and read in many, so any grouping would encode the
    writer's view of a table whose whole purpose is to serve the readers.
  * Remedy deliberately does not mint a writer for a RETIRED name to make the
    two sets collapse into one.  A retired name's writer was removed on
    purpose and its readers were kept on purpose; re-creating the writer would
    resurrect a mechanism a decision deleted, which AGENTS.md's "Replacing is
    deleting" forbids, and deleting the readers would stop run logs already on
    disk from rendering.  The set is therefore allowed to be non-empty, and
    every entry cites the decision that retired it.
"""

from __future__ import annotations

#: Every event name this repository WRITES, measured from the source by
#: ``tests/orchestration/test_event_names.py``.  A name enters this set in the
#: same commit as the code path that writes it; the test fails otherwise.
EVENT_NAMES: frozenset[str] = frozenset(
    {
        "agent_loop_inspected",
        "apply_record_saved",
        "brain_node_inspected",
        "brain_viewer_prepared",
        "budget.tick",
        "builder_bridge_intent_approved",
        "builder_bridge_test_completed",
        "builder_completed",
        "builder_patch_parsed",
        "builder_started",
        "command.accepted",
        "command_discovery_completed",
        "context_coverage_inspected",
        "continued_from_node",
        "contract_decision",
        "cycle_completed",
        "cycle_healed",
        "cycle_loop_terminal",
        "cycle_repair_round",
        "diff_repair_applied",
        "diff_repair_not_used",
        "job_created",
        "job_final",
        "job_paused",
        "job_planned",
        "job_resumed",
        "job_stopped",
        "memory_learned",
        "patch_apply_proof_recorded",
        "patch_intent_applied",
        "patch_intent_approved",
        "patch_intent_created",
        "patch_intent_failed",
        "patch_intent_rejected",
        "patch_intent_skipped",
        "planning_completed",
        "planning_failed",
        "planning_started",
        "project_brain_inspected",
        "project_constitution_loaded",
        "project_memory_recalled",
        "proof_collected",
        "repair_context_created",
        "repair_loop_cycle_started",
        "repair_loop_stopped",
        "repair_loop_succeeded",
        "repair_mode_selected",
        "repair_round_fell_back_to_full_file",
        "repair_task_created",
        "repo_application_completed",
        "repo_application_skipped",
        "resume_blocked",
        "resume_completed",
        "resume_started",
        "resume_test_completed",
        "resume_test_started",
        "revert_blocked",
        "revert_completed",
        "revert_failed",
        "revert_started",
        "run_usage_recorded",
        "sequencing_proof",
        "snapshot_create_completed",
        "snapshot_verified",
        "source_patch_applied",
        "steering_message_consumed",
        "steering_message_received",
        "task_completed",
        "task_decision_answered",
        "task_lesson_written",
        "task_needs_decision",
        "task_paused",
        "task_resumed",
        "task_round_completed",
        "task_run_completed",
        "task_run_failed",
        "task_run_noop",
        "task_run_started",
        "task_vetoed",
        "test_failure_artifact_created",
        "test_run_blocked",
        "test_run_completed",
        "test_run_requested",
        "test_run_started",
        "test_run_timed_out",
        "token_policy_applied",
        "verification_failed",
        "verification_passed",
        "workspace_materialized",
        "worktree_prepared",
        "worktree_recovered",
        "worktree_retained",
    }
)

#: Names NOTHING writes any more and live code still READS, on purpose, so that
#: run logs written before the writer was removed keep rendering.  Every entry
#: names the decision that retired its writer: an entry with no such citation is
#: an accident and belongs in neither set — give it a writer or delete its
#: readers.  The test enforces both edges. A retired name that GAINS a writer
#: moves up into EVENT_NAMES, because it is no longer retired; a retired name
#: that loses its LAST reader is deleted outright, because nothing can then
#: observe it.  Unlike the quarantine this set replaces, its floor is not zero:
#: see the fourth deliberate absence above.
RETIRED_EVENT_NAMES: frozenset[str] = frozenset(
    {
        # Retired by DECISION F271 D3, which deleted its only writer
        # `patch_revert.py` under finding R-0982 and ruled in as many words that
        # the readers stay, each reading run logs already on disk.  Those readers
        # are `change_set.py`, `project_brain.py` and `ui_server.py`; the fourth
        # reader that ruling kept, `autonomy_readiness._has_revert_snapshot`, was
        # deleted by F277 round 2 because it fed a signal no level checked, which
        # is the one of the four that was an accident rather than a retirement.
        # The live revert path writes `revert_completed`, a per-apply event that
        # carries no `intent_id` and no path by design, so it is a different
        # event and not this one under another spelling (DECISION F277 D5).
        "patch_intent_reverted",
        # Retired by DECISION F031 D2 and D9, which retired the blocker addend
        # and the scan that read this name; `ui_server.py` carries that reading
        # in a comment of its own above `_count_open_decisions`.  The readers
        # `project_summary.py`, `ui_view_model.py` and `ui_server.py` render
        # stop reasons from run logs already on disk, and five test files plant
        # the event to exercise them.
        "stop_reason_recorded",
    }
)


def is_declared_event(name: str) -> bool:
    """True when ``name`` is a declared event name, written or retired."""
    return name in EVENT_NAMES or name in RETIRED_EVENT_NAMES


def assert_declared_event(name: str) -> None:
    """Raise ``ValueError`` unless ``name`` is declared above.

    Called from ``RunLogWriter.log`` only under ``REMEDY_STRICT_EVENT_NAMES``,
    so a production job never fails a ledger write on this.
    """
    if not is_declared_event(name):
        raise ValueError(
            f"undeclared run-ledger event name {name!r} — add it to EVENT_NAMES "
            "in packages/orchestration/event_names.py in the same commit as the "
            "code path that writes it"
        )


def known_event_names() -> tuple[str, ...]:
    """Every declared name, written and retired, in sorted order."""
    return tuple(sorted(EVENT_NAMES | RETIRED_EVENT_NAMES))
