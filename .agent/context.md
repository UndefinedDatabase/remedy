# Context

## Active Branch
`feature/step17-timeline`

## PR
(none yet)

## Scope
Step 17: Timeline v1 — read-only CLI cockpit over run-log events.

New files:
- packages/orchestration/timeline.py: load_run_events, summarize_timeline
- tests/test_timeline.py: 45 tests

Modified:
- apps/cli/main.py: _cmd_timeline + "timeline" subparser + dispatch
- docs/architecture.md: Timeline v1 section

## Key facts
- `remedy timeline <job_id>` reads all *.jsonl under <data_dir>/runs/<job_id>/
- events sorted by timestamp across multiple JSONL files
- plain text output: header, Events, Current status, Next suggested action
- task events grouped into compact blocks (started → terminal)
- unknown events rendered as "○ <name>" — never crash
- interrupted task (no terminal event) rendered as "! <type> interrupted"
- next action is deterministic: permission_denied → set-permission,
  patch risk → review, pending → run-next-task-local, else → inspect/create-job
- read-only: no state mutation, no external deps
- 680 tests pass
