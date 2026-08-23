# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the merge
commit of pull request #213 which closed F022. `.agent/live_review.md` is the
source of truth for the record, the round map and the finding-id ceiling.

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
R3 records the R2 verdict and takes the decision-inbox inventory into
`.agent/f031_inventory.md`: the queue store and its types, the CLI surface, the
producers, the blocked-subtree computation, the decision event kinds on both
sides, the write-channel command, and what the UI has today — each measured in
the source, no T-slice planned until it is on disk.

## Next Steps
1. R4 records the R3 verdict and rules the tick-shaped questions the inventory
   leaves open — chiefly the event-kind envelope, since the feature file says
   "envelope coordination if not yet present" and the inventory settles which.
2. T001 follows the feature file's Task slicing: the read endpoint, the
   blocked-size computation, scoping, and contract tests per producer type.

## Risks
- Open findings, stated with the rule and the commit DECISION F009 D10 requires:
  by §3 item 10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — `
  line — the open set is 236 measured at `9e773d4a`.
- The findings THIS FEATURE MUST STILL ACT ON — a narrower set, named as what it
  is and not called "open" — are R-0403, R-0413, R-0431, R-0445, R-0495, R-0533,
  R-0574, R-0625, R-0632, R-0672, R-0674, R-0675, R-0676 and R-0677. R-0495 and
  R-0574 are the two Highs, both inherited from the closed F085 and F086.
- F031 depends on F009, F050 and F051. All three are marked `[x]` in
  `docs/roadmap/STATUS.md`, measured at `9e773d4a`; R3's inventory confirms what
  each actually left behind in the source rather than trusting the mark.
- The record holds `Gate: R19` from F022 as its seed entry. If F031 reaches its
  own R19 that key collides — the §3 item 26 defect. A round before then renames
  the seed or the scheme; this bullet is the reminder.
