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

ROUND 4 — CLI wiring. `study run [--path PATH] [--project PROJECT] [--json]`
(new `apps/cli/commands/study_cmd.py`, wired into `collect_all_handlers`)
calls `run_study` with `study_call_fn()` as the default `call_fn`. DECISION
F266 D3: the new `study` group ships `user_facing=False` (advanced/internal,
like `patch`/`test`/`brain`), not added to the operator-pinned
`VISIBLE_GROUP_ORDER` — that promotion is F268's call, when `remedy do`
actually drives it. Books R-0958's resolution from round 3.

## Next Steps

1. T003 — the three-step proved end to end against a foreign repository
   fixture, including the new memory-card grounding source for
   `teacher ask` (it has none today).
2. Closure sequence.

## Risks

- `teacher ask` has no memory-card retrieval path today (measured round
  1): T003 must add one, which is more than wiring three commands
  together and should be sized as its own round.
