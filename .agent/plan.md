# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0405. Open findings: thirty-four — the thirty-two carried from F077, plus
R-0403 registered at the claim and R-0404 registered at the R1 gate.
`.agent/live_review.md` is the source of truth for that ledger; this file
mirrors it and nothing else.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R2: the R1 gate is recorded, R-0404 registered, and the T001 gauntlet-harness
inventory is written read-only into `.agent/f082_inventory.md`.

## Next Steps
1. R3 — T001: the factoring the inventory justifies, the five frozen orders
   with their version tags, the record schema, and a dry run against recorded
   fixture evidence. The gauntlet's own seven test files stay UNMODIFIED.
2. R4 — T002: history append, trend computation, the regression rules and the
   improving, flat and degrading goldens.
3. R5 — T003: the `stats bench` CLI, model-context recording and a
   fake-provider bench run end to end.
4. R6 the integration gate, R7 closure.

## Risks
- The factoring in T001 is the feature file's own named risk. R2 answers what
  may move before anything moves; an answer of "cannot move without editing a
  gauntlet test" is a finding against the plan, not a licence to edit the test.
- Thirty-four open findings is the largest carry any feature has started with.
