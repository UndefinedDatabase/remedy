# Plan — F114 Cost preview per command

Branch: feature/f114-cost-preview-per-command, cut from `main` after
pull request 234 was merged at the Open PR Gate.

## Goal

Expensive actions stop starting silently: commands that will spend real
money show an upfront estimate band with its basis and require
confirmation above a configured threshold in attended mode; unattended
runs rely on budgets, not prompts (docs/roadmap/features/T3_F114.md).

## Current Step

Round 3 books round 2's PASS verdict (RECORD2) and completes T001: the
new module `packages/orchestration/cost_preview.py` (`estimate_cost_band`,
`CostBandEstimate`, `ESTIMATE_UNAVAILABLE`) computes a real USD band —
never a fabricated point — from two `TokenBand` values, a repeat count
and a `PredictiveBudgetConfig`, reusing round 2's
`token_economy.tokens_to_cost_usd()`. Its tests land in
`tests/orchestration/test_cost_preview.py`. Neither file has any
production caller yet — that is T002, next.

## Next Steps

- T002: CLI helper (`apps/cli`) — threshold confirm, tty/non-tty
  semantics (pipe never hangs), `--yes` audited, reusing
  `loop_cmd.py`'s `_confirm_materialization`/`_stdin_is_a_tty` pattern,
  calling `cost_preview.estimate_cost_band()` for the shown numbers.
- T003: mark expensive commands in `apps/cli/command_catalog.py`,
  goldens for preview lines, docs.
- Acceptance fixtures, the integration gate, then the closure sequence.

## Risks

- No expensive-command registry exists yet — T003 is greenfield.
- `estimate_cost_band`'s two-band-plus-repeat-count shape is this
  feature's own design choice (feature file gives a suggested shape
  only); T002 is where it meets real CLI call sites and may need a
  small adjustment, not a rewrite.