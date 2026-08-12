# Handoff — F111 R3 — R2 gate persisted, R-0299 fixed

Branch feature/f111-diff-only-repair, round base 5d8d8c56, from main 4e0b762e.
No PR, no merge, main untouched, pushed after every commit (R-0289). Findings
24 open, next free ID R-0300 — none registered this round, one landed.

## Commits (insertions from `git log --shortstat`; each < 500)
| Item | SHA | Path | Ins |
|---|---|---|---|
| C1 | 1bf62e2f | .agent/authored/f111-r3-1.md | 225 |
| C2 | 6eec3395 | .agent/last_block.md | 182 |
| C3 | 2fd0d777 | .agent/live_review.md | 51 |
| C4 | c473d1a0 | diff_repair.py + test_diff_repair.py | 47 |
| C5 | 2d8cb1db | .agent/live_review.md | 2 |
| C6 | b5093741 | .agent/plan.md | 20 |
| C7 | self-referential (this commit) | .agent/handoff.md | see git show |

## Changed files
| File | Change |
|---|---|
| .agent/authored/f111-r3-1.md | new; the R3 block, byte for byte |
| .agent/last_block.md | rewritten from the authored copy |
| .agent/live_review.md | pure append x2: R2 PASS + R-0298/R-0299, then Landed |
| packages/orchestration/diff_repair.py | new `out_of_bounds` reason; docstring lists 5 |
| tests/orchestration/test_diff_repair.py | +3 tests; 18 -> 21, none weakened |
| .agent/plan.md | rewritten for R3 |
| .agent/handoff.md | this file |

## Gates — command, real exit code, counted value
a. `sha256sum` LRG/PLAN -> exit 0, 2 of 2 match the block's stated digests (BLOCK
   states none by construction, R-0298; pinned by cmp, sha a5088325).
   `cmp` BLOCK/authored, authored/last_block, PLAN/plan.md -> exit 0 silent, 3 of 3
b. `git show --numstat` C3 live_review.md -> exit 0 `51 0`; C5 -> exit 0 `2 0` —
   delete column 0 in both, so both were pure appends
c. `grep -c` live_review.md: `^- R-0` exit 0 = 24; `^Landed:` exit 0 = 1; `^Done:`
   exit 1 = 0 (exit 1 is the pass). `grep -c out_of_bounds diff_repair.py` exit 0 = 3
d. `python3 -m pytest tests/orchestration/test_diff_repair.py -q` -> exit 0,
   21 collected / 21 passed (18 before this round)
e. `python3 -m pytest tests/cli/test_golden_path.py -q` -> exit 0, 42 passed (canary)
f. `python3 -m pytest tests/orchestration/test_test_runner.py -q -k 'plan_md or
   context_md'` -> exit 0, 3 passed, 48 deselected
g. mutation red-proof runs AFTER this commit in disposable worktree .remedy-wt/r3mut
   only; exit code, failing test id, worktree list, clean-tree recheck: in handback
h. `git rev-list --left-right --count origin/<branch>...HEAD` -> in handback, after
   this commit is pushed; insertions 225/182/51/47/2/20, each below the 500 cap

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
Deviations, declared: C4 adds one test beyond the three ordered, none weakened;
this file needed a second commit to come back under its own 60-line cap.

## Next expected action
R4 — settle where the hunk line ranges come from, then wire them in.
