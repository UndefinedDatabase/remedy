# Plan — operator amendment amend1027b-v1

## Goal
Remedy closes as version 1 (2026-10-27): three truth defects fixed (A1 scope.match, A2 what
one_job counts, A3 the 16-character order id of a job made elsewhere), the feature loop stops
(Package 3 "Nach v1"), and improvements come only from reports and failed runs.

## Current Step
Done. A1 and A2 (dc69345ff), A3 (758077b7c), B2 (bafb89737), B1 and B4 (2bdeb922c), repairs of
the full runs (24701fb03, f2d26d40a); B3 in ~/Repos/system (9d85dff). Full suite green on
f2d26d40a (24433 passed, 11 skipped). Closing: merge, push, supervisor restart, handback
`~/.remedy-loop/amend1027b-v1.handback.md`.

## Next Steps
1. None by Rule A5: Package 1 has no open line (F319 was its last; F316 waits in Package 3). The next work is an order to the project remedy
   from a report over Universe or a failed run (docs/roadmap/V1.md).

## Risks
- The installed metadata of the editable install still says 0.1.0 until it is reinstalled;
  pyproject declares 1.0.0.
