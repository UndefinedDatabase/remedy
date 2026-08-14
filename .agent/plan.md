# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0427. Open findings: fifty-six — the thirty-two carried from F077, plus
R-0403 to R-0426 registered on this branch. `.agent/live_review.md` is the
source of truth for that ledger; this file mirrors it and nothing else.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R15 records the R14 gate, registers R-0423 to R-0426, and builds T003b's READ
half: the `models` map a run already writes into `run.json` becomes a defaulted
`BenchRecord` field that survives the history file. No gauntlet module is
touched and no additive ruling is needed — R-0426 corrects the plan claim that
one was.

## Next Steps
1. R16 — the fake-provider bench run end to end, clearing R11's Q6 four
   blockers: no entry point, local-Ollama reach, a `time.monotonic()` call in
   `::run_order`, and history resolving to the real data root; plus the Q7 pin
   for "the bench never runs implicitly".
2. R17 the integration gate, R18 closure.

## Risks
- "The bench never runs implicitly" is an ACCEPTANCE criterion that NO test
  pins (R11 Q7). It holds today only by absence: `append_bench_run` and
  `dry_run_from_order_set` have no caller under `apps/`, `packages/` or
  `scripts/`. An unpinned criterion at closure is a blocker, so R16 pins it.
- The builder's model stays unobservable: making it visible means reaching into
  `orchestrator_loop.py::execute_dispatched_job`. Closure states that absence
  rather than implying three roles were recorded.
- The delivered order set is three, not the Design's five (R-0411). Closure may
  not quote five, and DECISION F082 D3 binds the recovery to a bench-owned
  fixture rather than an edit to the gauntlet's template.
- The freeze holds against a file-side edit only (R-0410). The Built State
  states that threat model rather than quoting the criterion whole.
- Reviewer defects are the dominant finding class here and four more landed at
  R14. Nine standing counter-measures now bind every block: R-0417 staleness,
  R-0418 Fortschritt, R-0419 grep-every-writer, R-0420 measure-the-block,
  R-0421 count-the-list, R-0422 composite-property, R-0423 measure-the-slice,
  R-0424 count-your-own-contribution, R-0425 read-back-the-line-number.
