# Context — F151 Worker adapter contract v2

## Active Branch
`feature/f151-worker-adapter-contract`, from `main` at `4232c579e` (the merge of pull request 382).

## Scope
F151 as `docs/roadmap/features/T8_F151.md` states it, in the order of DECISION F151 D1: T001 the
inventory, T002 the contract and its conformance kit, T003 the reference adapter, the import guard
and the registry linkage. The open findings are all F314's; F151 takes none.

## Do not touch
Loop transport, retries and evidence, routing policy semantics, registry storage (the feature
file's Do-not-touch). Adapters build invocations and map outputs; they never retry or time out.

## Active assumptions
- The deleted `worker_registry` and main builder adapter stay deleted (DECISION F151 D1).
- The reference adapter changes no behaviour: its goldens equal today's outputs.

## Constraints
- Under 500 insertions per commit; commit subjects carry no leading-slash tokens.
- pytest runs only the round's selection, once, capped by `tests/conftest.py` (resource safety);
  the full suite runs once, in the closure.

## Steps
The item-status table of each round lives in `.agent/handoff.md`.
