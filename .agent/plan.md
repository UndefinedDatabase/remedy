# Plan — F296 Evidence-triggered tier escalation (routing v2)

## Goal
A task that fails on a cheaper tier gets its next repair round on the next tier up, for reasons
the evidence names and never for provider unavailability, recorded in evidence, report, events and
ledger, off by default (docs/roadmap/features/T3_F296.md; DECISIONs F296 D1 to D5).

## Current Step
Round 6 (session 1): the closure's evidence round — book round 5 and register R-1421 (the suite's
CPU cost, owned by F314), the staging reclaim, the evidence job and the review package.

## Next Steps
1. The closing round: the Built State, the rotation, the STATUS line with the README sync and
   SU-074's consumed_by, and the pull request, left unmerged.

## Risks
- A package that builds BLOCKED_EVIDENCE is a closure blocker; its validator errors name the fix.
