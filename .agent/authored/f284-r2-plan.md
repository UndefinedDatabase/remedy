# Plan — F284 Findings paydown v3

Branch: feature/f284-findings-paydown-v3, cut from `main` at
`a36a8759`, the merge commit of pull request 275 (F019 Live node
materialization).

## Goal

Pay down the four open findings F284 owns, each by the repair its own text
names, with the evidence that discharged it
(`docs/roadmap/features/T2_F284.md`, DECISIONS F284 D1 and D2).

## Current Step

ROUND 2: book round 1's PASS with the resolutions of R-1046 and R-0499,
record DECISION F284 D2, and land T003 (R-0950): the smoke tests judge
teardown by the harness's own sweep and read an open fallback port by the
process that holds it.

## Next Steps

1. The closure sequence: the one full suite in the integration-gate round,
   the checklist consolidation, the Built State, and the self-use run that
   alone can resolve R-1008.
2. The evidence package and the STATUS flip.

## Risks

R-1008 resolves only if the closure's self-use run lands a diff its
reviewer passes; otherwise it is carried by name to the next paydown.
Open findings after round 2's booking: 2.
