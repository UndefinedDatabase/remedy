# Plan — F114 Cost preview per command

Branch: feature/f114-cost-preview-per-command, cut from `main` after
pull request 234 was merged at the Open PR Gate.

## Goal

Expensive actions stop starting silently: commands that will spend real
money show an upfront estimate band with its basis and require
confirmation above a configured threshold in attended mode; unattended
runs rely on budgets, not prompts (docs/roadmap/features/T3_F114.md).

## Current Step

Round 1, session 1 — claim F114 in the STATUS ledger and set this file
and `.agent/context.md`. Branch already cut. Round 2 extracts the shared
cost-arithmetic helper (`packages/orchestration/budget_guard.py:482-484`,
today inlined inside `predict_next_task_cost`) into
`packages/orchestration/token_economy.py` as `tokens_to_cost_usd()`, with
`predict_next_task_cost` refactored to call it (no behavior change).
Round 3 ships the new module `packages/orchestration/cost_preview.py`
(band estimator + basis labels) and its tests, completing T001.

## Next Steps

- Round 2: extract `tokens_to_cost_usd()`, refactor
  `predict_next_task_cost` to use it, regression-prove
  `tests/orchestration/test_budget_guard.py` unchanged.
- Round 3: `cost_preview.py` (`estimate_cost_band`) +
  `tests/orchestration/test_cost_preview.py` — completes T001.
- T002: CLI helper (`apps/cli`) — threshold confirm, tty/non-tty
  semantics (pipe never hangs), `--yes` audited, reusing
  `loop_cmd.py`'s `_confirm_materialization`/`_stdin_is_a_tty` pattern.
- T003: mark expensive commands in `apps/cli/command_catalog.py`,
  goldens for preview lines, docs.

## Risks

- No `cost_preview.py` or expensive-command registry exists yet — T003
  is greenfield, not a rename.
- Two class vocabularies exist (`model_routing.TASK_CLASS_TIERS` vs
  `token_economy.TokenBand`); the estimator commits to `TokenBand`
  (round 3 states which and why).