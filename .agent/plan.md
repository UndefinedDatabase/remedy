# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1–D25.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R48 finishes R47 and repairs it. R47 landed the door's `fp:` dispatch and the
`approve`/`reject` options but left `tests/ui_server/` RED on an import guard
its block never widened, and never reached the door's tests, the answerability
mirror or the browser proof. R48 registers the three defects — all three in the
reviewer's block, not in the worker's execution — greens the tip, then lands
the three missing pieces.

## Next Steps
1. R49: the clarification FORM over `payload.clarifications`, which is what lets
   an operator answer a question instead of accepting its default.
2. A reviewer-file round landing the §3 checklist item R-0694 through R-0699 now
   share: a block reads the TARGET before ordering anything against it — every
   guard whose ruled set the change widens, every constant a test compares
   against, and every fixture whose state decides an outcome.
3. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- SIX OF THE EIGHT PRODUCING TYPES STILL CANNOT BE ANSWERED THROUGH THE DOOR
  once this round lands. R-0693 measures the gap and names `fp:` as the one
  R47 and R48 close between them; the rest are outside F031's scope, and the
  inbox tells the truth about every one of them.
- APPROVING FROM THE INBOX ACCEPTS EVERY CLARIFICATION DEFAULT. DECISION F031
  D24 rules that and R49 is where an operator gains any other choice.
- SIX CONSECUTIVE ROUNDS HAVE NOW RAISED A REVIEWER-SPEC DEFECT with one root
  cause — a block ordering something against a file it had not read. Step 2
  above is the fix and it is the highest-value work left in this feature.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 251 at `20eabead`
  and this round takes it to 254.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
