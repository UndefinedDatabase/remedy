# Plan — F040 Completion/return digest

Branch: feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge
commit of pull request 222. SESSION 2, round 7.

## Goal
Coming back is calm: a digest endpoint condenses state, cost with its basis, top
ownership entries, open decisions and ONE primary action into a hero card, shown
at job end or on the first UI open after absence — the "what happened while I
was gone" answer in one glance.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| the F040 claim and the seam inventory | done | round 1, PASS |
| the spec decisions D2 to D7 | done | rounds 2, 3, 5 and 6 |
| T001 the composition, endpoint, goldens | done | rounds 3-5, all PASS |
| T002 the client digest seam and its guard | done | round 6, PASS |
| T002 the trigger, dismiss and last-seen rule | done | this round |
| T002 the hero card and its CSS conformance | open | next |
| T003 CLI parity and the end-to-end | open | |

## Next Steps
1. This round rules where a dismissal persists (DECISION F040 D8) and builds
   `digestVisibility.ts` as a pure total rule over injected values — no clock,
   no storage, no copy.
2. The next round builds the hero card itself: the `.tsx` that binds the clock
   and the storage port at the edge, the binding CSS from the feature file, the
   copy audit its Acceptance names, and the CSS conformance guard.
3. Then T003's `remedy job digest`, the end-to-end, the integration gate and
   closure.

## Risks
- R-0570 and R-0752 stay OPEN, routed to the paydown branch. R-0753 stays OPEN
  as this feature's documented risk: the persisted actuals record has no money
  field, so the digest's cost basis can only answer `absent` in production.
- The urgency formula still has two homes until the TypeScript copy is retired,
  pinned equal by `tests/ui_contracts/test_decision_urgency_parity.py`.
