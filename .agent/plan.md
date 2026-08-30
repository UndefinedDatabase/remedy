# Plan — F258 Self-use track v2

Branch: feature/f258-self-use-v2, cut from `main` at `18ae7129`, the merge
commit of pull request 225. SESSION 1, opening the feature.

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
| the F040 closure candidate | done | this round; no id spent |
| the F258 claim and the branch | done | this round |
| the seam inventory | done | this round, `.agent/f258_inventory.md` |
| T001 the self-replenishing generator | open | next round, ordered from the inventory |
| T002 consumed means executed | open | |
| T003 findings flow back | open | |

## Next Steps
1. This round claims F258, discharges the one candidate F040's closure gate
   raised (new evidence on the already-open R-0570, no new id), and measures
   the queue/planner/job-execution/budget/approval seams T001-T003 compose
   over.
2. The round after it orders T001 — the generator's source-priority logic and
   its `provenance` field — from what the inventory measured; there is
   currently NO code caller of `plan_next_self_use_item` at any closure point,
   so the inventory names exactly what today's manual precondition-6 step
   does instead.
3. T002 depends on T001 producing a real item to run against; T003 is largely
   wiring existing finding-ledger machinery once T002 exists.

## Risks
- R-0570 (Low) stays OPEN and is deliberately NOT repaired here — same reason
  as F040's own round 1: the fix edits `README.md` and a test neither F258
  owns, and AGENTS.md forbids mixing an unrelated fix into a feature branch.
- The queue's `consumed_by`-is-closure-only invariant (DECISION F257 D2) binds
  T001: the generator may APPEND a new pending item but must never be the
  thing that marks one consumed.
