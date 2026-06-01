# Plan — Steps 289-296

## Goal
Test suite re-architecture, source apply transactionality, dashboard truth, frontend fixes, truncation metadata, and final baseline.

## Current Step
All steps complete. Ready for commit + push.

## Steps
- [x] Step 289: Test taxonomy, migration map, domain directory structure
- [x] Step 290: Migrate ~1088 tests from 25 step files into 19 domain-oriented suites + guard test
- [x] Step 291: Source apply transactionality + unified diff hunk validation
- [x] Step 292: Taskfile command body risk inspection (parity with Makefile/package.json)
- [x] Step 293: Dashboard truth v3 — scoped test_status, event-backed actor, real graph data, runnable command
- [x] Step 294: Frontend degraded state visibility (DegradedBanner) + CommandBar copies command
- [x] Step 295: Truncation metadata survives CLI event log, job metadata, trust report
- [x] Step 296: Full baseline 3677 passed, 1 skipped, 0 failed. Guardrails green.
