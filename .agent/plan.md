# Plan — amend0827-process-diet

Branch: feature/amend0827-process-diet, cut from `main` at `f4eae1d4`, the
merge commit of pull request #215 which closed F031. Operator collection
order amend0827, no self-drive loop; the operator prompt carries the
authorization for every decision below, including the six process rules.

## Goal
Cut the process overhead the F031 measurement exposed. Six operator-decided
rules land as dated amendments in AGENTS.md,
docs/agents/planner_reviewer_prompt.md and
docs/agents/self_drive_protocol.md, each with one sentence of reason and a
reversal instruction. The four `.agent/candidates.md` entries left by the
F031 closure are worked off in the same order, which unblocks the next
feature claim.

## Current Step
C0 lands this file and `.agent/context.md`. Then the amendments, then the
candidates.

| Item | Status | Reason |
|------|--------|--------|
| C0 — plan and context | in progress | |
| C1 — prose_slips.md + AGENTS.md (rules 1, 2, 3, 6) | open | |
| C2 — planner_reviewer_prompt.md (rules 1-6) | open | |
| C3 — self_drive_protocol.md (rules 1, 4, 5, 6) | open | |
| C4 — candidates worked off; R-0430/0582/0676/0700 resolved | open | rule 3 |
| C5 — handoff | open | |

## Next Steps
1. Land C1 through C5, gate each against the four state readers and the
   docs gate, then push and open the pull request.
2. The next session claims the next feature per Rule A5 with an empty
   `.agent/candidates.md`.

## Risks
- The change set includes `AGENTS.md`, which the single-session micro-round
  type does not name among its allowed paths. The operator prompt authorizes
  it explicitly; it is declared in the handoff rather than assumed.
- Rule 3 resolves four open findings by amendment rather than by repair.
  That is the operator's decision and is recorded as such, so a later reader
  does not read the `Done:` texts as evidence of a fix that never ran.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 253 at this
  branch point and 249 after C4.
