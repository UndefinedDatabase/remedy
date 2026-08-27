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
R51 lands the SERVER half of the clarification FORM. `_dispatch_decision_resolve`
stops hard-coding `answers={}`: it takes an OPTIONAL `args.answers`, validates it
against the plan's own open questions, and passes it through, so an operator
approving from the inbox can choose something other than every default. The
round also records R50's PASS and rules DECISION F031 D26.

## Next Steps
1. R52: the BROWSER half — the pending card renders a field per open
   clarification and posts them — together with the tests pinning the two
   refusals DECISION F031 D26 rules, which R51 ships documented but unguarded.
2. A reviewer-file round landing the §3 checklist item R-0694 through R-0699
   share: a block reads the TARGET before ordering anything against it — every
   guard whose ruled set the change widens, every constant a test compares
   against, and every fixture whose state decides an outcome.
3. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- THE TWO REFUSALS D26 RULES SHIP UNGUARDED FOR ONE ROUND. The 490-line block
  cap forced the split; R52's first commit is their test, and until it lands the
  door's own docstring is the only record of the contract.
- SIX OF THE EIGHT PRODUCING TYPES STILL CANNOT BE ANSWERED THROUGH THE DOOR.
  R-0693 measures the gap; the rest are outside F031's scope, and the inbox
  tells the truth about every one of them rather than offering a refused button.
- SIX ROUNDS RAISED A REVIEWER-SPEC DEFECT WITH ONE ROOT CAUSE — a block
  ordering something against a file it had not read. Step 2 above is the fix
  and it is the highest-value work left in this feature.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 255 at `242144ff`
  and this round leaves it at 255.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
