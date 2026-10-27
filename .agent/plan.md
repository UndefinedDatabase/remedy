# Plan — operator amendment amend1027b-v1

## Goal
Remedy closes as version 1 (2026-10-27): three truth defects fixed (A1 scope.match, A2 what
one_job counts, A3 the 16-character order id of a job made elsewhere), the feature loop stops
(Package 3 "Nach v1"), and improvements come only from reports and failed runs.

## Current Step
A1: `scope.match` and the final review's `changed_files_match` are null when nothing can be
compared; the story says "nicht ermittelt". Two fake-builder runs as tests.

## Next Steps
1. A2: the story's `scope.tasks` and `scope.tasks_text` ("Ein Job mit zwei Aufgaben: der Code
   und sein Test.").
2. A3: `order_id` per job is the 16-character order id; the order routes resolve a batch prefix;
   interface 1.32, docs, CHANGELOG.
3. B2: STATUS.md V1 line, Package 3, Rule A5 reads Package 1 only (roadmap_index, protocol).
4. B1 V1.md, B4 README and CHANGELOG 1.0.0, B3 the loop helpers in ~/Repos/system.
5. Full suite, review loop, ruff, merge, push, supervisor restart, handback.

## Risks
- The client answers are recorded (client-answers-v1): a changed answer is re-recorded.
