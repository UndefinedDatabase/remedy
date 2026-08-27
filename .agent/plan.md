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
All six rules are on disk and the candidates file is empty. C7 writes the
state files and the branch is pushed for review.

| Item | Status | Reason |
|------|--------|--------|
| C0 — plan and context | done | |
| C1 — prose_slips.md + AGENTS.md (rules 1, 2, 3, 6) | done | |
| C1b — cap sweep: handback_template, split_workflow | done | rule 3 lived in 4 files |
| C2 — planner_reviewer_prompt.md (rules 1-6) | done | |
| C3 — self_drive_protocol.md (rules 1, 4, 5, 6) | done | |
| C4 — candidates worked off; R-0430/0582/0676/0700 resolved | done | rule 3 |
| C5 — session number in template and operator brief | done | rule 6 |
| C6 — state files, push, PR | in progress | |

## Next Steps
1. Push, open the pull request, watch the hosted run to green, merge at the
   Open PR Gate.
2. The next session claims the next feature per Rule A5. `.agent/candidates.md`
   is EMPTY, so no block condition stands.

## Risks
- The change set includes `AGENTS.md`, which the single-session micro-round
  type does not name among its allowed paths. The operator prompt authorizes
  it explicitly; it is declared in the handoff rather than assumed.
- Rule 3 resolves four open findings by amendment rather than by repair.
  That is the operator's decision and is recorded as such, so a later reader
  does not read the `Done:` texts as evidence of a fix that never ran.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 253 at this
  branch point and 249 now, measured: findings 270 unchanged, Done 17 to 21.
