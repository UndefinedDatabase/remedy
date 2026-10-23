# Plan — F151 Worker adapter contract v2

## Goal
Give the neutrality promise its interface: a typed adapter contract (capabilities, invocation
building, stream and usage mapping, isolation) with a reusable conformance kit, today's builder path
wrapped as the reference adapter with golden equality, and orchestration importing only the contract.

## Current Step
Round 3: the T002 repair, DECISION F151 D3 — the transport dimension over the whole class chain
with the failure class exempt (R-1435, R-1436), and one test per unguarded kit check (R-1437).

## Next Steps
1. T003: the `claude-cli` reference adapter with golden equality, the import guard with a violation
   fixture, the registry linkage, the deletion of `LLMWorker`, and the docs.
2. The closure sequence.

## Risks
- The surviving call path is spread over several modules; wrapping it must not move transport,
  retries or evidence out of the loop (the feature file's Do-not-touch).
