# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. `.agent/live_review.md` is the source of truth for the open set and for
the next free finding id; this file repeats neither.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure fails
the right stage with a readable summary, and runtime stays within a budget.

## Current Step
R26 is closed PASS: the integration gate ran the full suite on the branch and at
the merge base and found 0 branch-only and 0 base-only failures. R27 records that
verdict, registers and resolves R-0489, and lands the feature file's Built State
section — the last content this feature owes, and a closure precondition the
closure commit's own path set cannot satisfy itself. T001, T002 and T003 are
COMPLETE.

## Next Steps
1. Closure per docs/roadmap/STATUS_closure_protocol.md: the evidence job, then a
   FRESH review zip from a clean tree, then the STATUS line and the README
   capability sync in ONE commit, then the PR. The zip's package name and
   SHA-256 do not exist until the worker builds it, so the STATUS line is
   authored as a template with named slots and gated on its GRAMMAR.

## Risks
- Hosted wall time is still unmeasured, and the first hosted run is that
  measurement. `standard` needs 935.14 s at its slowest local sample against a
  2100 s budget, and it is also the stage carrying the toolchain-dependent tests.
- The lint ceiling is a RATCHET. Raising it to make a round green converts the
  one honest lint signal in this repository into decoration.
- Closure packaging has a documented history of BLOCKED_EVIDENCE traps. The
  closure block names each one it must clear rather than discovering them at zip
  time.
- R-0482 (a live `NameError` on a guard's refusal path) and R-0487
  (`docs/README.md` is never link-checked) are both frozen here and belong to a
  paydown branch: each is a code- or test-content fix this feature may not make.
