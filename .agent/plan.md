# Plan — F045 Loop definitions

Branch: feature/f045-loop-definitions, cut from main at cb3ef34f. No PR open;
nothing merged this round. Next free finding ID: R-0358. Open findings: 3 —
R-0350, R-0354 and R-0357 — RECOMPUTED this round from `.agent/live_review.md`
by the gate (b) command (every `^- R-\d+ — ` paragraph minus every
`^Done: R-\d+ — ` line), never carried forward from the R13 block. R-0357 was
registered this round on the R12 inventory's terminal citation.

## Goal
Recurring work gets a declarative, versionable form: a LOOP defines trigger,
scope, action, budget and stop rules in the project's config file, and
`remedy loop run` executes one as a completely normal job/mission with loop
provenance in evidence. DONE when a fixture loop validates, runs through the
standard pipeline unchanged, and an invalid spec fails validation with precise
messages before anything runs (docs/roadmap/features/T2_F045.md).

## Current Step
R13, the report half of the Acceptance line. `ReportSources` now carries
`loop_ref`, `collect_report_sources` reads it under
`loop_run.LOOP_REF_METADATA_KEY` (imported, never retyped), and `_header_lines`
emits `- Loop: <name>` directly after `- Mission: …` — conditionally, so the
three goldens stay byte-identical (71 passed; 0 deletions in the test file's
numstat). Because `report_path` puts `report.md` INSIDE `job_evidence_dir`,
that one line covers evidence and report at once. Still missing: an end-to-end
run that drives a loop job through `run_cycles` and reads the written file.

## Next Steps
1. R14: the end-to-end fixture loop driving `run_cycles` — a loop materializes
   a job, the job runs to a terminal state through `_apply_terminal`, and the
   written `report.md` on disk carries the loop line.
2. The integration gate (docs/agents/integration_gate.md).
3. Closure per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- No ./remedy.toml exists in this repo; every test builds its own tmp config.
- Schedule and event triggers are validated but INERT until the scheduler
  feature. `loop run` says so off `LoopRunOutcome.notice`.
- `loop run` writes to the REAL job store unless given `root`, so every test
  isolates through `REMEDY_DATA_DIR` or an explicit root.
- `run_report` now imports `loop_run` locally, inside the function. `loop_run`
  does not import `run_report`, so no cycle today; an import in the other
  direction would create one.
- R14 must pick its pipeline: `run_cycles` writes the report this change
  touches, `run_job_fulfill` discards the loop's plan (inventory Q1).
- This branch has carried no PR across several sessions; that call is the
  operator's and this session did not make it either way.

Fortschritt: ~72 % (T001 ✅ · T002 ✅ · T003 läuft) — Schätzung
