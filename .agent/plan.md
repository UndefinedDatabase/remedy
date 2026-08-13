# Plan — F045 Loop definitions

Branch: feature/f045-loop-definitions, cut from main at cb3ef34f. No PR open;
nothing merged this round. Next free finding ID: R-0347. Open findings: 3 on
this branch (R-0344, R-0345, R-0346, all OPEN in `.agent/live_review.md`); the
15 carried from F115 live in git history at 57a24947.

## Goal
Recurring work gets a declarative, versionable form: a LOOP defines trigger,
scope, action, budget and stop rules in the project's config file, and
`remedy loop run` executes one as a completely normal job/mission with loop
provenance in evidence. DONE when a fixture loop validates, runs through the
standard pipeline unchanged, and an invalid spec fails validation with precise
messages before anything runs (docs/roadmap/features/T2_F045.md).

## Current Step
R2 done — the R1 block's three findings registered, DECISIONs F045 D1-D3
landed in `.agent/decisions.md`, and T002 built:
`packages/orchestration/loop_run.py` materializes a job-action loop as an
ordinary PLANNED job carrying `loop_ref` provenance, with
`tests/orchestration/test_loop_run.py` pinning the approval semantics.
R3 = T003.

## Next Steps
1. T003 — `remedy loop list | validate | run`, action dispatch (`run_loop`,
   including the mission path per DECISION F045 D3), last-run display from
   evidence, and an end-to-end fixture loop through the fake-provider pipeline.
2. Integration gate, then closure per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- Loops are parsed from a config file that does not exist in this repo (there
  is no ./remedy.toml). Every test therefore builds its own tmp config path;
  nothing may depend on a repo-level config file appearing.
- Schedule and event triggers are parsed and validated but INERT until the
  scheduler feature. Running one must say so honestly rather than silently
  behaving like a manual trigger.
- Action dispatch and the mission path deliberately do NOT exist yet:
  `loop_to_job` refuses any action kind other than `job` and both land in T003
  per DECISION F045 D3. Until then no caller may treat `loop_to_job` as the
  general loop entry point.

Fortschritt: ~35 % (T001 ✅ · T002 ✅ · T003 offen) — Schätzung
