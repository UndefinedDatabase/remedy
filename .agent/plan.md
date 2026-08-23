# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the merge
commit of pull request #213 which closed F022. `.agent/live_review.md` is the
source of truth for the open set, the round map and the finding-id ceiling.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the file-based decision queue, live via
decision.requested and decision.resolved events driving the badge, with
branch-only blocking semantics intact. DONE when the inbox lists fixture
decisions of every producing type with correct blocked-size math, answering from
a card round-trips through the write channel into the same effects the CLI
produces, the badge tracks live, and ordering follows a documented rule over age
and blocked size rather than vibes.

## Current Step
R1 claims F031. It advances this plan, flips the STATUS line to `[~]`, resets
the review record for the new feature, writes the F022 R19 gate entry that
closes that feature's record, registers the single candidate F022 carried as
R-0677, and empties `.agent/candidates.md` in the same round.

## Next Steps
1. R2 records the R1 verdict on disk.
2. R3 takes the decision-inbox inventory in the source and MEASURES each part:
   the file-based queue store and its CLI, every producer that writes a
   decision, the DAG module's blocked-subtree entry point, and the decision
   event kinds the stream carries today on the Python and the TypeScript side.
3. T001 follows the feature file's Task slicing once that inventory is on disk.

## Risks
- The open set carried into F031 is R-0403, R-0413, R-0431, R-0445, R-0495,
  R-0533, R-0574, R-0625, R-0672, R-0674, R-0675 and R-0676, each re-read in the
  record at `6325ac2f` and carrying no resolution line there, plus R-0677 which
  R1 mints. R-0495 and R-0574 are the two Highs, both inherited from the
  already-closed F085 and F086 and neither an F031 defect.
- That set is NOT mechanically derivable from `.agent/live_review.md`. The
  record carries no machine-readable resolution marker, so the §3 item 10 rule
  yields 235 where the practice yields 12, and the plan's Risks section is the
  only carrier. R3 rules how the open set is to be derived; until it does, this
  bullet is the set.
- F031 depends on F009, F050 and F051. F009 is closed; whether F050 and F051 are
  built is UNMEASURED at this commit and R3's inventory settles it before any
  T-slice is planned.
