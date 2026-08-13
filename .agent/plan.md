# Plan — F045 Loop definitions

Branch: feature/f045-loop-definitions, cut from main at cb3ef34f. No PR was
open at the Open PR Gate — the F115 closure PR #195 and the amend0813 PR #196
were both already merged. Next free finding ID: R-0344. Open findings: 0 on
this branch; the 15 carried from F115 live in git history at 57a24947.

## Goal
Recurring work gets a declarative, versionable form: a LOOP defines trigger,
scope, action, budget and stop rules in the project's config file, and
`remedy loop run` executes one as a completely normal job/mission with loop
provenance in evidence. DONE when a fixture loop validates, runs through the
standard pipeline unchanged, and an invalid spec fails validation with precise
messages before anything runs (docs/roadmap/features/T2_F045.md).

## Current Step
R1 — claim, state reset and T001: the spec model, config loading and
validation in packages/orchestration/loop_spec.py plus its unit tests.

## Next Steps
1. T002 — run materialization, loop_ref provenance, approval-semantics tests
   (a loop never implies --yes; an explicit spec flag is audited like the CLI
   flag).
2. T003 — `remedy loop list | validate | run`, last-run display from evidence,
   and an end-to-end fixture loop through the fake-provider pipeline.
3. Integration gate, then closure per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- Loops are parsed from a config file that does not exist in this repo (there
  is no ./remedy.toml). Every test therefore builds its own tmp config path;
  nothing may depend on a repo-level config file appearing.
- Schedule and event triggers are parsed and validated but INERT until the
  scheduler feature. Running one must say so honestly rather than silently
  behaving like a manual trigger.

Fortschritt: ~5 % (R1 läuft · T001 offen · T002 offen · T003 offen) — Schätzung
