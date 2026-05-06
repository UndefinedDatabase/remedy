# Plan

## Goal
Step 24: Brain Node Detail v1 — read-only explanation/detail layer for individual Project Brain nodes.

## Prior step
Step 23.1: Project Brain polish (visual legend, constitution dedupe, safe cycle, --json).

## Status
COMPLETE — 1183 tests pass.

## Steps
1. [x] Create packages/orchestration/brain_detail.py
   - BrainNodeDetail frozen=True dataclass (13 fields)
   - build_brain_node_detail(job, graph, node_id, events) -> BrainNodeDetail
     - Raises ValueError (safe message) if node_id not found
     - Handles all 12 node types: job, task, artifact, patch_intent,
       approval_decision, verification, permission_blocker, run_event,
       agent_loop, constitution, memory_placeholder, mcp_placeholder
     - Connections: incoming + outgoing edges with neighbour info
     - Affected files: repo_applied_files for artifact/task; target_path for patch_intent
     - Full redaction: no content, diff preview, approval_reason, event.message, command output
   - summarize_brain_node_detail(detail) -> str
   - export_brain_node_detail_json(detail) -> dict
2. [x] Add remedy brain-node <job_id> <node_id> [--json] CLI command
   - brain_node_inspected run-log event with exact schema:
     {node_id, node_type, connected_count, evidence_count}
   - unknown node exits 1 with safe message
3. [x] Create tests/test_brain_detail.py (52 tests)
   - All 12 node types tested
   - Connection directions tested
   - 5 redaction sentinels
   - CLI happy path, --json, error exits, run-log schema
4. [x] Update docs/architecture.md — Brain Node Detail v1 section
5. [x] Update .agent files
6. [x] Run full suite (1183 pass)
7. [ ] Commit Step 24 changes
8. [ ] Push to feature/step21-project-constitution-v1

## Branch
feature/step21-project-constitution-v1
