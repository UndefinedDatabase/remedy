# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1–D23.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R46 is a RECORD ROUND and changes no executable file: it registers R-0696,
records R45's PASS and lands DECISION F031 D23, which moves the rest of the
programme by one. DECISION F031 D19 is now COMPLETE on both sides of the wire —
the endpoint derives answerability and the browser renders a refused answer as
pasteable text rather than as a button the write door would turn away.

## Next Steps
1. R47: retire the duplicate contract guard R-0696 names, then land the
   `fp:`-prefixed dispatch DECISION F009 D5 planned and did not ship, reusing
   `flight_plan.resolve_flight_plan_approval`.
2. R48: the clarification FORM over `payload.clarifications`.
3. A reviewer-file round landing the §3 checklist item R-0694, R-0695 and R-0696
   share: a block reads the TARGET — a predicate's refusal conditions, a test
   file's existing guards — before ordering anything against it.
4. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- SEVEN OF THE EIGHT PRODUCING TYPES STILL CANNOT BE ANSWERED THROUGH THE DOOR.
  The inbox no longer CLAIMS they can, which is what D19 bought; R47 is where
  the `fp:` prefix gains a real dispatch. R-0693 measures the gap.
- NO DOM HARNESS REACHES THE INBOX MARKUP, so the component is guarded only by
  comment-stripped SOURCE reading in
  `tests/ui_contracts/test_decision_answer_wiring.py` and by `tsc --noEmit`.
  The R45 gate measured what that buys: a component ignoring `answer.posts`
  leaves `vitest` GREEN at 454 and turns those guards RED, so the guards are
  load-bearing and deleting one silently un-tests the render.
- THREE CONSECUTIVE ROUNDS RAISED A REVIEWER-SPEC DEFECT, not a worker defect —
  R-0694, R-0695 and R-0696 — and all three have one root cause: the block was
  written without reading the thing it ordered against. Step 3 above is the fix.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 251 at `d53bdb9b`
  and this round takes it to 252.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
