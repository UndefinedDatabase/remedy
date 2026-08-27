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
R53 builds the MODEL and COMMAND halves of the FORM and stops there. The card
model gains the plan's open questions from `payload.clarifications`, and the
answer builder learns to carry the `answers` map R51's door already validates.
Both halves are pure and the shipped vitest config reaches both, which is why
the markup is R54: DECISION F031 D5 rules branching into this layer.

## Next Steps
1. R54: the COMPONENT half — the pending card renders a field per open
   clarification and the flow carries the map this round builds.
   `tests/ui_contracts/test_decision_answer_wiring.py` pins the card's call
   string and its two-writer count, so that round moves those guards with it.
2. A reviewer-file round landing the §3 checklist item R-0694 through R-0699
   share: a block reads the TARGET before ordering anything against it — every
   guard whose ruled set the change widens, every constant a test compares
   against, and every fixture whose state decides an outcome.
3. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- SIX OF THE EIGHT PRODUCING TYPES STILL CANNOT BE ANSWERED THROUGH THE DOOR.
  R-0693 measures the gap; the rest are outside F031's scope, and the inbox
  tells the truth about every one of them rather than offering a refused button.
- THE FORM IS REACHABLE ONLY BY A NON-BROWSER CLIENT UNTIL R54. This round moves
  the seam to the edge of the markup and no further.
- TWO WHOLE-MODEL `toEqual` ASSERTIONS IN `decisionCard.test.ts`, counted at
  `e62726c7`, PIN EVERY KEY OF `DecisionCardModel`, so a new field turns them
  red in the commit that adds it. That is the guard working, not a regression.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 255 at `e62726c7`
  and this round leaves it at 255.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
