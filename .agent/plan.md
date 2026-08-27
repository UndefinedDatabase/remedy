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
R55 lands the §3 checklist item R-0703 calls for — a vitest colour ordered
inside a worktree must name its config, scope its selection and report the
unmutated control first — and repairs this file, whose R54 revision named a
checklist round its own Next Steps list no longer held (R-0704). The markup is
renumbered to R56, and that renumbering is stated here rather than performed
silently. The R-0694 through R-0699 item is NOT in this round: those six
findings have not been re-read from the record, and an item written from memory
is the trap this list exists to close.

## Next Steps
1. The second §3 checklist item: the R-0694 through R-0699 share — a block reads
   the TARGET before ordering anything against it — landed together with the
   counter-measure R-0704 names, in a round that re-reads all seven findings
   from `.agent/live_review.md` first.
2. R56: the COMPONENT half — the pending card renders a field per open
   clarification and the flow carries the map R53 built.
   `tests/ui_contracts/test_decision_answer_wiring.py` pins the card's call
   string and its two-writer count, so that round moves those guards with it.
3. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- SIX OF THE EIGHT PRODUCING TYPES STILL CANNOT BE ANSWERED THROUGH THE DOOR.
  R-0693 measures the gap; the rest are outside F031's scope, and the inbox
  tells the truth about every one of them rather than offering a refused button.
- THE FORM IS REACHABLE ONLY BY A NON-BROWSER CLIENT UNTIL R56. R53 moved the
  seam to the edge of the markup and no further.
- TWO CONSECUTIVE ROUNDS RAISED A DEFECT IN THE REVIEWER'S OWN BLOCK, both found
  by the worker before the reviewer read the diff. That is the split working,
  but it is also why the checklist rounds outrank the markup.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 256 at `84551691`
  and R-0704 takes it to 257.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
