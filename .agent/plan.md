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

Round 3, session 1 — T001c, consolidation order E.b. The orchestrator's
model is read today straight from the `orchestrator.model` config key at
two call sites, bypassing `role_config` entirely, so it is a third
independent answer to "which model". This round routes it through
`role_config` while keeping the config key exactly as the operator-facing
surface it already is. Round 2's PASS verdict is booked in the same round.

## Next Steps

- T002: the resolver proper — the class table seeded from
  `docs/agents/model_routing_policy.md`, the config schema, the hard-rule
  checks, and one violating fixture per rule refused with the rule named.
  Consolidation order E.d puts the per-call-site class declarations here,
  AFTER the seam work, so a declared class cannot record a routing reason
  that a rival mechanism then overrode.
- T003: the promotion-evidence discipline, the evidence fields and the
  goldens — a promotion without evidence refused, with evidence logged.
- The integration gate, then the closure sequence, which also runs the one
  checklist consolidation pass DECISION F110 D1 carries into it.

## Risks

- E.b is behaviour-neutral at today's configuration: the two sources
  already answer the same model id. That is measured, not assumed, and it
  is why the round's tests use a patched discriminator rather than
  comparing the two sources.
- E.c is deliberately NOT done. Rebinding `make_structured_call_fn`'s
  Ollama planner is failover work and the feature file puts it out of
  scope; the inventory's section G records the distinction.
- `R-0767` stays OPEN on the same seam and must not be absorbed.
