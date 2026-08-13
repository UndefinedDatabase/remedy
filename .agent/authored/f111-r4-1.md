── STEP R4/4 — F111 Diff-only repair — SESSION CLOSE ─────────────────────────
Goal:        Persist the R3 gate and finding R-0300, refresh the plan, and
             write the session-closing handoff. No code this round.
Bundle:      C1 block save; C2 last_block mirror; C3 findings append;
             C4 plan rewrite; C5 closing handoff. Push after EVERY commit.
Change:      EXACTLY these paths and nothing else:
             .agent/authored/f111-r4-1.md (new), .agent/last_block.md,
             .agent/live_review.md, .agent/plan.md, .agent/handoff.md.
             No production file, no test file, no docs change this round.
Constraints: AGENTS.md in full. Apply authored slices by COPYING or
             `cat >>`; never retype or reflow them. Do NOT create a PR, do
             NOT merge, never touch main, never force-push. Never write a
             `Done:` line. This round lands NO fix, so it writes no new
             `Landed:` line either — the one already in the file stays.
             Scratch stays under .remedy-wt/.

AUTHORED SLICES — TWO stated digests (LRG, PLAN), plus BLOCK which is pinned
by the C1 cmp rather than by a digest (R-0298):
  .remedy-wt/f111r4/LRG   sha256=9892593c75f2a82124dd0d6dd96414c47d960476aea9f5f85513d78122a6e2b1  append to .agent/live_review.md
  .remedy-wt/f111r4/PLAN  sha256=b088e70eca313c3b5ed89b8bda80d6a1e6691eb8c286c7ce5e546375bbe41186  replaces .agent/plan.md
  .remedy-wt/f111r4/BLOCK = this entire step block, byte for byte (cmp only)

PROCEDURE (in order; commit AND push at every numbered item):

0. Preconditions: `git status --porcelain` empty; branch is
   feature/f111-diff-only-repair; `git log -1 --format=%h` is 4717ce8c.
   Verify the TWO stated digests. Any mismatch => STOP.

1. C1 — `cp .remedy-wt/f111r4/BLOCK .agent/authored/f111-r4-1.md`; `cmp`
   silent. Commit: chore(f111): save the R4 step block verbatim   -> push

2. C2 — `cp .agent/authored/f111-r4-1.md .agent/last_block.md`; `cmp`
   silent. Commit: chore(f111): mirror the R4 block into last block  -> push

3. C3 — `cat .remedy-wt/f111r4/LRG >> .agent/live_review.md`
   PURE APPEND: `git show --numstat <C3> -- .agent/live_review.md` must read
   `43 0`. A nonzero delete column means a rewrite: STOP and hand back.
   Commit: chore(f111): record the R3 gate and finding R-0300   -> push

4. C4 — `cp .remedy-wt/f111r4/PLAN .agent/plan.md`; `cmp` silent.
   Commit: chore(f111): rewrite the plan for the session close   -> push

5. C5 — rewrite .agent/handoff.md yourself (your own text), <=60 lines.
   COUNT THE LINES BEFORE COMMITTING (`wc -l`); the R3 handoff needed two
   extra commits because it was written first and measured second. It must
   contain: feature and round (F111 R4, SESSION CLOSE); the branch; a
   per-commit SHA table for C1-C5 (C5 self-referential); a changed-files
   table; the real gate results below; open findings 25 with next free ID
   R-0301; an item-status table over C1-C5, each item exactly once; and a
   NEXT SESSION block stating, in this order:
     - the branch is UNMERGED and has NO PR by design; the next session's
       Open PR Gate does not apply because no PR exists — it resumes this
       branch directly;
     - work completed: R1 claim and state reset, R2 DECISION F111 D1 plus
       T001's `select_repair_hunks` (21 tests, mutation-proved), R3 the
       `out_of_bounds` fix;
     - next action: R5 closes R-0300 with one test, then wires T001 — but
       the wiring source of line ranges MUST be settled by reading code
       first (see .agent/plan.md Next Steps 1);
     - the three reviewer-side findings this session opened against its own
       blocks: R-0298, and for context R-0294 and R-0297 from F107.
   Commit: chore(f111): write the session closing handoff   -> push

Done when (record command + real exit code + counted value; never the word
"green"):
  a. the two stated digests match; cmp BLOCK vs authored silent; cmp
     authored vs last_block silent; cmp PLAN vs .agent/plan.md silent.
  b. `git show --numstat <C3> -- .agent/live_review.md` -> `43 0`
  c. `grep -c '^- R-0' .agent/live_review.md` -> 25
     `grep -c '^Landed:' .agent/live_review.md` -> 1 (unchanged)
     `grep -c '^Done:' .agent/live_review.md` -> 0 (exit 1 is the pass)
     `grep -c '^### R3 — PASS' .agent/live_review.md` -> 1
     `wc -l < .agent/plan.md` -> 40; `wc -l < .agent/handoff.md` -> <= 60
  d. `python3 -m pytest tests/cli/test_golden_path.py -q` -> exit 0 (canary)
  e. `python3 -m pytest tests/orchestration/test_test_runner.py -q -k 'plan_md or context_md'`
     -> exit 0, 3 passed. Do NOT run
     tests/ui_server/test_dashboard_contract.py (R-0221: real npm build).
  f. `python3 -m pytest tests/orchestration/test_diff_repair.py -q` -> exit 0,
     21 passed (unchanged: this round touches no code).
  g. `git status --porcelain` -> empty; `git worktree list` -> one entry;
     `git rev-list --left-right --count origin/feature/f111-diff-only-repair...HEAD`
     -> `0 0`; per-commit insertions each < 500.
Handback:    completion report (tables + raw gate results) and
             .agent/handoff.md rewritten as C5. Do not merge, do not open a
             PR, do not touch .agent/candidates.md or .agent/decisions.md.

<<<BEGIN SLICE LRG sha256=9892593c75f2a82124dd0d6dd96414c47d960476aea9f5f85513d78122a6e2b1 lines=43>>>

### R3 — PASS (2026-08-13)
Reviewed by the main session over 1bf62e2f..4717ce8c. Re-run by the reviewer,
not read off the handback: `python3 -m pytest
tests/orchestration/test_diff_repair.py -q` exit 0, 21 passed (18 before this
round); `python3 -m pytest tests/cli/test_golden_path.py -q` exit 0, 42
passed. The mutation red-proof was RE-RUN INDEPENDENTLY by the reviewer in
its own disposable worktree: reverting the call-site reason to a bare
`no_ranges` turns exactly two tests red,
`TestOutOfBounds::test_range_past_eof_is_out_of_bounds` and
`TestOutOfBounds::test_out_of_bounds_path_does_not_block_present_one`, at
2 failed / 19 passed — matching the worker's report. That worktree was
removed and pruned; `git worktree list` shows only the primary checkout.
Transport: primary cmp proof, no digest fallback — `.remedy-wt/f111r3/BLOCK`
and `.agent/authored/f111-r3-1.md` byte-identical at sha256 a5088325...,
`.agent/last_block.md` equal to both, `.agent/plan.md` equal to its original,
and the 51-line findings slice sits verbatim inside `.agent/live_review.md`.
Append purity by numstat: `51 0` for the findings commit, `2 0` for the
Landed line. Scope: exactly the seven ordered paths. The findings-first
ordering held — C3 persisted R-0298 and R-0299 BEFORE any code commit.
Markers: 24 `- R-0` entries, exactly 1 `Landed:`, 0 `Done:`, and the Landed
line names its commit by SUBJECT rather than by a SHA it could not contain
(R-0274). The fix is minimal: `_expand_and_merge_ranges` is unchanged and the
discrimination happens at the call site. Deviation ACCEPTED: C7 took three
commits because the first handoff came in at 62 lines against its own 60-line
cap; the worker trimmed forward rather than force-pushing — the correct order
of preferences — and declared it. One finding registered below.

- R-0300 (Low, F111 R3, uncovered behaviour change, self-declared by the
  worker in its handback): the R-0299 fix also changes what a range against a
  ZERO-LINE file reports. `_expand_and_merge_ranges` clamps `end` to
  `min(line_count, ...)`, which is 0 for an empty file, while `start` is at
  least 1 — so every span is dropped, and the new call-site discrimination at
  `packages/orchestration/diff_repair.py:136-141` then reports
  `out_of_bounds` where the pre-fix code reported `no_ranges`. The new reading
  is the correct one under the round's own definition (lines were named and
  none of them exist in that file), so nothing on disk is wrong. It is
  registered because it is a SECOND behaviour change beyond the past-EOF case
  the round was ordered to make, and no test pins it — an unpinned behaviour
  is one refactor away from silently reverting. The worker found it in its own
  diff and declared it rather than leaving it for a reader, which is the
  behaviour these rounds are supposed to produce. Fix, one test: an empty file
  with a non-empty range reports `out_of_bounds`. OPEN.
<<<END SLICE LRG>>>

<<<BEGIN SLICE PLAN sha256=b088e70eca313c3b5ed89b8bda80d6a1e6691eb8c286c7ce5e546375bbe41186 lines=40>>>
# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e.
Next free finding ID: R-0301. Last reviewed SHA: 4717ce8c (R3 PASS).
Open findings: 25, none above Medium.

## Goal
Repairs stop resending whole files: a repair round carries only the
failure-relevant hunks with a configurable context margin, the model answers
with a schema-enforced unified diff that is fence-checked and applied
strictly, and ANY hunk conflict discards the attempt whole and falls back to
today's full-file round with the reason recorded
(docs/roadmap/features/T2_F111.md).

## Current Step
R4 — persist the R3 gate and finding R-0300, then END THE SESSION cleanly at
its context limit. T001's helper `select_repair_hunks` is built, tested at 21
tests and mutation-proved, but has NO call site yet. DECISION F111 D1 is on
disk and the feature file is amended.

## Next Steps
1. R5 — close R-0300 with one test (empty file + non-empty range reports
   `out_of_bounds`), then WIRE T001. Settle this FIRST by reading code, never
   by assuming: `repair_context.build_repair_context(job_id, test_run_event,
   events)` carries `affected_files` (paths only), takes no repo_root and has
   no line ranges, so the ranges must come from elsewhere — most likely
   `review_scope._parse_diff` over the diff of the `source_patch_applied`
   event. Confirm that event actually carries a diff before designing.
2. T002 — versioned unified-diff response schema, fence pre-check before any
   apply, strict apply with an all-or-nothing conflict fallback, on the
   `builder_bridge` seam D1 selected.
3. T003 — mode and token evidence per repair round, plus a fixture comparison
   recording both modes' token counts.
4. Integration gate, then closure.

## Risks
- The full suite is RED at the merge base with five known ids (R-0286): the
  integration gate compares base against branch, never absolute green.
- `review_scope._parse_diff` and `source_apply._apply_hunks` already exist and
  must be reused, never duplicated.
<<<END SLICE PLAN>>>
