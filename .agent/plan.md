# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0488. `.agent/live_review.md` is the source of
truth for the open set; this file repeats no count of it.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure fails
the right stage with a readable summary, and runtime stays within a budget.

## Current Step
R22 is closed FAIL and R23 recorded it. R22's commits are all correct and none is
rewritten; what failed was a claim in its new ist-doc that no gate covered — the
TypeScript compile check was attributed to the `ui` stage, and the code puts it in
`standard`. R23 registered that as R-0486 and repaired the document in the same
round, gated by a stage collection rather than by prose. R23 also registered
R-0487 — `docs/README.md` is never link-checked, a test-content defect this
feature may not fix — and routed it out. R-0485 is resolved. T003 stays COMPLETE.

## Next Steps
1. The integration-gate round: the full suite exactly once, per
   docs/agents/integration_gate.md. It is also the round that records R23's
   verdict and resolves R-0486. R-0487 stays open and is not resolved here.
2. Then closure per docs/roadmap/STATUS_closure_protocol.md — evidence job plus a
   FRESH review zip, both mandatory, then the authored STATUS line and the PR.

## Risks
- Hosted wall time is still unmeasured, and the first hosted run is that
  measurement. `standard` needs 935.14 s at its slowest local sample against a
  2100 s budget, and it is also the stage carrying the npm-dependent compile.
- The lint ceiling is a RATCHET. Raising it to make a round green converts the
  one honest lint signal in this repository into decoration.
- R-0482 is a live `NameError` on a guard's refusal path, frozen under that
  ceiling rather than fixed, and belongs to a branch of its own. R-0487, the
  `docs/README.md` link guard that checks the wrong file, belongs to that same
  paydown branch: both are test- or guard-content fixes this feature may not make.
