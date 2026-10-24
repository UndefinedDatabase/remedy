# Context — F162 Sandbox profiles per adapter

## Active Branch
`feature/f162-sandbox-profiles`, from `main` at `39beac4e1` (the merge of pull request 388).

## Scope
F162 as `docs/roadmap/features/T8_F162.md` states it, in the order of DECISION F162 D1: the findings
pass, T001 the profile schema, built-ins and tighten-only comparator, T002 process-level enforcement
per dimension with platform honesty, T003 adapter defaults, evidence, the optional container stage
with its ADR and the honesty document. The open findings are all F316's; F162 takes none.

## Do not touch
Exec-guard internals (extended, not forked), isolation HOME mechanics, air-gap policy (the feature
file's Do-not-touch).

## Active assumptions
- No paid model call is made outside a round that orders one by name.
- A dimension a platform cannot enforce is recorded unenforced, never faked.

## Constraints
- Under 500 insertions per commit; commit subjects carry no leading-slash tokens.
- pytest runs only the round's selection, once, capped by `tests/conftest.py` (resource safety);
  the full suite runs once, in the closure.

## Steps
The item-status table of each round lives in `.agent/handoff.md`.
