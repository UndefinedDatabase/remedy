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
R8 records the R7 verdict, adds the R7 evidence to R-0585, and rules the two
infrastructure DECISIONS T002 depends on: F021 D4 on the frontend test
environment and F021 D5 on the single-subscription fan-out. It mints no finding
id and builds nothing. The branch is mid-feature and carries no pull request by
design.

## Next Steps
1. R9 builds T002 on the ground D4 and D5 rule: the feed, its rows and the
   NowCard over fixture streams, with the scroll discipline that never yanks a
   reader who has scrolled up.
2. R10 onward T003: graph-focus wiring, the disabled steering input, and the
   additive envelope field DECISION F021 D2 permits.

## Risks
- T002's rules land in pure `.ts` modules under the node vitest D4 keeps, and
  its `.tsx` components are gated by a Python source contract under
  `tests/ui_contracts/`. A rule that reaches for the DOM is a sign it was put in
  the wrong half.
- The event ring D5 rules is the first state the brain-stream runner retains per
  event rather than in aggregate, so the view-identity contract that runner
  documents is the thing most likely to break under it.
- Jump-to-node needs the additive envelope field DECISION F021 D2 permits. That
  is the one production seam this feature opens, and it stays one field.
- T001 is built and verified but its catalog covers only what a static walk can
  see. The generic line carries the eleven runtime-computed emitters, and R-0649
  records that the walk's roots also reach vendored third-party Python.
- The open set holds no code defect of F021; R-0403, R-0607, R-0608, R-0609,
  R-0611 and R-0613 stay routed to a paydown branch.
