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
R5 records the R4 verdict, adds new evidence to the open finding R-0419, and
rules DECISION F021 D3, which corrects the seed DECISION F021 D1 chose for
T001's coverage constant. It edits no production file: T001 is built at R6, on
ground this round makes correct.

## Next Steps
1. R6 builds T001 headless-first: `apps/ui/src/api/humanize.ts` with the catalog
   and its honest generic line, the vitest generic-path test, and the
   `tests/ui_contracts/` derivation test DECISION F021 D3 rules.
2. R7 rules the frontend test environment, which today collects no component
   test, and the single-subscription fan-out, before T002 needs them.
3. R8 onward T002 then T003, in the feature file's Task slicing order.

## Risks
- The vocabulary DECISION F021 D3 rules is 83 kinds wide. If a catalog entry per
  kind pushes T001 past the 500-insertion commit cap, R6 splits it by source —
  the run-log half and the JobPlan-trace half — in two commits of one round.
- T002 cannot be tested until the frontend test environment changes: measured at
  `4a7b5cbf`, `apps/ui/vitest.config.ts` sets `environment: "node"` and
  `include: ["src/**/*.test.ts"]`, so no `.test.tsx` is collected at all.
- Jump-to-node needs the additive envelope field DECISION F021 D2 permits. That
  is the one production seam this feature opens, and it stays one field.
- The open set holds no code defect of F021; R-0403, R-0607, R-0608, R-0609,
  R-0611 and R-0613 stay routed to a paydown branch.
