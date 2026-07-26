# Handoff — F016 Scaling task granularity — round 1 (T001–T003)

Review of dcb8b1a..HEAD

## State
- Branch: `feature/f016-task-granularity` (pushed)
- Base: `dcb8b1a` (merge of PR #149 into main, via Open PR Gate)
- STATUS.md: F016 claimed `[~]`
- live_review.md: reset for F016, finding IDs continue at R-0141
- Evidence bundle / review zip: not built this round (not ordered)

## Item-Status Table
| Item | Status | Reason |
|------|--------|--------|
| T001 split rules + config + table tests | done | |
| T002 merge rule + dependency-safety tests | done | |
| T003 revalidation + wiring + integration | done | |

## Commits
| SHA | Subject |
|-----|---------|
| 88911bd | chore(f016): claim F016, reset live review and plan |
| 8b5360c | feat(f016): pure split heuristic + planning config keys |
| 6513fca | test(f016): table-driven split cases |
| fc2e219 | feat(f016): merge rule for trivial neighbors |
| 51e2575 | feat(f016): revalidate, wire normalization into plan generation |

## Changed files (net)
| File | Change |
|------|--------|
| packages/orchestration/task_granularity.py | new, pure module (no I/O) |
| packages/orchestration/config.py | 4 keys under `planning.granularity.*` |
| packages/orchestration/flight_plan.py | wiring, record on FlightPlanResult, plan.md section |
| apps/cli/commands/do_cmd.py | `_normalization` persisted at both call sites |
| tests/orchestration/test_task_granularity.py | new, 26 tests |
| tests/orchestration/test_flight_plan.py | +6 normalization/wiring tests |
| tests/orchestration/test_config.py | +5 key tests |
| tests/cli/test_plan_approval.py | +1 CLI persistence test |
| docs/system/remedy-toml-configuration-system-v0.md | new keys documented |

## Verification (raw, all exit 0)
- `pytest tests/orchestration/test_task_granularity.py -q` → 26 passed
- `pytest tests/orchestration/test_config.py -q` → 62 passed
- `pytest tests/orchestration/test_flight_plan.py -q` → 29 passed
- `pytest tests/cli/test_plan_approval.py -q` → 27 passed
- `pytest tests/orchestration/schemas/test_schemas.py -q` → 44 passed
- `pytest tests/cli/test_golden_path.py -q` (canary) → 42 passed
- Full suite NOT run this round (scoped round gate per §3 tiers).
- `ruff check` clean on all touched files; 6 pre-existing import-order
  errors in tests/cli/test_plan_approval.py were confirmed present on the
  base commit and left alone.

## Open findings
None (R-0141+ unused).

## Next expected action
Reviewer round on `dcb8b1a..HEAD`.
