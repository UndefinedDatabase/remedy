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
R41 registers the one finding the R40 gate raised and records R40's PASS. It is
a state round: no code, no test. R-0691 is registered and deliberately NOT fixed
here — a substring guard cannot hold an "and nothing else" clause, so the repair
is a naming repair and it is routed to the integration-gate round rather than
earning a fourth consecutive round of guard hardening.

## Next Steps
1. The clarification FORM, and the ruling on `NeedsAttentionCard`'s decision
   branch (DECISION F031 D4).
2. The integration-gate round per `docs/agents/integration_gate.md`, whose block
   also carries the checklist items R-0683, R-0377, R-0419, R-0429, R-0560,
   R-0582, R-0583, R-0633 and R-0691 route there, then closure per
   `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- NO DOM HARNESS REACHES THE INBOX MARKUP, and it has now produced findings in
  three consecutive rounds. The shipped vitest config collects
  `src/**/*.test.ts`, so the wiring is gated by comment-stripped SOURCE reading
  and by `tsc --noEmit`, never by a rendered click. R-0686 and R-0687 were the
  markup itself; R-0689, R-0690 and R-0691 are the guards written to close them.
  A guard over source text pins what a string CONTAINS and what an enumerated
  list EXCLUDES; it cannot pin "and nothing else", and a name that says
  otherwise is the recurring defect.
- THE DEFAULT DEADLINE CREATES A TIMER IT CANNOT CANCEL, as
  `decisionAnswerFlow.ts`'s own header records: the seam DECISION F031 D18 chose
  carries no handle, so when the submit wins the 20-second timer still fires.
- THE SERVER STILL ACCEPTS A BLANK ANSWER AND WRITES IT ONCE. R29 stopped it in
  the browser only; DECISION F031 D14 routes that check to F009, not fixed here.
- Open findings, by the rule and commit DECISION F009 D10 requires — every
  `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the set is 246 at
  `3afdb209` and this round takes it to 247.
- The findings THIS FEATURE MUST STILL ACT ON are R-0377, R-0403, R-0413,
  R-0419, R-0429, R-0431, R-0441, R-0445, R-0471, R-0495, R-0533, R-0560,
  R-0574, R-0582, R-0583, R-0593, R-0601, R-0622, R-0625, R-0632, R-0633,
  R-0672, R-0674, R-0675, R-0676, R-0677, R-0678, R-0679, R-0683, R-0684,
  R-0685 and R-0691; R-0495 and R-0574 are the two Highs.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
