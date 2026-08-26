# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1–D20.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R43 lands DECISION F031 D19's first clause: `build_decision_inbox` gains a third
derived key saying whether the write door's `decision.resolve` can answer this
card, computed with the door's OWN predicate rather than a type check. It also
records R42's PASS, registers R-0694 and lands D20, which splits D19's R43 into
an endpoint round and a browser round because one round cannot hold both.

## Next Steps
1. R44: the browser half of D19 — `DecisionCardModel` gains the field and
   `DecisionInboxCard` renders a non-answerable card's `next_actions` as
   pasteable TEXT rather than as a posting button.
2. R45: the `fp:`-prefixed dispatch DECISION F009 D5 planned and did not ship,
   reusing `flight_plan.resolve_flight_plan_approval`. Then R46: the
   clarification FORM over `payload.clarifications`.
3. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- SEVEN OF THE EIGHT PRODUCING TYPES CANNOT BE ANSWERED THROUGH THE DOOR, and
  every one still ships an enabled button until R44. R-0693 measures it, D19
  rules it, and this round only makes the fact visible on the wire.
- NO FIXTURE CAN TELL THE DOOR'S PREDICATE FROM A TYPE CHECK, because branch 8
  derives its id FROM the escalation record, so the two coincide everywhere.
  R43's guard against that drift is a documented deliberate absence, not a test,
  and the block says so rather than implying coverage it does not have.
- NO DOM HARNESS REACHES THE INBOX MARKUP. `apps/ui/vitest.config.ts` collects
  `src/**/*.test.ts`, so R44's component change will be gated by
  comment-stripped SOURCE reading and by `tsc --noEmit`, never by a rendered
  click. R-0689, R-0690 and R-0691 are the guards written against that gap.
- THE DEFAULT DEADLINE CREATES A TIMER IT CANNOT CANCEL, as
  `decisionAnswerFlow.ts`'s own header records: the seam DECISION F031 D18 chose
  carries no handle, so when the submit wins the 20-second timer still fires.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 249 at `5b810e33`
  and this round takes it to 250.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
