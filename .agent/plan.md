# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the merge
commit of pull request #213 which closed F022. `.agent/live_review.md` is the
source of truth for the record, the round map and the finding-id ceiling;
`.agent/f031_inventory.md` is the measured source inventory R3 landed.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via decision events
driving the badge, with branch-only blocking semantics intact. DONE when the
inbox lists fixture decisions of every producing type with correct blocked-size
math, answering from a card round-trips through the write channel into the same
effects the CLI produces, the badge tracks live, and ordering follows a
documented rule over age and blocked size rather than vibes.

## Current Step
R4 records the R3 verdict and the R-0601 recurrence, and carries the inventory's
consequences into this plan. It rules nothing: the design questions below are
R5's, written with room to think rather than settled in a record round.

## Next Steps
1. R5 rules three things the inventory forces, each as a DECISION in
   `.agent/decisions.md`: (a) what "the decision queue" IS, since
   `decision_queue.py` performs no I/O and re-derives decisions from the job's
   events, so the feature file's "FILE-BASED (the established store with its
   CLI)" describes the event log rather than the module; (b) whether the badge
   is fed by EMITTING the decision event kinds that do not exist today or by
   re-deriving on snapshot refetch; (c) whether the two declared-but-unproduced
   types stay in the set, since a fixture per producing type is the acceptance
   criterion and two types have no producer to fixture.
2. R6 records the R5 verdict and plans T001 against whatever R5 ruled.

## Risks
- Open findings, stated with the rule and the commit DECISION F009 D10 requires:
  by §3 item 10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — `
  line — the open set is 236, measured at R3's C4.
- The findings THIS FEATURE MUST STILL ACT ON — a narrower set, named as what it
  is and not called "open" — are R-0403, R-0413, R-0431, R-0445, R-0495, R-0533,
  R-0574, R-0601, R-0625, R-0632, R-0672, R-0674, R-0675, R-0676 and R-0677, of
  which R-0495 and R-0574 are the two Highs, inherited from F085 and F086.
- THE BADGE F031 IS ASKED TO DRIVE IS A CONSTANT ZERO TODAY. `decision_count`
  and the `open_decisions` sum both count `human_decision_requested`, which no
  producer emits and which `event_schemas.py` does not declare. This is the
  largest gap between the feature file and the source, and no T-slice estimate
  is sound until R5 rules item 1(b).
- The record holds `Gate: R19` from F022 as its seed entry. If F031 reaches its
  own R19 that key collides — the §3 item 26 defect. A round before then renames
  the seed or the scheme; this bullet is the reminder.
