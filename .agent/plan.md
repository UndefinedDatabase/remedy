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

ROUND 3 — fix R-0958 (the `_walk_repo` dotfile-mangling defect, registered
this round) and land the `study` role's real provider bridge:
`StudyCategoryNarration` (a minimal structured schema mirroring
`GeneratedSummaryContent`), `study_call_fn()` (mirrors `summary_call_fn()`:
`resolve_role_config("study")` → `make_structured_call_fn`, adapted to
`run_study`'s existing plain-string `call_fn` contract so round 2's tests
need no changes), and the matching `ROLE_CONFIG_CALL_SITES` inventory
entry.

## Next Steps

1. CLI wiring — a standalone `study` command in the catalog, using
   `study_call_fn()` as its default `call_fn`.
2. T003 — the three-step proved end to end against a foreign repository
   fixture, including the new memory-card grounding source for
   `teacher ask`.
3. Closure sequence.

## Risks

- `teacher ask` has no memory-card retrieval path today (measured round
  1): T003 must add one, which is more than wiring three commands
  together and should be sized as its own round.
