# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0446. Open findings: seventy-three — the thirty-two carried from F077,
plus R-0403 to R-0445 registered on this branch, less R-0435 and R-0436
resolved at R20. `.agent/live_review.md` is the source of truth; this file
mirrors it.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R22 records the R21 integration-gate PASS, registers R-0443 to R-0445 — a
scratch-directory hazard, a parity gate blind to what it was ordered to detect,
and a standing defect in `docs/agents/integration_gate.md` — rules the closure
split at DECISION F082 D12, and rewrites the feature file's Built State section
so R23 starts from a settled closure precondition.

## Next Steps
1. R23 closure per docs/roadmap/STATUS_closure_protocol.md: the evidence job,
   a FRESH review zip, the STATUS line, the README count and Tier-2 row,
   `.agent/candidates.md`, and the PR.

## Risks
- The integration gate PASSED: zero branch-only failures, and the eight
  base-only failures are attributed to the environment class in both
  directions. Closure claims full-suite green on that evidence and on the
  reviewer's own run at c536123b, and on nothing else.
- Closure preconditions are met but not yet re-measured at the closure head:
  no Blocker or High finding is open (73 open, all Medium or Low) and the
  integrity gate passes today. R23 re-runs both rather than carrying them.
- The review zip is the closure BLOCKER of record — a failing build stops the
  closure, and R-0403 already records that the zip packages `.remedy-wt/`.
- Every acceptance measurement was taken under DOUBLES, never a live provider;
  the delivered order set is three, not five (R-0411); the freeze holds against
  a file-side edit only (R-0410); the builder's model stays unobservable.
  Closure states all four absences rather than implying otherwise.
- Reviewer and handback text defects remain the dominant finding class: the
  standing counter-measures binding every block are R-0417 through R-0445,
  stated as a range and deliberately WITHOUT a count (R-0436).
