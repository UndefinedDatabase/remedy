# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0438. Open findings: sixty-seven — the thirty-two carried from F077, plus
R-0403 to R-0437 registered on this branch. `.agent/live_review.md` is the
source of truth for that ledger; this file mirrors it and nothing else.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R19 repairs R-0435: the mission double stores a real `GateResult` through
`dod_gate.py::save_gate_result` inside the run's isolated root, so a bench row
can PASS, and two new properties assert what the rows SAY — every row passes on
a clean fixture run, and a run with one order's verdict HELD produces exactly
one `pass_drop` warning. It also repairs R-0436's numeral here. It changes no
production code.

## Next Steps
1. R20 the integration gate, per docs/agents/integration_gate.md.
2. R21 closure: STATUS line, Built State, closure candidates, the PR.

## Risks
- Until R19 is GATED, no round may claim the bench runs green on fixtures: the
  claim is what R-0435 is about, and a worker's green is not a verdict.
- The delivered order set is three, not the Design's five (R-0411), the freeze
  holds against a file-side edit only (R-0410), and the builder's model stays
  unobservable — closure states all three absences rather than implying five
  orders and three recorded roles.
- `wall_s` is clock-derived from `gauntlet_runner.py::run_order` and every row's
  `cost` is `None` under doubles, so pass rate is the only trend a real run can
  prove; cost and wall warnings stay golden-pinned.
- Reviewer defects remain the dominant finding class: the standing
  counter-measures binding every block are R-0417 through R-0437, stated as a
  range and deliberately WITHOUT a count (R-0436).
