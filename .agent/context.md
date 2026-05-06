# Context

## Active Branch
feature/step21-project-constitution-v1

## PR
(open — see GitHub)

## Scope
Step 21 + 21.1 + 21.2: Project Constitution v1 (extraction, integration, hygiene).
Step 22: External Agent Loop Contract v1 (orchestration contract).
Step 22.1: Agent Loop stale blocker fix + run-log/redaction hardening.

New files:
- packages/orchestration/project_constitution.py
- packages/orchestration/agent_loop.py
- tests/test_project_constitution.py (81 tests)
- tests/test_agent_loop.py (68 tests)

Modified:
- apps/cli/main.py: constitution, agent-loop commands
- packages/orchestration/cockpit.py, trust_report.py, timeline.py
- docs/architecture.md

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
- 1051 tests pass
