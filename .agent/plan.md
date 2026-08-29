# Plan — F040 Completion/return digest

Branch: feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge
commit of pull request 222. SESSION 1, round 3.

## Goal
Coming back is calm: a digest endpoint condenses state, cost with its basis, top
ownership entries, open decisions and ONE primary action into a hero card, shown
at job end or on the first UI open after absence — the "what happened while I
was gone" answer in one glance.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| the F040 claim and the seam inventory | done | round 1, PASS |
| the spec decisions D2, D3 and D4 | done | round 2, PASS |
| the one-source urgency and R-0751 | done | round 2, PASS |
| T001 the composition module and its tests | done | this round |
| T001 the endpoint, its route tests and goldens | open | next round |
| T002 the hero card, triggers, the TS retirement | open | |
| T003 CLI parity and the end-to-end | open | |

## Next Steps
1. This round builds `packages/orchestration/job_digest.py` as a pure
   composition over the report sources, the inbox read path and the budget
   counters, with the four state-shape fixtures its tests are named for.
2. The round after it wires the endpoint into the server's handlers dict, adds
   its route tests and the goldens.
3. T002 then builds the hero card and retires the TypeScript urgency copy per
   DECISION F040 D2; T003 adds CLI parity and the end-to-end.

## Risks
- R-0570 and R-0752 (both Low) stay OPEN and are routed to the paydown branch:
  their fixes edit `README.md`, `tests/docs/test_docs_consistency.py` and
  thirteen feature files, none of which F040 owns.
- Two homes for the urgency formula exist until T002. They are pinned equal by
  `tests/ui_contracts/test_decision_urgency_parity.py` rather than trusted.
