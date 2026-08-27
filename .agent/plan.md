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
R54 is the REVIEWER-FILE round, and it now runs BEFORE the markup rather than
after it. R53's probes exposed a second checklist gap — a block ordered a vitest
red-proof inside a worktree by a route that cannot run there, and whose
whole-root control is red UNMUTATED — so the markup round, which needs exactly
such probes, would walk into the same trap. This half registers R-0703 and
re-sequences; the checklist edit follows, and the markup becomes R55.

## Next Steps
1. R55: the COMPONENT half — the pending card renders a field per open
   clarification and the flow carries the map R53 built.
   `tests/ui_contracts/test_decision_answer_wiring.py` pins the card's call
   string and its two-writer count, so that round moves those guards with it.
2. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- SIX OF THE EIGHT PRODUCING TYPES STILL CANNOT BE ANSWERED THROUGH THE DOOR.
  R-0693 measures the gap; the rest are outside F031's scope, and the inbox
  tells the truth about every one of them rather than offering a refused button.
- THE FORM IS REACHABLE ONLY BY A NON-BROWSER CLIENT UNTIL R55. R53 moved the
  seam to the edge of the markup and no further.
- A VITEST RED-PROOF IN A WORKTREE NEEDS BOTH `--config <primary>` AND A SCOPED
  SELECTION. R-0653's own resolution recorded this at F022 R7 and nothing
  promoted it into the checklist, which is why R53's block repeated it.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 255 at `1bff8736`
  and R-0703 takes it to 256.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
