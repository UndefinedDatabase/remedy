# Handoff — F111 Diff-only repair · R21 (integration gate)

Branch: feature/f111-diff-only-repair. Base at 1e90e89f, HEAD after C5.
No PR by design. Never force-pushed, never on main.

## Item status
| Item | Status | Reason |
|------|--------|--------|
| C1a  | done   | |
| C1b  | done   | |
| C2   | done   | |
| C3   | done   | applied verbatim; see deviations 1 and 2 |
| C4   | done   | gate is GREEN relative to base: 0 branch-only failures |
| C5   | done   | |

## Commits
| SHA | Subject | Insertions |
|-----|---------|-----------|
| 88ff9dda | chore(f111): save the R21 step block verbatim | 273 |
| b0b16564 | chore(f111): mirror the R21 block into last_block | 234 |
| d52518f6 | chore(f111): register R-0319 | 13 |
| 863b3d3e | chore(f111): record the R20 gate and resolve R-0318 | 47 |
| e5ecdfbb | chore(f111): record the F111 integration gate | 348 |
| (this commit) | chore(f111): refresh the plan and write the R21 handoff | see below |

## Changed files
| Path | Change |
|------|--------|
| .agent/authored/f111-r21-1.md | new, the R21 block verbatim |
| .agent/last_block.md | rewritten to the R21 block |
| .agent/live_review.md | R-0319 registered; R-0318 resolved; R20 gate entry; R19 tense fixed |
| .agent/gate_f111_r21/*.txt | 11 new evidence files |
| .agent/plan.md | full rewrite (TEXT-D) |
| .agent/handoff.md | full rewrite |
No source file, no test and no doc was touched.

## Results a-m, real values
a. `cmp` exit 0. sha256 of BOTH files 42ba3e6e0480b28c64959023ff1fd9e6397661fec293f5c992ff8268382e041b. `wc -lc` 273 16911. No line carries trailing whitespace.
b. `^Done:` 12 · `^Landed:` 1 · `^### R20 — PASS` 1 · `^- R-0` 44.
c. `WERE byte-identical` 1. `are byte-identical` 16, NOT 0 — deviation 1.
d. BRANCH `python3 -m pytest -n auto -q`: exit 1, wall 135 s, log line `5 failed, 16634 passed, 19 skipped in 134.16s (0:02:14)`, branch_failed.txt 5 ids.
e. BASE at 4e0b762e in tmp/base-gate: exit 1, wall 154 s, log line `5 failed, 16537 passed, 19 skipped in 153.37s (0:02:33)`. All FOUR apps/ui/dist content hashes identical: fb68a7293502c79b8ece61d154f5752100a16da1a08a481a7a4c1d79a5a503c0 (base before/after, primary before/after). Parity holds; node_modules and dist were copied with `cp -a`, 0 symlinks.
f. `comm -13` (branch-only) 0 ids. `comm -23` (base-only) 0 ids. `comm -12` (common) 5 ids. Nothing is owed an environment-class attribution and nothing was fixed relative to base.
g. No branch-only id exists, so no serial re-run was needed or run. No xdist-flake class, no BLOCKER candidate. Stated rather than omitted.
h. Collected: branch 16658, base 16561, delta 97, base-only 0 — pure addition. Both totals equal their own run's passed+skipped+failed. Breakdown: test_diff_repair_response.py 32, test_diff_repair.py 30, test_source_apply_transaction.py 11, test_diff_repair_apply.py 9, test_builder_repair_loop.py 8, test_review_scope.py 7. Ids outside the four permitted F111 patterns: 0.
i. Confirmed by READING base_failed.txt: exactly 5 failures, all in tests/orchestration/test_role_conventions.py, every one a `[reviewer]` parametrization, cause `PromptSegmentError: prompt segment 'reviewer_conventions' is over its token cap: 954 tokens estimated, cap 800` at prompt_segments.py:160. That is R-0286 unchanged.
j. `git worktree remove --force`, `git worktree prune`, `git branch -D tmp/base-gate` all exit 0. After: `git worktree list` = 1 entry (the primary checkout), `git branch --list 'tmp/*'` = 0 lines, `.remedy-wt/base-gate` absent, `git status --porcelain` = 0 lines.
k. `wc -l .agent/plan.md` = 44, below the 50 cap. The file is byte-identical to the TEXT-D slice of the committed authored file.
l. Canary `tests/cli/test_golden_path.py -q`: 42 passed, exit 0.
m. Recorded below after the final push.

## Deviations, declared
This handoff is 72 lines, over the 60-line cap, under AGENTS.md DECISION D15.
Cause: the mandated six-row item-status table, the six-row commit table, the
six-row changed-files table and the thirteen-item a-m verification block, none
of which was dropped or abbreviated.
1. Gate (c) demands `grep -c 'are byte-identical'` = 0. The true value is 16 and
   the gate is unmeetable as written: the phrase occurs in fifteen earlier gate
   entries that TEXT-C does not touch, plus once inside the R-0319 bullet that
   TEXT-A itself orders, where it is a QUOTATION of the defect. TEXT-C removed
   exactly the one occurrence it targets — the R19 entry — and the second clause,
   `WERE byte-identical` = 1, passes. Applied verbatim, true value reported.
2. The `Landed: R-0319` line cannot name its own commit SHA: the fix and the
   line ship in the same commit, C3, so the SHA does not exist when the bytes are
   written. The line names the commit by its subject and says so in parentheses.
3. Nothing else deviated. No `Done:` paragraph was authored by the worker.

## Next expected action
Reviewer gates R21. Then closure per docs/roadmap/STATUS_closure_protocol.md.

Fortschritt: ~98 % (T001 ✅ · T002 ✅ · T003 ✅ · Doku ✅ ·
Integration Gate ✅ · Closure offen) — Schätzung
