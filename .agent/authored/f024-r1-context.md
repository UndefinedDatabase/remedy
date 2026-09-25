# Context — F024 Phase timeline with scrubber

## Active Branch
feature/f024-phase-timeline-scrubber, cut from `main` at `1bb3a35d`
(the merge commit of pull request 278, F023 Semantic zoom L0–L3).

## Scope
F024 (Tier 5): the phase timeline with its scrubber — the phase mapping
table, boundary goldens and sub-glyph extraction (T001), snapshot
memoization with the prefix-equality property test (T002), and the bar,
scrubber, LIVE toggle, banner, catch-up, keyboard and end-to-end (T003),
as `docs/roadmap/features/T5_F024.md` specifies, with
`docs/ui/design_reference/ux_spec.md` §12 authoritative on the visuals.

## Do not touch
The reducer, the event schema, and story-replay narration (F039).

## Active assumptions
- Phases begin at their first marker and only move forward; Finalized
  is derived from the reducer's task states because no completion event
  exists (DECISION F024 D1).

## Constraints
- UI checks run through the pytest nodes that wrap the toolchain in the
  primary checkout: eslint in `tests/ui_contracts/test_ui_lint.py`, tsc in
  `tests/ui_server/test_dashboard_contract.py`, and vitest in
  `tests/orchestration/test_test_runner.py`.
- A round touching `docs/roadmap/**` also gates `tests/docs/`.
- Destructive verification runs only inside a disposable git worktree under
  `.remedy-wt/`, never in the primary checkout.
- Per operator amendment amend0917-throughput (2026-09-17): the full pytest
  suite runs exactly once per feature, in the closure sequence's
  integration-gate round.

## Steps
The item-status table for each round lives in that round's handback,
`.agent/handoff.md`.
