# Plan — F040 Completion/return digest

Branch: feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge
commit of pull request 222. SESSION 2, round 5.

## Goal
Coming back is calm: a digest endpoint condenses state, cost with its basis, top
ownership entries, open decisions and ONE primary action into a hero card, shown
at job end or on the first UI open after absence — the "what happened while I
was gone" answer in one glance.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| the F040 claim and the seam inventory | done | round 1, PASS |
| the spec decisions D2 to D5 | done | rounds 2 and 3 |
| the one-source urgency and R-0751 | done | round 2, PASS |
| T001 the composition module and its tests | done | round 3, PASS |
| T001 the endpoint and its route tests | done | round 4, PASS |
| T001 the envelope goldens and R-0754 | done | this round |
| T002 the hero card, triggers, the TS retirement | open | next |
| T003 CLI parity and the end-to-end | open | |

## Next Steps
1. This round meets T001's last acceptance clause: one stored envelope golden
   per state shape, frozen and never self-blessed. T001 is complete when it
   lands — the goldens were the clause round 4 left open.
2. T002 builds the hero card against the design reference, wires the trigger,
   dismiss and last-seen mechanics, and retires the TypeScript urgency copy per
   DECISION F040 D2.
3. T003 adds `remedy job digest` and the end-to-end, then the integration gate
   and closure.

## Risks
- R-0570, R-0752 and R-0753 stay OPEN. The first two are routed to the paydown
  branch; R-0753 is a documented risk this feature carries, because the persisted
  actuals record has no money field for the digest's cost basis to read.
- Two homes for the urgency formula exist until T002, pinned equal by
  `tests/ui_contracts/test_decision_urgency_parity.py` rather than trusted.
