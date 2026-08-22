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
R18 retires R-0652: the NowCard's live badge goes back to the agent's own
running flag, because a badge keyed to the stream ring latched on forever once
any action had arrived and rendered "Live" beside the word "Idle". R16's detail
line is unchanged. It also records the R17 verdict, which was PASS on all
fifteen gates, and registers R-0653.

## Next Steps
1. R19 builds the recency dot's PURE time rule — a function of the last action's
   arrival and a passed-in now, so the fade to idle after the quiet window is
   testable without a clock — and wires it, giving the badge and the dot one
   honest liveness source per T5_F021 line 63.
2. R20 wires the scroll rule into `ActivityFeedCard`: the scroll container, and
   the new-rows pill component_spec.md line 86 binds.
3. R21 gives each row its click-jump to the node, the graph-focus API T003 opens
   with, then T003: the disabled steering input with its honest tooltip.

## Risks
- No DOM environment exists in this repository, so components are gated by
  `npx tsc --noEmit` and by Python source contracts, and behaviour is put in
  PURE modules that vitest can reach.
- Vitest IS reviewer-runnable as `npm run test:unit` from `apps/ui` (R-0651),
  but ONLY green: a fresh worktree has no `node_modules` (R-0518) and the
  symlink that would supply them is denied, so no vitest case has ever been
  mutation-proved. Every pure module therefore also carries a Python source
  contract whose red control IS runnable — that is the compensating control,
  and R-0653 records it.
- Reflog gates name the OPERATION field, never the whole row, and marker sweeps
  are LINE-ANCHORED, never containment (R-0613, R-0364).
- No code defect of F021 is open once R18 lands; R-0364, R-0403, R-0607,
  R-0608, R-0609, R-0611, R-0613, R-0622, R-0651 and R-0653 stay routed to a
  paydown branch.
