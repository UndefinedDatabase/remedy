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

Round 6, session 2 — T002c, the PER-PROJECT OVERRIDE SCHEMA. An override
map is validated before it is applied: every violation is collected and
named, a malformed entry is reported rather than crashed on, and an
override breaking a hard rule is REFUSED rather than silently dropped,
because a dropped override leaves the operator believing it took effect.
`mission` joins the orchestration class set per DECISION F110 D2, so an
override demoting it is refused by name. Round 5's PASS verdict and that
DECISION are booked in the same round.

## Next Steps

- T003: the promotion-evidence discipline, the evidence fields and the
  goldens — a promotion without evidence refused, with evidence logged.
- The per-call-site class declarations and the resolver seam
  (consolidation order E.d), which is where the override map is finally
  READ from a config file instead of being passed in.
- Then the integration gate, and the closure sequence, which also runs
  the one checklist consolidation pass DECISION F110 D1 carries into it.

## Risks

- The safety-relevant class set is EMPTY in production today, so the
  safety rule is proven against a fixture set in its override-map form
  exactly as it already is in its per-choice form.
- Nothing routes in production yet and no config file is read: the schema
  validates a mapping handed to it, and the reader that produces that
  mapping arrives with the seam round.
- `R-0767` stays OPEN on the same seam and must not be absorbed.
