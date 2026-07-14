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

- `budget_exhausted` (F018) is still a reserved class: classifiable, wired to nothing.
- **F011 (Kill switch) is ACCEPTED and `[x]`** — external verdict `PASS_WITH_RISKS —
  ACCEPTED` (2026-07-14), Evidence job `49955e41c49f41bc`, package
  `remedy-review-20260714-223538-READY_FOR_REVIEW.zip`, 0 open findings.
  `packages/orchestration/safe_points.py` is the control protocol
  (`control/jobs/<id>/stop.json`, archived on consume); the safe points live in `run_job`
  (before ANY work, including workspace acquisition) and `run_pingpong`; the job gains the
  additive `stopped` state; each consumed request leaves one `job_stopped` event and one
  `stopped` post-mortem under `evidence/stop_postmortems/<request_id>/`.
  `remedy job stop <id> [--status]`.
- **`packages/common/secure_fs.py` is the ONE implementation of the containment rules**
  (directory-FD anchoring, no-follow stat + open/fstat identity comparison, mode-bit
  writability, fail-closed). F010's post-mortem writer and F011's control area both call it —
  a hardening fix cannot land in one and miss the other.
- F011's stop finalization is a durable transaction: archive → post-mortem → event →
  STOPPED → persist → and only then remove the pending request, which is the commit record.
- F008, F009, F012, F017, F018 and F146 are NOT started. F012 is the next unchecked feature.
- F011's accepted v1 boundaries: no SIGKILL/stale-RUNNING recovery, no deep checkpoints, no
  OS-signal stop path, no signal handler/thread/daemon, no database.
- No database, no new dependency, no provider call, no Docker anywhere in F010.
- F010's accepted residual risk: the post-mortem writer does not resist a **same-UID**
  process that renames an already-opened private evidence directory (that adversary can
  edit the evidence directly anyway). Everything else — traversal, pre-existing symlinks,
  inode substitution, ineffective `O_NOFOLLOW`, check/open races — is refused. See
  `docs/roadmap/features/T0_F010.md`.
