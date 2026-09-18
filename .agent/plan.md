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

ROUND 5 — fix two defects the reviewer found in round 4's CLI wiring
before they block T003. R-0960 (Medium): `study run` now resolves its
project scope through `resolve_scope`, the SAME mechanism `teacher ask`
uses, so both commands agree on one registered project id for one
repository — falling back to the raw path with an honest warning only
when no project is registered. R-0959 (Low): a direct test now proves
`"study.run"` is a real key of `collect_all_handlers()`'s result, not
just present in the catalog.

## Next Steps

1. The `teacher ask` memory-card grounding source (`SOURCE_STUDY` in
   `packages/orchestration/teacher_qa.py`) — it has none today.
2. T003 — the three-step proved end to end against a foreign repository
   fixture.
3. Closure sequence.

## Risks

- None new this round; the two fixes above were caught before landing
  anything that depended on them.
