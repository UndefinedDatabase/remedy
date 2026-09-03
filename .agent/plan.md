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

Round 10, session 3 — THE CONFIGURATION ROUND. `config.py` learns to
resolve a TABLE-VALUED key through the precedence chain it already has,
F110 registers `model_routing.task_class_tiers`, and the routing layer lays
that table over the seed mapping through the validator round 6 built. A
project can re-tier a class; it cannot re-tier one the hard rules protect,
and a refused map warns with the rule named and routes seeded — DECISION
F110 D5. Round 9's PASS verdict and its two prose slips are booked in the
same round.

## Next Steps

- The promotion-evidence round: the evidence map is read from configuration
  too, so a documented benchmark run can license a cheaper tier — the last
  unbuilt clause of T003.
- The acceptance round: a fixture run whose every call's evidence shows
  class, tier and reason, per the feature file's Acceptance section.
- The integration gate round, before closure.
- The closure sequence, which also runs the one checklist consolidation
  pass DECISION F110 D1 carries into it, and which updates the Design
  bullet of `docs/roadmap/features/T3_F110.md`.

## Risks

- `config.py` is imported almost everywhere, so the flatten change is the
  round's real blast radius; the unmoved suites are the regression evidence.
- A refused override map must not break config resolution — the round 9
  lesson one layer further out.
- `R-0767` stays OPEN on the same seam and must not be absorbed.
