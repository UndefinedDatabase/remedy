# Plan — F315 The loop runs through the adapter

## Goal
The ping-pong loop's claude-cli builder and reviewer calls run through `ClaudeCliReferenceAdapter`:
the adapter builds the invocation and maps stream, usage and errors; the loop keeps transport,
timeouts, retries, failover, pacing and evidence; the goldens stay byte-equal and the import guard
stays green.

## Current Step
Round 1: claim F315, re-head the review record, DECISION F315 D1, and T001's inventory
`.agent/f315_inventory.md`, reviewed before any code.

## Next Steps
1. T002: the builder and reviewer calls through the adapter behind the seam DECISION F315 D2 names,
   with a test that replaces the adapter and sees the loop follow it.
2. T003: the resume and parse-retry paths through the adapter, the provider's retired copies, docs.
3. The closure sequence.

## Risks
- Every module that builds the provider sits under `packages/orchestration/`, which may not import a
  concrete adapter; the seam must be filled from the wiring layer without a dynamic-import detour.
- `pingpong_provider.py` and the loop are held by the structure ledger: no listed function grows.
