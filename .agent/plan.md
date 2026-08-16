# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0477. Open findings: the seventy-five carried out
of the F082 record plus R-0448 to R-0476 registered on this branch, of which
R-0456 to R-0459, R-0467, R-0472 and R-0475 are resolved. `.agent/live_review.md`
is the source of truth.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure fails
the right stage with a readable summary, and runtime stays within a budget.

## Current Step
R14 records the R13 PASS, registers R-0475 and R-0476, and completes the
three-sample serial reading of `standard` that R13's single uncapped probe left
at one point, so R15's ceiling rests on a measured spread rather than on one
run. It writes no ceiling and no production code.

## Next Steps
1. R15 carries a per-stage timeout in the stage table and writes the budget stage
   from the `## Q11` spread, because today's `remedy ci` kills `standard` at the
   runner's 600-second default — measured at R13, three samples, exit 124 each.
   R15 also rules on R-0468 from the 26-error ruff baseline `## Q10` records, and
   settles the determinism stage's shape as a DECISION.

## Risks
- `remedy ci` cannot complete `standard` today: `scripts/remedy_pytest_runner.py`
  defaults `REMEDY_PYTEST_TIMEOUT_SEC` to 600 and the stage needs far longer
  serially. Raising that default repo-wide would change every other caller of the
  runner, so R15 carries the timeout on the stage instead. The figures are in
  `## Q11`; this file repeats none of them.
- The determinism suite is already wholly inside `standard` — 850 ids, 0 outside,
  measured at R11 — so a determinism stage would duplicate work unless
  `standard`'s expression is narrowed in the same change.
- 26 ruff errors stand repo-wide (R-0468) and no stage lints. A lint ceiling
  arrives red unless the baseline is recorded first, which `## Q10` does.
