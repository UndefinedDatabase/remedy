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
R65 records the R64 verdict and runs the INTEGRATION GATE of
`docs/agents/integration_gate.md` over this branch, writing its evidence under
`.agent/gate_f031_r65/`. It is the LAST round of its session: its handback is
the session terminator and the next session resumes from it. The gate MEASURES
and never repairs — no production file is touched and no finding moves.

## Next Steps
1. Closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- THE GATE MEASURES AND MUST NEVER REPAIR. A red branch run ends the round with
  a report; no test is deleted, no assertion weakened and no ceiling raised to
  make a run green, and the fix for any blocker is its own gated round.
- THE BASE WORKTREE NEEDS A THROWAWAY BRANCH AND COPIED ARTIFACTS. A detached
  HEAD fails the self-dogfood guard by design (DECISION D3), and a symlinked
  `node_modules` lets an npm lifecycle write back into the primary checkout
  (F053 R3), so both are copied and the branch is deleted afterwards.
- THE STALENESS CLASS IS REPAIRED BEFORE THE BASE RUN, NOT ATTRIBUTED AFTER IT.
  A fresh checkout writes `apps/ui/src` NOW while the copied `dist` keeps its
  old mtime, so `_frontend_is_stale()` fires and the request path fails; that
  cost F022 R15 sixty-three base-only failures to attribute by hand.
- THE FORM IS ANSWERABLE BUT SIX OF THE EIGHT PRODUCING TYPES STILL CANNOT BE
  ANSWERED THROUGH THE DOOR. R-0693 measures the gap; the rest are outside
  F031's scope, and the inbox tells the truth about every one of them rather
  than offering a refused button.
- THIS FILE NAMES NO ROUND NUMBER IT HAS NOT BEGUN. Twice a pre-assigned label
  went stale the moment a round was inserted ahead of it; a step is named by
  what it does, and its number is knowable only when it starts.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 252 at `2d4001b4`
  and this round moves it by nothing.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
