# Plan — F040 Completion/return digest

Branch: feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge
commit of pull request 222. SESSION 3, round 11.

## Goal
Coming back is calm: a digest endpoint condenses state, cost with its basis, top
ownership entries, open decisions and ONE primary action into a hero card, shown
at job end or on the first UI open after absence — the "what happened while I
was gone" answer in one glance.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| the spec decisions D2 to D10 | done | rounds 2-9 |
| T001 the composition, endpoint, goldens | done | rounds 3-5, all PASS |
| T002 the client digest seam and its guard | done | round 6, PASS |
| T002 the trigger, dismiss and last-seen rule | done | round 7, PASS |
| T002 the hero card stylesheet and its guard | done | round 8, PASS |
| T002 the card's copy rules and the §17 screen | done | round 9, PASS |
| T002 the card component and its guard | done | this round |
| T002 the mount, the data load and the layout CSS | open | next |
| T003 CLI parity and the end-to-end | open | |

## Next Steps
1. This round builds `DigestHeroCard.tsx` with the dismissal port bound at its
   edge, pins it with a pytest text guard, and repairs R-0756 — the prototype
   test round 9 shipped blind.
2. The next round MOUNTS the card: the shell placement, the digest load through
   `jobDigestPath`, the last-seen clock, and the layout CSS this round
   deliberately did not write.
3. Then T003's `remedy job digest`, the end-to-end, the integration gate and
   closure.

## Risks
- R-0570, R-0752 and R-0755 stay OPEN and are routed to the paydown branch; none
  is F040's to fix. R-0753 stays OPEN as this feature's documented risk.
- The card gets no vitest colour at all, and the reason is the runner rather than
  the session: `apps/ui/vitest.config.ts` sets `environment: "node"` and includes
  `src/**/*.test.ts` only, and the package ships no DOM library, so a `.tsx` is
  neither collected nor renderable. Its colour is a pytest text guard, which IS
  red proved, plus `tsc`.