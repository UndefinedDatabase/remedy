# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0485. `.agent/live_review.md` is the source of
truth for the open set; this file repeats no count of it.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure fails
the right stage with a readable summary, and runtime stays within a budget.

## Current Step
R20 is closed PASS and R21 recorded it. R21 landed the first half of T003: the
hosted workflow `.github/workflows/ci.yml`, a thin wrapper that installs the
Python and the UI toolchain and then calls `remedy ci run` once, plus the guard
tests pinning its load-bearing properties — it calls the entrypoint, it selects
no tests of its own, it installs the UI toolchain before the run, and it never
auto-retries.

## Next Steps
1. T003's second half: the CI documentation under `docs/`, registered in the
   `docs/README.md` index, carrying the runtime-budget table from the measured
   data in `.agent/f083_inventory.md` `## Q9` through `## Q12` and saying plainly
   that hosted wall time is NOT measured — only the local samples are.
2. Then the integration-gate round, then closure per
   docs/roadmap/STATUS_closure_protocol.md.

## Risks
- Hosted wall time is unmeasured. `standard` needs 935.14 s at its slowest local
  sample against a 2100 s budget, and a hosted runner with fewer cores may exceed
  it. The first hosted run is the measurement; raising `timeout_sec` before that
  evidence exists would be a guess wearing a budget's name.
- The lint ceiling is a RATCHET. Raising it to make a round green converts the
  one honest lint signal in this repository into decoration.
- R-0482 is a live `NameError` on a guard's refusal path, frozen under that
  ceiling rather than fixed, and belongs to a branch of its own.
