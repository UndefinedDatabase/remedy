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
CLOSURE 1 of 3. This round writes the R66 verdict, resolves R-0693 — the only
open High this feature raised, whose DECISION F031 D19 repair landed in full —
and gives `docs/roadmap/features/T5_F031.md` the `## Built State` section it has
never had, which is the closure protocol's precondition 4. No production code
and no new decision. STATUS.md and README.md are NOT touched here: the closure
commit owns them and it is two rounds away.

## Next Steps
1. CLOSURE 2 of 3 — the feature-scoped evidence bundle and a FRESH review zip
   built from a clean tree at the reviewed head. A failing zip build is a
   closure BLOCKER, never something to work around.
2. CLOSURE 3 of 3 — the STATUS line from `[~]` to `[x]` with the README
   capability sync in the SAME commit, the candidates file, and the pull
   request. The PR is NOT merged in this session.

## Risks
- R-0693 IS THE ONLY OPEN HIGH THIS FEATURE RAISED, and its repair is on disk:
  the `fp:` dispatch in the write door, the third endpoint key, and a card that
  posts nothing the door would refuse. R-0495 and R-0574 are inherited standing
  Highs that rode through six prior closures and ride through this one as
  documented risks, which is what PASS_WITH_RISKS means.
- SIX OF THE EIGHT PRODUCING TYPES STILL CANNOT BE ANSWERED THROUGH THE DOOR.
  DECISION F031 D19 rules them out of F031's scope, and the inbox tells the
  truth about every one of them rather than offering a refused button.
- THE PARITY CLAIM OF THE R65 GATE IS VOID AND STAYS VOID. A rebuild ran inside
  the base run window and the evidence says so; it costs nothing only because
  the base-only set is empty, so no id was owed an attribution.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 252 before this
  round and 251 after it, R-0693 being the one entry that moves.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
