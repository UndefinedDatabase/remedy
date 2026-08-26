# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1–D17.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R33 records R32's PASS and the R-0633 recurrence R32's red proof exposed — a
reviewer gate naming a test its own mutation cannot reach. It writes no code:
the whole change set is `.agent/` state.

## Next Steps
1. R34, T003's wiring round: ship `decisionOutcome.ts`, mapping a send's result
   to the sentence and tone an operator reads; thread the server token from
   `RemedyApp`'s `readUrlState` through `RemedyShell` and `RightLivePanel`;
   call the nonce, request, submit and outcome modules on an answer click;
   enable the buttons; and retire the three "nothing posts yet" sentences in
   `decisionCard.ts`, `decisionAnswer.ts` and `DecisionInboxCard.tsx`.
2. The clarification FORM, and the ruling on `NeedsAttentionCard`'s decision
   branch (DECISION F031 D4).
3. The integration-gate round per `docs/agents/integration_gate.md`, whose
   block also carries the §3 checklist items R-0683, R-0377, R-0419, R-0429,
   R-0560 and R-0633 route there, then closure per
   `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- A SEND THAT NEVER ANSWERS HAS NO DEADLINE. `submitDecisionSendRequest` sets
  no timeout by design (DECISION F031 D16), so R34's handler must not leave a
  button disabled forever on a promise that never settles.
- THE SERVER STILL ACCEPTS A BLANK ANSWER AND WRITES IT ONCE. R29 stopped it
  in the browser only; DECISION F031 D14 routes the server-side check to F009,
  which owns the write door, and it is NOT fixed here.
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 241 at `1d29f322` and this round leaves it there; R-0633 gains a
  recurrence and stays OPEN.
- The findings THIS FEATURE MUST STILL ACT ON are R-0377, R-0403, R-0413,
  R-0419, R-0429, R-0431, R-0441, R-0445, R-0471, R-0495, R-0533, R-0560,
  R-0574, R-0593, R-0601, R-0622, R-0625, R-0632, R-0633, R-0672, R-0674,
  R-0675, R-0676, R-0677, R-0678, R-0679, R-0683, R-0684 and R-0685; R-0495
  and R-0574 are the two Highs.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
