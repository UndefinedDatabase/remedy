── STEP R42 — F105 ───────────────────────────────────────────
Goal:        Persist the R41 reviewer gate, resolve R-0256, R-0263 and R-0264
             with reviewer-authored `Done:` text, and produce the read-only
             shape inventory T004 needs before any `remedy stats cache` code is
             written.
Bundle:      C1 save this block · C2 every `.agent/live_review.md` edit ·
             C3 the T004 inventory · C4 plan and handoff.
Change:      `.agent/authored/f105-r42-1.md`, `.agent/last_block.md`,
             `.agent/live_review.md`, `.agent/t004_inventory.md`,
             `.agent/plan.md`, `.agent/handoff.md`. Nothing else.
             NO production code, NO test files, NO `docs/`: state only.
Constraints: C3 is an INVESTIGATION, not an implementation. Read the code,
             write down what is there, and write down what is MISSING — do not
             add a command, a module, a field or a test this round. An
             inventory that guesses is worse than one that says "not found":
             every claim in it carries a `path:line` a reader can open. Do not
             touch `packages/`, `apps/`, `tests/` or `docs/`. Write no `Done:`
             paragraph of your own — the three below are authored (§4.4).
Done when:   every gate below is run and its REAL exit code recorded.

C1 — save this block verbatim, TWO commits
  C1a `cp /home/decodeux/Repos/remedy/.remedy-wt/f105-r42-1.block.md`
      `.agent/authored/f105-r42-1.md`. Commit it ALONE.
  C1b `cp` the same bytes to `.agent/last_block.md`. Commit separately.
  `sha256sum` all three plus `cmp`; digest in the handback.

C2 — `.agent/live_review.md`, ONE commit
  Apply PAIR_D1 and PAIR_D2 (REWRITEs — each replaces the worker's one-line
  `Landed:` marker with the reviewer's `Done:` paragraph), PAIR_D3
  (CONTAINS-FROM, the `Done:` paragraph appended below R-0264's OPEN line) and
  PAIR_S (CONTAINS-FROM, the R41 gate record plus the R42 step line at the END
  of the file). All four share ONE path in ONE commit: reconcile them TOGETHER
  against that commit's `git show -U0`.

C3 — `.agent/t004_inventory.md`, ONE commit, NEW file, YOUR OWN words
  A read-only inventory answering exactly these six questions, in this order,
  each answer carrying the `path:line` it rests on, and saying "not found"
  where that is the truth:
  1. Where does a per-call cache-read figure enter the system today? Start at
     `packages/orchestration/token_actuals.py` and
     `packages/orchestration/provider_token_evidence.py` and report which
     field carries it, what its type is, and what a provider that reports
     nothing leaves behind.
  2. `apps/cli/commands/stats_ledger_cmd.py` already renders a `Cache read`
     column for `remedy stats cost`. Report its row shape, how it decides to
     print `unmeasured` rather than `0`, and which function a `cache`
     subcommand would sit beside.
  3. Does anything today carry a ROLE dimension on a token figure — `intake`,
     `flight_plan`, `builder` and so on? `packages/orchestration/prompt_trace.py`
     records `role` on a trace entry; the ledger records usage per call. Report
     whether a JOIN key exists between the two, name it, and if none exists say
     so plainly — that gap IS the T004 design question.
  4. What does the ledger's schema look like where a cache-read figure lands
     (`packages/orchestration/token_ledger.py`), and would a per-role grouping
     need a schema change or only a query change?
  5. Which fixtures exist that a `remedy stats cache` test could read as
     ACTUALS? The acceptance line is "cache stats render from fixture actuals",
     so name the fixture files and the tests that already build them.
  6. What is the smallest honest first slice? One paragraph, naming the files
     it would touch, and naming explicitly what it would NOT do.
  End the file with a short "Open questions for the reviewer" list. Do not
  answer them yourself and do not implement around them.

C4 — plan and handoff, ONE commit
  Apply PAIR_P_PLAN to `.agent/plan.md` as a FULL replacement, then rewrite
  `.agent/handoff.md` in your own words per AGENTS.md.

<<<PAIR_D1_FROM>>>
  Landed: R-0256 — 3e2fa6bc passes composed= at all three do_cmd.py call sites.
<<<END_PAIR_D1_FROM>>>

<<<PAIR_D1_TO>>>
  Done: R-0256 (2026-08-10) — RESOLVED. One composition now feeds both the
  provider and the trace at every site. `run_intake` and `plan_job_llm` take a
  keyword-only `composed` (R39, gated at c44a582c) and all three
  `apps/cli/commands/do_cmd.py` sites hand theirs down (3e2fa6bc): intake at
  217, flight-plan at 267, replan at 2888. The comment that described the
  second composition was replaced in the same commit rather than left to rot.
  Verified by the reviewer against the applied files, not the diff alone:
  `composed=` occurs 3x in `do_cmd.py` and
  `on_call=make_flight_plan_call_recorder(` still occurs 2x, so the existing
  wiring guard is intact. Red-proof by the reviewer in a disposable worktree at
  87ef21d9, a mutation the round did NOT order: deleting
  `composed=intake_composed,` alone turns
  `test_every_cli_call_site_hands_its_composition_down` RED, so the guard
  discriminates per site and not only on the one site R41 mutated.
<<<END_PAIR_D1_TO>>>

<<<PAIR_D2_FROM>>>
  Landed: R-0263 — 398c7752 lands both tests in the corrected startswith form.
<<<END_PAIR_D2_FROM>>>

<<<PAIR_D2_TO>>>
  Done: R-0263 (2026-08-10) — RESOLVED. Both tests landed in the form this
  finding proved correct: `assert len(seen) == 1` plus
  `assert seen[0].startswith(composed.text)`, never equality, because
  `run_structured_call` hands `call_fn` the schema-decorated prompt. The
  length pin keeps what the old list-equality assertion also asserted, so
  nothing was traded away for the fix. Verified by the reviewer: the scoped
  suite is `119 passed in 0.97s` re-run independently, and both mutations
  reproduce RED — reverting the `intake.py` ternary reddens only the intake
  test, reverting the `flight_plan.py` ternary only the flight-plan test. The
  finding's own root cause — an authored assertion about a callee's contract
  the block never read — stays on disk as the D8 item-5 widening.
<<<END_PAIR_D2_TO>>>

<<<PAIR_D3_FROM>>>
  gate below supplies it. OPEN.
<<<END_PAIR_D3_FROM>>>

<<<PAIR_D3_TO>>>
  gate below supplies it. OPEN.
  Done: R-0264 (2026-08-10) — RESOLVED. The R40 step line now carries the
  correction ("That reading was wrong ... the round stayed gateable and the
  next session gated it below", 3682dac9) and the R40 gate record sits directly
  beneath it, so the disk no longer tells a resuming reader that no gate is
  coming. The distinction this finding names is the durable part: §4.13's
  terminator is a property of a BRANCH at closure, where no later round exists
  to write the record. A session boundary is not that; a round left ungated by
  a session limit is an ordinary handback and the next session gates it. Nothing
  in §4.13 needed changing — it already says "branch" — so no amendment was
  authored and none should be.
<<<END_PAIR_D3_TO>>>

<<<PAIR_S_FROM>>>
  Both changes were red-proofed by the reviewer in disposable worktrees at
  7f622b7f before this block was authored.
<<<END_PAIR_S_FROM>>>

<<<PAIR_S_TO>>>
  Both changes were red-proofed by the reviewer in disposable worktrees at
  7f622b7f before this block was authored.
- Reviewer gate on R41 (2026-08-10): PASS, with one deviation declared by the
  worker and ACCEPTED. Range `7f622b7f..87ef21d9` = six commits, nine paths,
  exactly the nine the block named; nothing under `packages/` or `docs/`.
  Insertions per commit 383, 299, 43, 44, 16 and 111, each far under 500.
  Transport by the PRIMARY shape: `.remedy-wt/f105-r41-1.block.md`, the
  committed `.agent/authored/f105-r41-1.md` and `.agent/last_block.md` all
  three hash to
  `58b153128ab2711982bfed1163a80f6286ab2f9c0716d060390594b155773baf`
  at 383 lines against D5's cap of 400; both `cmp` runs silent.
  The two production diffs were read line by line against the authored TOs and
  are byte-identical to them: three keyword lines added to `do_cmd.py`, one
  stale comment replaced, two test classes appended, one wiring guard appended.
  Gates re-run by THIS reviewer, none taken from the handback: the scoped suite
  `119 passed in 0.97s`; `tests/docs/` `294 passed in 0.25s`;
  `test_dashboard_contract.py` `70 passed in 3.99s`; the canary
  `42 passed in 19.92s`. `composed=` 3x and
  `on_call=make_flight_plan_call_recorder(` 2x in `do_cmd.py`; the transport
  marker count is 0 in all seven touched text files; `.agent/plan.md` is 37
  lines against the cap of 50.
  One spot-check the block did NOT order, run in a disposable worktree at
  87ef21d9 and removed after: deleting `composed=intake_composed,` alone turns
  the wiring guard RED, so it discriminates per site.
  The deviation, ACCEPTED: `.agent/handoff.md` at 127 lines with its DECISION
  D15 stated-cause line. The mandated tables account for it and no section was
  dropped.
  One reviewer-side lesson, not a finding, because it cost nothing: the block's
  C5 instruction placed a `Landed:` line inside PAIR_F's TO region, which broke
  that TO's contiguity in the final file. The worker measured the post-state,
  declared it and did not hide it. A block that orders a later insertion into an
  earlier pair's TO should say so at authoring time, in the pair's own shape
  declaration.
  `LAST_REVIEWED_SHA` advances 7f622b7f -> 87ef21d9.
- R42: state and investigation round — record the R41 gate, resolve R-0256,
  R-0263 and R-0264, and produce the read-only `.agent/t004_inventory.md` that
  T004 needs before any `remedy stats cache` code exists. No production code.
<<<END_PAIR_S_TO>>>

<<<PAIR_P_PLAN>>>
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
R42 landed. T001, T002 and T003 are DONE and gated: every builder composes via
the registry and one composition now feeds both the provider and the trace at
all three CLI sites. R41 is GATED PASS; `LAST_REVIEWED_SHA` is 87ef21d9.
R-0256, R-0263 and R-0264 are RESOLVED with reviewer-authored `Done:` text.
Open findings: R-0221, R-0239, R-0247, R-0262.
T004 is the only slice left; `.agent/t004_inventory.md` is its ground truth.
No PR; one is created at CLOSURE.

## Next Steps
- T004 slice 1, scoped from the inventory: `remedy stats cache` over actuals,
  cache-read share per role, `unmeasured` and never `0` where no provider
  reported — the discipline `remedy stats cost` already applies.
- Then the before/after comparison note in the feature's evidence, with honest
  numbers whatever they are (the feature file's T004 line).
- Then the integration gate (docs/agents/integration_gate.md); R-0221 will
  attribute phantom base-only failures there and that is expected, not new.
- Then closure (docs/roadmap/STATUS_closure_protocol.md), where the evidence
  job, the FRESH review zip, the STATUS line and the PR all land.

## Risks
- T004 may find no join key between a trace's `role` and a ledger row. If so
  the honest first slice reports per-role only where the join exists and says
  "not reported" elsewhere — it never invents a role for a call.
- R-0221 stays open and will cost the integration gate phantom base-only
  failures.
- R-0262 stays OPEN and out of scope: it needs the composition moved inside the
  `try` in `plan_job_llm` AND at the CLI sites, pinned by a raising composer.
<<<END_PAIR_P_PLAN>>>

GATES — run every one, record the REAL exit code in the handback

A transport
  `sha256sum .remedy-wt/f105-r42-1.block.md .agent/authored/f105-r42-1.md
  .agent/last_block.md` — all three EQUAL; two `cmp` runs, both silent.

B size
  `wc -l .agent/authored/f105-r42-1.md` against the cap of 400 (D5).

C pair shapes, MEASURED not assumed
  Slice every pair from the COMMITTED `.agent/authored/f105-r42-1.md` with a
  whole-line marker reader; never retype. Verify FIRST that every FROM occurs
  exactly 1x in its target before its write, and STOP if one does not. Then:
  PAIR_D1 and PAIR_D2 are REWRITEs — FROM 0x, TO 1x after the write. PAIR_D3
  and PAIR_S are CONTAINS-FROM — FROM 1x, TO 1x. PAIR_P_PLAN: `cmp` the applied
  `.agent/plan.md` against the slice, `wc -l` against the cap of 50.
  A declared shape that does not equal the measured shape is a STOP. No pair
  this round writes into another pair's TO region.

D added-line reconciliation for C2
  `git show -U0 <C2> -- .agent/live_review.md`: every ADDED line appears in some
  TO, every REMOVED line is a FROM. Both stray counts must be 0.

E marker leakage
  `^<<<` line count is 0 in `.agent/live_review.md`, `.agent/t004_inventory.md`,
  `.agent/plan.md` and `.agent/handoff.md`. Report the numbers, not the word.

F state-file contracts
  `python3 -m pytest tests/docs/ -q` and
  `python3 -m pytest tests/ui_server/test_dashboard_contract.py -q`.
  `.agent/plan.md` keeps `## Goal` and a `Steps` substring;
  `.agent/live_review.md` keeps exactly one `## Steps` heading.

G no production drift
  `git diff --name-only 87ef21d9..HEAD` lists ONLY these six paths:
  `.agent/authored/f105-r42-1.md`, `.agent/last_block.md`,
  `.agent/live_review.md`, `.agent/t004_inventory.md`, `.agent/plan.md`,
  `.agent/handoff.md`. Report the list. Nothing under `packages/`, `apps/`,
  `tests/` or `docs/`.

H no `Landed:` survivors
  `grep -c 'Landed: R-0256' .agent/live_review.md` and the same for R-0263 —
  BOTH must be 0, because PAIR_D1 and PAIR_D2 replace those lines. Report the
  two numbers.

I canary
  `python3 -m pytest tests/cli/test_golden_path.py -q`.

J inventory honesty
  Every `path:line` claim in `.agent/t004_inventory.md` was opened and read
  before it was written. Spot-report three of them with the line they point at,
  so the reviewer can check the pointer without re-deriving the file.

K hygiene
  `git status --porcelain` EMPTY. `git worktree list` shows the primary ALONE.
  Per-commit insertions each under 500 via `git show --numstat`.

No mutation red-proof is ordered and none is to be run: nothing executable
changes, so there is no branch to mutate (D8 item 5, DECISION F105 D10).

Handback: completion report + rewrite `.agent/handoff.md` (changed-files table,
item-status table for C1a/C1b/C2/C3/C4, the gate table with real exit codes, the
transport and pair proofs, the three spot-reported inventory pointers,
open-findings count, and the next expected action). Then `git push`. Do NOT
create a PR — the PR is created at CLOSURE only.
──────────────────────────────────────────────────────────────
