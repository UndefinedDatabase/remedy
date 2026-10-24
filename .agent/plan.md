# Plan — F157 Capability matrix & honest degradation

## Goal
A declarative register maps every capability-consuming feature to the capabilities it requires
and to one registered degradation; one central `require_or_degrade` call sits at each usage site;
the run's `capability_decisions.jsonl` evidence, a report section and a command-line line show
when a degradation ran; a guard fails a capability read outside the matrix
(`docs/roadmap/features/T8_F157.md`).

## Current Step
Round 10, the closure's evidence round: book round 9, the staging reclaim, the evidence job
`f157r10e1001` and the review package.

## Next Steps
1. The closing round: the Built State, the ledger rotation, SU-081's `consumed_by`, the STATUS
   line with the README sync, and the pull request, left unmerged.

## Risks
- A package that does not read `READY_FOR_REVIEW` blocks the closure until it is repaired.
