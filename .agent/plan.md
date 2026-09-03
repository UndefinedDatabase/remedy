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

Round 9, session 3 — THE WIRING ROUND, the third and last clause of T001.
All seven inventoried call sites route through the seam in one change,
because all seven already funnel through `resolve_role_config`: that
function now calls `route_role_call` and carries the routed-call evidence
on the `RoleConfig` it already returns. DECISION F110 D4 rules where that
evidence lands. Round 8's PASS verdict and its prose slip are booked in
the same round.

## Next Steps

- The configuration round: the per-project override map and the promotion
  evidence map are READ from configuration rather than defaulting to the
  shipped table — consolidation order E.d.
- The acceptance round: a fixture run whose every call's evidence shows
  class, tier and reason, per the feature file's Acceptance section.
- The integration gate round, before closure.
- The closure sequence, which also runs the one checklist consolidation
  pass DECISION F110 D1 carries into it, and which updates the Design
  bullet of `docs/roadmap/features/T3_F110.md`.

## Risks

- `resolve_role_config` now calls into the policy layer, so a routing fault
  could become a config-resolution fault. `repair` is the live case: it
  raises when no originating class is supplied, which is why the wiring
  answers `None` there rather than breaking a resolution that worked.
- Recording is not selecting: the seam answers a TIER and F110 maps no tier
  to a model id, so this round changes what is RECORDED and nothing about
  which model runs.
- `R-0767` stays OPEN on the same seam and must not be absorbed.
