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

Round 15, session 5 — THE INTEGRATION GATE, the tier-3 full-suite gate this
feature owes before closure. `docs/agents/integration_gate.md` steps 1-5 run
against the branch and against the merge base in a throwaway worktree, with the
base-worktree UI parity restored the way findings R-0591 and R-0736 require and
BOTH comparison sets attributed the way R-0590 requires. The evidence lands
under `.agent/gate_f110_r15/`. Round 14's PASS verdict, the resolution of
`R-0789` and one prose slip are booked in the same round. This round changes no
code: a red gate is handed back, never repaired here.

## Next Steps

- The closure sequence, which takes two rounds, runs the one §3 checklist
  consolidation pass DECISION F110 D1 carries into it, needs an evidence job
  and a FRESH review zip, and updates the Design and Task-slicing bullets of
  `docs/roadmap/features/T3_F110.md`.
- The STATUS line and the closure pull request, which the operator merges at
  the next feature's Open PR Gate.

## Risks

- The base worktree is the known-fragile half: without the R-0591 symlink
  argument and the R-0736 mtime advance it produces false base failures by the
  hundred, so the gate reports `_frontend_is_stale()` from inside that tree
  before the run rather than after it.
- `R-0767` stays OPEN on the same seam and must not be absorbed.
