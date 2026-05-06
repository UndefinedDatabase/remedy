# Context

## Active Branch
feature/step21-project-constitution-v1

## PR
(open — see GitHub)

## Scope
Step 21 + 21.1 + 21.2: Project Constitution v1 (extraction, integration, hygiene).
Step 22: External Agent Loop Contract v1 (orchestration contract).
Step 22.1: Agent Loop stale blocker fix + redaction hardening.
Step 23: Project Brain Graph v1 (read-only graph model/export).
Step 23.1: Project Brain polish (visual legend, constitution dedupe, safe cycle, --json).

New files:
- packages/orchestration/project_constitution.py
- packages/orchestration/agent_loop.py
- packages/orchestration/project_brain.py
- tests/test_project_constitution.py (81 tests)
- tests/test_agent_loop.py (68 tests)
- tests/test_project_brain.py (80 tests)

Modified:
- apps/cli/main.py: constitution, agent-loop, brain (+ --json) commands
- packages/orchestration/cockpit.py, trust_report.py, timeline.py
- docs/architecture.md

## Key facts (Project Brain — Steps 23/23.1)
- Read-only graph: BrainNode, BrainEdge, ProjectBrainGraph (all frozen=True dataclasses)
- Node types (12): job, task, artifact, patch_intent, approval_decision, verification,
  permission_blocker, run_event, agent_loop, constitution, memory_placeholder, mcp_placeholder
- Edge types (11): has_task, created_artifact, emitted_event, produced_patch_intent,
  decided_by, verified_by, blocked_by, inspected_by, governed_by,
  future_memory_layer, future_mcp_layer
- memory_placeholder + mcp_placeholder ALWAYS present (status=informational)
- Nodes sorted by (_NODE_TYPE_ORDER, id); edges by (source, target, type)
- project_constitution_loaded → constitution node ONLY, NOT also a run_event node
- _safe_int: "2"→2, "not-a-number"→0, None→0, missing→0 (no exception escapes)
- Visual legend in summary: pending=grey, running=pulsing, completed=white,
  blocked=red, needs approval=amber, memory layer=violet, mcp quarantine=orange
- remedy brain <job_id> --json → export_project_brain_json with sort_keys=True
- project_brain_inspected metadata schema: {node_count, edge_count, task_count, patch_intent_count}
- Redaction applies to both text and --json output
- 1131 tests pass

## Key facts (Agent Loop — Step 22.1)
- derive_agent_loop_state reflects CURRENT state, not worst historical event
- Stale perm_denied events (task later completed or no longer pending) do NOT block
- blocked_reason format: "permission_denied:workspace_write"
- agent_loop_inspected metadata schema: {stage, decision, cycle, max_cycles, pending_finding_count}
