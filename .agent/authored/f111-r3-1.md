── STEP R3/~12 — F111 Diff-only repair ───────────────────────────────────────
Goal:        Persist the R2 gate and findings R-0298 and R-0299, then fix
             R-0299: the omissions record gets a distinct `out_of_bounds`
             reason so a stale line range stops being reported as "no ranges".
Bundle:      C1 block save; C2 last_block mirror; C3 findings append;
             C4 the R-0299 fix + tests; C5 the Landed line; C6 plan rewrite;
             C7 handoff. Push after EVERY commit.
Change:      EXACTLY these paths and nothing else:
             .agent/authored/f111-r3-1.md (new), .agent/last_block.md,
             .agent/live_review.md, .agent/plan.md, .agent/handoff.md,
             packages/orchestration/diff_repair.py,
             tests/orchestration/test_diff_repair.py.
             No other production file. No docs/ or docs/roadmap/ change this
             round, so the docs gate does not apply.
Constraints: AGENTS.md in full. Apply authored slices by COPYING or
             `cat >>` exactly as each step says; never retype or reflow
             them. Do NOT create a PR, do NOT merge, never touch main, never
             force-push. Never write a `Done:` line — that text is the
             reviewer's alone. This round DOES land a fix, so a `Landed:`
             line is REQUIRED and is yours to author (finding R-0285: a
             zero-gate on `^Landed:` is only ever safe in a round that lands
             nothing). Scratch stays under .remedy-wt/.

AUTHORED SLICES — TWO stated digests (LRG, PLAN), plus BLOCK which is pinned
by the C1 cmp rather than by a digest (a file cannot state the hash of bytes
that include the statement — finding R-0298):
  .remedy-wt/f111r3/LRG   sha256=8059f5a3fb82a610e17c27f8a58b79e5cc8dbdea25c9f30d2a272b01409bcaa3  append to .agent/live_review.md
  .remedy-wt/f111r3/PLAN  sha256=b28dd64bec6843352addde171f729f028ec48b552c33ed0c5c658c213ec3e78c  replaces .agent/plan.md
  .remedy-wt/f111r3/BLOCK = this entire step block, byte for byte (cmp only)

PROCEDURE (in order; commit AND push at every numbered item):

0. Preconditions: `git status --porcelain` empty; branch is
   feature/f111-diff-only-repair; `git log -1 --format=%h` is 5d8d8c56.
   Verify the TWO stated digests (LRG, PLAN). Any mismatch => STOP.

1. C1 — `cp .remedy-wt/f111r3/BLOCK .agent/authored/f111-r3-1.md`; `cmp`
   silent. Commit: chore(f111): save the R3 step block verbatim   -> push

2. C2 — `cp .agent/authored/f111-r3-1.md .agent/last_block.md`; `cmp`
   silent. Commit: chore(f111): mirror the R3 block into last block  -> push

3. C3 — FINDINGS PERSIST FIRST, in their own commit, before any fix:
   `cat .remedy-wt/f111r3/LRG >> .agent/live_review.md`
   PURE APPEND: `git show --numstat <C3> -- .agent/live_review.md` must read
   `51 0`. A nonzero delete column means a rewrite: STOP and hand back.
   Commit: chore(f111): record the R2 gate and findings R-0298 R-0299 -> push

4. C4 — fix R-0299 in packages/orchestration/diff_repair.py:
   (a) Distinguish the two causes that today both report `no_ranges`:
       - a path whose range list is empty, OR whose entries are all empty
         sequences, keeps the reason `no_ranges`;
       - a path that HAD at least one non-empty range but whose spans all
         clamped away (every span had start > end, i.e. the range lies
         outside the file) gets the NEW reason `out_of_bounds`.
   (b) Update the module docstring's list of omission reasons to name all
       five: `missing`, `binary`, `no_ranges`, `out_of_bounds`, `budget`.
   (c) Keep the one-line WHY comment convention above every definition.
   Do NOT change any other behaviour: margins, merging, ordering, binary and
   missing detection, and the budget rule stay exactly as they are.
   Add tests to tests/orchestration/test_diff_repair.py:
       - a path whose only range starts past EOF -> omitted `out_of_bounds`,
         and the selection carries no hunk for it;
       - a path whose range list is `[[]]` (one empty entry) -> still
         `no_ranges`;
       - the existing empty-list case still reports `no_ranges` (keep the
         current test; do not weaken it).
   Gate: `python3 -m pytest tests/orchestration/test_diff_repair.py -q`
   exit 0; report tests collected and passed (it was 18 before this round).
   Commit: feat(f111): report out of bounds ranges distinctly   -> push

5. C5 — append ONE line to .agent/live_review.md, authored by YOU, in the
   protocol's worker form (docs/agents/planner_reviewer_prompt.md §4.4):
     Landed: R-0299 — <one line: what changed, and the commit named by its
     SUBJECT, never by its SHA — a commit cannot contain its own SHA
     (finding R-0274)>
   Do NOT write `Done:`. PURE APPEND again: the numstat delete column must
   be 0. Commit: chore(f111): mark R-0299 landed   -> push

6. C6 — `cp .remedy-wt/f111r3/PLAN .agent/plan.md`; `cmp` silent.
   Commit: chore(f111): rewrite the plan for R3   -> push

7. C7 — rewrite .agent/handoff.md yourself (your own text): <=60 lines,
   feature+round (F111 R3), branch, per-commit SHA table (C1-C7, C7
   self-referential), changed-files table, the real gate results below,
   open findings 24 with next free ID R-0300, an item-status table over
   C1-C7 with each item exactly once, and next expected action: R4 = settle
   where the hunk line ranges come from, then wire them in.
   Commit: chore(f111): rewrite the handoff for R3   -> push

MUTATION RED-PROOF (after C7, inside a disposable worktree ONLY, never the
primary checkout):
  `git worktree add .remedy-wt/r3mut HEAD`
  In that worktree only, change the new `out_of_bounds` reason string back to
  `no_ranges`, then run
  `python3 -m pytest tests/orchestration/test_diff_repair.py -q` there.
  The new out-of-bounds test MUST go RED. Record the real exit code and the
  failing test id, then `git worktree remove --force .remedy-wt/r3mut` and
  `git worktree prune`; report `git worktree list` and confirm the primary
  checkout's `git status --porcelain` is still empty. If it does NOT go red,
  say so plainly — that is a finding about the test, not something to fix
  quietly.

Done when (record command + real exit code + counted value; never the word
"green"):
  a. the two stated digests match; cmp BLOCK vs authored silent; cmp
     authored vs last_block silent; cmp PLAN vs .agent/plan.md silent.
  b. `git show --numstat <C3> -- .agent/live_review.md` -> `51 0`
     `git show --numstat <C5> -- .agent/live_review.md` -> delete column 0
  c. `grep -c '^- R-0' .agent/live_review.md` -> 24
     `grep -c '^Landed:' .agent/live_review.md` -> 1
     `grep -c '^Done:' .agent/live_review.md` -> 0 (exit 1 is the pass)
     `grep -c 'out_of_bounds' packages/orchestration/diff_repair.py` -> at
     least 2 (the reason and the docstring); report the real number
  d. `python3 -m pytest tests/orchestration/test_diff_repair.py -q` -> exit
     0; report collected and passed.
  e. `python3 -m pytest tests/cli/test_golden_path.py -q` -> exit 0 (canary)
  f. `python3 -m pytest tests/orchestration/test_test_runner.py -q -k 'plan_md or context_md'`
     -> exit 0; report how many ran. (The .agent contract readers. Do NOT run
     tests/ui_server/test_dashboard_contract.py — finding R-0221: it shells
     out to a real npm build.)
  g. mutation red-proof as specified, plus `git worktree list` and
     `git status --porcelain` empty.
  h. `git rev-list --left-right --count origin/feature/f111-diff-only-repair...HEAD`
     -> `0 0`; per-commit insertions each < 500.
Handback:    completion report (tables + raw gate results) and
             .agent/handoff.md rewritten as C7. Do not merge, do not open a
             PR, do not touch .agent/candidates.md or .agent/decisions.md.

<<<BEGIN SLICE LRG sha256=8059f5a3fb82a610e17c27f8a58b79e5cc8dbdea25c9f30d2a272b01409bcaa3 lines=51>>>

### R2 — PASS (2026-08-13)
Reviewed by the main session over f71ebc06..5d8d8c56. Every number below the
reviewer produced by re-running the command, not by reading the handback.
`python3 -m pytest tests/orchestration/test_diff_repair.py -q` exit 0, 18
passed. `python3 -m pytest tests/docs/ -q` exit 0, 294 passed. `python3 -m
pytest tests/cli/test_golden_path.py -q` exit 0, 42 passed. The mutation
red-proof was RE-RUN INDEPENDENTLY by the reviewer in its own disposable
worktree: removing the `max(1, ...)` clamp turns exactly two tests red,
`TestMarginClamping::test_start_of_file_clamps_to_line_1` and
`TestMarginClamping::test_margin_wider_than_file_yields_whole_file`, at
2 failed / 16 passed — matching the worker's report. That worktree was
removed and pruned; `git worktree list` shows only the primary checkout and
`git status --porcelain` is empty. Transport: primary cmp proof, no digest
fallback — `.remedy-wt/f111r2/BLOCK` and `.agent/authored/f111-r2-1.md` are
byte-identical at sha256 85e49d42..., `.agent/plan.md` matches its original,
and both appends sit verbatim at their targets' tails. Append purity proved
by numstat: `51 0` for live_review, `17 0` for the feature file. Scope:
exactly the eight ordered paths. `packages/orchestration/diff_repair.py`
imports only `__future__`, `collections.abc`, `dataclasses` and `pathlib`,
holds no `@@` and neither parses nor applies a diff — the reuse constraint
held. Two Low findings registered below; neither blocks the round.

- R-0298 (Low, F111 R2, reviewer-side authoring defect): step 0 of the R2
  block ordered the worker to "verify all four scratch digests", while the
  block's slice table states digests for only three — LRG, FF and PLAN. The
  fourth entry, BLOCK, is defined as "this entire step block, byte for byte"
  and cannot carry its own digest by construction: a file cannot state the
  hash of bytes that include the statement itself. The worker verified 3 of
  3, pinned BLOCK by the C1 `cmp` instead, and DECLARED the gap rather than
  inventing a fourth number — the wanted behaviour, and the reason this cost
  the round nothing. Same unmeetable-by-construction class as R-0282 and
  R-0285. Forward-looking fix, applied from R3 on: the slice table names how
  many digests it STATES, then BLOCK separately as pinned by the C1 cmp, and
  step 0 counts only the stated ones — the count is whatever that round has,
  never a number carried over from another round. OPEN.
- R-0299 (Low, F111 R2, spec gap in T001): `select_repair_hunks` reports the
  reason `no_ranges` for two different situations. One is a path whose range
  list is genuinely empty (`diff_repair.py:120-122`). The other is a path
  whose ranges ALL clamp away because they point outside the file:
  `_expand_and_merge_ranges` drops every span at `diff_repair.py:85-86` when
  `start > end`, and the caller then reports `no_ranges` at `:129`. The
  second case is a different and load-bearing signal — line numbers past EOF
  mean the ranges came from a diff that no longer matches the file on disk,
  which is exactly the staleness a repair round must not swallow silently.
  This feature's omissions record exists to name what was left out AND why,
  so two causes sharing one reason buys a wrong answer in a later debugging
  session. NOT a worker defect: the eight clauses the R2 block specified did
  not cover the out-of-bounds case, and the worker chose the conservative
  reading and declared it in the handback. Fix ordered in R3: a distinct
  `out_of_bounds` reason with its own test. OPEN.
<<<END SLICE LRG>>>

<<<BEGIN SLICE PLAN sha256=b28dd64bec6843352addde171f729f028ec48b552c33ed0c5c658c213ec3e78c lines=40>>>
# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e.
Next free finding ID: R-0300. Last reviewed SHA: 5d8d8c56 (R2 PASS).

## Goal
Repairs stop resending whole files: a repair round carries only the
failure-relevant hunks with a configurable context margin, the model answers
with a schema-enforced unified diff that is fence-checked and applied
strictly, and ANY hunk conflict discards the attempt whole and falls back to
today's full-file round with the reason recorded
(docs/roadmap/features/T2_F111.md).

## Current Step
R3 — persist the R2 gate and findings R-0298 and R-0299, then fix R-0299 by
giving the omissions record a distinct `out_of_bounds` reason. T001's helper
`select_repair_hunks` exists and is tested but has NO call site yet; wiring
is the next round's work, deliberately separated so a green gate is never
mistaken for a working feature.

## Next Steps
1. R4 — wire the selected hunks into the repair payload. OPEN QUESTION the
   next session must settle FIRST, by reading code and not by assuming:
   `repair_context.build_repair_context(job_id, test_run_event, events)`
   carries `affected_files` (paths only), takes no repo_root and has no line
   ranges, so the hunk ranges must come from somewhere else — most likely
   `review_scope._parse_diff` over the diff of the `source_patch_applied`
   event. Confirm the event actually carries a diff before designing.
2. T002 — versioned unified-diff response schema, fence pre-check before any
   apply, strict apply with an all-or-nothing conflict fallback, on the
   `builder_bridge` seam DECISION F111 D1 selected.
3. T003 — mode and token evidence per repair round, plus a fixture
   comparison recording both modes' token counts.
4. Integration gate, then closure.

## Risks
- The full suite is RED at the merge base with five known ids (R-0286), so
  the integration gate compares base against branch, never absolute green.
- `review_scope._parse_diff` and `source_apply._apply_hunks` already exist
  and must be reused, never duplicated.
<<<END SLICE PLAN>>>
