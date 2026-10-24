# Plan — F158 Cost normalization & price catalog

## Goal
Cross-vendor money becomes comparable, honestly: one configured currency (`cost.currency`, default
usd) shared by budgets, previews, the ledger and the catalog; a versioned price catalog per adapter
with sources; each ledger call valued with a normalized cost, the pricing version and a basis
(provider_reported wins, the catalog cross-checks and warns past a threshold, a stale catalog warns
and never blocks); and `remedy worker pricing update` imports catalogs behind a shown diff
(`docs/roadmap/features/T8_F158.md`, amendment A1). F153 waits behind F316 (DECISION F158 D1).

## Current Step
Round 4 (session 1), T002 part 2 per DECISION F158 D5: book round 3, the two cost keys, the
`call_valuations` table and its basis rules in `packages/orchestration/call_valuation.py`, the
evidence hook valuing each mirrored call, the staleness check, and their goldens.

## Next Steps
1. Round 5, T003 part 1: the recompute of valuations when a catalog's pricing version changes, with
   the `calls` rows proven unchanged by a hash, and `remedy worker pricing update` with its shown
   diff, frozen by DECISION F158 D6.
2. T003 part 2: `remedy stats cost` reading the valuations with their basis, flagged and stale
   rows, the docs and the end-to-end; then the closure in the next session.

## Risks
- Catalog prices may cite only sources already on disk (DECISION F158 D2 (3)); the shipped
  catalog is empty, so the goldens use fixture catalogs.
