# Plan — Steps 4869-4878: Job Runner Continuation Config Truth Closure v4

## Goal
Fix two continuation-config bugs:
1. max_rounds not restored on paused continuation
2. Explicit --builder fake / --reviewer fake ignored after persisted non-fake

Root cause: CLI handler collapses omitted options to default values, making
omitted indistinguishable from explicitly-set-to-default.

## Current Step
Implementing Steps 4869-4878.

## Steps
- Step 4869: Omitted-vs-explicit handling (None flow for CLI args)
- Step 4870: Restore persisted max_rounds on continuation
- Step 4871: Allow explicit provider override back to fake
- Step 4872: Preserve and override test command correctly
- Step 4873: Preserve and override write mode correctly
- Step 4874: Execution config source/audit fields
- Step 4875: Real command-path pause/continue tests
- Step 4876: Explicit override tests
- Step 4877: Preserve completion gate and job safety
- Step 4878: Architecture guard and handoff
