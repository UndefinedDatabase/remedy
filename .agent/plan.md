# Plan — F045 Loop definitions

Branch: feature/f045-loop-definitions, cut from main at cb3ef34f. No PR open;
nothing merged this round. Next free finding ID: R-0356. Open findings: 4 —
R-0350, R-0353, R-0354 and R-0355, each named explicitly rather than by
position (R-0354's counter-measure) and each still carrying `OPEN.` with no
`Done:` line in `.agent/live_review.md`. R-0344..R-0349, R-0351 and R-0352 are
resolved there. The 15 carried from F115 live in git history at 57a24947.

## Goal
Recurring work gets a declarative, versionable form: a LOOP defines trigger,
scope, action, budget and stop rules in the project's config file, and
`remedy loop run` executes one as a completely normal job/mission with loop
provenance in evidence. DONE when a fixture loop validates, runs through the
standard pipeline unchanged, and an invalid spec fails validation with precise
messages before anything runs (docs/roadmap/features/T2_F045.md).

## Current Step
R9, a REPAIR round: the reviewer FAILED R8 on one defect, now registered as
R-0355 and fixed. `remedy loop list` printed `loop_spec.INERT_TRIGGER_NOTICE`
("scheduler not yet available; ran on demand") as a legend, so a row reading
`last run: never` was followed one line later by a claim that the loop ran.
The listing now has its own `INERT_TRIGGER_LEGEND` in
`apps/cli/commands/loop_cmd.py`, saying only what a listing can know: the
trigger cannot fire until the scheduler exists, so such a loop has to be run
manually. `INERT_TRIGGER_NOTICE` is untouched and stays `remedy loop run`'s to
display off `LoopRunOutcome.notice`. The test pins both directions — the legend
appears, and the run notice appears NOWHERE in a listing. The rest of R8
(wiring, catalog, validate, last-run display) was verified correct, not reopened.

## Next Steps
1. R10 is `remedy loop run <name> [--yes]`, where `INERT_TRIGGER_NOTICE` is
   displayed for real off `LoopRunOutcome.notice`, plus the end-to-end fixture
   loop through the fake-provider pipeline.
2. Then the integration gate.
3. Then closure per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- Loops are parsed from a config file that does not exist in this repo (no
  ./remedy.toml). Every test builds its own tmp config path; nothing may
  depend on a repo-level config file appearing.
- Schedule and event triggers are parsed and validated but INERT until the
  scheduler feature. Running one must say so honestly, never silently behave
  like a manual trigger.
- The CLI's read-only half is landed but `loop run` is not, so no
  operator-visible path yet exercises the loop_ref provenance end to end.

Fortschritt: ~60 % (T001 ✅ · T002 ✅ · T003 läuft) — Schätzung
