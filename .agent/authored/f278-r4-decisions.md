
DECISION F278 D3 (2026-09-22, round 4) — THE RUNTIME GROUP AND THE INLINE WRITERS END T002, AND
WHAT T002 DELIBERATELY LEAVES.

CONTEXT. `packages/runtimes/dev_server.py` carried `atomic_write_bytes`, `atomic_write_text` and
`_atomic_write`, used by `runtime_supervisor`, by `apps/cli/commands/runtime_cmd.py` and by one
test. Measured at `ce53bd0c`: its temporary name was `.<name>.<pid>.tmp`, unique per PROCESS but
shared by two threads of one process, and its file fsync sat inside `contextlib.suppress(OSError)`.
DECISION F278 D1 also put here the two inline writers the guard cannot see:
`repository_snapshot.update_apply_record_state`, which wrote a fixed `.json.tmp` sibling with no
fsync, and `project_registry.save_project`, which used `mkstemp` correctly but never fsynced.

CHOSEN. (1) All three runtime helpers are deleted and every caller imports `durable_write`; the
file mode stays 0o600, the default of both. A caller the old helper silently gave a directory
gets its own `mkdir` where no `ensure_runtime_dir` or `mkdir` already precedes it — the
supervisor's handshake and the command's stop request. (2) A failed fsync now RAISES where the
old runtime helper suppressed it. A runtime record whose data may not be on disk is the silent
incompleteness T2_F278.md exists to remove, and every runtime call site that must not raise
already wraps its write in its own `suppress`, which this round leaves as it found it.
(3) `update_apply_record_state` keeps its boolean and its "record unchanged on failure"
promise; `save_project` keeps raising, as it did. (4) The guard's `STILL_TO_MIGRATE` is EMPTY
from this round: any function matching `_?atomic_(private_)?write` outside `packages/common/` is
now a failure.

WHAT T002 DELIBERATELY LEAVES. Plain writers that never claimed atomicity — `write_text`,
`write_bytes`, and small wrappers such as `repository_snapshot._write_private` — are outside
T2_F278.md's T002, whose subject is the private ATOMIC-write copies and the temporary-file race.
They are not measured here and no claim is made about them. `safe_publish.publish_atomically` and
the descriptor-anchored writers in `secure_fs` stay, as DECISION F278 D1 states.

ALTERNATIVES. Keep `atomic_write_text` in `dev_server` as a one-line alias of `durable_write` so
the importers need no edit — rejected: AGENTS.md "Replacing is deleting" forbids the alias, and
the guard would have to allow it by name. Keep the suppressed fsync for runtime records —
rejected under (2).

REVERSE by deleting this paragraph and restoring the three runtime helpers and the two inline
writers from git history at `ce53bd0c`.
