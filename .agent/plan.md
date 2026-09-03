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

Round 18 — CLOSURE ROUND 3: THE BUILT STATE SECTION. Round 17's evidence
job and review zip are booked (`Gate: F110 R17`, PASS): package
`remedy-review-20260903-181544-READY_FOR_REVIEW.zip`, SHA-256
`767304077110354d0005b2f6c70cd53502b831c4161be6a5f6a65a31c136457b`,
accepted HEAD `953cade0`. This round gives
`docs/roadmap/features/T3_F110.md` its Built State section and corrects
two Design bullets against what actually shipped (the module is
`model_routing.py`, not `routing.py`; a violating override WARNS per
DECISION F110 D5, it does not fail validation) — both as APPENDED "AS
BUILT" corrections, never a silent rewrite of the original intent text.

## Next Steps

- Round 19: the closure commit — the authored STATUS `[x]` line and the
  README capability sync in the SAME commit, `SU-006`'s `consumed_by` set
  to `F110`, and the pull request.

## Risks

- The zip already built at round 17 is the one closure references; round
  19 does not rebuild it.
- `R-0767` stays OPEN on the same seam and must not be absorbed.
- `R-0784` stays OPEN; its fix belongs to F258's generator, not to F110.