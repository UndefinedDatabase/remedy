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
R14 makes the feed LIVE: the ring travels from the one `useBrainStream` call
down through `RightLivePanel` into `ActivityFeedCard`, which renders the newest
rows first and says so when the bound dropped some. It also records the R13
verdict, which was PASS on every gate.

## Next Steps
1. R15 adds the scroll discipline that never yanks a reader who has scrolled
   up, and the NowCard over the ACTION-class subset with its recency dot.
2. R16 gives each row its click-jump to the node, which is the graph-focus API
   T003 opens with.
3. R17 onward T003: the disabled steering input with its honest tooltip, and
   the additive envelope field DECISION F021 D2 permits.

## Risks
- No DOM environment exists in this repository, so components are gated by
  `npx tsc --noEmit` and by Python source contracts. A contract that reads a
  prop name is the only thing standing between "published" and "rendered".
- `useSyncExternalStore` compares with `Object.is`. Any later edit that rebuilds
  the view or the ring on every call re-renders forever; the contract tests in
  `tests/ui_contracts/test_brain_stream_ring.py` hold that line.
- `npx vitest run` is DENIED to the reviewer's session class, so a frontend
  round's vitest colour rests on the worker's transcript. Every such round
  carries a Python red control the reviewer reproduces itself.
- Reflog gates name the OPERATION field, never the whole row: this repository's
  commit subjects discuss amends by design (R-0613).
- No code defect of F021 is open; R-0403, R-0607, R-0608, R-0609, R-0611,
  R-0613 and R-0622 stay routed to a paydown branch.
