# Plan — Steps 6081-6140 — F007 — Runtime harness

## Goal
A local runtime harness that can start, wait for, inspect and stop the target
project's dev server safely: `remedy runtime serve|probe|stop`, bound to
`.remedy/config.toml [runtime]`, with a free-port fallback, HTTP readiness, bounded
logs and a process-TREE shutdown that leaves no zombies and can never kill an
unrelated process that inherited a recycled PID.

## Current Step
**Final F007 round: persistent runtime supervisor implemented; merging as the
honest checkpoint. F008 and F146 untouched.**

## Final round — persistent supervisor

The reviewed implementation let the SHORT-LIVED `runtime serve` CLI own the dev
server and the log pump, so the server died ~300 ms after the CLI exited. `serve`
now starts a persistent supervisor (`packages/runtimes/runtime_supervisor.py`, run as
`python -m packages.runtimes.runtime_supervisor`) in its own session:

    serve CLI (short-lived)
      └── supervisor (survives the CLI)
            ├── bounded LogPump (owns the app's stdout for its whole life)
            └── application (child of the supervisor)

The supervisor opens the log, launches the app, records BOTH identities
(supervisor_pid/create_time/cmd/cwd/fingerprint/pgid/sid and the app's), persists
`starting`, waits for readiness, persists `running` transactionally, reports through a
private atomic filesystem handshake, and then stays alive: pumping logs, watching the
app and polling a local stop-request file. `serve` returns success only after it sees
a durable `running` record whose supervisor and app identities both verify.

`probe` reaches a served runtime and leaves it running; `stop` asks the supervisor to
shut down, waits, verifies the whole family is gone, and keeps a retryable
`stop_failed` state on survivors. A bare `starting` state is never `already_running`:
with a live supervisor it is `runtime_start_in_progress`, without one it is
`interrupted_start`. A `probing` runtime is never adopted by a permanent serve.

## External review 2 — FINDINGS

1. `session_id` was persisted but never verified: a state with the right PID and a
   FOREIGN group id made `killpg` fall on an unrelated process group.
2. Lifecycle transitions were incoherent: probe verified state outside the lock, and
   serve released the lock (and wrote `running`) before readiness.
3. `RuntimeSpec.fingerprint()` hashed only cmd+cwd, so a changed port, host, health
   path, timeout or env still reported `already_running`.
4. `LogPump` opened runtime.log inside its thread, so a log failure left a live
   server with only an in-memory error string.
5. `_abort_start` ignored the rollback result and always cleared state, so a
   surviving process was reported as an atomic failure.
6. `load_state()` collapsed absent/corrupt/unreadable into None (a corrupt file let a
   second server start), and AccessDenied silently deleted the state.

## Corrections

- **F1** `pgid` and `sid` are recorded from `os.getpgid`/`os.getsid` after Popen and
  verified live before any signal; a mismatch, an uninspectable group, or a group
  equal to Remedy's own blocks. The killpg target is the LIVE observed group, never
  the stored number.
- **F2** explicit statuses (`starting`, `running`, `probing`, `stop_failed`,
  `start_cleanup_failed`, `identity_unproven`, `identity_mismatch`). Serve holds the
  lifecycle lock from state read through readiness and only then commits `running`;
  a probe that creates a server owns its whole bounded lifecycle under the lock.
- **F3** versioned `rspec1` fingerprint over argv, resolved cwd, port, host,
  health_path, ready_timeout_s and sorted env; the resolved-launch fingerprint stays
  a separate process identity.
- **F4** the log file is opened synchronously BEFORE Popen and handed to the pump,
  whose `start()` waits for a real pumping handshake; a later pump failure is
  surfaced in probe/wait_ready results and in the persisted state (`log_error`).
- **F5** `_abort_start()` returns `{stopped, survivors, stop_error, pump_status,
  partial_state_removed}`; a survivor is carried on the `RuntimeStartError`, kept as
  a retryable `start_cleanup_failed` state, and exits 5. A failed atomic write
  deletes its temp file.
- **F6** typed `load_state_result()` (absent/valid/corrupt/unreadable) and
  `classify_state()` (verified/definitely_gone/pid_reused/identity_mismatch/
  identity_unproven). Corrupt or unreadable state blocks start and stop (exit 5) and
  is never deleted; unproven/mismatched identities keep their record and kill
  nothing; only a gone process or a proven reuse is auto-cleared.

## External review — FINDINGS

1. `verify_state()` checked only PID/create_time/liveness: an unrelated process with
   the right PID and creation time but a wrong command was "verified" and killed.
2. Startup was not transactional: a `save_state` failure after `Popen` left a live,
   unmanaged process.
3. No lifecycle lock: two concurrent `runtime serve` calls started two servers and
   the second state write orphaned the first.
4. A failed stop deleted the state and still reported `ok=true`.
5. `MAX_LOG_BYTES` bounded reads only — runtime.log grew without limit.
6. Malformed TOML types raised raw `ValueError` instead of exit code 2.

## Corrections

- **F1** identity is now the whole record: project root and digest, PID, tight
  creation time, live `cmdline()` (with exactly two documented launcher forms:
  script shim and npm's process-title rewrite), live cwd, and a fingerprint
  recomputed from resolved argv + cwd + project. An uninspectable process is
  UNPROVEN, so the destructive stop is blocked. `serve` compares the running
  runtime's spec fingerprint with the resolved spec and blocks a different one with
  `runtime_spec_mismatch` instead of starting a second or killing the first.
- **F2** start is all-or-nothing: any failure after `Popen` (log open, create-time
  inspection, serialization, atomic write) stops the tree, joins the pump, removes
  partial state and raises `RuntimeStartError`. `save_state()` writes temp + fsync +
  `os.replace`, and refuses to persist a running state with no creation time.
- **F3** an fcntl `runtime.lock` per project digest serializes read → verify →
  start/stop → commit (transitions only, never the server's lifetime), released in a
  `finally`, with an honest timeout error. Different projects never block each other.
- **F4** a survivor keeps a retryable `stop_failed` state (survivors + stop_error),
  `stopped=false`, `ok=false` and exit code **5**; a later stop retries. Readiness
  failure obeys the same rule.
- **F5** a daemon log pump drains the pipe continuously and trims runtime.log to the
  newest half whenever it passes the cap, so the child never blocks and the file
  stays bounded (cap + one chunk). Stop joins the pump; it can only outlive a stop
  in the same pathological survivor case the stop already reports.
- **F6** every runtime TOML value is type-checked (int/float/bool/str/table) and
  every malformed value becomes a `RuntimeConfigError` → CLI exit 2, never a
  traceback.

## Delivered
- T001 `packages/runtimes/dev_server.py` — RuntimeSpec / RuntimeState /
  RuntimeProbeResult / DevServer. argv only (never `shell=True`), own session,
  psutil recursive process-tree stop with grace → kill → process-group last resort
  and a reaped parent. Durable state at `<data>/projects/<digest>/runtime.json`
  (PID + creation time + command fingerprint, so a reused PID is never killed) and
  logs at `runtime.log`, always read back bounded. A requested port that is busy is
  never fought over: a free port is chosen and the EFFECTIVE port reported.
  A readiness failure stops the tree and leaves no state claiming to be active.
- T002 `packages/runtimes/runtime_config.py` + `apps/cli/commands/runtime_cmd.py` —
  `.remedy/config.toml [runtime]` is canonical (the general remedy.toml system is
  untouched); detection from checked-in files only (vite / next / fastapi-uvicorn),
  never importing project code; ambiguity BLOCKS with configuration-required;
  explicit config always wins. CLI group + catalog entries; exit codes 0/2/3/4.
- T003 real `apps/ui` Vite probe (subprocess marker), using the already-installed
  local dependencies — no npm install, no network.

## Tests
dev_server 28, runtime_config 19, runtime CLI 16, lifecycle safety 51, state machine
32, **CLI process boundary 14**, real apps/ui 7 (incl. the serve-CLI-exit Vite proof)
— **167 passed**, each file separately.
Affected: command catalog 23, CLI UX 57, config CLI 14, config 55, stream evidence 38.
compileall / `bash -n` / `git diff --check` clean. Zero provider calls.

## Boundaries (binding)
No SSE endpoint, EventSource, React hook, polling badge or UI work (that is F008,
Tier 5, and it depends on F146 which does not exist). No F146 project registry: the
project digest is F006's resolved-path digest. No provider call. No Docker. No
`shell=True`. No kill-by-port. No PID-only identity.

## Status
Merged as an honest checkpoint (see the PR body). F007 stays `[~]` until an external
acceptance round covers the supervisor architecture; the last reviewed package
(`959213bbdabe432f`) predates it.
