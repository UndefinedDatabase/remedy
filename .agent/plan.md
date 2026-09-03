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

Round 8, session 2 — T001, the CALL-SITE AND ROLE INVENTORY and the
ROUTING SEAM. Every role Remedy resolves a runtime config for declares a
task class; the policy document's own repair-prompt rule, pinned as a
string since round 4, becomes executable; and the set of provider-call
sites is checked by an AST sweep against a declared constant, so a new
call site cannot land undeclared. Round 7's PASS verdict, its prose slip
and DECISION F110 D3 are booked in the same round.

## Next Steps

- The wiring round: the existing call sites route through the seam, and
  the override map and evidence map are READ from configuration instead
  of being passed in.
- The integration gate round, before closure.
- The closure sequence, which also runs the one checklist consolidation
  pass DECISION F110 D1 carries into it, and which updates the Design
  bullet of `docs/roadmap/features/T3_F110.md` so the roadmap names the
  orchestration class set DECISION F110 D2 widened.

## Risks

- Five of the seven call sites pass the role as a variable, so the
  inventory pins the call SITES rather than the role strings; a role
  reaching the resolver dynamically is still caught by that module's own
  unknown-role warning.
- Nothing is wired yet and no config file is read: the declaration lands
  before the wiring, deliberately.
- `R-0767` stays OPEN on the same seam and must not be absorbed.
