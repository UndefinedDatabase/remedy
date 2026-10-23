# Plan — F151 Worker adapter contract v2

## Goal
Give the neutrality promise its interface: a typed adapter contract (capabilities, invocation
building, stream and usage mapping, isolation) with a reusable conformance kit, today's builder path
wrapped as the reference adapter with golden equality, and orchestration importing only the contract.

## Current Step
Round 1: claim F151, re-head the review record, DECISION F151 D1, and T001's inventory
`.agent/f151_inventory.md`, reviewed before any code.

## Next Steps
1. T002: the contract module, the conformance kit and recorded samples, proved against a broken toy
   adapter; DECISION F151 D2 names the modules and the ownership table from the inventory.
2. T003: the reference adapter with golden equality, the import guard, the registry linkage, docs.
3. The closure sequence.

## Risks
- The surviving call path is spread over several modules; wrapping it must not move transport,
  retries or evidence out of the loop (the feature file's Do-not-touch).
