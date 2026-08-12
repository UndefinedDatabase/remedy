# Handoff — F111 R5 — the range source lands, R-0300/0301/0302 closed

Branch feature/f111-diff-only-repair, round base c9064b17, from main 4e0b762e.
Findings 26 open, next free ID R-0303. R-0299 is now RESOLVED (reviewer text).
No PR, no merge, main untouched, never force-pushed; pushed after every commit.

## Commits (insertions per `git log --numstat`; each < 500)
| Item | SHA | Path | Ins |
|---|---|---|---|
| C1 | b1135684 | .agent/authored/f111-r5-1.md | 200 |
| C2 | 09926e75 | .agent/last_block.md | 185 |
| C3 | 7517f370 | .agent/live_review.md | 59 |
| C4 | b0fe0e59 | .agent/live_review.md | 1 |
| C5 | 83aec443 | diff_repair.py 31, review_scope.py 11, test_diff_repair.py 122 | 164 |
| C6 | 87df3a40 | docs/roadmap/features/T2_F111.md | 20 |
| C7 | 01d39dd1 | .agent/live_review.md | 3 |
| C8 | 296ffd03 | .agent/plan.md | 26 |
| C9 | self-referential (this commit) | .agent/handoff.md | see git show |

## Changed files
| File | Change |
|---|---|
| .agent/authored/f111-r5-1.md | new; the R5 block, byte for byte |
| .agent/last_block.md | rewritten from the authored copy |
| .agent/live_review.md | R4 PASS + R-0301/0302 appended; R-0299 Landed->Done; 3 Landed |
| packages/orchestration/review_scope.py | new public seam `parse_diff_line_ranges` |
| packages/orchestration/diff_repair.py | new `changed_line_ranges_from_patch` + imports |
| tests/orchestration/test_diff_repair.py | +9 tests: empty-file range, patch->ranges |
| docs/roadmap/features/T2_F111.md | D1 loop name fixed (D2); D3 range source added |
| .agent/plan.md | rewritten; falsified `source_patch_applied` hypothesis deleted |
| .agent/handoff.md | this file |

## Gates — command, real exit code, counted value
a. `sha256sum` LRG/RS/DR/TESTS/FEATD3 -> exit 0, 5 of 5 match the stated digests;
   `cmp` BLOCK/authored and authored/last_block -> exit 0, silent, 2 of 2
b. `git show --numstat` live_review.md: C3 `59 0`, C4 `1 1`, C7 `3 0` (exit 0 each)
c. live_review.md `grep -c`: `^- R-0` = 27 (exit 0); `^Landed:` = 3 (exit 0);
   `^Landed: R-0299` = 0 (exit 1, the pass); `^Done:` = 1; `^### R4 — PASS` = 1
d. slice-count python3 -c -> exit 0, all four counts 1 (review_scope, diff_repair,
   test_diff_repair, T2_F111). `grep -c`: `^def parse_diff_line_ranges` 1,
   `^def changed_line_ranges_from_patch` 1, `^from packages.orchestration.
   review_scope import` 1, `^    changed_line_ranges_from_patch,` 1
e. T2_F111.md: `run_bounded_repair_loop` = 0 (exit 1, the pass);
   `run_builder_bridge_loop` = 2 (exit 0)
f. pytest exit 0 each: test_diff_repair.py 30 passed (21 before);
   test_review_scope.py 32 passed; tests/docs/ 294 passed;
   tests/cli/test_golden_path.py 42 passed. `ruff check` 3 files -> exit 0
g. MUTATION RED-PROOF in disposable worktree .remedy-wt/f111r5wt (never the primary
   checkout): the two `for file_op in patch.file_ops:` lines deleted ->
   `2 failed, 28 passed`, exactly `test_file_ops_paths_carry_no_lines` and
   `test_a_file_ops_path_is_reported_as_no_ranges_by_selection`, as expected.
   Worktree removed and pruned; `git worktree list` = 1 entry
h. `git status --porcelain` exit 0, empty; per-commit insertions 200/185/59/1/164/
   20/3/26, each < 500; `git rev-list --left-right --count origin/<branch>...HEAD`
   -> `0 0` through C8, rechecked after C9 is pushed

## Item status
| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | |
| C7 | done | |
| C8 | done | |
| C9 | done | |
Deviations, declared: this file is 78 lines, over the 60-line cap. Cause is
mandated content only: a 9-row per-commit table, a 9-row changed-files table, an
8-gate verification table with commands and real values, and a 9-row item-status
table (DECISION D15). No section dropped, no prose padding.

## NEXT EXPECTED ACTION
T002 — versioned unified-diff response schema, fence pre-check before any apply,
strict apply with an all-or-nothing conflict fallback, on the `builder_bridge`
seam (`run_builder_bridge_loop`). T001 now has BOTH its selector and its range
source but STILL NO CALL SITE: T003 wires `changed_line_ranges_from_patch` in.
