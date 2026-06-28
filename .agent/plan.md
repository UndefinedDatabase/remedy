# Plan — Steps 5053-5072: Agent Run Trace + Job-Flow Cockpit Bridge v1

## Goal
Make Remedy able to prove, inspect, and visualize its own Builder/Reviewer/
Repair/Final-Audit loop from real evidence. Close 6 verified gaps.

## Current Step
All 6 deliverables complete. Reviewer findings R-4201, R-4202, R-4203 fixed.

## Reviewer Fixes Applied
- R-4201: Narrowed `except Exception` in `_load_job()` to specific types
- R-4202: Return 400 for malformed IDs, 404 for valid-but-missing UUIDs
- R-4203: Fixed 12 lint errors (unused imports, import ordering)
