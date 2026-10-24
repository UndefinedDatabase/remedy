# Plan — F158 Cost normalization & price catalog

## Goal
Cross-vendor money becomes comparable, honestly: one configured currency (`cost.currency`, default
usd) shared by budgets, previews, the ledger and the catalog; a versioned price catalog per adapter
with sources; each ledger call valued with a normalized cost, the pricing version and a basis
(provider_reported wins, the catalog cross-checks and warns past a threshold, a stale catalog warns
and never blocks); and `remedy worker pricing-update` imports catalogs behind a shown diff
(`docs/roadmap/features/T8_F158.md`, amendments A1 to A3). F153 waits behind F316 (D1).

## Current Step
Round 7 (session 2), the closure's integration-gate round: book round 6 and register R-1471;
repair R-1471 in `docs/guides/do-run-v1.md`; the checklist's consolidation pass; the closure's
self-use item run to its approval gate, never applied; the one full suite and its CPU cost.

## Next Steps
1. Round 8: book round 7 with R-1471 resolved and any self-use run defect registered; the evidence
   script, the evidence bundle and the review package.
2. Round 9: the Built State, the ledger rotation, the STATUS acceptance with its README sync and
   the self-use queue's `consumed_by`, and the pull request, left unmerged for the next session.

## Risks
- Catalog prices may cite only sources already on disk (DECISION F158 D2 (3)); the shipped
  catalog is empty, so a priced valuation needs an imported catalog.
- A red full suite turns round 8 into a repair round (amend0917-throughput rule 2).
