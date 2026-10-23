# Plan — F151 Worker adapter contract v2

## Goal
Give the neutrality promise its interface: a typed adapter contract (capabilities, invocation
building, stream and usage mapping, isolation) with a reusable conformance kit, today's builder path
wrapped as the reference adapter with golden equality, and orchestration importing only the contract.

## Current Step
Round 6: R-1439 (the guard's parent-package form) and R-1440 (the `none` capabilities line), the
docs page `docs/system/worker-adapter-contract-v1.md`, its index rows, and the architecture page's
worker section.

## Next Steps
1. The closure sequence: the integration gate with the one full suite and the self-use run, the
   evidence round, then the closing round.

## Risks
- None open beyond R-1439 and R-1440, which this round repairs.
