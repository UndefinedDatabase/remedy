# Context

## Active Branch
feature/step21-project-constitution-v1

## PR
(open — see GitHub)

## Scope
Step 21 + 21.1 + 21.2: Project Constitution v1.
Step 22 + 22.1: External Agent Loop Contract v1.
Step 23 + 23.1: Project Brain Graph v1 + polish.
Step 24: Brain Node Detail v1.

New files:
- packages/orchestration/project_constitution.py
- packages/orchestration/agent_loop.py
- packages/orchestration/project_brain.py
- packages/orchestration/brain_detail.py
- tests/test_project_constitution.py (81 tests)
- tests/test_agent_loop.py (68 tests)
- tests/test_project_brain.py (80 tests)
- tests/test_brain_detail.py (52 tests)

Modified:
- apps/cli/main.py: constitution, agent-loop, brain (--json), brain-node (--json) commands
- packages/orchestration/cockpit.py, trust_report.py, timeline.py
- docs/architecture.md

## Key facts (Brain Node Detail — Step 24)
- BrainNodeDetail frozen=True: 13 fields including why_it_exists, connected_to, evidence,
  affected_files, next_actions, redaction_notes
- Raises ValueError (safe, truncated message) if node_id not found
- connected_to: {direction, edge_type, node_id, node_type, node_label} per edge
- Redaction: no content, diff preview, approval_reason, event.message, command output
- User prompt truncated to 120 chars for job node
- brain_node_inspected schema: {node_id, node_type, connected_count, evidence_count}
- 1183 tests pass

## Key facts (Project Brain — Steps 23/23.1)
- Read-only graph: BrainNode, BrainEdge, ProjectBrainGraph frozen dataclasses
- 12 node types, 11 edge types
- Visual legend: pending=grey, running=pulsing, completed=white,
  blocked=red, needs approval=amber, memory layer=violet, mcp quarantine=orange
- project_constitution_loaded → constitution node ONLY (not also run_event)
- _safe_int for agent_loop cycle parsing
- project_brain_inspected schema: {node_count, edge_count, task_count, patch_intent_count}

## Key facts (Agent Loop — Step 22.1)
- derive_agent_loop_state reflects CURRENT state, not worst historical event
- blocked_reason format: "permission_denied:workspace_write"
- agent_loop_inspected schema: {stage, decision, cycle, max_cycles, pending_finding_count}
