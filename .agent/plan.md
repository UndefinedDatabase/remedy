# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0460. Open findings: the seventy-five carried out
of the F082 record plus R-0448 to R-0459 registered on this branch.
`.agent/live_review.md` is the source of truth; this file mirrors it.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure fails
the right stage with a readable summary, and runtime stays within a budget.

## Current Step
R6 records the R5 PASS, registers R-0456 to R-0459 and repairs the three runner
defects the R5 review found: the run is anchored at the repository root, because
a marker selection carries no path and pytest otherwise collects from wherever
the caller stands; a run in which no stage ran is red rather than green; and a
guard assertion that could not fail is replaced by one that can.

## Next Steps
1. R7 adds the `remedy ci [--stage NAME] [--json]` CLI seam Q8 names — the
   catalog group, the entry and a `COMMAND_HANDLERS` module — and the summary
   table it prints, which states the accepted `standard`/`smoke` double-run.

## Risks
- No test yet runs a stage for real: the injected runner buys speed at the cost
  of never proving the subprocess seam end to end, and this round narrows that
  gap only as far as the cwd anchor. R7 must land one real stage invocation.
  `fast` still rests on a single 391.8 s reading.
