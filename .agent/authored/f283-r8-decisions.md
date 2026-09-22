
DECISION F283 D3 (2026-09-21, round 8) — THE SINGLE-PASS `job run --json` ANSWERS IN THE ENVELOPE,
AND A BLOCKED RESUME REFUSES THROUGH `fail()` WITH ITS OLD KEYS KEPT.

CONTEXT. `job run` and `job resume` declare `supports_json`. While the resolved cycle count is
one — the F046 rollout default — `_cmd_job_run_cycles` hands the run to
`_cmd_run_next_task_local`, which prints its outcome as a prose line on stdout whatever the flag
says: `Job <id> | task=... verified=pass log=...`, a dry-run block after it when there is one,
and on a verification failure one `verification failure:` line per failed check on stderr and
exit 1. A job with no pending task prints `Job <id> — no pending tasks. log=...` and exits 0.
The multi-cycle branch, by contrast, already prints `result.to_json()` under the flag. Separately,
`_cmd_resume` refuses a blocked resume by hand: under the flag it prints its own
`{"resumed": false, "blocked_reason": ..., "worktrees": [...]}` with no `ok` and no
`schema_version`, and without it prints `Resume blocked: ...` lines with no `Error: ` prefix.

CHOSEN, part (a) — THE SINGLE PASS. Under the flag, `_cmd_run_next_task_local` writes exactly
one envelope to stdout and no prose there. A run that verified is `emit_ok(...)` carrying the
facts the prose line carries, as keys: `job_id`, `task_id`, `task_type`, `model`,
`elapsed_ms`, `remaining`, `file`, `repo` (null when none), `patch_intents`, `verified` (true),
`failures` (empty), `dry_run` (the dry-run block's text, or null) and `log`. A run whose
verification failed is `fail("verification_failed", "<n> verification check(s) failed",
json_output=True, ...)` carrying the same keys with `verified` false and `failures` a list of
`{"check", "message"}` objects, at exit 1 — the same code the text branch uses, because the
work happened and the failure is its verdict, which is what `fail()`'s `ok: false` says to a
machine. A job with no pending task is `emit_ok(job_id=..., outcome="no_pending_tasks",
log=...)` at exit 0. With the flag off every byte and exit code is unchanged.

CHOSEN, part (b) — THE BLOCKED RESUME. Both blocked branches become
`fail("resume_blocked", <message>, json_output=json_output, resumed=False,
blocked_reason=<the same value>, worktrees=<the same list>)` at exit 1. The three keys a
consumer already reads stay under the same names and values, and the envelope adds `ok`,
`schema_version`, `error` and `message`. The text branch gains the `Error: ` prefix, as DECISION
F277 D8 part (b) ruled for the two unprefixed `job context` refusals and for the same reason: an
operator grepping for `Error: ` was missing these; the per-worktree lines become the message's
indented continuation lines, so each blocked worktree is still named on its own line.

ALTERNATIVES. Print `result.to_json()`-style raw objects for the single pass, as the
multi-cycle branch does — rejected: T002's acceptance line asks for the envelope on success, and
adding one more un-enveloped success document is adding to that sweep's work. Leave the blocked
resume's JSON as it is and only add `ok` by hand — rejected: that is a second hand-rolled
envelope, the exact shape `fail()` exists to replace.

REVERSE by deleting this paragraph and restoring `_cmd_run_next_task_local` and `_cmd_resume` in
`apps/cli/commands/job.py` from git history at the parent of the commit that lands this
decision's patch.
