# Plan — F152 Worker config isolation

## Goal
A worker tool's personal configuration never reaches a run: each adapter declares its isolation
method (the tool's own flag or environment, a cleaned environment with a throwaway home, the
sandbox as reinforcement) with a required ADR, the call builder applies it and records
`worker_isolation` evidence, `remedy doctor` checks it, and the conformance kit refuses an
adapter without its ADR (`docs/roadmap/features/T8_F152.md`).

## Current Step
Round 9, the closure's evidence round: book round 8's PASS and R-1463 resolved, save the evidence
script, the staging reclaim, the evidence job `f152r9e1001` and the review package.

## Next Steps
1. The closing round: the Built State, the ledger rotation, the STATUS acceptance with the README
   sync and SU-082's `consumed_by`, and the pull request, left unmerged; the real-binary A/B is
   named as the open risk while operator question Q26 is unanswered.

## Risks
- A package that does not read `READY_FOR_REVIEW` blocks the closure until it is repaired.
