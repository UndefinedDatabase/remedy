# Plan — F110 Model routing by task class

Branch: feature/f110-model-routing-by-task-class, cut from `main` after
pull request 232 was merged at the Open PR Gate.

## Goal

End one-model-for-everything: every provider call declares a TASK CLASS, a
router maps classes to model tiers, and each routed call records the routed
model WITH its reason. The hard rules of
`docs/agents/model_routing_policy.md` are ENFORCED IN CODE, and moving a
class to a cheaper tier is possible only against documented benchmark
evidence — never by editing a mapping casually.

## Current Step

Round 17 — CLOSURE ROUND 2: THE EVIDENCE JOB AND THE REVIEW ZIP. Round 16
is CLOSED: the self-use precondition ran to a real terminal state
(`SU-006`, job `6f74dd7367704fd5`, `status='blocked'` at the normal
approval gate after a cross-session resume), its two defect strings are
recorded as new evidence on the already-OPEN `R-0784` rather than as a
fresh id, and DECISION F110 D6 already ruled the checklist-consolidation
obligation discharged. This round builds the closure evidence bundle
(`f110-closure`, covering `T001`-`T003`) and a FRESH review zip over the
accepted HEAD this round creates. No STATUS line, no README edit, no
Built State section and no pull request happen here.

## Next Steps

- Round 18: give `docs/roadmap/features/T3_F110.md` its Built State
  section and its Design/Task-slicing bullet updates — split out of what
  round 16's own plan called "round 17" because bundling it with the
  evidence job and zip would put this round over the 490-line block cap.
- Round 19: the closure commit — the authored STATUS `[x]` line and the
  README capability sync in the SAME commit, `SU-006`'s `consumed_by`
  set to `F110`, and the pull request.

## Risks

- The zip is a closure BLOCKER, not a formality: a `PACKAGE_STATUS` other
  than `READY_FOR_REVIEW` stops closure rather than being worked around.
- `R-0767` stays OPEN on the same seam and must not be absorbed.
- `R-0784` stays OPEN; its fix belongs to F258's generator, not to F110.