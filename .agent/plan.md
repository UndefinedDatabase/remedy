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
R56 lands the remaining §3 checklist items: the one R-0694, R-0695, R-0697 and
R-0698 share — a block reads the file it orders a change against, for what that
file already holds — and the one R-0699 and R-0704 share, that a description and
the enumeration it points at are read against each other. R-0696 is already
`Done:` and its resolution routes its root cause here. R-0694's fix clause asks
for a further item stating R-0631's append-reader rule; this round does not land
it. NO FINDING IS RESOLVED THIS ROUND.

## Next Steps
1. The resolution sweep: R-0695, R-0697, R-0698 and R-0699 carry code halves
   that landed at R44 and R48 with no `Done:` paragraph, so each is re-measured
   on disk and resolved, with the process halves item 34 discharges.
2. R57, the COMPONENT half: the pending card renders a field per open
   clarification and the flow carries the map R53 built.
   `tests/ui_contracts/test_decision_answer_wiring.py` pins the card's call
   string and its two-writer count, so that round moves those guards with it.
3. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- SIX OF THE EIGHT PRODUCING TYPES STILL CANNOT BE ANSWERED THROUGH THE DOOR.
  R-0693 measures the gap; the rest are outside F031's scope, and the inbox
  tells the truth about every one of them rather than offering a refused button.
- THE MARKUP IS R57, NOT R56, and the form stays reachable only by a non-browser
  client until it lands; the R55 plan numbered it R56 over an unnumbered round.
- THE REVIEWER'S OWN BLOCK KEEPS CARRYING THE DEFECT: R54 and R55 were each
  caught by the worker, and the R55 plan's round numbering by the reviewer at
  the R55 gate. That is the split working, and why checklist rounds come first.
- FINDINGS WHOSE CODE HALF HAS LANDED ARE STILL COUNTED OPEN, because only
  reviewer-authored text sets Resolved. Step 1 above is that debt.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 257 at `58de811a`
  and this round mints no id.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
