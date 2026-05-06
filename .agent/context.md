# Context

## Active Branch
feature/step21-project-constitution-v1

## PR
(open — see GitHub)

## Scope
Step 21 + 21.1: Project Constitution v1 — read-only policy extraction from known files in
an attached target repo, with trust-report and timeline integration polish.

New files:
- packages/orchestration/project_constitution.py: ProjectConstitution, load_project_constitution(), render_constitution()
- tests/test_project_constitution.py: 97 tests

Modified:
- apps/cli/main.py: constitution command + trust-report loads constitution at render time
- packages/orchestration/cockpit.py: optional constitution parameter
- packages/orchestration/trust_report.py: optional constitution parameter; Section 6 renders 5 distinct states
- packages/orchestration/timeline.py: project_constitution_loaded rendered as first-class event
- docs/architecture.md: Project Constitution v1 section + Step 21.1 updates

## Key facts
- Constitution is never persisted to job metadata — loaded fresh and read-only at render time
- project_constitution_loaded run log event: source_count, warning_count, has_test_commands only (no raw content)
- Trust Report Section 6: 5 cases — available/no-sources/unavailable/not-loaded/no-repo
- _cmd_trust_report passes constitution=None when no target_repo (not load_project_constitution(None))
- Timeline: project_constitution_loaded → "✓ Project Constitution loaded  sources=N  tests=yes/no"
- 982 tests pass
