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

Round 13, session 3 — THE EVIDENCE WIRING, the last unbuilt clause of T003.
The config-reading layer reads `model_routing.promotion_evidence`, parses it
through the round-12 parser, and hands the records BOTH to the table builder,
so a documented benchmark run licenses a cheaper tier, AND to the seam, so a
routed call's `promoted_by` names the run. Round 12's PASS verdict and one
prose slip are booked in the same round.

## Next Steps

- The acceptance round: a fixture run whose every call's evidence shows
  class, tier and reason, per the feature file's Acceptance section, plus
  the reviewer/worker pairing assertion that section also names.
- The integration gate round, before closure.
- The closure sequence, which also runs the one checklist consolidation
  pass DECISION F110 D1 carries into it, and which updates the Design and
  Task-slicing bullets of `docs/roadmap/features/T3_F110.md`.

## Risks

- Two consumers each read and parse the evidence table; `get_config` is
  cached so the cost is small, and keeping the existing signatures was
  judged worth more than saving it.
- A malformed evidence record fails CLOSED — the promotion it would have
  licensed is refused and the class keeps its seeded tier.
- `R-0767` stays OPEN on the same seam and must not be absorbed.
