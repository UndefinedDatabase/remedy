# Context

## Active Branch
feature/step20-trust-report-v1

## PR
(open — see GitHub)

## Scope
Step 20: Trust Report v1 — read-only auditable job summary.
Adds `remedy trust-report <job_id>`. No apply, no mutation, no new deps.

New files:
- packages/orchestration/trust_report.py: summarize_trust_report()
- tests/test_trust_report.py: 60 tests

Modified:
- apps/cli/main.py: trust-report command + subparser + dispatch
- docs/architecture.md: Trust Report v1 section

## Key facts
- Trust Report = auditable summary (Timeline = chronological, Cockpit = decision-oriented)
- 9 numbered sections: User request, Plan, Execution summary, Artifacts, Verification,
  Permissions/safety, Patch intents/decisions, Redaction/trust boundary, Next safe action
- Redaction: no raw exception text, no raw artifact content, no full diff previews
- CLI: exits 0 even when no run logs (section says "No run logs available")
- data_dir=None: run log dir path omitted; all other sections still render
  All approved + no pending tasks → next action notes apply not implemented.
- 826 tests pass
