# Plan — Steps 3606-3655: Staged Test + Promotion Truth Closure v0.4

## Goal
Close remaining staging safety gaps: tests run against staging dir (not target),
code_applied truth tied to promotion, blocked jobs expose blockers, promotion-first
contract ordering, existing MD files use modify intent, review bundle includes
fulfillment summary, demo docs commands valid, data_dir threaded consistently.

## Current Step
Complete. All implementation, tests (90 fulfillment, 2127+ total), and fixes done.

## Completed
- Contract: requires_target_promotion field + target_not_promoted/no_promotion_files blockers
- Promotion-first ordering: promote → record result → contract check → completion decision
- Existing MD detection: fixture worker checks (repo_root / target_file).exists() → modify vs create
- CLI truth: staging_promoted authoritative for code_applied; fulfillment_blockers + next_action surfaced
- Review bundle: fulfillment_summary.json section with staging/promotion/contract truth
- Demo docs: job create --json → JOB_ID=$(remedy job create "...")
- test_execution_service: data_dir threaded through _persist_test_record, _create_failure_artifact, finalize_test_outcome
- Tests: updated contract tests for requires_target_promotion, fixed COMMANDS→COMMAND_HANDLERS import, updated apply_blocked test to reflect modify intent fix
- Full suite: 2127+ passed (1 pre-existing failure in test_project_brain unrelated)

## Risks
- None remaining
