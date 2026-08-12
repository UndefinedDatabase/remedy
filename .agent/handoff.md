# Handoff — F111 R1 — claim, state reset, carry-forward

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e. No PR, no
merge, main untouched; pushed after every commit (R-0289). Open findings: 22,
next free ID R-0298. No fix landed this round, so neither marker was written.

## Commits (insertions from `git log --numstat`; each < 500)
| Item | SHA | Path | Ins |
|---|---|---|---|
| C1 | d956be2f | .agent/authored/f111-r1-1.md | 319 |
| C2 | b8398d5b | .agent/last_block.md | 293 |
| C3 | b1017248 | docs/roadmap/STATUS.md | 1 |
| C4 | db016f0b | .agent/live_review.md | 96 |
| C5 | 581fb90b | .agent/plan.md | 30 |
| C6 | e3abe7a4 | .agent/context.md | 27 |
| C7 | self-referential (this commit) | .agent/handoff.md | see git show |

## Changed files
| File | Change |
|---|---|
| .agent/authored/f111-r1-1.md | new; the R1 block, byte for byte |
| .agent/last_block.md | rewritten from the authored copy |
| docs/roadmap/STATUS.md | F111 line `[ ]` to `[~]`, one line |
| .agent/live_review.md | reset to F111; 22 findings carried from F107 |
| .agent/plan.md | rewritten for F111 |
| .agent/context.md | rewritten for F111 |
| .agent/handoff.md | this file |

## Gates — command, real exit code, counted value
a. `sha256sum` of SFROM STO LR PLAN CTX -> exit 0; 5 of 5 equal the block table
a. `cmp` BLOCK/authored -> exit 0 silent; `cmp` authored/last_block -> exit 0 silent
b. `grep -c -F -x '- [~] F111 — Diff-only repair' STATUS.md` -> exit 0, value 1
b. `grep -c -F -x '- [ ] F111 — Diff-only repair' STATUS.md` -> exit 1, value 0 (exit 1 is the pass)
b. `git show --numstat b1017248 -- docs/roadmap/STATUS.md` -> exit 0, reads `1 1`
c. `cmp` LR/live_review, PLAN/plan, CTX/context -> exit 0 silent, all three
d. `grep -c '^## Steps' .agent/live_review.md` -> exit 0, value 1
d. `grep -c '^- R-0' .agent/live_review.md` -> exit 0, value 22
d. `grep -c '^<<<'` on live_review, plan, context, handoff, STATUS -> exit 1, value 0 each (exit 1 is the pass)
d. `wc -l < .agent/plan.md` -> exit 0, value 37 (cap 50); `wc -l < .agent/context.md` -> exit 0, value 45
e. `python3 -m pytest tests/docs/ -q` -> exit 0, 294 passed (run at C3, rerun at HEAD)
f. `python3 -m pytest tests/cli/test_golden_path.py -q` -> exit 0, 42 passed
g. `git status --porcelain` -> exit 0, zero lines of output
g. `git rev-list --left-right --count origin/feature/f111-diff-only-repair...HEAD` -> exit 0, reads `0 0`
h. insertions 319, 293, 1, 96, 30, 27 -> each below the 500 cap

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
R2 — the repair-path DECISION plus T001 hunk selection.
