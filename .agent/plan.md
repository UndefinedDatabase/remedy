# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the merge
commit of pull request #213 which closed F022. `.agent/live_review.md` is the
record and the finding-id ceiling; `.agent/f031_inventory.md` is the measured
source inventory; `.agent/decisions.md` carries DECISION F031 D1, D2 and D3.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact. DONE when the inbox lists fixture
decisions of every PRODUCING type with correct blocked-size math, answering from
a card round-trips through the write channel into the same effects the CLI
produces, the badge tracks live, and ordering follows a documented rule over age
and blocked size rather than vibes.

## Current Step
R9 records the R8 verdict and MEASURES the UI ground T002 needs into
`.agent/f031_ui_inventory.md`. T001 is SHIPPED: the derivation module, the
`/api/jobs/<job_id>/decisions` route and 29 tests are on disk and green.

## Next Steps
1. R10 rules the two gaps Risks names below, each as a DECISION with
   alternatives and a reversal path, before any card ships.
2. T002a then builds the cards and the GENERIC options renderer — producers own
   the semantics, so no per-type form is hardcoded — with the tests whose shape
   R10's second ruling settles.
3. T002b adds ordering, filtering and the badge, where DECISION F031 D2 binds:
   the badge re-derives on refetch over the existing SSE stream, no new event
   kind ships, and the two constant-zero counters D2 names get replaced.

## Risks
- Open findings, stated with the rule and the commit DECISION F009 D10 requires:
  by §3 item 10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — `
  line — the open set is 238, measured at `1ec7a330`.
- The findings THIS FEATURE MUST STILL ACT ON — a narrower set, named as what it
  is and not called "open" — are R-0403, R-0413, R-0431, R-0445, R-0471, R-0495,
  R-0533, R-0574, R-0601, R-0625, R-0632, R-0672, R-0674, R-0675, R-0676, R-0677,
  R-0678 and R-0679; R-0495 and R-0574 are the two Highs, from F085 and F086.
- THE CANONICAL DESIGN REFERENCE HAS NO INBOX AND NO DECISION COMPONENT, so T002
  has no visual authority and may not improvise one: measured at `1ec7a330`,
  `component_spec.md` names no such component.
- THE SHIPPED UI TOOLCHAIN COLLECTS NO COMPONENT TEST. Measured at `1ec7a330`:
  `apps/ui/vitest.config.ts` sets `environment` to `node` and includes only
  `src/**/*.test.ts`, and `apps/ui/package.json` names no DOM harness — so T002's
  "component tests" is a spec claim R10 rules on, not a plan a round executes.
- The record holds `Gate: R19` from F022 as its seed entry. If F031 reaches its
  own R19 that key collides — the §3 item 26 defect. A round before then renames
  the seed or the scheme; this bullet is the reminder.
