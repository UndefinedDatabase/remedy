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
R27 is closed PASS. R28 is the CLOSURE round per
docs/roadmap/STATUS_closure_protocol.md: it records that verdict, then runs the
evidence job and a fresh review zip against this commit, writes the STATUS `[x]`
line together with the README capability sync in one commit, and opens the PR.
T001, T002 and T003 are COMPLETE, the integration gate passed at R26 with 0
branch-only and 0 base-only failures, and the feature file's Built State landed
at R27.

## Next Steps
1. The PR is NOT merged this session. It merges at the next feature's start via
   the AGENTS.md Open PR Gate; the gap is the operator's manual-review window.
2. A paydown branch for R-0482 and R-0487, which this feature deliberately did
   not fix.

## Risks
- Hosted wall time is still unmeasured, and the first hosted run is that
  measurement. `standard` needs 935.14 s at its slowest local sample against a
  2100 s budget, and it is also the stage carrying the toolchain-dependent tests.
- The lint ceiling is a RATCHET. Raising it to make a round green converts the
  one honest lint signal in this repository into decoration.
- R-0482 (a live `NameError` on a guard's refusal path) and R-0487
  (`docs/README.md` is never link-checked) are both frozen here: each is a code-
  or test-content fix this feature may not make.
