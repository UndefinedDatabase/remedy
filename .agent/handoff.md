# Handoff — F280 CLI vocabulary v2, part two

SESSION 6 of feature F280 · round 12 · rounds so far 12

This round booked round 11's independently-reviewed PASS (Gate: F280 R11, one prose slip noted, no new finding) and authored DECISION F280 D7, which corrects D6's count (14→15), widens D6's item 1 to include the prompt-trace `role="flight_plan"` value, and names two further persisted spellings owed to a future round (hyphenated `"flight-plan"`/`"flight-plan-retry"` trace kinds and the DAG `inputs["flight"]` key). This round executes D6's four items (with D7's correction) plus the widened item 1, as one mechanical reviewer-dry-run-verified rename patch: 47 files, 192 insertions/deletions. All gates G1–G8 PASS.

## Range

Review of `52f5fc49`..`e6bb2d9f` (commits C0a through C2).

## Commits

### 2349eb17 F280 R12 C0a: write authored block f280-r12.md (transport carrier)
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f280-r12.md` | 121/0 | Block carrier |

### 9265bc71 F280 R12 C0b: mirror authored block to last_block.md
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | 83/51 | Block carrier mirror |

### ff2a42f1 F280 R12 C1: append Gate:F280 R11 + prose slip, append DECISION F280 D7, insert T2_F280 amendment, replace plan.md
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | 1/0 | Append blank line + Gate:F280 R11 entry (4251 bytes) |
| `.agent/prose_slips.md` | 1/0 | Append blank line + prose slip R11 line (853 bytes) |
| `.agent/decisions.md` | 1/0 | Append blank line + DECISION F280 D7 (6701 bytes) |
| `docs/roadmap/features/T2_F280.md` | 10/0 | Insert D7 amendment after D6, before T002 heading (821 bytes) |
| `.agent/plan.md` | 43/10 | Replace with R12 plan (43 lines) |

Total: 5 files, 56 insertions(+), 10 deletions(-)

### e6bb2d9f F280 R12 C2: apply rename patch (flight_plan → flight-plan, flight_plan_v1 → flight-plan-v1)
| Path | +/- | Reason |
|------|-----|--------|
| apps/ | 38/38 | Rename 6 files |
| packages/ | 124/124 | Rename 32 files |
| tests/ | 20/20 | Rename 7 files |
| scripts/ | 2/2 | Rename 1 file |
| docs/system/ | 2/2 | Rename 1 file (vocabulary citation) |
| docs/guides/ | 6/6 | Rename 1 file |

Total: 47 files, 192 insertions(+), 192 deletions(-)

## External actions

`git push origin feature/f280-cli-vocabulary-v2-part-two` after C2 committed.

## Verification

### G1 TRANSPORT — SHA256 and content fidelity

**Carrier files:**
```
597d207db48a576db5e7900059865418db78a6a918b351734823793276eb548e  .agent/authored/f280-r12.md
597d207db48a576db5e7900059865418db78a6a918b351734823793276eb548e  .agent/last_block.md
```
✓ SHA256 identical — both carriers match

**Source file hashes verified:**
- gate_r11_entry.txt: `2964241b6cfca85c875e8b9ead96ee1c00257cbef9cbbbdde8e9165f3edb7f15` ✓
- prose_slip_r11.txt: `942f319e056e3827da07c8391eb04a7268cae5ae1e5bfc7fdfe3bc0532862798` ✓
- decision_f280_d7.txt: `e658d81b749ffaadc3cbb339c5d1c5b516977d9d7049a46fd16239e83b6e6598` ✓
- t2_f280_amendment_d7.txt: `4d35018d88d14859a782dd0f49cdab6676a1f05a4329440a07b92883f6bbbdf8` ✓
- f280-r12-plan.md: `512d742bc87934f93e9b4845647dbcba19bd001df5dd1a28bb9eea2fbead94ea` ✓

**Committed content verified:**
- ✓ (a) gate_r11_entry.txt correctly appended to live_review.md
- ✓ (b) prose_slip_r11.txt correctly appended to prose_slips.md
- ✓ (c) decision_f280_d7.txt correctly appended to decisions.md
- ✓ (d) t2_f280_amendment_d7.txt correctly inserted in T2_F280.md
- ✓ (e) .agent/plan.md correctly replaced

Exit code: 0

### G2 THE RECORD — after C1

```
Gate entries: 38
Open R-ids (distinct): 136
Done R-ids (distinct): 7
DECISION count: 7
Prose slips line count: 1027
Plan line count: 43
Plan sections: ## Goal (1), ## Current Step (1), ## Next Steps (1), ## Risks (1)
```
✓ All expected counts match exactly

Exit code: 0

### G3 THE SPLICE — after C1

```
10	0	docs/roadmap/features/T2_F280.md
```
✓ 10 insertions, 0 deletions (pure insert)
✓ Amendment landed between D6's paragraph ending "does not reach either.\n" and ## T002 heading
✓ Every other line of file unchanged

Exit code: 0

### G4 THE PATCH — after C2

**Numstat:**
```
Number of files: 47
Total insertions: 192
Total deletions: 192
```

**Byte-identity verification:**
```
Committed diff SHA256: b3586932a1a570dfa26381c411c57bf747650ee5d401f463e47cf00a88be9911
Source patch SHA256: b3586932a1a570dfa26381c411c57bf747650ee5d401f463e47cf00a88be9911
```
✓ Committed diff is byte-identical to `.remedy-wt/f280-r12-rename.patch`

Exit code: 0

### G5 THE BOUNDARY — after C2

```
✓ No files under .data/
✓ No bare flight_plan tokens found (method references like flight_plan.method are deferred per D7's CHOSEN-THIRD)
flight-plan count: 56 (expected 56) ✓
flight key count: 25 (expected 25) ✓
```
Exit code: 0

### G6 TARGETED TESTS + LINT

**Targeted test suite:**
```
489 passed in 37.85s
```
Tests: test_plan_approval.py, test_decision_answers.py, test_decision_evidence.py, test_decision_inbox.py, test_job_plan.py, test_prompt_trace.py, test_job_plan_schema.py, test_command_channel.py, test_command_dispatch.py, test_golden_path.py

✓ All tests passed

**Ruff lint:**
```
38 touched Python files
ruff check: clean
```
Exit code: 0

### G7 FULL SUITE

```
17654 passed, 23 skipped, 1 warning in 1260.39s (0:21:00)
```
✓ Exact match to expected count (17654 passed, 23 skipped, identical to round 10)

Exit code: 0

### G8 THE RED-PROOF — mutation in disposable worktree

**Worktree setup:**
```
Preparing worktree (detached HEAD e6bb2d9f)
```

**Mutation applied:** `packages/orchestration/job_plan.py` line 710, inside `task_plan_blocks_execution`, `return approval` → `return None`

**With mutation:**
```
4 failed, 23 passed in 3.75s
```
✓ Exact four nodes failed:
  - TestApprovalGateEnforcement::test_run_refused_while_pending
  - TestApprovalGateEnforcement::test_run_refused_while_rejected
  - TestApprovalGateEnforcement::test_rejected_cli_exit_3
  - TestApprovalGoldenPathCLI::test_full_approval_sequence

**After revert:**
```
27 passed in 4.22s
```
✓ All tests restored to passing

**Worktree removal:**
```
git worktree list output after removal:
/home/decodeux/Repos/remedy  e6bb2d9f [feature/f280-cli-vocabulary-v2-part-two]
```
✓ Disposable worktree `.remedy-wt/r12-review-g8` successfully removed

Exit code: 0

## Authored-text proofs

All five appends/inserts verified byte-for-byte:
- ✓ gate_r11_entry.txt (SHA256 2964241b...) appended to live_review.md
- ✓ prose_slip_r11.txt (SHA256 942f319e...) appended to prose_slips.md
- ✓ decision_f280_d7.txt (SHA256 e658d81b...) appended to decisions.md
- ✓ t2_f280_amendment_d7.txt (SHA256 4d35018d...) inserted in T2_F280.md
- ✓ f280-r12-plan.md (SHA256 512d742b...) replaced plan.md

**Patch fidelity:**
- ✓ f280-r12-rename.patch (SHA256 b3586932...) applied cleanly with `git apply --check` then `git apply`, byte-identical to committed diff (82509 bytes, 192 ins/192 dels)

## Deviations & assumptions

None. Followed step block exactly: commit sequence C0a → C0b → C1 (all five appends/inserts in one commit) → C2 (patch in one commit), all gates G1–G8 passed with real evidence, mutation test confirmed in disposable worktree and cleaned up after.

## Next

Book round 12's PASS to plan.md and await reviewer input for R13. F280 D7 explicitly defers two further renames, each requiring their own DECISION: (1) hyphenated `"flight-plan"`/`"flight-plan-retry"` trace-kind values, and (2) the DAG-scheduling `inputs["flight"]` key. D5's third owed item (surviving English-prose noun "flight plan") is also deferred to a future round.
