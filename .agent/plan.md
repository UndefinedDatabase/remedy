# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0436. Open findings: sixty-five — the thirty-two carried from F077, plus
R-0403 to R-0435 registered on this branch. `.agent/live_review.md` is the
source of truth for that ledger; this file mirrors it and nothing else.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R18 registers R-0434 and R-0435, rules the remaining round map at DECISION F082
D10, and repairs four defects: R-0431's self-contradicting context bullet, the
four stale pin sentences of R-0432 and R-0434, and R-0433's `Any` annotations. It
lands no capability and writes no test.

## Next Steps
1. R19 the acceptance proof for R-0435: the doubles store a DoD verdict, so a
   bench row can PASS, and three properties measure the Goal's three DONE
   conditions over real runs.
2. R20 the integration gate, per docs/agents/integration_gate.md.
3. R21 closure: STATUS line, Built State, closure candidates, the PR.

## Risks
- R-0435 is the closure blocker of record: until R19 lands, NO round may claim
  the bench runs green on fixtures or that a degraded run warns.
- The delivered order set is three, not the Design's five (R-0411), the freeze
  holds against a file-side edit only (R-0410), and the builder's model stays
  unobservable — closure states all three absences rather than implying five
  orders and three recorded roles.
- `wall_s` is clock-derived from `gauntlet_runner.py::run_order` and every row's
  `cost` is `None` under doubles, so pass rate is the only trend a real run can
  prove; cost and wall warnings stay golden-pinned.
- Reviewer defects remain the dominant finding class: fifteen standing
  counter-measures now bind every block, R-0417 through R-0435.
