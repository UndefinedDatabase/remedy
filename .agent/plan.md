# Plan — F296 Evidence-triggered tier escalation (routing v2)

## Goal
A task that fails on a cheaper tier gets its next repair round on the next tier up, for reasons
the evidence names and never for provider unavailability, recorded in evidence, report, events and
ledger, off by default (docs/roadmap/features/T3_F296.md; DECISIONs F296 D1 to D5).

## Current Step
Round 7 (session 1): the closing round — book round 6, the Built State, the ledger rotation, F296
accepted in STATUS with the README sync and SU-074's consumed_by, and the pull request, left
unmerged.

## Next Steps
1. The next session: Phase 1 rule 1, then the Open PR Gate merges F296's pull request, then the
   next feature's first commit books round 7's verdict, then Rule A5.

## Risks
- R-1421, the closure suite's CPU cost, is open and owned by F314.
