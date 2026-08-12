── STEP R25 (session terminator) — F105 ──────────────────────
Goal:        Put the R24 gate on disk and REGISTER the two findings it
             produced. No fix, no migration — this round persists state and
             ends the session.
Bundle:      C1 save this block · C2 record the R24 gate and register R-0253
             and R-0254 · C3 plan and handoff.
Change:      `.agent/authored/f105-r25-1.md`, `.agent/last_block.md`,
             `.agent/live_review.md`, `.agent/plan.md`, `.agent/handoff.md`.
             Nothing else. NO production file, NO test file is touched.
Constraints: Both findings are registered OPEN and are NOT fixed in this round.
             R-0254 is production code, so it needs a SPLIT round
             (docs/agents/planner_reviewer_prompt.md §3 "Round types") and this
             session has no reviewer left to gate it — leaving it open is the
             correct outcome, not a deferral to hide.
             This is the LAST round of the session. Its own gate is owed to the
             NEXT session's reviewer by construction (§4.13, the TERMINATOR).
             Do not open a repair round to close it.
Done when:   every gate below is run and its real exit code recorded.

C1 — save this block verbatim, TWO commits
  C1a `cp` this block to `.agent/authored/f105-r25-1.md`. Commit it ALONE.
  C1b `cp` the same bytes to `.agent/last_block.md`. Commit separately.
  Both are `cp` of the file on disk — never a retype. `sha256sum` both plus
  `cmp`, and record the digest in the handback.

C2 — the gate record and the two registrations (own commit)
  Apply all four pairs, slicing each from `.agent/authored/f105-r25-1.md` by
  its markers with a script. Marker lines never reach a target file.
  PAIR_A is a REWRITE (FROM and TO are disjoint): prove FROM 0x after, TO 1x.
  PAIR_B and PAIR_C are APPEND-shaped (the TO contains the FROM verbatim as its
  prefix): prove FROM exactly 1x, and count TO-only ADDED LINES IN THE DIFF —
  see R-0253 below, do NOT count whole-file occurrences.

<<<PAIR_A_FROM>>>
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0253.
<<<END_PAIR_A_FROM>>>

<<<PAIR_A_TO>>>
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0255.
<<<END_PAIR_A_TO>>>

<<<PAIR_B_FROM>>>
  the same round as this entry. Fixed and resolved in this same round; the NEXT
  session's gate verifies the rule is on disk and reads as intended.
<<<END_PAIR_B_FROM>>>

<<<PAIR_B_TO>>>
  the same round as this entry. Fixed and resolved in this same round; the NEXT
  session's gate verifies the rule is on disk and reads as intended.
- R-0253 (Low, F105 R24, reviewer-authored defect): §4.9's append-shaped pair
  obligation is written whole-file where it can only hold over the DIFF. The
  rule says "FROM exactly 1x plus each TO-ONLY addition exactly 1x". R24's
  PAIR_A had 34 TO-only lines, of which 33 occur once in the file and one —
  "`git worktree list` the primary alone at this verdict." — occurs twice,
  because the identical sentence already stood in the R22 gate paragraph. The
  gate was therefore unsatisfiable by construction, and the worker correctly
  MEASURED it and declared it rather than editing the text to dodge it. The
  reviewer re-measured and confirms: `git show --numstat` on the C2 commit
  reads exactly `34 0 .agent/live_review.md`, so the diff-scoped reading is
  both exact and achievable. This is the seventh unsatisfiable-gate instance
  across F104 and F105 and the second one DECISION F105 D8's checklist did not
  catch, because like item 5 it is not a property of the block's own bytes —
  it is a property of the TARGET FILE's existing content. Fix: amend §4.9 so
  the TO-only count is over lines ADDED BY THE DIFF, and add the whole-file
  collision to D8 as the check that catches it before emission. Note for
  whoever fixes it: prose that repeats an earlier gate's sentence is normal and
  desirable in this file, so the rule must bend, not the text. OPEN.
- R-0254 (Low, F105 R24): `_drop_one_newline_per_segment_boundary` in
  `packages/orchestration/pingpong_loop.py` raises `PromptSegmentError` with
  the text "builder prompt segment boundary carries no newline to drop between
  segments N and N+1", but since R24 the helper composes the REVIEWER prompt
  too. A reviewer-side boundary fault would report itself as a builder fault
  and send the next reader to the wrong function. The worker spotted this and
  correctly did NOT act: it is outside R24's declared change set and AGENTS.md
  Scope Control bars the "while I'm here" edit. Cost today is zero — the
  message is unreachable in production, which is exactly what R-0251 pinned —
  so this is a message-quality finding, not a correctness one. Fix: drop the
  word "builder", and update the two message assertions in
  `tests/orchestration/test_builder_prompt_golden.py::TestDropOneNewlinePerSegmentBoundary`
  in the same commit. Production code, so it needs a SPLIT round. OPEN.
<<<END_PAIR_B_TO>>>

<<<PAIR_C_FROM>>>
  `LAST_REVIEWED_SHA` advances b35d9d56 -> 554d9521.
<<<END_PAIR_C_FROM>>>

<<<PAIR_C_TO>>>
  `LAST_REVIEWED_SHA` advances b35d9d56 -> 554d9521.
- Reviewer gate on R24 (2026-08-10, same session): PASS. Migration-order step 6
  is landed, so ALL SIX T003 migration sites are done. Range
  `554d9521..HEAD` at df32f595, SIX commits, seven path rows. Insertions per
  `git log --numstat`: 258, 226, 34, 279, 142, 70 — each under 500, and the
  258-line authored save is under DECISION F105 D5's 400.
  Transport: `.agent/authored/f105-r24-1.md` and `.agent/last_block.md` are
  byte-identical under `cmp` at sha256 `eb6e071e399cd967…`, 258 lines.
  THE SPEC WAS PROVED SATISFIABLE BEFORE THE BLOCK WAS AUTHORED, the R-0250
  discipline applied forward for the second time. In a disposable worktree at
  554d9521 the reviewer proved the decomposition byte-exact over 3584 argument
  combinations in two passes: 2048 for the decomposition itself (80 distinct
  segment sets, 0 mismatches) and 1536 for the property the golden actually
  rests on — that registering in RANK order instead of source order leaves
  every segment's BYTES unchanged. It does: 0 per-segment differences, 0
  changes of last-segment identity, 0 boundaries needing the fallback newline.
  Without that second pass the golden's "reassemble in pre-migration order"
  assertion would have been an assumption, since
  `_drop_one_newline_per_segment_boundary` runs over the registration order.
  AFTER the round the reviewer re-proved content equality against the REAL
  pre-migration bytes, not against the worker's numbers:
  `git show 554d9521:packages/orchestration/pingpong_loop.py` was imported as a
  second live module and run side by side with HEAD's composer over 2048
  combinations and 160 distinct segment sets. 0 reassembly failures, 0 wrapper
  mismatches, 0 unknown segment names, 0 non-monotonic manifests. 224 renders
  are byte-identical to the old one and 1824 are genuinely reordered, so the
  reorder this feature exists to make is real and measured, not asserted.
  Gates re-run by THIS reviewer: the new golden 16 passed, the four caller
  suites 234 passed — equal to the worker's pre-round baseline, so the
  migration added no test to them and removed none — and the canary 42 passed.
  TWO mutation red-proofs of the REVIEWER's own choosing, distinct from the
  worker's M1 and M2, ran in a disposable worktree at HEAD. M3 changed
  `reviewer_task_input`'s rank from TASK to STEERING, which leaves every
  segment's TEXT identical and the ranks still non-decreasing: exactly one test
  failed, `test_the_fallback_full_shape_registers_its_segments_in_rank_order`.
  M4 changed `reviewer_scope_contract`'s rank from JOB_CONTEXT to DOSSIER:
  exactly the two shape tests failed. So the golden pins the rank ASSIGNMENT
  and not merely its monotonicity — the property R22's M4b established for the
  builder, now established for the reviewer. Both reverted, the worktree
  removed and pruned, `git status --porcelain` empty and `git worktree list`
  the primary alone at this verdict.
  Application re-measured disk to disk against the COMMITTED authored file,
  never a retype: PAIR_A APPEND with FROM 1x and TO 1x, PAIR_B's slice and
  `.agent/plan.md` byte-equal, plan 39 lines against the cap of 50, and not one
  transport marker of any shape left behind in either target.
  BOTH declared deviations ACCEPTED, and BOTH are charged to the reviewer.
  Deviation 1: gate D asked for failing test NAMES from a red that a
  module-level import makes a COLLECTION error, which yields none; the worker
  re-measured at test-name granularity in a worktree and got all 16. Deviation
  2 is registered as R-0253. Neither is held against R24. A round that measures
  a reviewer's gate and reports the number instead of the claim is the round
  working exactly as designed, for the third feature running.
  `LAST_REVIEWED_SHA` advances 554d9521 -> df32f595.
<<<END_PAIR_C_TO>>>

C3 — plan and handoff (own commit)
  Apply PAIR_D to `.agent/plan.md` as a FULL replacement, then rewrite
  `.agent/handoff.md`.

<<<PAIR_D_PLAN>>>
# Plan — F105 Cache-optimal prompt ordering

Branch: feature/f105-cache-optimal-prompt-ordering, cut from main at cfda4245
after PR #188 merged at the Open PR Gate. One-session self-drive, one delegated
worker per round. The next free finding ID lives in `.agent/live_review.md`
line 8 and is deliberately not duplicated here (R-0240's root cause).

## Goal
Prompt assembly stops being ad hoc. Every prompt composes from REGISTERED
SEGMENTS ordered by stability — system and conventions first, task and steering
last — every call records a segment manifest (name, rank, hash) into evidence,
and `remedy stats cache` shows the cache-read share per role from actuals.
Prompt CONTENT does not change; only its composition.

## Current Step
T001 and T002 are DONE and gated. T003's MIGRATION ORDER
(`.agent/t003_inventory.md`, never that file's catalogue "Site N" headings —
R-0241) is COMPLETE: all six sites are migrated, each under its own golden.
R24 is GATED; `LAST_REVIEWED_SHA` is df32f595. R25 is the session terminator —
it records the R24 gate and registers R-0253 and R-0254, and starts no work.
Open findings: R-0221, R-0239, R-0246, R-0247, R-0253, R-0254.
No PR; one is created at CLOSURE.

## Next Steps
- R26 gates R25 (state only), then fixes R-0254 — production code, so SPLIT —
  and R-0253, whose fix is §4.9 plus a sixth D8 checklist item.
- ONE round wires `on_call` for the three sites lacking call evidence:
  `mission_cmd.py:362` (orchestrator), `mission_cmd.py:187` +
  `gauntlet_runner.py:505` (mission), `do_cmd.py:253` + `:2860` (plan).
- Fix R-0246 in the round that next touches `mission_compiler.py`.
- Then T004, `remedy stats cache` over actuals; then the integration gate
  (docs/agents/integration_gate.md); then closure
  (docs/roadmap/STATUS_closure_protocol.md), where the PR is created.

## Risks
- R-0221 stays open and will cost the integration gate phantom base-only
  failures.
- The reviewer prompt was the worst-ordered of the six sites and 1824 of 2048
  measured renders reorder, so T004's before/after number should quote its
  cacheable-prefix gain specifically.
<<<END_PAIR_D_PLAN>>>

GATES — run every one, record the REAL exit code and the REAL output
  A transport: `sha256sum` on `.agent/authored/f105-r25-1.md` and
    `.agent/last_block.md`; `cmp` them. Digest in the handback.
  B size: `wc -l .agent/authored/f105-r25-1.md`.
  C application: PAIR_A FROM 0x after and TO 1x; PAIR_B and PAIR_C FROM 1x
    each; `cmp` the applied `.agent/plan.md` against the sliced PAIR_D;
    `wc -l .agent/plan.md` (must be under 50); the TO-only ADDED-LINE count
    from `git show --numstat` on the C2 commit, with the stray count.
  D marker leakage: grep `PAIR_A_FROM`, `PAIR_D_PLAN`, `END_PAIR` and `<<<` in
    `.agent/live_review.md` and `.agent/plan.md` — each must be 0.
  E contract tests: `python3 -m pytest tests/docs/ -q` and
    `python3 -m pytest tests/ui_server/test_dashboard_contract.py -q`. Both are
    state-file readers and this round rewrites two state files.
  F canary: `python3 -m pytest tests/cli/test_golden_path.py -q`.
  G hygiene: `git status --porcelain` empty; `git worktree list` the primary
    alone; `git log --numstat df32f595..HEAD` with the `+` column per commit.
  NO red-proof is ordered this round: nothing executable changes, so there is
  no branch to mutate (DECISION F105 D10, checklist item 5).
Handback:    completion report + rewrite `.agent/handoff.md` (changed-files
             table, item-status table over C1a/C1b/C2/C3, the gate table with
             REAL exit codes, transport and pair proofs, open-findings count,
             next action). State plainly that this round's OWN gate is owed to
             the next session per §4.13 and that no repair round was opened for
             it. Then push. Do NOT create a PR.
──────────────────────────────────────────────────────────────
