# Context — F158 Cost normalization & price catalog

## Active Branch
`feature/f158-cost-normalization`, from `main` at `407536a9b` (the merge of pull request 389).

## Scope
F158 as `docs/roadmap/features/T8_F158.md` states it, in the order of DECISION F158 D2: the
findings pass, T001 the currency consolidation, T002 the catalog and the writer's rules, T003 the
recompute, the update command and the end-to-end. F153 was moved behind F316 by DECISION F158 D1
and is not touched here. The open findings are F316's and F246's; F158 takes none.

## Do not touch
Budget mechanics (aligned, not changed), the ledger's raw capture, the bases vocabulary (the
feature file's Do-not-touch).

## Active assumptions
- No paid model call is made outside a round that orders one by name.
- No price is invented: a catalog price cites a source on disk, else the model stays unpriced.

## Constraints
- Under 500 insertions per commit; commit subjects carry no leading-slash tokens.
- pytest runs only the round's selection, once, capped by `tests/conftest.py` (resource safety);
  the full suite runs once, in the closure.

## Steps
The item-status table of each round lives in `.agent/handoff.md`.
