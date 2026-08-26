# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `f031_*_inventory.md` the inventories, `.agent/decisions.md` D1–D6.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R18 records the R17 verdict and rules DECISION F031 D6 — the urgency formula
T002b orders by — into `.agent/decisions.md` and the feature file's amendment
series. No code ships, and R-0681's `Done:` text is owed by R19.

## Next Steps
1. RESOLVE R-0681 FIRST: replace its `Landed:` line in `.agent/live_review.md`
   with authored `Done:` text. The fix itself landed at `6ede183c` and the
   reviewer gated it at R18; only the marker lags.
2. T002b ORDERING, under D6: add a numeric age to `DecisionCardModel`, ship the
   comparator as its own pure function beside `decisionCard.ts`, wire it where
   the inbox is handed to the card, and update the two `toEqual` blocks in
   `decisionCard.test.ts` that pin the model's exact shape.
3. T002b FILTERING by type, then the badge under DECISION F031 D2: it
   re-derives on refetch over the existing SSE stream, no new event kind ships,
   and D2's two constant-zero counters get replaced. T003 then wires answering
   and rules whether `NeedsAttentionCard`'s decision branch is retired (D4).

## Risks
- THE SEED-KEY COLLISION, carried forward while it stands:
  `.agent/live_review.md` holds `Gate: R19` as a seed entry inherited from
  F022, so an F031 entry under that key duplicates it — the §3 item 26 defect.
  A verdict is recorded by the NEXT round, so the colliding write is R20's. The
  seed is NOT rewritten (§3 item 20); that entry takes a feature-qualified key,
  ruled as a DECISION before R20 rather than left as this bullet.
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 239 at `48124293` and R18 does not move it.
- The findings THIS FEATURE MUST STILL ACT ON are R-0403, R-0413, R-0431,
  R-0441, R-0445, R-0471, R-0495, R-0533, R-0574, R-0601, R-0622, R-0625,
  R-0632, R-0672, R-0674, R-0675, R-0676, R-0677, R-0678, R-0679 and R-0681,
  the last awaiting only its resolution text; R-0495 and R-0574 are the Highs.
- R-0622 is live ground: eslint parses no TypeScript here and `npm run lint`
  exits 1 at 80 problems, so `typecheck` is the only static reader that works.
- THE SHIPPED MARKUP IS REACHED BY NO TEST, which DECISION F031 D5 rules its own
  feature, and R15's own probe measured it: deleting the mount turns nothing
  red. Every branch therefore stays in the pure layer under `apps/ui/src/api/`.
