# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1–D18.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R37 records R36's PASS and R-0582's recurrence, and applies that finding's own
cheaper repair: the gate transcript moves to the round report and the handback
keeps only the state the next session needs. This round writes no code.

## Next Steps
1. R38, the COMPONENT round and the LAST step of T003: thread the server token
   from `RemedyApp`'s `readUrlState` through `RemedyShell` and `RightLivePanel`,
   call `answerDecisionCard` on an answer click, render the message's sentence
   keyed by its tone, enable the buttons, and retire the three "nothing posts
   yet" sentences in `decisionCard.ts`, `decisionAnswer.ts` and
   `DecisionInboxCard.tsx`, which are true only while no component calls the
   flow.
2. The clarification FORM, and the ruling on `NeedsAttentionCard`'s decision
   branch (DECISION F031 D4).
3. The integration-gate round per `docs/agents/integration_gate.md`, whose
   block also carries the §3 checklist items R-0683, R-0377, R-0419, R-0429,
   R-0560, R-0582, R-0583 and R-0633 route there, then closure per
   `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- THE DEFAULT DEADLINE CREATES A TIMER IT CANNOT CANCEL, as
  `decisionAnswerFlow.ts`'s own header records: the `() => Promise<void>` seam
  DECISION F031 D18 chose carries no handle, so when the submit wins the
  20-second timer still fires. Named here because R38 wires it to a real click.
- THE SERVER STILL ACCEPTS A BLANK ANSWER AND WRITES IT ONCE. R29 stopped it in
  the browser only; DECISION F031 D14 routes that check to F009, not fixed here.
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 241 at `cc7f72e6` and this round leaves it there.
- The findings THIS FEATURE MUST STILL ACT ON are R-0377, R-0403, R-0413,
  R-0419, R-0429, R-0431, R-0441, R-0445, R-0471, R-0495, R-0533, R-0560,
  R-0574, R-0582, R-0583, R-0593, R-0601, R-0622, R-0625, R-0632, R-0633,
  R-0672, R-0674, R-0675, R-0676, R-0677, R-0678, R-0679, R-0683, R-0684 and
  R-0685; R-0495 and R-0574 are the two Highs.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
