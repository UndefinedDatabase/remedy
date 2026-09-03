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

Round 19 — THE CLOSURE COMMIT (final round of this feature). Round 18's
Built State section is booked (`Gate: F110 R18`, PASS); closure
precondition 4 is satisfied. This round books the authored STATUS `[x]`
line and the README capability paragraph in ONE commit, sets `SU-006`'s
`consumed_by` to `F110` in `scripts/self_use_queue.json`, and opens the
pull request. The PR is NOT merged this session — it merges at the next
feature's Open PR Gate, the operator's manual-review window.

## Next Steps

None — this is the feature's last round. The next session's Phase 0
finds an open, non-draft PR from this branch into `main` and merges it
at the Open PR Gate before claiming a new feature.

## Risks

- `R-0767` and `R-0784` stay OPEN; both predate F110 and are documented,
  not F110 defects — see the Built State section's own citations.
