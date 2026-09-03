STEP F110 T001b / ROUND 2 - F110 Model routing by task class
FEATURE F110 - Model routing by task class (Tier 3) - SESSION 1, ROUND 2

Goal
  Consolidate the rival provider-name resolution in
  packages/orchestration/pingpong_job.py onto role_config - consolidation order
  E.a of the T001a inventory - book round 1's PASS verdict into the ledger, and
  resolve R-0768 BY NAME, because the inventory measured that the finding's
  expected fix and E.a are the same edit.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f110-r2.md
  C0b mirror it to .agent/last_block.md
  C1  apply PLAN2 to .agent/plan.md (FIRST substantive commit, item 23)
  C2  append RECORD1 to .agent/live_review.md and SLIPS2 to
      .agent/prose_slips.md - round 1's verdict, booked
  C3  THE PRODUCTION COMMIT: the resolver in pingpong_job.py per SPEC CODE
  C4  THE TEST COMMIT: the new resolver tests and the six fixture repairs
  C5  append DONE1 to .agent/live_review.md - R-0768 resolved
  C6  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f110-r2.md (new, C0a) · .agent/last_block.md (C0b) ·
  .agent/plan.md (C1) · .agent/live_review.md (C2 and C5) ·
  .agent/prose_slips.md (C2) · packages/orchestration/pingpong_job.py (C3) ·
  tests/orchestration/test_job_role_routing.py (new, C4) ·
  tests/orchestration/test_job_task_runner.py (C4) · .agent/handoff.md (C6)

BASE for this round is bbfbb83b. Every byte and count below was measured there.

Constraints
  1. Every authored slice is applied BYTE FOR BYTE: extract it by delimiter
     index from the COMMITTED .agent/authored/f110-r2.md - marker lines
     EXCLUDED - and write it with a script, never by retyping. If a slice looks
     wrong, apply it as written and DECLARE it in the handback.
  2. C1 is the first substantive commit; this round touches the finding ledger,
     so item 23 binds.
  3. COMMIT ORDER IS FIXED AND DONE1 DEPENDS ON IT: C3 (production) precedes C4
     (tests), which precedes C5 (the DONE1 append). DONE1 states facts about
     this round's own landed change and names this constraint rather than a SHA,
     per §3 item 20 as R-0524 carves it out. Do not reorder these three.
  4. Newline conventions, MEASURED at bbfbb83b: .agent/live_review.md ends
     WITHOUT a trailing newline (2140941 bytes) and must still end without one
     after C2 and after C5 - each append is the two bytes newline newline
     followed by the slice. .agent/prose_slips.md likewise ends WITHOUT one.
     .agent/plan.md ends WITH one. Where an extractor yields a trailing newline
     the target does not take, the TARGET's convention wins - this is the round 1
     SLIPS1 ambiguity, now settled, and it is not a contradiction to declare.
  5. NO RUFF GATE IS ORDERED and you must not add one. Round 1 measured that the
     worker's permission layer refuses ruff while the reviewer's does not; the
     reviewer lints C3 itself at review. Write the module to the repository's
     existing style and say nothing about lint.
  6. Do not repair R-0767. It stays OPEN: it widens a CLI allow-list, touches no
     resolver, and is not this round's work.
  7. A sentence OUTSIDE the change set that this round makes stale is DECLARED
     in the handback and NOT repaired.
  8. Read .agent/STOP from disk before the first commit and again before C6. If
     it exists, finish the commit in hand, write the handback, and stop.
  9. Self-review loop before every commit. Push after C6. No pull request, no
     merge. Destructive verification only inside a disposable git worktree.

SPEC CODE - packages/orchestration/pingpong_job.py, written by YOU
  You write this code; it is described, not sliced. Two changes, nothing else.

  (a) A NEW MODULE-LEVEL FUNCTION placed immediately above the existing
      `def _resolve_cfg(` line, which occurs exactly once at bbfbb83b:

        def default_role_provider_name(role, injected_provider=None) -> str

      It returns the provider NAME to record for `role` when neither an explicit
      value nor a persisted one was given. If `injected_provider` is not None and
      carries a non-empty `name` attribute, return that name. Otherwise return
      `role_config.resolve_role_config(role).provider`. Import role_config INSIDE
      the function body: `packages/orchestration/pingpong_job.py` does not import
      it at module level at bbfbb83b and a module-level import risks a cycle you
      have not measured. Carry the one-line WHY comment directly above the def,
      per AGENTS.md Code Discoverability: the recorded provider must name what
      actually ran, and a literal default made an unflagged run report a provider
      it never used.

  (b) THE TWO CALL SITES, in the block that currently reads exactly:

        builder_name, builder_src = _resolve_cfg(
            builder_name, ec.builder if ec else None, "fake")
        reviewer_name, reviewer_src = _resolve_cfg(
            reviewer_name, ec.reviewer if ec else None, "fake")

      Replace each literal "fake" third argument with
      `default_role_provider_name("builder", builder_provider)` and
      `default_role_provider_name("reviewer", reviewer_provider)` respectively.
      Change NOTHING else in that block: max_rounds, test_command,
      claude_cli_write_mode and every later `_resolve_cfg` call keep their
      current defaults. The SOURCE taxonomy is untouched - the resolved default
      still reports source "default", which is what keeps
      `test_first_run_sources_all_default` green.

SPEC TESTS - written by YOU
  (c) NEW FILE tests/orchestration/test_job_role_routing.py, unit tests over
      `default_role_provider_name` ONLY. It is a pure function, so these run with
      no network and no job. Cover at least: no injected provider resolves to
      `role_config.resolve_role_config(role).provider`; an injected provider whose
      `name` is "fake" resolves to "fake"; an injected object with no usable name
      falls back to the role_config answer. Assert against
      `role_config.resolve_role_config(...).provider` rather than against the
      literal "ollama", so the test pins the SEAM and not today's default value.
  (d) SIX FIXTURE REPAIRS in tests/orchestration/test_job_task_runner.py. These
      six tests drive the CLI handler with no injected provider through the
      helper `_make_args`, which defaults `builder` and `reviewer` to None, so
      before this round they relied on the literal default to get a fake run:
        TestCliPauseContinueSmoke::test_full_pause_continue_cycle
        TestMaxRoundsContinuation::test_cli_handler_max_rounds_continuation
        TestCommandPathFullConfigContinuation::test_no_config_drift_in_report
        TestCommandPathGateSmoke::test_normal_two_task_job_completes
        TestCommandPathPreApplySmoke::test_handler_mutation_blocks
        TestCommandPathPreApplySmoke::test_handler_clean_run_unaffected
      Repair each by passing builder="fake" and reviewer="fake" to its
      `_make_args(...)` call - that helper already accepts both keys at
      bbfbb83b. WEAKEN NO ASSERTION, delete no test, change no expected value:
      the fixture is being made to STATE what its own docstring already says.
      The reviewer measured this list in a disposable worktree; if a seventh
      test moves, report it and do NOT repair it silently.

Done when - the gates. Run each, record the REAL exit code and the REAL output.

  G1 TRANSPORT. After C0b: sha256sum .agent/authored/f110-r2.md
     .agent/last_block.md - one digest, twice, both lines reported verbatim.
     This proves the saved copy and its mirror agree and nothing more; the
     reviewer holds no scratch original (§3 item 37).
  G2 THE PLAN. Extract PLAN2 from the COMMITTED authored file, then:
       cmp <extracted> .agent/plan.md          -> exit 0
       wc -l .agent/plan.md                    -> report; must be under 50
       grep -c '^## Goal' .agent/plan.md       -> 1
       grep -c '^## Next Steps' .agent/plan.md -> 1
  G3 THE TWO LEDGER APPENDS, the record file, full arithmetic. For RECORD1 at C2
     and again for DONE1 at C5, each against the file size immediately before
     that commit: report before + 2 separator bytes + slice length, the real new
     size, and whether they are equal. Then, for each, a SECOND READER that
     counts no byte: split the WHOLE file on blank-line boundaries, let N be
     counted BY THE SCRIPT from the slice, and report whether the LAST N units
     equal the slice's N paragraphs IN ORDER. Then, for each, a NEGATIVE CONTROL:
     in a scratch copy flip one byte inside the FIRST appended paragraph and
     report that the second reader REJECTS it. Also report:
       grep -c '^Gate: F110 R1 — ' .agent/live_review.md   -> 1
       grep -c '^Done: R-0768 — ' .agent/live_review.md    -> 1
     and the same two counts taken BEFORE C2 and BEFORE C5 respectively, which
     must both be 0, so the 1 is this round's append and not a pre-existing line.
  G4 THE PROSE FILE. .agent/prose_slips.md gets a BYTE-EQUALITY CHECK ONLY, which
     is all amend0827 rule 5 allows: report whether the file's final bytes equal
     the extracted SLIPS2 slice, whether the pre-C2 content is preserved as an
     exact byte PREFIX, and whether the file still ends without a newline.
  G5 THE PRODUCTION CHANGE. On packages/orchestration/pingpong_job.py at C3:
       git show --numstat C3 -- <that path>   -> report insertions and deletions
       count of the string "fake") in the file BEFORE C3 and AFTER C3
       count of 'default_role_provider_name' AFTER C3 -> report it
       python3 -c "import ast,pathlib;ast.parse(pathlib.Path('packages/orchestration/pingpong_job.py').read_text())"
         -> exit 0, the file still parses
     Report the diff's added and removed lines verbatim; the change must be the
     new function plus the two third arguments and NOTHING else.
  G6 THE MUTATION RED PROOF, in a disposable git worktree at the C4 commit and
     NEVER in the primary checkout. Report the UNMUTATED CONTROL FIRST: run
     tests/orchestration/test_job_role_routing.py unmutated and report its exit
     code and count. Then mutate ONLY the fallback line of
     default_role_provider_name in
     `packages/orchestration/pingpong_job.py` inside that worktree, so the
     function returns the literal "fake" when no provider is injected, and report
     which test ids go RED. THE DISCRIMINATOR: the no-injection case must redden
     while the injected-provider case stays GREEN. A run where both redden, or
     neither, is a failed proof - report it as such rather than reporting a
     colour. Remove the worktree and prune when done; the primary checkout is
     porcelain-empty at the handback.
  G7 THE SUITES, EACH AS ITS OWN INVOCATION, RUN SERIALLY. The reviewer measured
     each of these at bbfbb83b. The first must hold its count with the six
     fixtures repaired - a count that moves is the finding:
       python3 -m pytest tests/orchestration/test_job_task_runner.py -q      191 passed
       python3 -m pytest tests/orchestration/test_role_config.py tests/orchestration/test_provider_mode.py tests/orchestration/test_execution_config_evidence.py -q   75 passed
       python3 -m pytest tests/test_do_job_flow.py tests/orchestration/test_repair_loop.py tests/orchestration/test_long_run_executor.py -q   383 passed
       python3 -m pytest tests/orchestration/test_job_role_routing.py -q     report the count
       python3 -m pytest tests/cli/test_golden_path.py -q                     42 passed
  G8 THE TREE, THE COMMITS AND THE SWEEP. Read git status --porcelain
     immediately before C6 is staged, and git ls-files .remedy-wt (no output),
     and git worktree list (no worktree of this round's own making). Then, for
     C0a through C5 - the commits BEFORE the handback commit, per item 14 -
     report each one's insertion count from git show --numstat, the '+' column
     ONLY, and compare it CELL BY CELL against the Commits table of the handback
     you are writing. C6's own numbers go to neither a round report nor this
     file; the reviewer measures them at the next gate. Then THE STALENESS SWEEP
     over every file this round touched, one entry per file, stale or NOT stale,
     and why.

Handback
  Rewrite .agent/handoff.md per docs/agents/handback_template.md: SESSION 1 of
  F110, round 2, the state block, the item-status table with every ordered item
  appearing exactly once, the Commits table, one line per gate then the
  transcripts, the deviations, the next steps. No length cap.

SLICES. Each slice lies between its own one-line BEGIN and END marker. The
marker lines are NEVER part of the slice. The slices carried here are PLAN2,
RECORD1, SLIPS2 and DONE1.

<<<BEGIN PLAN2>>>
# Plan — F110 Model routing by task class

Branch: feature/f110-model-routing-by-task-class, cut from `main` after
pull request 232 was merged at the Open PR Gate.

## Goal

End one-model-for-everything: every provider call declares a TASK CLASS, a
router maps classes to model tiers, and each routed call records the routed
model WITH its reason. The hard rules of
`docs/agents/model_routing_policy.md` are ENFORCED IN CODE, and moving a
class to a cheaper tier is possible only against documented benchmark
evidence — never by editing a mapping casually.

## Current Step

Round 2, session 1 — T001b, the single resolver seam. The T001a inventory
measured model selection as FOUR rival mechanisms; this round removes the
worst of them by making `packages/orchestration/pingpong_job.py` resolve
its builder and reviewer provider names through `role_config` instead of
the literal `"fake"`. Round 1's PASS verdict is booked into the ledger in
the same round, and `R-0768` is resolved BY NAME because its expected fix
and consolidation order E.a are the same edit.

## Next Steps

- T001c: consolidation order E.b — read `orchestrator.model` THROUGH
  role_config so the orchestrator stops being a third answer to "which
  model". E.c is deliberately NOT done: rebinding
  `make_structured_call_fn`'s Ollama planner is failover work and the
  feature file puts it out of scope.
- T002: the resolver proper — the class table seeded from
  `docs/agents/model_routing_policy.md`, the config schema, the hard-rule
  checks, and one violating fixture per rule refused with the rule named.
- T003: the promotion-evidence discipline, the evidence fields and the
  goldens — a promotion without evidence refused, with evidence logged.
- The integration gate, then the closure sequence, which also runs the one
  checklist consolidation pass DECISION F110 D1 carries into it.

## Risks

- E.a changes what an unflagged run RECORDS and therefore what it runs.
  Six CLI-handler tests encoded the old default and are repaired in the
  same round; a seventh moving test is a finding, not a fixture to patch.
- `R-0767` stays OPEN on the same seam. It widens a CLI allow-list and
  must not be absorbed into a routing commit.
<<<END PLAN2>>>

<<<BEGIN RECORD1>>>
Gate: F110 R1 — the round 1 entry. VERDICT PASS, over the range `6f2230ce..bbfbb83b`. THE OPEN PR GATE WAS EXECUTED AND THE REVIEWER RE-READ IT: pull request 232 is `MERGED` at `2026-09-03T06:30:55Z` with merge commit `6f2230cea29af36a75fea253afc10f4dfe5a79f0`, `gh pr list --state open` answers `[]`, and `git diff --stat edb16a46 6f2230cea29af36a75fea253afc10f4dfe5a79f0` produces NO output — so the base carries the same tree as `edb16a46` and every byte, size and suite count the round 1 block stated at `edb16a46` is true of the base as well. THE TRANSPORT PROOF IS NAMED FOR WHAT IT COVERS, per §3 item 37: this session's reviewer is read-only and held no scratch original, so G1's single digest `3d24b6967e29b302e001d5bf9ce067d98b744c6defecf609d4a98224f39e3126` over `.agent/authored/f110-r1.md` and `.agent/last_block.md` proves the saved copy and its mirror agree and proves NOTHING about the emitted bytes; that claim is unmeasurable in this workflow and is not made. WHAT REPLACES IT IS STRONGER THAN THE DIGEST AND THE REVIEWER MEASURED IT INDEPENDENTLY: each whole-file slice extracted by delimiter index from the COMMITTED authored file is byte-identical to its target, at 1967 bytes for `.agent/plan.md`, 3147 for `.agent/context.md` and 1903 for `.agent/candidates.md` — and those three figures are exactly the byte counts the reviewer measured when authoring the slices, before the block was emitted, so the authored bytes demonstrably survived the round intact. THE TWO APPENDS WERE RE-VERIFIED BYTE FOR BYTE by the reviewer: `.agent/decisions.md` equals its base plus one newline plus the 2162-byte DEC1 slice, 723474 + 1 + 2162 = 725637 matching the file's real size, and its last 7 blank-line units equal DEC1's 7 paragraphs in order; `.agent/prose_slips.md` equals its base plus two newlines plus the 8 SLIPS1 paragraphs, with the base preserved as an exact byte PREFIX and the file still ending without a newline, which is that file's own convention. THE ROUND'S ONE REAL AMBIGUITY WAS THE REVIEWER'S AND THE WORKER RESOLVED IT CORRECTLY: the block's constraint 3 and its gate G5(b) admit two readings of "the slice" for SLIPS1, the marker-excluded region being 3383 bytes WITH the newline that terminates its last line and 3382 without, and only the 3382 reading lets the file keep the newline convention constraint 3 states; the worker took that reading, reported BOTH numbers, and declared the contradiction rather than silently choosing. THE SUITES WERE RE-RUN BY THE REVIEWER, each as its own invocation and serially, at 295, 30, 515, 52, 21, 16 and 42, every one exit 0 — the seven counts the block predicted, NO COUNT MOVED in either direction, which is what a round editing no test and no production code owes. THE T001a INVENTORY IS A REAL MEASUREMENT AND THE REVIEWER CONFIRMED IT WITH AN INDEPENDENT SCAN rather than by re-running the worker's own command: a separately written `ast` walk over `packages`, `apps` and `scripts` finds 5 production call sites of `resolve_role_config`, 8 of `make_structured_call_fn` and 1 of `create_provider`, which are exactly the row counts of the inventory's sections A, B and C. Two spot-checks of the reviewer's own choosing both hold: `apps/cli/commands/do_cmd.py` really does call `_resolve_cli_role_configs` at line 1409 WITHOUT binding its result and bind it at line 2603, and `design_worker` and `test_worker` really do occur exactly once each as quoted strings in production, in their own declaration in `packages/orchestration/role_config.py`. THE CANDIDATE DISCHARGE IS COMPLETE AND SPENT NO ID: `.agent/candidates.md` now reads EMPTY, DECISION F110 D1 carries F109's unperformed checklist consolidation into F110's closure sequence, the eight lessons F109 rounds 8 through 21 owed are on disk in `.agent/prose_slips.md`, and the open set is UNCHANGED at 279 by set difference over 347 distinct registered ids and 68 distinct resolved — which is correct, because amend0827 rule 2 spends an id only on a defect with product effect and none of the four candidates was one. A RULING THE RECORD OWES, because the round declared it as an open obligation: deviation D5 asks whether F109's closure verdict must be booked into this ledger, and it MUST NOT. §4 item 13 rules that the last round of a branch has no on-disk gate entry BY CONSTRUCTION and says in terms not to open a round to close it; F109 round 21 was that round, its own handback declared the same, and the reviewer verdict of that session took the form of the four closure candidates on the disk vehicle, which this round has now discharged. Nothing is missing and D5 needs no path in any later block. TWO OPERATIONAL FACTS THIS RECORD CARRIES FORWARD. First, deviation D3 is right and it changes how blocks are written: the WORKER's permission layer refuses `ruff`, while the reviewer's does not — measured this session as `ruff 0.15.17` answering "All checks passed!" over `packages/orchestration/role_config.py` under the repository's own configuration — so a ruff gate must be run REVIEWER-SIDE and never ordered to a worker. Second, the worker's completion report gave commit `bbfbb83b`'s insertion count as 594, which is `.agent/handoff.md`'s LINE COUNT; `git show --numstat` reads 485 insertions against 376 deletions. That is the §3 item 28 class, the figure never entered any committed file, and the block had already routed that commit's numbers to this gate rather than to the handback — so nothing on disk is wrong and it is a `.agent/prose_slips.md` line, not an id. THE TREE is clean, `git ls-files .remedy-wt` returns nothing, the ten committed paths are exactly the change set, and the branch is pushed at `bbfbb83b`.
<<<END RECORD1>>>

<<<BEGIN SLIPS2>>>
2026-09-03 · F110 R1 · The reviewer's own pre-emission count of the round 1 block projected 397 lines and the block as emitted and committed is 398, measured on the committed `.agent/authored/f110-r1.md`; the §3 item 1 cap of 400 was met either way and no gate consumed the projected figure. Reviewer-prose miscount, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F110 R1 · The reviewer's own step block admitted two readings of "the slice" for the SLIPS1 append — constraint 3 required `.agent/prose_slips.md` to keep ending without a newline while gate G5(b) asked the file's final bytes to equal the extracted slice, which is 3383 bytes with the newline terminating its last line and 3382 without — and only the 3382 reading satisfies both; the worker took it, reported both numbers and declared the ambiguity instead of choosing silently. Reviewer-prose ambiguity between two clauses of one block, nothing wrong on disk and the intended bytes landed; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F110 R1 · The worker's completion report gave commit `bbfbb83b`'s insertion count as 594, which is `.agent/handoff.md`'s line count rather than the `+` column; `git show --numstat` reads 485 insertions against 376 deletions, and the figure never entered any committed file because the block had already routed that commit's numbers to the next gate. This is the §3 item 28 class. Worker completion-report slip, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIPS2>>>

<<<BEGIN DONE1>>>
Done: R-0768 — 2026-09-03, RESOLVED by F110 round 2 (T001b, the single resolver seam). THE DEFECT: `packages/orchestration/pingpong_job.py` resolved the builder and reviewer provider names against the LITERAL default `"fake"` and never imported `role_config`, so an unflagged `remedy do job-run` recorded `builder='fake' (source='default')` and could report a pass that no real provider had earned. THE FIX, landed by the commit this round's constraint 3 fixes as the production commit — the one preceding the test commit, which in turn precedes the commit carrying this paragraph: the two literals are replaced by `default_role_provider_name(role, injected_provider)`, a named function in the same module returning an INJECTED provider's own `name` when a provider object was passed, and otherwise `role_config.resolve_role_config(role).provider`. BOTH HALVES ARE LOAD-BEARING AND THE REVIEWER MEASURED WHY, in a disposable worktree at `bbfbb83b`: replacing the literal with a bare `"ollama"` reddens EIGHT tests in `tests/orchestration/test_job_task_runner.py`, and the injected-name branch fixes two of them, because a run that injects `FakeProvider` — whose `name` property returns `"fake"` — must still RECORD `fake`, and recording anything else would swap one false name for another. The remaining six drive the CLI handler with no injected provider through `_make_args`, which defaults `builder` and `reviewer` to None; they are repaired by naming `fake` explicitly at that helper call, which makes the fixture state what its own docstring already says and weakens no assertion. Resolved when an unflagged run records the resolved product default instead of the literal — pinned directly on the resolver by the new `tests/orchestration/test_job_role_routing.py`, and discriminated by this round's mutation red proof, which reverts the no-injection branch to `return "fake"` and requires the no-injection case to redden while the injected-provider case stays green. THE SCOPE NOTE THIS RESOLUTION OWES: F110 did not go looking for `R-0768`. The T001a inventory measured that the finding's own expected fix and F110's consolidation order E.a are THE SAME EDIT, so the round making that edit resolves it BY NAME rather than letting a repair ride in unannounced under a routing commit. `R-0767`, its sibling on the same seam, is NOT resolved here: it widens a CLI allow-list, touches no resolver, and stays OPEN.
<<<END DONE1>>>
