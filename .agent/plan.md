# Plan — F158 Cost normalization & price catalog

## Goal
Cross-vendor money becomes comparable, honestly: one configured currency (`cost.currency`, default
usd) shared by budgets, previews, the ledger and the catalog; a versioned price catalog per adapter
with source comments; ledger rows gain raw counters, a normalized cost, the pricing version and a
basis (provider_reported wins, the catalog cross-checks and warns past a threshold, a stale catalog
warns and never blocks); and `remedy worker pricing update` imports catalogs behind a shown diff
(`docs/roadmap/features/T8_F158.md`). F153 waits behind F316 (DECISION F158 D1).

## Current Step
Round 1 (session 1): claim F158, book F162's round 12, re-head the review record, DECISIONs F158 D1
and D2, operator question Q27, and the findings pass `.agent/f158_inventory.md`, reviewed before
any code is authored.

## Next Steps
1. Round 2, T001: the currency consolidation — the `cost.currency` key, the audit of every money
   field and display, the mixed-currency guard — with its shape frozen by a DECISION from the
   reviewed inventory.
2. T002: the catalog format and validation, the ledger's additive columns, the writer's basis,
   cross-check and staleness rules, and their goldens.
3. T003: the recompute by pricing version (raw counters immutable), the update command with its
   shown diff, the docs and the end-to-end; then the closure.

## Risks
- Catalog prices may cite only sources already on disk (DECISION F158 D2 (3)); a model without one
  stays unpriced.
