── STEP R10/4 — F111 Diff-only repair — SESSION CLOSE, applier order fix ─────
Goal:        Persist the R9 gate and findings R-0309, R-0310 and R-0311, fix
             R-0311 — `source_apply._apply_hunks` inserts every added line at
             the hunk's START instead of at its position, silently reordering
             any file whose hunk adds below its first line — and close the
             session. The apply-and-fallback function of T002 is R11 and is
             NOT in this round.
Bundle:      C1 block save; C2 last_block mirror; C3 gate+findings append;
             C4 the applier fix + tests; C5 the Landed line; C6 plan and
             closing handoff. Commit AND push at every item.
Change:      EXACTLY these paths and nothing else:
             .agent/authored/f111-r10-1.md (new), .agent/last_block.md,
             .agent/live_review.md, .agent/plan.md, .agent/handoff.md,
             packages/orchestration/source_apply.py,
             tests/orchestration/test_source_apply_transaction.py.
Constraints: AGENTS.md in full. Apply every authored slice by READING ITS
             SCRATCH FILE (`cat` / `cp`) — never retype, never reflow.
             Do NOT touch `.agent/candidates.md` or `.agent/decisions.md`.
             Do NOT touch `diff_repair.py`, `diff_repair_response.py`,
             `review_scope.py`, `structured_patch.py`, `builder_bridge.py`,
             `repair_context.py` or `pingpong_loop.py`.
             Change NOTHING in `source_apply.py` outside `_apply_hunks`.
             Write no `Done:` line: only reviewer-authored text sets Resolved
             (docs/agents/planner_reviewer_prompt.md §4.4). The ONE `Landed:`
             line C5 orders is the worker's correct marker.
             This is the LAST round of the session — after C6, stop and hand
             back. Do not start R11.

PROCEDURE (in order; commit AND push at every numbered item):

0. Preconditions: `git status --porcelain` empty; branch is
   feature/f111-diff-only-repair; `git log -1 --format=%h` is 33f408b2.
   Any mismatch => STOP and hand back.  `mkdir -p .remedy-wt/f111r10`.

1. C1 — Save this ENTIRE step block (from the `── STEP R10/4` line through the
   final `Handback:` line, byte for byte) to `.remedy-wt/f111r10/BLOCK`, then
   `cp .remedy-wt/f111r10/BLOCK .agent/authored/f111-r10-1.md`; `cmp` silent.
   Commit: chore(f111): save the R10 step block verbatim   -> push

2. C2 — `cp .agent/authored/f111-r10-1.md .agent/last_block.md`; `cmp` silent.
   Commit: chore(f111): mirror the R10 block into last block   -> push

3. C3 — FINDINGS FIRST. Write the slice delimited by `<<<LRG_BEGIN` and
   `<<<LRG_END` (marker lines excluded) to `.remedy-wt/f111r10/LRG`, then
   `cat .remedy-wt/f111r10/LRG >> .agent/live_review.md`.
   PURE APPEND: in `git show --numstat <C3> -- .agent/live_review.md` the
   DELETE column must be exactly `0`; report the real insertion count.
   Commit: chore(f111): record the R9 gate and findings R-0309 to R-0311 -> push

<<<LRG_BEGIN

### R9 — PASS (2026-08-13)
Reviewed by the main session over 456a25e9..33f408b2. Every ordered gate was
re-run by the reviewer, and the new split was probed live against the real
applier rather than read off the handback. Transport: PRIMARY cmp proof, no
digest fallback — `.remedy-wt/f111r9/BLOCK`, `.agent/authored/f111-r9-1.md`
and `.agent/last_block.md` are byte-identical, `.remedy-wt/f111r9/PLAN` and
`.agent/plan.md` are byte-identical, and `str.count` of both the LRG and the
DONE slice against `.agent/live_review.md` prints 1. Numstat purity: `50 0`
for the gate append and `5 1` for the R-0307 resolution, the single deletion
being the retired `Landed:` line. Markers: 33 `- R-0`, 5 `Done:`, 0 `Landed:`
(exit 1, the pass), 1 `### R8 — PASS`. Caps: the block is 330 lines, under the
DECISION F105 D5 limit of 400; per-commit insertions 330/262/50/5/139/110/93,
each under 500. Tests: `python3 -m pytest
tests/orchestration/test_review_scope.py
tests/orchestration/test_diff_repair_response.py
tests/orchestration/test_diff_repair.py tests/cli/test_golden_path.py -q` exit
0, 138 passed — 39 (32 before, 7 new), 27 (23 before, 4 new), 30 unchanged, 42
canary; `python3 -m pytest tests/orchestration/test_final_verifier.py
tests/orchestration/test_reviewer_prompt_scope.py
tests/orchestration/test_pingpong.py tests/test_path_utils.py
tests/test_data_paths.py -q` exit 0, 197 passed — the 146 `_parse_diff`
consumer pin the reviewer measured BEFORE the round, unchanged, plus the 51
repo-wide guards. Hygiene: `git status --porcelain` empty, `git worktree list`
one entry, remote comparison `0 0`. Scope: exactly the nine ordered paths.

Deviation ACCEPTED: C7 applied a 47-line PLAN slice where the block said 46.
The worker applied the authored bytes verbatim and declared the mismatch
rather than reflowing text to hit a number, which is the correct call — the
error is the reviewer's and is registered as R-0309 below.

- R-0309 (Low, F111 R9, reviewer-side arithmetic in an authored block): the R9
  block stated its PLAN slice was 46 lines and gated `wc -l` on that number;
  the slice is 47 lines. Third instance of the class after R-0282 and R-0305,
  and the second in three rounds, so the rule R-0305 stated is not being
  applied: any count an authored block asserts about a file — including a file
  the block itself carries — is MEASURED before emission, never recalled. The
  reviewer cannot measure its own not-yet-written slice with a shell, so the
  standing fix is different in kind: gate authored slices on `cmp` against the
  applied file, which proves byte identity, and never on a line count, which
  proves nothing the `cmp` does not already prove. OPEN.

- R-0310 (Low, F111 R9, cosmetic residue in a correct function):
  `split_diff_by_path` drops preamble before the FIRST `---` line, so in a
  git-style multi-file diff the `diff --git` and `index` lines introducing
  file N+1 stay at the TAIL of file N's section. The worker disclosed this
  instead of writing a test that would have to pass dishonestly. The reviewer
  proved the residue harmless: `_apply_hunks` breaks its hunk body on any line
  starting with `diff `, and its outer loop skips every line that is not a
  hunk header, so both sections of a two-file git diff applied to the right
  content in a live probe. Kept for v1 as a cosmetic wart, not a correctness
  defect; a section is still a standalone applicable diff. OPEN.

- R-0311 (High, F111 R9, pre-existing silent file corruption in the
  applicator): `source_apply._apply_hunks` collects each addition WITH its
  position, then throws those positions away and inserts every added line at
  `insert_at = orig_start + offset` — the start of the hunk. Any hunk whose
  additions are not on its first line therefore writes them to the wrong
  place. On the repository's own test input, `original = "alpha\nbeta\ngamma\n"`
  with `@@ -1,3 +1,3 @@\n alpha\n-beta\n+BETA\n gamma\n`, the function returns
  `alpha\ngamma\nBETA\n` where the diff says `alpha\nBETA\ngamma\n`. The
  existing guard `TestHunkValidation::test_correct_context_applies` passes only
  because it asserts `"BETA" in result` and never checks order, which is how
  this survived. Every `intent_kind="unified_diff"` patch in Remedy lands
  through this function, and F111's Done criterion is literally that no repair
  path can silently corrupt a file, so the diff channel cannot ship over it.
  Fixed in R10 per DECISION F111 D4. OPEN.

### DECISION F111 D4 (2026-08-13) — the applier order fix is in scope
Chosen: repair `_apply_hunks` inside F111, in R10, scoped to hunk application
order and nothing else. Alternatives considered: (a) route it to a new feature
and ship F111's diff channel over a corrupting applier — rejected, because the
feature's own Done criterion forbids exactly that; (b) work around it in
`diff_repair_response` — rejected, because it would be a second applier, which
this feature has refused twice already. The feature file's Do-not-touch names
"applicator semantics", and an off-by-one in where a line lands is not a
semantic of the applicator, it is a defect in it: the all-or-nothing contract,
the fence preflight, the snapshot gate and the rollback path are untouched by
this fix. Reverse by reverting R10's C4 commit; the tests it adds name the
behaviour precisely enough that a reverter knows what they are giving up.
<<<LRG_END

4. C4 — fix `packages/orchestration/source_apply.py`, function `_apply_hunks`
   ONLY, plus tests in `tests/orchestration/test_source_apply_transaction.py`.
   Rewrite the per-hunk application as a SPLICE, keeping every validation
   the function performs today, byte for byte in behaviour on rejection:
     - `orig_start = int(m.group(1)) - 1`, as today;
     - walk the hunk body exactly as today, keeping the SAME break condition
       (`@@`, `diff `, `---`, `+++`) and the SAME strict checks: a `-` or a
       ` ` line whose index is out of range, or whose content does not equal
       `lines[actual_idx]`, still returns None immediately;
     - while walking, build `new_block`: append `line[1:]` for a ` ` line and
       for a `+` line, append nothing for a `-` line; and count `old_len` as
       the number of ` ` and `-` lines the hunk consumed;
     - after the body, splice:
       `result_lines[orig_start + offset : orig_start + offset + old_len] = new_block`
       then `offset += len(new_block) - old_len`;
     - a line inside a hunk body that is none of ` `, `+`, `-` (in practice
       `\ No newline at end of file`) is IGNORED: it neither consumes an
       original line nor contributes to `new_block`. This is a deliberate
       change from today's `pos += 1`, which made such a marker swallow a
       line. Declare it in the handback.
   Delete the now-unused `removals`/`additions` bookkeeping and the
   `insert_at` block. Update the function's docstring to say that a hunk is
   applied by splicing its new block over the exact original range it
   consumed, and that context and removal lines are still validated against
   real file content before anything is written.
   TESTS in `tests/orchestration/test_source_apply_transaction.py`,
   class `TestHunkValidation`:
     - STRENGTHEN the existing `test_correct_context_applies` to assert the
       FULL expected string `"alpha\nBETA\ngamma\n"` instead of the
       substring check `"BETA" in result`. Its weakness is why R-0311
       survived; leaving it weak leaves the hole open.
     - add: an addition in the MIDDLE of a hunk lands between its neighbours
       (`"a\nb\nc\nd\n"` with `@@ -1,3 +1,4 @@\n a\n b\n+NEW\n c\n` ->
       `"a\nb\nNEW\nc\nd\n"`);
     - add: an addition at the END of a hunk lands last, not first;
     - add: TWO hunks in one diff both land correctly, proving the running
       `offset` is right after a splice that changes length;
     - add: a pure deletion hunk removes exactly its line and nothing else;
     - add: a `\ No newline at end of file` marker inside a hunk body does not
       swallow the following line;
     - keep every existing rejection test passing UNCHANGED: wrong context,
       wrong removal, context out of range, removal out of range, empty diff.
   Commit: fix(f111): apply each diff hunk at its own position   -> push

5. C5 — APPEND at the very end of `.agent/live_review.md`: one blank line,
   then exactly one line, written to `.remedy-wt/f111r10/LANDED` first and
   applied from that file:
Landed: R-0311 — `_apply_hunks` now splices each hunk's new block over the range it consumed; six order tests added and the weak substring assertion strengthened, commit C4 of R10.
   In `git show --numstat <C5> -- .agent/live_review.md` the DELETE column
   must be exactly `0` and the insertion count exactly `2`.
   Commit: chore(f111): mark the applier order fix as landed   -> push

6. C6 — `.agent/plan.md` FULL REPLACEMENT with the slice delimited by
   `<<<PLAN_BEGIN` and `<<<PLAN_END` (marker lines excluded). Write it to
   `.remedy-wt/f111r10/PLAN` first, then `cp .remedy-wt/f111r10/PLAN
   .agent/plan.md`; `cmp` silent. Do NOT gate it on a line count and do NOT
   reflow it: the `cmp` is the proof (finding R-0309).
   Then rewrite `.agent/handoff.md` in YOUR OWN text as the SESSION-CLOSING
   handoff. COUNT THE LINES BEFORE COMMITTING (`wc -l`): 60 or fewer, or
   carry a DECISION D15 "Deviations, declared" line naming the REAL measured
   count and the mandated content that caused it. Mandated content: feature
   and round (F111 R10, SESSION CLOSE); the branch; a per-commit SHA table
   for C1-C6 with insertions; a changed-files table; the real gate results
   below with commands and real exit codes; open findings 30 with next free
   id R-0312; an item-status table over C1-C6 whose Status cells carry the
   SAME status you declare in the handback (finding R-0306); this line
   verbatim, on its own line (finding R-0304):
Fortschritt: ~60 % (T001 ✅ · T002: Record + Split ✅, Apply+Fallback offen · T003 offen · Applier-Fix R-0311 ✅) — Schätzung
   and a NEXT SESSION block stating, in this order: that the branch is
   UNMERGED and has NO PR by design, so the Open PR Gate does not apply and
   Phase 0 must sweep `feature/*` branches (finding R-0290) to see it; what
   this session completed (the R7, R8 and R9 gates; T002's record,
   validation, fence pre-check, per-path split and conversion; and the
   R-0311 applier fix under DECISION F111 D4); that the next action is R11,
   the apply-and-fallback half of T002; and that NOTHING imports
   `diff_repair.py` or `diff_repair_response.py` yet — both are seams, T003
   wires them, and a green suite over an unreferenced module is not a
   working feature. Keep to mandated content: prose padding is a finding at
   any length (AGENTS.md, DECISION D15).
   plan.md and handoff.md land in ONE commit.
   Commit: chore(f111): write the session closing handoff   -> push

<<<PLAN_BEGIN
# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e,
unmerged. Last reviewed SHA: 33f408b2 (R9 PASS). Next free finding
ID: R-0312. Open findings: 30, one High (R-0311, fixed in R10,
awaiting the reviewer's Done text), the rest Low or Medium.

## Goal
Repairs stop resending whole files: a repair round carries only the
failure-relevant hunks with a configurable context margin, the model
answers with a schema-enforced unified diff that is fence-checked and
applied strictly, and ANY hunk conflict discards the attempt whole
and falls back to today's full-file round with the reason recorded
(docs/roadmap/features/T2_F111.md).

## Current Step
R10 fixed `source_apply._apply_hunks`, which inserted every added
line at the hunk's START instead of at its position, so any hunk
whose additions were not on its first line silently reordered the
file it applied to (finding R-0311, DECISION F111 D4). The applier
now splices each hunk's new block over the exact original range it
consumed. T002 otherwise stands at record, validation, fence
pre-check, split and conversion — all on disk in
`diff_repair_response.py` and `review_scope.split_diff_by_path`, and
all still WITHOUT a call site.

## Next Steps
1. R11 — the apply half of T002: run a converted patch through
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
- R-0311 was live for the whole life of the structured unified-diff
  path. Any earlier evidence claiming a clean diff apply predates
  this fix and cannot be trusted about line ORDER.
- `review_scope` is now the only module that reads hunk headers or
  splits a diff by path; `source_apply._apply_hunks` is the only
  applier. Neither may be duplicated.
- A green suite over unreferenced modules is not a working feature.
  T003 is the round that makes F111 real.
<<<PLAN_END

Done when (record command + real exit code + counted value; never the word
"green"):
  a. `cmp .remedy-wt/f111r10/BLOCK .agent/authored/f111-r10-1.md` silent;
     `cmp .agent/authored/f111-r10-1.md .agent/last_block.md` silent;
     `cmp .remedy-wt/f111r10/PLAN .agent/plan.md` silent.
  b. `git show --numstat <C3> -- .agent/live_review.md` -> delete column `0`;
     `git show --numstat <C5> -- .agent/live_review.md` -> `2 0` exactly.
     Report C3's real insertion count.
  c. on the final `.agent/live_review.md`:
     `grep -c '^- R-0'` -> 36 ; `grep -c '^Done:'` -> 5
     `grep -c '^Landed:'` -> 1 ; `grep -c '^### R9 — PASS'` -> 1
     `grep -c '^### DECISION F111 D4'` -> 1
     python3 -c "import pathlib;print(pathlib.Path('.agent/live_review.md').read_text().count(pathlib.Path('.remedy-wt/f111r10/LRG').read_text()))"
     -> exit 0, printed count 1
  d. `grep -c '^## Goal' .agent/plan.md` -> 1 ;
     `grep -c '^## Next Steps' .agent/plan.md` -> 1 ;
     `grep -c 'R-0312' .agent/plan.md` -> 1 ; report `wc -l` as a fact, not
     as a gate. `wc -l < .agent/handoff.md` -> the real number, 60 or fewer
     unless the D15 line declares it; `grep -c '^Fortschritt: '` -> 1
  e. THE FIX, proved by value and not by colour. Run and paste the real
     output of:
     python3 -c "from packages.orchestration.source_apply import _apply_hunks; print(repr(_apply_hunks('alpha\nbeta\ngamma\n', '@@ -1,3 +1,3 @@\n alpha\n-beta\n+BETA\n gamma\n')))"
     -> exit 0, and the printed value MUST be 'alpha\nBETA\ngamma\n'.
     Before your fix this same command printed 'alpha\ngamma\nBETA\n'.
  f. `python3 -m pytest tests/orchestration/test_source_apply_transaction.py
     tests/orchestration/test_source_apply.py
     tests/orchestration/test_fence_e2e.py -q` -> exit 0, at least 174 passed
     (174 is the pre-round count the reviewer measured; report the real one).
  g. `python3 -m pytest tests/orchestration/test_diff_repair.py
     tests/orchestration/test_diff_repair_response.py
     tests/orchestration/test_review_scope.py -q` -> exit 0, 96 passed
     (30 + 27 + 39), unchanged: this round touches none of those modules.
     `python3 -m pytest tests/cli/test_golden_path.py -q` -> exit 0, 42
     passed (canary). Do NOT run tests/ui_server/test_dashboard_contract.py
     (R-0221: it runs a real npm build).
  h. the applier's OTHER consumers, which this fix could regress:
     `python3 -m pytest tests/test_patch_apply.py
     tests/orchestration/test_autonomy.py
     tests/orchestration/test_fence_production_e2e.py -q` -> report the real
     exit code and count. If any of these was ALREADY failing at 33f408b2,
     check that by running the same command in a disposable worktree at
     33f408b2 and say so — a pre-existing red is not this round's regression,
     but an undeclared one is a finding.
  i. red-proof, inside a DISPOSABLE `git worktree` at HEAD and nowhere else:
     in that worktree only, revert the splice to the old
     `insert_at = orig_start + offset` insertion, run
     `python3 -m pytest tests/orchestration/test_source_apply_transaction.py -q`
     and record the real exit code and the failing test ids; then remove and
     prune the worktree. If it does NOT go red, say so plainly.
  j. `git status --porcelain` -> empty; `git worktree list` -> one entry;
     per-commit insertions each < 500;
     `git rev-list --left-right --count origin/feature/f111-diff-only-repair...HEAD`
     -> `0 0` after the final push.
Handback:    completion report (per-commit table, changed-files table,
             item-status table over C1-C6 with real statuses, raw gate
             results a-j with real exit codes) and `.agent/handoff.md`
             rewritten as C6. Do not merge, do not open a PR.
