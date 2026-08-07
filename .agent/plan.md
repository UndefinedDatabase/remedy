# Plan — F254 Model alias table & dead-model doctor check

Branch: feature/f254-model-alias-table · claimed `[~]` in
docs/roadmap/STATUS.md. PR #185 (S1+S2 self-drive skill) was merged at
R1's Open PR Gate. 0 open findings — R-0211 was raised against the
reviewer's own authoring and fixed inside R2; next free finding ID
R-0212.

## Goal
Every hardcoded default model id moves behind ONE alias module, and
`remedy doctor` gains a check that flags any configured or default
model id sitting on a config-driven known-dead list. Done when doctor
flags a dead id in a fixture and a repo scan proves no hardcoded dated
model string survives outside the alias module.

## Current Step
R2 — first commit: persist the R1 PASS verdict, register finding
R-0211 and record DECISION D10. Then the alias module
packages/orchestration/model_aliases.py as the single source of
Remedy's built-in default model ids, with all five ids relocated behind
it (role_config.py's provider table and ClaudeProvider's default) and
covered by tests/orchestration/test_model_aliases.py. Pure relocation:
no model id changes value, so every existing test that pins a dated id
must stay green.

## Next Steps
- R3: the config-driven known-dead list and the `remedy doctor` check,
  whose output names the offending id, where it came from (config vs
  built-in default) and the alias to update.
- R4: the repo-scan test proving no dated model string survives outside
  the alias module, plus the docs/ update this feature owes — the alias
  module is new architecture and AGENTS.md requires it documented and
  registered in the docs/README.md index.
- Then the integration gate, then closure per
  docs/roadmap/STATUS_closure_protocol.md (evidence job + a fresh
  review zip are mandatory).

## Risks
- This is the S4 rehearsal: Phases 1 and 2 of the self-drive protocol
  run for real for the first time. A protocol gap found here is a
  finding, and fixing it may cost a round.
- Hard date 2026-08-12 for the SSH-only operator constraint; today is
  2026-08-07.
- Live provider probing is a Non-goal, so the dead list is data the
  operator maintains rather than something Remedy discovers. The check
  is therefore only as fresh as its data file — the doctor output must
  say so instead of implying it knows the provider's real state.
