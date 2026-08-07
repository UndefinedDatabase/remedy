# Plan — F254 Model alias table & dead-model doctor check

Branch: feature/f254-model-alias-table · claimed `[~]` in
docs/roadmap/STATUS.md. PR #185 (S1+S2 self-drive skill) was merged at
R1's Open PR Gate. 0 open findings; next free finding ID R-0215.
R-0211, R-0212 and R-0213 were reviewer-authoring defects, each fixed
in the round after it was raised. R-0214 is different: it is a rule
this project keeps overriding, and it leaves the branch as a closure
candidate in .agent/candidates.md.

## Goal
Every hardcoded default model id moves behind ONE alias module, and
`remedy doctor` gains a check that flags any configured or default
model id sitting on a config-driven known-dead list. Done when doctor
flags a dead id in a fixture and a repo scan proves no hardcoded dated
model string survives outside the alias module.

## Current Step
R5 — first commit: persist the R4 PASS verdict, register finding
R-0214, record DECISIONS D12 and D13, and file the handoff-cap
conflict in .agent/candidates.md so it survives this branch. Then wire
the dead-model check into `remedy doctor core`: a WARNING that names
the offending id, whether it came from a built-in default or a config
key, and the alias to repoint — while a list that cannot be READ stays
a hard failing check.

## Next Steps
- R6: the repo-scan test proving no built-in model id survives outside
  the alias module, plus the docs/ update this feature owes — the alias
  module and the dead-model list are new architecture and AGENTS.md
  requires them documented and registered in the docs/README.md index.
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
