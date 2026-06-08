# Plan — Steps 940-959: Test Failure Artifact v1 + Repair Loop v0

## Goal
When a test fails, Remedy creates a safe structured failure artifact and fix task.
First "Remedy keeps working" moment. No raw output in UI/CLI/events.

## Current Step
959 — Final handoff

## Steps
- [x] 940: Handoff setup
- [x] 941: TestFailureArtifact model
- [x] 942: Build failure artifact from test result
- [x] 943: Persist failure artifact in Job
- [x] 944: Failure events
- [x] 945: Fix task creation
- [x] 946: Repair loop v0 orchestrator
- [x] 947: CLI: repair start
- [x] 948: CLI: failure show
- [x] 949: Integrate with remedy do result (failure_summary field)
- [x] 950-951: Redaction + linking tests (40 tests)
- [x] 952: Repair loop tests (9 tests)
- [x] 953: Runtime CLI tests (6 tests)
- [x] 954-955: Proof chain + context inspector awareness (structural)
- [x] 956: Docs (docs/repair-loop-v0.md)
- [x] 957-959: Targeted tests + review + final handoff

## Pre-existing Issue
`test_project_brain.py::TestFileProvenanceChain::test_full_chain_order` fails on main.
