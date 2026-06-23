# Plan — Steps 4076-4145: Claude CLI Safety Closure v1

## Goal
Make first real local Claude CLI staged self-run safe. Fix staging-cwd blocker,
add target snapshot guard, external run storage, no-test honesty, JSON UX.

## Current Step
Complete. All implementation, tests, verification done.

## Completed
- Builder ClaudeCliProvider runs with cwd=staging_dir (not target repo)
- Reviewer ClaudeCliProvider runs without cwd (read-only, prompt-only)
- Target snapshot guard: before/after hash comparison blocks any target mutation
- Run storage moved to Remedy data root (resolve_data_root()/pingpong_runs/)
- No-test behavior: test_passed=None, test_summary="tests_not_run", tests_not_run=true
- JSON export includes report_command, report_json_command, report_path, tests_not_run
- Reviewer staging mutation detection
- 34 E2E tests covering all 23 required cases + regression reproduction
- Real Claude CLI smoke: ran on temp repo, target_mutated=false
- Full suite: 7247 passed, 0 failed, 8 skipped
- Fast lane: 571 passed
- Runtime lane: 4/4 suites
- Lint: ruff clean, mypy clean (196 files)
- Fulfillment: 109 passed x2

## Risks
- Real Claude CLI builder could not write in non-interactive mode (expected)
