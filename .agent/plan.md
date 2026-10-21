# Plan — F060 Long-run certificate

## Goal
A finished job can prove itself to someone who was not there: `remedy job certificate <id>` packs
its report, token truth, verdicts, ownership, run manifest and a hash manifest with claims into one
small bundle, and `remedy verify <bundle>` checks every member and every claim on any machine, with
the failing member named (docs/roadmap/features/T3_F060.md; DECISIONs F060 D1 to D5).

## Current Step
Round 7 (session 1), the closing round (`docs/roadmap/STATUS_closure_protocol.md` steps 4 and 5):
book round 6, the Built State's closure facts, no rotation (DECISION F060 D5), F060 accepted in
STATUS with the README sync and `SU-071`'s `consumed_by`, and the pull request, left unmerged.

## Next Steps
1. The next session: Phase 1 rule 1 (`.agent/STOP`), then the Open PR Gate merges F060's pull
   request; Rule A5 proposes the next feature.

## Risks
- The integrity check fails on High findings F060 does not own (DECISION F310 D7, Q20).
