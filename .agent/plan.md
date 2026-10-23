# Plan — F151 Worker adapter contract v2

## Goal
Give the neutrality promise its interface: a typed adapter contract (capabilities, invocation
building, stream and usage mapping, isolation) with a reusable conformance kit, today's builder path
wrapped as the reference adapter with golden equality, and orchestration importing only the contract.

## Current Step
Round 5: R-1438's tests, and T003's second half under DECISION F151 D5 — the `adapter_ref` linkage,
the adapter registry reached by `remedy worker show`, the import guard, and `LLMWorker` deleted.

## Next Steps
1. The docs page for the contract, the architecture page's worker section, and the README index.
2. The closure sequence.

## Risks
- The surviving call path is spread over several modules; wrapping it must not move transport,
  retries or evidence out of the loop (the feature file's Do-not-touch).
