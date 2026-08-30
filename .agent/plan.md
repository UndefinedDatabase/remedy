# Plan — F258 Self-use track v2

Branch: feature/f258-self-use-v2, cut from `main` at `18ae7129`, the merge
commit of pull request 225. SESSION 1, round 3.

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
| T001 part 2 — the generator module, tier 1 | done | this round |
| T001 part 3 — wiring the closure protocol doc | open | next round |
| T002 consumed means executed | open | |
| T003 findings flow back | open | |

## Next Steps
1. This round builds `packages/orchestration/self_use_generator.py`: Tier 1
   (the finding ledger) is real and tested; Tiers 2-3 are honest `None`
   placeholders per DECISION F258 D2. Nothing calls it yet — the real queue
   is untouched.
2. The round after it wires `generate_and_append_if_empty` into
   `docs/roadmap/STATUS_closure_protocol.md` precondition 6's own text, so a
   future closure round reads "call the generator" rather than "curate by
   hand" — still a session/human action, since nothing in this protocol runs
   unattended, but the function now exists to call.
3. T002 depends on a generated item actually being run, not just appended;
   T003 wires existing finding-ledger machinery once T002 exists.

## Risks
- R-0570 (Low) stays OPEN, routed away, unrelated to this branch.
- Tiers 2 and 3 are placeholders, not gaps hidden from the record: DECISION
  F258 D2 names exactly what each needs before it can be real.