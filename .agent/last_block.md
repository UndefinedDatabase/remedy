── STEP R11/5 — F111 Diff-only repair — applier header off-by-one ────────────
Goal:        Record the R10 PASS gate, resolve R-0311, register R-0312, R-0313
             and R-0314, and fix R-0312: `_apply_hunks` computes every hunk's
             0-based start as `line - 1`, but a hunk whose OLD COUNT is 0 is a
             pure insertion whose content goes AFTER the line its header names,
             so every such hunk lands one line too early and `@@ -0,0 +1 @@`
             splices at index -1, turning a prepend into an append. The
             apply-and-fallback half of T002 is R12 and is NOT in this round.
Bundle:      C1 block save; C2 last_block mirror; C3 gate + Done + findings;
             C4 the header fix + tests; C5 the Landed line; C6 plan and
             handoff. Commit AND push at every item.
Change:      EXACTLY these paths and nothing else:
             .agent/authored/f111-r11-1.md (new), .agent/last_block.md,
             .agent/live_review.md, .agent/plan.md, .agent/handoff.md,
             packages/orchestration/source_apply.py,
             tests/orchestration/test_source_apply_transaction.py.
Constraints: AGENTS.md in full. Apply every authored slice by READING ITS
             SCRATCH FILE (`cat` / `cp`) — never retype, never reflow.
             Do NOT touch `.agent/candidates.md`, `.agent/context.md` or
             `.agent/decisions.md`.
             Do NOT touch `diff_repair.py`, `diff_repair_response.py`,
             `review_scope.py`, `structured_patch.py`, `builder_bridge.py`,
             `repair_context.py` or `pingpong_loop.py`.
             Change NOTHING in `source_apply.py` outside `_apply_hunks`, and
             nothing inside `_apply_hunks` except the start computation and the
             two rejections item 4 names. No docs/ change: this fix restores
             the placement the format already dictates, it does not change a
             documented behaviour, and widening the change set is scope drift.
             Write no `Done:` line of your own: only reviewer-authored text
             sets Resolved (docs/agents/planner_reviewer_prompt.md §4.4). The
             ONE `Landed:` line C5 orders is the worker's correct marker.
             Do not start R12.

PROCEDURE (in order; commit AND push at every numbered item):

0. Preconditions: `git status --porcelain` empty; branch is
   feature/f111-diff-only-repair; `git log -1 --format=%h` is 8644def9.
   Any mismatch => STOP and hand back.  `mkdir -p .remedy-wt/f111r11`.

1. C1 — Save this ENTIRE step block (from the `── STEP R11/5` line through the
   final `Handback:` line, byte for byte) to `.remedy-wt/f111r11/BLOCK`, then
   `cp .remedy-wt/f111r11/BLOCK .agent/authored/f111-r11-1.md`; `cmp` silent.
   Commit: chore(f111): save the R11 step block verbatim   -> push

2. C2 — `cp .agent/authored/f111-r11-1.md .agent/last_block.md`; `cmp` silent.
   Commit: chore(f111): mirror the R11 block into last block   -> push

3. C3 — FINDINGS FIRST, two operations on `.agent/live_review.md`:
   (a) DELETE its LAST line — the R-0311 `Landed:` line, which the reviewer now
       replaces with authored `Done:` text (§4.4). It is the final line of the
       file; remove that one line and nothing else.
   (b) Write the slice delimited by `<<<LRG_BEGIN` and `<<<LRG_END` (marker
       lines excluded) to `.remedy-wt/f111r11/LRG`, then
       `cat .remedy-wt/f111r11/LRG >> .agent/live_review.md`.
   In `git show --numstat <C3> -- .agent/live_review.md` the DELETE column must
   be exactly `1`; report the real insertion count.
   Commit: chore(f111): record the R10 gate and findings R-0312 to R-0314 -> push

<<<LRG_BEGIN
### R10 — PASS (2026-08-13)
Reviewed by the main session over 33f408b2..8644def9. Every ordered gate was
re-run by the reviewer on this machine; nothing was read off the handback.
Transport: PRIMARY cmp proof — `.agent/authored/f111-r10-1.md` and
`.agent/last_block.md` are byte-identical. Numstat purity: `80 0` for the gate
append and `2 0` for the `Landed:` line, both pure appends as ordered. Markers
on the final file: 36 registered ids, 5 resolutions, 1 landed marker, 1 R9 pass
heading, 1 D4 heading. The fix proved BY VALUE, not by colour:
`_apply_hunks('alpha\nbeta\ngamma\n', '@@ -1,3 +1,3 @@\n alpha\n-beta\n+BETA\n gamma\n')`
printed `'alpha\nBETA\ngamma\n'` at exit 0. Tests, each re-run by the reviewer:
179 passed for the source-apply tier, 138 for the untouched modules plus the
golden-path canary, 225 for the applier's other consumers. Red-proof: in a
disposable worktree at HEAD with `source_apply.py` checked out from 33f408b2,
`pytest tests/orchestration/test_source_apply_transaction.py -q` exited 1 with
5 failed / 10 passed — exactly the five ids the handback named, and
`test_pure_deletion_hunk_removes_only_its_line` passes on the old code, as the
handback declared. Worktree removed and pruned; `git status --porcelain` empty,
`git worktree list` one entry. Scope: exactly the seven ordered paths.

Deviation ACCEPTED: C5's authored `Landed:` line says "six order tests added";
C4 adds five new tests and strengthens one existing assertion. The worker
applied the authored bytes verbatim and declared the mismatch instead of
reflowing text to match a number, which is the correct call — the error is the
reviewer's and is registered as R-0314 below.

Done: R-0311 — `_apply_hunks` no longer collects a hunk's additions and dumps
them at the hunk's start; it splices the hunk's new block over the exact
original range the hunk consumed, so an added line lands at its own position.
Proved by value at the R10 gate and pinned by five new order tests plus the
strengthened `test_correct_context_applies`, which now asserts the full result
string instead of a substring. Resolved. The header-side placement defect found
while gating this fix is a SEPARATE finding, R-0312 below, not a reopening.

- R-0312 (High, F111 R10, hunk-header off-by-one in the applicator, the same
  Done-criterion class as R-0311): `_apply_hunks` computes every hunk's 0-based
  start as `int(m.group(1)) - 1`. That is correct only for a hunk that consumes
  at least one original line. A unified-diff hunk whose OLD COUNT is 0 is a pure
  insertion, and its header names the line AFTER which the content goes, so its
  0-based index is the line number ITSELF. Confirmed against real `git diff
  -U0`, not from memory: inserting `X` between `a` and `b` in `a\nb\nc\n` emits
  `@@ -1,0 +2 @@`, prepending emits `@@ -0,0 +1 @@`, appending emits
  `@@ -3,0 +4 @@`. Measured on the R10 applier against `'a\nb\nc\n'`:
  `@@ -1,0 +2 @@\n+X\n` returned `'X\na\nb\nc\n'` where the diff says
  `'a\nX\nb\nc\n'`; `@@ -3,0 +4 @@\n+X\n` returned `'a\nb\nX\nc\n'` where the
  diff says `'a\nb\nc\nX\n'`; and `@@ -0,0 +1 @@\n+X\n` returned
  `'a\nb\nc\nX\n'` — `orig_start` is -1 there, so `result_lines[-1:-1]` inserts
  before the trailing element and a PREPEND silently becomes an APPEND. The
  same three values were measured on the PRE-R10 applier, so this is not an R10
  regression: it is the older half of the same defect, and R-0311's fix could
  not reach it because every test in that round used hunks with context. No
  validation fires on any of these inputs — a pure-insertion hunk has no context
  and no removal line to check — so the file is written wrong and reported as
  applied, which is exactly the failure this feature's Done criterion names.
  OPEN.

- R-0313 (Medium, F111 R10, acceptance narrowed by the body-walk rewrite):
  R10 changed a hunk-body line that is none of ` `, `+`, `-` from `pos += 1` to
  ignored. The block declared that for `\ No newline at end of file`, which is
  right, but it also covers a case the block did not name: a BLANK context line
  whose single leading space was stripped in transport arrives as `""`. The old
  applier consumed it as context; the new one ignores it, `old_len` runs one
  short, and the next `-` or context line then validates against the wrong
  original index and returns None. Measured both sides on this machine:
  `'a\n\nb\n'` with `@@ -1,3 +1,3 @@\n a\n\n-b\n+B\n` returned `'a\n\nB\n'`
  before R10 and returns None after it. The direction is SAFE — an
  all-or-nothing rejection that falls back, never a corrupted file — so this is
  not a corruption finding. It matters because F111 exists to apply
  MODEL-generated diffs, and stripping the trailing space off a blank line is
  among the most common things a model or a transport does, so the diff channel
  will fall back on a class of otherwise-valid answers. The fix does NOT belong
  in `_apply_hunks`: `diff_text.split("\n")` also yields a trailing `""` for any
  diff ending in a newline, so treating `""` as context there would make the
  last hunk consume one original line too many — trading a safe rejection for a
  silent corruption. Normalise on the response side, where the diff's own line
  structure is known. Deferred to T002/T003 by decision, not fixed in R11. OPEN.

- R-0314 (Low, F111 R10, fourth instance of an unmeasured count in authored
  text): the R10 block's authored `Landed:` line asserted "six order tests
  added"; C4 adds five and strengthens one. R-0282, R-0305 and R-0309 are the
  same class. R-0309's standing fix — gate authored slices on `cmp`, never on a
  line count — was applied to R10's slices and worked; the count that broke was
  embedded in authored PROSE, which a `cmp` gate cannot catch by construction.
  Widened rule, applied from R11 onward: an authored text states a number about
  the change set only when that number is already measured on disk, and when it
  cannot be — because the change does not exist yet — the text names the thing
  without a count. OPEN.

### DECISION F111 D5 (2026-08-13) — the header off-by-one is in scope too
Chosen: fix R-0312 inside F111, in R11, scoped to the hunk-header start
computation and nothing else. This extends DECISION F111 D4 by the same
reasoning: the feature's Done criterion is that no repair path can silently
corrupt a file, and a pure-insertion hunk that lands its content at the wrong
index — or turns a prepend into an append — is that criterion failing, not an
"applicator semantic" the Do-not-touch list protects. Alternatives considered:
(a) ship the diff channel and file the header bug against a later feature —
rejected, it is the same defect class the round before this one just refused to
ship over; (b) reject every zero-old-count hunk instead of placing it correctly
— rejected, `-U0` diffs are the SMALLEST diffs a model can send and this feature
exists to make repairs smaller, so refusing them would defeat its purpose while
leaving the `@@ -0,0` splice-at-minus-one path reachable anyway. Reverse by
reverting R11's C4 commit; the tests it adds name the behaviour precisely enough
that a reverter knows what they are giving up.
<<<LRG_END

4. C4 — fix `packages/orchestration/source_apply.py`, function `_apply_hunks`
   ONLY, plus tests. Change EXACTLY this and nothing else:
     - read the hunk's OLD COUNT from the header: the existing regex already
       captures it as group(2); an ABSENT group means a count of 1 (that is the
       `@@ -2 +1,0 @@` short form), so treat `None` as 1.
     - when that count is 0 the hunk is a pure insertion whose content goes
       AFTER the named line, so `orig_start = int(m.group(1))`; otherwise
       `orig_start = int(m.group(1)) - 1`, exactly as today.
     - after the body walk, REJECT (`return None`) when the header declared an
       old count of 0 but the body consumed original lines (`old_len != 0`):
       the header contradicts its own body, and guessing which one is right is
       how fuzzy apply starts. This repository applies diffs strictly
       (docs/roadmap/features/T2_F111.md, "Edge cases").
     - REJECT (`return None`) when the computed splice index is negative. It is
       reachable from a malformed `@@ -0,N @@` with N >= 1 whose body adds lines
       without consuming any, so no splice can ever run at a negative index.
   Everything else in the function stays byte-identical: the body walk, both
   validation branches, the ignore branch, the splice and the offset arithmetic.
   Add one sentence to the docstring: a hunk whose old count is 0 is an
   insertion AFTER the line its header names, and every other hunk starts AT it.
   TESTS in `tests/orchestration/test_source_apply_transaction.py`, class
   `TestHunkValidation`. Every expected value below was measured against real
   `git diff -U0` output before this block was written:
     - `@@ -1,0 +2 @@\n+X\n` on `"a\nb\nc\n"` -> `"a\nX\nb\nc\n"`
     - `@@ -0,0 +1 @@\n+X\n` on `"a\nb\nc\n"` -> `"X\na\nb\nc\n"` — the prepend
       that silently appended; name that in the test's docstring
     - `@@ -3,0 +4 @@\n+X\n` on `"a\nb\nc\n"` -> `"a\nb\nc\nX\n"`
     - two zero-count insertion hunks in ONE diff both land correctly, proving
       the running `offset` survives a splice that consumes nothing
     - contradiction rejected: `@@ -1,0 +2 @@\n a\n+X\n` on `"a\na\nb\n"` ->
       None. Use that ORIGINAL, with the repeated `a`, on purpose: it is the
       input where the context line still MATCHES at the shifted index, so the
       test proves the new `old_len != 0` rejection and not the pre-existing
       context validation.
     - negative index rejected: `@@ -0,1 +0,2 @@\n+X\n` on `"a\nb\n"` -> None.
       On the R10 applier this returned `'a\nb\nX\n'`; the reviewer measured it.
     - keep EVERY existing test in the file passing UNCHANGED, including all
       five R10 order tests and every rejection test.
   Commit: fix(f111): place zero-count hunks after their header line   -> push

5. C5 — APPEND at the very end of `.agent/live_review.md`: one blank line, then
   exactly one line, written to `.remedy-wt/f111r11/LANDED` first and applied
   from that file:
Landed: R-0312 — a hunk whose old count is 0 now splices after the line its header names, a contradicting header and a negative index are rejected, and the new cases are pinned by tests, commit C4 of R11.
   In `git show --numstat <C5> -- .agent/live_review.md` the DELETE column must
   be exactly `0` and the insertion count exactly `2`.
   Commit: chore(f111): mark the header fix as landed   -> push

6. C6 — `.agent/plan.md` FULL REPLACEMENT with the slice delimited by
   `<<<PLAN_BEGIN` and `<<<PLAN_END` (marker lines excluded). Write it to
   `.remedy-wt/f111r11/PLAN` first, then `cp .remedy-wt/f111r11/PLAN
   .agent/plan.md`; `cmp` silent. Do NOT gate it on a line count and do NOT
   reflow it: the `cmp` is the proof (finding R-0309).
   Then rewrite `.agent/handoff.md` in YOUR OWN text. COUNT THE LINES BEFORE
   COMMITTING (`wc -l`): 60 or fewer, or carry a DECISION D15 "Deviations,
   declared" line naming the REAL measured count and the mandated content that
   caused it. Mandated content: feature and round (F111 R11); the branch; a
   per-commit SHA table for C1-C6 with insertions; a changed-files table; the
   real gate results a-k with commands and real exit codes; open findings 33
   with next free id R-0315; an item-status table over C1-C6 whose Status cells
   carry the SAME status you declare in the handback (finding R-0306); this
   line verbatim, on its own line (finding R-0304):
Fortschritt: ~62 % (T001 ✅ · T002: Record + Split ✅, Apply+Fallback offen · T003 offen · Applier-Fixes R-0311 + R-0312 ✅) — Schätzung
   and a NEXT SESSION block stating, in this order: that the branch is UNMERGED
   and has NO PR by design, so the Open PR Gate does not apply and Phase 0 must
   sweep `feature/*` branches (finding R-0290) to see it; that R11 closed the
   header half of the applier placement defect; that the next action is R12, the
   apply-and-fallback half of T002; that R-0313 is open BY DECISION and its
   normalisation belongs to T002/T003 on the response side, not to the applier;
   and that NOTHING imports `diff_repair.py` or `diff_repair_response.py` yet —
   both are seams, T003 wires them, and a green suite over an unreferenced
   module is not a working feature. Keep to mandated content: prose padding is a
   finding at any length (AGENTS.md, DECISION D15).
   plan.md and handoff.md land in ONE commit.
   Commit: chore(f111): rewrite the plan and handoff for R11   -> push

<<<PLAN_BEGIN
# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e,
unmerged. Last reviewed SHA: 8644def9 (R10 PASS). Next free finding
ID: R-0315. Open findings: 33, measured on disk as 39 registered
minus 6 resolved; one High (R-0312, fixed in R11, awaiting the
reviewer's Done text). Earlier states carried 30, which was stale.

## Goal
Repairs stop resending whole files: a repair round carries only the
failure-relevant hunks with a configurable context margin, the model
answers with a schema-enforced unified diff that is fence-checked and
applied strictly, and ANY hunk conflict discards the attempt whole
and falls back to today's full-file round with the reason recorded
(docs/roadmap/features/T2_F111.md).

## Current Step
R11 closed the header half of the applier's placement defect: a hunk
whose OLD COUNT is 0 is a pure insertion whose content belongs AFTER
the line its header names, but `_apply_hunks` subtracted 1 from every
header, so such hunks landed one line early and `@@ -0,0 +1 @@`
spliced at index -1, turning a prepend into an append (R-0312,
DECISION F111 D5). R10 had fixed the in-body half (R-0311). T002
otherwise stands at record, validation, fence pre-check, split and
conversion — all on disk, all still WITHOUT a call site.

## Next Steps
1. R12 — the apply half of T002: run a converted patch through
   `apply_structured_patch`, and on ANY hunk conflict discard the
   attempt whole, record `fallback_reason`, report mode
   `full_fallback`, and prove every touched file byte-identical to
   its pre-attempt state.
2. T003 — wire `changed_line_ranges_from_patch` and the response
   channel into `run_builder_bridge_loop`, emit mode and token
   evidence per repair round, add the fixture token comparison.
3. Integration gate, then closure.

## Risks
- The full suite is RED at the merge base with five known ids
  (R-0286): the integration gate compares base against branch.
- R-0313 is open by decision: a blank context line stripped to ""
  makes a diff REJECT where the pre-R10 applier applied it. Safe
  direction, but the normalisation belongs on the response side and
  T002/T003 must carry it.
- `review_scope` is the only module that reads hunk headers or
  splits a diff by path; `source_apply._apply_hunks` is the only
  applier. Neither may be duplicated.
- A green suite over unreferenced modules is not a working feature.
  T003 is the round that makes F111 real.
<<<PLAN_END

Done when (record command + real exit code + counted value; never the word
"green"):
  a. `cmp .remedy-wt/f111r11/BLOCK .agent/authored/f111-r11-1.md` silent;
     `cmp .agent/authored/f111-r11-1.md .agent/last_block.md` silent;
     `cmp .remedy-wt/f111r11/PLAN .agent/plan.md` silent.
  b. `git show --numstat <C3> -- .agent/live_review.md` -> delete column `1`;
     `git show --numstat <C5> -- .agent/live_review.md` -> `2 0` exactly.
     Report C3's real insertion count.
  c. on the final `.agent/live_review.md`:
     `grep -c '^- R-0'` -> 39 ; `grep -c '^Done:'` -> 6
     `grep -c '^Landed:'` -> 1 ; `grep -c '^### R10 — PASS'` -> 1
     `grep -c '^### DECISION F111 D5'` -> 1
     python3 -c "import pathlib;print(pathlib.Path('.agent/live_review.md').read_text().count(pathlib.Path('.remedy-wt/f111r11/LRG').read_text()))"
     -> exit 0, printed count 1
  d. `grep -c '^## Goal' .agent/plan.md` -> 1 ;
     `grep -c '^## Next Steps' .agent/plan.md` -> 1 ;
     `grep -c 'R-0315' .agent/plan.md` -> 1 ; report `wc -l` as a fact, not as
     a gate. `wc -l < .agent/handoff.md` -> the real number, 60 or fewer unless
     the D15 line declares it; `grep -c '^Fortschritt: ' .agent/handoff.md` -> 1
  e. THE FIX, proved by value and not by colour. Run and paste the real output:
     python3 -c "from packages.orchestration.source_apply import _apply_hunks as A; print(repr(A('a\nb\nc\n','@@ -1,0 +2 @@\n+X\n')), repr(A('a\nb\nc\n','@@ -0,0 +1 @@\n+X\n')), repr(A('a\nb\nc\n','@@ -3,0 +4 @@\n+X\n')))"
     -> exit 0, and the three printed values MUST be
     'a\nX\nb\nc\n' 'X\na\nb\nc\n' 'a\nb\nc\nX\n'.
     The reviewer measured this same command on the R10 applier; it printed
     'X\na\nb\nc\n' 'a\nb\nc\nX\n' 'a\nb\nX\nc\n' — the corruption, on this
     machine, not recalled.
  f. the R10 fix must still hold:
     python3 -c "from packages.orchestration.source_apply import _apply_hunks as A; print(repr(A('alpha\nbeta\ngamma\n','@@ -1,3 +1,3 @@\n alpha\n-beta\n+BETA\n gamma\n')))"
     -> exit 0, printed value 'alpha\nBETA\ngamma\n'.
  g. `python3 -m pytest tests/orchestration/test_source_apply_transaction.py
     tests/orchestration/test_source_apply.py
     tests/orchestration/test_fence_e2e.py -q` -> exit 0, at least 179 passed
     (179 is the count the reviewer measured at the R10 gate; report the real
     one).
  h. `python3 -m pytest tests/orchestration/test_diff_repair.py
     tests/orchestration/test_diff_repair_response.py
     tests/orchestration/test_review_scope.py tests/cli/test_golden_path.py -q`
     -> exit 0, 138 passed, unchanged: this round touches none of those modules,
     and 42 of the 138 are the canary. Do NOT run
     tests/ui_server/test_dashboard_contract.py (R-0221: it runs a real npm
     build).
  i. the applier's OTHER consumers, which this fix could regress:
     `python3 -m pytest tests/test_patch_apply.py
     tests/orchestration/test_autonomy.py
     tests/orchestration/test_fence_production_e2e.py -q` -> report the real
     exit code and count; the reviewer measured 225 passed at the R10 gate. If
     any of these is now failing, check whether it ALREADY failed at 8644def9 by
     running the same command in a disposable worktree at 8644def9 and say so —
     a pre-existing red is not this round's regression, but an undeclared one is
     a finding.
  j. red-proof, inside a DISPOSABLE `git worktree` at HEAD and nowhere else: in
     that worktree only, restore the unconditional `orig_start =
     int(m.group(1)) - 1` and remove the two new rejections, run
     `python3 -m pytest tests/orchestration/test_source_apply_transaction.py -q`
     and record the real exit code and the failing test ids; then remove and
     prune the worktree. If it does NOT go red, say so plainly.
  k. `git status --porcelain` -> empty; `git worktree list` -> one entry;
     per-commit insertions each < 500;
     `git rev-list --left-right --count origin/feature/f111-diff-only-repair...HEAD`
     -> `0 0` after the final push.
Handback:    completion report (per-commit table, changed-files table,
             item-status table over C1-C6 with real statuses, raw gate results
             a-k with real exit codes) and `.agent/handoff.md` rewritten as C6.
             Do not merge, do not open a PR.
