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

Round 12, session 3 — THE PROMOTION-EVIDENCE SCHEMA. `config.py` learns
that a table-valued key can declare what its ENTRIES hold, F110 registers
`model_routing.promotion_evidence` as a table of records, and
`model_routing` gains a PURE parser turning that raw mapping into
`PromotionEvidence`. Nothing is wired: no call reads the key yet, so the
schema is pinned before routing behaviour moves. Round 11's PASS verdict is
booked and `R-0787` and `R-0788` are resolved.

## Next Steps

- The wiring round: `resolve_effective_task_class_tiers` reads the evidence
  table too and passes it to the builder and to the seam, so a documented
  run actually licenses a cheaper tier at a routed call.
- The acceptance round: a fixture run whose every call's evidence shows
  class, tier and reason, per the feature file's Acceptance section.
- The integration gate round, before closure.
- The closure sequence, which also runs the one checklist consolidation
  pass DECISION F110 D1 carries into it, and which updates the Design
  bullet of `docs/roadmap/features/T3_F110.md`.

## Risks

- `config.py` is read by 25 test files, so the gate list for a change in
  that layer is deliberately wider than round 10's, which shipped a red
  tip from a suite outside the narrow set.
- A malformed evidence record fails CLOSED — the promotion it would have
  licensed is refused — which is the opposite direction from a malformed
  override, and both are stated in code.
- `R-0767` stays OPEN on the same seam and must not be absorbed.
