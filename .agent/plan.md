# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0423. Open findings: fifty-two — the thirty-two carried from F077, plus
R-0403 to R-0422 registered on this branch. `.agent/live_review.md` is the
source of truth for that ledger; this file mirrors it and nothing else.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R14 records the R13 gate and registers R-0420, R-0421 and R-0422 — a block over
its line cap, a numeral that contradicted its own enumeration, and a gate that
could not be satisfied as written. All three charge the reviewer; the worker
found two of them. It writes no code.

## Next Steps
1. R15 — T003b the read half and the run: carry `models` from
   `gauntlet_evidence.py::RunEvidence` into the bench record, which needs its
   own additive ruling because that is a third gauntlet module; then the
   fake-provider bench run, clearing R11's Q6 four blockers — no entry point,
   local-Ollama reach, a `time.monotonic()` call in `::run_order`, and history
   resolving to the real data root; and the Q7 pin for "the bench never runs
   implicitly".
2. R16 the integration gate, R17 closure.

## Risks
- "The bench never runs implicitly" is an ACCEPTANCE criterion that NO test
  pins (R11 Q7). It holds today only by absence: `append_bench_run` and
  `dry_run_from_order_set` have no caller under `apps/`, `packages/` or
  `scripts/`. An unpinned criterion found at closure is a closure blocker, so
  R15 pins it.
- The builder's model stays unobservable, because making it visible means
  reaching into `orchestrator_loop.py::execute_dispatched_job`. Closure states
  that absence rather than implying three roles were recorded.
- The delivered order set is three, not the Design's five (R-0411). Closure
  may not quote five, and DECISION F082 D3 binds the recovery to a
  bench-owned fixture rather than an edit to the gauntlet's template.
- The freeze holds against a file-side edit only (R-0410). The Built State
  states that threat model rather than quoting the acceptance criterion whole.
- Reviewer-block defects are the dominant finding class on this branch, and
  three more landed at R13. No count of the class is stated here because none
  has been taken. The counter-measures now standing are R-0417's staleness
  gate, R-0418's Fortschritt rule, R-0419's grep-every-writer rule, R-0420's
  measure-the-block rule, R-0421's count-the-list rule and R-0422's
  composite-property rule, and all six bind every block from here.
