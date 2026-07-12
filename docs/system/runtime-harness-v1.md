# Runtime harness v1 (F007)

> **Status (2026-07-12):** `[~]` — merged through PR #127 (`7733a1d`, follow-up
> `d0a08a1`), **external acceptance pending**. Treat it as a working checkpoint, not
> as an accepted feature. Target: [`../roadmap/features/T0_F007.md`](../roadmap/features/T0_F007.md).

Starts, inspects and stops the target project's development server — locally, with no
Docker and no provider call.

## Configuration

Canonical binding is `.remedy/config.toml`:

```toml
[runtime]
cmd = ["npm", "run", "dev", "--", "--port", "{port}"]   # argv, never a shell string
cwd = "apps/ui"
port = 5173
health_path = "/"
ready_timeout_s = 30
```

`{port}` is replaced with the EFFECTIVE port (and exported as `PORT`). Without a
config, the runtime is detected from checked-in files only — Vite, Next.js,
FastAPI/Uvicorn. Two candidates is ambiguity, and ambiguity blocks with
"configuration required". Explicit config always wins. Malformed values are
configuration errors, never tracebacks.

## Commands

| Command | What it does |
|---|---|
| `remedy runtime serve --repo <path> [--json]` | Starts a **persistent** dev server and returns. The supervisor keeps it alive. |
| `remedy runtime probe --repo <path> [--json]` | Probes a served runtime without stopping it; otherwise starts one, probes it and stops it again. |
| `remedy runtime stop --repo <path> [--json]` | Stops the supervisor, the app and all descendants. Idempotent. |

## Supervisor ownership

`serve` is short-lived, so it does not own the runtime. It starts
`python -m packages.runtimes.runtime_supervisor` in its own session; the supervisor
owns the application and the bounded log pump for the runtime's whole life and reports
back over a private atomic handshake file. `serve` reports success only after a durable
`running` record exists whose supervisor **and** application identities both verify.

## State and logs

```
<data root>/projects/<project-digest>/runtime.json    # durable state (atomic writes)
<data root>/projects/<project-digest>/runtime.log     # bounded, capped, newest kept
<data root>/projects/<project-digest>/runtime.lock    # lifecycle lock (fcntl)
```

Nothing is ever killed by port number, and nothing is killed unless its live pid,
creation time, command line, fingerprint and process group all verify.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | success |
| 2 | configuration error (missing, ambiguous, unsafe or mismatched spec) |
| 3 | startup error (the process could not start, or died before readiness) |
| 4 | readiness error (the health URL never answered in time) |
| 5 | lifecycle/state error (stop failure, surviving rollback, corrupt or unprovable state, lock busy) |

## Recovery and manual cleanup

- **`stop_failed`** — something survived; the state is kept, run `remedy runtime stop`
  again.
- **`interrupted_start`** — a `starting` record with no live supervisor; stop it to
  clean up. A duplicate is never started.
- **`identity_unproven` / `identity_mismatch`** — the recorded process cannot be proven
  to be ours; nothing is killed and the record is kept for you to inspect.
- **corrupt / unreadable `runtime.json`** — blocks start and stop (exit 5) and is never
  deleted; inspect the file, then remove it yourself if it is genuinely stale.

## Known limitations

- Not externally accepted yet (`[~]`).
- No watchdog: if the supervisor is killed while the app lives, `probe`/`stop` clean up,
  but nothing restarts the runtime.
- Project identity is a resolved-path digest (F146 is not implemented): moving the
  project directory orphans its runtime state.
- The log pump is a daemon thread; it is joined on every normal stop, but a process that
  survives a failed stop can leave it blocked on the pipe — the same case the stop
  already reports as a survivor.
