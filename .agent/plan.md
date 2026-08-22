# Plan — F021 Live activity feed + now-card

Branch: feature/f021-live-activity-feed, cut from `main` at `4548995d`, the merge
commit of pull request #210, which the reviewer merged at the Open PR Gate before
this branch was created. `.agent/live_review.md` is the source of truth for the
open set, the round map and the finding-id ceiling.

## Goal
The raw SSE event stream becomes a story a human can follow: a humanization
catalog maps the streamed event kinds to plain lines, a NowCard shows the newest
ACTION-class event with a recency-driven activity dot, and feed rows carry their
seq and click-jump to their node in the graph. DONE when the catalog covers the
kind set DECISION F021 D3 rules and an unknown kind renders an honest generic
line rather than vanishing, the feed renders fixture streams per the binding CSS,
jump-to-node focuses the right node, and the steering input renders DISABLED with
its honest tooltip until F030 lands.

## Current Step
R9 records the R8 verdict and ships T002's first production code: the pure
projection from a brain-stream frame to a feed row, with its node-vitest tests,
under the test discipline DECISION F021 D4 rules. It mints no finding id. The
module is deliberately uncalled until R10 wires it to the ring.

## Next Steps
1. R10 builds the bounded ring DECISION F021 D5 rules: `recent` on
   `BrainStreamState` and on `BrainStreamView`, appended inside
   `receiveBrainFrame` rather than in the runner's `dispatch`, so a reconnect
   replay cannot duplicate a row.
2. R11 builds the feed and NowCard components over fixture streams, with the
   scroll discipline that never yanks a reader who has scrolled up, gated by a
   Python source contract under `tests/ui_contracts/`.
3. R12 onward T003: graph-focus wiring, the disabled steering input, and the
   additive envelope field DECISION F021 D2 permits.

## Risks
- The ring is the one place a reconnect can duplicate rows. `receiveBrainFrame`
  already drops a frame whose seq is not ahead of `lastSeq`; an append written
  anywhere else silently bypasses that guard.
- The view-identity contract `createBrainStreamRunner` documents is what R10 is
  most likely to break: `useSyncExternalStore` compares with `Object.is`, so a
  freshly built array on every call re-renders forever.
- Jump-to-node needs the additive envelope field DECISION F021 D2 permits. That
  is the one production seam this feature opens, and it stays one field.
- The catalog covers only what a static walk can see. The generic line carries
  the eleven runtime-computed emitters, and R-0649 records that the walk's roots
  also reach vendored third-party Python.
- The open set holds no code defect of F021; R-0403, R-0607, R-0608, R-0609,
  R-0611 and R-0613 stay routed to a paydown branch.
