# Plan — F114 Cost preview per command

Branch: feature/f114-cost-preview-per-command, cut from `main` after
pull request 234 was merged at the Open PR Gate.

## Goal

Expensive actions stop starting silently: commands that will spend real
money show an upfront estimate band with its basis and require
confirmation above a configured threshold in attended mode; unattended
runs rely on budgets, not prompts (docs/roadmap/features/T3_F114.md).

## Current Step

Round 8 books round 7's PASS verdict (RECORD7) and wires the real
`confirm_cost_preview()` call into `_cmd_job_run_cycles`
(`apps/cli/commands/job.py`), gating both the single-cycle short-circuit
and the full `run_cycles` path. The estimate is `CostBandEstimate(None,
None, ESTIMATE_UNAVAILABLE, {})` - honest, since `job.run` has no
per-task class data before it starts - which A9 treats as expensive, so
every call now confirms unless `--yes` or `--unattended` (mapped to
skip-prompt, per the feature doc's unattended-never-prompts rule). This
round also repairs existing `_cmd_job_run_cycles` call sites in
tests/orchestration/test_long_run_executor.py and
tests/orchestration/test_escalation.py that would otherwise trip the new
gate under pytest's non-tty stdin, and adds two new tests for the gate
itself.

## Next Steps

- T003 continuation: goldens for the preview line, docs for `--yes` and
  the cost-preview behavior.
- T003 continuation: consider marking other "rerunning subtrees" /
  "long explanations" commands `is_expensive` - only `job.run` so far.
- Acceptance fixtures, the integration gate, then the closure sequence
  (PR, Open PR Gate). No PR exists yet.
- Session note: round 8, session 2 - 3 delegated rounds this session
  (6, 7, 8), within the 4-5 default.

## Risks

- Every non-interactive `job.run` call now needs `--yes` or
  `--unattended` or it exits with EXIT_USAGE - by design (A9), but a
  real behavior change for existing automation, worth flagging to the
  operator as breaking, not additive.
- Real cost bands for `job.run` still do not exist - a future round
  needs real task-class data to replace the unavailable estimate.