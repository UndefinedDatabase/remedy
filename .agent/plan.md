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
R11 records the R9 and R10 verdicts in one ledger commit and rules the two
measured gaps as DECISION F031 D4 and D5, routing both into the feature file.
R10 was this same bundle and stopped on the now-absent `.agent/STOP` sentinel.
T001 is SHIPPED: the module, the route and 29 tests are green.

## Next Steps
1. T002a builds the inbox card and the GENERIC options renderer as PURE model
   functions under `apps/ui/src/api/` with `.test.ts` beside them, per D5, and
   the card shell D4 fixes; the extensibility test covers a novel options
   payload at the model layer.
2. T002b adds ordering over age and blocked size, filtering, and the badge,
   where DECISION F031 D2 binds: the badge re-derives on refetch over the
   existing SSE stream, no new event kind ships, and the two constant-zero
   counters D2 names get replaced.
3. T003 wires answering through the write channel, and rules there whether
   `NeedsAttentionCard`'s decision branch is retired, which D4 leaves open.

## Risks
- Open findings, stated with the rule and the commit DECISION F009 D10 requires:
  by §3 item 10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — `
  line — the open set is 238, measured at `99d77d5c`.
- The findings THIS FEATURE MUST STILL ACT ON — a narrower set, named as what it
  is and not called "open" — are R-0403, R-0413, R-0431, R-0445, R-0471, R-0495,
  R-0533, R-0574, R-0601, R-0625, R-0632, R-0672, R-0674, R-0675, R-0676, R-0677,
  R-0678 and R-0679; R-0495 and R-0574 are the two Highs, from F085 and F086.
- D5 leaves the card's rendered markup reached by NO test, deliberately and
  scheduled rather than discovered. Every branch lives in the pure model; if a
  branch ever migrates into the component, it leaves the tested region.
- The record holds `Gate: R19` from F022 as its seed entry. If F031 reaches its
  own R19 that key collides — the §3 item 26 defect. A round before then renames
  the seed or the scheme; this bullet is the reminder.
