# Context — F157 Capability matrix & honest degradation

## Active Branch
`feature/f157-capability-matrix`, from `main` at `0f811a713` (the merge of pull request 386).

## Scope
F157 as `docs/roadmap/features/T8_F157.md` states it, in the order of DECISION F157 D1: T001 the
inventory, T002 the matrix module and its guards, T003 the consolidation per consumer, the report
section, the badge and the end-to-end. The open findings are all F316's; F157 takes none.

## Do not touch
The fallback implementations (referenced, not moved), the adapters' capability declarations and
the per-feature semantics (the feature file's Do-not-touch).

## Active assumptions
- Consumers ask the matrix, never an adapter's capabilities directly; the call takes the resolved
  model and provider pair.
- Every consolidated consumer's existing tests stay unmodified.

## Constraints
- Under 500 insertions per commit; commit subjects carry no leading-slash tokens.
- pytest runs only the round's selection, once, capped by `tests/conftest.py` (resource safety);
  the full suite runs once, in the closure.

## Steps
The item-status table of each round lives in `.agent/handoff.md`.
