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
R1 is the claim round. It creates the branch, resets the review record carrying
the F009 open set forward, gates F009 R34, registers the one closure candidate
F009 carried, empties the candidates file and claims F021 in the roadmap ledger.
It builds nothing.

## Next Steps
1. R2 the inventory, MEASURED in the source rather than read off the feature
   file: which module owns the F008 SSE subscription and how the client store
   fans it out, where the Part E event-kind list is defined, and what the graph
   already exposes as a focus API.
2. R3 record R2 and rule the feed's shape as a DECISION: the humanize catalog's
   module and its coverage-test contract, the ACTION-class subset the NowCard
   reads, and the disabled-steering flag.
3. R4 onward the built work, in the T001 then T002 then T003 order the feature
   file's Task slicing names.

## Risks
- F021 is a UI feature, so docs/ui/design_reference/ is binding for every visual
  surface and assets_spec.md is the asset authority; any visual deviation needs
  an assumption_log entry with a technical reason.
- One SSE subscription with client-side fan-out is an architecture line from the
  feature file's Orchestrator brief: a second EventSource is rejected.
- The open set carried into the review record at C3 holds no code defect of
  F021; R-0403, R-0607, R-0608, R-0609, R-0611 and R-0613 stay routed to a
  paydown branch.
