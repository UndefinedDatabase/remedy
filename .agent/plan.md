# Plan — F152 Worker config isolation

## Goal
A worker tool's personal configuration never reaches a run: each adapter declares its isolation
method (the tool's own flag or environment, a cleaned environment with a throwaway home, the
sandbox as reinforcement) with a required ADR, the call builder applies it and records
`worker_isolation` evidence, `remedy doctor` checks it, and the conformance kit refuses an
adapter without its ADR (`docs/roadmap/features/T8_F152.md`).

## Current Step
Round 10, the closing round: book round 9 and register R-1464 for F316, the Built State, the ledger
rotation, F152 accepted in STATUS with the README sync and SU-082's `consumed_by`, and the pull
request, left unmerged.

## Next Steps
1. The next session merges F152's pull request at the Open PR Gate, books round 10's verdict in the
   next feature's first commit, and claims the next feature by Rule A5.
