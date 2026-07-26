# Plan — F016 Scaling task granularity

## Goal
Right-size Flight-Plan tasks automatically: split oversized tasks, merge
trivial neighbors, record every transformation on the plan. Pure heuristic
module (no cost history exists yet), wired at ONE point in plan generation,
failing open to the original plan.

## Checklist
- [x] Setup: Open PR Gate (#149 merged), branch, STATUS claim, state files
- [x] T001 split rules + config keys + table tests (gate green)
- [x] T002 merge rule + dependency-safety table tests (gate green)
- [x] T003 revalidation/abort + bypass + wiring into plan_job_llm +
      plan.md normalization section + mixed-fixture integration (gate green)

## Current Step
Push, open PR, hand back: completion report with per-commit changed-files
tables and raw verification transcripts, then rewrite .agent/handoff.md.

## Next Steps
Reviewer round on feature/f016-task-granularity.

## Risks
- Plan schema classes untouched (F014 R-0121); the record lives only in
  fp_dict["_normalization"] and FlightPlanResult.
- Merge overlap is token-based, so two files under a common directory count
  as related — over-eager merging is possible, and visible in the record.
