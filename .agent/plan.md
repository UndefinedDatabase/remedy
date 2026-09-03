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

Round 5, session 1 — T002b, the THREE HARD RULES the policy document and
`docs/roadmap/features/T3_F110.md` both name, each shipped as its own
named check that returns the rule's name when violated: a reviewer never
routed weaker than its paired worker, orchestrator and mission-compile
calls always top tier, and a safety-relevant class never below mid. Each
rule gets a violating fixture that is refused with the rule named, which
is the feature file's own acceptance wording. Round 4's PASS verdict is
booked in the same round.

## Next Steps

- T002c: the config schema and per-project overrides, where the hard
  rules always win and a violating override fails validation naming the
  rule — the checks this round ships are what that validation calls.
- T003: the promotion-evidence discipline, the evidence fields and the
  goldens — a promotion without evidence refused, with evidence logged.
- Then the per-call-site class declarations (consolidation order E.d),
  the integration gate, and the closure sequence, which also runs the one
  checklist consolidation pass DECISION F110 D1 carries into it.

## Risks

- The safety-relevant class set is EMPTY in production today, because the
  policy document scopes it to "fence/DoD evaluation prompts, if any
  become LLM calls" and none is one yet. The check is therefore proven
  against a fixture set so it is not a rule that can never fire.
- Nothing routes in production yet: the table and its rules are pinned
  before any call site declares a class (order E.d).
- `R-0767` stays OPEN on the same seam and must not be absorbed.
