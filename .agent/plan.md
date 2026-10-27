# Plan — operator amendment amend1027b-v1

## Goal
Remedy closes as version 1 (2026-10-27): three truth defects fixed (A1 scope.match, A2 what
one_job counts, A3 the 16-character order id of a job made elsewhere), the feature loop stops
(Package 3 "Nach v1"), and improvements come only from reports and failed runs.

## Current Step
A1, A2 (dc69345ff) and A3 (758077b7c) done. B2: STATUS.md reads "V1 — abgeschlossen am
2026-10-27" after F319; Package 1's 20 open lines moved to Package 3; Rule A5 reads Package 1 only.
B3 is committed in ~/Repos/system (9d85dff).

## Next Steps
1. B1 V1.md, B4 README, CHANGELOG 1.0.0 and pyproject 1.0.0.
2. Full suite, review loop, ruff, merge, push, supervisor restart, handback.

## Risks
- The client answers are recorded (client-answers-v1): a changed answer is re-recorded.
