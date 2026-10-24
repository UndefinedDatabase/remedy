# Plan — F152 Worker config isolation

## Goal
A worker tool's personal configuration never reaches a run: each adapter declares its isolation
method (the tool's own flag or environment, a cleaned environment with a throwaway home, the
sandbox as reinforcement) with a required ADR, the call builder applies it and records
`worker_isolation` evidence, `remedy doctor` checks it, and the conformance kit refuses an
adapter without its ADR (`docs/roadmap/features/T8_F152.md`).

## Current Step
Round 8, the closure's repair round: book round 7's FAIL and register R-1463, rename the A/B
marker out of the `REMEDY_` namespace, and run the one full suite again on the repaired tree,
replacing the transcript at its path.

## Next Steps
1. The evidence round: the staging reclaim, the evidence job and the review package.
2. The closing round: the Built State, the ledger rotation, the STATUS acceptance with the README
   sync and the self-use queue, and the pull request, left unmerged; the real-binary A/B is named
   as the open risk while operator question Q26 is unanswered.

## Risks
- A second red suite is the second of at most three repair rounds (operator amendment
  amend0917-throughput rule 2); each must strictly shrink the bad set.
