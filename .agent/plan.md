# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0455. Open findings: the seventy-five carried out
of the F082 record plus R-0448 to R-0454 registered on this branch.
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
R3 records the R2 PASS, registers R-0453 and R-0454, repairs the finding-count
sentence R-0453 reports, and rules DECISION F083 D2 — the stage set is Q4's five
selections; `safety` and `architecture` do not become stages; the eight-item
`standard`/`smoke` overlap is accepted and documented; `determinism` and
`budgets` are script invocations rather than marker selections. Per-stage
parallelism and the feature file's marker spellings are deferred, each with its
reason. It writes no code.

## Next Steps
1. R4 builds T001 over D2: the stage runner, the five marker selections, the
   summary table and its tests, plus the one measurement D2.5 defers — each
   stage timed with and without `-n auto`, and the per-stage setting pinned from
   that reading.
2. The CLI seam is the one Q8 names; the stage runner reuses the existing pytest
   subprocess runner rather than reimplementing it.

## Risks
- Every finding registered on this branch so far is a defect in the reviewer's
  own block text, and R-0452 records that a counter-measure written as finding
  prose does not bind the next block. R-0453 and R-0454 are the evidence that it
  still does not: both were registered one round after their own family's rule.
- `fast` costs 391.8 s, measured once on one machine with an unrelated stale
  process present. The documented runtime budget the Goal requires cannot rest
  on a single reading, and no hosted runner exists yet to give a second one.
- D2.3 accepts a double-run of eight tests to avoid editing marker semantics.
  If the summary table does not state it, the acceptance becomes a silent defect.
