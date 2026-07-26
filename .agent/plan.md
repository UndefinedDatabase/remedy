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
Integration gate RUN, handed back BLOCKED by the literal rule: the
base-vs-branch new-failure list is non-empty (10 ids). Second branch run
reproduces none of them and adds 6 others → suite nondeterminism under
`-n auto`. One real item recorded as an R-0142 candidate (branch NAME
`task-granularity` matches the `sk-` secret pattern). No repair this
round, per the round constraint.

## Next Steps
Await reviewer decision: accept F016 and track R-0142 separately, or
order a stabilization round.

## Risks
- Plan schema classes untouched (F014 R-0121); the record lives only in
  fp_dict["_normalization"] and FlightPlanResult.
- Merge overlap is token-based, so two files under a common directory count
  as related — over-eager merging is possible, and visible in the record.
