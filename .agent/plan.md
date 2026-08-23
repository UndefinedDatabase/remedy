# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the merge
commit of pull request #213 which closed F022. `.agent/live_review.md` is the
source of truth for the record and the finding-id ceiling;
`.agent/f031_inventory.md` is the measured source inventory; `.agent/decisions.md`
carries DECISION F031 D1, D2 and D3, which settle the design.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact. DONE when the inbox lists fixture
decisions of every PRODUCING type with correct blocked-size math, answering from
a card round-trips through the write channel into the same effects the CLI
produces, the badge tracks live, and ordering follows a documented rule over age
and blocked size rather than vibes.

## Current Step
R7 builds T001: the derivation module `packages/orchestration/decision_inbox.py`,
its wiring into the `/api/jobs/<job_id>/decisions` route, and the contract tests
with a fixture per PRODUCING type. It also records the R6 verdict, and is the
first round of this feature to touch production code.

## Next Steps
1. R8 records the R7 verdict and plans T002: the cards, the generic options
   renderer, ordering and filtering, and the badge — where DECISION F031 D2
   binds, so the badge re-derives on refetch over the existing SSE stream.
2. T002 replaces the two constant-zero counters D2 names: the `decision_count`
   local of `_build_dashboard` and the `open_decisions` sum of
   `_build_live_state_json`, both in `packages/orchestration/ui_server.py`. The
   THIRD, in `_build_orchestrator_section`, is fed by `orchestrator_brain` and
   is NOT part of this feature.
3. T003 wires answering through the existing `decision.resolve` write channel,
   adds the clarification forms and deep links, and closes with the end-to-end.

## Risks
- Open findings, stated with the rule and the commit DECISION F009 D10 requires:
  by §3 item 10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — `
  line — the open set is 238, measured at `e73da3ef`.
- The findings THIS FEATURE MUST STILL ACT ON — a narrower set, named as what it
  is and not called "open" — are R-0403, R-0413, R-0431, R-0445, R-0471, R-0495,
  R-0533, R-0574, R-0601, R-0625, R-0632, R-0672, R-0674, R-0675, R-0676, R-0677,
  R-0678 and R-0679; R-0495 and R-0574 are the two Highs, from F085 and F086.
- Only the `task_decision` branch of `list_decisions` carries a task id, so it is
  the only type whose blocked count can be non-zero — measured in
  `.agent/f031_inventory.md` Q3, and T001 pins it in both directions.
- The record holds `Gate: R19` from F022 as its seed entry. If F031 reaches its
  own R19 that key collides — the §3 item 26 defect. A round before then renames
  the seed or the scheme; this bullet is the reminder.
