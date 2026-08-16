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
R25 is closed PASS and R26 recorded it. R26 is the integration-gate round per
docs/agents/integration_gate.md: the full suite once on the branch, once at the
merge base f3fd96d7 in a throwaway worktree, the two FAILED lists compared, and
every id in either direction attributed by direct evidence. Its measured values
live in `.agent/gate_f083_r26/`, not in this file. T001, T002 and T003 are
COMPLETE and every documentation claim in this feature is pinned to a
measurement.

## Next Steps
1. Closure per docs/roadmap/STATUS_closure_protocol.md — the evidence job and a
   FRESH review zip, both mandatory, then the authored STATUS line and the PR.
   The closure run is the second and last full-suite run this feature gets.

## Risks
- Hosted wall time is still unmeasured, and the first hosted run is that
  measurement. `standard` needs 935.14 s at its slowest local sample against a
  2100 s budget, and it is also the stage carrying the toolchain-dependent tests.
- The lint ceiling is a RATCHET. Raising it to make a round green converts the
  one honest lint signal in this repository into decoration.
- R-0482 (a live `NameError` on a guard's refusal path) and R-0487
  (`docs/README.md` is never link-checked) are both frozen here and belong to a
  paydown branch: each is a code- or test-content fix this feature may not make.
