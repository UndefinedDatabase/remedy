# Plan — F152 Worker config isolation

## Goal
A worker tool's personal configuration never reaches a run: each adapter declares its isolation
method (the tool's own flag or environment, a cleaned environment with a throwaway home, the
sandbox as reinforcement) with a required ADR, the call builder applies it and records
`worker_isolation` evidence, `remedy doctor` checks it, and the conformance kit refuses an
adapter without its ADR (`docs/roadmap/features/T8_F152.md`).

## Current Step
Round 7, the closure's integration-gate round: book round 6's PASS and R-1460 to R-1462 resolved,
the checklist's one consolidation pass, the self-use item run to its approval gate through the
isolated claude-cli worker, and the feature's one full suite with its cost reading.

## Next Steps
1. The evidence round: the staging reclaim, the evidence job and the review package.
2. The closing round: the Built State, the ledger rotation, the STATUS acceptance with the README
   sync and the self-use queue, and the pull request, left unmerged; the real-binary A/B is named
   as the open risk while operator question Q26 is unanswered.

## Risks
- The self-use run is the first real claude-cli call through the declared flags and the cleaned
  environment; a refusal or a lost login there is a finding of this feature.
