# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0443. Open findings: seventy — the thirty-two carried from F077, plus
R-0403 to R-0442 registered on this branch, less R-0435 and R-0436 resolved at
R20. `.agent/live_review.md` is the source of truth; this file mirrors it.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R21 records the R20 PASS verdict, registers R-0440 to R-0442 — three text
defects, two the reviewer's and one the handback's — repairs the stale D10
citation in `.agent/context.md`, and runs the integration gate per
docs/agents/integration_gate.md: the full suite on the branch and at the merge
base 668d40f7, the comm compare, and per-id attribution for every branch-only
failure. It changes no code and no test.

## Next Steps
1. R22 closure: evidence job, FRESH review zip, the STATUS line, Built State,
   closure candidates, the PR.

## Risks
- The integration gate is the first full-suite run on this branch. A
  reproducible branch-only failure coupled to F082 code is a BLOCKER and its
  repair is its own reviewer-gated round, not a fix inside this one.
- All three DONE conditions are MEASURED by the suite, not argued, but they
  were measured under DOUBLES and never under a live provider; closure says so.
- The delivered order set is three, not the Design's five (R-0411), the freeze
  holds against a file-side edit only (R-0410), and the builder's model stays
  unobservable — closure states all three absences.
- `wall_s` is clock-derived and every row's `cost` is `None` under doubles, so
  pass rate is the only trend a real run can prove.
- Reviewer and handback text defects remain the dominant finding class: the
  standing counter-measures binding every block are R-0417 through R-0442,
  stated as a range and deliberately WITHOUT a count (R-0436).
