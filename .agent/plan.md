# Plan — F315 The loop runs through the adapter

## Goal
The ping-pong loop's claude-cli builder and reviewer calls run through `ClaudeCliReferenceAdapter`:
the adapter builds the invocation and maps what the loop's evidence does not own; the loop keeps
transport, timeouts, retries, failover, pacing and evidence; the goldens stay byte-equal and the
import guard stays green.

## Current Step
Round 6, the closing round: the Built State, the rotation, SU-079's consumed_by, the STATUS line
with the README sync, and the pull request, left unmerged.

## Next Steps
1. The next session merges F315's pull request at the Open PR Gate and claims the next feature by
   Rule A5.

## Risks
- R-1442, raised by the closure's self-use run, is open and owned by F314.
