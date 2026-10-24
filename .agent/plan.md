# Plan — F158 Cost normalization & price catalog

## Goal
Cross-vendor money becomes comparable, honestly: one configured currency (`cost.currency`, default
usd) shared by budgets, previews, the ledger and the catalog; a versioned price catalog per adapter
with sources; each ledger call valued with a normalized cost, the pricing version and a basis
(provider_reported wins, the catalog cross-checks and warns past a threshold, a stale catalog warns
and never blocks); and `remedy worker pricing update` imports catalogs behind a shown diff
(`docs/roadmap/features/T8_F158.md`, amendment A1). F153 waits behind F316 (DECISION F158 D1).

## Current Step
Round 3 (session 1), T002 part 1 per DECISION F158 D4: book round 2, amendment A1, the catalog
format with its loader and refusals in `packages/orchestration/price_catalog.py`, and the shipped
`claude-cli` catalog, empty until a price with a source is imported.

## Next Steps
1. Round 4, T002 part 2: each ledger call valued at record time — the normalized cost, its basis,
   the pricing version, the cross-check warning past the threshold and the staleness warning —
   with their goldens, frozen by DECISION F158 D5; the orphan entry for the catalog goes.
2. T003: the recompute by pricing version with the raw counters immutable, `remedy worker pricing
   update` with its shown diff, the docs and the end-to-end; then the closure.

## Risks
- Catalog prices may cite only sources already on disk (DECISION F158 D2 (3)); the shipped
  catalog is empty, so the goldens use fixture catalogs.
