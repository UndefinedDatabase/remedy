# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0461. Open findings: the seventy-five carried out
of the F082 record plus R-0448 to R-0460 registered on this branch, of which
R-0456 to R-0459 are resolved. `.agent/live_review.md` is the source of truth.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure fails
the right stage with a readable summary, and runtime stays within a budget.

## Current Step
R7 closes the record R6 left open: the R6 PASS verdict, R-0460 registered, and
the four `Landed:` lines replaced by the reviewer's `Done:` resolutions, since
only reviewer-authored text sets Resolved. It writes no code, and it repairs the
map because the CLI seam moves out of this round.

## Next Steps
1. R8 makes the runner reachable: a `ci` group and `ci.run` entry in
   `apps/cli/command_catalog.py`, `apps/cli/commands/ci_cmd.py` carrying
   `COMMAND_HANDLERS` and the summary table, its wiring in
   `apps/cli/commands/__init__.py`, and `tests/cli/test_ci_cmd.py` — including
   one test that really launches a stage argv through the pytest runner script.

## Risks
- `fast` still rests on a single 391.8 s reading, and the inventory showed it is
  inverted with respect to cost. Until that is measured under `-n auto`, no
  runtime budget can be written from measured data.
