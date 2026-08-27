# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1–D24.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R47 makes the flight-plan approval answerable through the write door, which is
the half of DECISION F009 D5 that was planned and never shipped: the door
dispatches an `fp:`-prefixed id to `flight_plan.resolve_flight_plan_approval`,
the pending decision carries `approve` and `reject` as payload options, and
`_answerable_by_decision_resolve` mirrors the door's own two conditions. The
round also retires the duplicate contract guard R-0696 named.

## Next Steps
1. R48: the clarification FORM over `payload.clarifications`, which is what lets
   an operator answer a question instead of accepting its default.
2. A reviewer-file round landing the §3 checklist item R-0694, R-0695 and R-0696
   share: a block reads the TARGET — a predicate's refusal conditions, a test
   file's existing guards, a payload's exact-equality assertions — before
   ordering anything against it.
3. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- SIX OF THE EIGHT PRODUCING TYPES STILL CANNOT BE ANSWERED THROUGH THE DOOR
  once this round lands. R-0693 measures the gap and names `fp:` as the one
  round R47 closes; the rest are outside F031's scope, and the inbox tells the
  truth about every one of them rather than offering a button that is refused.
- APPROVING FROM THE INBOX ACCEPTS EVERY CLARIFICATION DEFAULT. DECISION F031
  D24 rules that and R48 is where an operator gains any other choice; the
  endpoint says so in its own docstring and nothing in the browser claims more.
- NO DOM HARNESS REACHES THE INBOX MARKUP, so the browser half is evidenced
  only by `apps/ui/src/api/decisionCard.test.ts` over `decisionAnswers` and by
  the comment-stripped source guards in
  `tests/ui_contracts/test_decision_answer_wiring.py`.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 252 at `a73c137e`
  and this round takes it to 251.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
