# Plan — F040 Completion/return digest

Branch: feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge
commit of pull request 222. SESSION 2, round 9.

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
| T002 the card's copy rules and the §17 screen | done | this round |
| T002 the card itself, its mount and wiring | open | next session |
| T003 CLI parity and the end-to-end | open | |

## Next Steps
1. This round rules DECISION F040 D10 and builds `digestCardCopy.ts`: the state
   label the digest needs, and the rule turning the report's markup into copy
   the cockpit may show, with `scrubUiText` as the final §17 screen.
2. The next round mounts the card — the `.tsx`, the trigger wiring onto
   `digestVisibility`, the dismissal port bound at the edge per D8, and the
   stylesheet from round 8. Every rule it needs is now built and pinned.
3. Then T003's `remedy job digest`, the end-to-end, the integration gate and
   closure.

## Risks
- R-0570, R-0752 and R-0755 stay OPEN and are routed to the paydown branch; none
  is F040's to fix. R-0753 stays OPEN as this feature's documented risk.
- The card round is the first this feature cannot red-prove: a `.tsx` has no
  pure logic left to test and this repository renders no component. Every
  decidable rule has been pushed out of it on purpose, so what remains is
  wiring, pinned as TEXT by a guard.
