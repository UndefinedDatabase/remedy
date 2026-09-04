# Context — F114 Cost preview per command

## Active Branch
feature/f114-cost-preview-per-command, cut from `main` at the merge
commit of pull request 234.

## Scope
F114 (Tier 3, depends on F103 — done; enhanced by F074 calibration, not
yet built): commands that will spend real money show an upfront estimate
band with its basis and require confirmation above a configured
threshold in attended mode; unattended runs rely on budgets, not
prompts. Task slicing: T001 the shared estimator extraction + band
computation + basis labels + unit tests; T002 the CLI helper + threshold
+ tty/non-tty semantics + tests; T003 marking the expensive commands +
goldens for their preview lines + docs.

## Do not touch
The interactive guard's package boundary
(`tests/test_no_interactive_guard.py`, `_GUARDED_PACKAGES` / empty
`_ALLOWLIST`), budget enforcement, calibration (F074) — all explicitly
out of scope per `docs/roadmap/features/T3_F114.md` Do not touch.
Confirmation prompts live in `apps/cli` ONLY, never inside a guarded
package.

## Assumptions
- `packages/orchestration/budget_resolution.PredictiveBudgetConfig` /
  `resolve_predictive_budget_config()` already supply the reusable
  inputs (price basis + per-`TokenBand` class-default tokens); only the
  one-line multiply at `budget_guard.py:482-484` needs extracting, not a
  new config layer.
- `apps/cli/commands/loop_cmd.py` already has the reusable confirm
  pattern: `_confirm_materialization` (an `input()` y/N prompt),
  `_stdin_is_a_tty`, and the `--yes` flag
  (`apps/cli/command_catalog.py:653`) — T002 reuses this shape rather
  than inventing a second one.
- No `cost_preview.py` or expensive-command registry exists today
  (confirmed by search); T001/T003 are new files, not refactors of
  existing ones.
- The estimator commits to `token_economy.TokenBand` (LOW/MEDIUM/HIGH)
  as its class vocabulary, distinct from `model_routing.TASK_CLASS_TIERS`
  (a cost TIER, not a token-size band) — round 3 states this explicitly
  in `cost_preview.py`'s own docstring.

## Constraints
The bullets in this first group are STANDING project constraints, carried
forward from the context this file replaced.

- A round touching `docs/roadmap/**` also gates
  `tests/orchestration/test_roadmap_index.py` beside `tests/docs/`.
- A round rewriting `.agent/` state gates the four state readers:
  `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
  `tests/regression/test_resource_safety.py` and
  `tests/orchestration/test_integrity_gate.py`.
- Every handback runs the canary `pytest tests/cli/test_golden_path.py`.
- Destructive verification runs only inside a disposable git worktree,
  never in the primary checkout, which satisfies `git status --porcelain`
  empty at every verdict.
- THE FOUR STATE READERS ARE RUN AS FOUR, NOT AS THREE.
- `ruff check` is DENIED to this session's reviewer, measured at the
  F114 claim (`ruff check packages/orchestration/budget_guard.py`
  answers "This command requires approval"). A round of F114 that ships
  a `.py` file gates `python3 -m py_compile <path>` instead, and the
  worker attempts `ruff check` itself, reporting success or the exact
  refusal.

This round is NOT UI work — no design-reference binding applies.

## Steps
The item-status table for each round lives in that round's handback,
`.agent/handoff.md`, which AGENTS.md's "Completion Report — Item-Status
Table" section requires of every completion report. This file deliberately
does not restate it.