# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1–D26.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R52 closes the gap DECISION F031 D26 named when it split the FORM in two. R51
gave the write door a THIRD refusal — a malformed or unknown `args.answers` —
and shipped it with no test; this round pins both halves of that refusal at the
door's own answer surface. It changes no production file and records R51's PASS.

## Next Steps
1. R53: the BROWSER half of the FORM — the pending card renders a field per open
   clarification and posts them as `args.answers`. `payload.clarifications`
   already reaches the browser, and `decisionAnswers` already derives the two
   words the door takes, so this is a component and a model field rather than a
   new wire format.
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
- THE FORM IS REACHABLE ONLY BY A NON-BROWSER CLIENT UNTIL R53. The door takes
  `args.answers` and the card carries the questions, but nothing in the UI yet
  puts the two together, so an operator's only route is still every default.
- SIX ROUNDS RAISED A REVIEWER-SPEC DEFECT WITH ONE ROOT CAUSE — a block
  ordering something against a file it had not read. Step 2 above is the fix
  and it is the highest-value work left in this feature.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 255 at `743a8f7b`
  and this round leaves it at 255.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
