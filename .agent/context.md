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
Step 26: Context Coverage v0.
Step 26.1: Context Coverage robustness and UX polish.
Step 26.2: Smoke viewer LAN URL and Context Coverage test polish.
Step 26.5: Brain Viewer loading diagnostics and no-infinite-spinner hardening.

New files:
- scripts/remedy_smoke.sh (LAN Brain Viewer smoke helper)
- packages/orchestration/project_constitution.py
- packages/orchestration/agent_loop.py
- packages/orchestration/project_brain.py
- packages/orchestration/brain_detail.py
- packages/orchestration/brain_viewer.py
- packages/orchestration/context_coverage.py
- tests/test_project_constitution.py (81 tests)
- tests/test_agent_loop.py (68 tests)
- tests/test_project_brain.py (80 tests)
- tests/test_brain_detail.py (52 tests)
- tests/test_brain_smoke.py (39 tests)
- tests/test_brain_viewer.py (67 tests)
- tests/test_context_coverage.py (88 tests)

Modified:
- apps/cli/main.py: constitution, agent-loop, brain (--json), brain-node (--json), brain-view, context commands
- packages/orchestration/project_brain.py: NT_CONTEXT_COVERAGE, ET_HAS_CONTEXT_SNAPSHOT, node/edge
- packages/orchestration/brain_detail.py: _detail_context_coverage handler
- packages/orchestration/brain_viewer.py: _LAYER_MAP, ctx-badge HTML/JS
- packages/orchestration/cockpit.py, trust_report.py, timeline.py
- docs/architecture.md

## Key facts (Context Coverage v0 — Step 26)
- CLI: remedy context <job_id> [--json]
- derive_context_coverage(job, events, *, constitution=None) -> ContextCoverageSnapshot
- 10 signals: attached_repo(15), project_constitution(15), planned_tasks(10),
  builder_artifacts(10), patch_intents(10), verification_results(10), run_logs(10),
  approval_decisions(5), project_memory(10, always absent), mcp_tool_context(5, always absent)
- score = round(present_weight / 100 * 100), clamped 0..100
- project_memory always absent: "MemPalace not connected yet"
- mcp_tool_context always absent: "MCP Quarantine / Skill Registry not connected yet"
- export_context_coverage_json schema: {version:1, job_id, scope, score, present_weight, total_weight, signals, missing_keys}
- context_coverage_inspected metadata schema: {score, present_signal_count, missing_signal_count, scope}
- Redaction: no content, diff, reason, message, command output in any signal/detail/export
- Brain: NT_CONTEXT_COVERAGE (13th node type), ET_HAS_CONTEXT_SNAPSHOT
  - id="context_coverage", always present
  - status: low(<50) / partial(50-79) / strong(>=80)
  - metadata: {score, present_signal_count, missing_signal_count, scope}
  - edge: job --has_context_snapshot--> context_coverage
- Brain Viewer: context_coverage in layer 1, ctx-badge in header showing "Context: <score>%"
- 1356 tests pass (88 in test_context_coverage.py)

## Key facts (Context Coverage robustness — Step 26.1)
- _safe_int(value, default=0): crash-safe int parsing; replaces int(...) for artifact metadata
- patch_intents: uses _safe_int(a.metadata.get("patch_intent_count")) — "not-an-int"/[]/None safe
- v0 maximum score = 85 (project_memory +10 + mcp +5 always absent); stated in Meaning section
- _cmd_context: stale/missing repo now prints "Warning: project constitution unavailable for context coverage." to stderr; mirrors _cmd_brain_view; no exception text leaks
- brain-node detail for context_coverage: no "confidence", "model_confidence", "confidence_score" top-level keys

## Key facts (Brain Viewer v0 — Step 25 / 25.1)
- CLI: remedy brain-view <job_id>
- Writes to REMEDY_DATA_DIR/viewers/<job_id>/index.html + viewer_data.json
- Stdout: "Brain Viewer v0: <path>"
- Constitution loading is advisory: stale/missing repo → constitution=None + safe stderr warning
- BrainViewerData frozen dataclass: {job_id, generated_at, graph, node_details, positions, detail_fallback_count}
- detail_fallback_count: int = 0; increments on per-node detail failure
- export_brain_viewer_json schema: {version:1, job_id, generated_at, graph, node_details, positions, detail_fallback_count}
- brain_viewer_prepared schema: {node_count, edge_count, detail_count, detail_fallback_count, mode}
- Layered radial layout: job=0(centre), constitution/task/context_coverage=1(r=150),
  artifact/run_event/agent_loop=2(r=290), patch_intent/approval/verification/blocker=3(r=420),
  memory_placeholder/mcp_placeholder=4(r=530)
- 1335 tests pass

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

## Key facts (Brain Node Detail — Step 24)
- BrainNodeDetail frozen=True: 13 fields including why_it_exists, connected_to, evidence,
  affected_files, next_actions, redaction_notes
- Raises ValueError (safe, truncated message) if node_id not found
- connected_to: {direction, edge_type, node_id, node_type, node_label} per edge
- brain_node_inspected schema: {node_id, node_type, connected_count, evidence_count}

## Key facts (Project Brain — Steps 23/23.1)
- Read-only graph: BrainNode, BrainEdge, ProjectBrainGraph frozen dataclasses
- 13 node types (now including context_coverage), 12 edge types (now including has_context_snapshot)
- project_brain_inspected schema: {node_count, edge_count, task_count, patch_intent_count}

## Key facts (Agent Loop — Step 22.1)
- derive_agent_loop_state reflects CURRENT state, not worst historical event
- agent_loop_inspected schema: {stage, decision, cycle, max_cycles, pending_finding_count}
