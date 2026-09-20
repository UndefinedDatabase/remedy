"""F277 T001 — the one table of run-ledger event names.

``RunEvent.event`` is a bare ``str``.  Roughly forty modules read the ledger
back by literal comparison, so a reader comparing against a name nothing writes
is indistinguishable from one that works: it simply never matches, and the
dimension it feeds scores absent forever.  Two such readers had been doing
exactly that since the day they were written.  This module is the declaration
those comparisons can be checked against, and
``tests/orchestration/test_event_names.py`` is what checks them — by reading the
code, not this docstring.

Dependency-free on purpose: it imports nothing from ``packages.orchestration``,
so any module in the package can validate a name through it without risking an
import cycle.  This mirrors ``model_aliases.py``, the table F254 built for the
same reason.

Public API::

    EVENT_NAMES: frozenset[str]            # every name some code path WRITES
    READ_ONLY_EVENT_NAMES: frozenset[str]  # names only READ — see below
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
        "job_planned",
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
        "task_completed",
        "task_decision_answered",
        "task_needs_decision",
        "task_round_completed",
        "task_run_completed",
        "task_run_failed",
        "task_run_noop",
        "task_run_started",
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

#: Names some module READS and NOTHING writes — every comparison against one of
#: these is dead code today.  This set is a QUARANTINE, not a vocabulary: it may
#: only ever shrink, and the test enforces that in both directions (a name that
#: gains a writer must move up into EVENT_NAMES; a name that loses its last
#: reader must be deleted outright).  Each is disposed of by giving it a writer
#: or by deleting the reader together with whatever it feeds — never by leaving
#: the dimension permanently absent.
READ_ONLY_EVENT_NAMES: frozenset[str] = frozenset(
    {
        # Read by `autonomy_readiness.py` and `memory_learn.py`; the readiness
        # dimension it feeds has therefore never scored present.
        "command_discovery_completed",
        # Read by `change_set.py`, `project_brain.py` and `ui_server.py`, which
        # replay reverts already on disk; `patch_intent_applied` and the other
        # patch_intent_* names are written, this one alone is not.  Its writer
        # spells it `revert_completed` and carries no `intent_id`, the key two
        # of those readers index by, so the rename is a metadata contract and
        # not a spelling — see DECISION F277 D4.
        "patch_intent_reverted",
        # Read by `autonomy_loop.py`; the writer spells it
        # `snapshot_create_completed`.
        "snapshot_created",
        # Read by `project_summary.py`, `ui_server.py` and `ui_view_model.py`.
        # `ui_server.py` already records in a comment that this name has no
        # emitter outside tests (DECISION F031 D2 / D9).
        "stop_reason_recorded",
    }
)


def is_declared_event(name: str) -> bool:
    """True when ``name`` is a declared event name, written or quarantined."""
    return name in EVENT_NAMES or name in READ_ONLY_EVENT_NAMES


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
    """Every declared name, written and quarantined, in sorted order."""
    return tuple(sorted(EVENT_NAMES | READ_ONLY_EVENT_NAMES))
