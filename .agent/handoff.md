# Handoff — F107 R5 (T003 tiered selector) — COMPLETE

Branch: feature/f107-context-compiler-v2. R4 reviewed PASS at 2c75bddf.
C1–C6 landed in a PRIOR worker session that ended before PROCEDURE step 7.
This session added nothing to them: it ran the mutation probe, re-ran every
gate against the disk state, and closes the round with C7 alone.
Open findings: 8 (R-0221/0239/0247/0262/0265/0266/0268/0270). Next free: R-0272.
R-0271 is RESOLVED by C3 (reviewer-authored text). No STOP file appeared.
T001+T002 frozen: their 29 tests still pass unchanged inside the 42.

## Commits

| Item | SHA      | Subject                                                   | +/-     |
|------|----------|-----------------------------------------------------------|---------|
| C1   | 1e759980 | chore(f107): save the R5 step block verbatim              | 393/0   |
| C2   | 2e77d48e | chore(f107): mirror the R5 block into last_block          | 322/255 |
| C3   | 4860115e | chore(f107): record the R4 gate and resolve R-0271        | 55/2    |
| C4   | 026f463c | chore(f107): advance plan to R5 T003                      | 11/12   |
| C5   | 51ed7886 | feat(f107): tiered context selector with budget demotion  | 351/8   |
| C6   | 3df24506 | test(f107): tier assignment budget demotion and omissions | 284/2   |
| C7   | self-ref | chore(f107): rewrite handoff for R5                       | 76/77   |

## Changed files

| File                                         | Change                           |
|----------------------------------------------|----------------------------------|
| .agent/authored/f107-r5-1.md                 | new; byte-copy of the R5 block   |
| .agent/last_block.md                         | byte-copy of the R5 block        |
| .agent/live_review.md                        | slices FIX1 + LR4 (C3)           |
| .agent/plan.md                               | slice PLAN4 (full replacement)   |
| packages/orchestration/context_compiler.py   | T003 selector layer (C5)         |
| tests/orchestration/test_context_compiler.py | 13 T003 tests appended (C6)      |
| .agent/handoff.md                            | this rewrite (C7)                |

## Gate results (command → real exit → counted value)

a. `sha256sum` .remedy-wt/f107-r5-1.block.md, .agent/authored/f107-r5-1.md,
   .agent/last_block.md → exit 0 → all three
   220d64ec8aa49a38761e011a9c4159cef350fc1dfcaf05fcff14dd8a546e8b5b, 393 lines
   each. `cmp` IS available this session and was also run over both pairs →
   exit 0 both. Slice re-extraction from .agent/last_block.md → exit 0 → all
   five markers MATCH: FIX1FROM 06f8ce67… 1L, FIX1TO 547f5a52… 2L, LR4FROM
   3541d8ff… 1L, LR4TO b07a255e… 53L, PLAN4 320c4890… 28L. 0 MISMATCH.
b. `git show --numstat 4860115e -- .agent/live_review.md` → exit 0 → `55  2`.
   FIX1FROM "  carry. OPEN." occurs 0x; the LR4FROM Landed line occurs 0x.
   All 2 FIX1TO lines and all 53 LR4TO lines occur exactly 1x among the 55
   lines C3 adds — 0 strays. `grep -c '^## Steps'` → exit 0 → 1;
   `grep -c '^Done: R-0271'` → exit 0 → 1.
c. `sha256sum .agent/plan.md` → exit 0 → 320c489005c5aafc…, equal to the
   verified PLAN4 body and its marker digest (`cmp` exit 0);
   `wc -l < .agent/plan.md` → exit 0 → 28.
d. `python3 -m pytest tests/orchestration/test_context_compiler.py -q` →
   exit 0 → 42 passed (29 frozen T001+T002 + 13 new T003).
e. `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0 → 42 passed.
f. `grep -c '^<<<'` → live_review.md 0, plan.md 0, handoff.md 0 (grep exit 1).
g. `git status --porcelain` → empty; `git worktree list` → primary alone;
   HEAD == origin/feature/f107-context-compiler-v2 after push; insertions per
   commit 393, 322, 55, 11, 351, 284, C7 76 — each < 500.
h. `git diff --name-only 2c75bddf..HEAD` → exit 0 → exactly the seven paths of
   the Changed files table, nothing else.
i. `python3 -m ruff check packages/orchestration/context_compiler.py
   tests/orchestration/test_context_compiler.py` → exit 0 → "All checks
   passed!", 0 errors.
j. MUTATION PROBE, disposable worktree .remedy-wt/f107_r5_mut at 3df24506
   only: in `_largest_tokens_first` the sort key `(-s.estimated_tokens,
   s.rel_path)` became `(s.estimated_tokens, s.rel_path)`, so budget phase A
   picks the SMALLEST tier-2 file. `python3 -m pytest
   tests/orchestration/test_context_compiler.py -q` → exit 1 → 1 failed,
   41 passed. The one failure is
   `test_budget_demotes_the_largest_tier_two_file_first`:
   `At index 1 diff: ('lib_big.py', 2, 'full') != ('lib_big.py', 2,
   'signatures')`. The ordering rule bites. Worktree removed and pruned;
   `git worktree list` shows the primary alone.

## Item status

| Item | Status | Reason                                                       |
|------|--------|--------------------------------------------------------------|
| C1   | done   | prior session; re-verified here by digest and by cmp          |
| C2   | done   | prior session; sha256 identical to block and authored copy    |
| C3   | done   | prior session; rewrite pair, numstat `55 2`, both FROM 0x     |
| C4   | done   | prior session; plan.md sha256 == PLAN4 marker digest, 28L     |
| C5   | done   | prior session; not re-opened this round, gates d/i green      |
| C6   | done   | prior session; not re-opened this round, 42 passed            |
| C7   | done   | this session's only commit; self-ref: own SHA not writable    |

Deviations, declared (1). This file is 95 lines, over the block's 60. Cause is
mandated content: the seven-row per-commit table, the seven-row changed-files
table, the ten-gate result block with the mutation-probe transcript detail, and
the seven-row item-status table (AGENTS.md DECISION D15 permits up to 100 when
a per-commit table of more than five commits requires it). No section dropped.
No fix was needed this round, so no `Landed:` line appears.

Next expected action: R6 = T004 segment integration and the `remedy job
context` CLI view.
