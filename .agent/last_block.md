── STEP repair + close / F107 R12 — pin the DONE test, close the session ──
Goal:        The end-to-end test that stands for F107's DONE condition is
             pinned to the compiler's own output so disabling the compiled path
             can no longer satisfy it (finding R-0283), the R11 verdict and its
             three findings reach disk, and the handoff closes this session.
Bundle:      C1 save this block · C2 mirror it · C3 apply the four authored
             live_review pairs · C4 the R-0283 test fix · C5 plan · C6 handoff.
Change:      exactly these SIX paths, nothing else:
             .agent/authored/f107-r12-1.md (new, C1)
             .agent/last_block.md (C2)
             .agent/live_review.md (C3, the four pairs below ONLY)
             tests/orchestration/test_context_compiler_e2e.py (C4)
             .agent/plan.md (C5, full replacement by slice PLAN12)
             .agent/handoff.md (C6)

Constraints:
 - AGENTS.md is the highest authority. Self-review loop before every commit, one
   logical step per commit, push after the last one, clean tree at handback.
   Never work on main, never force-push, never amend, rebase or revert.
 - NO PRODUCTION CODE MOVES THIS ROUND. `packages/` and `apps/` are frozen:
   `packages/orchestration/pingpong_loop.py` and
   `packages/orchestration/context_compiler.py` must be byte-identical at the
   end of this round to what they are at its start. C4 touches ONE test file.
 - Do NOT run the integration gate and do NOT create a PR. Both belong to the
   next session, and the handoff says so.
 - Verify every claim against the file before you write it. If anything below
   names a symbol, line or field that does not exist, STOP that item, do the
   safe thing, and DECLARE the correction in the handback.

Detail for C4 — the R-0283 fix, in
tests/orchestration/test_context_compiler_e2e.py:
 The failing property is that
 `test_compiled_run_shrinks_the_context_and_still_solves_the_task` (at
 test_context_compiler_e2e.py:152) keeps passing when the compiled path is
 bypassed entirely, because a fall-through run without `mentioned_files` also
 produces a smaller context. Add to THAT test — keeping every assertion already
 in it — a pin that no fall-through can satisfy:
   - compile the same fixture with `compile_task_context` and render it with
     `render_compiled_context_text`, using the same fenced paths and candidate
     list the test already passes to the run, and
   - assert the compiled run's `context_chars` EQUALS `len(<that rendered
     text>)` as a real number, not a bound.
 That ties the number the run reports to the bytes the compiler produced, so
 disabling the wiring changes the value and reddens the test. Import the two
 functions the way this module already imports from the compiler. Change no
 other test in the file and change no production code.

Detail for C5 and C6:
 - Replace `.agent/plan.md` entirely with slice PLAN12.
 - Rewrite `.agent/handoff.md` as the SESSION-CLOSING handoff. It must state:
   the rounds this session closed (R9, R10 and R11, all three reviewed PASS by
   the in-session reviewer, plus this R12), `LAST_REVIEWED_SHA` standing at
   04154822 with R12 itself awaiting review by construction
   (docs/agents/planner_reviewer_prompt.md §4.13 — the last round of a session
   has no on-disk gate entry and that absence is the TERMINATOR, not a missing
   gate), the open-findings count and their IDs, that no PR exists and none was
   created, that main is untouched, and that the next expected action is the
   integration gate per docs/agents/integration_gate.md followed by closure.

<<<BEGIN SLICE HDR3FROM sha256=f538e69d732216c02a2cbbe84f580095a5bb066fb2b1812babc020f96f1384f0 lines=1>>>
> Branch: feature/f107-context-compiler-v2. Next free ID: R-0282.
<<<END SLICE HDR3FROM>>>
<<<BEGIN SLICE HDR3TO sha256=293430f9f6eda011d5a107e9dc689a9c59bd4de652c38a9588dffedc345ad444 lines=1>>>
> Branch: feature/f107-context-compiler-v2. Next free ID: R-0285.
<<<END SLICE HDR3TO>>>
<<<BEGIN SLICE LRF8FROM sha256=76c285627b795cf5a3df39f545e314f749823c92867bde2a931999298131e924 lines=1>>>
  is worth one line: the next reader trusts it. Fixed in this round's C6. OPEN.
<<<END SLICE LRF8FROM>>>
<<<BEGIN SLICE LRF8TO sha256=a915e97199d94f9ca09930b53b2757b78efcdcf10d2f387557c194341db7016b lines=27>>>
  is worth one line: the next reader trusts it. Fixed in this round's C6. OPEN.
- R-0282 (Low, F107 R11): the R11 block's Change line said "exactly these nine
  paths" and gate l repeated "nine", while the list under it enumerates EIGHT.
  The worker measured 8, touched nothing outside the list, and declared the
  discrepancy. Reviewer arithmetic, costing a deviation on a round that did
  nothing wrong — the same tax R-0274, R-0277 and R-0280 record. OPEN.
- R-0283 (Medium, F107 R11): `test_compiled_run_shrinks_the_context_and_still`
  `_solves_the_task` — the test that stands for the FEATURE'S DONE CONDITION —
  passes with the entire compiled path disabled. The reviewer measured it rather
  than reading the disclosure: setting `use_compiled_context = False` in a
  disposable worktree at 04154822 turns the e2e module to `3 failed, 3 passed`
  and that test is among the THREE THAT STILL PASS. The cause is that the
  baseline run passes `mentioned_files` while the fall-through compiled run
  passes none, so its context is smaller for a reason that has nothing to do
  with F107. A shrink assertion that a bypass satisfies pins nothing. The worker
  found this itself, reported it, and deliberately did NOT repair it after
  measuring, which would have made its own probe self-fulfilling — that is
  exactly right, and it is why this is a finding against the round's test
  strength and not against its honesty. Fixed in R12 C4 by pinning the compiled
  run's `context_chars` to the length of `render_compiled_context_text` over the
  same fixture, which no fall-through can satisfy. OPEN.
- R-0284 (Low, F107 R11): two line citations in the R11 block were wrong —
  `build_scope_contract_for_builder` sits at pingpong_loop.py:2741, not :2694,
  and the stale "one writing function" string sat at
  test_context_compiler.py:805, not :801. Both were declared, neither cost
  anything but the declaring, and both are the reviewer-citation class the
  block's own constraint tells workers to expect. OPEN.
<<<END SLICE LRF8TO>>>
<<<BEGIN SLICE LR11FROM sha256=a0092d07a90fe1fce25c7b51fb4bc412c73de8eda9348efe42b8ef692eaf1fca lines=1>>>
  `LAST_REVIEWED_SHA` advances f86bda87 -> c50080e0.
<<<END SLICE LR11FROM>>>
<<<BEGIN SLICE LR11TO sha256=7350212ff4331a36801bec89967102c8eaa34a2048e53001bf79e30805af91e5 lines=32>>>
  `LAST_REVIEWED_SHA` advances f86bda87 -> c50080e0.

- Reviewer gate on R11 (2026-08-12): PASS — and this is the round that makes
  F107's DONE condition real. Range c50080e0..04154822 = eight commits touching
  the EIGHT paths the R11 block enumerated (its prose said nine; that is
  R-0282). Transport by the PRIMARY shape: the reviewer original
  `.remedy-wt/f107-r11-1.block.md` survives, its body is byte-identical to
  `.agent/authored/f107-r11-1.md` and `.agent/last_block.md`, all three sha256
  to 121401148a1ec2f1… at 314 lines, and all nine slice bodies recompute to
  their BEGIN-marker digests. `git show --numstat 815e4294 --
  .agent/live_review.md` reads `78  1` — one deletion, HDR2 being the only
  REWRITE — and the anchored greps return exactly their specified values
  (R-0282 header 1, R-0280 header 0, `^- R-0280` 1, `^- R-0281` 1, `^Done:` 7,
  `^Landed:` 0). Every gate was RE-RUN by this reviewer: 6 passed on the new
  end-to-end module, 61 on the compiler suite, 42 on the canary, `ruff check`
  "All checks passed!", and THE REGRESSION GATE HELD — `test_pingpong.py` plus
  `test_pingpong_integration.py` return 43 passed, the same 43 measured before
  C4 touched the loop every job runs through. The C4 diff was read line by line:
  three keyword-only parameters that default to today's behaviour, one
  all-or-nothing branch, a local import inside that branch, records written only
  where the caller points, and `build_repo_context` reached unchanged in every
  other case — the default path does not move. GATE j WAS RE-RUN, not read: the
  fixture repo runs twice through `run_pingpong` with `FakeProvider`, and BOTH
  runs reach `staged_review_passed` while `context_chars` falls 4613 -> 899 and
  the size record reads whole_file_tokens 1067, compiled_tokens 195,
  saved_tokens 872, saved_ratio 0.817244611059044, with `src/invoice_report.py`
  omitted for `distance`. A fixture task is solved by the fake provider on a
  context 81.7% smaller, and the omissions record explains the exclusion: that
  is the feature file's Done sentence, measured. All ten declared deviations
  re-measured accurate; the substantive one is registered as R-0283 after the
  reviewer reproduced it independently, and the two citation errors are R-0284.
  `LAST_REVIEWED_SHA` advances c50080e0 -> 04154822.
<<<END SLICE LR11TO>>>
<<<BEGIN SLICE LRD4FROM sha256=55be908927376fe34b1bb62554ba38db2fadd9cdbdc5afc9829a4e09567ffc14 lines=1>>>
that made the ordering matter. Open findings 13 -> 12.
<<<END SLICE LRD4FROM>>>
<<<BEGIN SLICE LRD4TO sha256=d1bbafad03b72039a82ace9c68beabe85877e239c9de8377542eb2ed84692f39 lines=8>>>
that made the ordering matter. Open findings 13 -> 12.

Done: R-0281 — RESOLVED. `tests/orchestration/test_context_compiler.py` no
longer calls `write_omitted_context_json` "the one writing function" (commit
b4e9d423, numstat `1 1` — one line changed and nothing else in the file), and
the reviewer's own re-run of that module returns 61 passed. The stale-absolute
claim class now has no live instance in this feature's files. Open findings
15 -> 14.
<<<END SLICE LRD4TO>>>
<<<BEGIN SLICE PLAN12 sha256=a949117f430008cca4e2dd7dfcbbf9e43b576314f2f09947c4b228f89c5b095b lines=27>>>
# Plan — F107 Context compiler v2

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0285. R11 reviewed PASS at 04154822.

## Goal
The context compiler selects fenced-path files, their direct import
neighbors, and only SIGNATURES of distant dependencies, under a total
context token budget with tier demotion — and writes an omissions record
naming everything it left out and why. DONE when a fixture repo's task
context shrinks measurably versus whole-files with the fixture task still
solvable by the fake provider, and the omissions record explains every
exclusion (docs/roadmap/features/T2_F107.md).

## Current Step
R12 — repair and session close: the DONE-condition end-to-end test is pinned to
the compiler's own output so a bypass can no longer satisfy it (finding
R-0283), the R11 verdict and three findings are persisted, and the handoff
closes the session. T004 is complete: the CLI view, the records and the
end-to-end run all exist and were re-measured by the reviewer.

## Next Steps
1. Integration gate per docs/agents/integration_gate.md — the full suite, the
   first of the two runs a feature gets.
2. Closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, a FRESH
   review zip, the authored STATUS line, then the PR. The branch has no PR yet
   and it is never merged in the session that creates it.
<<<END SLICE PLAN12>>>

PROCEDURE — in this order, one commit per numbered step:
 1. Save this ENTIRE block, byte for byte, from the `── STEP` line to the last
    line of this procedure, to `.agent/authored/f107-r12-1.md`. The expected
    digest is the BLOCK_SHA256 line that the reviewer original
    `.remedy-wt/f107-r12-1.block.md` carries as its LAST line; that trailer sits
    one line PAST the region you save and is not part of the saved bytes. Verify
    BEFORE anything else; on mismatch STOP and report, never repair bytes.
    Commit C1.
 2. Copy that file over `.agent/last_block.md`; `cmp` the two, exit 0 and
    silent. Commit C2.
 3. Apply the four pairs to `.agent/live_review.md` by exact-string replacement
    of the FROM body with the TO body, verifying each slice's sha256 BEFORE use.
    HDR3 is a REWRITE (FROM and TO are disjoint); LRF8, LR11 and LRD4 are
    APPENDS (each TO literally contains its FROM). Commit C3 alone.
 4. C4, its own commit, self-review loop before it.
 5. Replace `.agent/plan.md` entirely with slice PLAN12; `cmp` and `sha256sum`
    against the marker. Commit C5.
 6. Run every gate in Done-when, record the REAL exit code and counted value of
    each, then rewrite `.agent/handoff.md` and commit C6. Push.
 7. Do NOT write a `Done:` line of your own.

Done when — run each, record exit code AND counted value:
 a. `cmp .agent/authored/f107-r12-1.md .agent/last_block.md` → exit 0, silent;
    `sha256sum` of both == the BLOCK_SHA256 trailer named in step 1.
 b. Each of the nine slice bodies recomputes to its BEGIN-marker digest at its
    declared line count.
 c. `git show --numstat <C3> -- .agent/live_review.md` → the deletion column is
    exactly 1, HDR3 being the only REWRITE. Then, LINE-ANCHORED (finding
    R-0278): `grep -c '^> Branch:.*Next free ID: R-0285'` → 1;
    `grep -c '^> Branch:.*Next free ID: R-0282'` → 0; `grep -c '^- R-0282'` → 1;
    `grep -c '^- R-0283'` → 1; `grep -c '^- R-0284'` → 1; `grep -c '^Done:'` →
    8; `grep -c '^Landed:'` → 0; `grep -c '^## Steps'` → 1; `grep -c '^<<<'` → 0
    (also 0 in `.agent/plan.md` and `.agent/handoff.md`).
 d. `python3 -m pytest tests/orchestration/test_context_compiler_e2e.py -q` →
    exit 0, 6 passed.
 e. THE PROBE THAT DECIDES THIS ROUND, inside a disposable `git worktree` at
    HEAD and nowhere else: set `use_compiled_context = False` in
    `packages/orchestration/pingpong_loop.py` — the same mutation that produced
    `3 failed, 3 passed` at 04154822 — re-run the e2e module, and report the
    exact counts and the names of the failing tests. The fix is proven only if
    `test_compiled_run_shrinks_the_context_and_still_solves_the_task` is now
    AMONG THE FAILURES. Remove and prune the worktree, then confirm
    `git status --porcelain` is empty and the mutated file is unchanged in the
    primary checkout.
 f. Regression, because the e2e module exercises the loop:
    `python3 -m pytest tests/orchestration/test_pingpong.py
    tests/orchestration/test_pingpong_integration.py -q` → exit 0, 43 passed.
 g. Canary: `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, 42
    passed.
 h. `python3 -m ruff check tests/orchestration/test_context_compiler_e2e.py` →
    exit 0.
 i. `git diff --stat 04154822..HEAD -- packages apps` → EMPTY output: no
    production file moved this round.
 j. `git status --porcelain` → empty; `git worktree list` → primary checkout
    alone; HEAD == origin/feature/f107-context-compiler-v2; insertions per
    commit, each < 500.
 k. `git diff --name-only 04154822..HEAD` → exactly the six paths of the Change
    list, nothing else.

Handback: completion report + rewrite `.agent/handoff.md` per
docs/agents/handback_template.md, with the changed-files table, the item-status
table covering C1-C6, and every gate above with its real exit code and counted
value. Declare any deviation; a declared deviation costs nothing, an undeclared
one costs the round.
──────────────────────────────────────────────────────────────
