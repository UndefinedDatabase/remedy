# F280 R4 Handback

## SESSION
SESSION 2 of feature F280 · round 4 · rounds so far 1

## RANGE
Review of f478cac4..af468d9e

## COMMITS

### 645caa61 F280 R4 C0a/C0b: stage the round 4 block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f280-r4.md | 446 | Block file transport |
| .agent/last_block.md | 315 | Block mirror |

### f478cac4 F280 R4 C1: book round 3 PASS with R-0906 and R-0909 resolutions
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | 44 | PLAN4 full replacement |
| .agent/live_review.md | 6 | RECORD4 append |

### af468d9e F280 R4 C2: move job-creation test fixtures off job create CLI word to direct call
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f280-r4-jobcreate.jsonl | 5 | Carrier copy |
| tests/test_test_runner.py | 2 | Direct _cmd_create_job call |
| tests/orchestration/test_test_runner.py | 2 | Direct _cmd_create_job call |
| tests/test_command_discovery.py | 4 | Two direct _cmd_create_job calls |
| scripts/remedy_smoke.sh | 10 | Direct _cmd_create_job call with env vars |

## EXTERNAL ACTIONS
None

## VERIFICATION

### G1 TRANSPORT
Exit code: 0
- SHA256 .agent/authored/f280-r4.md: 09931a283ed0b7331005eea91f38157c91a60c638db707a8c78e408700905585 (match)
- .agent/last_block.md byte-identical: True
- Carrier SHA256: 24e4d530540d314d56130ef1852fa669f4947b805f45d0b8a1398f3cea04875f (match)

### G2 THE RECORD
Exit code: 0
- .agent/plan.md SHA256: 5f6e961c2a9af595c97849a27e403844fb1d40b5ee353fb4232ac7dfe3fb0c6e (match)
- Line count: 44 (max 50) ✓
- ## Goal count: 1 ✓
- ## Next Steps count: 1 ✓
- Gate: F\d+ R\d+ count: 31 (expected 31) ✓
- Gate: F280 R3 count: 1 (expected 1) ✓
- Distinct R-\d+ ids: 132 (expected 132) ✓
- Distinct Done: R-\d+ ids: 6 (expected 6, new: R-0906, R-0909) ✓
- Open set by distinct id: 126 (expected 126) ✓

### G3 THE TABLE
Exit code: 0
- Changed files match expected set ✓
- Tree object hashes at C2: all match ✓
- Ruff check: All checks passed! ✓
- Pytest (4 test files with 1 deselected): 226 passed, 1 deselected ✓
- Bash syntax: OK ✓
- C2 insertions: 23 (under 500-line cap) ✓

### G4 THE SWEEP
Exit code: 0
- dispatch_job_create pattern search: 0 lines (expected 0) ✓
- smoke_job_create pattern search: 0 lines (expected 0) ✓

### G5 THE SUITE (SPEC S)
Exit code: 1 - FAILED
- Command: python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs
- Result: 2 failed, 17641 passed, 23 skipped, 1 warning in 1304.61s
- Failed tests:
  - tests/test_remedy_smoke_script.py::TestSmokeScriptText::test_create_job_uses_write_readme_task_type
  - tests/test_remedy_smoke_script.py::TestSmokeScriptText::test_create_job_uses_task_description_flag

## AUTHORED-TEXT PROOFS
None applied

## DEVIATIONS & ASSUMPTIONS

### STOP: Gate G5 (SPEC S) failed - Red gate is a STOP condition (constraint 3)

The full suite test fails on two tests in `tests/test_remedy_smoke_script.py` that check for the presence of `--task-type write_readme` and `--task-description` flags in the smoke script text. 

The carrier's fifth edit changes `scripts/remedy_smoke.sh` from calling `remedy job create` with CLI flags (`--task-type write_readme --task-description "..."`) to calling `_cmd_create_job()` directly with Python keyword arguments (`task_type='write_readme', task_description='Write/update README.md for smoke target.'`).

The failing tests look for these flag strings in the script text itself and are now failing because the flags are no longer in the script - they're Python keyword arguments instead. The tests are:
- `test_create_job_uses_write_readme_task_type`: Looks for `"--task-type write_readme"` in script text
- `test_create_job_uses_task_description_flag`: Looks for `"--task-description"` in script text

Per the block's constraint 3: "A red gate is a STOP: commit nothing of the table, and hand back with the row and the reading." However, since C2 was already committed and we're past that point, C2 remains as the last committed state before the gate failure.

## NEXT

Phase 1 rule 1; STOP due to red gate G5 (SPEC S exit 1); the smoke-script tests expect CLI flag text that the carrier's edit removed, requiring either: (1) the tests in test_remedy_smoke_script.py need to be updated to check for the new calling convention, or (2) the carrier's smoke script edit needs revision. This is a production-test mismatch that needs reviewer decision before proceeding.

