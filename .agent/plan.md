# Plan — operator amendment amend1027b-v1

## Goal
Remedy closes as version 1 (2026-10-27): three truth defects fixed (A1 scope.match, A2 what
one_job counts, A3 the 16-character order id of a job made elsewhere), the feature loop stops
(Package 3 "Nach v1"), and improvements come only from reports and failed runs.

## Current Step
A1 and A2 done (dc69345ff). A3: every job names its 16-character order id; the order routes
resolve a batch prefix (`resolve_order_record`); docs and CHANGELOG at 1.32.

## Next Steps
1. B2: STATUS.md V1 line, Package 3, Rule A5 reads Package 1 only (roadmap_index, protocol).
2. B1 V1.md, B4 README and CHANGELOG 1.0.0, B3 the loop helpers in ~/Repos/system.
3. Full suite, review loop, ruff, merge, push, supervisor restart, handback.

## Risks
- The client answers are recorded (client-answers-v1): a changed answer is re-recorded.
