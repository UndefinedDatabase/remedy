# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0456. Open findings: the seventy-five carried out
of the F082 record plus R-0448 to R-0455 registered on this branch.
`.agent/live_review.md` is the source of truth; this file mirrors it.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure fails
the right stage with a readable summary, and runtime stays within a budget.

## Current Step
R5 records the R4 PASS — a clean round, no finding — splits the map's R5 clause
so the runner and the CLI seam stop sharing one round, and builds
`packages/orchestration/ci_run.py`: one stage in, one `StageResult` out, every
stage going through `scripts/remedy_pytest_runner.py` so the process-group
cleanup, the output caps and the timeout survive. The command runner is injected,
so `tests/orchestration/test_ci_run.py` proves the wiring without spawning pytest.

## Next Steps
1. R6 adds the `remedy ci [--stage NAME] [--json]` CLI seam Q8 names — the
   catalog group, the entry and a `COMMAND_HANDLERS` module — and the summary
   table it prints, which states the accepted `standard`/`smoke` double-run.
2. R7 measures each stage with and without `-n auto`, pins the per-stage setting
   from that reading (DECISION F083 D2.5), and adds the per-stage selection
   tests over a fixture tree rather than live collected counts.

## Risks
- No test yet runs a stage for real, by design: the injected runner buys speed
  at the cost of never proving the subprocess seam end to end. R6 must land one
  real stage invocation. `fast` still rests on a single 391.8 s reading.
