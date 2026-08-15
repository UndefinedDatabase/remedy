# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0440. Open findings: sixty-seven — the thirty-two carried from F077, plus
R-0403 to R-0439 registered on this branch, less R-0435 and R-0436 resolved at
R20. `.agent/live_review.md` is the source of truth; this file mirrors it.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R20 records the R19 PASS verdict, registers R-0438 and R-0439 — both reviewer
block defects — converts R-0435 and R-0436 from `Landed:` to reviewer-authored
`Done:`, and rules at DECISION F082 D11 that the integration gate is R21 and
closure R22. It changes no code and no test.

## Next Steps
1. R21 the integration gate, per docs/agents/integration_gate.md.
2. R22 closure: STATUS line, Built State, closure candidates, the PR.

## Risks
- All three DONE conditions are now MEASURED by the suite, not argued: R19's
  two new properties cover green-on-fixtures and the degraded-run warning, and
  the history property already covered survival across runs. Closure states
  they were measured under DOUBLES, never under a live provider.
- The delivered order set is three, not the Design's five (R-0411), the freeze
  holds against a file-side edit only (R-0410), and the builder's model stays
  unobservable — closure states all three absences rather than implying five
  orders and three recorded roles.
- `wall_s` is clock-derived and every row's `cost` is `None` under doubles, so
  pass rate is the only trend a real run can prove; the R19 warning property is
  scoped to `pass_drop` for exactly that reason.
- Reviewer defects remain the dominant finding class: the standing
  counter-measures binding every block are R-0417 through R-0439, stated as a
  range and deliberately WITHOUT a count (R-0436).
