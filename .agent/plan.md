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

Round 16, session 5 — CLOSURE ROUND 1: THE SELF-USE PRECONDITION AND THE
CHECKLIST-CONSOLIDATION RULING. Round 15's PASS verdict (the integration
gate: branch clean, both base-only failures attributed to the XDIST-FLAKE
class, no blocker) is booked. Closure precondition 6's self-use item is
generated (the queue is exhausted at 0 pending), planned and RUN for real
through the shipped generator and runner, mirroring F109 R19's own
precedent exactly — never promoted, never faked. DECISION F110 D6 rules on
the section-3 consolidation pass DECISION F110 D1 committed to: it ran,
found two real merge candidates, and performed neither, because
renumbering would falsify roughly 2,013 existing by-number citations the
append-only ledger forbids correcting; the checklist stays at 37 items,
amend0827 rule 4's "same length" branch.

## Next Steps

- Round 17: register the self-use run's defects (if any) as findings, run
  the evidence job and build a FRESH review zip, and give
  `docs/roadmap/features/T3_F110.md` its Built State section plus the
  Design/Task-slicing bullet updates.
- Round 18: the closure commit — the authored STATUS line, the README
  capability sync in the same commit, the self-use item's `consumed_by`
  set to `F110`, and the PR.

## Risks

- The self-use run may land `blocked` at its own approval gate (F109's
  SU-005 did) — a normal outcome per `self_use_runner`'s own docstring,
  not a failure of this round; its defects route to round 17's findings.
- `R-0767` stays OPEN on the same seam and must not be absorbed.
