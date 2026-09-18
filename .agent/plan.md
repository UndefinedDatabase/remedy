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

ROUND 6 — the `teacher ask` grounding source `teacher ask` never had:
`SOURCE_STUDY` in `packages/orchestration/teacher_qa.py`, threaded through
`ask_teacher` and `_cmd_teacher_ask`, which fetches every `machine-study`
card for the resolved project, deduplicated by key keeping only the
NEWEST value per key (a repeated `study run` on the same project appends
rather than overwrites, per the memory store's own append-only design —
the same staleness-by-recency pattern `context_summary.py` already
applies elsewhere), and renders them as one `[study]` prompt block.
`docs/agents/teacher_conventions.md` gains a fourth grounding-source
bullet to match.

## Next Steps

1. T003 — the three-step proved end to end against a foreign repository
   fixture: `study run` then `teacher ask` genuinely answering from what
   it found.
2. Closure sequence.

## Risks

- None new this round.
