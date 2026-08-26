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
R19 records the R18 verdict, resolves R-0681 with authored `Done:` text, and
registers a recurrence of R-0385 against the reviewer's own R17 block, which ran
409 prose lines against a 400-line cap. No code ships.

## Next Steps
1. R20 ships T002b ORDERING under DECISION F031 D6, already on disk: add
   `ageSeconds` to `DecisionCardModel` — `buildDecisionCardModel` computes that
   local already and only omits it from the returned object — ship the
   comparator as `apps/ui/src/api/decisionOrder.ts` with its own `.test.ts`,
   wire it in `RightLivePanel`, and update the two `toEqual` blocks in
   `decisionCard.test.ts` that pin the model's exact shape. R20 must ALSO rule
   the seed-key collision the first risk below names.
2. T002b FILTERING by type — D6 narrows the feature file's "filters by
   type/job" to TYPE alone, `DecisionInboxEntry` carrying no job field.
3. T002b BADGE under DECISION F031 D2: it re-derives on refetch over the
   existing SSE stream, no new event kind, D2's two constant-zero counters
   replaced. T003 then wires answering and rules `NeedsAttentionCard` (D4).

## Risks
- THE SEED-KEY COLLISION, now the nearest deadline: `.agent/live_review.md`
  holds `Gate: R19` as a seed entry inherited from F022, and a verdict is
  recorded by the NEXT round, so R20's ledger entry is the first that would
  duplicate that key — the §3 item 26 defect. The seed is NOT rewritten (§3
  item 20); R20 rules a feature-qualified key as a DECISION before writing it.
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 238 once C2 lands, from 239 at `6c758fc8`.
- The findings THIS FEATURE MUST STILL ACT ON are R-0403, R-0413, R-0431,
  R-0441, R-0445, R-0471, R-0495, R-0533, R-0574, R-0601, R-0622, R-0625,
  R-0632, R-0672, R-0674, R-0675, R-0676, R-0677, R-0678 and R-0679; R-0495 and
  R-0574 are the two Highs. R-0681 leaves this list at C2.
- BLOCK CAPS ARE TWO, not one: 490 lines TOTAL (DECISION F085 D6) and 400 lines
  PROSE (DECISION F085 D5). R-0385's recurrence is what happens when only the
  first is checked; every block from here states and re-measures both.
- THE SHIPPED MARKUP IS REACHED BY NO TEST, which DECISION F031 D5 rules its own
  feature, so T002b's logic lives in the pure layer under `apps/ui/src/api/`.
