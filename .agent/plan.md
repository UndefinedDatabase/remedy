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
R13 publishes the ring on `BrainStreamView`: `recent` and `recentDropped` join
the view, `publish()` compares the ring by reference, and `cachedView` is seeded
from the initial state so the first timer announces nothing. It also records the
R12 verdict, which was PASS on every gate.

## Next Steps
1. R14 builds the feed and NowCard components over the published ring, read
   from the ONE `useBrainStream` call `RemedyShell` already makes — no second
   call, no new `EventSource`. `recentDropped` above zero renders the
   dropped-rows notice that points at the timeline.
2. R15 adds the scroll discipline that never yanks a reader who has scrolled
   up, over fixture streams, gated by a Python source contract.
3. R16 onward T003: graph-focus wiring, the disabled steering input, and the
   additive envelope field DECISION F021 D2 permits.

## Risks
- `useSyncExternalStore` compares with `Object.is`. Any later edit that rebuilds
  the view or the ring on every call re-renders forever; the contract tests in
  `tests/ui_contracts/test_brain_stream_ring.py` are what hold that line.
- `npx vitest run` is DENIED to the reviewer's session class, so a frontend
  round's vitest colour rests on the worker's transcript. `npx tsc --noEmit`
  and the Python source contracts ARE reviewer-runnable, so every frontend
  round carries a Python red control the reviewer reproduces itself.
- A block's newline convention is stated PER SLICE KIND: R-0650 the hard way.
- No code defect of F021 is open; R-0403, R-0607, R-0608, R-0609, R-0611,
  R-0613 and R-0622 stay routed to a paydown branch.
