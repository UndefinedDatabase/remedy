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

Round 11, session 3 — THE REPAIR ROUND. Round 10 was gated FAIL: its
production work is correct and stays, but the branch tip ships a red suite
and a committed test file fails ruff. `R-0787` (High) is a config test
double that asserted an exact key and so refused the second, legitimate
reader the F110 wiring added; `R-0788` (Low) is an unsorted import block.
Both are registered, then fixed, and no file under `packages/` or `apps/`
is touched.

## Next Steps

- The promotion-evidence round: the evidence map is read from configuration
  too, so a documented benchmark run can license a cheaper tier — the last
  unbuilt clause of T003.
- The acceptance round: a fixture run whose every call's evidence shows
  class, tier and reason, per the feature file's Acceptance section.
- The integration gate round, before closure.
- The closure sequence, which also runs the one checklist consolidation
  pass DECISION F110 D1 carries into it, and which updates the Design
  bullet of `docs/roadmap/features/T3_F110.md`.

## Risks

- A test double that is too permissive stops proving anything, so the
  refusal `R-0787` removes is replaced by a positive test that reads the
  keys the stub recorded, and that test is red-proofed.
- `R-0767` stays OPEN on the same seam and must not be absorbed.
