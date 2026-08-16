# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0475. Open findings: the seventy-five carried out
of the F082 record plus R-0448 to R-0474 registered on this branch, of which
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
R13 records the R12 PASS, registers R-0474, and measures the SERIAL cost of every
CI stage three times through the production `run_ci_stage` instrument, because
`remedy ci` passes no `-n auto` and every reading in `## Q9` therefore describes a
run the command does not perform. It writes no ceiling and no production code.

## Next Steps
1. R14 writes the budget and determinism stages from the `## Q10` samples, never
   from the `-n auto` readings in `## Q9`. R-0473 binds the ceiling to the
   observed spread with its headroom stated, or to a budget that says on its face
   how many samples it rests on. R14 also rules on R-0468 from the ruff baseline
   `## Q10` records, and settles the determinism stage's shape as a DECISION.

## Risks
- The determinism suite is already wholly inside `standard` — 850 ids, 0 outside,
  measured at R11 — so a determinism stage would duplicate work unless
  `standard`'s expression is narrowed in the same change.
- `scripts/remedy_pytest_runner.py` defaults `REMEDY_PYTEST_TIMEOUT_SEC` to 600
  and returns 124 on a kill. `standard` collects 12579 items and has never been
  run serially, so today's `remedy ci` may already truncate its largest stage.
  R13 measures it; until then the outcome is unknown, not assumed.
- 26 ruff errors stand repo-wide (R-0468) and no stage lints. A lint ceiling
  arrives red unless the baseline is recorded first, which `## Q10` does.
