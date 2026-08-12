# Handoff — F111 R2 — R1 gate, DECISION D1, T001 hunk selection

Branch feature/f111-diff-only-repair, cut from main at 4e0b762e, round base
b0ab8e09. No PR, no merge, main untouched; pushed after every commit (R-0289).
Findings 22 open, next free ID R-0298 — this round registers none.

## Commits (insertions from `git log --shortstat`; each < 500)
| Item | SHA | Path | Ins |
|---|---|---|---|
| C1 | f71ebc06 | .agent/authored/f111-r2-1.md | 275 |
| C2 | 80aa231b | .agent/last_block.md | 231 |
| C3 | 6683dad8 | .agent/live_review.md | 51 |
| C4 | a8c211b0 | docs/roadmap/features/T2_F111.md | 17 |
| C5 | b8a1846e | diff_repair.py + test_diff_repair.py | 409 |
| C6 | c817a094 | .agent/plan.md | 18 |
| C7 | self-referential (this commit) | .agent/handoff.md | see git show |

## Changed files
| File | Change |
|---|---|
| .agent/authored/f111-r2-1.md | new; the R2 block, byte for byte |
| .agent/last_block.md | rewritten from the authored copy |
| .agent/live_review.md | pure append: R1 PASS gate + DECISION F111 D1 |
| docs/roadmap/features/T2_F111.md | pure append: the D1 scope amendment |
| packages/orchestration/diff_repair.py | new; pure selection helper, no call sites |
| tests/orchestration/test_diff_repair.py | new; 18 tests over clauses 1-8 |
| .agent/plan.md | rewritten for R2 |
| .agent/handoff.md | this file |

## Gates — command, real exit code, counted value
a. `sha256sum` LRG/FF/PLAN -> exit 0, 3 of 3 match the block (BLOCK carries no
   stated digest there, being self-referential; it is pinned by cmp, sha 85e49d42).
   `cmp` BLOCK/authored, authored/last_block, PLAN/plan.md -> exit 0 silent, 3 of 3
b. `git show --numstat` C3 live_review.md -> exit 0 `51 0`; C4 T2_F111.md -> exit 0
   `17 0` — delete column 0 in both, so both were pure appends
c. `grep -c` live_review.md: `^### DECISION F111 D1` exit 0 = 1; `^### R1 — PASS`
   exit 0 = 1; `^- R-0` exit 0 = 22 (unchanged); `^Done:` exit 1 = 0 (exit 1 passes)
d/e/f. `python3 -m pytest -q`: test_diff_repair.py exit 0, 18 collected/18 passed;
   tests/docs/ exit 0, 294 passed (at C4 and at HEAD); test_golden_path.py exit 0, 42
g. `grep -c '@@' diff_repair.py` -> exit 1, value 0 (exit 1 is the pass; no diff
   parser added); its 4 imports are __future__, collections.abc, dataclasses and
   pathlib — not pingpong_loop/builder_bridge/source_apply/review_scope
h. mutation red-proof runs AFTER this commit in disposable worktree .remedy-wt/r2mut
   only; exit code, failing test id, worktree list, clean-tree recheck: in handback
i. `git rev-list --left-right --count origin/<branch>...HEAD` -> exit 0 `0 0`; insertions 275/231/51/17/409/18, each below the 500 cap

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
Deviations, declared: none.

## Next expected action
R3 — wire the selected hunks into the repair context.
