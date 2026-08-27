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
R60 is a record round and touches no file outside `.agent/`. It writes the R59
verdict, resolves R-0631, R-0694 and R-0705 against the §3 items that landed at
`513bb9e0`, and registers the two reviewer defects the R59 worker declared
before review: an ordered-equality gate defeated by git's hunk anchoring, and a
delegation wrapper that described the block's own last line wrongly. No
production code, no `docs/` file and no decision this round.

## Next Steps
1. The COMPONENT half: the pending card renders a field per open clarification
   and the flow carries the map R53 built.
   `tests/ui_contracts/test_decision_answer_wiring.py` pins the card's call
   string and its two-writer count, so that round moves those guards with it.
2. The integration-gate round per `docs/agents/integration_gate.md`, then
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
- NO GATE COMPARES THE EMITTED BLOCK TO THE COMMITTED ONE AND NONE CAN. §3 item
  37 closes the reviewer's obligation to SAY so; the gap itself stands, and
  every transport claim is the saved copy to its mirror to disk.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 253 at `84f362e5`,
  and three closing beside two opening leaves it at 252.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
