# F308 round 2 — amendment 1: the closed status matrix names `split`

Applies to round 2 (`.agent/authored/f308-r2.md`) after its C3 at `dc08a2ab2`, which stopped at
gate 3 with two red nodes in `tests/orchestration/test_task_expectation_status_truth.py`. The
round's block did not name that file, which mirrors the closed set DECISION F308 D2 (5) widens.
That test's own rule is that the manifest's status vocabulary equals the job record's `TASK_*`
constants, and `TASK_SPLIT` is one of them, so naming `split` there carries out D2 rather than
weakening an assertion. This amendment replaces the block's "no existing test is edited" for that
file alone, and for exactly the two edits below.

### C3b — `F308 R2 C3b: the closed status matrix and the job record's vocabulary name split (amendment 1)`
Paths: `tests/orchestration/test_task_expectation_status_truth.py`, `.agent/prose_slips.md`,
`.agent/authored/f308-r2-amend1.md` (NEW FILE).
1. Copy this amendment (`block-amend1.md` in the round's prep folder) to
   `.agent/authored/f308-r2-amend1.md`; `cmp` prints nothing. Copy `dry-prose_slips.md` over
   `.agent/prose_slips.md`; `cmp` prints nothing.
2. In the test file: the `_ALLOWED` entry for `EXPECT_SKIPPED` reads `{"skipped", "vetoed", "split"}`,
   and the set in `test_the_status_vocabulary_matches_the_jobplan` gains `PJ.TASK_SPLIT` after
   `PJ.TASK_VETOED`. The docstring of `test_the_exhaustive_matrix` says "All 42 pairs"; with eight
   statuses it now enumerates 48, so it reads "Every pair." Nothing else in the file changes.
3. Then run gate 3 again, once, and gates 4 to 6, and continue with C4 exactly as the block orders,
   naming C3b in the changed-files table and in the item-status table, and this amendment in the
   handback's deviations.
