# Plan — F313 Contract 1.22 for the Orb

## Goal
Remedy ships what F310, F311 and F312 added to its clients as contract 1.22: both versions, the
release matrix, the two pages and recorded answers for the universe's kit
(`docs/roadmap/features/T12_F313.md`, DECISIONs F313 D1 and D2).

## Current Step
Round 2 (session 1): book round 1 and register R-1390; repair R-1390, so the digest's decisions
carry a budget stop's `blockers` (DECISION F313 D1 addendum); and T002: the hand-written parts of
`docs/system/public-http-api-v1.md` and `docs/system/machine-client-contract-v1.md`, the two
routes' descriptions at "since 1.22", and both generated sections regenerated (D1 (3)).

## Next Steps
1. T003: `scripts/record_client_answers.py`, the folder `docs/system/client-answers-v1/` and the
   test that runs its check (D2).
2. The closure sequence: the integration gate with the one full suite, the evidence, acceptance.

## Risks
- The integrity check fails on High findings F313 does not own (DECISION F310 D7, Q20).
