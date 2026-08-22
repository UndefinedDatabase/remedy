# Plan — F021 Live activity feed + now-card

Branch: feature/f021-live-activity-feed, cut from `main` at `4548995d`, the merge
commit of pull request #210, which the reviewer merged at the Open PR Gate before
this branch was created. `.agent/live_review.md` is the source of truth for the
open set, the round map and the finding-id ceiling.

## Goal
The raw SSE event stream becomes a story a human can follow: a humanization
catalog maps event kinds to plain lines, a NowCard shows the newest ACTION-class
event with a recency dot, and feed rows carry their seq and click-jump to their
node. DONE when the catalog covers the kind set DECISION F021 D3 rules and an
unknown kind renders an honest generic line rather than vanishing, the feed
renders fixture streams per the binding CSS, jump-to-node focuses the right
node, and the steering input renders DISABLED with its tooltip until F030.

## Current Step
R19 writes the activity dot's rule as a PURE function in `recency.ts` with its
vitest and a source contract: `none` before anything has acted, `fresh` inside
the fresh window, `fading` until the quiet window closes, `idle` after it, and
`fresh` rather than `idle` when the clocks disagree. `nowMs` is passed in and no
clock is read. Nothing is wired this round. It also records the R18 verdict,
which was PASS on all fourteen gates.

## Next Steps
1. R20 wires BOTH pure rules: `recency.ts` becomes the ONE liveness source for
   the NowCard's badge AND its new dot, which is what keeps them from
   disagreeing, and `feedScroll.ts` drives the feed's scroll container and the
   new-rows pill component_spec.md line 86 binds.
2. R21 gives each row its click-jump to the node, the graph-focus API T003 opens
   with, then T003: the disabled steering input with its honest tooltip.
3. Closure: the evidence round, then the STATUS-commit round.

## Risks
- No DOM environment exists in this repository, so components are gated by
  `npx tsc --noEmit` and by Python source contracts, and behaviour is put in
  PURE modules that vitest can reach. Wiring rounds are therefore the risky
  ones, and R20 is the last of them.
- Vitest IS reviewer-runnable as `npm run test:unit` from `apps/ui` (R-0651),
  but ONLY green: a fresh worktree has no `node_modules` (R-0518) and the
  symlink that would supply them is denied, so no vitest case has ever been
  mutation-proved. Every pure module therefore also carries a Python source
  contract whose red control IS runnable — that is the compensating control,
  and R-0653 records it.
- A source contract must assert a discriminating string. `"none"` also appears
  in the `RecencyLevel` union, so the pre-stream guard asserts the whole return
  statement; a looser guard survives the mutation it exists to catch.
- Reflog gates name the OPERATION field, never the whole row, and marker sweeps
  are LINE-ANCHORED, never containment (R-0613, R-0364).
- No code defect of F021 is open; R-0364, R-0403, R-0607, R-0608, R-0609,
  R-0611, R-0613, R-0622, R-0651 and R-0653 stay routed to a paydown branch.
