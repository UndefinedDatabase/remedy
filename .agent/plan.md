# Plan — F152 Worker config isolation

## Goal
A worker tool's personal configuration never reaches a run: each adapter declares its isolation
method (the tool's own flag or environment, a cleaned environment with a throwaway home, the
sandbox as reinforcement) with a required ADR, the call builder applies it and records
`worker_isolation` evidence, `remedy doctor` checks it, and the conformance kit refuses an
adapter without its ADR (`docs/roadmap/features/T8_F152.md`).

## Current Step
Round 3, T001 under DECISION F152 D3: the `WorkerIsolation` declaration and its validation, the
claude-cli declaration and its flags, the kit's isolation check, the `worker_isolation` module
(child environment, digest, evidence line, throwaway home), the spawn policies' environment, the
evidence line per provider build, and the record's mechanism section rewritten to D3.

## Next Steps
1. T002: the A/B proof utility over a throwaway home with a poisoned configuration, run against a
   stub executable in every selection, and the real-binary run behind a switch that is off by
   default.
2. T003: the per-adapter doctor check, the conformance-kit requirement that the record exists and
   that the command line carries the declared flags, and the docs.
3. The closure sequence: the integration gate, the evidence package, the STATUS acceptance.

## Risks
- A worker that reached its model through variables outside the allowlist loses them; the
  allowlist keeps the API key and the proxies, and the handoff names the rest.
