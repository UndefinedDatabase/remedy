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
R20 builds the activity dot's rule as a PURE function in `recency.ts` with its
vitest and a source contract — the work R19 halted before reaching. It also
records R19, which HALTED at a self-contradicting gate of the reviewer's own
making, and registers R-0654.

## Next Steps
1. R21 wires BOTH pure rules: `recency.ts` becomes the ONE liveness source for
   the NowCard's badge AND its dot, and `feedScroll.ts` drives the feed's scroll
   container and the new-rows pill component_spec.md line 86 binds.
2. R22 gives each row its click-jump to the node, then T003: the disabled
   steering input with its honest tooltip.
3. Closure: the evidence round, then the STATUS-commit round.

## Risks
- No DOM environment exists here, so components are gated by `npx tsc --noEmit`
  and by Python source contracts, and behaviour lives in PURE modules vitest can
  reach. The wiring round is the risky one.
- Vitest is reviewer-runnable as `npm run test:unit` (R-0651) but only GREEN: a
  worktree has no `node_modules` (R-0518), so no vitest case has been
  mutation-proved. The Python contract is the mutation-proved guard (R-0653).
- A source contract must assert a DISCRIMINATING string: `"none"` also appears
  in the `RecencyLevel` union, so the pre-stream guard asserts the whole return
  statement rather than the bare token.
- A plan slice is MEASURED before its gate is written: R19 died because its gate
  demanded a line count its own slice could not have (R-0654).
- No code defect of F021 is open; R-0364, R-0403, R-0607, R-0608, R-0609,
  R-0611, R-0613, R-0622, R-0651 and R-0653 stay routed to a paydown branch.
