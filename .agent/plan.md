# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0431. Open findings: sixty — the thirty-two carried from F077, plus R-0403
to R-0430 registered on this branch. `.agent/live_review.md` is the source of
truth for that ledger; this file mirrors it and nothing else.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R17 records the R16 gate, registers R-0429 and R-0430, and lands the
fake-provider bench run: a new `packages/orchestration/bench_run.py` joining the
frozen order set to a campaign, its evidence to rows, and the rows to a history
file, with both roots required rather than defaulted. It spends the D9
allowlist's one name and repairs R-0427.

## Next Steps
1. R18 the integration gate: the bench green on fixtures across two runs with
   history surviving, and a deliberately degraded run raising the regression
   warning — the Goal's three DONE conditions, measured together.
2. R19 closure: STATUS line, Built State, closure candidates, the PR.

## Risks
- The delivered order set is three, not the Design's five (R-0411). Closure may
  not quote five, and DECISION F082 D3 binds the recovery to a bench-owned
  fixture rather than an edit to the gauntlet's template.
- The freeze holds against a file-side edit only (R-0410). The Built State
  states that threat model rather than quoting the criterion whole.
- The builder's model stays unobservable: making it visible means reaching into
  `orchestrator_loop.py::execute_dispatched_job`. Closure states that absence
  rather than implying three roles were recorded.
- `wall_s` is clock-derived from `gauntlet_runner.py::run_order`, not a bench
  clock. Closure states that rather than implying the bench measures time.
- Reviewer defects remain the dominant finding class. Thirteen standing
  counter-measures now bind every block: R-0417 staleness, R-0418 Fortschritt,
  R-0419 grep-every-writer, R-0420 measure-the-block, R-0421 count-the-list,
  R-0422 composite-property, R-0423 measure-the-slice, R-0424
  count-your-own-contribution, R-0425 read-back-the-line-number, R-0427
  name-the-quantified-set, R-0428 re-derive-the-base-at-delegation, R-0429
  resolve-your-own-ordinals, R-0430 state-the-numeral-in-the-handoff.
