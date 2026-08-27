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
CORRECTION ROUND. The RECORD ROUND passed every gate, and this round writes that
verdict together with a correction to a clause the reviewer itself authored
inside `R-0708`. The finding's conclusion stands and this round proves it from
the diff; only the supporting clause was wrong. It writes NO STATUS line, syncs
NO README and creates NO pull request: closure is deferred to the operator.

## Next Steps
1. CLOSURE 3 of 3 — the STATUS line from `[~]` to `[x]` with the README
   capability sync in the SAME commit, then the pull request, which is NOT
   merged in the session that creates it. The five closure values it needs
   already exist and are carried in the handoff; the package is NOT rebuilt.

## Risks
- CLOSURE PRECONDITION 2 IS INTERMITTENT RATHER THAN GREEN. The reviewer ran
  `python3 -m pytest -n auto -q` five times at the reviewed head and measured
  four GREEN at 17817 passed with 20 skipped, and one RED at 17816 passed with
  one failed. The red is `R-0708`.
- `R-0708` IS NOT AN F031 DEFECT, AND THE REASON IS NARROWER THAN THIS PLAN
  ONCE CLAIMED. F031 does change `tests/ui_server/`, five files of it, one of
  them `test_live_state.py` itself. What F031 does to that file is APPEND one
  test class that starts no server; the failing class, its five-second helper
  and the failing test are untouched by this branch.
- WHETHER AN INTERMITTENTLY GREEN PRECONDITION MAY CARRY AN `[x]` IS AN OPERATOR
  QUESTION. The rules do not answer it, and guardrail G8 of the self-drive
  protocol ends a session on exactly that kind of question rather than guessing.
- THE CLOSURE PACKAGE ALREADY EXISTS and does not need rebuilding. It was built
  from a clean tree at the reviewed head and its manifest names that head.
- R-0495 and R-0574 are inherited standing Highs from the already-closed F085
  and F086, documented risks rather than F031 defects, and they rode through six
  prior closures on the same footing.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 252 and this round
  moves it by nothing.
