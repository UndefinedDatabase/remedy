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
R22 ships the PURE HALF of T002b filtering: `decisionFilter.ts` derives the
offered types from the models present, applies the chosen one and says what an
empty result means, with its tests beside it, plus the `decisionCard.ts` comment
repair. It also writes the R21 verdict, which no R21 artefact could carry.

## Next Steps
1. R23 wires the control into `DecisionInboxCard` and repairs that file's own
   `Recurrence: R-0593` note. `docs/ui/design_reference/` is binding under
   `.agent/context.md`: the FilterChips section of `component_spec.md` rules the
   interaction, and a control authored without reading it is a §4.5 block
   condition, not a finding.
2. T002b BADGE under DECISION F031 D2: it re-derives on refetch over the
   existing SSE stream, no new event kind, D2's two constant-zero counters
   replaced.
3. T003 wires answering through the existing write channel and rules
   `NeedsAttentionCard` (DECISION F031 D4); then the integration-gate round and
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- THE EMPTY-STATE TRAP, waiting for R23: `DecisionInboxCard` opens with
  `if (decisions.length === 0) return null;`, and that guard must keep reading
  the UNFILTERED list. Filtering to zero matches would otherwise unmount the
  card AND its own control and strand the operator with no way back.
- NO TEST REACHES THE MARKUP under DECISION F031 D5, so every branch that can
  live in `apps/ui/src/api/` is placed there, where the shipped vitest config
  reaches it, and R23's markup stays a projection pinned by review alone.
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 238 at `f13b92c0`, unchanged by this round.
- The findings THIS FEATURE MUST STILL ACT ON are R-0403, R-0413, R-0431,
  R-0441, R-0445, R-0471, R-0495, R-0533, R-0574, R-0593, R-0601, R-0622,
  R-0625, R-0632, R-0672, R-0674, R-0675, R-0676, R-0677, R-0678 and R-0679;
  R-0495 and R-0574 are the two Highs.
- BLOCK CAPS ARE TWO, not one: 490 lines TOTAL (DECISION F085 D6) and 400 lines
  PROSE (DECISION F085 D5); every block states and re-measures both.
