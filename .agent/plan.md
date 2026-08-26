# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1–D19.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R42 records R41's PASS, registers the two findings that gate raised, repairs the
51-line plan R41 shipped, and lands DECISION F031 D19 with its roadmap mirror.
It is a state round: no code, no test. Neither finding is fixed here — R-0692's
repair IS this file, and R-0693's is the three-round programme D19 rules.

## Next Steps
1. R43: `build_decision_inbox` gains a third derived key and the card renders no
   button the door refuses — D19 clause one and clause three.
2. R44: the `fp:`-prefixed dispatch DECISION F009 D5 planned and did not ship,
   reusing `flight_plan.resolve_flight_plan_approval`. Then R45: the
   clarification FORM over `payload.clarifications`.
3. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- SEVEN OF THE EIGHT PRODUCING TYPES CANNOT BE ANSWERED THROUGH THE DOOR, and
  every one ships an enabled button today. `escalation.find_task_decision`
  matches escalation records alone, so at `59521bf5` every id but a task
  decision's is answered 409. R-0693 measures it and D19 rules the repair.
- NO DOM HARNESS REACHES THE INBOX MARKUP. `apps/ui/vitest.config.ts` collects
  `src/**/*.test.ts`, so the wiring is gated by comment-stripped SOURCE reading
  and by `tsc --noEmit`, never by a rendered click. R-0689, R-0690 and R-0691
  guard that gap, and a source guard pins containment, not completeness.
- THE DEFAULT DEADLINE CREATES A TIMER IT CANNOT CANCEL, as
  `decisionAnswerFlow.ts`'s own header records: the seam DECISION F031 D18 chose
  carries no handle, so when the submit wins the 20-second timer still fires.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 247 at `59521bf5`
  and this round takes it to 249.
- The findings THIS FEATURE MUST STILL ACT ON are R-0377, R-0403, R-0413,
  R-0419, R-0429, R-0431, R-0441, R-0445, R-0471, R-0495, R-0533, R-0560,
  R-0574, R-0582, R-0583, R-0593, R-0601, R-0622, R-0625, R-0632, R-0633,
  R-0672, R-0674, R-0675, R-0676, R-0677, R-0678, R-0679, R-0683, R-0684,
  R-0685, R-0691, R-0692 and R-0693; R-0495, R-0574 and R-0693 are the Highs.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
