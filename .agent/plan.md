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
R57 is the resolution sweep. R-0695, R-0697, R-0698 and R-0699 carry code halves
that landed at R44 and R48 and process halves that landed at R56, and every one
of the four is measured on disk at this gate — each with an unmutated control
and a mutation that names the guard the fix created — and resolved. The round
also widens §3 item 35 from a MISSING list item to a WRONG round label, because
the R56 block reproduced R-0704's class inside the very slice that landed that
item's first half.

## Next Steps
1. R-0704 stays OPEN until its widened counter-measure has been measured on
   disk at a later gate, rather than being resolved by the round that writes it.
   That round also carries the item R-0694's own fix clause asks for, which
   states R-0631's append-reader rule.
2. The COMPONENT half: the pending card renders a field per open clarification
   and the flow carries the map R53 built.
   `tests/ui_contracts/test_decision_answer_wiring.py` pins the card's call
   string and its two-writer count, so that round moves those guards with it.
3. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- SIX OF THE EIGHT PRODUCING TYPES STILL CANNOT BE ANSWERED THROUGH THE DOOR.
  R-0693 measures the gap; the rest are outside F031's scope, and the inbox
  tells the truth about every one of them rather than offering a refused button.
- THIS FILE NAMES NO ROUND NUMBER IT HAS NOT BEGUN. Twice a pre-assigned label
  went stale the moment a round was inserted ahead of it; a step is named by
  what it does, and its number is knowable only when it starts.
- THE FORM IS REACHABLE ONLY BY A NON-BROWSER CLIENT until the component half
  lands. R53 moved the seam to the edge of the markup and no further.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 257 at `941b8966`
  and the four resolutions this round lands take it to 253.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
