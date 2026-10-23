# Plan — F315 The loop runs through the adapter

## Goal
The ping-pong loop's claude-cli builder and reviewer calls run through `ClaudeCliReferenceAdapter`:
the adapter builds the invocation and maps stream, usage and errors; the loop keeps transport,
timeouts, retries, failover, pacing and evidence; the goldens stay byte-equal and the import guard
stays green.

## Current Step
Round 2, T002: the worker adapter slot filled by the command line, every claude-cli command line
built by the installed adapter, and the test that replaces the adapter and sees the loop follow it
(DECISION F315 D2).

## Next Steps
1. T003: usage and error mapping through the adapter, the stream decision, the resume and
   parse-retry paths, the readers of the `build_claude_cli_args` re-export re-pointed and the
   re-export deleted, the docs.
2. The closure sequence.

## Risks
- A process that runs a job without the command line or the test configuration finds an empty
  slot; the provider reports it as a provider error, by design (D2 (4)).
- `pingpong_provider.py` and the loop are held by the structure ledger: no listed function grows.
