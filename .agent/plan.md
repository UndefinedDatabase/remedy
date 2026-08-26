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
R15 records the R14 verdict, registers the R-0441 recurrence, and renders what
R14 wired: `DecisionInboxCard` projects `dashboard.decisionInbox` into markup
built from the shipped `RightLivePanel.module.css` shell and mounted in
`RightLivePanel`, branching on nothing of its own.

## Next Steps
1. T002b adds ordering over age and blocked size, filtering, and the badge,
   where DECISION F031 D2 binds: the badge re-derives on refetch over the
   existing SSE stream, no new event kind ships, and D2's two constant-zero
   counters get replaced. The ordering rule is documented on the sort control.
2. T003 wires answering through the write channel — the card's answer buttons
   ship DISABLED until it lands — and rules there whether
   `NeedsAttentionCard`'s decision branch is retired, which D4 leaves open.
3. The DOM harness that would test the markup is its own feature per DECISION
   F031 D5, and nothing in F031 waits on it.

## Risks
- THE SEED-KEY COLLISION, carried forward and never to be dropped while it
  stands: `.agent/live_review.md` holds `Gate: R19` as a seed entry inherited
  from F022, so if F031 reaches its own R19 that key collides — the §3 item 26
  defect. A round before then renames the seed or the scheme. F031 is at R15,
  so five rounds remain.
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 238 at `e12a4d46`, and a recurrence resolves nothing, so C2 leaves it
  at 238.
- The findings THIS FEATURE MUST STILL ACT ON are R-0403, R-0413, R-0431,
  R-0441, R-0445, R-0471, R-0495, R-0533, R-0574, R-0601, R-0622, R-0625,
  R-0632, R-0672, R-0674, R-0675, R-0676, R-0677, R-0678 and R-0679; R-0495 and
  R-0574 are the two Highs. This bullet states no count of that list.
- R-0622 is live ground: eslint parses no TypeScript here and `npm run lint`
  exits 1 at 80 problems, so `typecheck` is the only static reader that works.
- THE MARKUP THIS ROUND SHIPS IS REACHED BY NO TEST, which DECISION F031 D5
  rules its own feature. Every branch therefore stays in `decisionCard.ts`; one
  migrating into the `.tsx` leaves the tested region silently.
