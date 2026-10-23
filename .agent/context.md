# Context — F133 Provider trust score

## Active Branch
`feature/f133-provider-trust-score`, from `main` at `11fda065b` (the merge of pull request 381).

## Scope
F133 as `docs/roadmap/features/T7_F133.md` states it, in the order of DECISION F133 D1: T001 the
inventory, T002 the aggregation, T003 the stats view and the routing-context note. The open findings
are all F314's; F133 takes none.

## Do not touch
Routing decisions, tournament machinery, promotion discipline (the feature file's Do-not-touch).
Trust informs routing and never overrides it.

## Active assumptions
- The deleted provider-trust pair stays deleted (DECISION F133 D1).
- A metric with no recorded source is shown as missing, never estimated.

## Constraints
- Under 500 insertions per commit; commit subjects carry no leading-slash tokens.
- pytest runs only the round's selection, once, capped by `tests/conftest.py` (resource safety);
  the full suite runs once, in the closure.

## Steps
The item-status table of each round lives in `.agent/handoff.md`.
