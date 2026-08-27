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
RECORD ROUND. CLOSURE 2 of 3 PASSED and this round writes that verdict, which
would otherwise evaporate exactly as registered finding R-0659 describes. It
also registers R-0708, the intermittent server-start failure the reviewer hit
while running closure precondition 2. It writes NO STATUS line, syncs NO README
and creates NO pull request: closure is deferred to the operator.

## Next Steps
1. CLOSURE 3 of 3 — the STATUS line from `[~]` to `[x]` with the README
   capability sync in the SAME commit, then the pull request, which is NOT
   merged in the session that creates it. The three closure values it needs
   already exist and are carried in the handoff; the package is NOT rebuilt.

## Risks
- CLOSURE PRECONDITION 2 IS INTERMITTENT RATHER THAN GREEN, AND THAT IS WHY
  CLOSURE DID NOT HAPPEN IN THE SESSION THAT PRODUCED THE PACKAGE. The reviewer
  ran `python3 -m pytest -n auto -q` five times at the reviewed head and measured
  four GREEN at 17817 passed with 20 skipped, and one RED at 17816 passed with
  one failed. The red is R-0708. It is not an F031 defect: this feature changed
  nothing under `apps/`, `packages/` or `tests/`.
- WHETHER AN INTERMITTENTLY GREEN PRECONDITION MAY CARRY AN `[x]` IS AN OPERATOR
  QUESTION. The rules do not answer it, and guardrail G8 of the self-drive
  protocol ends a session on exactly that kind of question rather than guessing.
- THE CLOSURE PACKAGE ALREADY EXISTS and does not need rebuilding. It was built
  from a clean tree at the reviewed head and its manifest names that head.
- R-0495 and R-0574 are inherited standing Highs from the already-closed F085
  and F086, documented risks rather than F031 defects, and they rode through six
  prior closures on the same footing.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 251 before this
  round and 252 after it, R-0708 being the one entry that moves.
