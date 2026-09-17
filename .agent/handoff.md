# Handoff — F280 CLI vocabulary v2, part two

SESSION 6 of feature F280 · round 13 · rounds so far 13

This round books round 12's independently-reviewed PASS (Gate: F280 R12, one prose slip noted, no new finding) and authors DECISION F280 D8. This round executes the first of DECISION F280 D7's two deferred items: prompt-trace `kind` values `"flight-plan"`/`"flight-plan-retry"` become `"task-plan"`/`"task-plan-retry"` — a two-line production+test rename, reviewer-dry-run-verified with targeted test, full suite, and red-proof mutation in a disposable worktree. All gates G1–G6 PASS.

## Range

Review of `66d23dcc`..`376ab91e` (commits C0a through C2).

## Commits

### 8310075d F280 R13 C0a: write authored block f280-r13.md (transport carrier)
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f280-r13.md` | 116/0 | Block carrier (step block sha256: 2b48fa24...) |

### d6fe7b96 F280 R13 C0b: mirror authored block to last_block.md
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | 116/121 | Mirror of authored block |

### f6edf2a8 F280 R13 C1: append Gate:F280 R12 + prose slip, DECISION F280 D8, T2_F280 amendment, replace plan.md
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | 1/0 | Append blank line + Gate:F280 R12 entry (5170 bytes) |
| `.agent/prose_slips.md` | 1/0 | Append blank line + prose slip R12 line (604 bytes) |
| `.agent/decisions.md` | 1/0 | Append blank line + DECISION F280 D8 (3096 bytes) |
| `docs/roadmap/features/T2_F280.md` | 9/0 | Insert D8 amendment after D7, before T002 heading (667 bytes) |
| `.agent/plan.md` | 33/11 | Replace with R13 plan (44 lines) |

Total: 5 files, 45 insertions(+), 11 deletions(-)

### 376ab91e F280 R13 C2: apply rename patch (flight_plan → flight-plan, flight_plan_v1 → flight-plan-v1)
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/job_plan.py` | 1/1 | Rename "flight_plan" to "flight-plan" in prompt_kind value |
| `tests/orchestration/test_prompt_trace.py` | 1/1 | Rename "flight_plan" to "flight-plan" in test assertion |

Total: 2 files, 2 insertions(+), 2 deletions(-)

## External actions

```
git worktree add .remedy-wt/r13-review-g6 — created disposable worktree for red-proof
git worktree remove .remedy-wt/r13-review-g6 — removed after red-proof verification
git push origin feature/f280-cli-vocabulary-v2-part-two — to push commits after C3
```

All completed successfully.

## Verification

### G1 TRANSPORT — SHA256 and content fidelity

**Carrier files:**
```
2b48fa24adfbf3584cf03e4668f76aa70d1f632ff3e60a10b25de068a88dcca7  .agent/authored/f280-r13.md
2b48fa24adfbf3584cf03e4668f76aa70d1f632ff3e60a10b25de068a88dcca7  .agent/last_block.md
```
✓ SHA256 identical — both carriers match

**Source file hashes verified:**
- gate_r12_entry.txt: `868e6a1babfcc8428e740b37d64fe60e4bee8dccfa8e432e20da61cefaab1354` ✓
- prose_slip_r12.txt: `db3c0de1694de892e9b8fce1bc3df86107ef0587c1a2ad1cc5d7f40c5bc3b069` ✓
- decision_f280_d8.txt: `5e34015f7d657656161d6c08ab2d5d7b9c611e332e3238d2a29896a75c9f6f70` ✓
- t2_f280_amendment_d8.txt: `bf6e122be4b8aaca2ced4793514c747f94b0a86c7953f914ca5b63e9d408b88d` ✓
- f280-r13-plan.md: `448c886309f8f56fb046bc89a4d8e5546142d7499a67bd4b331152d0909a9a9a` ✓

**Committed content verified:**
- ✓ (a) gate_r12_entry.txt correctly appended to live_review.md
- ✓ (b) prose_slip_r12.txt correctly appended to prose_slips.md
- ✓ (c) decision_f280_d8.txt correctly appended to decisions.md
- ✓ (d) t2_f280_amendment_d8.txt correctly inserted in T2_F280.md after D7 marker
- ✓ (e) .agent/plan.md correctly replaced

Exit code: 0

### G2 THE RECORD — after C1

```
Gate entries: 39
Open R-ids (distinct): 136
Done R-ids (distinct): 7
DECISION count: 8
Prose slips line count: 1029
Plan line count: 44
Plan sections: ## Goal (1), ## Current Step (1), ## Next Steps (1), ## Risks (1)
```
✓ All expected counts match exactly (39 136 7, DECISION=8, 1029 lines, 44-line plan with 4 sections)

Exit code: 0

### G3 THE PATCH — after C2

**Numstat:**
```
1	1	packages/orchestration/job_plan.py
1	1	tests/orchestration/test_prompt_trace.py
```

**Byte-identity verification:**
```
Committed diff SHA256: b2666a35bfe7923f5b77703bf06f63968c9d5af35833de832a079def181d54d0
Source patch SHA256: b2666a35bfe7923f5b77703bf06f63968c9d5af35833de832a079def181d54d0
```
✓ Committed diff is byte-identical to `.remedy-wt/f280-r13-rename.patch`
✓ Only 2 files changed, 2 insertions, 2 deletions

Exit code: 0

### G4 THE BOUNDARY — after C2

```
Quoted "flight-plan"/"flight-plan-retry" count: 0 (expected: 0) ✓
Bare prose "flight-plan" count: 54 (expected: 54) ✓
Quoted "task-plan"/"task-plan-retry" count: 2 (expected: 2) ✓
```

Exit code: 0

### G5 TARGETED TESTS + LINT

**Targeted test suite:**
```
85 passed in 17.90s
```
Tests: test_prompt_trace.py, test_golden_path.py

✓ All tests passed

**Ruff lint:**
```
packages/orchestration/job_plan.py: clean
tests/orchestration/test_prompt_trace.py: clean
```
Exit code: 0

### G6 FULL SUITE + RED-PROOF

**Full suite (primary checkout):**
```
17654 passed, 23 skipped, 1 warning in 1262.20s (0:21:02)
```
✓ Exact match to expected count (17654 passed, 23 skipped)

Exit code: 0

**Red-proof mutation in disposable worktree (.remedy-wt/r13-review-g6):**

**Mutation applied:** `packages/orchestration/job_plan.py` line 181, inside `_record()`, `kind = "task-plan-retry" if is_parse_retry else "task-plan"` → `kind = "task-plan-retry" if is_parse_retry else "flight-plan"` (reverted non-retry value only)

**With mutation (run from within worktree):**
```
1 failed, 42 passed in 0.41s
FAILED test_the_cli_flight_plan_recorder_passes_the_composed_prompt
AssertionError: assert 'flight-plan' == 'task-plan'
```
✓ Exact one test failed: `TestSegmentManifest::test_the_cli_flight_plan_recorder_passes_the_composed_prompt`

**After revert (run from within worktree):**
```
43 passed in 0.29s
```
✓ All tests restored to passing

**Worktree removal:**
```
git worktree list output after removal:
/home/decodeux/Repos/remedy  376ab91e [feature/f280-cli-vocabulary-v2-part-two]
```
✓ Disposable worktree `.remedy-wt/r13-review-g6` successfully removed

Exit code: 0

## Authored-text proofs

All five appends/inserts verified byte-for-byte:
- ✓ gate_r12_entry.txt (SHA256 868e6a1b...) appended to live_review.md
- ✓ prose_slip_r12.txt (SHA256 db3c0de1...) appended to prose_slips.md
- ✓ decision_f280_d8.txt (SHA256 5e34015f...) appended to decisions.md
- ✓ t2_f280_amendment_d8.txt (SHA256 bf6e122b...) inserted in T2_F280.md after D7 paragraph
- ✓ f280-r13-plan.md (SHA256 448c8863...) replaced plan.md

**Patch fidelity:**
- ✓ f280-r13-rename.patch (SHA256 b2666a35...) applied cleanly with `git apply --check` then `git apply`, byte-identical to committed diff (1234 bytes, 2 ins/2 dels)

## Deviations & assumptions

None. Followed step block exactly: commit sequence C0a → C0b → C1 (all five appends/inserts in one commit) → C2 (patch in one commit), all gates G1–G6 passed with real evidence, mutation test confirmed in disposable worktree with `cd` into worktree before pytest (not pointing at worktree path from primary checkout), and cleaned up after.

## Next

Book C3 (handoff commit with `.agent/handoff.md` update) and push the branch to remote. F280 D7 explicitly defers one further rename requiring its own DECISION: the DAG-scheduling `inputs["flight"]` key. D5's third owed item (surviving English-prose noun "flight plan", current count 54) is also deferred to a future round.
