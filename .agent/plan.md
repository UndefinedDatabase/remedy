# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0456. Open findings: the seventy-five carried out
of the F082 record plus R-0448 to R-0455 registered on this branch.
`.agent/live_review.md` is the source of truth; this file mirrors it.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure in
each stage fails the right stage with a readable summary, and total runtime
stays within a documented budget.

## Current Step
R4 records the R3 PASS, registers R-0455 — the round map and the two files that
name the next round disagreed about what R4 is — repairs that map, and lands
this feature's first code: `packages/orchestration/ci_stages.py`, the five stage
selections DECISION F083 D2 ruled, as data with no execution in it, plus the
structural guards in `tests/orchestration/test_ci_stages.py`.

## Next Steps
1. R5 wires the stage runner over `scripts/remedy_pytest_runner.py`, adds the
   `remedy ci` CLI seam Q8 names, and renders the summary table, which states
   the accepted `standard`/`smoke` double-run.
2. R6 measures each stage with and without `-n auto` and pins the per-stage
   setting from that reading (DECISION F083 D2.5), and adds the per-stage
   selection tests over a fixture tree rather than live collected counts.

## Risks
- Every finding registered on this branch so far is a defect in the reviewer's
  own block text, and R-0452 records that a counter-measure written as finding
  prose does not bind the next block. R-0455 is more of that same evidence.
- `fast` costs 391.8 s, measured once on one machine with an unrelated stale
  process present. The documented runtime budget the Goal requires cannot rest
  on a single reading, and no hosted runner exists yet to give a second one.
- The stage table carries no collected count on purpose. That keeps it from
  going stale, but it also means nothing yet proves a stage selects what R2
  measured; R6's fixture-tree tests are what close that gap.
