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
R6 builds T001: the humanize module with its honest generic line, the catalog
data whose key set the contract test pins to the Python emitters, the vitest
behaviour tests, and that contract test. It also records the R5 verdict and
promotes the rule R-0449 and R-0494 carry into the §3 pre-emission checklist.

## Next Steps
1. R7 rules the frontend test environment, which today collects no component
   test at all, and the single-subscription fan-out — both are infrastructure
   DECISIONS T002 needs before it can be written.
2. R8 builds T002: the feed, its rows and the NowCard over fixture streams, with
   the scroll discipline that never yanks a reader who has scrolled up.
3. R9 onward T003: graph-focus wiring, the disabled steering input, and the
   additive envelope field DECISION F021 D2 permits.

## Risks
- T002 cannot be tested until the frontend test environment changes: measured at
  `82fcc7c0`, `apps/ui/vitest.config.ts` sets `environment: "node"` and
  `include: ["src/**/*.test.ts"]`, so no `.test.tsx` is collected at all. R7
  rules it.
- The catalog cannot cover the kinds whose names are computed at runtime; G5
  measures eleven such writers. The generic line is the whole of their coverage,
  which is why T001 ships its test rather than treating it as a nicety.
- Jump-to-node needs the additive envelope field DECISION F021 D2 permits. That
  is the one production seam this feature opens, and it stays one field.
- The open set holds no code defect of F021; R-0403, R-0607, R-0608, R-0609,
  R-0611 and R-0613 stay routed to a paydown branch.
