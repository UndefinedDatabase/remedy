# Plan — F114 Cost preview per command

Branch: feature/f114-cost-preview-per-command, cut from `main` after
pull request 234 was merged at the Open PR Gate.

## Goal

Expensive actions stop starting silently: commands that will spend real
money show an upfront estimate band with its basis and require
confirmation above a configured threshold in attended mode; unattended
runs rely on budgets, not prompts (docs/roadmap/features/T3_F114.md).

## Current Step

Round 6 books round 5's PASS verdict (RECORD5) and starts T003's first
slice: marking which commands are expensive. Adds `is_expensive: bool =
False` to `CommandEntry` (apps/cli/command_catalog.py) and marks
`job.run` (the feature doc's "mission runs" case) as the first and only
expensive command so far. Catalog tests in tests/test_command_catalog.py
assert the field's type, that exactly `job.run` is marked, and that
`job.run.is_expensive` is True. This round does NOT wire
`confirm_cost_preview()` into `job.run`'s real execution path yet -
`_cmd_job_run_cycles` (apps/cli/commands/job.py) has no task-count/class
data to build a `CostBandEstimate` from today, and that data-gathering
design is separate, larger work.

## Next Steps

- T003 continuation: gather real task-count/class data for `job.run`
  (see `packages/orchestration/token_economy.py`'s `TokenBand`
  classification and `budget_guard.py`'s `predict_next_task_cost` for
  the existing analogous consumer pattern), then wire
  `confirm_cost_preview()` into `_cmd_job_run_cycles`
  (apps/cli/commands/job.py).
- T003 continuation: goldens for the preview line, docs
  (docs/roadmap/features/T3_F114.md's "Suggested tests:
  tests/cli/test_cost_preview.py" path does not exist yet).
- Acceptance fixtures, the integration gate, then the closure sequence.
- Session note: this is round 6, session 2 of F114 (session 1 closed at
  round 5 per amend0827 rule 6's 4-5 default).

## Risks

- `job.run` is marked expensive but still has zero confirm-path callers
  after this round - same "proven live only by mutation red-proof, not a
  real caller yet" shape as T001/T002's modules, now also true of the
  catalog flag itself until the next round wires it.
- Only one command is marked so far; the feature doc's "rerunning
  subtrees" and "long explanations" cases still need their own fixture
  commands identified before they can be marked too.