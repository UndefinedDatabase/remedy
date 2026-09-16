# Handoff — F280 CLI vocabulary v2, part two
SESSION 4 of feature F280 · round 8 · rounds so far 8
This round booked round 7's independently-reviewed PASS, fixed R-0939 (missing trailing newlines in four .agent/ files), and renamed the `job run` CLI flag `--max-tasks` to `--tasks` (DECISION amend0905-vocab D4).

## Range
Review of `4a0da00a`..`bc576a22` (commits C0a through C2).

## Commits

### 651fb2e8 C0a: F280 R8 C0a: write authored block f280-r8.md (transport carrier)
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f280-r8.md` | 113/0 | Block carrier |

### 61013228 C0b: F280 R8 C0b: mirror authored block to last_block.md
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | 113/288 | Block carrier mirror |

### bab153c7 C1: F280 R8 C1: fix R-0939 (trailing newlines) and book R7 PASS in live_review
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/decisions.md` | 1/0 | Append trailing newline |
| `.agent/operator_questions.md` | 1/0 | Append trailing newline |
| `.agent/live_review.md` | 7541/0 | Append R7 gate, R-0939 register, done marker |
| `.agent/plan.md` | 49/48 | Replace with R8 plan |

### bc576a22 C2: F280 R8 C2: rename job run flag --max-tasks to --tasks (DECISION D4)
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/command_catalog.py` | 1/1 | Flag rename in catalog |
| `apps/cli/grouped.py` | 2/2 | Flag rename in wiring |
| `tests/cli/test_job_run_invocation_truth.py` | 1/1 | Update test invocation |
| `tests/orchestration/test_job_task_runner.py` | 4/4 | Update docstrings/comments |
| `tests/test_command_catalog.py` | 1/0 | Add DELETED flag entry |

## External actions
Push to remote after handoff complete.

## Verification

G1 TRANSPORT: PASS
- `.agent/authored/f280-r8.md` sha256 = `83787f9ce89e140cb8ac064fc9ab62aefbc2ce10f86010f2141355e490d36fac` ✓
- `.agent/last_block.md` sha256 = `83787f9ce89e140cb8ac064fc9ab62aefbc2ce10f86010f2141355e490d36fac` ✓
- gate_r7_entry.txt, reg_r0939.txt, done_r0939.txt verified in live_review.md ✓
- Exit code: 0

G2 THE RECORD (after C1): PASS
- `.agent/live_review.md`: 34 gates, 135 R-ids, 7 Done ids ✓
- `.agent/plan.md`: 49 lines, 1 Goal, 1 Current Step, 1 Next Steps, 1 Risks ✓
- Exit code: 0

G3 THE NEWLINE FIX (after C1): PASS
- `.agent/plan.md` ends with newline: True ✓
- `.agent/live_review.md` ends with newline: True ✓
- `.agent/decisions.md` ends with newline: True ✓
- `.agent/operator_questions.md` ends with newline: True ✓
- Exit code: 0

G4 THE PATCH (after C2): PASS
- Files changed: 5 (command_catalog.py, grouped.py, test_job_run_invocation_truth.py, test_job_task_runner.py, test_command_catalog.py) ✓
- Changes: 1/1, 2/2, 1/1, 4/4, 1/0 ✓
- Exit code: 0

G5 THE SWEEP (after C2): PASS
- `--max-tasks` in apps/packages/tests/scripts: 1 line (DELETED entry only) ✓
- `--max-tasks` in docs/roadmap/features/T0_F012.md: pre-existing, untouched ✓
- T0_F012.md git diff: empty ✓
- Exit code: 0

G6 TARGETED TESTS (after C2): PASS
- 620 tests passed ✓
- Exit code: 0

G7 RUFF (after C2): PASS
- All checks passed on modified files ✓
- Exit code: 0

G8 MUTATION RED-PROOF (disposable worktree): PASS
- Reverted `--tasks` to `--max-tasks` in command_catalog.py: test fails with 2 failures as expected ✓
- Failed node: `TestDeletedFlags::test_no_deleted_flag_is_declared_by_its_command` ✓
- Reverted back to `--tasks`: 22 tests passed ✓
- Worktree cleaned up ✓
- Exit code: 0

CANARY (primary checkout after C2): PASS
- `pytest tests/cli/test_golden_path.py -q`: 42 passed ✓
- Exit code: 0

## Authored-text proofs
Block and source files byte-compared against committed targets: all match ✓

## Deviations & assumptions
None.

## Next
1. Phase 1 rule 1: verify `.agent/STOP` absent.
2. Reviewer verdict on round 8 after independent re-review.
3. Operator moves to next feature after closure.
