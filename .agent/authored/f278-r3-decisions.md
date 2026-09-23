
DECISION F278 D2 (2026-09-22, round 3) — THE BOOLEAN HELPERS: WHICH CALLERS KEEP A BOOLEAN AND
WHICH NOW RAISE.

CONTEXT. `real_test_execution`, `self_dogfood_execution` and `token_economy` each carried an
`_atomic_write` that caught every `OSError` and returned False, wrote a FIXED sibling
`<name>.tmp` without any fsync, and, in two of the three, chmodded the parent directory to 0o700.
Measured at `b449d7b2`, five call sites: two in `create_snapshot_proof` and one in
`_store_request` IGNORED the boolean, so a failed write returned a snapshot proof or a request id
for a record that was never on disk; `save_attempt` and `save_token_budget_profile` RETURN it.

CHOSEN. (1) A function whose own return value is the boolean keeps it: `save_attempt` and
`save_token_budget_profile` answer False on an `OSError` from making the directory or from
`durable_write`, exactly as before. (2) A call site that ignored the boolean now lets the error
propagate: `create_snapshot_proof` and `_store_request` raise instead of returning an artifact
whose record is not on disk. That is T2_F278.md's own reason for existing — an artifact that is
silently incomplete is indistinguishable from a complete one — and no caller measured relied on
the silence. (3) The private parent directory is kept by `mkdir(mode=0o700, ...)` in the two
modules that chmodded it. That mode applies when the directory is CREATED; a directory that
already exists is no longer re-chmodded on every write, which is the one behaviour this drops,
and no test in the repository pinned it. (4) Each module's test file gains a class that patches
`durable_write` to record and to fail, so reverting the module turns those tests red beside the
guard.

ALTERNATIVES. Keep the silence with `contextlib.suppress(OSError)` at the ignoring sites —
rejected under (2). Add a boolean-returning variant to `secure_fs` — rejected: two call sites
return the boolean, and a second shared helper is the shape T002 exists to remove. Keep an
explicit `os.chmod` of the parent at every write — rejected: it re-adds a suppressed
`except OSError: pass` per site for a property nothing asserts.

REVERSE by deleting this paragraph and restoring the three `_atomic_write` definitions from git
history at `b449d7b2`.
