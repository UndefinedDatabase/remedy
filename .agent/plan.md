# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0470. Open findings: the seventy-five carried out
of the F082 record plus R-0448 to R-0469 registered on this branch, of which
R-0456 to R-0459 and R-0467 are resolved. `.agent/live_review.md` is the source
of truth.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure fails
the right stage with a readable summary, and runtime stays within a budget.

## Current Step
R11 records the R10 PASS, registers R-0468 and R-0469, and measures every stage
serially and under `-n auto` into `.agent/f083_inventory.md` Q5, so the budget
stage can be written from data. It lands no stage and no production code.

## Next Steps
1. R12 writes the determinism and budget stages from the Q5 readings, decides
   the determinism stage's shape as a recorded DECISION, and rules on R-0468.

## Risks
- The determinism stage has no marker of its own and the run-manifest suite is
  auto-marked `integration`, so it may already sit wholly inside `standard`.
  Q5 gate 9 measures that; until it is measured, no stage shape is chosen.
