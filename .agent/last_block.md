── STEP R40 (SESSION CLOSE) — F105 ───────────────────────────
Goal:        Persist the R39 reviewer gate, register R-0263 (the reviewer's own
             unsatisfiable test assertion, which cost R39 its C4 item), correct
             the R39 step line that C2 landed before the blocker was known, and
             close the session against `.agent/STOP`.
Bundle:      C1 save this block · C2 every `.agent/live_review.md` edit ·
             C3 plan and handoff.
Change:      `.agent/authored/f105-r40-1.md`, `.agent/last_block.md`,
             `.agent/live_review.md`, `.agent/plan.md`, `.agent/handoff.md`.
             Nothing else. NO production code, NO test files: state only.
Constraints: `.agent/STOP` is present. This is a CLOSING round: apply these
             pairs, commit, push, and stop. Do NOT start R40's real work (the
             three `do_cmd.py` call sites), do NOT re-land R39's C4 tests, do
             NOT delete or move `.agent/STOP` — it is the operator's file. Do
             not touch `packages/`, `apps/`, `tests/` or `docs/`. Write no
             `Done:` paragraph of your own (§4.4).
Done when:   every gate below is run and its REAL exit code recorded.

C1 — save this block verbatim, TWO commits
  C1a `cp /home/decodeux/Repos/remedy/.remedy-wt/f105-r40-1.block.md`
      `.agent/authored/f105-r40-1.md`. Commit it ALONE.
  C1b `cp` the same bytes to `.agent/last_block.md`. Commit separately.
  `sha256sum` all three plus `cmp`; digest in the handback.

C2 — `.agent/live_review.md`, ONE commit
  Apply PAIR_ID (REWRITE, the header's next-free-ID line), PAIR_F
  (CONTAINS-FROM, R-0263 appended at the end of `## Findings`) and PAIR_S
  (REWRITE, the R39 step line corrected plus the R39 gate record, at the END of
  the file). All three share ONE path in ONE commit: reconcile them TOGETHER
  against that commit's `git show -U0`.

C3 — plan and handoff, ONE commit
  Apply PAIR_P_PLAN to `.agent/plan.md` as a FULL replacement, then rewrite
  `.agent/handoff.md` in your own words per AGENTS.md as the SESSION-CLOSING
  handoff: it names the STOP file, the last reviewed SHA, the open findings,
  and the exact next action for whoever resumes.

<<<PAIR_ID_FROM>>>
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0263.
<<<END_PAIR_ID_FROM>>>

<<<PAIR_ID_TO>>>
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0264.
<<<END_PAIR_ID_TO>>>

<<<PAIR_F_FROM>>>
  today: a composer bug surfaces as a traceback instead of the deterministic
  skeleton. OPEN.
<<<END_PAIR_F_FROM>>>

<<<PAIR_F_TO>>>
  today: a composer bug surfaces as a traceback instead of the deterministic
  skeleton. OPEN.

- R-0263 (Medium, F105 R39, reviewer-authored defect): the R39 block ordered
  two tests whose central assertion, `assert seen == [composed.text]`, cannot
  hold for ANY implementation of the function under test. `run_structured_call`
  does not hand its `base_prompt` to `call_fn`; it hands
  `build_schema_prompt(model_cls, base_prompt, carry)`, which appends a schema
  instruction — 1489 further characters for `JobIntake`. The worker applied the
  pairs, measured `2 failed, 66 passed`, reverted them rather than commit a
  knowingly-red suite, and declared it. That judgement is right and the defect
  is entirely the reviewer's: the block asserted a property of a helper whose
  contract it never read. This is the D8 item-5 class — "reads the code the
  block points at" — widened from mutation reachability to ANY authored
  assertion about a callee's contract, and it is registered as a finding rather
  than a lesson because it cost a real item (C4) and left `composed=` shipping
  untested on its new branch. The fix is known and already proved in a
  disposable worktree at R39: with `assert seen[0].startswith(composed.text)`
  both tests pass at `68 passed`, and reverting either ternary red-proofs its
  own test. Whoever runs R40 lands that corrected form. OPEN.
<<<END_PAIR_F_TO>>>

<<<PAIR_S_FROM>>>
- R39: SPLIT round — record the R38 gate and take the first half of R-0256: a
  keyword-only `composed` on `run_intake` and `plan_job_llm`, one test each,
  both red-proofed. The three `do_cmd.py` call sites are R40's, split out
  because one block carrying both would have broken the D5 cap.
<<<END_PAIR_S_FROM>>>

<<<PAIR_S_TO>>>
- R39: SPLIT round — record the R38 gate and take the first half of R-0256: a
  keyword-only `composed` on `run_intake` and `plan_job_llm`. The three
  `do_cmd.py` call sites were split out to R40 because one block carrying both
  would have broken the D5 cap. The two tests this line originally promised did
  NOT land; the reason is R-0263, registered above.
- Reviewer gate on R39 (2026-08-10): PASS, with two deviations declared by the
  worker and both ACCEPTED. Range `5ca4debd..c44a582c` = five commits, seven
  paths; `apps/cli/commands/do_cmd.py` is absent, as the block required.
  Insertions per commit 347, 281, 37, 21 and 141, each far under 500.
  Transport by the PRIMARY shape: the scratch original
  `.remedy-wt/f105-r39-1.block.md`, the committed
  `.agent/authored/f105-r39-1.md` and `.agent/last_block.md` all three hash to
  `377d8c5e6ffaa18a7d98f17e6dab2ab630e50132417c4109f199022e28bf345b`
  at 347 lines against D5's cap of 400; both `cmp` runs silent.
  All six pairs re-sliced from the COMMITTED authored file: DECLARED equals
  MEASURED for every one, every FROM 1x before its write. PAIR_INTAKE, PAIR_FP
  and PAIR_FP2 REWRITEs at FROM 0x / TO 1x; PAIR_LR CONTAINS-FROM at FROM 1x /
  TO 1x. C2 and C3 reconcile with 0 strays in both directions.
  Gates re-run by THIS reviewer, none taken from the handback: the scoped pair
  `66 passed in 0.67s`; the canary `42 passed in 23.37s`; the C3 diff read line
  by line against the two authored TOs and byte-identical to them. The blocker
  was reproduced independently rather than believed: `run_intake` called with a
  sentinel `composed` sends the provider a prompt that is NOT equal to
  `composed.text` but DOES start with it, 1489 characters longer, carrying
  `SENTINEL` and not the mission argument. So the FEATURE is correct and the
  reviewer's ASSERTION was wrong — registered as R-0263.
  Deviation 1, C4 skipped: ACCEPTED. Landing a knowingly-red pair to satisfy a
  block would be the fabrication the block conditions exist to stop.
  Deviation 2, `.agent/plan.md` not byte-for-byte PAIR_P_PLAN: ACCEPTED. The
  slice claimed "one test each, both red-proofed", which C4 did not deliver;
  AGENTS.md requires plan.md to reflect the current state and carry the exact
  blocker, and AGENTS.md outranks a reviewer's block. The worker applied the
  slice, corrected only the three statements C4 falsified, and declared each.
  Gate I was vacuous as written and the worker said so instead of reporting a
  colour it could not have measured — the R-0252 lesson, applied correctly by a
  worker for once rather than discovered by a reviewer.
  `LAST_REVIEWED_SHA` advances 5ca4debd -> c44a582c.
- R40: SESSION CLOSE — persist this gate, register R-0263, correct the R39 step
  line, and stop against `.agent/STOP`. No production code. This round is the
  last of the session, so by §4.13 its own verdict has no on-disk gate entry: it
  lives in `.agent/handoff.md` and the session's completion report.
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
SESSION CLOSED against `.agent/STOP`. T001 and T002 are DONE and gated; T003's
six migration sites are all migrated. R39 is GATED PASS; `LAST_REVIEWED_SHA` is
c44a582c. R-0256 is HALF fixed: `run_intake` and `plan_job_llm` accept a
keyword-only `composed`, landed and gated, with no test on the new branch yet.
Open findings: R-0221, R-0239, R-0247, R-0256, R-0262, R-0263.
No PR; one is created at CLOSURE.

## Next Steps
- Resume by landing R39's two tests with `seen[0].startswith(composed.text)`,
  which fixes R-0263. Proved in a worktree at R39: 68 passed, and reverting
  either ternary red-proofs its own test.
- Then finish R-0256: pass `composed=` at the three
  `apps/cli/commands/do_cmd.py` sites that already build one — intake,
  flight-plan (whose comment about the second composition goes stale and must
  be replaced) and replan. The new keyword goes on its OWN line: the suite
  counts `on_call=make_flight_plan_call_recorder(` over the WHOLE file
  (tests/orchestration/test_prompt_trace.py, `== 2`).
- Then T004, `remedy stats cache` over actuals; then the integration gate
  (docs/agents/integration_gate.md); then closure
  (docs/roadmap/STATUS_closure_protocol.md), where the PR is created.

## Risks
- R-0221 stays open and will cost the integration gate phantom base-only
  failures.
- R-0262 stays OPEN and out of scope: it needs the composition moved inside the
  `try` in `plan_job_llm` AND at the CLI sites, pinned by a raising composer.
<<<END_PAIR_P_PLAN>>>

GATES — run every one, record the REAL exit code in the handback

A transport
  `sha256sum .remedy-wt/f105-r40-1.block.md .agent/authored/f105-r40-1.md
  .agent/last_block.md` — all three EQUAL; two `cmp` runs, both silent.

B size
  `wc -l .agent/authored/f105-r40-1.md` against the cap of 400 (D5).

C pair shapes, MEASURED not assumed
  Slice every pair from the COMMITTED `.agent/authored/f105-r40-1.md` with a
  whole-line marker reader; never retype. Verify FIRST that every FROM occurs
  exactly 1x in its target before the write, and STOP if one does not. Then:
  PAIR_ID and PAIR_S are REWRITEs — FROM 0x, TO 1x after the write. PAIR_F is
  CONTAINS-FROM — FROM 1x, TO 1x. PAIR_P_PLAN: `cmp` the applied
  `.agent/plan.md` against the slice, `wc -l` against the cap of 50.
  A declared shape that does not equal the measured shape is a STOP.

D added-line reconciliation for C2
  `git show -U0 <C2> -- .agent/live_review.md`: every ADDED line appears in some
  TO, every REMOVED line is a FROM. Both stray counts must be 0.

E marker leakage
  `^<<<` line count is 0 in `.agent/live_review.md`, `.agent/plan.md` and
  `.agent/handoff.md`. Report the numbers, not the word.

F state-file contracts
  `python3 -m pytest tests/docs/ -q` and
  `python3 -m pytest tests/ui_server/test_dashboard_contract.py -q`.
  `.agent/plan.md` keeps `## Goal` and a `Steps` substring;
  `.agent/live_review.md` keeps its `## Steps` heading.

G no production drift
  `git diff --name-only c44a582c..HEAD` lists ONLY paths under `.agent/`.
  Report the list. Nothing under `packages/`, `apps/`, `tests/` or `docs/`.

H canary
  `python3 -m pytest tests/cli/test_golden_path.py -q`.

I hygiene
  `git status --porcelain` shows `?? .agent/STOP` and NOTHING else — that file
  stays. `git worktree list` shows the primary ALONE. Per-commit insertions each
  under 500 via `git show --numstat`.

No mutation red-proof is ordered and none is to be run: nothing executable
changes, so there is no branch to mutate (D8 item 5, DECISION F105 D10).

Handback: completion report + rewrite `.agent/handoff.md` (changed-files table,
item-status table for C1a/C1b/C2/C3, the gate table with real exit codes, the
transport and pair proofs, open-findings count, and the next action for the
session that resumes). Then `git push` and STOP — no further rounds, no PR.
──────────────────────────────────────────────────────────────
