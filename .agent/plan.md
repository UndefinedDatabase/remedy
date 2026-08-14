# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0414. Open findings: forty-three — the thirty-two carried from F077, plus
R-0403 to R-0413 registered on this branch. `.agent/live_review.md` is the
source of truth for that ledger; this file mirrors it and nothing else.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R6 records the R5 gate, registers R-0412 and R-0413, retires the two superseded
regions of `.agent/context.md`, and closes T001 with `bench_dry_run.py` — the
join from a frozen order file to a bench row over RECORDED fixture evidence.

## Next Steps
1. R7 — T002: history append under the data root's project area, trend
   computation, the regression rules, and the improving, flat and degrading
   goldens.
2. R8 — T003: the `stats bench` CLI, model-context recording, and a
   fake-provider bench run end to end.
3. R9 the integration gate, R10 closure.

## Risks
- The delivered order set is three, not the Design's five (R-0411). Closure
  may not quote five, and DECISION F082 D3 binds the recovery to a
  bench-owned fixture rather than an edit to the gauntlet's template.
- The freeze holds against a file-side edit only (R-0410). The Built State
  states that threat model rather than quoting the acceptance criterion whole.
