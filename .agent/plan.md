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
R19 is closed PASS and R20 recorded it. R20 corrected R-0480's cause from the
`## Q13` measurement — the variable is a missing `apps/ui/node_modules`, not a
cold npx cache — and ruled DECISION F083 D6: the tsc check resolves the LOCAL
compiler or skips with an install hint, instead of silently grading a cached
`tsc@2.0.4` stub. R-0480, R-0483 and R-0484 are resolved. T001 and T002 are
complete.

## Next Steps
1. T003, the last slice: hosted workflow files that call the same `remedy ci`
   entrypoint, the docs, and the runtime-budget documentation from the measured
   data in `## Q9` through `## Q12`. The workflow MUST run
   `npm ci --prefix apps/ui` before the `ui` stage — DECISION F083 D6 makes that
   step load-bearing, because without it the tsc check skips hosted too.
2. Then the integration-gate round, then closure per
   docs/roadmap/STATUS_closure_protocol.md.

## Risks
- If T003's workflow omits the `npm ci` step, the `ui` stage goes GREEN hosted by
  skipping, and the Acceptance line is met by a skip rather than a compile. That
  is the same false green D6 removed, wearing a different hat.
- The lint ceiling is a RATCHET. Raising it to make a round green converts the
  one honest lint signal in this repository into decoration.
- R-0482 is a live `NameError` on a guard's refusal path, frozen under that
  ceiling rather than fixed, and belongs to a branch of its own.
