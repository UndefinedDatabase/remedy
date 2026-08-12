# Handoff — F107 R7 (repair round for R-0273) — COMPLETE

Branch: feature/f107-context-compiler-v2. R6 reviewed PASS at 861eb371. One
worker session, C1–C7. No commit amended/rebased/reverted/reordered, no PR
created, main never touched, no existing test edited. Open findings: 10
(R-0221/0239/0247/0262/0265/0266/0268/0270/0272 + R-0273, which C3 REGISTERS
and C5 LANDS — only reviewer text resolves it, so it stays OPEN). Next free:
R-0274. No `Done:` line was written; the fix carries a single `Landed: R-0273`
line in .agent/live_review.md, committed with C5.

## Commits

| Item | SHA      | Subject                                                  | +/-     |
|------|----------|----------------------------------------------------------|---------|
| C1   | db8bcbd5 | chore(f107): save the R7 step block verbatim             | 328/0   |
| C2   | b92e8182 | chore(f107): mirror the R7 block into last_block         | 255/291 |
| C3   | 4909b1b1 | chore(f107): record the R6 gate and register R-0273      | 68/0    |
| C4   | 3af97f23 | chore(f107): advance plan to R7 repair                   | 9/9     |
| C5   | 027f13fd | fix(f107): render signatures at the compiled line cap    | 16/5    |
| C6   | d8beb79f | test(f107): the rendering matches the cap it was compiled at | 113/0 |
| C7   | ec2da616 | chore(f107): rewrite handoff for R7                      | 75/70   |
| C8   | self-ref | chore(f107): correct the grep line number in the handoff | see log |

## Changed files

| File                                         | Change                           |
|----------------------------------------------|----------------------------------|
| .agent/authored/f107-r7-1.md                 | new; byte-copy of the R7 block   |
| .agent/last_block.md                         | byte-copy of the R7 block        |
| .agent/live_review.md                        | slices LRF3 + LR6 (C3); Landed (C5) |
| .agent/plan.md                               | slice PLAN6 (full replacement)   |
| packages/orchestration/context_compiler.py   | the three FIX CONTRACT edits (C5)|
| tests/orchestration/test_context_compiler.py | 3 tests appended (C6)            |
| .agent/handoff.md                            | this rewrite (C7)                |

## Gate results (command → real exit → counted value)

a. All five slice bodies recompute to their BEGIN-marker digests at their
   declared lengths → 0 MISMATCH: LRF3FROM 4ad9497d… 1L, LRF3TO e3fdd106… 20L,
   LR6FROM d85c84ac… 1L, LR6TO dac43442… 50L, PLAN6 047fcc7a… 28L. TOOL: `cmp`
   (available) plus `sha256sum`. `cmp` of .remedy-wt/f107-r7-1.block.md against
   .agent/authored/f107-r7-1.md and against .agent/last_block.md → exit 0 both,
   silent; all three sha256 to ce03b5df0205be2a…, 328 lines.
b. C3 append proof → `git show --numstat 4909b1b1 -- .agent/live_review.md` →
   exit 0 → `68  0`: 0 DELETIONS, so neither anchor line was edited. Each FROM
   still occurs exactly 1x in the file. TO-only lines 19 (LRF3TO) + 49 (LR6TO)
   = 68, each exactly 1x among the 68 added lines; 0 added lines belong to
   neither body. `grep -c '^## Steps'` → 1; `grep -c '^- R-0273'` → 1.
c. `cmp` extracted PLAN6 body against .agent/plan.md → exit 0, silent;
   `sha256sum .agent/plan.md` → 047fcc7a691f9589… == the marker digest;
   `wc -l < .agent/plan.md` → exit 0 → 28.
d. `python3 -m pytest tests/orchestration/test_context_compiler.py -q` →
   exit 0 → 55 passed (the 52 frozen tests unchanged + 3 new).
e. `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0 → 42 passed.
f. `grep -c '^<<<'` → live_review.md 0, plan.md 0, handoff.md 0 (grep exit 1).
g. `git status --porcelain` → empty; `git worktree list` → primary alone;
   HEAD == origin/feature/f107-context-compiler-v2 after the push; insertions
   per commit 328, 255, 68, 9, 16, 113, C7 — each < 500.
h. `git diff --name-only 861eb371..HEAD` → exit 0 → exactly the seven paths of
   the Changed files table, nothing else. `grep -rn "CompiledContext("
   packages/ tests/ apps/` → exit 0 → ONE line,
   packages/orchestration/context_compiler.py:878, the single construction
   site (:875 before C5 added the field; C8 corrects that stale number).
   `python3 -m ruff check packages/orchestration/context_compiler.py
   tests/orchestration/test_context_compiler.py` → exit 0 → "All checks
   passed!", 0 errors.
i. Step 7, disposable worktree .remedy-wt/f107_r7_mut at d8beb79f only, both
   checks run there and never in the checkout:
   (i) RED-PROOF — edit 3 alone reverted to `DEFAULT_SIGNATURE_LINE_CAP` in
   `render_compiled_context_text`, field and constructor left in place.
   `python3 -m pytest tests/orchestration/test_context_compiler.py -q` →
   exit 1 → 1 failed, 54 passed:
   `test_signature_blocks_render_at_the_cap_the_context_was_compiled_at` on
   `assert bodies[selected.rel_path] == expected_body` →
   `assert 'def deep_0()..."""Deep 5."""' == 'def deep_0()..."""Deep 0."""'`.
   The regression test BITES.
   (ii) file restored with `git checkout --`, then a DIFFERENT mutation:
   `compile_task_context` stores `line_cap=DEFAULT_SIGNATURE_LINE_CAP` instead
   of the caller's value. Same command → exit 1 → 3 failed, 52 passed:
   `test_the_compiled_context_carries_the_line_cap_it_was_compiled_at` on
   `AssertionError: assert 200 == 2`, the regression test on the same body
   assertion as above, and
   `test_two_contexts_compiled_at_the_same_custom_cap_stay_equal` on
   `AssertionError: assert 200 == 2`. Worktree removed and pruned;
   `git worktree list` → primary alone.

## Item status

| Item | Status | Reason                                                       |
|------|--------|--------------------------------------------------------------|
| C1   | done   | cmp + sha256 identical to the R7 block, 328 lines             |
| C2   | done   | cmp + sha256 identical to block and authored copy             |
| C3   | done   | append pair, numstat `68 0`, both FROM still 1x               |
| C4   | done   | plan.md sha256 == PLAN6 marker digest, 28L, cmp silent        |
| C5   | done   | three FIX CONTRACT edits + the `Landed: R-0273` line          |
| C6   | done   | 3 tests appended, no existing test edited, 55 passed          |
| C7   | done   | handoff rewrite at ec2da616                                   |
| C8   | deviated | eighth commit, same path: gate h's grep line number was stale |

Deviations, declared (2). (1) This file is 114 lines — over the block's 60 and
over the AGENTS.md D15 100-line ceiling. Cause is mandated content: two
eight-row tables, the nine-gate block whose gate i carries BOTH step-7
transcripts with their failing test names and assertion texts, and the
eight-row item-status table. No section was dropped to fit. (2) The block's
bundle is C1–C7; C8 is an eighth commit, touching only .agent/handoff.md, a
path the Change line already names. Cause: gate h recorded the
`grep -rn "CompiledContext("` hit at :875, the line it sat on when the grep was
run BEFORE C5, while after C5 it is :878. Leaving a stale counted value in the
return channel is the worse error, so it was corrected in its own commit rather
than by amending C7.

Next expected action: R8 = T004 part 2 — the `remedy job context` CLI view, an
end-to-end fixture task solved by the fake provider, and the size comparison in
evidence.
