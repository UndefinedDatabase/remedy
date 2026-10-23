# Plan — F315 The loop runs through the adapter

## Goal
The ping-pong loop's claude-cli builder and reviewer calls run through `ClaudeCliReferenceAdapter`:
the adapter builds the invocation and maps what the loop's evidence does not own; the loop keeps
transport, timeouts, retries, failover, pacing and evidence; the goldens stay byte-equal and the
import guard stays green.

## Current Step
Round 3, T003: the usage of a call that is not streamed from the adapter, the stream and error
classes kept with the loop's evidence, the re-export deleted, the docs (DECISION F315 D3).

## Next Steps
1. The closure sequence: the integration gate round with the one full suite, the checklist
   consolidation and the self-use item; then the evidence round; then the closing round.

## Risks
- A process that runs a job without the command line or the test configuration finds an empty
  slot; the provider reports it as a provider error, by design (D2 (4)).
- `pingpong_provider.py` and the loop are held by the structure ledger: no listed function grows.
