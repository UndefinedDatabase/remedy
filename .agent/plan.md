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
R12 builds the STATE half of the bounded ring DECISION F021 D5 rules: `recent`
and `recentDropped` on `BrainStreamState`, appended inside `receiveBrainFrame`
behind its replay guard, bounded at `BRAIN_RECENT_LIMIT` with the drop counted.
It also records the R11 verdict, which was PASS on every gate.

## Next Steps
1. R13 publishes the ring on `BrainStreamView` in `brainStreamRunner.ts`.
   `publish()` compares `recent` BY REFERENCE, sound only because
   `receiveBrainFrame` returns the identical state object when it drops a
   replay, and `cachedView` is seeded FROM the initial state rather than from a
   fresh `[]`, or the very first publish fires on nothing.
2. R14 builds the feed and NowCard over fixture streams, with the scroll
   discipline that never yanks a reader who has scrolled up, and the
   dropped-rows notice that points at the timeline.
3. R15 onward T003: graph-focus wiring, the disabled steering input, and the
   additive envelope field DECISION F021 D2 permits.

## Risks
- The view-identity contract `createBrainStreamRunner` documents is what R13 is
  most likely to break: `useSyncExternalStore` compares with `Object.is`, so a
  freshly built array on every call re-renders forever.
- `npx vitest run` is DENIED to the reviewer's session class, so a frontend
  round's vitest colour rests on the worker's transcript. `npx tsc --noEmit`
  and the Python source contracts ARE reviewer-runnable, so every frontend
  round carries a Python red control the reviewer reproduces itself.
- A block's newline convention is stated PER SLICE KIND: R-0650 the hard way.
- No code defect of F021 is open; R-0403, R-0607, R-0608, R-0609, R-0611,
  R-0613 and R-0622 stay routed to a paydown branch.
