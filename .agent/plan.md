# Plan — F254 Model alias table & dead-model doctor check

Branch: feature/f254-model-alias-table · claimed `[~]` in
docs/roadmap/STATUS.md. PR #185 (S1+S2 self-drive skill) was merged at
R1's Open PR Gate. 0 open findings; next free finding ID R-0216.
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
R6 — first commit: persist the R5 PASS verdict and register finding
R-0215. Then three things that finish the build: fix the doctor
warning's text-mode verbosity and its miscounted detail line; add the
repo-scan test that closes the feature's second acceptance criterion,
using the ast module so comments are out of scope by construction
rather than by allow-list; and write the docs this feature owes,
registered in the docs/README.md index.

## Next Steps
- R7: the integration gate per docs/agents/integration_gate.md — the
  first and only full-suite run before closure.
- R8: closure per docs/roadmap/STATUS_closure_protocol.md — the
  evidence job and a fresh review zip are mandatory there, a zip
  failure is a closure blocker, and the STATUS line flips to `[x]`
  last, followed by the PR. The PR is NOT merged in the same session
  that creates it.
- Carried past this feature: .agent/candidates.md holds the R-0214
  handoff-cap amendment. It is a block condition at the next feature
  claim and must be registered or resolved by the first reviewed round
  of whatever comes next.

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
