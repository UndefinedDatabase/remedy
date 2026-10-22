# Plan — F296 Evidence-triggered tier escalation (routing v2)

## Goal
A task that fails on a cheaper tier gets its next repair round on the next tier up, for reasons
the evidence names and never for provider unavailability, recorded in evidence, report, events and
ledger, off by default (docs/roadmap/features/T3_F296.md; DECISIONs F296 D1 to D5).

## Current Step
Round 5 (session 1): the closure's integration-gate round — book round 4, T003's Amendment (the
default stays off, DECISION F296 D5), the checklist's consolidation pass, the closure's self-use
item run to its approval gate, and the feature's one full suite.

## Next Steps
1. The evidence bundle and the review package (or a repair round naming every bad node id).
2. The closing round: the Built State, the rotation, the STATUS line, the README and the pull
   request.

## Risks
- The self-use run makes real provider calls through the `self_use` role, at most its budget.
- The full suite is the feature's one run; a red node is this feature's to repair
  (amend0917-throughput rule 2).
