# Plan — Steps 4917-4926: Job Evidence Nested Path Containment Closure v1

## Goal
Close nested task evidence path traversal vulnerability in job evidence export.

## Current Step
All steps complete. Awaiting 5-minute quiet window.

## Steps
- Step 4917: Add safe task evidence path helper (_task_evidence_dir)
- Step 4918: Use helper for all nested task evidence writes
- Step 4919: Unavailable task traversal regression test
- Step 4920: Run_id task traversal regression test
- Step 4921: File mapping containment tests
- Step 4922: Strengthen output path traversal tests
- Step 4923: Preserve redaction and evidence behavior
- Step 4924: Preserve existing job and safety flows
- Step 4925: Architecture guard for nested path containment
- Step 4926: Final handoff
