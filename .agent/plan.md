# Plan — F152 Worker config isolation

## Goal
A worker tool's personal configuration never reaches a run: each adapter declares its isolation
method (the tool's own flag or environment, a cleaned environment with a throwaway home, the
sandbox as reinforcement) with a required ADR, the call builder applies it and records
`worker_isolation` evidence per call, `remedy doctor` checks it, and the conformance kit refuses an
adapter without its ADR (`docs/roadmap/features/T8_F152.md`).

## Current Step
Round 1: claim F152, re-head the review record and book F157's round 11, DECISION F152 D1, and the
findings pass — the reserved isolation slot, the invocation seam, the environment machinery, the
claude command line's configuration surfaces, the evidence, doctor and the kit — committed as
`.agent/f152_inventory.md` for review.

## Next Steps
1. T001: the isolation declaration, the per-call evidence field and the throwaway-home mechanics
   with their unit tests, with the shape frozen from the reviewed inventory by DECISION F152 D2.
2. T002: the reference adapter's research as an ADR, reviewed; then its enforcement and the
   poisoned-config A/B proof.
3. T003: the doctor check, the conformance-kit requirement and the docs.
4. The closure sequence: the integration gate, the evidence package, the STATUS acceptance.

## Risks
- A throwaway home can hide the tool's own login; the inventory reads where the claude command line
  finds its credentials before any design depends on a fresh home.
