# Plan — F114 Cost preview per command

Branch: feature/f114-cost-preview-per-command, cut from `main` after
pull request 234 was merged at the Open PR Gate.

## Goal

Expensive actions stop starting silently: commands that will spend real
money show an upfront estimate band with its basis and require
confirmation above a configured threshold in attended mode; unattended
runs rely on budgets, not prompts (docs/roadmap/features/T3_F114.md).

## Current Step

Round 10 adds T003's docs item: a new user guide,
`docs/guides/cost-preview-user-guide-v0.md`, documenting `job.run`'s
cost-preview behavior end to end - the estimate line, the basis label,
the `cost_preview.confirm_above_usd` config key, `--yes`, `--unattended`,
and the non-tty exit-2-with-hint path - and registers it in
`docs/README.md` (Quick-Find Table + Guides section). No production
code or test changes this round.

## Next Steps

- T003 continuation: consider marking other "rerunning subtrees" /
  "long explanations" commands `is_expensive` - only `job.run` so far.
- Real cost bands for `job.run` still do not exist - a future round
  needs real task-class data to replace the unavailable estimate.
- Acceptance fixtures continue; the integration gate, then the closure
  sequence (PR, Open PR Gate). No PR exists yet.
- Session note: round 10, session 3 - 1 delegated round this session so
  far, at the 4-5 default.

## Risks

- Docs-only round: no gate over packages/apps/ this round beyond the
  standing .agent-state readers and the docs link-check suite.
- The guide documents behavior round 8/9 already gated; a future
  behavior change to cost_preview.py or cost_preview_confirm.py must
  update this guide in the same round (named here so it is not missed).