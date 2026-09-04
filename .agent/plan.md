# Plan — F114 Cost preview per command

Branch: feature/f114-cost-preview-per-command, cut from `main` after
pull request 234 was merged at the Open PR Gate.

## Goal

Expensive actions stop starting silently: commands that will spend real
money show an upfront estimate band with its basis and require
confirmation above a configured threshold in attended mode; unattended
runs rely on budgets, not prompts (docs/roadmap/features/T3_F114.md).

## Current Step

Round 5 books round 4's PASS verdict (RECORD4) and completes T002: the
new shared module `apps/cli/cost_preview_confirm.py`
(`render_estimate_line`, `confirm_cost_preview`, `EXIT_USAGE`) reuses
`loop_cmd.py`'s tty/prompt shape, calling round 4's
`resolve_confirm_above_usd()` and T001's `estimate_cost_band()`. Its
tests land in `tests/cli/test_cost_preview_confirm.py`. No real command
calls it yet - that is T003, a separate future round.

## Next Steps

- T003: mark expensive commands in `apps/cli/command_catalog.py`, wire
  them to `confirm_cost_preview()`, goldens for the preview lines, docs.
- Acceptance fixtures, the integration gate, then the closure sequence.
- Session note: this is round 5 of the 4-5 default; the next round is a
  natural point to consider a fresh session per amend0827 rule 6, unless
  context remains ample.

## Risks

- No expensive-command registry exists yet - T003 is greenfield.
- T003 will be the first round with a REAL production caller; until
  then, both `cost_preview.py` and `cost_preview_confirm.py` are
  fully-tested but uncalled code, proven live only by their own
  mutation red-proofs.