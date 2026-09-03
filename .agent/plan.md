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

Round 14, session 4 — THE R-0789 REPAIR AND THE PAIRING ACCEPTANCE. Two
deliberate-absence notes that round 13's own wiring falsified are repaired in
one commit, in `model_routing.py` and in `config.py`. The feature file's last
unbuilt acceptance clause — the reviewer/worker pairing asserted on a REAL
fixture round — is built as tests that resolve BOTH halves of a round through
the production seam under four real configurations, including the one where a
documented benchmark run is supplied for the reviewer class and the hard rule
refuses the table anyway. Round 13's PASS verdict, the finding and two prose
slips are booked in the same round.

## Next Steps

- The integration gate round, which docs/agents/integration_gate.md governs
  and which needs the R-0736 base-worktree mtime-parity repair and a cold
  `dist` build budgeted for.
- The closure sequence, which takes two rounds, runs the one §3 checklist
  consolidation pass DECISION F110 D1 carries into it, and updates the Design
  and Task-slicing bullets of `docs/roadmap/features/T3_F110.md`.

## Risks

- The pairing acceptance rests on `REVIEWER_WORKER_CLASS_PAIRS` holding at
  least one pair whose halves are both declared by a role; SPEC (c1) asserts
  exactly that, so an emptied table is reported as a failure rather than as a
  vacuous pass.
- `R-0767` stays OPEN on the same seam and must not be absorbed.
