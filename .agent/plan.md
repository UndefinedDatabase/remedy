# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0412. Open findings: forty-one — the thirty-two carried from F077, plus
R-0403 to R-0411 registered on this branch. `.agent/live_review.md` is the
source of truth for that ledger; this file mirrors it and nothing else.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R5 closes this session: the R4 gate recorded, R-0409 to R-0411 and DECISION
F082 D3 registered, the state mirrors re-synced, and the handoff written. No
code changed this round.

## Next Steps
1. A NEW session resumes at R6 — T001 closed: the dry run of
   `build_bench_record` against RECORDED fixture evidence, order file to row.
2. R7 — T002: history append under the data root's project area, trend
   computation, the regression rules, and the improving, flat and degrading
   goldens.
3. R8 — T003: the `stats bench` CLI, model-context recording, and a
   fake-provider bench run end to end.
4. R9 the integration gate, R10 closure.

## Risks
- The delivered order set is three, not the Design's five (R-0411). Closure
  may not quote five, and DECISION F082 D3 binds the recovery to a
  bench-owned fixture rather than an edit to the gauntlet's template.
- The freeze holds against a file-side edit only (R-0410). The Built State
  states that threat model rather than quoting the acceptance criterion whole.
