# Plan — F254 Model alias table & dead-model doctor check

Branch: feature/f254-model-alias-table · claimed `[~]` in
docs/roadmap/STATUS.md. PR #185 (S1+S2 self-drive skill) was merged at
R1's Open PR Gate. 0 open findings; next free finding ID R-0217.
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
R7 — first commit: persist the R6 PASS verdict, register finding
R-0216 and fix it. Then the integration gate per
docs/agents/integration_gate.md: the first and only full-suite run of
this feature, and the only round permitted to claim "full suite
green". A regression there is a normal repair round, not a crisis.
Both of the feature file's acceptance criteria are already met and
pinned; nothing else is owed before closure.

## Next Steps
- R8: closure per docs/roadmap/STATUS_closure_protocol.md — the
  evidence job and a fresh review zip are mandatory there, a zip
  failure is a closure blocker, and the STATUS line flips to `[x]`
  last, followed by the PR. The PR is NOT merged in the same session
  that creates it; it merges at the NEXT work item's Open PR Gate,
  which is the operator's manual-review window.
- Carried past this feature: .agent/candidates.md holds the R-0214
  handoff-cap amendment. It is a block condition at the next feature
  claim and must be registered or resolved by the first reviewed round
  of whatever comes next.
- Also carried: the four reviewer-authoring findings of this feature
  (R-0211 through R-0213 and R-0216) are all Done, but two of them
  were the same defect — a FROM that edits a list must span the whole
  list. That belongs in reviewer conventions, not only in a branch's
  live review; whoever runs closure should consider filing it as a
  second closure candidate rather than letting it die with the branch.

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
