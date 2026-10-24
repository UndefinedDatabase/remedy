# Plan — F152 Worker config isolation

## Goal
A worker tool's personal configuration never reaches a run: each adapter declares its isolation
method (the tool's own flag or environment, a cleaned environment with a throwaway home, the
sandbox as reinforcement) with a required ADR, the call builder applies it and records
`worker_isolation` evidence, `remedy doctor` checks it, and the conformance kit refuses an
adapter without its ADR (`docs/roadmap/features/T8_F152.md`).

## Current Step
Round 5: book round 4's FAIL, resolve R-1455 to R-1457 and register R-1458 and R-1459; repair
both; and T003 under DECISION F152 D5 — the kit's record and flag requirement, the isolation
checks of `worker doctor`, and the docs.

## Next Steps
1. The closure sequence: the integration gate with the one full suite, the evidence package and
   the review zip, the Built State, the STATUS acceptance and the pull request, with the
   real-binary A/B named as the open risk while operator question Q26 is unanswered.

## Risks
- A worker that reached its model through variables outside the allowlist loses them; the
  allowlist keeps the API key and the proxies.
