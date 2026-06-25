# Plan — Steps 4799-4806: CLI Repair Default Truth Closure v5

## Goal
Fix CLI dispatch so omitted --repair-rounds stays None (default=2), not coerced to 0.

## Current Step
Complete. All implementation, tests, verification done.

## Completed
- Step 4799: Removed `int(... or 0)` coercion; omitted --repair-rounds passes None
- Step 4800: CLI dispatch test: omitted → None
- Step 4801: CLI dispatch test: explicit 0 → 0
- Step 4802: CLI dispatch test: explicit 1 → 1
- Step 4803: Catalog help text verified: "default: 2, cap: 10; 0 disables repair"
- Step 4804: Existing resolver tests preserved (7 tests)
- Step 4805: All repair governance + test-evidence dominance tests pass
- Step 4806: Architecture guard clean, full suite 7677 passed
- 6 new tests (131 total in test_repair_loop.py)
- Full suite: 7677 passed, 0 failed
- Lint: ruff clean, compileall clean
