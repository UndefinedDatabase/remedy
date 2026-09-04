# Plan — F114 Cost preview per command

Branch: feature/f114-cost-preview-per-command, cut from `main` after
pull request 234 was merged at the Open PR Gate.

## Goal

Expensive actions stop starting silently: commands that will spend real
money show an upfront estimate band with its basis and require
confirmation above a configured threshold in attended mode; unattended
runs rely on budgets, not prompts (docs/roadmap/features/T3_F114.md).

## Current Step

Round 4 books round 3's PASS verdict (RECORD3) and starts T002 (the CLI
helper): a new config key `cost_preview.confirm_above_usd` (default 0.5,
F114 Design: "around half a dollar") registers in
`packages/orchestration/config.py`, and a new resolver
`resolve_confirm_above_usd()` lands in `cost_preview.py` itself, same
env>TOML>default authority as `resolve_predictive_budget_config`. Round 5
completes T002: the actual CLI confirm helper in `apps/cli`, reusing
`loop_cmd.py`'s `_confirm_materialization`/`_stdin_is_a_tty` shape,
calling this round's resolver and `estimate_cost_band`. No CLI file is
touched this round.

## Next Steps

- Round 5: `apps/cli/cost_preview_confirm.py` (new shared module) — the
  render+confirm helper, tty/non-tty semantics (pipe never hangs),
  `--yes` audited — completing T002. Its own tests land in
  `tests/cli/test_cost_preview_confirm.py`.
- T003: mark expensive commands in `apps/cli/command_catalog.py`,
  goldens for preview lines, docs.
- Acceptance fixtures, the integration gate, then the closure sequence.

## Risks

- No expensive-command registry exists yet — T003 is greenfield.
- `apps/cli/` has no existing shared confirm/exit-code module; round 5
  creates the first one rather than extending something that exists.