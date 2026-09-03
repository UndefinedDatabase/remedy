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

Round 7, session 2 — T003, the PROMOTION-EVIDENCE DISCIPLINE. Moving a
class to a CHEAPER tier is refused unless a documented benchmark run
backs it: no evidence, incomplete evidence and below-threshold evidence
are each refused with their own rule name, the bars are seeded from the
policy document's "Promotion rule" section and pinned to it by a sync
test, and every routed call can report which evidence promoted it. Round
6's PASS verdict and its two prose slips are booked in the same round.

## Next Steps

- The resolver seam and the per-call-site task-class declarations
  (consolidation order E.d): the single place model selection happens,
  where the override map and the evidence map are finally READ from
  configuration instead of being passed in.
- The integration gate round, before closure.
- The closure sequence, which also runs the one checklist consolidation
  pass DECISION F110 D1 carries into it, and which updates the Design
  bullet of `docs/roadmap/features/T3_F110.md` so the roadmap names the
  orchestration class set DECISION F110 D2 widened.

## Risks

- The safety-relevant class set is EMPTY in production today, so that
  rule is proven against a fixture set in both its per-choice and its
  override-map form.
- Nothing routes in production yet and no config file is read: the schema
  and the evidence discipline validate mappings handed to them.
- `R-0767` stays OPEN on the same seam and must not be absorbed.
