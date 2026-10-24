# Plan — F158 Cost normalization & price catalog

## Goal
Cross-vendor money becomes comparable, honestly: one configured currency (`cost.currency`, default
usd) shared by budgets, previews, the ledger and the catalog; a versioned price catalog per adapter
with sources; each ledger call valued with a normalized cost, the pricing version and a basis
(provider_reported wins, the catalog cross-checks and warns past a threshold, a stale catalog warns
and never blocks); and `remedy worker pricing-update` imports catalogs behind a shown diff
(`docs/roadmap/features/T8_F158.md`, amendments A1 to A3). F153 waits behind F316 (D1).

## Current Step
Round 6 (session 1), T003 part 2 per DECISION F158 D7: book round 5, the recompute and the summary
in `packages/orchestration/call_valuation.py`, `remedy stats recompute-costs` and `remedy stats
valuations`, `docs/system/price-catalog-v1.md`, amendment A3, and the end-to-end. With it T001 to
T003 are built.

## Next Steps
1. The closure, in session 2 (STATUS_closure_protocol.md): book round 6; the Built State; the
   checklist consolidation pass; the self-use run; the one full suite with its transcript.
2. The evidence job and the review package, then the ledger rotation, the STATUS acceptance with
   its README sync, and the pull request, left unmerged for the next session's Open PR Gate.

## Risks
- Catalog prices may cite only sources already on disk (DECISION F158 D2 (3)); the shipped
  catalog is empty, so a priced valuation needs an imported catalog.
