# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0453. Open findings: eighty — the seventy-five
carried out of the F082 record, plus R-0448 to R-0452 registered on this branch.
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
R2 is the T001 MARKER INVENTORY: it records the R1 PASS, registers R-0451 and
R-0452, rules DECISION F083 D1, and writes `.agent/f083_inventory.md` — which
markers exist and who assigns them, the collected count per marker, whether the
candidate stage selections cover the suite without overlapping, the measured
wall time per stage, and what the repository already provides that the stage
runner must reuse rather than copy. It builds no stage runner.

## Next Steps
1. R3 builds T001 — the stage runner, the marker selections and the summary
   table — over the shape R2's inventory settles, and no earlier.
2. The stage split is chosen from R2's measured data, not from the feature
   file's suggested shape, wherever the two disagree.

## Risks
- The feature file names a `live-provider` marker; the reviewer's own grep of
  `pyproject.toml` found the live-provider role carried by `real_ollama` and no
  marker of that name. R2 settles the naming in writing before R3 depends on it.
- Five of the six findings registered on this branch are defects in the
  reviewer's own block text, and R-0452 records that a counter-measure written
  as finding prose does not bind the next block. Whether the pre-emission
  checklist change holds is measurable only in later rounds.
- Measuring stage wall time means running most of the suite. DECISION F083 D1
  rules that a red stage is data for the inventory rather than a round blocker,
  so the round can complete over a repository that is red for unrelated reasons.
