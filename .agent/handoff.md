# F280 Round 17 Handoff

**Feature**: F280 CLI vocabulary v2, part two  
**Round**: 17 (fix and widen test round)  
**Session**: 9  
**Branch**: feature/f280-cli-vocabulary-v2-part-two  

## Commits

| Commit | SHA | Description |
|--------|-----|-------------|
| C1 | d0d331b6 | Append Gate:F280 R16 + Done:R-0942 + Done:R-0943 + finding R-0944, replace plan.md |
| C2 | 91876a2d | Fix R-0944: mission group visibility, widen group integrity test |

**Previous**: e1c140a2 (F280 R16 handback: repair R-0942 and R-0943)

## Changes Summary

| File | Changes |
|------|---------|
| `.agent/live_review.md` | +184 lines (Gate R16 entry, Done R-0942, Done R-0943, finding R-0944) |
| `.agent/plan.md` | +1 -44 (updated for round 17 scope) |
| `.agent/authored/f280-r17.md` | +78 (step block for this round) |
| `.agent/last_block.md` | +78 (mirrored step block) |
| `apps/cli/command_catalog.py` | -1 (removed user_facing=False from mission) |
| `tests/cli/test_cli_ux.py` | +20 -4 (widened partition constants, added new test) |

**Total**: 356 insertions, 49 deletions across 6 files

## Verification Results

**G1 RECORD** (after C1):
- Gates: 43 ✓
- Finding IDs: 140 ✓
- Done IDs: 9 ✓
- plan.md lines: 45 with 1x Goal, 1x Current Step, 1x Next Steps, 1x Risks ✓

**G2 R-0944 REPAIRED** (after C2):
- mission.user_facing: True (not False) ✓
- Visible groups: exactly 16 as D4 specifies ✓
- Advanced groups: exactly 12 as D4 specifies ✓
- Hidden groups: exactly 1 (roadmap) ✓
- Partition assertion: passed (output: "partition matches D4") ✓

**G3 TARGETED TESTS + LINT** (after C2):
- pytest tests/cli/test_cli_ux.py tests/test_command_catalog.py tests/cli/test_golden_path.py: 169 passed ✓
- Ruff check apps/cli/command_catalog.py tests/cli/test_cli_ux.py: clean ✓

**G4 RED-PROOF** (disposable worktree .remedy-wt/g4-redproof):
- Reverted fix (user_facing=False back on mission) → test_catalog_partition_matches_d4 fails ✓
- Restored fix → test passes ✓
- Worktree removed, only primary checkout remains ✓

## Findings Status

- **R-0942** (HIGH, smoke script syntax): BOOKED DONE in this round (repaired R16)
- **R-0943** (MEDIUM, decision.py crash): BOOKED DONE in this round (repaired R16)
- **R-0944** (MEDIUM, mission visibility + test): FIXED in this round
- **Open findings**: 131 distinct IDs remain open (140 registered minus 9 resolved)

## Changes Description

### C1: Record Booking and New Finding Registration
- Books Gate:F280 R16 independently-reviewed PASS (no new finding)
- Resolves and closes R-0942 (smoke script parsing, repaired in round 16)
- Resolves and closes R-0943 (decision.py approve action guard, repaired in round 16)
- Registers R-0944 (Medium): mission group visibility contradicts DECISION amend0905-vocab D4, and test coverage is insufficient

### C2: Fix R-0944 and Widen Guard Test
- Removes `user_facing=False` from mission GroupDef in command_catalog.py (default is True)
- Widens `_USER_FACING_GROUPS` constant from 8 to 16 groups (full D4 visible list)
- Widens `_INTERNAL_GROUPS` constant from 2 to 12 groups (full D4 advanced list)
- Adds test_catalog_partition_matches_d4 to TestGroupDefIntegrity asserting:
  - Catalog carries exactly 29 groups
  - Only roadmap has hidden=True
  - visible/advanced partition matches D4 exactly

## Implementation Notes

**R-0944 Fix Rationale**:
- The mission group controls mission-related commands already documented and working
- Moving mission from advanced-only to visible-by-default improves discoverability
- DECISION amend0905-vocab D4 explicitly names mission in the visible groups list
- No other group's description, label, or command order was modified (per constraints)

**Test Coverage Expansion**:
- Old constants covered only 8 visible + 2 advanced = 10 of 29 groups
- New constants cover all 16 visible + 12 advanced groups
- New test directly asserts the full partition, preventing future drift
- When a group's visibility changes, the test fails immediately

## Tree State

- Clean checkout: `git status --porcelain` shows no uncommitted changes
- No disposable worktrees remain: `git worktree list` shows only primary
- Ready for independent review (planner/reviewer of session 9+)

## Next Steps

1. Independent review by planner/reviewer (DECISION amend0905-vocab D4 coverage)
2. If review confirms PASS with no new findings:
   - T001 and Acceptance list both hold
   - Next round begins F280's closure sequence:
     - Integration gate round (full suite once)
     - Self-use precondition verification
     - Evidence job and review zip generation
3. If review finds issues:
   - Record findings, fix in new round(s)
   - Closure deferred until all findings are resolved
