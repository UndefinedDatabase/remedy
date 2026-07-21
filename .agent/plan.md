# Plan — F017 Scope Fences — Final Cleanup & Review Preparation

## Goal
Close 4 contracts: split unrelated roadmap commit, complete
diagnostic redaction, add real production E2E, make docs truthful.
One clean F017 branch + one canonical READY_FOR_REVIEW ZIP.

## Scope 1 — clean branch reconstruction
- backup branch at mixed HEAD
- roadmap branch from base with 0b71df6
- clean F017 branch: all commits except 0b71df6
- verify no T14/T15/T16/T17 feature files changed
- record old-to-new commit mapping

## Scope 2 — general POSIX diagnostic redaction
- _POSIX_ABS_RE: match ANY absolute path, not just known roots
- 20+ table-driven sanitizer tests
- commit on clean branch

## Scope 3 — real production E2E
- test_fence_production_e2e.py
- run_job_fulfill: per-job/config/env deny → staging discarded
- run_do_continue: denied intent → FENCE_VIOLATION stop
- CLI _cmd_job_fences: human/JSON/rules/builtin/error paths
- commit on clean branch

## Scope 4 — docs consistency + Evidence + package
- fix 12 failing F017 assertions (accept [~])
- update agent state files
- update T0_F017.md
- run all required validation suites
- fresh Evidence via create_manual_completion_bundle
- canonical ZIP via make_review_zip.sh
- no post-ZIP commit

## Current Step
Scope 1: creating backup and clean branches.

## Constraints
No Fable/subagents/providers/network/Docker.
Do not amend/squash. Do not push/PR/merge/modify main.
F017 [~]. F018 [ ].
