# Plan

## Goal
Step 2.5: Storage and CLI Hardening — make local job persistence robust and the CLI usable before Step 3.

## Current Step
In progress — continuing on feature/step2-packaging-cli (PR #3 open, in-scope extension).

## Next Steps
1. Job.created_at field (timezone-aware UTC datetime)
2. Storage: JobNotFoundError, _resolve_data_dir(), list_jobs()
3. CLI: list-jobs, show-job commands
4. Tests: update monkeypatch pattern, add list_jobs + sorting tests
5. README: storage resolution docs, new commands
6. Push updates to PR #3

## Risks
- _resolve_data_dir uses __file__ to find repo root; fine for editable/source installs
- list_jobs silently skips corrupted files; documented limitation
