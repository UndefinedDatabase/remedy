# Plan — F045 Loop definitions

Branch: feature/f045-loop-definitions, cut from main at cb3ef34f. No PR open;
nothing merged this round. Next free finding ID: R-0350. Open findings: 2
(R-0348, R-0349, both OPEN in `.agent/live_review.md`); R-0344..R-0347 carry a
`Done:` line as of R4. The 15 carried from F115 live in git history at 57a24947.

## Goal
Recurring work gets a declarative, versionable form: a LOOP defines trigger,
scope, action, budget and stop rules in the project's config file, and
`remedy loop run` executes one as a completely normal job/mission with loop
provenance in evidence. DONE when a fixture loop validates, runs through the
standard pipeline unchanged, and an invalid spec fails validation with precise
messages before anything runs (docs/roadmap/features/T2_F045.md).

## Current Step
R4 done. R-0344 to R-0347 are resolved with `Done:` lines verified against the
disk; R-0348 and R-0349 — the two R3 block defects the R3 worker refused to
write — are registered. DECISION F045 D4 (`action.mission` is a goal TEMPLATE)
and D5 (`loop_ref` rides on the JOB, not on the Mission) are in
`.agent/decisions.md`, D5 with the rationale `mission_state.py` actually
supports. `loop_spec._semantic_errors` now validates `action.mission`'s
placeholders, pinned by two tests. `docs/agents/self_drive_protocol.md` gives
the STOP sentinel a re-check point inside the round loop.

## Next Steps
1. R5 = the dispatch: `run_loop`, the inert-trigger notice on the run path,
   the shared job builder both action kinds use, and `last_run_for_loop`.
2. R6 = the CLI: `remedy loop list`, `validate`, `run <name> [--yes]`, the
   last-run display, and the end-to-end fixture loop.
3. Then the integration gate, then closure.

## Risks
- Loops are parsed from a config file that does not exist in this repo (no
  ./remedy.toml). Every test builds its own tmp config path; nothing may
  depend on a repo-level config file appearing.
- Schedule and event triggers are parsed and validated but INERT until the
  scheduler feature. Running one must say so honestly, never silently behave
  like a manual trigger.
- The mission path lands in R5 and writes real mission records, so every test
  that touches it passes an explicit `root`.

Fortschritt: ~45 % (T001 ✅ · T002 ✅ · T003 läuft) — Schätzung
