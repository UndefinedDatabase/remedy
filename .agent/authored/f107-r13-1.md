── STEP integration gate / F107 R13 — full suite, branch and base ──
Goal:        The integration gate runs for the first and only pre-closure time:
             the full suite on this branch and at the merge base 2e4142c3, every
             branch-only failure attributed by direct evidence, the whole run
             committed as evidence under `.agent/gate_f107_r13/`. The R12 PASS
             verdict, the resolution of R-0283 and the new finding R-0285 reach
             `.agent/live_review.md` FIRST, so nothing is lost if this session
             dies mid-suite.
Bundle:      C1 save this block · C2 mirror it · C3 apply the four authored
             live_review pairs · C4 the gate runs + their evidence dir · C5 plan
             · C6 handoff.
Change:      exactly these SIX paths, nothing else:
             .agent/authored/f107-r13-1.md (new, C1)
             .agent/last_block.md (C2)
             .agent/live_review.md (C3, the four pairs below ONLY)
             .agent/gate_f107_r13/** (new dir, C4)
             .agent/plan.md (C5, full replacement by slice PLAN13)
             .agent/handoff.md (C6)

Constraints:
 - AGENTS.md is the highest authority. Self-review loop before every commit, one
   logical step per commit, push after the last one, clean tree at handback.
   Never work on main, never force-push, never amend, rebase, revert or delete a
   branch other than the throwaway `tmp/base-gate` this block creates.
 - NO PRODUCTION CODE, NO TEST CODE MOVES THIS ROUND. `packages/`, `apps/` and
   `tests/` are frozen: `git diff --stat d7dd12b6..HEAD -- packages apps tests`
   must be EMPTY at handback. This round measures; it does not repair.
 - A red integration gate is NOT repaired here. If a branch-only failure is
   reproducible and coupled to F107 code, STOP after C4, record it, and hand
   back — the fix is its own reviewer-gated round (integration_gate.md step 4).
 - Do NOT create a PR, do NOT run the closure evidence job or the review zip,
   do NOT edit docs/roadmap/STATUS.md. Closure is the next round.
 - Do NOT write a `Done:` or `Landed:` line of your own anywhere.
 - Verify every claim against the file before you write it. If anything below
   names a symbol, line, path or count that does not exist, STOP that item, do
   the safe thing, and DECLARE the correction in the handback. A declared
   deviation costs nothing; an undeclared one costs the round.

Detail for C4 — the gate, per docs/agents/integration_gate.md. Read that file
first; it governs, and what follows only pins this feature's specifics.
 - Run logs are written OUTSIDE the repo worktree while a suite runs and copied
   into `.agent/gate_f107_r13/` only after the run exits (R-0176: a log growing
   inside the repo changes the worktree digest mid-run and reddens the
   manifest-identity ids as false positives). Use `$HOME/.cache/remedy-gate/
   f107-r13/` as the scratch dir. If writing there is refused, fall back to the
   gitignored `.remedy-wt/gate-scratch/` and DECLARE the fallback.
 - Evidence file names end in `.txt`, never `.log` (R-0169: `.gitignore` drops
   `*.log` and the review-zip guard rejects any `\.log$` member).
 1. BRANCH RUN, from the repo root with a clean tree at the C3 head:
    `python3 -m pytest -n auto -q`. Record in `branch_run.txt`: cwd, HEAD sha,
    branch, the exact command, start/end UTC, the raw TAIL (last ~25 lines),
    `PYTEST_EXIT_CODE` and wall_clock_seconds. Then
    `grep '^FAILED' <log> | sort > .agent/gate_f107_r13/branch_failed.txt`
    (an empty file if there are none — create it either way).
 2. BASE RUN. `git worktree add -b tmp/base-gate .remedy-wt/base-gate 2e4142c3`
    — on a THROWAWAY BRANCH, never detached: the self-dogfood branch guard
    refuses a detached HEAD by design (DECISION D3). Restore UI parity BY COPY,
    never by symlink (the auto-build writes THROUGH a symlink into the primary
    checkout): `cp -a apps/ui/node_modules` and `cp -a apps/ui/dist` into the
    base worktree. Set `REMEDY_UI_NO_AUTO_BUILD=1` for the base run but do NOT
    trust it alone. VERIFY the neutralization: record in `dist_hashes.txt` the
    aggregate CONTENT hash of `apps/ui/dist` BEFORE and AFTER the base run, for
    BOTH the base worktree and the primary checkout, by
    `find apps/ui/dist -type f -print0 | sort -z | xargs -0 sha256sum |
    sha256sum`. A changed PRIMARY hash means something wrote through — stop and
    report it. A changed BASE hash voids the parity claim and forces per-id
    attribution instead. Same command as step 1; record `base_run.txt` and
    `base_failed.txt` the same way.
 3. COMPARE, into `comm_branch_only_failures.txt` (`comm -13 base_failed.txt
    branch_failed.txt`) and `comm_base_only_failures.txt` (`comm -23`). Both
    files are created even when empty.
 4. ATTRIBUTE, into `attribution.txt`, following the shape of the accepted
    `.agent/gate_f105_r49/attribution.txt` (read it — it is the precedent, not a
    template to copy blindly). It carries: the headline numbers for both runs
    with real exit codes and wall clock; the collected-test delta between branch
    and base with its cause; the two `comm` counts; and a PER-ID verdict table
    in which EVERY id from BOTH comm files appears exactly once, none silently
    absent. For every BRANCH-ONLY id: serial re-run of the exact node id —
    serial-pass means the xdist-flake class (record, not a blocker); serial-fail
    means reproduce it at the merge base before blaming F107. For every
    BASE-ONLY id: name the missing artifact or the mechanism per id by direct
    evidence, or it counts as a genuine base failure and blocks the verdict.
    End the file with the line `VERDICT IS NOT ISSUED HERE` and the reason
    (integration_gate.md step 5: only the reviewer issues the gate verdict).
 5. CLEAN UP, into `worktree_cleanup.txt`: `git worktree remove --force
    .remedy-wt/base-gate`, `git worktree prune`, `git branch -D tmp/base-gate`,
    then `git worktree list` and `git branch --list 'tmp/*'` as proof, with the
    real exit codes. The primary checkout satisfies `git status --porcelain`
    empty afterwards.
 6. Keep each evidence file small: TAILS and lists, never a full 16k-test log.
    If any single evidence file would exceed 400 lines, trim it to the head and
    tail with an explicit `[... N lines elided ...]` marker.

Detail for C5 and C6:
 - Replace `.agent/plan.md` entirely with slice PLAN13; `cmp` and `sha256sum`
   against the marker.
 - Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It must
   carry: feature and round, branch, the per-commit changed-files table for
   C1-C6, the verification table below with REAL exit codes and counted values,
   BOTH gate headline numbers, the branch-only and base-only counts, the open
   findings count and IDs, and the next expected action (closure per
   docs/roadmap/STATUS_closure_protocol.md). Keep it under 100 lines; if the
   mandated content genuinely does not fit, exceed the cap and carry the
   DECISION D15 "Deviations, declared" line naming the real line count and the
   specific mandated content that caused it. Never drop a section to fit.

<<<BEGIN SLICE HDR4FROM sha256=293430f9f6eda011d5a107e9dc689a9c59bd4de652c38a9588dffedc345ad444 lines=1>>>
> Branch: feature/f107-context-compiler-v2. Next free ID: R-0285.
<<<END SLICE HDR4FROM>>>
<<<BEGIN SLICE HDR4TO sha256=7e5c39d424ecde0c939bc254410e6ce2a3e7381f8df9c5313ac0319b928ee8c5 lines=1>>>
> Branch: feature/f107-context-compiler-v2. Next free ID: R-0286.
<<<END SLICE HDR4TO>>>
<<<BEGIN SLICE LRF9FROM sha256=d4f14311bc105b46cd8d63a4d1028643cfbceb8a0e28a30c0d863e9c023f6615 lines=1>>>
  block's own constraint tells workers to expect. OPEN.
<<<END SLICE LRF9FROM>>>
<<<BEGIN SLICE LRF9TO sha256=f9fbc76db0379359d58ea731e672fc4517f96b643bcd2c46f7eecb01e10f9604 lines=11>>>
  block's own constraint tells workers to expect. OPEN.
- R-0285 (Low, F107 R12): the R12 block's gate c ordered `grep -c '^Landed:'` ->
  0 over `.agent/live_review.md` in the one round whose C4 LANDED a fix for
  R-0283, and its Change line confined that file to the four authored pairs.
  docs/agents/planner_reviewer_prompt.md §4.4 tells a worker to mark exactly
  that case `Landed: R-XXXX` in this file, so the block's own zero-gate made the
  protocol's marker unwritable. The worker obeyed the gate, put the landed note
  in the handoff header instead, and declared the conflict as its deviation 4 —
  the right call, and the fifth reviewer-block defect this feature has taxed a
  worker with (R-0274, R-0277, R-0280, R-0282). The rule the next block follows:
  a zero-gate over `^Landed:` is safe only in a round that lands no fix. OPEN.
<<<END SLICE LRF9TO>>>
<<<BEGIN SLICE LR12FROM sha256=3d16eef41d6b61b3c0822acb5c9f086bc294fca82be5bc1b521880c1747311d3 lines=1>>>
  `LAST_REVIEWED_SHA` advances c50080e0 -> 04154822.
<<<END SLICE LR12FROM>>>
<<<BEGIN SLICE LR12TO sha256=3151e03906add1042ef8db1ba087aea57fe5b8877621ff50c7c607a04fe88b5d lines=36>>>
  `LAST_REVIEWED_SHA` advances c50080e0 -> 04154822.

- Reviewer gate on R12 (2026-08-12): PASS, and the round's decisive claim was
  reproduced in BOTH directions rather than read. Range 04154822..d7dd12b6 = six
  commits over exactly the six paths the R12 block enumerated, `git diff
  --name-only` returning that set and nothing else. Transport by the PRIMARY
  shape: `cmp .agent/authored/f107-r12-1.md .agent/last_block.md` exits 0 and
  silent under this reviewer's own run, both files sha256 to
  edc2563b00979927cd17d8837a3887d1b17620ea0fcf5844cbb20b9f92bbac54 at 242 lines
  — the value the R12 block's BLOCK_SHA256 trailer declares — and
  `.agent/plan.md` hashes to a949117f430008cc… as slice PLAN12 specified.
  `git show --numstat e7c700fc -- .agent/live_review.md` reads `65  1`: one
  deletion, HDR3 the only REWRITE. The anchored counts hold on disk now —
  `^Done:` 8, `^Landed:` 0, `^## Steps` 1, and `^<<<` 0 in live_review.md,
  plan.md and handoff.md alike.
  THE PROBE WAS RE-RUN BY THIS REVIEWER, twice, inside the disposable worktree
  `.remedy-wt/r13probe` and nowhere else, with the same one-line mutation
  `use_compiled_context = False` at pingpong_loop.py:2662 (`git diff --numstat`
  `1  1` each time). At 04154822 the e2e module returns 3 failed, 3 passed and
  `test_compiled_run_shrinks_the_context_and_still_solves_the_task` is among the
  THREE THAT STILL PASS — R-0283 reproduced independently, not quoted. At
  d7dd12b6 the same mutation returns 4 failed, 2 passed and that same test is
  now among the failures, on the new pin, verbatim `assert
  compiled.context_chars == len(expected_compiled_text)` -> `E assert 265 ==
  899`. 265 is the fall-through pack, 899 the compiler's own rendered bytes: the
  test that stands for F107's DONE condition finally bites the wiring it names.
  The worktree was removed and pruned; `git worktree list` is the primary
  checkout alone and `git status --porcelain` is empty. Every other gate re-run
  green by this reviewer: 6 passed on the e2e module, 43 on `test_pingpong.py`
  plus `test_pingpong_integration.py` — the same 43 R11 measured, so the loop
  every job runs through did not move — 42 on the canary, `ruff check` "All
  checks passed!", `git diff --stat 04154822..HEAD -- packages apps` EMPTY, and
  each commit's insertion column under 500 (242, 177, 65, 12, 8, 112). All six
  declared deviations re-measured accurate; deviation 4 becomes R-0285 because
  the conflict it declared was the block's, not the worker's.
  `LAST_REVIEWED_SHA` advances 04154822 -> d7dd12b6.
<<<END SLICE LR12TO>>>
<<<BEGIN SLICE LRD5FROM sha256=04f58aa97661534430c6bf142337ebd148a6fc083f7b7338154b6e3f8edafb0e lines=2>>>
claim class now has no live instance in this feature's files. Open findings
15 -> 14.
<<<END SLICE LRD5FROM>>>
<<<BEGIN SLICE LRD5TO sha256=858484d44f4f018b1e17b5fa6ec486658123dea86e9eb5818f161eaf051e3e23 lines=12>>>
claim class now has no live instance in this feature's files. Open findings
15 -> 14.

Done: R-0283 — RESOLVED. The end-to-end test that stands for F107's DONE
condition no longer passes with the compiled path disabled. Commit 0df94864
(numstat `12  0`, one test file, no production byte moved) pins the compiled
run's `context_chars` to `len(render_compiled_context_text(...))` over the same
fixture, and this reviewer's own mutation probe — `use_compiled_context = False`
in a disposable worktree — turns the module from `3 failed, 3 passed` at
04154822, where the test PASSED, to `4 failed, 2 passed` at d7dd12b6, where it
fails on `assert 265 == 899`. A bypass can no longer satisfy the feature's Done
sentence. Open findings 14 -> 13.
<<<END SLICE LRD5TO>>>
<<<BEGIN SLICE PLAN13 sha256=4434ae2d39625ad4a555b7c4adc9f759123563c5c41906e78f928db8971d0e63 lines=27>>>
# Plan — F107 Context compiler v2

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0286. R12 reviewed PASS at d7dd12b6.

## Goal
The context compiler selects fenced-path files, their direct import
neighbors, and only SIGNATURES of distant dependencies, under a total
context token budget with tier demotion — and writes an omissions record
naming everything it left out and why. DONE when a fixture repo's task
context shrinks measurably versus whole-files with the fixture task still
solvable by the fake provider, and the omissions record explains every
exclusion (docs/roadmap/features/T2_F107.md).

## Current Step
R13 — the integration gate per docs/agents/integration_gate.md: the full
suite on the branch and at the merge base 2e4142c3, every branch-only
failure attributed by direct evidence, the evidence committed under
`.agent/gate_f107_r13/`. The R12 PASS verdict, its finding R-0285 and the
resolution of R-0283 land in the same round. T001-T004 are complete and
reviewed; no production code moves here.

## Next Steps
1. Closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, a FRESH
   review zip, the reviewer-authored STATUS line, then the PR.
2. The closure PR is never merged in the session that creates it; it merges at
   the next feature's start via the AGENTS.md Open PR Gate.
<<<END SLICE PLAN13>>>

PROCEDURE — in this order, one commit per numbered step:
 1. Save this ENTIRE block, byte for byte, from the `── STEP` line to the last
    line of this procedure, to `.agent/authored/f107-r13-1.md`. The expected
    digest is the BLOCK_SHA256 line the reviewer original
    `.remedy-wt/f107-r13-1.block.md` carries as its LAST line; that trailer sits
    one line PAST the region you save and is not part of the saved bytes. Verify
    BEFORE anything else; on mismatch STOP and report, never repair bytes.
    Commit C1.
 2. Copy that file over `.agent/last_block.md`; `cmp` the two, exit 0 and
    silent. Commit C2.
 3. Apply the four pairs to `.agent/live_review.md` by exact-string replacement
    of the FROM body with the TO body, verifying each slice's sha256 BEFORE use
    and checking that each FROM occurs exactly 1x before you replace it. HDR4 is
    a REWRITE (FROM and TO are disjoint); LRF9, LR12 and LRD5 are APPENDS (each
    TO literally CONTAINS its FROM). Commit C3 alone. Do not touch this file
    again for the rest of the round.
 4. Run the gate exactly as Detail-C4 prescribes, then commit the evidence dir
    as C4. The branch run happens at the C3 head with a clean tree.
 5. Replace `.agent/plan.md` entirely with slice PLAN13. Commit C5.
 6. Run every gate in Done-when, record the REAL exit code and counted value of
    each, then rewrite `.agent/handoff.md` and commit C6. Push the branch.

Done when — run each, record exit code AND counted value:
 a. `cmp .agent/authored/f107-r13-1.md .agent/last_block.md` -> exit 0, silent;
    `sha256sum` of both == the BLOCK_SHA256 trailer named in step 1.
 b. Each of the nine slice bodies recomputes to its BEGIN-marker digest at its
    declared line count.
 c. `git show --numstat <C3> -- .agent/live_review.md` -> the deletion column is
    exactly 1, HDR4 being the only REWRITE. Then, LINE-ANCHORED:
    `grep -c '^> Branch:.*Next free ID: R-0286'` -> 1;
    `grep -c '^> Branch:.*Next free ID: R-0285'` -> 0; `grep -c '^- R-0285'` ->
    1; `grep -c '^Done:'` -> 9; `grep -c '^Landed:'` -> 0;
    `grep -c '^## Steps'` -> 1; `grep -c '^<<<'` -> 0 (also 0 in
    `.agent/plan.md` and `.agent/handoff.md`).
 d. THE GATE ITSELF. Report, as raw values, for BOTH runs: the exact command,
    the passed/skipped/failed counts, the pytest exit code and the wall clock.
    Report the two comm counts. Report, per branch-only id, its serial re-run
    result. The gate is GREEN for the reviewer only if every branch-only id is
    either absent or attributed to the xdist-flake class by a serial pass, and
    every base-only id is attributed to the environment class by named direct
    evidence.
 e. `sha256sum .agent/plan.md` == the PLAN13 marker digest; `cmp` against the
    extracted slice -> exit 0, silent; the file is 27 lines.
 f. Canary, in the primary checkout after the worktree is gone:
    `python3 -m pytest tests/cli/test_golden_path.py -q` -> exit 0, 42 passed.
 g. `git diff --stat d7dd12b6..HEAD -- packages apps tests` -> EMPTY output.
 h. `git status --porcelain` -> empty; `git worktree list` -> the primary
    checkout ALONE; `git branch --list 'tmp/*'` -> empty; HEAD ==
    origin/feature/f107-context-compiler-v2 after the push; insertions per
    commit, each < 500.
 i. `git diff --name-only d7dd12b6..HEAD` -> exactly the paths of the Change
    list and nothing else (the sixth, `.agent/handoff.md`, arrives with C6, so
    a measurement taken before C6 legitimately shows five plus the gate dir —
    say which you measured).
 j. `remedy integrity check --json` -> record the verdict verbatim. This is a
    closure precondition (STATUS_closure_protocol.md precondition 3) and the
    next round needs the value; a non-PASS is reported, not repaired here.

Handback: completion report + rewrite `.agent/handoff.md` per
docs/agents/handback_template.md, with the changed-files table, the item-status
table covering C1-C6, and every gate above with its real exit code and counted
value. Declare any deviation.
──────────────────────────────────────────────────────────────
