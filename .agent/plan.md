# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `f031_*_inventory.md` the inventories, `.agent/decisions.md` D1–D9.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R24 OPENS T002b's badge with its SERVER half: one re-derivation over
`decision_queue.list_decisions` replaces the two constant-zero counters DECISION
F031 D2 names in `ui_server.py`, so `metrics.open` and `open_decision_count`
answer with a real number, pinned by tests in both builder suites.

## Next Steps
1. R25 the badge's UI half — the count rendered where the operator sees it —
   plus the two comment repairs R-0682 and the R-0593 recurrence route there.
2. T003 wires answering through the existing write channel and rules
   `NeedsAttentionCard` (DECISION F031 D4).
3. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- THE COUNT IS A NEW READ ON A HOT PATH: `_build_live_state_json` answers the
  cockpit's poll, so the derivation it now calls must stay total and cheap. It
  is measured at 0.309 ms for 50 tasks against 500 events, and every branch of
  `list_decisions` already guards itself, but a raise escaping it would break
  the dashboard rather than the badge.
- A FAILURE READS AS ZERO, because both fields are typed `int` and carry no
  unknown state. That is honest only while the WHY comment above the helper
  says so and names `_build_orchestrator_section` as the richer shape.
- NO EVENT KIND IS ADDED, per DECISION F031 D2. A round that "fixes" the badge
  by emitting `decision.requested` has left this design, not completed it.
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 238 at `f548277e`, and this round's C2 raises it to 239 by minting
  R-0682, in the commit order the R24 block's constraint 4 fixes.
- The findings THIS FEATURE MUST STILL ACT ON are R-0403, R-0413, R-0431,
  R-0441, R-0445, R-0471, R-0495, R-0533, R-0574, R-0593, R-0601, R-0622,
  R-0625, R-0632, R-0672, R-0674, R-0675, R-0676, R-0677, R-0678, R-0679 and
  R-0682; R-0495 and R-0574 are the two Highs.
- BLOCK CAPS ARE TWO, not one: 490 lines TOTAL (DECISION F085 D6) and 400 lines
  PROSE (DECISION F085 D5); every block states and re-measures both.
