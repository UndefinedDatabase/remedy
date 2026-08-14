# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0408. Open findings: thirty-seven — the thirty-two carried from F077,
R-0403 at the claim, R-0404 at the R1 gate, and R-0405 to R-0407 at the R2
gate. `.agent/live_review.md` is the source of truth; this file mirrors it.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R3: the R2 gate recorded, R-0405 to R-0407 and DECISION F082 D1 registered,
`measure_tokens` repaired, and the bench record schema built as a pure
function over what a gauntlet run already produces.

## Next Steps
1. R4 — T001 finished: the five frozen order files with per-order version
   tags, the validation that a changed order without a bump FAILS, and the
   dry run against recorded fixture evidence.
2. R5 — T002: history append, trend computation, the regression rules and the
   improving, flat and degrading goldens.
3. R6 — T003: the `stats bench` CLI, model-context recording and a
   fake-provider bench run end to end.
4. R7 the integration gate, R8 closure.

## Risks
- `series` and `repair_rounds` have no source in the harness (R2 Q2, Q7).
  Both are recorded as explicitly-unmeasured rather than invented; a zero
  standing in for an unknown is the R-0178 mistake R-0407 just registered.
- Thirty-seven open findings is the largest carry any feature has started with.
