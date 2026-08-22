# Plan — F021 Live activity feed + now-card

Branch: feature/f021-live-activity-feed, cut from `main` at `4548995d`, the merge
commit of pull request #210, which the reviewer merged at the Open PR Gate before
this branch was created. `.agent/live_review.md` is the source of truth for the
open set, the round map and the finding-id ceiling.

## Goal
The raw SSE event stream becomes a story a human can follow: a humanization
catalog maps every Part E event kind to a plain line, a NowCard shows the newest
ACTION-class event with a recency-driven activity dot, and feed rows carry their
seq and click-jump to their node in the graph. DONE when the catalog covers every
Part E kind and an unknown kind renders an honest generic line rather than
vanishing, the feed renders fixture streams per the binding CSS, jump-to-node
focuses the right node, and the steering input renders DISABLED with its honest
tooltip until F030 lands.

## Current Step
R2 records the R1 verdict and then MEASURES the ground this feature builds on,
writing what it measured to `.agent/f021_inventory.md`: the F008 subscription and
whether a second consumer can attach without a second connection, the event
envelope, where the event kinds are defined, what the graph exposes for focusing
a node, and how the frontend tests are written and run. It builds nothing.

## Next Steps
1. R3 record R2 and rule the feed's shape as a DECISION on the measured ground:
   the humanize catalog's module and its coverage-test contract, the ACTION-class
   subset the NowCard reads, and the disabled-steering flag.
2. R4 onward the built work, in the T001 then T002 then T003 order the feature
   file's Task slicing names, starting with the catalog and its coverage test
   because the feature file's Orchestrator brief calls T001 headless-first.

## Risks
- The inventory may find NO single authoritative list of event kinds. T001's
  coverage test is specified against that list, so its absence is a design
  question for R3 rather than something a builder should improvise.
- F021 is a UI feature, so docs/ui/design_reference/ is binding for every visual
  surface and assets_spec.md is the asset authority; any visual deviation needs
  an assumption_log entry with a technical reason.
- One SSE subscription with client-side fan-out is an architecture line from the
  feature file's Orchestrator brief: a second EventSource is rejected.
- The open set carried into this record at R1 holds no code defect of F021;
  R-0403, R-0607, R-0608, R-0609, R-0611 and R-0613 stay routed to a paydown
  branch.
