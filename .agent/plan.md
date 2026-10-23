# Plan — F315 The loop runs through the adapter

## Goal
The ping-pong loop's claude-cli builder and reviewer calls run through `ClaudeCliReferenceAdapter`:
the adapter builds the invocation and maps what the loop's evidence does not own; the loop keeps
transport, timeouts, retries, failover, pacing and evidence; the goldens stay byte-equal and the
import guard stays green.

## Current Step
Round 5, the closure's evidence round: the staging reclaim, the evidence job and the review
package. The one full suite ran green in round 4; R-1442 is registered for F314.

## Next Steps
1. The closing round: the Built State, the rotation, SU-079's consumed_by, the STATUS line with the
   README sync, and the pull request, left unmerged.

## Risks
- A process that runs a job without the command line or the test configuration finds an empty
  slot; the self-use script installs the registry itself for that reason (DECISION F315 D2).
