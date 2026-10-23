# Plan — F315 The loop runs through the adapter

## Goal
The ping-pong loop's claude-cli builder and reviewer calls run through `ClaudeCliReferenceAdapter`:
the adapter builds the invocation and maps what the loop's evidence does not own; the loop keeps
transport, timeouts, retries, failover, pacing and evidence; the goldens stay byte-equal and the
import guard stays green.

## Current Step
Round 4, the closure's integration-gate round: the checklist's consolidation pass, the self-use
item run to its approval gate, and the feature's one full suite with its CPU cost.

## Next Steps
1. A repair round for every bad node id, when the suite is red; otherwise the evidence bundle and
   the review package.
2. The closing round: the Built State, the rotation, the STATUS line, the README, the pull request.

## Risks
- A process that runs a job without the command line or the test configuration finds an empty
  slot; the self-use script installs the registry itself for that reason (DECISION F315 D2).
