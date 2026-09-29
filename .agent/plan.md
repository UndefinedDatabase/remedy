# Plan — F291 Self-use sources v2

Branch: feature/f291-self-use-sources-v2, cut from `main` at
`aa5defde`, the merge commit of pull request 298 (F042 Multi-project cockpit).

## Goal

Give the self-use generator two sources that almost always have real work,
so a closure's self-use reading is rarely "queue exhausted"
(`docs/roadmap/features/T5_F291.md`, DECISIONS F291 D1 to D3).

## Current Step

ROUND 3, the integration gate: book round 2, record DECISION F291 D3, land
the self-use item SU-037's diff with two reviewer tests, add the Built
State's self-use paragraph, build the cockpit and run the one full suite.

## Next Steps

1. The evidence bundle and the review package.
2. The closing round: STATUS, README, the ledger's rotation and the pull
   request.

## Risks

Open findings: 0. A red suite is this feature's to repair, in at most
three repair rounds (amend0917-throughput rule 2).
