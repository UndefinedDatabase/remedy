# F280 Round 16 Handoff

**Feature**: F280 CLI vocabulary v2, part two  
**Round**: 16 (repair round)  
**Session**: 8  
**Branch**: feature/f280-cli-vocabulary-v2-part-two  

## Commits

| Commit | SHA | Description |
|--------|-----|-------------|
| C1 | 90438da2 | Append Gate:F280 R15 + findings R-0942/R-0943, replace plan.md |
| C2 | 75b0b192 | Fix R-0942: delete remedy_runtime_cli_smoke.py, remove Phase 1, add parse test |
| C3 | b2a4260c | Fix R-0943: guard approve action, restore CLI round-trip tests |

**Previous**: 94a37621 (F280 R15: add proposal fixture to test_decision_inbox.py)

## Changes Summary

| File | Changes |
|------|---------|
| `.agent/live_review.md` | +6 lines (Gate R15, R-0942, R-0943) |
| `.agent/plan.md` | +38 -18 (updated for round 16 scope) |
| `apps/cli/commands/decision.py` | +20 -5 (guard approve action for R-0943) |
| `scripts/remedy_backend_basis_smoke.py` | +12 -12 (remove RUNTIME_SMOKE phase, rename) |
| `scripts/remedy_runtime_cli_smoke.py` | DELETED (192 lines, no remaining purpose) |
| `tests/cli/test_smoke_scripts.py` | +10 (add ast.parse guard test) |
| `tests/orchestration/test_proposal_decision.py` | +149 (restore CLI round-trip tests) |

**Total**: 198 insertions, 229 deletions across 7 files

## Verification Results

**G1 RECORD** (after C1):
- Gates: 42 ✓
- Finding IDs: 139 ✓
- Done IDs: 7 ✓
- plan.md lines: 44 with 1x Goal, 1x Current Step, 1x Next Steps, 1x Risks ✓

**G2 R-0942 REPAIRED** (after C2):
- remedy_runtime_cli_smoke.py file absent ✓
- RUNTIME_SMOKE references: 0 ✓
- test_smoke_scripts.py: all passed (12 tests) ✓
- all scripts/*.py parse: ✓

**G3 R-0943 REPAIRED** (after C3):
- test_proposal_decision.py: all passed (14 tests) ✓
- Regression test included (approve on rejected task exits SystemExit(1), not ValueError) ✓

**G4 TARGETED TESTS + LINT** (after C3):
- Targeted suite: 215 tests passed ✓
- Ruff check: clean ✓

**G5 RED-PROOF** (disposable worktree):
- Reverted guard → test fails with ValueError ✓
- Restored guard → test passes ✓
- Worktree removed, only primary checkout remains ✓

## Findings Status

- **R-0942** (HIGH, smoke script syntax): REPAIRED in this round
- **R-0943** (MEDIUM, decision.py crash): REPAIRED in this round
- **Open findings**: 139 distinct IDs remain open (R-0942 and R-0943 resolution booked in next round R17 C1)

## Next Steps

1. Send for independent review (planner/reviewer session 9)
2. After review PASS, round 17 will:
   - Book Gate:F280 R16 PASS (C1)
   - Mark R-0942 and R-0943 DONE
   - Continue toward F280 closure sequence
3. Remaining work: confirm catalog-vs-D4 diff holds, execute closure gate sequence

## Tree State

- Clean checkout: `git status --porcelain` shows no uncommitted changes
- All commits pushed to origin
- Ready for review and merge
