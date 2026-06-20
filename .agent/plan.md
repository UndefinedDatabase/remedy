# Plan

## Goal
Steps 3146-3215: Job-Centric Core Finalization v0

## Completed
- PR #97 merged, main synced, branch created
- CLI help audit: job already has 16 commands, mission has run/report
- Added job.status and job.report facades (read-only, safe JSON, no .agent dep)
- Updated Happy Path to job-first (do → status → report → UI → review)
- Updated mission group description to "Advanced/internal"
- Updated command catalog with job.status + job.report entries
- Updated all docs: spine, quickstart, approval, boundary to job-first
- 18 new tests: catalog, happy path, taxonomy docs, no-agent, invalid-id safety
- Fixed test_command_catalog and test_cli_execution_loop_closure assertions
- Fast 557, runtime 57, full 7047 (2 pre-existing failures), lint clean

## Current Step
Commit, push, create PR, write handoff.
