# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the merge
commit of pull request #213 which closed F022. `.agent/live_review.md` is the
record and the finding-id ceiling; the two `f031_*_inventory.md` files are the
inventories; `.agent/decisions.md` carries DECISION F031 D1 through D5.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R16 records the R15 verdict and registers R-0681, a reviewer defect found at the
R15 gate: the spec named the component `DecisionInboxCard`, which
`apps/ui/src/api/decisionCard.ts` already exports as an interface. No code ships.

## Next Steps
1. REPAIR R-0681 FIRST, before new feature work: rename the INTERFACE in
   `apps/ui/src/api/decisionCard.ts` to name one endpoint ENTRY, carrying its
   three use sites and its `decisionCard.test.ts` import, and leave the
   component alone. Gate on `typecheck` and the unchanged 21 files, 316 tests.
2. T002b adds ordering over age and blocked size, filtering, and the badge,
   where DECISION F031 D2 binds: the badge re-derives on refetch over the
   existing SSE stream, no new event kind ships, and D2's two constant-zero
   counters get replaced.
3. T003 wires answering through the write channel — the card's answer buttons
   ship DISABLED until it lands — and rules there whether
   `NeedsAttentionCard`'s decision branch is retired, which D4 leaves open.

## Risks
- THE SEED-KEY COLLISION, carried forward and never to be dropped while it
  stands: `.agent/live_review.md` holds `Gate: R19` as a seed entry inherited
  from F022, so if F031 reaches its own R19 that key collides — the §3 item 26
  defect. A round before then renames the seed or the scheme. F031 is at R16,
  so four rounds remain, and this is now the nearer deadline of the two.
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 239 once C2 lands, from 238 at `4fc7dc77`.
- The findings THIS FEATURE MUST STILL ACT ON are R-0403, R-0413, R-0431,
  R-0441, R-0445, R-0471, R-0495, R-0533, R-0574, R-0601, R-0622, R-0625,
  R-0632, R-0672, R-0674, R-0675, R-0676, R-0677, R-0678, R-0679 and R-0681;
  R-0495 and R-0574 are the two Highs. This bullet states no count of that list.
- R-0622 is live ground: eslint parses no TypeScript here and `npm run lint`
  exits 1 at 80 problems, so `typecheck` is the only static reader that works.
- THE SHIPPED MARKUP IS REACHED BY NO TEST, which DECISION F031 D5 rules its own
  feature, and R15's own probe measured it: deleting the mount turns nothing
  red. Every branch therefore stays in `decisionCard.ts`.
