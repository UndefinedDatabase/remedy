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
R63 records the R62 verdict and lands the FORM RULE half of the clarification
form: one new pure module under `apps/ui/src/api/` names a field's key and
collects one decision's field values into the map the flow has accepted since
R61, with its own vitest file. No component, no stylesheet and no file under
`tests/` changes, and no finding moves in either direction.

## Next Steps
1. The MARKUP half: the card holds a field per open clarification, keys each by
   `decisionClarificationFieldKey`, collects them with
   `collectDecisionClarificationAnswers` and passes the map to
   `answerDecisionCard`. `tests/ui_contracts/test_decision_answer_wiring.py`
   pins the card's call string, so that round moves the guard with the call it
   pins, and the stylesheet gains the field rules.
2. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- THE RULE LANDS ONE ROUND BEFORE ITS ONLY CALLER. The module is reachable from
  its own vitest file alone until the markup half lands; that is ordered, and
  DECISION F031 D5 is why the rule is not written inside the card instead.
- SIX OF THE EIGHT PRODUCING TYPES STILL CANNOT BE ANSWERED THROUGH THE DOOR.
  R-0693 measures the gap; the rest are outside F031's scope, and the inbox
  tells the truth about every one of them rather than offering a refused button.
- THIS FILE NAMES NO ROUND NUMBER IT HAS NOT BEGUN. Twice a pre-assigned label
  went stale the moment a round was inserted ahead of it; a step is named by
  what it does, and its number is knowable only when it starts.
- A WORKTREE VITEST RUN OVER THE WHOLE SUITE IS RED AT BASE. A worktree carries
  no `apps/ui/node_modules`, so `react/jsx-dev-runtime` cannot resolve for the
  one test that reaches a `.tsx`; every worktree run is scoped to `src/api/`
  and passes the primary checkout's config.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 252 at `4cb80429`
  and this round moves it by nothing.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
