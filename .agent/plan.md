# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0463. Open findings: the seventy-five carried out
of the F082 record plus R-0448 to R-0462 registered on this branch, of which
R-0456 to R-0459 are resolved. `.agent/live_review.md` is the source of truth.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure fails
the right stage with a readable summary, and runtime stays within a budget.

## Current Step
R8 records the R7 PASS, registers R-0461 and R-0462, and lands the T001 CLI seam:
the `ci` catalog group and `ci.run` entry, `apps/cli/commands/ci_cmd.py` with its
summary table, the wiring into `collect_all_handlers`, and `tests/cli/test_ci_cmd.py`
— whose last test really launches a stage argv through the pytest runner script.

## Next Steps
1. R9 promotes R-0460's rule into the §3 pre-emission checklist as item 11
   (finding R-0461, its first item), then adds the per-stage selection tests over
   a fixture tree that pin each stage's marker expression against known markers.

## Risks
- `fast` still rests on a single 391.8 s reading, and the inventory showed it is
  inverted with respect to cost. Until that is measured under `-n auto`, no
  runtime budget can be written from measured data.
