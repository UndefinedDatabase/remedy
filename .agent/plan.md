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
R17 writes the feed's scroll discipline as a PURE rule in `feedScroll.ts` with
its vitest and a source contract: a reader at the newest edge is followed, a
reader who scrolled up is never yanked, and rows arriving meanwhile accumulate
as an unseen count that clears only on return. Nothing is wired this round. It
also records the R16 verdict, which was PASS on all fifteen gates, and registers
R-0652.

## Next Steps
1. R18 adds the recency dot over a PURE time function, so the fade to idle after
   the quiet window is testable without a clock. It also OWES the R-0652 repair:
   the NowCard's live badge must fade with that same rule instead of latching on
   forever once any action has entered the ring.
2. R19 wires both pure rules into `ActivityFeedCard` — the scroll container, the
   new-rows pill component_spec.md line 86 binds, and the dot.
3. R20 gives each row its click-jump to the node, the graph-focus API T003 opens
   with, then T003: the disabled steering input with its honest tooltip.

## Risks
- No DOM environment exists in this repository, so components are gated by
  `npx tsc --noEmit` and by Python source contracts, and behaviour is put in
  PURE modules that vitest can reach. A rule expressed as a scroll side effect
  would be untestable here, which is why R17 lands headless.
- Vitest IS reviewer-runnable as `npm run test:unit` from `apps/ui`; only the
  bare `npx vitest` spelling is denied (R-0651). Gate it that way and re-run it
  at review. It stays vacuous in a fresh worktree, which has no `node_modules`
  (R-0518), unless that directory is symlinked in.
- Reflog gates name the OPERATION field, never the whole row, and marker sweeps
  are LINE-ANCHORED, never containment (R-0613, R-0364).
- R-0652 is the one open code defect of F021 and R18 owns it; R-0364, R-0403,
  R-0607, R-0608, R-0609, R-0611, R-0613, R-0622 and R-0651 stay routed to a
  paydown branch.
