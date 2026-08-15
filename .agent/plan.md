# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. Next free finding id: R-0448. Open findings: seventy-five — the
thirty-two carried from F077, plus R-0403 to R-0447 registered on this branch,
less R-0435 and R-0436 resolved at R20. `.agent/live_review.md` is the source of
truth; this file mirrors it.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning. All three conditions are measured by the suite.

## Current Step
R23 is CLOSURE: it records the R22 PASS, registers R-0446 and R-0447, repairs
the self-contradicting round map R-0447 reports, then runs the closure algorithm
— the evidence job, a fresh review zip, the STATUS line claiming `[x]`, the
README count and Tier-2 row, `.agent/candidates.md`, and the PR.

## Next Steps
1. Nothing on this branch. The PR is NOT merged this session; it merges at the
   next feature's start via the AGENTS.md Open PR Gate, which is the operator's
   manual-review window.
2. The next feature is F083 — CI self-check, per Rule A5. A fresh session claims
   it and its first reviewed round registers or resolves every entry in
   `.agent/candidates.md`.

## Risks
- Closure is PASS_WITH_RISKS, not PASS: seventy-five findings are open, all
  Medium or Low, none a Blocker or High under either parse reading (R-0446).
- Three carried defects are open against process docs rather than against F082
  code: R-0445 (integration_gate.md manufactures eight false base failures on
  every run), R-0444 (a content digest cannot see an identical rebuild) and
  R-0403 (the review zip packages `.remedy-wt/`). None is repaired here; a
  process-doc fix inside a feature branch is scope drift.
- Every acceptance measurement was taken under DOUBLES, never a live provider;
  the delivered order set is three, not five (R-0411); the freeze holds against
  a file-side edit only (R-0410); the builder's model stays unobservable. The
  feature file's Built State states all four absences.
