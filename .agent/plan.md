# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0486. `.agent/live_review.md` is the source of
truth for the open set; this file repeats no count of it.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure fails
the right stage with a readable summary, and runtime stays within a budget.

## Current Step
R21 is closed PASS and R22 recorded it. R22 registered R-0485 (Low, a deviation
recorded outside the handoff's Deviations section) and fixed it by rule, not by
rewriting R21: the handback template now requires any departure from the block's
commit sequence to appear there. T003 is COMPLETE — the workflow and its guards
landed at R21, the documentation and the measured runtime budgets at R22.

## Next Steps
1. The integration-gate round: the full suite exactly once, per
   docs/agents/integration_gate.md. It is also the round that records R22's
   verdict and resolves R-0485.
2. Then closure per docs/roadmap/STATUS_closure_protocol.md — evidence job plus a
   FRESH review zip, both mandatory, then the authored STATUS line and the PR.

## Risks
- Hosted wall time is still unmeasured, and the first hosted run is that
  measurement. `standard` needs 935.14 s at its slowest local sample against a
  2100 s budget; a runner with fewer cores may exceed it. Raising `timeout_sec`
  before that evidence exists would be a guess wearing a budget's name.
- The lint ceiling is a RATCHET. Raising it to make a round green converts the
  one honest lint signal in this repository into decoration.
- R-0482 is a live `NameError` on a guard's refusal path, frozen under that
  ceiling rather than fixed, and belongs to a branch of its own.
