# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1-D26.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R61 writes the R60 verdict and lands the SEAM half of the clarification form.
`buildDecisionResolveCommand` has taken the answers map since R51; neither
`buildDecisionSendRequest` nor `answerDecisionCard` forwards it, so the map R53
built cannot reach the door from any caller. This round widens both hops and
tests them under the shipped vitest config. IT TOUCHES NO COMPONENT: the card,
its stylesheet and `tests/ui_contracts/test_decision_answer_wiring.py` are all
untouched, which is why the pinned call string stays green.

## Next Steps
1. The MARKUP half: the card renders a field per open clarification, collects
   them into the map, and passes it to the widened flow.
   `tests/ui_contracts/test_decision_answer_wiring.py` pins the card's call
   string at `answerDecisionCard(target, decision, answer.value)`, so that
   round moves the guard with the call it pins.
2. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- THE FORM WAS ONE STEP AND IS NOW TWO. Seven files in one round crossed the
  block cap and put a seam change beside a markup change; the seam is reachable
  by vitest and the markup is not, so they gate differently and are split.
- SIX OF THE EIGHT PRODUCING TYPES STILL CANNOT BE ANSWERED THROUGH THE DOOR.
  R-0693 measures the gap; the rest are outside F031's scope, and the inbox
  tells the truth about every one of them rather than offering a refused button.
- THIS FILE NAMES NO ROUND NUMBER IT HAS NOT BEGUN. Twice a pre-assigned label
  went stale the moment a round was inserted ahead of it; a step is named by
  what it does, and its number is knowable only when it starts.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 252 at `486b3ef8`
  and this round moves it by nothing.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
