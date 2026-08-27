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
R62 is a record round and touches no file outside `.agent/`. It writes the R61
verdict, which PASSED on every gate, and it is the LAST round of its session:
its handback is the session terminator and the next session resumes from it. No
finding is resolved and none is registered. No production code, no `docs/` file
and no decision this round.

## Next Steps
1. The MARKUP half: the card renders a field per open clarification, collects
   them into the map, and passes it to the flow R61 widened.
   `tests/ui_contracts/test_decision_answer_wiring.py` pins the card's call
   string at `answerDecisionCard(target, decision, answer.value)`, so that
   round moves the guard with the call it pins.
2. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- THE SEAM IS WIDENED AND NO CALLER USES IT YET. `answerDecisionCard` takes the
  map and forwards it; the card still calls with three arguments, so the form is
  reachable only from a test until the markup half lands.
- SIX OF THE EIGHT PRODUCING TYPES STILL CANNOT BE ANSWERED THROUGH THE DOOR.
  R-0693 measures the gap; the rest are outside F031's scope, and the inbox
  tells the truth about every one of them rather than offering a refused button.
- THIS FILE NAMES NO ROUND NUMBER IT HAS NOT BEGUN. Twice a pre-assigned label
  went stale the moment a round was inserted ahead of it; a step is named by
  what it does, and its number is knowable only when it starts.
- THE HANDBACK CAP IS BEING MET BY DECLARATION RATHER THAN BY FITTING. R-0582
  records the drift and gained an instance at the R60 gate; the live repair is
  a block that orders less into the handback, and this block orders the shape.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 252 at `81a9fad6`
  and this round moves it by nothing.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
