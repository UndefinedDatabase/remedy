# Plan — F158 Cost normalization & price catalog

## Goal
Cross-vendor money becomes comparable, honestly: one configured currency (`cost.currency`, default
usd) shared by budgets, previews, the ledger and the catalog; a versioned price catalog per adapter
with source comments; ledger rows gain raw counters, a normalized cost, the pricing version and a
basis (provider_reported wins, the catalog cross-checks and warns past a threshold, a stale catalog
warns and never blocks); and `remedy worker pricing update` imports catalogs behind a shown diff
(`docs/roadmap/features/T8_F158.md`). F153 waits behind F316 (DECISION F158 D1).

## Current Step
Round 2 (session 1), T001 per DECISION F158 D3: book round 1, the `cost.currency` key and
`packages/orchestration/cost_currency.py`, its reader in `remedy config validate`, the
mixed-currency guard, and the audit page `docs/system/cost-currency-v1.md`.

## Next Steps
1. Round 3, T002 part 1: the catalog format, its home and validation, and the feature-file
   amendment for the names the inventory found differ (`price_table` for `catalog_computed`, the
   catalog beside its module, no scoreboard, no cockpit), frozen by DECISION F158 D4.
2. T002 part 2: the ledger's additive columns and the writer's basis, cross-check and staleness
   rules, with their goldens.
3. T003: the recompute by pricing version (raw counters immutable), the update command with its
   shown diff, the docs and the end-to-end; then the closure.

## Risks
- Catalog prices may cite only sources already on disk (DECISION F158 D2 (3)); a model without one
  stays unpriced.
