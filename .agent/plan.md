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

Round 1, session 1 — merge F109's pull request at the Open PR Gate, claim
F110 in the ledger, discharge the four closure candidates F109 left open,
and land T001a: the call-site and role inventory that
`docs/roadmap/features/T3_F110.md`'s Orchestrator brief requires as a
deliverable BEFORE T002. The inventory is MEASURED from the code, never
recalled.

## Next Steps

- T001b: the single resolver seam. The inventory decides whether model
  selection is already consolidated in
  `packages/orchestration/role_config.py` or must be consolidated first.
- T002: the resolver, the config schema, the hard-rule checks, and one
  violating fixture per rule, refused with the rule named.
- T003: the promotion-evidence discipline, the evidence fields and the
  goldens — a promotion without evidence refused, with evidence logged.
- The integration gate, then the closure sequence, which also runs the one
  checklist consolidation pass DECISION F110 D1 carries into it.

## Risks

- Model selection is scattered today: `resolve_role_config` has production
  callers in several modules while `make_structured_call_fn` is called at
  sites that pass no resolved model at all. Consolidation is the first
  order and it touches live call paths.
- `R-0768` is OPEN over exactly this seam. F110 must not silently absorb
  its repair; the inventory records the overlap and leaves it registered.
