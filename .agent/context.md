# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 375-382: Resource-safe pytest harness, reviewer safety protocol, handoff truth.

## Completed
- Guarded pytest wrapper: scripts/remedy_pytest.sh (flock -n, timeout, foreground-only)
- Resource-safety policy: docs/reviewer-safety.md
- Reviewer protocol: no repeated full pytest, targeted tests during dev, one baseline at handoff
- Test command matrix: standardized in docs/reviewer-safety.md
- Emergency cleanup guidance: process inspection + kill instructions
- Handoff truth: live_review.md Steps 367-374 status corrected to PASS
- Resource-safety regression tests: 13 tests in tests/regression/test_resource_safety.py
- tests/README.md updated with wrapper instructions and safety section

## Resource-Safety Rules (permanent)
- Never run pytest in background (no run_in_background, no &, no nohup)
- Never run multiple pytest commands in parallel
- Always use scripts/remedy_pytest.sh for pytest execution
- Full pytest tests/ at most once per worker block
- Reviewers must not repeatedly run full baseline in watcher loop
- The wrapper uses flock -n to fail fast if lock is busy

## Constraints
- UI remains read-only
- Resume only from source_apply_proven (from_apply → tests) in v1
- No from_approval resume until patch persistence
- source_apply requires permission + approved intent

## Remaining Risks
- from_approval blocked until structured patch payload persistence
- Repair resume blocked until implementation
- Background worker not implemented

## Recommended Next Block
Steps 383-390 — Builder Prompt Quality And Real-Ollama Hardening
