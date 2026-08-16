# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0489. `.agent/live_review.md` is the source of
truth for the open set; this file repeats no count of it.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure fails
the right stage with a readable summary, and runtime stays within a budget.

## Current Step
R23 is closed PASS and R24 recorded it. R-0486 is resolved: the CI note now puts
the TypeScript compile check in `standard`, the stage that selects it. R24
registered R-0488 — the replacement paragraph called the toolchain a precondition
of ONE test when `standard` selects eight toolchain-dependent node ids across two
files — and repaired it in the same round. T003 stays COMPLETE. No documentation
claim in this feature is now unverified against a collection.

## Next Steps
1. The integration-gate round: the full suite exactly once, per
   docs/agents/integration_gate.md. It is also the round that records R24's
   verdict and resolves R-0488. Budget it as a full round of its own: a branch run
   plus a base run in a throwaway worktree, roughly 23 minutes of suite each.
2. Then closure per docs/roadmap/STATUS_closure_protocol.md — evidence job plus a
   FRESH review zip, both mandatory, then the authored STATUS line and the PR.

## Risks
- Hosted wall time is still unmeasured, and the first hosted run is that
  measurement. `standard` needs 935.14 s at its slowest local sample against a
  2100 s budget, and it is also the stage carrying the toolchain-dependent tests.
- The lint ceiling is a RATCHET. Raising it to make a round green converts the
  one honest lint signal in this repository into decoration.
- R-0482 (a live `NameError` on a guard's refusal path) and R-0487
  (`docs/README.md` is never link-checked) are both frozen here and belong to a
  paydown branch: each is a code- or test-content fix this feature may not make.
