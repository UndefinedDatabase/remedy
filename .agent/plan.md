# Plan — F158 Cost normalization & price catalog

## Goal
Cross-vendor money becomes comparable, honestly: one configured currency (`cost.currency`, default
usd) shared by budgets, previews, the ledger and the catalog; a versioned price catalog per adapter
with sources; each ledger call valued with a normalized cost, the pricing version and a basis
(provider_reported wins, the catalog cross-checks and warns past a threshold, a stale catalog warns
and never blocks); and `remedy worker pricing-update` imports catalogs behind a shown diff
(`docs/roadmap/features/T8_F158.md`, amendments A1 to A3). F153 waits behind F316 (D1).

## Current Step
Round 8 (session 2), the closure's evidence round: book round 7 with R-1471 resolved and R-1472
registered for F316; the evidence script; the staging reclaim, the evidence job `f158r8e1001` and
the review package.

## Next Steps
1. Round 9, the closing round: book round 8; the Built State; the ledger rotation; SU-084's
   `consumed_by` with the STATUS acceptance and its README sync; the pull request, left unmerged
   for the next session's Open PR Gate.

## Risks
- Catalog prices may cite only sources already on disk (DECISION F158 D2 (3)); the shipped
  catalog is empty, so a priced valuation needs an imported catalog.
- A package that builds BLOCKED_EVIDENCE turns round 9 into a repair round.
