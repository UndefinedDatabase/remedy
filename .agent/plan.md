# Plan — F141 Permission matrix per autonomy level

## Goal
What running work may DO becomes one enforced table: eight actions by F078's levels `L2` to `L5`,
answered by one check in `packages/orchestration/permission_matrix.py` that every seam calls, with
a test per cell, answers that cite their cell, audited approvals of an instance, a table rendered
from the constant, and no bypass parameter (docs/roadmap/features/T7_F141.md; DECISIONs F141 D1
to D8).

## Current Step
Round 11 (session 2), the closing round (`docs/roadmap/STATUS_closure_protocol.md` steps 4 and 5):
book round 10, the Built State brought current, no rotation (DECISION F141 D8), F141 accepted in
STATUS with the README sync and `SU-070`'s `consumed_by`, and the pull request, left unmerged.

## Next Steps
1. The next session: Phase 1 rule 1 (`.agent/STOP`), then the Open PR Gate merges F141's pull
   request; Rule A5 proposes the next feature.

## Risks
- The integrity check fails on High findings F141 does not own (DECISION F310 D7, Q20).
- R-1403 is owned by F307 and stays open at F141's closure.
