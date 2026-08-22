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
kind set DECISION F021 D1 rules and an unknown kind renders an honest generic
line rather than vanishing, the feed renders fixture streams per the binding CSS,
jump-to-node focuses the right node, and the steering input renders DISABLED with
its honest tooltip until F030 lands.

## Current Step
R4 records the R3 verdict and closes the reviewer's session at its stated round
cap, leaving the verdict on disk and a handoff that names the next session's
first action. It builds nothing. The branch is mid-feature and carries no pull
request by design.

## Next Steps
1. R5 builds T001 headless-first: the humanize catalog module, the coverage test
   DECISION F021 D1 rules, the honest generic line for an unrecognised kind, and
   goldens. `.agent/f021_inventory.md` at `4a7b5cbf` is the measured ground.
2. R6 rules the two remaining infrastructure DECISIONS before T002 needs them —
   the frontend test environment, which today collects no component test, and
   the single-subscription fan-out.
3. R7 onward T002 then T003, in the feature file's Task slicing order.

## Risks
- T002 cannot be tested until the frontend test environment changes: measured at
  `4a7b5cbf`, `apps/ui/vitest.config.ts` sets `environment: "node"` and
  `include: ["src/**/*.test.ts"]`, so no `.test.tsx` is collected at all. R6
  rules it; R5 does not need it because T001 is a pure module.
- Jump-to-node needs the additive envelope field DECISION F021 D2 permits. That
  is the one production seam this feature opens, and it stays one field.
- The open set carried into this record at R1 holds no code defect of F021;
  R-0403, R-0607, R-0608, R-0609, R-0611 and R-0613 stay routed to a paydown
  branch.
