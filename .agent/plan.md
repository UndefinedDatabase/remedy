# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `f031_*_inventory.md` the inventories, `.agent/decisions.md` D1–D7.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R20 ships T002b ORDERING under DECISION F031 D6: `DecisionCardModel` gains
`ageSeconds`, the comparator ships as `apps/ui/src/api/decisionOrder.ts` with its
own test, and `RightLivePanel` orders the inbox before handing it to the card.
R20 also rules DECISION F031 D7, the feature-qualified ledger key, and records
the R19 verdict under it.

## Next Steps
1. T002b FILTERING by type — DECISION F031 D6 narrows the feature file's
   "filters by type/job" to TYPE alone, `DecisionInboxEntry` carrying no job
   field, so the job filter waits on T003's deep links.
2. T002b BADGE under DECISION F031 D2: it re-derives on refetch over the
   existing SSE stream, no new event kind, D2's two constant-zero counters
   replaced.
3. T003 wires answering through the existing write channel and rules
   `NeedsAttentionCard` (DECISION F031 D4).

## Risks
- THE SEED-KEY COLLISION IS RULED, not merely noted: `.agent/live_review.md`
  holds a `Gate: R19` line inherited from F022, so DECISION F031 D7
  feature-qualifies every gate key from the R19 entry onward and the landed seed
  is never rewritten (§3 item 20).
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 238 at `ba75103e`.
- The findings THIS FEATURE MUST STILL ACT ON are R-0403, R-0413, R-0431,
  R-0441, R-0445, R-0471, R-0495, R-0533, R-0574, R-0601, R-0622, R-0625,
  R-0632, R-0672, R-0674, R-0675, R-0676, R-0677, R-0678 and R-0679; R-0495 and
  R-0574 are the two Highs.
- BLOCK CAPS ARE TWO, not one: 490 lines TOTAL (DECISION F085 D6) and 400 lines
  PROSE (DECISION F085 D5); every block states and re-measures both.
- THE SHIPPED MARKUP IS REACHED BY NO TEST, which DECISION F031 D5 rules its own
  feature, so this round's logic lives in the pure layer under `apps/ui/src/api/`
  and only the one-call wiring lands in `RightLivePanel.tsx`.
