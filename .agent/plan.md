# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `f031_*_inventory.md` the inventories, `.agent/decisions.md` D1–D8.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R23 CLOSES T002b's filtering half: `DecisionInboxCard` holds the chosen type in
its own state, draws the chips `decisionTypeChoices` derives and shows the quiet
line `decisionInboxView` returns when none survive. It also repairs the last two
`R-0593` comments inside this feature and writes the R22 verdict.

## Next Steps
1. T002b BADGE under DECISION F031 D2: it re-derives on refetch over the
   existing SSE stream, no new event kind, D2's two constant-zero counters
   replaced.
2. T003 wires answering through the existing write channel and rules
   `NeedsAttentionCard` (DECISION F031 D4).
3. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- THE EMPTY-STATE TRAP IS LIVE THIS ROUND: `DecisionInboxCard` opens with
  `if (decisions.length === 0) return null;`, and that guard must keep reading
  the UNFILTERED prop. Filtering to zero would otherwise unmount the card AND
  its own control and strand the operator with no way back, which is the whole
  reason `decisionInboxView` returns a quiet line instead.
- NO TEST REACHES THE MARKUP under DECISION F031 D5, so this round's `.tsx` is
  pinned by `tsc`, by structure and by review alone. Every branch that could
  live in `apps/ui/src/api/` already does, and R23 adds no test by design.
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 238 at `aa48d967`, unchanged by this round.
- The findings THIS FEATURE MUST STILL ACT ON are R-0403, R-0413, R-0431,
  R-0441, R-0445, R-0471, R-0495, R-0533, R-0574, R-0593, R-0601, R-0622,
  R-0625, R-0632, R-0672, R-0674, R-0675, R-0676, R-0677, R-0678 and R-0679;
  R-0495 and R-0574 are the two Highs.
- BLOCK CAPS ARE TWO, not one: 490 lines TOTAL (DECISION F085 D6) and 400 lines
  PROSE (DECISION F085 D5); every block states and re-measures both.
