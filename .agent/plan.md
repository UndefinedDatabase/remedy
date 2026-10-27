# Plan — operator amendment amend1027b-v1

## Goal
Remedy closes as version 1 (2026-10-27): three truth defects fixed (A1 scope.match, A2 what
one_job counts, A3 the 16-character order id of a job made elsewhere), the feature loop stops
(Package 3 "Nach v1"), and improvements come only from reports and failed runs.

## Current Step
A1, A2 (dc69345ff) and A3 (758077b7c) done. B2: STATUS.md reads "V1 — abgeschlossen am
2026-10-27" after F319; Package 1's 20 open lines moved to Package 3; Rule A5 reads Package 1 only
(bafb89737). B3 is committed in ~/Repos/system (9d85dff). B1 and B4: V1.md, README, CHANGELOG
1.0.0, pyproject 1.0.0.

## Next Steps
1. Full suite run 2 after the review repairs of run 1 (6 red: release matrix 1.32, contract test,
   context.md, an advertised-command comment); then merge, push, supervisor restart, handback.

## Risks
- The client answers are recorded (client-answers-v1): a changed answer is re-recorded.
