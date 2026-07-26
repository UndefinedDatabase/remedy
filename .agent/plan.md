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
- [x] Integration gate: branch vs base full-suite comparison, no F016
      regression (verdict persisted in .agent/live_review.md)
- [x] Closure: verdicts persisted, feature-file Built State written

## Current Step
Closure — integrity check, evidence job (T001–T003 attested), fresh review
zip, STATUS.md line, final commit, PR #150 description update. Do NOT merge:
the Open PR Gate handles that at the next feature start.

## Next Steps
None for F016 after closure.

## Risks
- Full suite is nondeterministic under xdist and pre-existing RED on base
  (~160-181 churning failures); serial re-runs pass. Backlog F135/F052.
- R-0142: redaction pattern false-positives on "sk-" substrings (Low, gap
  backlog) — branch-name artifact, vanishes on main.
- Cross-group merge-cycle interactions are caught only by the final
  whole-plan revalidation (coarse abort, fail-open) — by design.
