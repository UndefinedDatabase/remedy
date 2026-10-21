"""The digest's key tree, moved out of `apps/cli/client_interface.py` (structure step, F311 R3 C4).

`apps/cli/client_interface.py` imports `DIGEST_KEY_TREE` from here: the keys of the `client`
object `remedy status --json` answers, so that module stays below the structure ratchet's
file limit (the shape of `client_interface_story.py`'s docstring).
"""

from __future__ import annotations

from typing import Any

#: The tokens by kind a project ledger holds, a tree the digest carries for each job and each
#: project's day (DECISION F304 D13).
TOKENS_BY_KIND_KEY_TREE: dict[str, Any] = {key: {} for key in (
    "input", "output", "cache_read", "cache_creation",
)}

#: The keys of the `client` object in `remedy status --json` (DECISION F295 D4, D5, D7; DECISION
#: F304 D10 adds a job's `approval_card`, D11 its mission's blocking criteria, D12 its two words,
#: D13 the calls and tokens of each job and each project's day, D16 the `job_window`), as a tree:
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
            "project_ids": {},
            "order_source_path": {},
            "order_source_sha256": {},
            "upkeep_every": {},
            "upkeep_jobs_left": {},
            "upkeep_open_findings": {},
            "upkeep_deferred_step": {},
        },
        "cost_today": {"day": {}, "value_usd": {}, "basis": {}, "harness_invocations": {},
                       "tokens": TOKENS_BY_KIND_KEY_TREE},
    },
    "jobs": {
        "job_id": {},
        "project_id": {},
        "repo_path": {},
        "mission_id": {},
        "title": {},
        "state": {},
        "waits_for_apply": {},
        "cost": {"value_usd": {}, "basis": {}},
        "harness_invocations": {},
        "model_turns": {},
        "tokens": TOKENS_BY_KIND_KEY_TREE,
        "evidence": {
            "evidence_dir": {},
            "run_ids": {},
            "postmortem_path": {},
            "run_manifest_path": {},
            "result_diff_path": {},
            "result_diff_sha256": {},
        },
        "approval_card": {
            "changed_file_count": {},
            "changed_files": {},
            "test_command": {},
            "tasks": {
                "task_id": {},
                "title": {},
                "reviewer_verdict": {},
                "repair_rounds_used": {},
                "test_ran": {},
                "test_passed": {},
            },
            "blocking_criteria": {"id": {}, "text": {}, "status": {}},
            "checks_ran": {},
            "recommendation": {},
            "risk": {},
        },
    },
    "job_window": {"ended_limit": {}, "left_out": {}},
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
        "blockers": {},
        "created_at": {},
        "age_seconds": {},
    },
    "degraded": {},
    "skipped_files": {},
}
