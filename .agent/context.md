# Context — operator amendment amend1023-universe-trust

## Active Branch
`feature/amend1023-universe-trust`, from `main` at `adc9e3e96` (the merge of pull request 383,
F151, at this session's Open PR Gate).

## Scope
The operator's order of 2026-10-23 in five parts (see `.agent/plan.md`); every decision is a
DECISION amend1023 D<n> in `.agent/decisions.md`. Code, docs, commits and feature files in English.

## Do not touch
- `.data/` by direct reads: the repository's settings deny it. The live data is reached only
  through Remedy's own commands (`remedy client ...`, `remedy mission list`, `remedy job show`).
- `docs/roadmap/ROADMAP.md`.

## Active assumptions
- The probe order `luna-twmhd8` is supervisor order `048ff6987b7336bd`, mission `ed0ef1e8…`.
- The clients `orb-universe` and `orb-remedy` exist in the registry.

## Constraints
- Under 500 insertions per commit; commit subjects carry no leading-slash tokens.
- No test run until the end: one full suite run, then the repair loop, then only the affected
  test files again; never the full suite a second time for a docs repair.
- The structure ratchet's listed files and functions do not grow.
- Resource safety: pytest runs capped by `tests/conftest.py`; one full suite run, `-n auto`.

## Steps
The item-status table lives in the handback.
