# Context — current state

## Where the product is

- F001–F006 complete and merged. **F007 (Runtime harness) externally ACCEPTED** and merged
  into `main` (PR #129, merge `61e5b4a`); it is `[x]` in `docs/roadmap/STATUS.md`.
- **F010 (Automatic failure post-mortems) is ACCEPTED and `[x]`** — external verdict
  `PASS_WITH_RISKS — ACCEPTED` (2026-07-14), Evidence job `01363c70e13046e2`, package
  `remedy-review-20260714-135557-READY_FOR_REVIEW.zip`.
  - `packages/orchestration/failure_postmortem.py` — `FailureClass`, `FailureSignals`, the
    pure `classify()`, `PostmortemV1` and the atomic exactly-once writer.
  - `packages/orchestration/failure_stats.py` + `remedy stats failures` — file-based
    aggregation with an honest coverage line. No database.
  - Wiring: one post-mortem per finally-failed logical provider call (recovered retries
    write nothing), one rollup per terminally failed task, and one **job-scope** record for
    a job that failed before any task ran (worktree lock/conflict during workspace
    acquisition). Streamed call records are collected from the job stream tree and exported
    canonically under `task_runs/<task>/call_postmortems/`.
  - A post-mortem that cannot be written is durable (`postmortem_error` in the run JSON,
    `postmortem_integrity.json` in the export) and **blocks** the final verifier.
  - `runtime_probe_failed` is classifier-only: no production path emits it today.
  - `provider_timeouts.is_timeout_error()` / `is_nonzero_exit_error()` are now THE shared
    predicates; the retry path and the classifier both import them. Retry policy unchanged.
  - Config `postmortem.llm_summary` defaults **false**; v1 makes zero provider calls.

## Boundaries

- `stopped` (F011) and `budget_exhausted` (F018) are reserved classes: classifiable, wired
  to nothing.
- F008, F009, F011, F012, F017, F018 and F146 are NOT started.
- No database, no new dependency, no provider call, no Docker anywhere in F010.
- F010's accepted residual risk: the post-mortem writer does not resist a **same-UID**
  process that renames an already-opened private evidence directory (that adversary can
  edit the evidence directly anyway). Everything else — traversal, pre-existing symlinks,
  inode substitution, ineffective `O_NOFOLLOW`, check/open races — is refused. See
  `docs/roadmap/features/T0_F010.md`.
