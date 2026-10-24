# Context — F152 Worker config isolation

## Active Branch
`feature/f152-worker-config-isolation`, from `main` at `ef2b85f83` (the merge of pull request 387).

## Scope
F152 as `docs/roadmap/features/T8_F152.md` states it, in the order of DECISION F152 D1: the findings
pass, T001 the declaration, the evidence field and the throwaway home, T002 the reference adapter's
ADR then its enforcement and A/B proof, T003 doctor, the conformance-kit requirement and the docs.
The open findings are all F316's; F152 takes none.

## Do not touch
Sandbox policy semantics, adapter transport, and certification staging beyond the handshake (the
feature file's Do-not-touch).

## Active assumptions
- No paid model call is made outside a round that orders one by name.
- An environment digest is a hash of names and values that never prints a value.

## Constraints
- Under 500 insertions per commit; commit subjects carry no leading-slash tokens.
- pytest runs only the round's selection, once, capped by `tests/conftest.py` (resource safety);
  the full suite runs once, in the closure.

## Steps
The item-status table of each round lives in `.agent/handoff.md`.
