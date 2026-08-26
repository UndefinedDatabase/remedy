# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the merge
commit of pull request #213 which closed F022. `.agent/live_review.md` is the
record and the finding-id ceiling; `.agent/f031_inventory.md` and
`.agent/f031_ui_inventory.md` are the measured inventories; `.agent/decisions.md`
carries DECISION F031 D1 through D5.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact. DONE when the inbox lists fixture
decisions of every PRODUCING type with correct blocked-size math, answering from
a card round-trips through the write channel into the same effects the CLI
produces, the badge tracks live, and ordering follows a documented rule over age
and blocked size rather than vibes.

## Current Step
R12 records the R11 verdict and ships T002a's tested layer: the decision-card
PURE MODEL at `apps/ui/src/api/decisionCard.ts` with `decisionCard.test.ts`
beside it, per DECISION F031 D5. The generic options renderer lives here and
derives every affordance from the decision's own payload, never from its type.

## Next Steps
1. T002a's second round projects that model into a `.tsx` card built from the
   shipped `RightLivePanel.module.css` shell per DECISION F031 D4 and mounts it
   in `RightLivePanel`; the component carries no branching of its own.
2. T002b adds ordering over age and blocked size, filtering, and the badge,
   where DECISION F031 D2 binds: the badge re-derives on refetch over the
   existing SSE stream, no new event kind ships, and the two constant-zero
   counters D2 names get replaced.
3. T003 wires answering through the write channel, and rules there whether
   `NeedsAttentionCard`'s decision branch is retired, which D4 leaves open.

## Risks
- Open findings, stated with the rule and the commit DECISION F009 D10 requires:
  by §3 item 10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — `
  line — the open set is 238, measured at `8b4e2295`.
- The findings THIS FEATURE MUST STILL ACT ON — a narrower set, named as what it
  is and not called "open" — are R-0403, R-0413, R-0431, R-0445, R-0471, R-0495,
  R-0533, R-0574, R-0601, R-0622, R-0625, R-0632, R-0672, R-0674, R-0675,
  R-0676, R-0677, R-0678 and R-0679; R-0495 and R-0574 are the two Highs.
- R-0622 is live ground, not history: `npm run lint` exits 1 at 80 problems and
  eslint parses no TypeScript here, so no round of this feature can gate on it
  and every `.ts` file ships unlinted. `npm run typecheck` is the only static
  reader that works.
- The rendered markup stays reached by NO test until a DOM harness lands, which
  DECISION F031 D5 rules is its own feature. Every branch must therefore stay in
  the pure model; a branch that migrates into a `.tsx` leaves the tested region.
