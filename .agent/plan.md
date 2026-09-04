# Plan — F114 Cost preview per command

Branch: feature/f114-cost-preview-per-command, cut from `main` after
pull request 234 was merged at the Open PR Gate.

## Goal

Expensive actions stop starting silently: commands that will spend real
money show an upfront estimate band with its basis and require
confirmation above a configured threshold in attended mode; unattended
runs rely on budgets, not prompts (docs/roadmap/features/T3_F114.md).

## Current Step

Round 2 books round 1's PASS verdict (RECORD1) and extracts the shared
cost-arithmetic helper: `token_economy.tokens_to_cost_usd()` (new, pure,
None-propagating) replaces the inlined multiply at
`budget_guard.py:482-484` inside `predict_next_task_cost`, which now
calls it. Round 1's plan text named the wrong regression suite
(`test_budget_guard.py`); the real coverage of `predict_next_task_cost`
is `tests/orchestration/test_predictive_budget.py`, and the new
function's own unit tests land in
`tests/orchestration/test_token_economy.py` (both suites, plus
`test_budget_guard.py` itself, gate this round).

## Next Steps

- Round 3: `packages/orchestration/cost_preview.py` (`estimate_cost_band`,
  band computation from `PredictiveBudgetConfig`'s per-`TokenBand` class
  defaults, basis labels, "estimate unavailable" when no price basis) +
  `tests/orchestration/test_cost_preview.py` — completes T001.
- T002: CLI helper (`apps/cli`) — threshold confirm, tty/non-tty
  semantics (pipe never hangs), `--yes` audited, reusing
  `loop_cmd.py`'s `_confirm_materialization`/`_stdin_is_a_tty` pattern.
- T003: mark expensive commands in `apps/cli/command_catalog.py`,
  goldens for preview lines, docs.

## Risks

- No `cost_preview.py` or expensive-command registry exists yet — T003
  is greenfield, not a rename.
- The estimator commits to `token_economy.TokenBand`, distinct from
  `model_routing.TASK_CLASS_TIERS` (round 3 states which and why).