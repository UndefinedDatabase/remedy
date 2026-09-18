# Plan — F266 remedy study (repo comprehension pass)

Branch: feature/f266-remedy-study, cut from `main` at the merge commit of
pull request 254 (F281's closure).

## Goal

The three-step `remedy init` → `remedy study` → `remedy teacher` runs on an
arbitrary repository: `study` performs a bounded, read-only comprehension
pass and files APPROVED memory cards carrying `provenance: "machine-study"`
(DECISION D-C, `docs/roadmap/features/T4_F266.md`), and `teacher ask`
answers questions about that repository from those cards.

## Current Step

ROUND 2 — T001, the bounded comprehension pass. `packages/orchestration/study.py::run_study`
walks a repository (bounded entry cap, honest partial result), detects structure/core
modules/conventions/entry points heuristically, and optionally narrates each category through
an injectable `call_fn` bounded by the existing `should_stop`/`evaluate_budget` machinery
(`max_provider_calls`), falling back to the heuristic value on exhaustion or on any call_fn
exception — it never crashes. Each category is written as one card via `store_memory(...,
provenance="machine-study")`, so T002's auto-approval connects end to end this round. Read-only
against the studied repository, proved by a hash-tree test.

## Next Steps

1. CLI wiring — a standalone `study` command in the catalog, plus the
   `resolve_role_config("study", ...)` bridge call site (with the matching
   `ROLE_CONFIG_CALL_SITES` inventory update).
2. T003 — the three-step proved end to end against a foreign repository
   fixture, including the new memory-card grounding source for
   `teacher ask`.
3. Closure sequence.

## Risks

- `teacher ask` has no memory-card retrieval path today (measured round
  1): T003 must add one, which is more than wiring three commands
  together and should be sized as its own round.
