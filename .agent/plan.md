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
R64 records the R63 verdict and lands the MARKUP half of the clarification form:
the card holds a field per open clarification, keys each with the R63 module's
key rule, collects them with its collection rule and passes the map to
`answerDecisionCard`. The stylesheet gains the field rules and the contract
guard moves with the call string it pins. No finding moves in either direction.

## Next Steps
1. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- THE DEFAULT IS SHOWN AND MUST NEVER BE SENT. A blank or absent answer is what
  the server reads as "accept this question's default" (DECISION F031 D24), so
  a prefilled field would post the default as though it had been typed. The
  field starts empty and the default is visible text beside it.
- THE QUESTION IDS ARE NOT GUARANTEED DISTINCT. Neither
  `open_clarification_questions` nor `cardClarifications` deduplicates them, so
  a React key pairs the clarification's POSITION with its field key; the
  collected map still collapses a duplicate to one entry, because the write
  door's contract is keyed by question id.
- SIX OF THE EIGHT PRODUCING TYPES STILL CANNOT BE ANSWERED THROUGH THE DOOR.
  R-0693 measures the gap; the rest are outside F031's scope, and the inbox
  tells the truth about every one of them rather than offering a refused button.
- THIS FILE NAMES NO ROUND NUMBER IT HAS NOT BEGUN. Twice a pre-assigned label
  went stale the moment a round was inserted ahead of it; a step is named by
  what it does, and its number is knowable only when it starts.
- A WORKTREE VITEST RUN OVER THE WHOLE SUITE IS RED AT BASE. A worktree carries
  no `apps/ui/node_modules`, so `react/jsx-dev-runtime` cannot resolve for the
  one test that reaches a `.tsx`; every worktree vitest run is scoped to
  `src/api/` and passes the primary checkout's config. pytest in a worktree
  needs no such care and the reviewer measured it green at base.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 252 at `3de459cc`
  and this round moves it by nothing.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
