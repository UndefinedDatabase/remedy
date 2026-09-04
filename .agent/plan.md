# Plan — F114 Cost preview per command

Branch: feature/f114-cost-preview-per-command, cut from `main` after
pull request 234 was merged at the Open PR Gate.

## Goal

Expensive actions stop starting silently: commands that will spend real
money show an upfront estimate band with its basis and require
confirmation above a configured threshold in attended mode; unattended
runs rely on budgets, not prompts (docs/roadmap/features/T3_F114.md).

## Current Step

Round 7 books round 6's PASS verdict (RECORD6) and continues T003:
`job.run` gets a new `--yes` arg (`apps/cli/command_catalog.py`),
mirroring `loop.run`'s own `--yes` shape, to skip the cost-preview
confirmation prompt. A catalog test confirms it exists and is a flag.
This round still does NOT call `confirm_cost_preview()` from
`_cmd_job_run_cycles` - investigation found `job.run` has no per-task
class data before it starts (no `TokenBand` classification happens until
a task is pulled), so the real estimate `job.run` can honestly build is
"unavailable" (`band_usd_high=None`), which A9 already treats as
expensive - always confirm unless `--yes` or `--unattended`. Wiring that
call is round 8, once `--yes` exists for it to reference.

## Next Steps

- T003 continuation (round 8): import `confirm_cost_preview` and
  `CostBandEstimate` into `apps/cli/commands/job.py`; call it once near
  the top of `_cmd_job_run_cycles`, before either the single-cycle
  short-circuit (`_cmd_run_next_task_local`) or the full `run_cycles`
  path, with `basis="estimate_unavailable"` and
  `yes=(yes_flag or unattended)` - `--unattended` maps to skip-prompt
  because the feature doc requires unattended runs to never prompt and
  rely on budgets instead (T3_F114.md's own explicit rule).
- T003 continuation: goldens for the preview line, docs.
- Acceptance fixtures, the integration gate, then the closure sequence.
- Session note: round 7, session 2 of F114.

## Risks

- `job.run`'s `--yes` arg exists after this round but has zero real
  effect until round 8 wires the confirm call - same "schema before
  behavior" shape as round 6's own `is_expensive` mark.
- The "estimate unavailable" design means job.run will ALWAYS show the
  cost-preview prompt (or need --yes/--unattended) once wired, never a
  real dollar band, until a future round teaches it to classify pending
  tasks before running. This is honest (A9: unknown is expensive), not a
  shortcut, but it is a real UX gap worth flagging to the operator.