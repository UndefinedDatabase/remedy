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
Step 24.1: Brain CLI JSON + Detail Smoke Hardening.
Step 24.2: Brain Smoke Test Polish.
Step 24.3: Brain Smoke Final Polish.
Step 25: Brain Viewer v0.
Step 25.1: Brain Viewer v0 robustness polish + future architecture hooks.

New files:
- packages/orchestration/project_constitution.py
- packages/orchestration/agent_loop.py
- packages/orchestration/project_brain.py
- packages/orchestration/brain_detail.py
- packages/orchestration/brain_viewer.py
- tests/test_project_constitution.py (81 tests)
- tests/test_agent_loop.py (68 tests)
- tests/test_project_brain.py (80 tests)
- tests/test_brain_detail.py (52 tests)
- tests/test_brain_smoke.py (39 tests)
- tests/test_brain_viewer.py (46 tests)

Modified:
- apps/cli/main.py: constitution, agent-loop, brain (--json), brain-node (--json), brain-view commands
- packages/orchestration/cockpit.py, trust_report.py, timeline.py
- docs/architecture.md

## Key facts (Brain Viewer v0 — Step 25 / 25.1)
- CLI: remedy brain-view <job_id>
- Writes to REMEDY_DATA_DIR/viewers/<job_id>/index.html + viewer_data.json
- Stdout: "Brain Viewer v0: <path>"
- Constitution loading is advisory: stale/missing repo → constitution=None + safe stderr warning
- Warning text: "Warning: project constitution unavailable for viewer."
- No raw exception text in any output
- BrainViewerData frozen dataclass: {job_id, generated_at, graph, node_details, positions, detail_fallback_count}
- detail_fallback_count: int = 0 (default); increments on per-node detail failure
- export_brain_viewer_json schema: {version:1, job_id, generated_at, graph, node_details, positions, detail_fallback_count}
- Run-log event: brain_viewer_prepared schema: {node_count, edge_count, detail_count, detail_fallback_count, mode}
- mode is always "static" in v0
- Layered radial layout: job=layer0 (centre), constitution/task=layer1 (r=150),
  artifact/run_event/agent_loop=layer2 (r=290), patch_intent/approval/verification/blocker=layer3 (r=420),
  memory_placeholder/mcp_placeholder=layer4 (r=530)
- Read-only — no repo mutation, no external deps (stdlib only)
- Redaction: same policy as brain_detail — no content/diff/reason/message/command in any file
  (covers event.message and metadata.command_output from run-log events too)
- 1268 tests pass (46 in test_brain_viewer.py)

## Key facts — Future Brain Hierarchy (documented, not implemented)
- Job Brain: single job/prompt/run (current scope)
- Repo Brain: single repository + multi-job history
- Project Brain: multi-repo, multi-job, project-level memory + policies
- Remedy Global Brain: quarantined MCPs, approved MCP Skill Cards, model scorecards,
  global capability policies, verifier/provider/router knowledge
- MCP Skill Card lifecycle: quarantine → global approval → project opt-in (not automatic)
- Context Collector: reports Context Coverage (observable signals), not "knowledge %"
- Future "continue from node": new job linked by project_id, repo_id, parent_job_id, origin_node_id

## Key facts (Brain CLI JSON Contract — Steps 24.1 / 24.2)
- brain --json: canonical machine contract for future 2D/3D graph (version, job_id, nodes, edges)
- brain-node --json: canonical machine contract for future click-detail panels (13 keys)
- JSON stdout must be pure JSON; no "Remedy Project Brain" / "Remedy Brain Node Detail" headers
- stderr empty on success for both commands
- All 5 redaction sentinels absent from JSON stdout and run-log events
- project_brain_inspected schema: {node_count, edge_count, task_count, patch_intent_count}
- brain_node_inspected schema: {node_id, node_type, connected_count, evidence_count}
- Future frontend must treat --json stdout as only machine input; must not parse human text output
- Future frontend priority: 2D graph → 3D/Animus → MemPalace → MCP
- Step 24.3 is the final pre-frontend smoke hardening pass; JSON contract fully locked
- Step 25 = read-only local Brain Viewer v0; consumes only brain --json / brain-node --json

## Key facts (Brain Node Detail — Step 24)
- BrainNodeDetail frozen=True: 13 fields including why_it_exists, connected_to, evidence,
  affected_files, next_actions, redaction_notes
- Raises ValueError (safe, truncated message) if node_id not found
- connected_to: {direction, edge_type, node_id, node_type, node_label} per edge
- Redaction: no content, diff preview, approval_reason, event.message, command output
- User prompt truncated to 120 chars for job node
- brain_node_inspected schema: {node_id, node_type, connected_count, evidence_count}

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
