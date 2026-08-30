# Plan — F258 Self-use track v2

Branch: feature/f258-self-use-v2, cut from `main` at `18ae7129`, the merge
commit of pull request 225. SESSION 1, round 4.

## Goal
"Remedy is used on Remedy" keeps running with zero operator input: a generator
replenishes the self-use queue with exactly one dated, provenanced item
whenever it is empty at close, the consumed item is actually RUN through the
real job path under a small budget and stopped at the normal approval gate
rather than only planned, and any defect the run surfaces flows back into the
standard finding ledger.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| the F040 closure candidate | done | round 1 |
| the F258 claim and the seam inventory | done | round 1 |
| T001 part 1 — schema v2, the provenance field | done | round 2 |
| T001 part 2 — the generator module, tier 1 | done | round 3 |
| T001 part 3 — wiring the closure protocol doc | done | this round |
| T002 consumed means executed | open | |
| T003 findings flow back | open | |

## Next Steps
1. This round is docs-only: precondition 6 now names the generator as the
   step before "exhausted," and the two stale "never discovers" claims are
   corrected to point at the loader/generator split rather than contradict
   the module that now generates.
2. T001 itself is now feature-complete against the feature file's own text
   (the generator exists, fires when empty, is tested end to end). T002 is
   next: actually RUNNING a consumed item through the real job path under a
   small budget to the approval gate, not merely planning it.
3. T003 wires existing finding-ledger machinery once T002 exists.

## Risks
- R-0570 (Low) stays OPEN, routed away, unrelated to this branch.
- T002's "small dedicated budget" and "isolated worktree" seams were named,
  not yet designed, by round 1's inventory (`.agent/f258_inventory.md` §4-5)
  — the next round's own DECISION settles the concrete flags and commands.
