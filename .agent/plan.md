# Plan — Steps 7601-7700 — F011 closure and integration

## Goal
A running job can be stopped safely from a second terminal. `remedy job stop <id>` writes a
durable control file; the runner notices at the next safe point, lets the in-flight provider
call finish, starts nothing new, rolls the incomplete task back to pending, persists the job
as `stopped`, writes a `job_stopped` ledger event and a `FailureClass.STOPPED` post-mortem,
archives the request, and exits cleanly. A later run resumes at the first pending task.

## Contract baseline
`docs/roadmap/features/T0_F011.md` as committed on `main` at `cc0ec37`. It matches the
operator prompt: safe points before new work only, in-flight call finishes, additive STOPPED
state, checkpoint v1 = the persisted job, archive not delete, unknown job exits 3, malformed
control file → reason `unknown` never a crash, per-call check is a file-stat with no config
reload. No material differences found; nothing built against a stale assumption.

## Discovery — the actual seams (Phase 1)

1. **Caller loop that dispatches persisted job tasks** — `packages/orchestration/pingpong_job.py::run_job`
   (`for idx, task in enumerate(job.tasks)`, line ~1588). It owns persistence, the target
   snapshot guard and the job worktree handle. THIS is the F011 job model — not the Core
   `Job` (UUID) worker-queue model in `storage.py` / `apps/cli/commands/job.py`.
2. **Job persistence** — `pingpong_job._persist_job(job)` → `<data_root>/jobs/<job_id>/job.json`,
   read back by `load_job_plan(job_id)`; serialization through `_export_job` / `_import_job`.
3. **State constants** — `TASK_PENDING/RUNNING/PASSED/APPLIED/BLOCKED/FAILED/SKIPPED`,
   `JOB_PLANNED/RUNNING/BLOCKED/COMPLETED/PAUSED` (plain module-level strings; additive).
4. **Builder provider call** — `pingpong_loop.run_pingpong`, `_call_with_retry(... role="builder")`
   at line ~2454, inside `for round_num in range(1, max_rounds + 1)`.
5. **Reviewer provider call** — same function, `_call_with_retry(... role="reviewer")` at ~2643.
6. **Reviewer parse retry** — the bounded single retry at ~2681 (`_begin_stream_call(..., "parse-retry")`).
7. **Repair-round boundary** — the top of each `round_num` iteration (~2382); `is_repair` is
   `round_num > 1 and (findings or repair_triggered)`.
8. **Task rollback after provider failure** — the caller sets `TASK_FAILED` / `TASK_BLOCKED`
   and `_block_job()`; a task only becomes durable at `TASK_APPLIED` after `_verify_in_place_apply`.
9. **Event ledger** — append is `run_log.RunLogWriter(job_id).log(event, **metadata)` writing
   `<data_root>/runs/<job_id>/<run_id>.jsonl`; read is `timeline.load_run_events()` and
   `event_ledger.list_events()` (pure normalization). NOTE: `timeline.append_run_event` and
   `event_persistence.emit_important_event` coerce the job id to a UUID, so they are for Core
   Jobs only — a JobPlan id (16 hex) must use `RunLogWriter` directly.
10. **F010 writers** — `failure_postmortem.write_postmortem(directory, record, root=…)`,
    `build_job_rollup`, `build_task_rollup`; job-level site is
    `pingpong_job._write_job_postmortem_record` → `jobs/<job_id>/evidence/postmortem.json`.
11. **Evidence export** — `job_evidence.py::_write_job_postmortem` / `_write_task_postmortems`,
    `postmortem_integrity.json` (`POSTMORTEM_INTEGRITY_FILE`) blocks the final verifier.
12. **Resume** — `pingpong_job.resume_job_plan(job_id)` → validates the worktree, calls `run_job`,
    which skips `TASK_APPLIED/PASSED/SKIPPED` and continues at the first pending task.
13. **CLI seams** — `apps/cli/command_catalog.py::CATALOG` (`CommandEntry`, group `job`) plus a
    handler module exporting `COMMAND_HANDLERS`, registered in `apps/cli/commands/__init__.py`
    (the F010 `stats failures` command is the template).
14. **Exit codes** — `EXIT_USAGE = 2` for argument validation, `1` for operational errors
    (`failure_stats_cmd`); F011 adds `3` for an unknown job, as the contract requires.
15. **Private-file idiom** — `dev_server.atomic_write_bytes` (0600 temp, fsync, `os.replace`),
    `RUNTIME_DIR_MODE = 0o700`. F011 re-implements the same idiom inside
    `safe_points.py` (orchestration must not import the runtime package) and adds F010's
    no-follow stat + `fstat` identity checks.

Data-root helpers live in `packages/orchestration/data_paths.py`; F011 adds
`control_dir` / `job_control_dir` / `job_stop_request_path` / `job_stop_archive_dir` beside them.

## Not in scope
Signal handlers, threads, daemons, SIGKILL/stale-RUNNING recovery, deep checkpoints, budgets
(F018), F012, F017. Retry policy and F010 classification are untouched.

## Status
F011 `[~]` — implementation round; not externally accepted.


## Hardening round 1 (external FINDINGS on `remedy-review-20260714-203106`)

Formally clean package, eleven real defects. Externally: `68 passed, 5 failed` on the F011
suites (the five read-only-control-area tests, because `os.access` lies to root), and
`429 passed, 2 deselected` on everything else.

Fixed: (1) control I/O reverted to full-path operations and could be redirected through a
symlinked parent — now uses the shared directory-FD-anchored primitives extracted from F010
into `packages/common/secure_fs.py`, with mode-bit writability checks that hold under root;
(2) a malformed `request_id` could traverse out of the archive — degraded ids are now a
deterministic safe hash, re-validated at the archive boundary; (3) `requested_at` was
untrusted free text reaching the evidence — now a validated ISO-8601 timestamp or empty;
(4) the request was deleted before the STOPPED state was durable — the pending file is now
the commit record and is removed last; (5) an archive failure created a false consumed
episode — an unarchived request is no episode at all; (6) `job_stopped` had no idempotency —
now exactly once per request id, checked only during finalization; (7) the pre-start stop
check ran after workspace acquisition — now before any work; (8) request creation raced —
now create-only publication, concurrent callers converge on one id; (9) stopping an
already-stopped job planted a trap request — now idempotent; (10) the global `--status`
parser change broke `propose list` — now a per-ArgDef flag declaration; (11) the run JSON
dropped the stop signal — now a bounded, redacted, versioned `stop` block.

## Next
Package Evidence and one READY_FOR_REVIEW ZIP. F011 stays `[~]`. F012 not started.


## Hardening round 2 (external FINDINGS on `remedy-review-20260714-210839`)

Externally: `test_safe_points.py` 70 passed, `test_job_stop.py` 26 passed, and
`119 passed, 1 failed` combined — the one failure being the over-broad no-leftover assertion
tripping over the review host's unrelated `artifact_tool_rpc_daemon-bun` child.

The real blocker: `secure_fs.anchor_root()` opened the trusted root's PARENT by raw name, so a
symlinked parent (`real/link -> outside`) redirected the whole root — for F011's control area
AND, through the shared helper, for F010's post-mortem writer.

Fixed: `anchor_root()` walks from the filesystem root, identity-checking every component, and
creates missing components only through held descriptors (no `Path.mkdir(parents=True)` before
validation); relative roots are made absolute first and walked identically; both features
inherit the fix. The no-leftover test is scoped to processes the test itself created, with two
tests proving it still catches a real leak.

## Next
Package Evidence and one READY_FOR_REVIEW ZIP. F011 stays `[~]`. F012 not started.


## Closure (2026-07-14)

External verdict on `remedy-review-20260714-223538-READY_FOR_REVIEW.zip`
(sha256 `47b5e2e9…36b3b9f2`, Evidence job `49955e41c49f41bc`, linked prior
`4044e32fa99d47a6`): **PASS_WITH_RISKS — ACCEPTED**, 0 open findings. 20/20 proofs matched,
no uncovered Source/Test file, provider calls 0, postmortem integrity clean. Core block 327
passed; affected block 213 passed, 2 deselected (the pre-existing `docs/resume.md` docs test,
unrelated to F011 and left alone).

F011 is `[x]`. Accepted boundaries: no SIGKILL/stale-RUNNING recovery, no deep checkpoints, no
OS-signal stop path, no signal handler/thread/daemon, no database. F012 is the next unchecked
feature and has **NOT** been started.
