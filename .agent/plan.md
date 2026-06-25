# Plan — Steps 4857-4868: Job Runner Completion Gate + Continuation Config Closure v3

## Goal
Fix completion gate (don't trust final_status alone) and persist execution config across paused continuation.

## Current Step
Implementing all steps.

## Steps
- Step 4857: Deterministic job task completion gate (validate_job_task_result)
- Step 4858: Corrupted-result completion gate tests
- Step 4859: Durable job execution config model
- Step 4860: Preserve config across paused continuation
- Step 4861: Make next_command safe for paused jobs
- Step 4862: Real CLI pause/continue config tests
- Step 4863: Explicit config override tests
- Step 4864: Job report execution-config section
- Step 4865: Preserve token-bounded job context
- Step 4866: Preserve job workspace and target safety
- Step 4867: Real CLI smoke command-path proof
- Step 4868: Architecture guard and handoff
