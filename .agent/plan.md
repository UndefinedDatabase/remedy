# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0482. `.agent/live_review.md` is the source of
truth for the open set; this file repeats no count of it.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure fails
the right stage with a readable summary, and runtime stays within a budget.

## Current Step
None in flight. R15 is closed PASS: every stage carries a measured `timeout_sec`,
the runner is handed that budget per call, and `standard` is no longer killed at
the runner's 600-second default. R16-REC is closed PASS and recorded it. This
repair round, R17, registered R-0481 and rewrote this file; it ends the session.
Round numbering, ruled at R-0481: 16 is spent by the record round and 17 by this
one, so the next engineering round is R18. R18 has not started.

## Next Steps
1. R18 takes the three items DECISION F083 D3 deferred: the `budgets` STAGE
   T2_F083's Design asks for, which checks documented ceilings and runs the guard
   tests and does not yet exist; a ruling on R-0468 from the 26-error ruff
   baseline `## Q10` records; and the determinism stage's shape settled as a
   DECISION. It is a SPLIT round — the budgets stage is production code — and its
   gates must honour R-0478, R-0479 and R-0480.

## Risks
- A per-stage `timeout_sec` is a kill threshold, NOT the budgets stage; reading
  R15 as the stage would close F083 with a Design item unbuilt.
- The determinism suite is already wholly inside `standard` (850 ids, 0 outside,
  measured at R11), so a determinism stage duplicates work unless `standard`'s
  expression is narrowed in the same change.
- A budgets stage that runs the integrity gate or a repo-wide lint count while
  other stages execute against the same checkout will read a clean repository as
  dirty (R-0479). Sequence it, or it reports a failure that is not there.
- The `ui` stage is RED on a clean checkout with a cold npx cache (R-0480), so
  the Acceptance line "clean checkout: green" is not met today. R18 rules on it.
