# Plan — F060 Long-run certificate

## Goal
A finished job can prove itself to someone who was not there: `remedy job certificate <id>` packs
its report, token truth, verdicts, ownership, run manifest and a hash manifest with claims into one
small bundle, and `remedy verify <bundle>` checks every member and every claim on any machine, with
the failing member named (docs/roadmap/features/T3_F060.md; DECISIONs F060 D1 to D4).

## Current Step
Round 6 (session 1), the closure's evidence round (`docs/roadmap/STATUS_closure_protocol.md` steps
1 and 2): book round 5 and resolve R-1406, commit the evidence script, run the staging reclaim, the
evidence job `f060r6e1001` and the review package.

## Next Steps
1. The closing round: the Built State's closure facts, the rotation or its recorded skip, SU-071's
   `consumed_by`, the STATUS flip with the README sync, and the pull request, left unmerged.

## Risks
- The integrity check fails on High findings F060 does not own (DECISION F310 D7, Q20).
