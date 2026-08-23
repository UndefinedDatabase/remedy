# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the merge
commit of pull request #213 which closed F022. `.agent/live_review.md` is the
source of truth for the record and the finding-id ceiling;
`.agent/f031_inventory.md` is the measured source inventory; `.agent/decisions.md`
carries DECISION F031 D1, D2 and D3, which settle the design.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact. DONE when the inbox lists fixture
decisions of every PRODUCING type with correct blocked-size math, answering from
a card round-trips through the write channel into the same effects the CLI
produces, the badge tracks live, and ordering follows a documented rule over age
and blocked size rather than vibes.

## Current Step
R6 records the R5 verdict, registers finding R-0679, and plans T001. It writes no
production code: the next round is the first of this feature to do so.

## Next Steps
1. R7 builds T001 against the rulings: a read endpoint that derives its cards
   from `list_decisions` in `packages/orchestration/decision_queue.py` (D1 — the
   queue is a derived view, so no storage is added), carrying per card the type,
   the age, and a blocked count wired from `blocked_downstream` in
   `packages/orchestration/dag_schedule.py`, which no decision reads today.
2. R7 ships contract tests with a fixture per PRODUCING type — the eight types a
   branch of `list_decisions` emits (D3), NOT the ten of `DECISION_TYPES` — plus
   the scoping rule and the unreadable-entry honesty the feature file requires.
3. R8 records the R7 verdict and plans T002, where D2 binds: the badge
   re-derives on refetch over the existing stream and no new event kind ships.

## Risks
- Open findings, stated with the rule and the commit DECISION F009 D10 requires:
  by §3 item 10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — `
  line — the open set is 237, measured at `49c50d05`.
- The findings THIS FEATURE MUST STILL ACT ON — a narrower set, named as what it
  is and not called "open" — are R-0403, R-0413, R-0431, R-0445, R-0495, R-0533,
  R-0574, R-0601, R-0625, R-0632, R-0672, R-0674, R-0675, R-0676, R-0677, R-0678
  and R-0679, of which R-0495 and R-0574 are the two Highs, inherited from F085
  and F086.
- T001 IS THE FIRST ROUND OF THIS FEATURE TO TOUCH PRODUCTION CODE, so it is a
  SPLIT round by the §3 Round-types rule and its gates grow accordingly: the
  suites this feature has been running are state readers and will not exercise a
  new endpoint. R7's block must add the suite that does.
- The record holds `Gate: R19` from F022 as its seed entry. If F031 reaches its
  own R19 that key collides — the §3 item 26 defect. A round before then renames
  the seed or the scheme; this bullet is the reminder.
