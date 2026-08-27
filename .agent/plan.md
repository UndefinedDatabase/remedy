# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1–D22.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R45 carries answerability into the browser, which is DECISION F031 D19's second
clause and the half D20 split off. `DecisionCardModel` gains the endpoint's third
key, every answer gains a `posts` flag derived from it, and `DecisionInboxCard`
renders a non-posting answer as pasteable TEXT rather than as a button the write
door would refuse. It also records R44's PASS and lands DECISION F031 D22.

## Next Steps
1. R46: the `fp:`-prefixed dispatch DECISION F009 D5 planned and did not ship,
   reusing `flight_plan.resolve_flight_plan_approval`. Then R47: the
   clarification FORM over `payload.clarifications`.
2. A reviewer-file round landing the §3 checklist item R-0694 and R-0695 share:
   a block computing a value from another module's predicate reads that
   predicate's OWN refusal conditions, not merely its route to the data.
3. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- AFTER THIS ROUND THE INBOX STILL OFFERS NO WAY TO ANSWER SEVEN OF THE EIGHT
  PRODUCING TYPES — it stops LYING about them, which is D19's whole claim, and
  R46 is where the `fp:` prefix gains a real dispatch. R-0693 measures the gap.
- NO DOM HARNESS REACHES THE INBOX MARKUP. `apps/ui/vitest.config.ts` collects
  `src/**/*.test.ts` and no DOM environment ships, so this round's component
  change is gated by comment-stripped SOURCE reading in
  `tests/ui_contracts/test_decision_answer_wiring.py` and by `tsc --noEmit`.
- THE REGION GUARD FORBIDS AN OPERATOR, NOT AN ORDER: the reader between the
  last `</button>` and the outcome `<p` rejects `?`, `&&` and `||`, so a correct
  render written in the other order goes red for an unrelated-looking reason.
- THE DEFAULT DEADLINE CREATES A TIMER IT CANNOT CANCEL, as
  `decisionAnswerFlow.ts`'s own header records: the seam DECISION F031 D18 chose
  carries no handle, so when the submit wins the 20-second timer still fires.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 251 at `f98a91cd`
  and this round does not move it.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
