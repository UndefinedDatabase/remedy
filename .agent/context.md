# Context

## Active Branch
feature/step18-cockpit-v1

## PR
(none yet)

## Scope
Step 18: Cockpit v1 — decision-oriented overlay on run-log events.
`remedy cockpit <job_id>` answers: "where are we, what matters, what needs the user, what can continue automatically?"

New files:
- packages/orchestration/cockpit.py: summarize_cockpit + helpers
- tests/test_cockpit.py: ~50 tests

Modified:
- apps/cli/main.py: _cmd_cockpit + "cockpit" subparser + dispatch
- docs/architecture.md: Cockpit v1 section (after Timeline v1 section)

## Key facts
- Timeline = chronological audit trail; Cockpit = decision surface
- summarize_cockpit(job, events, *, data_dir=None) -> str
- Sections: header, Situation, Needs your attention, Can continue automatically,
  Important artifacts, Next best action
- repo_generated_write attention item only fires when EXPLICITLY denied, not at default
- Shares load_run_events from timeline.py — one reader, two views
- read-only: no state mutation, no external deps
- 766 tests pass
