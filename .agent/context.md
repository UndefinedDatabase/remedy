# Context — F314 Findings paydown v10

## Active Branch
`feature/f314-findings-paydown-v10`, from `main` at `47cdb1b06` (the merge of pull request 385).

## Scope
F314 as `docs/roadmap/features/T2_F314.md` states it: the twelve open findings it owns, one slice
per module or concern in the order of DECISION F314 D1. The finding text is the spec. R-1246,
R-1351 and R-1353 are carried by name at the closure.

## Do not touch
The resolutions F307 landed; the record is append-only (the feature file's Do-not-touch).

## Active assumptions
- No builder can reach the network: the tool sandbox unshares it (DECISION F314 D2).
- A slice that edits a structure-ledger row draws its boundary first, in a commit of its own.

## Constraints
- Under 500 insertions per commit; commit subjects carry no leading-slash tokens.
- pytest runs only the round's selection, once, capped by `tests/conftest.py` (resource safety);
  the full suite runs once, in the closure.

## Steps
The item-status table of each round lives in `.agent/handoff.md`.
