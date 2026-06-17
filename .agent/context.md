# Context

## Active Branch
feature/steps-2696-2715-fast-lane-runtime-split-v0.1
(forked from main at 21fa4bc after PR #89 merged).

## Scope
Steps 2696-2715: Fast lane runtime split + doctor core safety closure.
Split subprocess-heavy tests into runtime lane. Harden error redaction. No new features.

## Changed Line Map
| File | Lines | Symbols | Purpose | Risk |
|------|-------|---------|---------|------|
| `remedy_test_fast.sh` | rewrite | — | Pure in-process only (6 files, removed 4 subprocess) | LOW |
| `remedy_test_runtime.sh` | NEW | — | 4 subprocess-heavy CLI integration files | LOW |
| `worker_facade_cmd.py` | +8 | `_safe_err` | Regex path redaction + key=value secret scrub | LOW |
| `test_worker_facade_cmd.py` | +65 | `TestDoctorCoreSafeErr` (3 tests) | Path + secret + mnt/tmp/Users redaction | LOW |
| `test_product_spine.py` | +22 | 4 new tests | Subprocess exclusion + runtime lane checks | LOW |
| `test_test_categories.py` | +30 | 5 new tests | Subprocess exclusion + runtime lane checks | LOW |
| `test-lanes-v0.md` | +20/-13 | — | Added runtime lane section, updated fast lane | LOW |
| `plan.md` | rewrite | — | Builder metadata | LOW |
| `context.md` | rewrite | — | Builder metadata | LOW |
| `live_review.md` | rewrite | — | Reviewer metadata | LOW |

## Test evidence
- Fast lane: 395 passed, 0.60s (pure in-process)
- Runtime lane: 54 passed, 6.24s (CLI integration)
- Lint: 0 issues (ruff + mypy, 191 files)
- Full suite: 6876 passed, 8 skipped, 0 failures (205.62s)

## Resource safety
All pytest runs use scripts/remedy_pytest.sh (flock-serialized, timeout-bounded).
No shell=True. No background pytest.
