# Plan — F152 Worker config isolation

## Goal
A worker tool's personal configuration never reaches a run: each adapter declares its isolation
method (the tool's own flag or environment, a cleaned environment with a throwaway home, the
sandbox as reinforcement) with a required ADR, the call builder applies it and records
`worker_isolation` evidence, `remedy doctor` checks it, and the conformance kit refuses an
adapter without its ADR (`docs/roadmap/features/T8_F152.md`).

## Current Step
Round 4: book round 3's FAIL and R-1455 to R-1457; repair them (the capability-route test states
its property, an adapter without a declaration is refused, the record's Consequences follow D3);
and T002 under DECISION F152 D4, the A/B proof utility with its stand-in proof and red controls.

## Next Steps
1. T003: the per-adapter doctor check, the conformance-kit requirement that the record exists and
   that the command line carries the declared flags, and the docs.
2. The closure sequence: the integration gate, the evidence package, the STATUS acceptance, with
   the real-binary A/B named as the open risk while operator question Q26 is unanswered.

## Risks
- A worker that reached its model through variables outside the allowlist loses them; the
  allowlist keeps the API key and the proxies.
