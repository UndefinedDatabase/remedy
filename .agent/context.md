# Context

## Active Branch
feature/step21-project-constitution-v1

## PR
(open — see GitHub)

## Scope
Step 21 + 21.1 + 21.2: Project Constitution v1 (extraction, integration, hygiene).
Step 22: External Agent Loop Contract v1 (orchestration contract).
Step 22.1: Agent Loop stale blocker fix + run-log/redaction hardening.
Step 23: Project Brain Graph v1 (read-only graph model/export).

New files:
- packages/orchestration/project_constitution.py
- packages/orchestration/agent_loop.py
- packages/orchestration/project_brain.py
- tests/test_project_constitution.py (81 tests)
- tests/test_agent_loop.py (68 tests)
- tests/test_project_brain.py (60 tests)

Modified:
- apps/cli/main.py: constitution, agent-loop, brain commands
- packages/orchestration/cockpit.py, trust_report.py, timeline.py
- docs/architecture.md

## Key facts (Project Brain — Step 23)
- Read-only graph: BrainNode, BrainEdge, ProjectBrainGraph (all frozen=True dataclasses)
- Node types (12): job, task, artifact, patch_intent, approval_decision, verification,
  permission_blocker, run_event, agent_loop, constitution, memory_placeholder, mcp_placeholder
- Edge types (11): has_task, created_artifact, emitted_event, produced_patch_intent,
  decided_by, verified_by, blocked_by, inspected_by, governed_by,
  future_memory_layer, future_mcp_layer
- memory_placeholder + mcp_placeholder ALWAYS present (status=informational)
- Nodes sorted by (_NODE_TYPE_ORDER, id); edges by (source, target, type)
- Redaction: no artifact.content, diff preview, approval_reason, event.message, command output
- project_brain_inspected metadata schema: {node_count, edge_count, task_count, patch_intent_count}
- export_project_brain_json: {"version": 1, "job_id", "nodes": [...], "edges": [...]}
- 1111 tests pass

## Key facts (Agent Loop — Step 22.1)
- derive_agent_loop_state reflects CURRENT state, not worst historical event
- Stale perm_denied events (task later completed or no longer pending) do NOT block
- Check 1 (current block): explicit "deny" override in job.metadata["permissions"] + pending tasks
  - default-deny capabilities (repo_generated_write) do NOT trigger this check
- Check 2 (event-based): task_run_failed perm_denied with PENDING task and no later task_run_completed
- blocked_reason format: "permission_denied:workspace_write" (capability in colon-separated suffix)
- Summary renders: "blockers: permission_denied (workspace_write)"
- Next action uses concrete capability: "remedy set-permission <job_id> allow workspace_write"
- agent_loop_inspected metadata schema is fixed: {stage, decision, cycle, max_cycles, pending_finding_count}
- Redaction sentinels: DIFF_PREVIEW, RAW_COMMAND_OUTPUT, APPROVAL_REASON, EVENT_MESSAGE, ARTIFACT_CONTENT
