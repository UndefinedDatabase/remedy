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

Round 4, session 1 — T002a, the class table itself. A new module
`packages/orchestration/model_routing.py` maps each task class the policy
document names to a model tier, and a SYNC TEST parses that document and
asserts the two agree — the acceptance line
`docs/roadmap/features/T3_F110.md` calls out by name. An unknown class
routes to the top tier with the reason `unknown_class_conservative`.
Round 3's PASS verdict is booked in the same round.

## Next Steps

- T002b: the three hard rules, each a named check with a violating fixture
  that is refused with the rule named — reviewer never weaker than its
  paired worker, orchestrator and mission-compile always top tier,
  safety-relevant classes never below mid. Deliberately NOT in round 4:
  an unenforced rule on disk is a claim its round cannot prove.
- T002c: the config schema and per-project overrides, where hard rules
  always win and a violating override fails validation naming the rule.
- T003: the promotion-evidence discipline, the evidence fields and the
  goldens — a promotion without evidence refused, with evidence logged.
- Then the per-call-site class declarations (consolidation order E.d),
  the integration gate, and the closure sequence, which also runs the one
  checklist consolidation pass DECISION F110 D1 carries into it.

## Risks

- The table is not wired to any call site yet, by design: E.d puts the
  declarations after the seam work. Nothing routes in production today.
- `apps/cli/commands/mission_cmd.py`'s `_orchestrator_call_fn` docstring
  went half-stale in round 3 and needs a later round's change set.
- `R-0767` stays OPEN on the same seam and must not be absorbed.
