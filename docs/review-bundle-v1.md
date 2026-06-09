# Review Bundle v1

Safe state package for reviewers, GPT, or team members.
Contains only safe summaries — no raw content, no secrets, no caches.

## Generate

```bash
remedy review bundle <job_id> [--output <path>] [--json]
```

Default output: `.data/review_bundles/<job_id>-review-bundle.zip`

## What's included

| Section | Content |
|---|---|
| `manifest.json` | Bundle version, included/skipped sections, safety warnings |
| `job_summary.json` | Job state, task list, artifact list (safe metadata only) |
| `proof_chains.json` | Change verification status (no raw diffs) |
| `event_summary.json` | Event counts by type, timestamps (no raw metadata) |
| `trust_report.json` | Audit trail summary text (truncated to 5000 chars) |
| `context_inspection.json` | Included/excluded paths, budget, policy gates (no file bodies) |
| `changed_files_safe.json` | Changed file paths, status, proof status (no file content) |
| `repair_summary.json` | Failure/fix/intent counts, pending intents |
| `command_summary.json` | Available CLI commands for this job |
| `bundle_readme.md` | How to review the bundle |

## What's excluded

- Raw artifact bodies
- Raw diffs
- Raw source files
- Raw stdout/stderr
- Secrets / `.env`
- `.data` directory
- `node_modules`, `dist`, `build`, `.cache`
- `__pycache__`, `*.pyc`
- `.git` directory

## Safety

The bundle builder runs a post-build safety audit checking for:
- Raw output references (tracebacks)
- Cache file references (__pycache__, .pyc)
- Secret patterns

Missing optional data produces safe empty sections, not crashes.

## Relation to make_review_zip.sh

`make_review_zip.sh` bundles tracked project files for code review.
`remedy review bundle` bundles safe job state for reviewer inspection.
They serve different purposes:
- `make_review_zip.sh` = project code snapshot
- `remedy review bundle` = job state summary (no code)

## Sharing safely

1. Generate: `remedy review bundle <job_id>`
2. Verify: check the JSON output — `safety.is_safe` should be `true`
3. Share the zip — it contains only safe metadata
