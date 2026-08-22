# Plan — F021 Live activity feed + now-card

Branch: feature/f021-live-activity-feed, cut from `main` at `4548995d`, the merge
commit of pull request #210. `.agent/live_review.md` is the source of truth for
the open set, the round map and the finding-id ceiling.

## Goal
The raw SSE event stream becomes a story a human can follow: a humanization
catalog maps event kinds to plain lines, a NowCard shows the newest ACTION-class
event with a recency dot, and feed rows carry their seq and click-jump to their
node. DONE when the catalog covers the kind set DECISION F021 D3 rules and an
unknown kind renders an honest generic line rather than vanishing, the feed
renders fixture streams per the binding CSS, jump-to-node focuses the right
node, and the steering input renders DISABLED with its tooltip until F030.

## Current Step
R21 records R20, which PASSED all fifteen gates, registers R-0655 and corrects
in a NEW entry the false numeral R20 left in the ledger. No code changes: the
four pure rules are built and the wiring round has not begun.

## Next Steps
1. R22 is THE WIRING ROUND and the largest component change of this feature:
   `recency.ts` becomes the ONE liveness source for the NowCard's badge AND its
   new dot, and `feedScroll.ts` drives the feed's scroll container and the
   new-rows pill component_spec.md line 86 binds. It is the first round needing
   CSS, so `docs/ui/design_reference/assets_spec.md` is the asset authority.
2. R23 gives each row its click-jump to the node, then T003: the disabled
   steering input with its honest tooltip.
3. Closure: the evidence round, then the STATUS-commit round.

## Risks
- No DOM environment exists here, so components are gated by `npx tsc --noEmit`
  and by Python source contracts. R22 wires four rules at once and is where that
  gap bites hardest; consider splitting it if its block exceeds the cap.
- Vitest is reviewer-runnable as `npm run test:unit` (R-0651) but only GREEN: a
  worktree has no `node_modules` (R-0518), so no vitest case has been
  mutation-proved. The Python contract is the mutation-proved guard (R-0653).
- A gate that names a line count states the MEASURED value, never a bound the
  slice was not checked against (R-0654); and a numeral corrected in one place
  is swept everywhere the block quotes it (R-0655).
- No code defect of F021 is open; R-0364, R-0403, R-0607, R-0608, R-0609,
  R-0611, R-0613, R-0622, R-0651, R-0653, R-0654 and R-0655 stay routed to a
  paydown branch.
