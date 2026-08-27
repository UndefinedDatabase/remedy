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
R49 is a RECORD ROUND and changes no executable file: it registers R-0700,
R-0701 and R-0702 and records R48's PASS. THE FLIGHT-PLAN APPROVAL IS NOW
ANSWERABLE END TO END — the door dispatches an `fp:` id to
`resolve_flight_plan_approval`, the pending card offers the two words that door
accepts, and the answerability key mirrors both of its refusal conditions — and
the branch tip is green at 486 in `tests/ui_server/` and 455 under vitest.

## Next Steps
1. R50: retire the stale round number R-0702 names in
   `packages/orchestration/ui_server.py`, extract the duplicated helper R-0701
   names, then land the clarification FORM over `payload.clarifications`.
2. A reviewer-file round landing the §3 checklist item R-0694 through R-0699
   share: a block reads the TARGET before ordering anything against it — every
   guard whose ruled set the change widens, every constant a test compares
   against, and every fixture whose state decides an outcome.
3. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- SIX OF THE EIGHT PRODUCING TYPES STILL CANNOT BE ANSWERED THROUGH THE DOOR.
  R-0693 measures the gap; the rest are outside F031's scope, and the inbox
  tells the truth about every one of them rather than offering a refused button.
- APPROVING FROM THE INBOX ACCEPTS EVERY CLARIFICATION DEFAULT. DECISION F031
  D24 rules that and R50's FORM is where an operator gains any other choice.
- SIX ROUNDS RAISED A REVIEWER-SPEC DEFECT WITH ONE ROOT CAUSE — a block
  ordering something against a file it had not read. Step 2 above is the fix
  and it is the highest-value work left in this feature.
- A ROUND NUMBER IS BAKED INTO SHIPPED PRODUCTION TEXT (R-0702) and went stale
  within one round of landing. The lesson generalises past this instance: a
  docstring names the DECISION or the feature, never the round.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 254 at `4f474e19`
  and this round takes it to 257.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
