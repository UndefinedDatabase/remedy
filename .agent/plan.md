# Plan — F045 Loop definitions

Branch: feature/f045-loop-definitions, cut from main at cb3ef34f. No PR open;
nothing merged this round. Next free finding ID: R-0358. Open findings: 2 —
R-0350 and R-0354 — RECOMPUTED this round by the gate (b) command over
`.agent/live_review.md` (every `^- R-\d+ — ` paragraph minus every
`^Done: R-\d+ — ` line), never carried forward from the R14 block. That matches
what the block expected; no deviation to declare. R-0357 closed this round.

## Goal
Recurring work gets a declarative, versionable form: a LOOP defines trigger,
scope, action, budget and stop rules in the project's config file, and
`remedy loop run` executes one as a completely normal job/mission with loop
provenance in evidence. DONE when a fixture loop validates, runs through the
standard pipeline unchanged, and an invalid spec fails validation with precise
messages before anything runs (docs/roadmap/features/T2_F045.md).

## Current Step
T003 is COMPLETE. `test_a_fixture_loop_runs_end_to_end_and_its_report_names_the_loop`
drives the whole path once: a tmp-config `[[loop]]` materializes a job through
`run_loop`, that job goes through `run_cycles` with a fake provider and the
`task_step` seam, and the `report.md` written at the terminal state carries the
`- Loop: nightly-tidy` line. Terminal status OBSERVED at this gate, not ordered:
`all_green` after 3 cycles and 3 provider calls — `run_loop` already calls
`job_runner.plan_job`, so the job arrives with the planner's three fixed tasks
and the fixture adds none. The persisted job is read back with
`storage.load_job`, so the loop ref is proven on disk, not in memory.

## Next Steps
1. The integration gate (docs/agents/integration_gate.md).
2. Closure per docs/roadmap/STATUS_closure_protocol.md.
3. Then the two open findings, R-0350 and R-0354, if closure does not absorb them.

## Risks
- No ./remedy.toml exists in this repo; every test builds its own tmp config.
- Schedule and event triggers are validated but INERT until the scheduler
  feature. `loop run` says so off `LoopRunOutcome.notice`.
- `report_path` resolves through `jobs_dir()`, which reads REMEDY_DATA_DIR and
  honours no `root=`. Any future test touching the report MUST isolate through
  the environment; `root=` alone is not enough (R-0351/R-0352).
- `run_report` imports `loop_run` locally, inside the function. `loop_run` does
  not import `run_report`, so no cycle today; the other direction would make one.
- The end-to-end test pins `len(job.tasks) == 3`, which couples it to
  `job_runner._PLANNING_TASK_SPECS`. Changing that list breaks this test, by
  design — it is the observed value, named in a comment beside the assertion.
- This branch has carried no PR across several sessions; that call is the
  operator's and this session did not make it either way.

Fortschritt: ~80 % (T001 ✅ · T002 ✅ · T003 ✅) — Schätzung
