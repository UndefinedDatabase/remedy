── STEP T003 migration-order 6/6 — F105 ──────────────────────
Goal:        Migrate `_build_reviewer_prompt` to registered prompt segments,
             the last of the six T003 sites, under a content-equality golden.
Bundle:      C1 save this block · C2 record the R23 gate · C3 capture the
             frozen renders and add the reviewer golden · C4 the migration
             itself · C5 plan and handoff.
Change:      `.agent/authored/f105-r24-1.md`, `.agent/last_block.md`,
             `.agent/live_review.md`, `tests/orchestration/test_reviewer_prompt_golden.py`
             (new), `packages/orchestration/pingpong_loop.py`, `.agent/plan.md`,
             `.agent/handoff.md`. Nothing else.
Constraints: Prompt CONTENT does not change; only its composition. The two
             mutually exclusive branches STAY a branch over which segments are
             REGISTERED — a single unconditional registry would emit both diff
             shapes and both scope shapes, which is a content change
             (`.agent/t003_inventory.md` Site 2, "Migration risk").
             `_build_reviewer_prompt` keeps its exact signature and return type.
             No caller changes; no evidence wiring in this round.
             C3 lands BEFORE C4: the renders must be captured from the
             PRE-migration function.
Done when:   every gate below is run and its real exit code recorded.

REVIEWER'S PRE-PROOF — why this spec is known satisfiable
Before authoring this block the reviewer proved the decomposition below
byte-exact against the current `_build_reviewer_prompt`, in a disposable
worktree at 554d9521, over 3584 argument combinations in two passes:
  pass 1  2048 combinations (1024 without a spec-compliance checklist on disk,
          1024 with one), 80 distinct segment sets, 0 byte mismatches.
  pass 2  1536 combinations comparing PRE-MIGRATION registration order against
          RANK order: 0 per-segment byte differences, 0 changes of
          last-segment identity, 0 boundaries needing the fallback newline,
          0 reassembly mismatches.
Pass 2 is the one that matters for the golden's soundness.
`_drop_one_newline_per_segment_boundary` runs over the REGISTRATION order, so
registering in rank order could in principle move which segment keeps its
trailing newline. It does not: the last segment is always the last rank-5 one
in both orderings, and every non-last segment already ends in "\n". Segment
BYTES are therefore invariant under the reorder, which is exactly what lets the
golden reassemble them in pre-migration order and get the old render back.

C1 — save this block verbatim, TWO commits
  C1a `cp` this block to `.agent/authored/f105-r24-1.md`. Commit it ALONE.
  C1b `cp` the same bytes to `.agent/last_block.md`. Commit separately.
  Both are `cp` of the received block — never a retype. Verify with
  `sha256sum` on both plus `cmp`, and record both digests in the handback.

C2 — record the R23 gate (own commit, FIRST content commit)
  Slice PAIR_A by its markers from `.agent/authored/f105-r24-1.md` and apply to
  `.agent/live_review.md`. APPEND-shaped: the TO CONTAINS the FROM verbatim as
  its prefix. Obligation is FROM exactly 1x and each TO-ONLY line exactly 1x —
  not "FROM 0x after".

<<<PAIR_A_FROM>>>
  `LAST_REVIEWED_SHA` advances 54049e6b -> b35d9d56.
<<<END_PAIR_A_FROM>>>

<<<PAIR_A_TO>>>
  `LAST_REVIEWED_SHA` advances 54049e6b -> b35d9d56.
- Reviewer gate on R23 (2026-08-10, next session): PASS. Range
  `b35d9d56..HEAD` at 554d9521, FIVE commits, eight path rows. Insertions per
  `git log --numstat`: 368, 292, 78, 45, 36 — each under 500, and the 368-line
  authored save is under DECISION F105 D5's 400.
  Transport proved disk to disk under the §4.9 DIGEST FALLBACK, stated as
  required: the previous session's scratchpad originals no longer exist, so the
  proof is `sha256sum` over the two COMMITTED files plus `cmp`.
  `.agent/authored/f105-r23-1.md` and `.agent/last_block.md` are byte-identical
  at `fd3271aedac2f81f…`, 368 lines each.
  Gates re-run by THIS reviewer, not accepted from the handback: the golden
  21 passed, `tests/docs/` 294 passed, the canary 42 passed,
  `test_dashboard_contract.py` 70 passed — every number equal to the worker's.
  `.agent/plan.md` measured 47 lines against the cap of 50. Zero BEGIN/END
  transport markers in all four target files; the six `PAIR_` hits in
  `.agent/live_review.md` were read and are prose inside finding text, not
  stray marker lines.
  TWO mutation red-proofs of the REVIEWER's own choosing ran in a disposable
  worktree at HEAD and BOTH went red, so R-0251's pin is real and not merely
  present. M1 deleted the `elif` fallback branch of
  `_drop_one_newline_per_segment_boundary`: exactly two tests failed,
  `test_the_leading_newline_of_the_later_segment_is_the_fallback` and
  `test_each_boundary_chooses_its_own_branch`, reproducing the worker's gate F
  to the test name. M2 replaced the `else: raise` with `pass`: exactly one test
  failed, `test_a_boundary_with_no_newline_at_all_is_illegal`. Both reverted,
  the worktree removed and pruned, `git status --porcelain` empty and
  `git worktree list` the primary alone at this verdict.
  R-0251 and R-0252 are confirmed RESOLVED against the disk, not the summary:
  the test class exists with five tests and the red-proof above, and checklist
  item 5 plus DECISION F105 D10 are on disk and read as intended.
  Declared deviation 1 ACCEPTED and it is the round working as intended: the
  worker MEASURED PAIR_D's shape, found the block's word "prefix" wrong where
  the FROM is the TO's SUFFIX, and reported the measurement instead of the
  claim. Containment holds either way, so application was unaffected.
  `LAST_REVIEWED_SHA` advances b35d9d56 -> 554d9521.
<<<END_PAIR_A_TO>>>

C3 — the golden, captured mechanically, BEFORE the migration (own commit)
  New file `tests/orchestration/test_reviewer_prompt_golden.py`, modelled on
  `tests/orchestration/test_builder_prompt_golden.py` — read that file first
  and follow its shape; it is the site-5 sibling of this one.
  Fixture shapes, four, covering BOTH branches:
    scoped_minimal   scope_packet only
    scoped_full      scope_packet, scope_contract, prior_findings,
                     repair_round=2, safe_diff, test_result
    fallback_minimal no optional argument at all
    fallback_full    scope_contract, prior_findings, repair_round=2,
                     task_excerpt (+ task_sha256, task_tokens_estimated),
                     files_changed, safe_diff, test_result
  Capture `_FROZEN_RENDERS` MECHANICALLY: `git worktree add --detach` at
  554d9521, render the four shapes THERE with the pre-migration function, write
  `repr()` of each render straight into the file. Not one character of prompt
  text is retyped by hand. Say so in the module docstring, with the SHA, as the
  sibling file does. Remove and prune the worktree afterwards.
  `_PRE_MIGRATION_ORDER` — one list serves both branches:
    reviewer_system, reviewer_goal, reviewer_spec_compliance, reviewer_scope,
    reviewer_scope_contract, reviewer_repair, reviewer_task_input,
    reviewer_builder_summary, reviewer_files_changed, reviewer_focused_diff,
    reviewer_staged_diff, reviewer_test_result
  Tests, mirroring the sibling:
    - per shape: segments reassembled in `_PRE_MIGRATION_ORDER` and joined with
      `PROMPT_SEGMENT_DELIMITER` equal the frozen render; the manifest's
      sha256 set equals the frozen parts' sha256 set.
    - the reorder is REAL: `fallback_minimal` is byte-identical to its frozen
      render, and `scoped_full` and `fallback_full` are NOT.
    - per shape: manifest ranks are non-decreasing.
    - `scoped_full` registers exactly, in this order:
      reviewer_system(0), reviewer_scope(3), reviewer_scope_contract(3),
      reviewer_goal(4), reviewer_repair(5), reviewer_builder_summary(5),
      reviewer_focused_diff(5), reviewer_test_result(5)
    - `fallback_full` registers exactly, in this order:
      reviewer_system(0), reviewer_scope_contract(3), reviewer_goal(4),
      reviewer_task_input(4), reviewer_repair(5), reviewer_builder_summary(5),
      reviewer_files_changed(5), reviewer_staged_diff(5),
      reviewer_test_result(5)
    - the inversions are fixed, asserted on the MANIFEST not on string
      positions: in `scoped_full`, index(reviewer_scope) and
      index(reviewer_scope_contract) both < index(reviewer_goal); in
      `fallback_full`, index(reviewer_scope_contract) < index(reviewer_goal)
      and index(reviewer_task_input) < index(reviewer_repair). Assert the
      OPPOSITE holds in the frozen renders, so the test proves a change.
    - `_build_reviewer_prompt` returns `compose_reviewer_prompt(...).text` for
      all four shapes.
  This commit is TEST-ONLY and MUST be red against the pre-migration code for
  the compose_* tests. Write it, run it, RECORD the red, then do C4. Do not
  combine C3 and C4 into one commit.

C4 — the migration (own commit)
  Add `compose_reviewer_prompt` to `packages/orchestration/pingpong_loop.py`
  next to `compose_builder_prompt`, same shape: build a
  `list[tuple[str, SegmentStabilityRank, list[str]]]`, hand the joined texts to
  `_drop_one_newline_per_segment_boundary`, register in RANK order into a
  `PromptSegmentRegistry`, return `compose_prompt_segments(...)`.
  Signature identical to `_build_reviewer_prompt`'s, returning `ComposedPrompt`.
  `_build_reviewer_prompt` becomes a one-line delegation returning `.text`,
  keeping its docstring updated the way `_build_builder_prompt`'s was.
  Segment table — names, ranks, conditions, and the parts each carries. Take
  the parts EXPRESSIONS verbatim from today's function bodies; the reviewer
  proved these exact groupings byte-exact.
    reviewer_system            SYSTEM       always   [_REVIEWER_SYSTEM, "\n"]
    reviewer_goal              TASK         always   ["## Original Goal\n{goal}\n"]
    reviewer_spec_compliance   JOB_CONTEXT  if the rendered summary is truthy
    reviewer_scope             JOB_CONTEXT  scope-packet branch, always
    reviewer_scope_contract    JOB_CONTEXT  if scope_contract
    reviewer_repair            STEERING     if prior_findings and repair_round>0
    reviewer_task_input        TASK         fallback branch, if task_excerpt
    reviewer_builder_summary   STEERING     always
    reviewer_files_changed     STEERING     fallback branch, if files_changed
    reviewer_focused_diff      STEERING     scope-packet branch, safe_diff else
                                            diff_summary — the elif STAYS an elif
    reviewer_staged_diff       STEERING     fallback branch, same elif
    reviewer_test_result       STEERING     if test_result
  The `reviewer_repair` parts list is the header string, then one entry per
  finding, then a trailing "" — exactly as today, and exactly as
  `builder_repair` does it.
  The two diff caps stay distinct: `_REVIEWER_SCOPED_DIFF_CAP` with
  "\n[FOCUSED DIFF TRUNCATED]" on the scoped branch, `_REVIEWER_DIFF_CAP` with
  "\n[DIFF TRUNCATED]" on the fallback. Do not unify them.
  `_load_review_scope_packet` is still consulted when `scope_packet is None`,
  before the branch is chosen, exactly as today.
  Add the one-line WHY comment above `compose_reviewer_prompt` naming this as
  T003 migration site 6 and stating that its golden is equal-modulo-ordering,
  the way site 5's comment does.

C5 — plan and handoff (own commit)
  Apply PAIR_B to `.agent/plan.md` as a FULL replacement, then rewrite
  `.agent/handoff.md`.

<<<PAIR_B_PLAN>>>
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
T001 and T002 are DONE and gated. T003 counts in the MIGRATION ORDER of
`.agent/t003_inventory.md`, never that file's catalogue "Site N" headings
(R-0241). R23 is GATED; `LAST_REVIEWED_SHA` is 554d9521. R24 takes
migration-order step 6, `_build_reviewer_prompt`, the LAST of the six, under a
content-equality golden. Its decomposition was proved byte-exact by the
reviewer over 3584 argument combinations before the block was authored,
including the rank-order-vs-registration-order invariance the golden rests on.
Open findings: R-0221, R-0239, R-0246, R-0247. No PR; one is created at CLOSURE.

## Next Steps
- R25 gates R24. With step 6 landed, all six T003 migration sites are done.
- ONE later round wires `on_call` for the three sites lacking call evidence:
  `mission_cmd.py:362` (orchestrator), `mission_cmd.py:187` +
  `gauntlet_runner.py:505` (mission), `do_cmd.py:253` + `:2860` (plan).
- Fix R-0246 in the round that next touches `mission_compiler.py`.
- Then T004, `remedy stats cache` over actuals; then the integration gate
  (docs/agents/integration_gate.md); then closure
  (docs/roadmap/STATUS_closure_protocol.md), where the PR is created.

## Risks
- R-0221 stays open and will cost the integration gate phantom base-only
  failures.
- The reviewer prompt is the worst-ordered of the six sites, so T004's
  before/after number should quote its cacheable-prefix gain specifically.
<<<END_PAIR_B_PLAN>>>

GATES — run every one, record the REAL exit code and the REAL output
  A transport: `sha256sum` on `.agent/authored/f105-r24-1.md` and
    `.agent/last_block.md`; `cmp` them. Both digests in the handback.
  B size: `wc -l .agent/authored/f105-r24-1.md`.
  C application: FROM/TO occurrence counts for PAIR_A; `cmp` the applied
    `.agent/plan.md` against the sliced PAIR_B; `wc -l .agent/plan.md` (must be
    under 50); grep the three marker strings `PAIR_A_FROM`, `PAIR_B_PLAN`,
    `END_PAIR` in `.agent/live_review.md` and `.agent/plan.md` — each must be 0.
  D C3 red: run the new golden against the PRE-migration code and record the
    failure count and the failing test names. This is the ordered RED.
  E C4 green: `python3 -m pytest tests/orchestration/test_reviewer_prompt_golden.py -q`.
  F callers unchanged: `python3 -m pytest tests/orchestration/test_pingpong_cli.py
    tests/orchestration/test_reviewer_prompt_scope.py
    tests/orchestration/test_builder_prompt_golden.py
    tests/orchestration/test_prompt_segments.py -q`. Record the count and state
    whether it equals the pre-round baseline; take that baseline BEFORE C4.
  G canary: `python3 -m pytest tests/cli/test_golden_path.py -q`.
  H red-proofs, in a disposable `git worktree` at HEAD, NEVER in the primary
    checkout. Both mutations are on always-registered segments, so both are
    reachable in every shape:
      M1 change `reviewer_goal`'s rank from TASK to SYSTEM. Expect RED on the
         rank-order and inversion tests. Report the failing test names.
      M2 drop the bare "\n" from `reviewer_system`'s parts. Expect RED on the
         frozen-render tests. Report the failing test names.
    Revert both, `git worktree remove` and `git worktree prune`, then show
    `git status --porcelain` empty and `git worktree list`.
  I hygiene: `git status --porcelain` empty; `git log --numstat b35d9d56..HEAD`
    with the `+` column per commit, each under 500.
Handback:    completion report + rewrite `.agent/handoff.md` (changed-files
             table, item-status table, the gate table with REAL exit codes, the
             transport and pair proofs, open-findings count, next action).
──────────────────────────────────────────────────────────────
