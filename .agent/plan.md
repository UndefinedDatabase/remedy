# Plan — F045 Loop definitions

Branch: feature/f045-loop-definitions, cut from main at cb3ef34f. No PR open;
nothing merged this round. Next free finding ID: R-0354. Open findings: 4
(R-0350, R-0351, R-0352, R-0353, all OPEN in `.agent/live_review.md`);
R-0344..R-0349 carry a `Done:` line as of R5. The 15 carried from F115 live in
git history at 57a24947.

## Goal
Recurring work gets a declarative, versionable form: a LOOP defines trigger,
scope, action, budget and stop rules in the project's config file, and
`remedy loop run` executes one as a completely normal job/mission with loop
provenance in evidence. DONE when a fixture loop validates, runs through the
standard pipeline unchanged, and an invalid spec fails validation with precise
messages before anything runs (docs/roadmap/features/T2_F045.md).

## Current Step
R5 reviewed PASS. The action dispatch is built: `run_loop` routes on
`action.kind` across the job and mission kinds, `_materialize_loop_job` is the
one place both paths build a loop's job, the inert trigger yields
`INERT_TRIGGER_NOTICE` instead of pretending it fired, and `last_run_for_loop`
reads the most recent run out of the job store. DECISION F045 D5 (`loop_ref`
rides on the JOB) is pinned by a test that goes red if provenance moves onto
the `Mission` record. R-0348 and R-0349 are resolved with `Done:` lines
verified against the disk. R-0350, R-0351, R-0352 and R-0353 are open: a
review finding the R4 block asserted without measuring, the two dispatch
defects the R5 review found, and the citation gap that halted R6 once.

## Next Steps
1. R7 fixes R-0351 and R-0352 FIRST — the persisted job must carry both the
   mission text and the caller's `root` before `_materialize_loop_job` saves.
2. Then the CLI: `remedy loop list`, `remedy loop validate`,
   `remedy loop run <name> [--yes]`, the last-run display, and the end-to-end
   fixture loop.
3. Then the integration gate, then closure per
   docs/roadmap/STATUS_closure_protocol.md.

## Risks
- Loops are parsed from a config file that does not exist in this repo (no
  ./remedy.toml). Every test builds its own tmp config path; nothing may
  depend on a repo-level config file appearing.
- Schedule and event triggers are parsed and validated but INERT until the
  scheduler feature. Running one must say so honestly, never silently behave
  like a manual trigger.
- The mission path persists jobs and missions through two different root
  resolutions until R-0352 is fixed, so no caller may rely on `root` isolating
  a whole run.

Fortschritt: ~60 % (T001 ✅ · T002 ✅ · T003 läuft) — Schätzung
