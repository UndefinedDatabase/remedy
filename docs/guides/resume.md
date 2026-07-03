# Resume Guide

## What is Replay?

Replay reconstructs job progress from the event ledger — safe metadata only, no raw content. It shows what happened, which stages were reached, and why the pipeline stopped.

```sh
remedy event replay <job_id> --json
```

## What are Checkpoints?

Checkpoints are explicit boundaries in the job timeline where resume might be possible. Each checkpoint has:

- **kind**: what stage it represents
- **status**: available, inspectable, blocked, complete
- **safe_to_resume**: whether resume is implemented and data exists
- **blocked_reason**: why resume is not possible
- **required_data**: what data is needed
- **missing_data**: what data is absent

```sh
remedy job checkpoints <job_id> --json
```

## Resume v1 — Supported Modes

| Checkpoint | Resume Mode | Status | Notes |
|------------|-------------|--------|-------|
| `source_apply_proven` | from_apply → tests | **Implemented** | Runs tests via Remedy test_runner |
| `approval_recorded` | from_approval → apply | Blocked | Structured patch payload not persisted |
| `context_ready` | from_context → builder | Blocked | Builder resume not implemented |
| `tests_failed` | from_test_failure → repair | Blocked | Repair resume not implemented |
| `tests_passed` | complete | N/A | Nothing to resume |

### Resume from Applied Patch (from_apply)

When a patch has been applied but tests haven't run yet:

```sh
# Preview what resume would do (no mutation)
remedy job resume <job_id> --checkpoint <job_id>-applied --dry-run --json

# Execute resume — runs tests via Remedy's test_runner
remedy job resume <job_id> --checkpoint <job_id>-applied --json
```

Requires:
- `repo_test_run` permission on job
- Valid target repo path
- Discoverable test command

## Blocked Reasons

| Reason | Meaning | What to Do |
|--------|---------|------------|
| `resume_mode_not_implemented` | This resume path doesn't exist yet | Wait for future implementation |
| `missing_patch_payload` | Structured patch not persisted on job | Re-run builder instead |
| `approval_pending` | Patch needs approval first | `remedy patch approve <job_id> <intent_id>` |
| `permission_denied` | Job lacks required permission | `remedy job permit <job_id> repo_test_run allow` |
| `missing_repo_path` | No target repo on job | Attach repo first |
| `repo_path_not_found` | Repo directory doesn't exist | Check path |
| `missing_test_candidate` | No test command discovered | Add tests or Makefile |

## Dry-Run

Dry-run previews resume without mutation. It validates all prerequisites:

```sh
remedy job resume <job_id> --checkpoint <id> --dry-run --json
```

Output includes `can_resume`, `would_run_stage`, `blocked_reason`, `required_capabilities`.

Dry-run does not:
- Create events
- Modify job or repo
- Run tests
- Call providers

## UI Visibility

The dashboard shows resume status in the pipeline panel:
- Whether checkpoints exist
- Whether resume is available or blocked
- The next CLI command to copy

The UI is read-only — no browser resume button.

## Normal CI

Resume does not require Ollama or any external provider. The `from_apply` mode runs tests only.
