"""F298 T001 — the machine client interface as data, read from the code (DECISION F298 D2).

`docs/roadmap/features/T12_F298.md` T001 asks for one document, generated from the code and never
written by hand, that names what a program meets when it drives Remedy's command line. This
module builds it. Every list in it is read from the place the product already keeps it: the
command catalog for the operations, their arguments and the exit codes each can reach; the
command line's parser for whether an argument takes a value and may be repeated (R-1178);
`apps/cli/exit_codes.py` for what each exit code means; `RunState` for the job states;
`MISSION_STATUSES` for the mission status words; `docs/contracts/` for the contract templates;
`JobBudgets` for the budget kinds; and `apps/cli/json_envelope.py` for the envelope every
`--json` answer wears. A change in any of those places changes the document. The rest is
declared here: which catalog commands a client uses, `CLIENT_OPERATION_IDS`; the tree of the
keys the digest returns, `DIGEST_KEY_TREE`, which `tests/cli/test_client_interface.py` holds equal
to the keys `packages/orchestration/client_digest.py` writes and to what a real run's digest
returns (DECISION F298 D3); the refusal tokens each operation can answer with,
`OPERATION_REFUSAL_TOKENS`, which the same test file holds equal to a static reading of each
operation's handler, the way the catalog's exit codes are held (DECISION F298 D4); and the
top-level keys of the operations' answers, `OPERATION_ANSWER_KEYS`, held equal to the same
reading of each handler and to what a real run returns (DECISIONs F298 D5, D6 and D7); and the
keys under those keys, `ANSWER_KEY_TREES`, each tree held equal to the code that builds it and to
what a real run returns (DECISIONs F298 D8 to D18).

The feature file calls this document the contract. The product calls it the machine client
interface, because `docs/system/vocabulary.md` reserves "contract" for a mission's acceptance
criteria and nothing else (DECISION F298 D2).

Inside one major version the document only grows: a later minor version adds names and never
removes one.
"""

from __future__ import annotations

import argparse
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

#: The top-level keys an answer of each operation can carry beside the envelope's own, sorted, per
#: catalog command id: its answer when it succeeds and its refusals' added keys (DECISIONs F298 D5,
#: D6 and D7); `ANSWER_KEY_TREES` names the keys under them.
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
    "job.resume": (
        "action", "awaiting_checks", "blocked_reason", "budget_stop", "can_resume",
        "checkpoint_id", "checkpoint_index", "checkpoint_kind", "context_strategy", "cost_mirror",
        "created_at", "cycles", "cycles_run", "decision_id", "dry_run", "elapsed_ms",
        "execution_config", "failures", "file", "finished_at", "handoff_available",
        "has_workspace_changes", "isolation_mode", "job_id", "job_status", "job_title",
        "job_workspace_path", "log", "matches", "model", "next_command", "open_decision_ids",
        "outcome", "output_truncated", "patch_intents", "pending_tasks", "persisted_output_bytes",
        "plan_approval_gate", "postmortem", "reason", "redaction", "remaining",
        "repair_rounds_allowed", "repair_rounds_source", "repo", "repo_path", "required_approvals",
        "required_capabilities", "result_diff", "resume_mode", "resumed", "safety_summary",
        "stage", "state", "status", "stop_reason", "stop_request", "target_guard", "task_id",
        "task_type", "tasks", "terminal_status", "test_run_id", "tests_passed", "verified",
        "warning", "worktree", "worktree_head", "worktrees", "would_run", "would_run_stage",
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
    "job.evidence": ("files", "job_id", "manifest", "out_dir"),
    "patch.hunks": ("decision", "job_id", "matches", "view"),
    "patch.approve-hunks": ("attempt", "decided_at", "hunk_ids", "hunks", "matches", "task_id"),
    "patch.approve": ("intent_id", "matches", "reason_recorded", "risk", "state", "target_path"),
    "patch.reject": ("intent_id", "matches", "reason_recorded", "risk", "state", "target_path"),
    "mission.abandon": ("mission", "unmet_blocking_criteria", "version"),
    "client.interface": (
        "answer_trees", "answers", "budget_kinds", "contract_templates", "digest", "envelope", "exit_codes",
        "interface_version", "job_states", "mission_statuses", "operations",
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

#: The keys of a job's execution configuration as its record exports them, a tree several answers
#: carry under `execution_config` (DECISION F298 D9).
EXECUTION_CONFIG_KEY_TREE: dict[str, Any] = {key: {} for key in (
    "builder", "builder_source", "reviewer", "reviewer_source", "builder_model",
    "builder_model_source", "builder_effort", "builder_effort_source", "reviewer_model",
    "reviewer_model_source", "reviewer_effort", "reviewer_effort_source", "repair_provider",
    "repair_provider_source", "repair_model", "repair_model_source", "repair_effort",
    "repair_effort_source", "max_rounds", "max_rounds_source", "repair_rounds_allowed",
    "repair_rounds_source", "test_command", "test_command_present", "test_command_source",
    "claude_cli_write_mode", "claude_cli_write_mode_source", "context_strategy", "timeout_sec",
    "timeout_sec_source", "timeout_profile", "timeout_profile_source", "max_output_chars",
    "max_output_chars_source", "stream_evidence", "stream_evidence_source", "max_tasks",
    "max_tasks_source",
)}

#: The keys of a job's target guard as its record exports them, a tree several answers carry
#: under `target_guard` (DECISION F298 D13).
TARGET_GUARD_KEY_TREE: dict[str, Any] = {key: {} for key in (
    "target_mutated", "target_content_mutated", "target_operational_artifacts_changed",
    "target_noise_changed", "changed_target_files", "ignored_operational_artifacts",
    "ignored_target_noise_files",
)}

#: The keys of a mission's contract, its acceptance criteria, as its record holds them, a tree
#: several answers carry under `contract` (DECISION F298 D14).
MISSION_CONTRACT_KEY_TREE: dict[str, Any] = {
    "schema": {},
    "template": {},
    "criteria": {
        "id": {},
        "text": {},
        "blocking": {},
        "origin": {},
        "milestones": {},
        "check": {
            "id": {},
            "kind": {},
            "spec": None,
            "blocking": {},
            "acceptance_refs": {},
            "description": {},
            "source": {},
        },
        "status": {},
        "evidence_ref": {},
    },
    "amendments": {
        "id": {},
        "text": {},
        "received_at": {},
        "applies_from": {},
        "criteria": {},
        "understood": {},
        "acknowledged_in": {},
    },
}

#: The keys of a job's budgets as its record exports them, the budget kinds, a tree answers carry
#: wherever they name budget limits (DECISION F298 D16).
JOB_BUDGETS_KEY_TREE: dict[str, Any] = {key: {} for key in (
    "max_total_tokens", "max_provider_calls", "max_wall_clock_minutes", "max_cost_usd", "deadline",
    "min_free_disk_bytes",
)}

#: The mark a key of a tree maps to when the object under it, or each element of the list under
#: it, has the shape of the object that holds the key: a shape that repeats itself (DECISION F298
#: D14). A mission plan's `_versions` holds each earlier version of the plan, and each of those
#: carries its own `_versions`; a key tree this interface answers holds a key tree under each of
#: its names (DECISION F298 D15).
KEY_TREE_REPEAT_MARK = "^"

#: The keys under the top-level keys of a job's report, the answer of `remedy job run` and of a
#: `remedy job resume` that hands the job to it (DECISIONs F298 D9 and D17).
JOB_REPORT_KEY_TREES: dict[str, Any] = {
    "tasks": {
        "task_id": {},
        "source_heading_number": {},
        "title": {},
        "status": {},
        "run_id": {},
        "final_status": {},
        "test_passed": {},
        "reviewer_verdict": {},
        "repair_rounds_used": {},
        "repair_rounds_allowed": {},
        "safe_diff_files": {},
        "error": {},
        "apply_manifest": {
            "task_id": {},
            "run_id": {},
            "applied_files": {},
            "missing_files": {},
            "unsupported_files": {},
            "unexpected_files": {},
            "duplicate_files": {},
            "applied_file_proofs": {
                "path": {},
                "existed_before_job": {},
                "baseline_sha256": {},
                "final_workspace_sha256": {},
                "task_id": {},
                "run_id": {},
                "baseline_mode": {},
                "final_mode": {},
            },
            "status": {},
        },
        "proof_summary": {
            "task_id": {},
            "title": {},
            "run_id": {},
            "final_status": {},
            "applied_files": {},
            "test_passed": {},
            "reviewer_verdict": {},
            "repair_rounds_used": {},
            "repair_rounds_allowed": {},
            "tokens_estimated": {},
        },
        "veto": {"reason": {}, "actor": {}, "requested_at": {}, "unreachable_task_ids": {}},
        "steering_not_consumed": {"message_id": {}, "text": {}, "received_at": {}},
    },
    "worktree": {
        "branch": {},
        "path": {},
        "base_commit": {},
        "head": {},
        "cleanup_status": {},
        "workspace_expected_present": {},
    },
    "result_diff": {"path": {}, "sha256": {}, "size_bytes": {}},
    "target_guard": TARGET_GUARD_KEY_TREE,
    "postmortem": {"path": {}, "error": {}},
    "execution_config": EXECUTION_CONFIG_KEY_TREE,
    "context_strategy": {
        "strategy": {},
        "previous_task_summary_limit": {},
        "full_job_history_in_prompt": {},
        "full_repo_in_prompt": {},
    },
    "cost_mirror": {"ledger_mirrored": {}, "out_dir": {}, "error": {}},
}

#: The keys under the top-level answer keys, per catalog command id and top-level key, as trees in
#: the form of `DIGEST_KEY_TREE` (DECISION F298 D8). A top-level key absent here carries no keys
#: under it. The key `*` stands for keys that are data, such as a path or a job id, and maps to the
#: tree under each of them; a key that maps to None holds an object whose keys the interface does
#: not fix, which only a mission contract's check `spec` does: its keys are the arguments of the
#: check's `kind`; a key that maps to `KEY_TREE_REPEAT_MARK` holds the tree of the object that holds
#: it again, which a mission plan's `_versions` does and the key trees `client.interface` answers
#: do. Every operation has an entry here, and one that maps to an empty dict answers no keys below
#: its top level (DECISION F298 D18).
ANSWER_KEY_TREES: dict[str, dict[str, Any]] = {
    "do.run": {
        "contract": MISSION_CONTRACT_KEY_TREE,
        "cost": {
            "roles": {
                "role": {},
                "calls": {},
                "tokens_in": {},
                "tokens_out": {},
                "cache_read": {},
                "cost_usd": {},
            },
            "cost_usd": {},
            "job_ids": {},
            "mirror_failed_job_ids": {},
            "mirror_errors": {"*": {}},
        },
        "jobs": {"job_id": {}, "tasks": {"title": {}, "deliverable": {}}},
        "steps": {"name": {}, "status": {}, "detail": {}},
        "landed": {"job_id": {}, "sha": {}, "branch": {}},
        "push": {
            "pushed": {},
            "sha": {},
            "remote": {},
            "ref": {},
            "error": {},
            "source": {},
            "open_blocking_criteria": {},
        },
    },
    "status.run": {
        "jobs": {"*": {"job_id": {}, "short_id": {}, "name": {}, "state": {}}},
        "client": DIGEST_KEY_TREE,
    },
    "job.run": JOB_REPORT_KEY_TREES,
    "job.resume": {
        **JOB_REPORT_KEY_TREES,
        "stop_request": {"pending": {}, "reason": {}},
        "worktree_head": {"outcome": {}, "checkpoint_head": {}, "live_head": {}},
        "budget_stop": {"stopped": {}, "decision_id": {}},
        "failures": {"check": {}, "message": {}},
        "cycles": {key: {} for key in (
            "cycle_index", "tasks_attempted", "tasks_completed", "tasks_failed", "tasks_escalated",
            "verify_result", "verify_command", "tokens_so_far", "started_at", "ended_at", "errors",
            "executed_task_ids", "skipped_blocked_task_ids", "awaiting_task_ids",
            "awaiting_downstream_task_ids", "paused_task_ids", "paused_downstream_task_ids",
            "open_decision_ids", "verify_failure_class", "repair_rounds_used", "healed_after_repair",
            "healed_without_changes", "repair_summary",
        )},
        "worktrees": {key: {} for key in (
            "run_id", "applicable", "prepared", "recovered", "blocked", "blocked_reason", "branch",
            "worktree_path", "base_commit", "head", "result_diff_sha256", "result_diff_size_bytes",
            "cleanup_status", "branch_kept", "notes",
        )},
    },
    "job.apply": {
        "modes_applied": {"*": {}},
        "temporary_worktree_cleanup": {
            "temporary_worktree_removed": {},
            "temporary_registration_removed": {},
            "cleanup_status": {},
            "cleanup_error": {},
        },
        "task_summaries": {
            "task_id": {},
            "title": {},
            "status": {},
            "run_id": {},
            "reviewer_verdict": {},
            "test_passed": {},
            "repair_rounds_used": {},
            "repair_rounds_allowed": {},
            "applied_files": {},
        },
        "file_readiness": {"path": {}, "kind": {}, "baseline_status": {}, "workspace_status": {}},
        "execution_config": EXECUTION_CONFIG_KEY_TREE,
    },
    "change.proof": {
        "next_safe_action_obj": {"label": {}, "command": {}, "reason": {}, "available": {}},
        "changes": {
            "target_path": {},
            "intent_id": {},
            "task_id": {},
            "task_title": {},
            "artifact_id": {},
            "approval_state": {},
            "apply_state": {},
            "test_state": {},
            "test_link": {},
            "proof_status": {},
            "safe_summary": {},
            "next_safe_action": {},
            "next_safe_action_obj": {"label": {}, "command": {}, "reason": {}, "available": {}},
            "missing_links": {},
        },
        "job_applies": {
            "job_apply_id": {},
            "status": {},
            "approved": {},
            "dry_run": {},
            "finished_at": {},
            "files_applied": {},
            "commit_sha": {},
            "pushed": {},
            "post_test_passed": {},
        },
    },
    "patch.hunks": {
        "view": {
            "version": {},
            "scope": {},
            "task_id": {},
            "source": {},
            "available": {},
            "reason": {},
            "truncated": {},
            "files": {
                "path": {},
                "old_path": {},
                "status": {},
                "stats": {"added": {}, "deleted": {}},
                "note": {},
                "hunks": {
                    "id": {},
                    "header": {},
                    "old_start": {},
                    "new_start": {},
                    "lines": {"kind": {}, "old_ln": {}, "new_ln": {}, "content": {}, "intraline": {}},
                },
            },
            "task_run_ids": {},
        },
        "decision": {
            "attempt_key": {},
            "decided_at": {},
            "hunks": {"id": {}, "state": {}, "reason": {}},
        },
    },
    "patch.approve-hunks": {
        "hunks": {"id": {}, "state": {}, "reason": {}, "landing": {}},
    },
    "job.evidence": {
        "files": {"*": {}},
        "manifest": {
            "bundle_version": {},
            "bundle_type": {},
            "job_id": {},
            "job_title": {},
            "job_file_sha256": {},
            "status": {},
            "repo_identity": {},
            "job_workspace_path": {},
            "created_at": {},
            "finished_at": {},
            "task_count": {},
            "task_ids": {},
            "task_statuses": {"*": {}},
            "task_run_ids": {"*": {}},
            "execution_config": EXECUTION_CONFIG_KEY_TREE,
            "context_strategy": {},
            "target_guard": TARGET_GUARD_KEY_TREE,
            "error": {},
            "bundle_generated_at": {},
        },
    },
    "patch.approve": {},
    "patch.reject": {},
    "mission.abandon": {
        "mission": {
            "schema_version": {},
            "id": {},
            "project_id": {},
            "goal": {},
            "status": {},
            "job_links": {"job_id": {}, "role": {}, "created_at": {}, "job_state": {}},
            "dossier_ref": {},
            "created_at": {},
            "mission_plan": {
                "schema_v": {},
                "milestones": {
                    "id": {},
                    "goal": {},
                    "rationale": {},
                    "depends_on": {},
                    "jobs_draft": {"title": {}, "goal": {}, "est_band": {}},
                    "dod_ref": {},
                },
                "risks": {},
                "assumptions": {},
                "compiled": {},
                "origin": {},
                "_versions": KEY_TREE_REPEAT_MARK,
                "_version": {},
                "_milestones_done": {},
            },
            "order": {"text": {}, "source_path": {}, "source_sha256": {}},
            "contract": MISSION_CONTRACT_KEY_TREE,
        },
    },
    "decision.resolve": {
        "answers": {"id": {}, "source": {}, "answer": {}},
        "raised": JOB_BUDGETS_KEY_TREE,
        "budgets": JOB_BUDGETS_KEY_TREE,
    },
    "client.interface": {
        "envelope": {"schema_version": {}, "reserved_keys": {}, "error_keys": {}},
        "operations": {
            "command_id": {},
            "command": {},
            "description": {},
            "arguments": {
                "name": {},
                "help": {},
                "option": {},
                "required": {},
                "takes_value": {},
                "repeatable": {},
            },
            "exit_codes": {},
            "refusal_tokens": {},
        },
        "exit_codes": {"code": {}, "name": {}, "meaning": {}},
        "digest": {"*": KEY_TREE_REPEAT_MARK},
        "answers": {"*": {}},
        "answer_trees": {"*": {"*": {"*": KEY_TREE_REPEAT_MARK}}},
    },
}


def _parser_actions(entry: Any) -> dict[str, argparse.Action]:
    """The actions the command line's parser builds for one catalog entry, by argument name."""
    from apps.cli.grouped import _add_command_args

    parser = argparse.ArgumentParser(add_help=False)
    _add_command_args(parser, entry)
    return {name: action for action in parser._actions
            for name in (action.option_strings or [action.dest])}


# WHY: the parser, not the catalog's `is_flag`, decides whether an argument takes a value and may
# be repeated, because it gives `--json`, `--approve` and others their own rules by name (R-1178,
# DECISION F298 D19).
def _argument_entry(arg: Any, action: argparse.Action) -> dict[str, Any]:
    """One catalog `ArgDef` as the document names it, with the parser action built for it."""
    return {
        "name": arg.name,
        "help": arg.help,
        "option": arg.is_option,
        "required": arg.required,
        "takes_value": action.nargs != 0,
        "repeatable": isinstance(action, argparse._AppendAction),
    }


def _operation_entry(command_id: str) -> dict[str, Any]:
    """One operation, read from its catalog entry, its parser and its refusal tokens.

    `KeyError` when the catalog has no such id, the parser no action for one of its arguments, or
    `OPERATION_REFUSAL_TOKENS` no entry for it.
    """
    from apps.cli.command_catalog import get_command

    entry = get_command(command_id)
    actions = _parser_actions(entry)
    return {
        "command_id": entry.command_id,
        "command": f"remedy {entry.group_id} {entry.subcommand}",
        "description": entry.description,
        "arguments": [_argument_entry(arg, actions[arg.name]) for arg in entry.args],
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
        "answer_trees": copy.deepcopy(ANSWER_KEY_TREES),
    }
