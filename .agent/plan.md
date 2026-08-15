# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0474. Open findings: the seventy-five carried out
of the F082 record plus R-0448 to R-0473 registered on this branch, of which
R-0456 to R-0459, R-0467 and R-0472 are resolved. `.agent/live_review.md` is the
source of truth.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure fails
the right stage with a readable summary, and runtime stays within a budget.

## Current Step
R12 records the R11 PASS, registers R-0470 to R-0473, and repairs the heading
collision R11 introduced by renaming the appended inventory section to `## Q9`.
It lands no stage and no production code.

## Next Steps
1. R13 writes the determinism and budget stages from the `## Q9` readings, under
   R-0473: at least three samples per stage that carries a ceiling, or a budget
   that states on its face how many samples it rests on. It also rules on R-0468.

## Risks
- The determinism suite is already wholly inside `standard` — 850 ids, 0 outside,
  measured at R11 — so a determinism stage would duplicate work unless
  `standard`'s expression is narrowed in the same change. Decide it as a DECISION.
- 26 ruff errors stand repo-wide (R-0468) and no stage lints. A lint ceiling in
  the budget stage arrives red unless the baseline is recorded first.
