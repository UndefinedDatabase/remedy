# Plan — F040 Completion/return digest

Branch: feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge
commit of pull request 222. SESSION 2, round 6.

## Goal
Coming back is calm: a digest endpoint condenses state, cost with its basis, top
ownership entries, open decisions and ONE primary action into a hero card, shown
at job end or on the first UI open after absence — the "what happened while I
was gone" answer in one glance.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| the F040 claim and the seam inventory | done | round 1, PASS |
| the spec decisions D2 to D6 | done | rounds 2, 3 and 5 |
| T001 the composition module and its tests | done | round 3, PASS |
| T001 the endpoint and its route tests | done | round 4, PASS |
| T001 the envelope goldens, R-0754 closed | done | round 5, PASS |
| T002 the client digest seam and its guard | done | this round |
| T002 the trigger, dismiss and last-seen rule | open | next |
| T002 the hero card and its CSS conformance | open | |
| T003 CLI parity and the end-to-end | open | |

## Next Steps
1. This round gives the browser a pure `jobDigest.ts` — decode, path, cost line
   — reading the exactness string from `costMetric.ts` rather than restating it,
   plus the Python guard that pins the module's purity.
2. The next round rules where a dismissal persists and builds the show/dismiss/
   last-seen rule as a pure function over an injected seam, the shape
   `decisionNonce.ts` established.
3. Then the hero card itself with its CSS conformance guard, and T003's
   `remedy job digest` plus the end-to-end, the integration gate and closure.

## Risks
- R-0570 and R-0752 stay OPEN, routed to the paydown branch. R-0753 stays OPEN
  as this feature's documented risk: the persisted actuals record has no money
  field, so the digest's cost basis can only answer `absent` in production.
- Two homes for the urgency formula exist until the TypeScript copy is retired,
  pinned equal by `tests/ui_contracts/test_decision_urgency_parity.py`.
