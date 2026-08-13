# Handoff — F111 Diff-only repair, R9 (T002b: the per-path diff split)

Branch: feature/f111-diff-only-repair. Open findings: 28. Next free ID: R-0309.
Fortschritt: ~60 % (T001 ✅ · T002 fast: Record + Split ✅, Apply+Fallback offen · T003 offen) — Schätzung
Deviations, declared (DECISION D15): 80 lines, over the 60 cap. Cause: the mandated
per-commit table (7 rows), changed-files table (8 rows), item-status table (7 rows) and
the nine ordered gate results a-i with their commands and real exit codes. No section
dropped; no prose padding added.

## Commits

| Item | SHA        | Subject                                     | Ins. |
|------|------------|---------------------------------------------|------|
| C1   | 1e08e5b7   | save the R9 step block verbatim             | 330  |
| C2   | a0552b96   | mirror the R9 block into last block         | 262  |
| C3   | 5ecec004   | record the R8 gate and finding R-0308       | 50   |
| C4   | daaa721d   | resolve R-0307 at the R8 gate               | 5    |
| C5   | 650616fc   | split a unified diff into per path sections | 139  |
| C6   | d1dbede4   | convert a diff repair response to a patch   | 110  |
| C7   | this commit| rewrite the plan and handoff for R9         | n/a  |

## Changed files

| Path                                            | Item   |
|-------------------------------------------------|--------|
| .agent/authored/f111-r9-1.md (new)              | C1     |
| .agent/last_block.md                            | C2     |
| .agent/live_review.md                           | C3, C4 |
| packages/orchestration/review_scope.py           | C5     |
| tests/orchestration/test_review_scope.py         | C5     |
| packages/orchestration/diff_repair_response.py   | C6     |
| tests/orchestration/test_diff_repair_response.py | C6     |
| .agent/plan.md, .agent/handoff.md               | C7     |

## Item status

| Item | Status   | Reason                                                       |
|------|----------|--------------------------------------------------------------|
| C1   | done     |                                                              |
| C2   | done     |                                                              |
| C3   | done     |                                                              |
| C4   | done     |                                                              |
| C5   | done     |                                                              |
| C6   | done     |                                                              |
| C7   | deviated | plan slice is 47 authored lines, not the 46 the block states; applied verbatim, never reflowed. C7's own SHA/insertions cannot be self-referenced. |

## Gates — command -> real exit code, counted value

- `cmp` BLOCK/authored, authored/last_block, PLAN/plan.md -> 0, all silent.
- `git show --numstat 5ecec004 -- .agent/live_review.md` -> `50 0` (pure append).
- `git show --numstat daaa721d -- .agent/live_review.md` -> `5 1` (the one rewrite).
- live_review.md: `^- R-0` 33, `^Done:` 5, `^Landed:` 0 (grep exit 1), `^### R8 — PASS` 1;
  `str.count` of the LRG slice 1, of the DONE slice 1.
- plan.md: `wc -l` 47 (see deviation), `^## Goal` 1, `^## Next Steps` 1, `R-0309` 1.
- `pytest test_final_verifier test_reviewer_prompt_scope test_pingpong -q` -> 0, 146 passed
  (behaviour pin: same 146 measured before the round).
- `pytest test_review_scope.py -q` -> 0, 39 passed (32 pre-round + 7 new).
- `pytest test_diff_repair_response.py -q` -> 0, 27 passed (23 pre-round + 4 new).
- `pytest test_diff_repair.py -q` -> 0, 30 passed, unchanged.
- `pytest tests/cli/test_golden_path.py -q` -> 0, 42 passed (canary).
- `pytest tests/test_path_utils.py tests/test_data_paths.py -q` -> 0, 51 passed.
- Red-proof in a disposable worktree at d1dbede4 (`split_diff_by_path` returning the
  WHOLE diff per path) -> exit 1, 6 failed / 60 passed: the four
  `test_split_diff_by_path_*` (round_trip, two_files_are_disjoint,
  drops_preamble_before_first_header, keeps_no_newline_marker) and two
  `TestDiffRepairResponseToPatch` (single_file, two_file). Worktree removed and pruned.
- `git status --porcelain` empty; `git worktree list` one entry; every per-commit
  insertion count < 500; remote comparison `0 0` after the final push.

Disclosed, not a gate failure: `split_diff_by_path` drops only the preamble BEFORE the
first `---`, exactly as its docstring states. In a real `git diff` with per-file
`diff --git`/`index` lines, file N+1's preamble therefore lands at the tail of file N's
section. R10 must decide whether the applicator tolerates it or the walk must cut there.

## NEXT SESSION

1. The branch is UNMERGED and has NO PR, by design.
2. Next action is R10: the apply and fallback half of T002.
3. NOTHING imports `diff_repair.py` or `diff_repair_response.py` yet — both are seams,
   and T003 is the round that wires them.
