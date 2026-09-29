# Plan — F291 Self-use sources v2

Branch: feature/f291-self-use-sources-v2, cut from `main` at
`aa5defde`, the merge commit of pull request 298 (F042 Multi-project cockpit).

## Goal

Give the self-use generator two sources that almost always have real work,
so a closure's self-use reading is rarely "queue exhausted"
(`docs/roadmap/features/T5_F291.md`, DECISIONS F291 D1 to D4).

## Current Step

ROUND 4, the first closure repair round: book round 3, register R-1114,
record DECISION F291 D4, repair the two readers of `tests/` that a
vanished temporary module fails, and run the one full suite again on the
repaired tree.

## Next Steps

1. The evidence bundle and the review package, once the suite is green.
2. The closing round: STATUS, README, the ledger's rotation and the pull
   request.

## Risks

Open findings: R-1114, repaired this round. At most two more repair rounds
remain (amend0917-throughput rule 2).
