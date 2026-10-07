"""F298 T001 — the machine client interface as data, read from the code (DECISION F298 D2).

`docs/roadmap/features/T12_F298.md` T001 asks for one document, generated from the code and never
written by hand, that names what a program meets when it drives Remedy's command line. This
module builds it. Every list in it is read from the place the product already keeps it: the
command catalog for the operations, their arguments and the exit codes each can reach;
`apps/cli/exit_codes.py` for what each exit code means; `RunState` for the job states;
`MISSION_STATUSES` for the mission status words; `docs/contracts/` for the contract templates;
`JobBudgets` for the budget kinds; and `apps/cli/json_envelope.py` for the envelope every
`--json` answer wears. A change in any of those places changes the document. Four things are
declared here: which catalog commands a client uses, `CLIENT_OPERATION_IDS`; the tree of the
keys the digest returns, `DIGEST_KEY_TREE`, which `tests/cli/test_client_interface.py` holds equal
to the keys `packages/orchestration/client_digest.py` writes and to what a real run's digest
returns (DECISION F298 D3); the refusal tokens each operation can answer with,
`OPERATION_REFUSAL_TOKENS`, which the same test file holds equal to a static reading of each
operation's handler, the way the catalog's exit codes are held (DECISION F298 D4); and the
top-level keys of the answers of the path's operations, `OPERATION_ANSWER_KEYS`, held equal to
the same reading of each handler and to what a real run of the path returns (DECISION F298 D5).

The feature file calls this document the contract. The product calls it the machine client
interface, because `docs/system/vocabulary.md` reserves "contract" for a mission's acceptance
criteria and nothing else (DECISION F298 D2).

Inside one major version the document only grows: a later minor version adds names and never
removes one.
"""

from __future__ import annotations

import copy
from typing import Any

#: The document's own version. Its major number changes only when a name is removed or changes
#: its meaning; adding a name raises the minor number.
CLIENT_INTERFACE_VERSION = "1.1"

#: The catalog commands a machine client uses: the path of DECISION F295 D17's page (propose,
#: read, answer, run on, approve and apply, prove), the hunk decision a client may choose, the
#: budget refusal of `job resume`, abandoning a mission, and this document's own command.
CLIENT_OPERATION_IDS: tuple[str, ...] = (
    "do.run",
    "status.run",
    "decision.resolve",
    "job.run",
    "job.resume",
    "job.apply",
    "change.proof",
    "job.evidence",
    "patch.hunks",
    "patch.approve-hunks",
    "patch.approve",
    "patch.reject",
    "mission.abandon",
    "client.interface",
)

#: The `error` tokens each operation's refusal envelope can carry, sorted, per catalog command id
#: (DECISION F298 D4). An operation with none here answers no refusal envelope of its own.
OPERATION_REFUSAL_TOKENS: dict[str, tuple[str, ...]] = {
    "do.run": (
        "invalid_argument", "invalid_budget", "order_file_empty", "order_file_invalid_header",
        "order_file_no_cost_cap", "order_file_not_found", "order_file_unreadable", "step_failed",
        "unsupported_contract_template", "unsupported_provider",
    ),
    "status.run": (),
    "decision.resolve": (
        "ambiguous_job_id", "answer_parse_error", "budget_limit_not_raisable",
        "budget_limit_not_raised", "clarifications_already_resolved", "decision_already_answered",
        "decision_not_found", "decision_not_resolvable", "follow_up_mission_error",
        "invalid_argument", "invalid_budget", "invalid_job_id", "job_not_found",
        "missing_argument", "mission_already_linked", "mission_error", "no_pending_plan_approval",
        "no_project", "option_not_applicable", "proposed_task_invalid_state",
        "proposed_task_not_found", "proposed_task_operation_failed", "stop_reason_not_found",
    ),
    "job.run": (
        "invalid_argument", "invalid_budget", "job_not_resumable", "job_not_started", "job_stopped",
        "serve_unreachable",
    ),
    "job.resume": (
        "ambiguous_job_id", "budget_decision_open", "builder_error", "builder_unavailable",
        "checkpoint_not_found", "checkpoint_not_resumable", "checkpoints_corrupt",
        "configuration_error", "confirmation_required", "invalid_argument", "invalid_budget",
        "invalid_builder_output", "invalid_job_id", "job_not_found", "job_not_resumable",
        "job_not_started", "job_stopped", "missing_dependency", "permission_denied",
        "plan_awaiting_approval", "plan_rejected", "resume_blocked", "serve_unreachable",
        "verification_failed", "worktree_drift",
    ),
    "job.apply": (),
    "change.proof": ("ambiguous_job_id", "invalid_job_id", "invalid_path", "job_not_found"),
    "job.evidence": ("job_not_found", "unsafe_task_id"),
    "patch.hunks": ("ambiguous_job_id", "invalid_job_id", "job_not_found"),
    "patch.approve-hunks": (
        "ambiguous_job_id", "duplicate_hunk", "empty_decision", "invalid_job_id", "job_not_found",
        "missing_reason", "no_diff_available", "overlapping_sets", "unknown_hunk",
        "untrustworthy_view",
    ),
    "patch.approve": ("ambiguous_job_id", "invalid_job_id", "job_not_found", "patch_intent_not_found"),
    "patch.reject": ("ambiguous_job_id", "invalid_job_id", "job_not_found", "patch_intent_not_found"),
    "mission.abandon": ("mission_error", "mission_not_found", "no_project"),
    "client.interface": (),
}

#: The top-level keys an answer of each operation of the path can carry beside the envelope's own,
#: sorted, per catalog command id: its answer when it succeeds and its refusals' added keys
#: (DECISION F298 D5). The other operations' answers are read in a later part of T001.
OPERATION_ANSWER_KEYS: dict[str, tuple[str, ...]] = {
    "do.run": (
        "contract", "cost", "failed_step", "job_ids", "jobs", "landed", "mission_id",
        "mission_plan_path", "next", "push", "shape", "shape_source", "steps", "stopped_before_apply",
        "unmet_blocking_criteria", "waiting_job_ids",
    ),
    "status.run": (
        "client", "decisions_open", "degraded", "jobs", "project", "runtime", "runtime_warning",
        "scope", "skipped_files", "stops_pending",
    ),
    "decision.resolve": (
        "answer", "answers", "assumption_log", "budgets", "closed_decisions", "cross_references",
        "decision_id", "follow_up_job_id", "follow_up_mission", "job_id", "matches", "mission_id",
        "next_command", "next_step", "option", "outcome", "raised", "reason_code", "state", "stop_id",
        "task_id",
    ),
    "job.run": (
        "context_strategy", "cost_mirror", "created_at", "execution_config", "finished_at",
        "handoff_available", "has_workspace_changes", "isolation_mode", "job_id", "job_title",
        "job_workspace_path", "next_command", "pending_tasks", "postmortem", "repair_rounds_allowed",
        "repair_rounds_source", "repo_path", "result_diff", "status", "target_guard", "tasks",
        "warning", "worktree",
    ),
    "job.apply": (
        "approved", "blocked_reason", "blocked_reasons", "commit_message_mode", "commit_sha",
        "commit_with_history", "context_strategy", "dry_run", "execution_config", "file_readiness",
        "files_applied", "files_blocked", "files_planned", "files_skipped", "finished_at",
        "history_commits", "job_apply_id", "job_id", "job_status", "job_title", "job_workspace_path",
        "merge_commit", "merge_conflicts", "merged_branch", "missing_source_files", "modes_applied",
        "post_test_command_present", "post_test_passed", "post_test_summary", "push", "push_error",
        "push_open_criteria", "push_ref", "push_remote", "pushed", "reviewed_task_files",
        "skip_blocked", "source_changed_files", "started_at", "status", "target_branch",
        "target_clean", "target_guard_ok", "target_repo", "task_summaries",
        "temporary_worktree_cleanup", "unexpected_source_files",
    ),
    "change.proof": (
        "changes", "generated_at", "goal", "job_applies", "job_id", "matches", "missing_links",
        "next_safe_action", "next_safe_action_obj", "overall_status", "path_filter", "version",
    ),
}

#: The keys of the `client` object in `remedy status --json` (DECISION F295 D4, D5, D7), as a tree:
#: each key maps to the tree of the object under it, or of every element of the list under it,
#: and a key with no keys under it maps to an empty tree (DECISION F298 D3).
DIGEST_KEY_TREE: dict[str, Any] = {
    "version": {},
    "read_at": {},
    "supervisor": {"answers": {}},
    "projects": {
        "project_id": {},
        "slug": {},
        "missions": {
            "mission_id": {},
            "status": {},
            "goal": {},
            "job_ids": {},
            "order_source_path": {},
            "order_source_sha256": {},
        },
        "cost_today": {"day": {}, "value_usd": {}, "basis": {}, "calls": {}},
    },
    "jobs": {
        "job_id": {},
        "project_id": {},
        "mission_id": {},
        "title": {},
        "state": {},
        "waits_for_apply": {},
        "cost": {"value_usd": {}, "basis": {}},
        "evidence": {
            "evidence_dir": {},
            "run_ids": {},
            "postmortem_path": {},
            "run_manifest_path": {},
            "result_diff_path": {},
            "result_diff_sha256": {},
        },
    },
    "awaiting_apply": {},
    "decisions": {
        "job_id": {},
        "project_id": {},
        "decision_id": {},
        "type": {},
        "severity": {},
        "question": {},
        "default": {},
        "options": {},
        "clarifications": {"id": {}, "question": {}, "default": {}},
        "created_at": {},
        "age_seconds": {},
    },
    "degraded": {},
    "skipped_files": {},
}


def _argument_entry(arg: Any) -> dict[str, Any]:
    """One catalog `ArgDef` as the document names it."""
    return {
        "name": arg.name,
        "help": arg.help,
        "option": arg.is_option,
        "required": arg.required,
        "takes_value": not arg.is_flag,
        "repeatable": arg.is_repeatable,
    }


def _operation_entry(command_id: str) -> dict[str, Any]:
    """One operation, read from its catalog entry and its refusal tokens.

    `KeyError` when the catalog has no such id or `OPERATION_REFUSAL_TOKENS` no entry for it.
    """
    from apps.cli.command_catalog import get_command

    entry = get_command(command_id)
    return {
        "command_id": entry.command_id,
        "command": f"remedy {entry.group_id} {entry.subcommand}",
        "description": entry.description,
        "arguments": [_argument_entry(arg) for arg in entry.args],
        "exit_codes": list(entry.exit_codes),
        "refusal_tokens": list(OPERATION_REFUSAL_TOKENS[command_id]),
    }


# WHY: the one builder of the document, so `remedy client interface` and F253's HTTP call print
# the same thing and the page is rendered from the same value (DECISION F298 D2).
def build_client_interface() -> dict[str, Any]:
    """The machine client interface as one JSON-ready dict; reads only, never writes."""
    from apps.cli.exit_codes import CLI_EXIT_CODES
    from apps.cli.json_envelope import RESERVED_KEYS, SCHEMA_VERSION
    from packages.core.models import JobBudgets, RunState
    from packages.orchestration.contract_templates import list_contract_templates
    from packages.orchestration.mission_state import MISSION_STATUSES

    return {
        "interface_version": CLIENT_INTERFACE_VERSION,
        "envelope": {
            "schema_version": SCHEMA_VERSION,
            "reserved_keys": list(RESERVED_KEYS),
            "error_keys": ["error", "message"],
        },
        "operations": [_operation_entry(command_id) for command_id in CLIENT_OPERATION_IDS],
        "exit_codes": [
            {"code": meaning.code, "name": meaning.name, "meaning": meaning.meaning}
            for meaning in CLI_EXIT_CODES
        ],
        "job_states": [state.value for state in RunState],
        "mission_statuses": list(MISSION_STATUSES),
        "contract_templates": list(list_contract_templates()),
        "budget_kinds": list(JobBudgets.model_fields),
        "digest": copy.deepcopy(DIGEST_KEY_TREE),
        "answers": {command_id: list(keys) for command_id, keys in OPERATION_ANSWER_KEYS.items()},
    }
