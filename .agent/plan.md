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

Round 2, session 1 — T001b, the single resolver seam. The T001a inventory
measured model selection as FOUR rival mechanisms; this round removes the
worst of them by making `packages/orchestration/pingpong_job.py` resolve
its builder and reviewer provider names through `role_config` instead of
the literal `"fake"`. Round 1's PASS verdict is booked into the ledger in
the same round, and `R-0768` is resolved BY NAME because its expected fix
and consolidation order E.a are the same edit.

## Next Steps

- T001c: consolidation order E.b — read `orchestrator.model` THROUGH
  role_config so the orchestrator stops being a third answer to "which
  model". E.c is deliberately NOT done: rebinding
  `make_structured_call_fn`'s Ollama planner is failover work and the
  feature file puts it out of scope.
- T002: the resolver proper — the class table seeded from
  `docs/agents/model_routing_policy.md`, the config schema, the hard-rule
  checks, and one violating fixture per rule refused with the rule named.
- T003: the promotion-evidence discipline, the evidence fields and the
  goldens — a promotion without evidence refused, with evidence logged.
- The integration gate, then the closure sequence, which also runs the one
  checklist consolidation pass DECISION F110 D1 carries into it.

## Risks

- E.a changes what an unflagged run RECORDS and therefore what it runs.
  Six CLI-handler tests encoded the old default and are repaired in the
  same round; a seventh moving test is a finding, not a fixture to patch.
- `R-0767` stays OPEN on the same seam. It widens a CLI allow-list and
  must not be absorbed into a routing commit.
