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
R13 records the R12 verdict and registers R-0680, a reviewer defect this round
repairs: the R12 plan rewrite dropped the seed-key warning below and it survived
nowhere else. T002a's tested layer is SHIPPED — `decisionCard.ts` with 27 cases
beside it, red-proofed against a mutation making it branch on a decision's type.

## Next Steps
1. Project the model into a `.tsx` card built from the shipped
   `RightLivePanel.module.css` shell per DECISION F031 D4, mounted in
   `RightLivePanel`, carrying no branching of its own — every decision it makes
   must first exist in `decisionCard.ts`.
2. T002b adds ordering over age and blocked size, filtering, and the badge,
   where DECISION F031 D2 binds: the badge re-derives on refetch over the
   existing SSE stream, no new event kind ships, and D2's two constant-zero
   counters get replaced.
3. T003 wires answering through the write channel, and rules there whether
   `NeedsAttentionCard`'s decision branch is retired, which D4 leaves open.

## Risks
- THE SEED-KEY COLLISION, restored here as the repair R-0680 names and never to
  be dropped again while it stands: `.agent/live_review.md` holds `Gate: R19` as
  a seed entry inherited from F022, so if F031 reaches its own R19 that key
  collides — the §3 item 26 defect. A round before then renames the seed or the
  scheme. F031 is at R13, so seven rounds remain.
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 239 once C2 lands, from 238 at `13306809`.
- The findings THIS FEATURE MUST STILL ACT ON are R-0403, R-0413, R-0431,
  R-0445, R-0471, R-0495, R-0533, R-0574, R-0601, R-0622, R-0625, R-0632,
  R-0672, R-0674, R-0675, R-0676, R-0677, R-0678, R-0679 and R-0680; R-0495 and
  R-0574 are the two Highs.
- R-0622 is live ground: eslint parses no TypeScript here and `npm run lint`
  exits 1 at 80 problems, so `typecheck` is the only static reader that works.
- The rendered markup is reached by NO test until a DOM harness lands, which
  DECISION F031 D5 rules its own feature. Every branch therefore stays in the
  pure model; one migrating into a `.tsx` leaves the tested region.
