# Plan — F157 Capability matrix & honest degradation

## Goal
A declarative register maps every capability-consuming feature to the capabilities it requires
and to one registered degradation; one central `require_or_degrade` call sits at each usage site;
the run's `capability_decisions.jsonl` evidence, a report section and a command-line line show
when a degradation ran; a guard fails a capability read outside the matrix
(`docs/roadmap/features/T8_F157.md`).

## Current Step
Round 8, the closure's integration-gate round: book round 7 and R-1454's resolution, the
checklist's consolidation pass, the self-use item run to its approval gate, and the one full suite.

## Next Steps
1. The evidence bundle and the review package (closure algorithm steps 1 and 2).
2. The closing round: the Built State, the ledger rotation, the STATUS line, the README and the
   pull request.

## Risks
- A red full suite or a self-use run defect turns the next round into a repair round first.
