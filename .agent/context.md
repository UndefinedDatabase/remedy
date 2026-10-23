# Context — F315 The loop runs through the adapter

## Active Branch
`feature/f315-loop-through-adapter`, from `main` at `4747f2c67` (the merge of pull request 384).

## Scope
F315 as `docs/roadmap/features/T8_F315.md` states it, in the order of DECISION F315 D1: T001 the
inventory, T002 the builder and reviewer calls through the adapter, T003 the resume and parse-retry
paths and the docs. The open findings are all F314's; F315 takes none.

## Do not touch
Loop transport, retries and evidence; the routing policy; the fake and Pi providers (the feature
file's Do-not-touch). The adapter builds invocations and maps outputs; it never retries or times out.

## Active assumptions
- Orchestration imports only the contract; a concrete adapter reaches it from the wiring layer.
- Every existing claude-cli golden and integration test stays unmodified.

## Constraints
- Under 500 insertions per commit; commit subjects carry no leading-slash tokens.
- pytest runs only the round's selection, once, capped by `tests/conftest.py` (resource safety);
  the full suite runs once, in the closure.

## Steps
The item-status table of each round lives in `.agent/handoff.md`.
