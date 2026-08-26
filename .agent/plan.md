# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1–D10.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R25 CLOSES T002b: the inbox card carries its own OPEN count, derived in
`decisionCard.ts` from the `isOpen` the model already sets, and the last two
comments in this feature that call counting and wiring absent are retired at
their source, each naming what falsified it.

## Next Steps
1. T003 wires answering through the existing write channel, adds the
   clarification form and the deep links, rules `NeedsAttentionCard` (DECISION
   F031 D4), and carries R-0682's `role="group"` fix in both files.
2. The integration-gate round per `docs/agents/integration_gate.md`, whose
   block also carries the §3 checklist item R-0683 routes there, then closure
   per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- THE BADGE MUST COUNT THE PROP, NOT THE VIEW. `DecisionInboxCard` holds both
  the unfiltered `decisions` prop and the filtered `view.visible`; a count taken
  from the second would drop every time a chip narrowed the list and would tell
  the operator the queue had shrunk when only their filter had.
- STILL NO TEST REACHES THE MARKUP under DECISION F031 D5, so the badge's
  RENDERING is pinned by `tsc`, structure and review, while its NUMBER is
  pinned by `decisionCard.test.ts`. Keeping the count a pure function is what
  makes that split possible.
- TWO NUMBERS NOW ANSWER ONE QUESTION from opposite sides of the wire:
  `metrics.open`, re-derived on the server at R24, and this badge, derived in
  the browser. They agree today because both read one queue through one
  endpoint, and nothing pins that agreement.
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 239 at `9ec7b2de`, and this round's C2 raises it to 240 by minting
  R-0683, in the commit order the R25 block's constraint 4 fixes.
- The findings THIS FEATURE MUST STILL ACT ON are R-0403, R-0413, R-0431,
  R-0441, R-0445, R-0471, R-0495, R-0533, R-0574, R-0593, R-0601, R-0622,
  R-0625, R-0632, R-0672, R-0674, R-0675, R-0676, R-0677, R-0678, R-0679,
  R-0682 and R-0683; R-0495 and R-0574 are the two Highs.
- BLOCK CAPS ARE TWO, not one: 490 lines TOTAL (DECISION F085 D6) and 400 lines
  PROSE (DECISION F085 D5); every block states and re-measures both.
