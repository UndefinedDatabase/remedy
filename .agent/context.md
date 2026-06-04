# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 565-579: Orchestrator task evaluation flow.
UI/timeline work is PAUSED. Backend/orchestration only.

## Canonical Review File
`.agent/live_review.md` — NOT `.data/live_review.md`

## Core Concept
When a reviewer finds a new issue, Remedy creates a proposed task.
Proposed tasks must be evaluated before implementation.
Only approved tasks become buildable.
Finalized is blocked while unresolved proposed tasks exist.

## Key Patterns
- Job persistence: `storage.py` save_job/load_job → `.data/jobs/{job_id}.json`
- Event ledger: `run_log.py` RunLogWriter → `.data/runs/<job_id>/<run_id>.jsonl`
- CLI commands: `command_catalog.py` CATALOG tuple + GROUPS dict
- Reviewer: `reviewer.py` ReviewerRecommendation → accept/reject flow
- Worker queue: `worker_queue.py` get_next_job selects `lifecycle_state == "queued"`

## What Must Change
- New ProposedTask domain model (dataclass in proposed_tasks.py)
- Proposed task store (JSON persistence in .data/)
- Review → proposal flow (reviewer creates proposed tasks, not direct tasks)
- Deterministic evaluator (rules-based, no LLM by default)
- State transitions: proposed → evaluated → approved_for_build | rejected | deferred
- Build queue gate: only approved tasks enter build
- Finalized gate: blocked by unresolved proposals
- CLI commands for propose/evaluate/approve/reject/defer/list
- Event audit trail via RunLogWriter

## Resource Safety
All pytest runs use scripts/remedy_pytest.sh (flock + timeout).
