# Plan

## Goal
Step 7.6: Verification Diagnostic Artifact Fix.

## Status
COMPLETE

## Steps
1. [x] finalize_task: capture current artifact ID before clearing output_artifact_ids;
       annotate by ID not task_id scan
2. [x] Tests: two consecutive failures; second failure metadata on second artifact
3. [x] decisions.md + commit + push

## Key Decisions
- capture output_artifact_ids[0] before clear(); use that ID for annotation lookup
- single-line ordering fix; no structural change
- failed artifacts accumulate in job.artifacts; each is annotated with its own failure metadata

## Branch
feature/step6-workspace-runtime (PR #7) — in-scope per PR Continuity Rule
