# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1-D26.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
RECORD ROUND. The CORRECTION ROUND passed every gate its block ordered and this
round writes that verdict. It also records, WITHOUT MINTING AN ID, a recurrence
of the OPEN finding `R-0430`: that round's handback declared a DECISION D15
overage without stating its own measured line count, which is exactly the
standing rule `R-0430` already carries. This round writes NO STATUS line, syncs
NO README and creates NO pull request.

## Next Steps
1. CLOSURE 3 of 3 — the STATUS line from `[~]` to `[x]` with the README
   capability sync in the SAME commit, then the pull request, which is NOT
   merged in the session that creates it. The five closure values it needs
   already exist and are carried in the handoff; the package is NOT rebuilt.
   IT IS BLOCKED ON THE OPERATOR QUESTION IN THE FIRST RISK BELOW, and no
   session starts it before that question is answered.

## Risks
- CLOSURE 3 IS BLOCKED ON AN OPERATOR QUESTION. Closure precondition 2 asks for
  a green suite; the reviewer measured four GREEN and one RED in five runs at
  the reviewed head, the red being `R-0708`. Whether an intermittently green
  precondition may carry an `[x]` is not answered by
  `docs/roadmap/STATUS_closure_protocol.md`, whose Failure-honesty section
  offers a repair round, an `[!]` line or an explicit operator decision — a
  choice guardrail G8 forbids this session to make for itself.
- `R-0708` IS NOT AN F031 DEFECT. Commit `6b68718e` is the only one on this
  branch touching `tests/ui_server/test_live_state.py`; it changes one import
  line and inserts a class that starts no server, and it leaves
  `TestUIServerIntegration`, its `_start_server` helper and
  `test_context_budget_endpoint` untouched.
- THE CLOSURE PACKAGE ALREADY EXISTS and does not need rebuilding. It was built
  from a clean tree at the reviewed head and its manifest names that head.
- R-0495 and R-0574 are inherited standing Highs from the already-closed F085
  and F086, documented risks rather than F031 defects.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 252 and this round
  moves it by nothing.
