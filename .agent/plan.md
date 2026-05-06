# Plan

## Goal
Step 23: Project Brain Graph v1 — read-only graph model and export for future visual cockpit.

## Prior step
Step 22.1: Agent Loop stale blocker fix + redaction hardening.

## Status
COMPLETE — 1111 tests pass.

## Steps
1. [x] Create packages/orchestration/project_brain.py
   - BrainNode, BrainEdge, ProjectBrainGraph frozen dataclasses
   - Node types: job, task, artifact, patch_intent, approval_decision, verification,
     permission_blocker, run_event, agent_loop, constitution, memory_placeholder, mcp_placeholder
   - Edge types: has_task, created_artifact, emitted_event, produced_patch_intent,
     decided_by, verified_by, blocked_by, inspected_by, governed_by,
     future_memory_layer, future_mcp_layer
   - build_project_brain, summarize_project_brain, export_project_brain_json
   - Redaction policy enforced
   - memory_placeholder + mcp_placeholder always present
   - Nodes sorted by type-priority then id; edges by source/target/type
2. [x] Add `remedy brain <job_id>` CLI command to apps/cli/main.py
   - Emits project_brain_inspected with exact schema:
     {node_count, edge_count, task_count, patch_intent_count}
3. [x] Create tests/test_project_brain.py (60 tests)
   - TestBrainNodeEdge, TestBuildProjectBrain, TestSummarizeProjectBrain,
     TestExportProjectBrainJson, TestRedactionHardening, TestCLIBrain
   - 5 redaction sentinels
4. [x] Update docs/architecture.md — Project Brain Graph v1 section
5. [x] Update .agent files
6. [x] Run full suite (1111 pass)
7. [ ] Commit Step 23 changes
8. [ ] Push to feature/step21-project-constitution-v1

## Branch
feature/step21-project-constitution-v1
