# Plan — Steps 4832-4844: Job Runner Correctness + Token Context Policy v1

## Goal
Fix correctness issues in Job Task Runner v0 and add token context policy.

## Current Step
Complete. All implementation, tests, verification done.

## Completed
- Step 4832: CLI command truth — all next_command uses hyphens (job-run, job-report, job-plan)
- Step 4833: CLI E2E tests — catalog, handlers, next_command copy-pasteability
- Step 4834: Deterministic task IDs by parse order (T001, T002, ...), source_heading_number stored
- Step 4835: Strict workspace apply manifest — missing/duplicate/traversal/unsafe paths block
- Step 4836: Reused promotion safety — path validation via _is_unsafe_path()
- Step 4837: Job-level target repo snapshot guard — _snapshot_target_repo/_check_target_repo_guard
- Step 4838: Task completion gate — requires review pass + strict apply + target guard
- Step 4839: Per-task proof summaries — TaskProofSummary dataclass persisted
- Step 4840: Token context policy — task_bounded_sequential_job, previous_summary_limit=5
- Step 4841: Token-bounded prompt tests — body truncation, summary bounding, no full body carryover
- Step 4842: Blocking-path E2E tests — missing/env/traversal/duplicate all block
- Step 4843: All existing flows preserved — 7807 passed full suite
- Step 4844: Architecture guard clean, lint clean, mypy clean
