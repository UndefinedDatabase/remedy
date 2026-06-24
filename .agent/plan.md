# Plan — Steps 4316-4395: Human-Approved Ping-Pong Promotion v0

## Goal
Implement `remedy do promote <run_id>` — safe human-approved promotion from
reviewed staging into real target repo. No auto-promotion. No git commit/push.

## Current Step
Complete. All implementation, tests, verification done.

## Completed
- New module: packages/orchestration/pingpong_promote.py
  - _is_blocked_path(): blocks .git, .env, caches, binary, traversal, absolute
  - persist_artifacts(): save staged file contents + manifest under run dir
  - load_artifacts(): load manifest and artifact dir
  - promote_run(): full promotion with eligibility, baseline, apply, post-test
  - _persist_promotion() / load_promotion(): promotion result persistence
  - export_promotion_json() / summarize_promotion(): output formatting
- Artifact persistence in run_pingpong finally block (staged_review_passed only)
- CLI: do promote command in do_cmd.py, catalog, grouped.py
- Report integration: promotion status in text and JSON reports
- 33 new tests in test_pingpong_promote.py
- Full suite: 7287 passed, 0 failed
- Lint: clean
- Architecture guard: clean (comments-only matches, no real violations)
- Dogfood smoke: 6/6 scenarios pass (run, dry-run, unapproved, approved+test, persist, JSON)
