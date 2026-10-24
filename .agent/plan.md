# Plan — F158 Cost normalization & price catalog

## Goal
Cross-vendor money becomes comparable, honestly: one configured currency (`cost.currency`, default
usd) shared by budgets, previews, the ledger and the catalog; a versioned price catalog per adapter
with sources; each ledger call valued with a normalized cost, the pricing version and a basis; and
`remedy worker pricing-update` imports catalogs behind a shown diff
(`docs/roadmap/features/T8_F158.md`, amendments A1 to A3). F153 waits behind F316 (D1).

## Current Step
Round 9 (session 2), the closing round: book round 8; the Built State; the ledger rotation; the
STATUS acceptance with its README sync and SU-084's `consumed_by`; the pull request, left unmerged.
F158 is then closed PASS_WITH_RISKS for R-1472, owned by F316.

## Next Steps
1. The next session: Phase 1 rule 1 (`.agent/STOP`), then the Open PR Gate merges F158's pull
   request, then round 9's verdict is booked in the next feature's first commit, then Rule A5.

## Risks
- None open for F158; R-1472 (self-use runs reach no token ledger) is owned by F316.
