── STEP R38 — F105 ───────────────────────────
Goal:        Record the R37 reviewer gate, resolve R-0261 with
             reviewer-authored `Done:` text, register R-0262, and leave the
             R-0256 production round fully specified for the next session.
Bundle:      C1 save this block · C2 every `.agent/live_review.md` edit ·
             C3 plan and handoff.
Change:      `.agent/authored/f105-r38-1.md`, `.agent/last_block.md`,
             `.agent/live_review.md`, `.agent/plan.md`, `.agent/handoff.md`.
             Nothing else. NO production code, NO test files: this is a
             state-only round.
Constraints: Do not touch `packages/`, `apps/`, `tests/` or `docs/`. Do not
             reflow any line you were not given a pair for. Write no `Done:`
             paragraph of your own — this block's authored text carries the
             only one this round has (§4.4).
Done when:   every gate below is run and its REAL exit code recorded.

C1 — save this block verbatim, TWO commits
  C1a `cp /home/decodeux/Repos/remedy/.remedy-wt/f105-r38-1.block.md`
      `.agent/authored/f105-r38-1.md`. Commit it ALONE.
  C1b `cp` the same bytes to `.agent/last_block.md`. Commit separately.
  `sha256sum` all three plus `cmp`; digest in the handback.

C2 — `.agent/live_review.md`, ONE commit
  Apply PAIR_A (REWRITE, the header's next-free-ID line), PAIR_B
  (CONTAINS-FROM, one append carrying BOTH the `Done:` for R-0261 and the
  registration of R-0262 after it, so the end of `## Findings` reads: the
  R-0261 finding, its `Done:`, a blank line, then R-0262) and PAIR_C
  (CONTAINS-FROM, the R37 step line and gate record at the END of the file).
  All three share ONE path in ONE commit: reconcile them TOGETHER against that
  commit's `git show -U0` — every added line comes from a TO, every removed
  line is a FROM.

C3 — plan and handoff, ONE commit
  Apply PAIR_P to `.agent/plan.md` as a FULL replacement, then rewrite
  `.agent/handoff.md` in your own words per AGENTS.md.

<<<PAIR_A_FROM>>>
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0262.
<<<END_PAIR_A_FROM>>>

<<<PAIR_A_TO>>>
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0263.
<<<END_PAIR_A_TO>>>

<<<PAIR_B_FROM>>>
  guard's OWN window against its OWN call, which is what R-0260 asked for and
  what a reader of that line needs. OPEN.
<<<END_PAIR_B_FROM>>>

<<<PAIR_B_TO>>>
  guard's OWN window against its OWN call, which is what R-0260 asked for and
  what a reader of that line needs. OPEN.
  Done: R-0261 (2026-08-10) — RESOLVED at F105 R37, commit 82cbb3e5. Neither
  comment quotes a cross-site character distance any more; both state what the
  guard holds and why no number is given. Verified by this reviewer against the
  applied files rather than the handback: `grep -c 7335` is 0 in both test
  files, while `.agent/live_review.md` keeps the number in this finding's own
  text, which is where a stale figure costs nothing. The per-site overshoots —
  71 and 27 — survive untouched, as R-0260's resolution requires, and the 317
  tests of the two modules stay green with the constant 200 and both
  `source.index` anchors unchanged.

- R-0262 (Low, F105 R38, pre-existing, registered NOT fixed): `plan_job_llm`
  composes its prompt OUTSIDE the `try` that turns a provider failure into
  `FlightPlanResult(plan=None, error_hint=...)`. In
  `packages/orchestration/flight_plan.py` the line
  `prompt = _build_plan_prompt(intake)` sits directly above `try:`, so a
  raising composer escapes the function instead of becoming a result the
  caller can render. That is the R-0257 shape in the function R-0257 did not
  cover. `run_intake` has the opposite, correct shape — its composition is an
  ARGUMENT inside the `try`. Registered rather than fixed, for two reasons
  worth stating: it is pre-existing and outside the R-0256 change set, and
  fixing the function ALONE would not save the CLI, because
  `apps/cli/commands/do_cmd.py` composes at its own call site outside any
  `try` as well. The honest fix is one round covering the function and both
  call sites together, pinned by a test that makes the composer raise. Cost
  today: a composer bug surfaces as a traceback instead of the deterministic
  skeleton. OPEN.
<<<END_PAIR_B_TO>>>

<<<PAIR_C_FROM>>>
  `LAST_REVIEWED_SHA` advances bcfb12e3 -> 25e6326a.
<<<END_PAIR_C_FROM>>>

<<<PAIR_C_TO>>>
  `LAST_REVIEWED_SHA` advances bcfb12e3 -> 25e6326a.
- R37: state round — record the R36 gate, resolve R-0259 and R-0260, register
  and fix R-0261. No production code.
- Reviewer gate on R37 (2026-08-10): PASS. Range `25e6326a..c30b365e` = five
  commits, seven paths; `git diff --stat` lists exactly the seven the block
  named, nothing under `packages/` or `apps/`. Insertions per commit 339, 281,
  101, 9 and 62, each far under 500.
  Transport by the PRIMARY shape, not the §4.9 fallback: the reviewer's scratch
  original `.remedy-wt/f105-r37-1.block.md`, the committed
  `.agent/authored/f105-r37-1.md` and `.agent/last_block.md` all three hash to
  `0fc0c2c71e800ac650febcf24dec1cc1a5733fc3998537ea8865b0ef9f99ef5a`
  at 339 lines, against DECISION F105 D5's cap of 400.
  All eight pairs re-sliced from the COMMITTED authored file by this reviewer's
  own marker reader: declared equals measured for every one. PAIR_V, PAIR_W,
  PAIR_X, PAIR_F2 and PAIR_G2 are REWRITEs at FROM 0x / TO 1x; PAIR_Y and
  PAIR_Z are CONTAINS-FROM at FROM 1x; PAIR_P is byte-equal to the applied
  `.agent/plan.md` at 42 lines against the cap of 50. C2's four live_review
  pairs reconcile together against `+101/-3` with 0 strays in both directions.
  Gates re-run by THIS reviewer, none taken from the handback: `tests/docs/`
  plus the dashboard contract `364 passed in 4.36s`; the scoped pair
  `317 passed in 1.41s`; the canary `42 passed in 19.73s`; `grep -c 7335` is 0
  in both test files; zero `^<<<` lines in all five written targets;
  `git status --porcelain` empty and `git worktree list` the primary alone at
  this verdict. No red-proof was ordered or run: nothing executable changed,
  which the worker proved by AST equality with docstrings blanked (D8 item 5).
  One deviation, DECLARED by the worker and ACCEPTED as correct: no
  `Landed: R-0261` line was written. The reviewer's worker brief asked for one
  while the block's own gate D mandated zero stray added lines in C2, and no TO
  contained such a line — so the block had no legal slot for it, and the worker
  chose the under-claiming side over a deliberately red gate. That judgement is
  right and the defect is the reviewer's: a block that registers AND fixes a
  finding in the same round must reserve the marker's slot inside a TO. The
  cost was nil, because the `Done:` text lands one round later either way,
  which is why this is recorded as a lesson rather than registered as a
  finding.
  `LAST_REVIEWED_SHA` advances 25e6326a -> c30b365e.
<<<END_PAIR_C_TO>>>

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
T001 and T002 are DONE and gated. T003's six migration sites are all migrated.
R37 is GATED; `LAST_REVIEWED_SHA` is c30b365e. R38 is a state-only round: it
records the R37 gate, resolves R-0261 and registers R-0262.
Open findings: R-0221, R-0239, R-0247, R-0256, R-0262.
No PR; one is created at CLOSURE.

## Next Steps
- R39 fixes R-0256, the next round and a SPLIT one: give `plan_job_llm`
  (`packages/orchestration/flight_plan.py`) and `run_intake`
  (`packages/orchestration/intake.py`) a keyword-only
  `composed: ComposedPrompt | None = None`, used as
  `composed.text if composed is not None else <the existing builder call>`.
  `ComposedPrompt` is already imported in both modules. In `run_intake` the
  expression MUST stay the argument inside the `try` (R-0257); in
  `plan_job_llm` it stays exactly where it is (R-0262 is not fixed there).
  Then pass `composed=` at the three `apps/cli/commands/do_cmd.py` call sites
  that already build one: the intake site, the flight-plan site (whose comment
  about the second composition goes stale and must be replaced) and the replan
  site. Two tests, one per module: build a ComposedPrompt with a sentinel,
  pass a DIFFERENT mission/facts to the function, assert the provider saw
  exactly `composed.text`. Red-proof each by reverting the function to its
  unconditional builder call — both branches are reachable from those tests.
  Prompt CONTENT must not change: digest `compose_*_prompt(...).text` for a
  fixed input before and after and show the two are equal.
- Then T004, `remedy stats cache` over actuals; then the integration gate
  (docs/agents/integration_gate.md); then closure
  (docs/roadmap/STATUS_closure_protocol.md), where the PR is created.

## Risks
- R-0221 stays open and will cost the integration gate phantom base-only
  failures.
- The reviewer prompt was the worst-ordered of the six sites and 1824 of 2048
  measured renders reorder, so T004's before/after number should quote its
  cacheable-prefix gain specifically.
<<<END_PAIR_P_PLAN>>>

GATES — run every one, record the REAL exit code in the handback

A transport
  `sha256sum .remedy-wt/f105-r38-1.block.md .agent/authored/f105-r38-1.md
  .agent/last_block.md` — all three EQUAL; two `cmp` runs, both silent. PRIMARY
  shape: the scratch original exists.

B size
  `wc -l .agent/authored/f105-r38-1.md` against the cap of 400 (D5).

C pair shapes, MEASURED not assumed
  Slice every pair from the COMMITTED `.agent/authored/f105-r38-1.md` with a
  whole-line marker reader; never retype. Verify FIRST that every FROM occurs
  exactly 1x in its target before the write, and STOP if one does not. Then:
    PAIR_A REWRITE: FROM 0x and TO 1x after the write.
    PAIR_B and PAIR_C CONTAINS-FROM: FROM exactly 1x after the write.
    PAIR_P: `cmp` the applied `.agent/plan.md` against the slice; `wc -l`
      against the cap of 50.
  A declared shape that does not equal the measured shape is a STOP.

D added-line reconciliation for C2
  `git show -U0 <C2> -- .agent/live_review.md`: every ADDED line appears in
  some TO, every REMOVED line is a FROM. Both stray counts must be 0.

E marker leakage
  `^<<<` line count is 0 in all three written targets — `.agent/live_review.md`,
  `.agent/plan.md`, `.agent/handoff.md`. Report the number, not the word.

F state-file contracts
  `python3 -m pytest tests/docs/ -q` and
  `python3 -m pytest tests/ui_server/test_dashboard_contract.py -q`.
  `.agent/plan.md` keeps `## Goal` and a `Steps` substring;
  `.agent/live_review.md` keeps its `## Steps` heading.

G no production drift
  `git diff --name-only 25e6326a..HEAD` lists ONLY paths under `.agent/`.
  Report the list. Nothing under `packages/`, `apps/`, `tests/` or `docs/`.

H canary
  `python3 -m pytest tests/cli/test_golden_path.py -q`.

I hygiene
  `git status --porcelain` empty at handback; `git worktree list` shows the
  primary ALONE; per-commit insertions each under 500 via `git show --numstat`.

No mutation red-proof is ordered for this round and none is to be run: nothing
executable changes, so there is no branch to mutate (D8 item 5, DECISION
F105 D10).

Handback: completion report + rewrite `.agent/handoff.md` (changed-files table,
item-status table for C1a/C1b/C2/C3, the gate table with real exit codes, the
transport and pair proofs, open-findings count, next expected action — which is
"gate R38, then run R39 per the plan's Next Steps"). Then `git push`. No PR —
one is created at CLOSURE.
──────────────────────────────────────────────────────────────
