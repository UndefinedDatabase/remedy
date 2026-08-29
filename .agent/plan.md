# Plan — F040 Completion/return digest

Branch: feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge
commit of pull request 222. SESSION 2, round 8.

## Goal
Coming back is calm: a digest endpoint condenses state, cost with its basis, top
ownership entries, open decisions and ONE primary action into a hero card, shown
at job end or on the first UI open after absence — the "what happened while I
was gone" answer in one glance.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| the spec decisions D2 to D9 | done | rounds 2-8 |
| T001 the composition, endpoint, goldens | done | rounds 3-5, all PASS |
| T002 the client digest seam and its guard | done | round 6, PASS |
| T002 the trigger, dismiss and last-seen rule | done | round 7, PASS |
| T002 the hero card stylesheet and its guard | done | this round |
| T002 the card, its mount and the copy audit | open | next |
| T003 CLI parity and the end-to-end | open | |

## Next Steps
1. This round transcribes the feature file's binding CSS into
   `DigestHeroCard.module.css` and pins it with a conformance guard, the split
   F037 used when a component could not be render-tested.
2. The next round mounts the card: the `.tsx`, the trigger wiring onto
   `digestVisibility`, the dismissal port bound at the edge per DECISION F040
   D8, and the copy audit the Acceptance names.
3. Then T003's `remedy job digest`, the end-to-end, the integration gate and
   closure.

## Risks
- R-0570, R-0752 and R-0755 stay OPEN and are routed to the paydown branch; none
  is F040's to fix. R-0753 stays OPEN as this feature's documented risk.
- THE CARD ROUND MUST SETTLE A COPY COLLISION: `ux_spec.md` §17 forbids the UI
  showing raw UUIDs, and the digest's own `primary_action.label` embeds a job-id
  prefix and a `td:` decision id — visible in the R5 goldens. The card either
  humanises that label or the envelope stops carrying it; a DECISION, not a
  silent choice.
