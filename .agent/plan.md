# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0409. Open findings: thirty-eight — the thirty-two carried from F077,
R-0403 at the claim, R-0404 at the R1 gate, R-0405 to R-0407 at the R2 gate,
and R-0408 at the R3 gate. `.agent/live_review.md` is the source of truth.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R4: the R3 gate recorded, R-0408 and DECISION F082 D2 registered, the sample
project surveyed, and the five frozen orders built behind a freeze that binds
each order's version to its digest.

## Next Steps
1. R5 — T001 closed: the dry run of `build_bench_record` against RECORDED
   fixture evidence, end to end from an order file to a row.
2. R6 — T002: history append, trend computation, the regression rules and the
   improving, flat and degrading goldens.
3. R7 — T003: the `stats bench` CLI, model-context recording and a
   fake-provider bench run end to end.
4. R8 the integration gate, R9 closure.

## Risks
- The five capabilities the feature file names may not all be expressible
  against the existing sample project. C2 surveys it FIRST and stops rather
  than inventing an order that cannot run — an unrunnable frozen order is
  worse than a missing one, because the freeze makes it permanent.
- Thirty-eight open findings is the largest carry any feature has started with.
