# Plan — F016 Scaling task granularity

## Goal
Right-size Flight-Plan tasks automatically: split oversized tasks, merge
trivial neighbors, record every transformation on the plan. Pure heuristic
module (no cost history exists yet), wired at ONE point in plan generation,
failing open to the original plan.

## Checklist
- [x] Setup: Open PR Gate (#149 merged), branch, STATUS claim, state files
- [x] T001 split rules + config keys + table tests (gate green)
- [ ] T002 merge rule + dependency-safety table tests
- [ ] T003 revalidation/abort + bypass + wiring into plan_job_llm +
      plan.md normalization section + mixed-fixture integration test

## Current Step
T002 — merge rule for consecutive small tasks (group cap, band bump,
external-dependency safety) in the same module + test file.

## Next Steps
T003 revalidation/abort, bypass, wiring into plan_job_llm, plan.md
normalization section, mixed-fixture integration + determinism tests.

## Risks
- Wiring touches two call sites (do_cmd.py ~241, ~2832); the record must be
  persisted as fp_dict["_normalization"] without touching plan schema classes
  (F014 R-0121: schema-size snapshot regression).
