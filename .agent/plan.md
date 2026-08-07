# Plan — F254 Model alias table & dead-model doctor check

Branch: feature/f254-model-alias-table · claimed `[~]` in
docs/roadmap/STATUS.md. PR #185 (S1+S2 self-drive skill) was merged at
R1's Open PR Gate. 0 open findings — R-0211, R-0212 and R-0213 were
all raised against the reviewer's own authoring and each was fixed in
the round that followed; next free finding ID R-0214.

## Goal
Every hardcoded default model id moves behind ONE alias module, and
`remedy doctor` gains a check that flags any configured or default
model id sitting on a config-driven known-dead list. Done when doctor
flags a dead id in a fixture and a repo scan proves no hardcoded dated
model string survives outside the alias module.

## Current Step
R4 — first commit: persist the R3 PASS verdict and register finding
R-0213. Then the known-dead model list: a shipped JSON data file, a
loader module that merges it with an operator config extension, and
unit tests. The `remedy doctor` wiring is deliberately NOT in this
round — changing the doctor's JSON contract is a separate risk and
gets its own round.

## Next Steps
- R5: wire the dead-model check into `remedy doctor core`, whose
  output names the offending id, where it came from (config vs
  built-in default) and the alias to update.
- R6: the repo-scan test proving no built-in model id survives outside
  the alias module, plus the docs/ update this feature owes — the alias
  module is new architecture and AGENTS.md requires it documented and
  registered in the docs/README.md index.
- R7: the integration gate per docs/agents/integration_gate.md.
- R8: closure per docs/roadmap/STATUS_closure_protocol.md — the
  evidence job and a fresh review zip are mandatory there, and a zip
  failure is a closure blocker.

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
