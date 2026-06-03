# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 383-390: Pytest wrapper exit-code fix, wrapper behavior tests, builder eval harness.

## Completed
- Pytest wrapper exit-code fix: `set +e` / `$?` / `set -e` pattern (was masking failures as success)
- Wrapper behavior tests: 6 tests (pass/fail/nonexistent/timeout/lock-busy/lock-message)
- Builder eval harness: packages/orchestration/builder_eval.py
- Standard eval cases: 9 categories (valid_file_op, valid_diff, prose, malformed, wrapper, unsafe_path, shell, no_text, empty)
- Prompt variant comparison: run_fixture_eval supports variant labeling
- Small-repo eval fixtures: missing_function, wrong_return, repair_cycle1/2, unsafe_path
- Real Ollama eval: opt-in via REMEDY_REAL_OLLAMA_EVAL=1, skips cleanly
- Eval CLI script: scripts/remedy_builder_eval.sh (--fixture, --ollama, --json)
- Eval report: safe metadata only, no raw content, redaction field on all records
- Handoff truth: live_review.md Steps 375-382 status consistent

## Resource-Safety Rules (permanent)
- Never run pytest in background
- Never run multiple pytest commands in parallel
- Always use scripts/remedy_pytest.sh for pytest execution
- Full pytest tests/ at most once per worker block
- Wrapper uses flock -n + timeout, propagates exit codes truthfully

## Constraints
- UI remains read-only
- Resume only from source_apply_proven (from_apply → tests) in v1
- No from_approval resume until patch persistence
- source_apply requires permission + approved intent

## Remaining Risks
- from_approval blocked until structured patch payload persistence
- Repair resume blocked until implementation
- Background worker not implemented
- Fixture eval shows 33% parse success — reflects that most standard cases are intentional failures

## Recommended Next Block
Steps 391-398 — Real-Ollama Prompt Iteration And Model Routing
