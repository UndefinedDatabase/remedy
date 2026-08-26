# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1–D21.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R44 repairs the key R43 landed. `answerable_by_decision_resolve` reported True
for an ALREADY-ANSWERED task decision, which the door refuses 409, so the helper
gains the OPEN condition the door itself applies, with the test that
discriminates it. The round also records R43's PASS, registers R-0695 and lands
DECISION F031 D21, which moves the browser half to R45.

## Next Steps
1. R45: the browser half of D19 — `DecisionCardModel` gains the field and
   `DecisionInboxCard` renders a non-answerable card's `next_actions` as
   pasteable TEXT rather than as a posting button.
2. R46: the `fp:`-prefixed dispatch DECISION F009 D5 planned and did not ship,
   reusing `flight_plan.resolve_flight_plan_approval`. Then R47: the
   clarification FORM over `payload.clarifications`.
3. A reviewer-file round landing the §3 checklist item R-0694 and R-0695 share.
4. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- SEVEN OF THE EIGHT PRODUCING TYPES CANNOT BE ANSWERED THROUGH THE DOOR, and
  every one still ships an enabled button until R45. R-0693 measures it, D19
  rules it, and the wire carries the fact from R43 on.
- THE DOOR'S PREDICATE IS TWO CONDITIONS, NOT ONE: the record must EXIST and be
  OPEN. R43 encoded only the first, no fixture answered a decision before
  reading the card, and the suite stayed green over a value that was false for
  every answered task decision. R-0695 carries the measurement.
- NO DOM HARNESS REACHES THE INBOX MARKUP. `apps/ui/vitest.config.ts` collects
  `src/**/*.test.ts`, so R45's component change will be gated by
  comment-stripped SOURCE reading and by `tsc --noEmit`, never by a rendered
  click. R-0689, R-0690 and R-0691 are the guards written against that gap.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 250 at `46ae059f`
  and this round takes it to 251.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
