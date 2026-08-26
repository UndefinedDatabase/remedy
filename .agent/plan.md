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
R38 is the COMPONENT round and the LAST step of T003: the server token reaches
the card, an answer click calls `answerDecisionCard`, the sentence it answers is
rendered by its tone, the buttons ship enabled, and the three sentences saying
nothing posts yet are retired. The round also records R37's PASS.

## Next Steps
1. The clarification FORM, and the ruling on `NeedsAttentionCard`'s decision
   branch (DECISION F031 D4).
2. The integration-gate round per `docs/agents/integration_gate.md`, whose block
   also carries the checklist items R-0683, R-0377, R-0419, R-0429, R-0560,
   R-0582, R-0583 and R-0633 route there, then closure per
   `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- THE DEFAULT DEADLINE CREATES A TIMER IT CANNOT CANCEL, as
  `decisionAnswerFlow.ts`'s own header records: the seam DECISION F031 D18 chose
  carries no handle, so when the submit wins the 20-second timer still fires.
  This round is the one that wires it to a real click.
- THE SERVER STILL ACCEPTS A BLANK ANSWER AND WRITES IT ONCE. R29 stopped it in
  the browser only; DECISION F031 D14 routes that check to F009, not fixed here.
- NO DOM HARNESS REACHES THIS ROUND'S MARKUP. The shipped vitest config collects
  `src/**/*.test.ts`, so the wiring is gated by comment-stripped SOURCE reading
  in `tests/ui_contracts/` and by `tsc --noEmit`, never by a rendered click.
- Open findings, by the rule and commit DECISION F009 D10 requires — every
  `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the set is 241 at
  `a1bf1f5d` and this round leaves it there.
- The findings THIS FEATURE MUST STILL ACT ON are R-0377, R-0403, R-0413,
  R-0419, R-0429, R-0431, R-0441, R-0445, R-0471, R-0495, R-0533, R-0560,
  R-0574, R-0582, R-0583, R-0593, R-0601, R-0622, R-0625, R-0632, R-0633,
  R-0672, R-0674, R-0675, R-0676, R-0677, R-0678, R-0679, R-0683, R-0684 and
  R-0685; R-0495 and R-0574 are the two Highs.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
