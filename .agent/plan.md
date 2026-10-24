# Plan — F152 Worker config isolation

## Goal
A worker tool's personal configuration never reaches a run: each adapter declares its isolation
method (the tool's own flag or environment, a cleaned environment with a throwaway home, the
sandbox as reinforcement) with a required ADR, the call builder applies it and records
`worker_isolation` evidence per call, `remedy doctor` checks it, and the conformance kit refuses an
adapter without its ADR (`docs/roadmap/features/T8_F152.md`).

## Current Step
Round 2: book round 1, DECISION F152 D2 (research before the contract, the isolation record's
kind, the real-binary proof off by default) with operator question Q26, and the claude-cli
isolation record `docs/adr/0002-claude-cli-worker-isolation.md` with its index rows, for review.

## Next Steps
1. T001: the isolation declaration in the contract with its required record reference, the
   reference adapter's declaration from the reviewed record, the per-call evidence field and the
   throwaway-home mechanics with their unit tests, shape frozen by DECISION F152 D3.
2. T002: the enforcement in the claude-cli call path and the A/B proof utility, run against a stub
   executable, with the real-binary run behind a switch that is off by default.
3. T003: the per-adapter doctor check, the conformance-kit requirement and the docs.
4. The closure sequence: the integration gate, the evidence package, the STATUS acceptance.

## Risks
- The claude command line cannot be run in these sessions; unverified points stay marked as such
  until the operator answers Q26.
