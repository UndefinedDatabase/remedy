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

ROUND 1 — claim F266 and settle T002's design first (per the Orchestrator
brief). DECISION D1: register the `study` role_config role (task class
`summarize`, the same cheap tier as `teacher`/`summary`; F110 deliberately
maps no tier to a model id, so `study`'s default model is the standard
provider-aware default like every other role, operator-overridable).
DECISION D2: add `provenance` to `MemoryEntry`, thread it through
`store_memory`, and make `provenance == "machine-study"` auto-approve at
creation as a data property, not a second code path.

## Next Steps

1. T001 — the bounded comprehension pass (structure, core modules,
   conventions, entry points), calling the new `study` role and stopping
   at its budget cap with an honest partial result.
2. CLI wiring — a standalone `study` command in the catalog.
3. T003 — the three-step proved end to end against a foreign repository
   fixture, including the new memory-card grounding source for
   `teacher ask`.
4. Closure sequence.

## Risks

- `teacher ask` has no memory-card retrieval path today (measured this
  round): T003 must add one, which is more than wiring three commands
  together and should be sized as its own round.
