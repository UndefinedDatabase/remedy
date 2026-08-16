# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0478. `.agent/live_review.md` is the source of
truth for the open set; this file repeats no count of it.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure fails
the right stage with a readable summary, and runtime stays within a budget.

## Current Step
None in flight. R15 is committed: every stage carries a measured `timeout_sec`,
the runner is handed that budget per call, and `standard` is no longer killed at
the runner's 600-second default. R15 did the timeout ONLY — DECISION F083 D3 in
`.agent/live_review.md` moved the other three items to R16 and gives the reason.

## Next Steps
1. R16 takes the three items D3 deferred: the `budgets` STAGE T2_F083's Design
   asks for, which is a stage that checks documented ceilings and runs the guard
   tests and does not yet exist; a ruling on R-0468 from the 26-error ruff
   baseline `## Q10` records; and the determinism stage's shape settled as a
   DECISION. It is a SPLIT round: the budgets stage is production code.

## Risks
- A per-stage `timeout_sec` is a kill threshold, NOT the budgets stage; reading
  R15 as the stage would close F083 with a Design item unbuilt.
- The determinism suite is already wholly inside `standard` (850 ids, 0 outside,
  measured at R11), so a determinism stage duplicates work unless `standard`'s
  expression is narrowed in the same change.
