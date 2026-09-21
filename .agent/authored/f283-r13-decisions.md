
DECISION F283 D8 (2026-09-21, round 13) — `remedy runtime` REFUSES THROUGH `fail()` WITH A TOKEN
PER ERROR CLASS, AND `error_class` SURVIVES IN THE PAYLOAD.

CONTEXT. `apps/cli/commands/runtime_cmd.py` refuses through a local `_fail(message, code, *,
json_output, payload)` that under `--json` prints `{"ok": false, "error": <the message>, ...}`
without `schema_version`, so its `error` key holds a sentence where every other command's holds a
token. Every call passes an `error_class` — `config`, `start`, `ready`, `handshake`, `state`,
`lock` or `stop` — which the module docstring's exit-code contract (2 to 5) is keyed on and which
is a contract with the supervisor subprocess and `packages/runtimes/dev_server.py`; this
feature's file rules that it survives. Four more exits print a result document and then exit
non-zero: the one-shot probe's cleanup survivors, a one-shot probe that did not reach readiness,
a served runtime whose health URL failed, and a `stop` that did not stop — the D5 shape.

CHOSEN. `_fail` is deleted. A module-local `_runtime_refusal(error_class, message, exit_code, *,
json_output, **payload)` calls `fail()` with the token `RUNTIME_ERROR_TOKENS[error_class]`,
`exit_code` unchanged and `error_class` kept in the payload beside every key the old call passed,
so the token and the class cannot drift apart. The tokens: `config` → `runtime_config_error`,
`start` → `runtime_start_failed`, `ready` → `runtime_not_ready`, `handshake` →
`runtime_handshake_timeout`, `state` → `runtime_state_error`, `lock` → `runtime_lock_busy`,
`stop` → `runtime_stop_failed`, and a class the supervisor reports that the table does not
name → `runtime_error`. The four result-shaped exits answer ONE failure envelope under `--json`
carrying the result document's keys except `ok` and `error`, whose sentence becomes the
envelope's `message`, at the exit code they use today; their text branches are unchanged. The old
`error` key held the sentence; a reader of it now reads `message`.

ALTERNATIVES. Fold `error_class` into the token and drop the key — rejected by this feature's own
file. Keep `_fail` and add `schema_version` to it — rejected: it is a second envelope writer.
Give each call site its own token — rejected: the class is the condition the exit-code contract
already names, and seven tokens keyed on it are what a consumer can branch on.

REVERSE by deleting this paragraph and restoring `apps/cli/commands/runtime_cmd.py` from git
history at the parent of the commit that lands this decision's patch.
