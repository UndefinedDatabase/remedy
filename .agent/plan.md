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
R21 is a RECORD round: it writes the R20 verdict into the ledger under the
DECISION F031 D7 key and adds two new instances to the open finding R-0593
instead of minting an id. No code ships. T002b ORDERING is SHIPPED and gated.

## Next Steps
1. R22 ships T002b FILTERING by TYPE, which DECISION F031 D6 narrows from the
   feature file's "filters by type/job" because `DecisionInboxEntry` carries no
   job field. READ `docs/ui/design_reference/` FIRST — `.agent/context.md` makes
   it binding for this feature and a control authored without it is a §4.5 block
   condition, not a finding. R22 also repairs the two comments R-0593 names.
2. T002b BADGE under DECISION F031 D2: it re-derives on refetch over the
   existing SSE stream, no new event kind, D2's two constant-zero counters
   replaced.
3. T003 wires answering through the existing write channel and rules
   `NeedsAttentionCard` (DECISION F031 D4).

## Risks
- THE EMPTY-STATE TRAP IN R22, found by the reviewer while mapping the ground:
  `DecisionInboxCard` opens with `if (decisions.length === 0) return null;`. If a
  filter is applied to the list that guard reads, filtering to zero matches
  unmounts the card AND its own filter control, stranding the operator with no
  way back. The guard must read the UNFILTERED list.
- THE PURE/MARKUP SPLIT under DECISION F031 D5: the filter PREDICATE and the
  list of types offered belong in `apps/ui/src/api/`, where the shipped vitest
  config reaches them; only the control and its `useState` may live in the
  markup, which no test reaches.
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 238 at `a462932f`, unchanged by this round.
- The findings THIS FEATURE MUST STILL ACT ON are R-0403, R-0413, R-0431,
  R-0441, R-0445, R-0471, R-0495, R-0533, R-0574, R-0593, R-0601, R-0622,
  R-0625, R-0632, R-0672, R-0674, R-0675, R-0676, R-0677, R-0678 and R-0679;
  R-0495 and R-0574 are the two Highs. R-0593 joins this list at C2.
- BLOCK CAPS ARE TWO, not one: 490 lines TOTAL (DECISION F085 D6) and 400 lines
  PROSE (DECISION F085 D5); every block states and re-measures both.
