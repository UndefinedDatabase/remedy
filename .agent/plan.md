# Plan — F158 Cost normalization & price catalog

## Goal
Cross-vendor money becomes comparable, honestly: one configured currency (`cost.currency`, default
usd) shared by budgets, previews, the ledger and the catalog; a versioned price catalog per adapter
with sources; each ledger call valued with a normalized cost, the pricing version and a basis
(provider_reported wins, the catalog cross-checks and warns past a threshold, a stale catalog warns
and never blocks); and `remedy worker pricing-update` imports catalogs behind a shown diff
(`docs/roadmap/features/T8_F158.md`, amendments A1 and A2). F153 waits behind F316 (D1).

## Current Step
Round 5 (session 1), T003 part 1 per DECISION F158 D6: book round 4, move the catalog's `worker`
group to its own module (structure rule 2), the update planner in
`packages/orchestration/price_catalog.py`, and `remedy worker pricing-update` with its shown
difference and `--yes`.

## Next Steps
1. Round 6, T003 part 2: the recompute of valuations after a catalog's pricing version changes,
   with the `calls` rows proven unchanged, `remedy stats cost` reporting the valuations with their
   basis and their flagged and stale prices, the docs, and the end-to-end, DECISION F158 D7.
2. The closure, in the next session: the consolidation pass, the self-use run, the one full suite,
   the evidence job, the review package and the STATUS line.

## Risks
- Catalog prices may cite only sources already on disk (DECISION F158 D2 (3)); the shipped
  catalog is empty, so the goldens use fixture catalogs.
