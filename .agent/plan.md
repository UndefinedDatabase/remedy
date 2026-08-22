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
R10 records the R9 verdict, adds R9's one surfaced defect as evidence to R-0437,
and closes the reviewer's session at its stated round cap of three delegated
rounds. It builds nothing and mints no finding id. The branch is mid-feature and
carries no pull request by design.

## Next Steps
1. R11 builds the bounded ring DECISION F021 D5 rules: `recent` on
   `BrainStreamState` and on `BrainStreamView`, appended inside
   `receiveBrainFrame` rather than in the runner's `dispatch`, so a reconnect
   replay cannot duplicate a row. `feedRowOf` is the projection it feeds.
2. R12 builds the feed and NowCard components over fixture streams, with the
   scroll discipline that never yanks a reader who has scrolled up, gated by a
   Python source contract under `tests/ui_contracts/`.
3. R13 onward T003: graph-focus wiring, the disabled steering input, and the
   additive envelope field DECISION F021 D2 permits.

## Risks
- The ring is the one place a reconnect can duplicate rows. `receiveBrainFrame`
  already drops a frame whose seq is not ahead of `lastSeq`; an append written
  anywhere else silently bypasses that guard.
- The view-identity contract `createBrainStreamRunner` documents is what the
  ring round is most likely to break: `useSyncExternalStore` compares with
  `Object.is`, so a freshly built array on every call re-renders forever.
- `npx vitest run` is DENIED to the reviewer's session class, so a frontend
  round's colour rests on the worker's transcript plus a red control the
  reviewer can verify from the authored bytes. Order the red control every time.
- Jump-to-node needs the additive envelope field DECISION F021 D2 permits. That
  is the one production seam this feature opens, and it stays one field.
- The open set holds no code defect of F021; R-0403, R-0607, R-0608, R-0609,
  R-0611 and R-0613 stay routed to a paydown branch.