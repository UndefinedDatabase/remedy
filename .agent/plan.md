# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0451. Open findings: seventy-eight — the
seventy-five carried out of the F082 record, plus R-0448, R-0449 and R-0450
registered at R1. `.agent/live_review.md` is the source of truth; this file
mirrors it.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure in
each stage fails the right stage with a readable summary, and total runtime
stays within a documented budget.

## Current Step
R1 is the CLAIM: cut the branch, reset the live review record carrying F082's
open set forward, register the three F082 closure-review candidates as R-0448,
R-0449 and R-0450, refresh the candidates carrier, and move the ledger line from
`[ ]` to `[~]`. No code and no test changes.

## Next Steps
1. R2 is the T001 marker inventory, which the feature file's orchestrator brief
   names as T001's first deliverable: collected count and wall time per marker,
   which markers already exist, and which stage each belongs to.
2. The stage split follows that data. No stage runner is written before it.

## Risks
- The three findings registered this round are all defects in the reviewer's own
  block text, and two of them, R-0449 and R-0450, are recurrences of R-0371 in
  the round that registered it. The counter-measures are written as standing
  rules inside the findings; whether they hold is measurable only in later rounds.
- R-0448's repair edits `docs/roadmap/STATUS_closure_protocol.md`, a process doc
  F083 does not own, so it joins R-0403, R-0444 and R-0445 on the paydown queue.
  That queue has no owner yet and grows by one this round.
- R-0205 is carried into this feature by its own feature file: live-state
  contract tests can turn main red for reasons unrelated to the change under
  review. It is in scope here rather than deferred.
