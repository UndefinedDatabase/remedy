# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the merge
commit of pull request #213 which closed F022. `.agent/live_review.md` is the
source of truth for the record, the round map and the finding-id ceiling;
`.agent/f031_inventory.md` is the measured source inventory R3 landed, and
`.agent/decisions.md` now carries the three rulings R5 made over it.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact. DONE when the inbox lists fixture
decisions of every PRODUCING type with correct blocked-size math, answering from
a card round-trips through the write channel into the same effects the CLI
produces, the badge tracks live, and ordering follows a documented rule over age
and blocked size rather than vibes.

## Current Step
R5 records the R4 verdict, registers finding R-0678, and rules the three design
questions the inventory forced as DECISION F031 D1, D2 and D3, appending the
matching amendment to the feature file.

## Next Steps
1. R6 records the R5 verdict and plans T001 against what D1, D2 and D3 ruled:
   the read endpoint over `list_decisions`, the blocked-size wiring from
   `blocked_downstream`, and a fixture per PRODUCING type.
2. T001 then lands that endpoint with its contract tests.

## Risks
- Open findings, stated with the rule and the commit DECISION F009 D10 requires:
  by §3 item 10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — `
  line — the open set is 236, measured at `f4311bf6`.
- The findings THIS FEATURE MUST STILL ACT ON — a narrower set, named as what it
  is and not called "open" — are R-0403, R-0413, R-0431, R-0445, R-0495, R-0533,
  R-0574, R-0601, R-0625, R-0632, R-0672, R-0674, R-0675, R-0676, R-0677 and
  R-0678, of which R-0495 and R-0574 are the two Highs, inherited from F085 and
  F086.
- THE TWO BADGE COUNTERS F031 MUST REPLACE ARE A CONSTANT ZERO TODAY, and they
  are named by their FUNCTIONS because the bare symbol is ambiguous: the
  `decision_count` local of `_build_dashboard` and the `open_decisions` sum of
  `_build_live_state_json`, both in `packages/orchestration/ui_server.py`, each
  count the event kind `human_decision_requested`, which no producer emits. A
  THIRD `decision_count`, in `_build_orchestrator_section` of the same file, is
  fed by `orchestrator_brain.list_decisions` and is NOT always zero and NOT part
  of this feature. All three readings were taken at `f4311bf6`.
- The record holds `Gate: R19` from F022 as its seed entry. If F031 reaches its
  own R19 that key collides — the §3 item 26 defect. A round before then renames
  the seed or the scheme; this bullet is the reminder.
