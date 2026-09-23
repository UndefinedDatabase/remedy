
DECISION F278 D1 (2026-09-22, round 2) — WHAT T002 MIGRATES, IN WHAT ORDER, AND HOW EACH DELETION
STAYS DELETED.

CONTEXT. T2_F278.md orders the survivor list re-derived from the tree when T002 is taken, never
carried from its 2026-09-08 counts. Measured by the reviewer at `41254292` by AST over `packages/`,
`apps/`, `tests/` and `scripts/`: eight private helper definitions matching `_?atomic_(private_)?write`
outside `packages/common/`, in six modules — `pingpong_job.atomic_write_text` (imported by
`checkpoints`, `mission_compiler` and `mission_state`), `proposed_tasks._atomic_write`,
`real_test_execution._atomic_write`, `self_dogfood_execution._atomic_write`,
`token_economy._atomic_write`, and `dev_server`'s `atomic_write_bytes`, `atomic_write_text` and
`_atomic_write` (the second imported by `runtime_supervisor` and `apps/cli/commands/runtime_cmd.py`).
F275's deletion took the rest of the 26 the feature file counted.

CHOSEN. (1) THE GUARD LANDS FIRST, AS A RATCHET. `tests/orchestration/test_durable_write_guard.py`
reads every definition under `packages/`, `apps/` and `scripts/` and fails on any helper outside
`packages/common/` that its `STILL_TO_MIGRATE` set does not name, and on any entry of that set that
no longer exists. The commit that deletes a copy removes its entry in the same commit, so each
deletion is pinned the moment it lands and a revert of it turns the guard red — which is the red
proof a migration otherwise lacks, because the copy it deletes worked. The set is empty when T002
ends. (2) ONE MODULE GROUP PER COMMIT: a helper and every importer it forces. (3) EACH CALL SITE
KEEPS ITS BYTES AND ITS CONTRACT. The payload is written exactly as before (no switch to
`durable_write_json`, whose sorted keys and trailing newline would change checkpoint digests); a
helper that created the parent directory is replaced by the caller's own `mkdir` where the caller
did not already make it; a helper that returned a boolean keeps that boolean at its call site.
(4) ORDER: the `pingpong_job` group and `proposed_tasks` in round 2; the three boolean helpers in
round 3; `dev_server` and its importers in round 4, together with the two INLINE temporary-file
writers the survey found, `repository_snapshot` (a fixed `.json.tmp` sibling) and
`project_registry` (no fsync at all), which define no helper and are therefore invisible to the
guard but are exactly the defect T2_F278.md's "Why this exists" measures.

NOT MIGRATED, BY NAME. `safe_publish.publish_atomically` publishes a finished review archive
through an anonymous `O_TMPFILE` inode with no-replace `linkat` and an inode-and-digest check after
publication; that is a different contract from a replace-write and its name does not match the
guard. `secure_fs.write_file_atomically`, `append_line_at` and `publish_dir_atomically` hold a
directory descriptor and live in `packages/common/`. `storage.py`'s `mkstemp` placement is on the
feature file's Do-not-touch list.

ALTERNATIVES. Land the guard last, as the feature file sketches — rejected: every migration commit
before it would have no red proof. Give `durable_write` a `make_parents` flag — rejected for now:
of the call sites measured, only `pingpong_job._persist_job` relied on the helper to create the
directory, and one explicit `mkdir` is smaller than a new parameter.

REVERSE by deleting this paragraph and `tests/orchestration/test_durable_write_guard.py`.
