# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0465. Open findings: the seventy-five carried out
of the F082 record plus R-0448 to R-0464 registered on this branch, of which
R-0456 to R-0459 are resolved. `.agent/live_review.md` is the source of truth.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure fails
the right stage with a readable summary, and runtime stays within a budget.

## Current Step
R9 records the R8 FAIL, registers R-0463 and R-0464, repairs the ruff I001 the
reviewer's own CI-CMD slice shipped, and performs the §3 promotion R-0460 claimed
and R-0461 assigned here — the convention-paragraph rule becomes item 11 of the
pre-emission checklist. The CLI seam itself landed in R8 and is not re-opened.

## Next Steps
1. R10 adds the per-stage selection tests over a fixture tree that pin each
   stage's marker expression against files whose markers are known, and promotes
   R-0463's dry-run rule into §3 as checklist item 12.

## Risks
- `fast` still rests on a single 391.8 s reading, and the inventory showed it is
  inverted with respect to cost. Until that is measured under `-n auto`, no
  runtime budget can be written from measured data.
