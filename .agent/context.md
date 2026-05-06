# Context

## Active Branch
feature/step21-project-constitution-v1

## PR
(open — see GitHub)

## Scope
Step 21 + 21.1 + 21.2 + Step 22: Project Constitution v1 (extraction, trust-report /
timeline integration, safety hygiene) and Agent Loop Contract v1 (orchestration contract
for external agent workflows).

New files:
- packages/orchestration/project_constitution.py
- packages/orchestration/agent_loop.py
- tests/test_project_constitution.py (81 tests)
- tests/test_agent_loop.py (56 tests)

Modified:
- apps/cli/main.py: constitution, agent-loop commands + trust-report loads constitution at render time
- packages/orchestration/cockpit.py: optional constitution parameter
- packages/orchestration/trust_report.py: optional constitution parameter; 5 rendering states
- packages/orchestration/timeline.py: project_constitution_loaded as first-class event
- docs/architecture.md: Project Constitution + Agent Loop sections

## Key facts (Agent Loop)
- Contract layer only — no external processes called in v1
- AgentAdapterSpec and AgentLoopState are frozen dataclasses
- derive_agent_loop_state: permission_denied → blocked (priority 1); pending non-low intents → needs_approval; all done + approved → complete; pending tasks → continue/build; no tasks → continue/planned
- Low-risk pending intents do NOT force needs_approval in v1
- agent_loop_inspected run log event: stage, decision, cycle, max_cycles, pending_finding_count only
- CLI: remedy agent-loop <job_id>

## Key facts (Constitution)
- Never persisted to job metadata — loaded fresh at render time
- project_constitution_loaded run log event: structured counts only
- Trust Report Section 6: 5 cases — available/no-sources/unavailable/not-loaded/no-repo
- Timeline: project_constitution_loaded → first-class event

- 1039 tests pass
