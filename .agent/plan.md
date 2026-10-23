# Plan — F151 Worker adapter contract v2

## Goal
Give the neutrality promise its interface: a typed adapter contract (capabilities, invocation
building, stream and usage mapping, isolation) with a reusable conformance kit, today's builder path
wrapped as the reference adapter with golden equality, and orchestration importing only the contract.

## Current Step
Round 4: R-1437's last two pins, and T003's first half under DECISION F151 D4 — the claude-cli
reference adapter `packages/providers/adapters/claude_cli_reference.py` with its goldens and kit run.

## Next Steps
1. T003's second half: the import guard with a violation fixture, the registry linkage that reaches
   the adapter, the deletion of `LLMWorker`, the docstrings and the docs page.
2. The closure sequence.

## Risks
- The surviving call path is spread over several modules; wrapping it must not move transport,
  retries or evidence out of the loop (the feature file's Do-not-touch).
