# Serve Daemon v1

> Built state of F200 (`docs/roadmap/features/T12_F200.md`, Tier 12, Amendment
> section). `remedy serve start` runs one supervisor per data root; while it
> answers, the command line sends it the four commands it carries and runs
> every other command directly, exactly as it does with no supervisor
> running. The target spec's unamended Context, Design and Task slicing
> predate this built state and are superseded where they disagree, per
> DECISION F200 D1.

## The three commands

`remedy serve start` runs the supervisor in the foreground until it receives
SIGTERM or SIGINT, or is interrupted at a terminal (`packages/orchestration/serve_daemon.py`,
`run_supervisor`). `remedy serve status` reports whether a supervisor answers
on the resolved data root's socket, and its process id when it does
(`supervisor_state`). `remedy serve stop` sends SIGTERM to that process and
waits for the socket to stop answering (`stop_supervisor`). All three are
implemented in `apps/cli/commands/serve_cmd.py`.

## One supervisor per data root

Every file the supervisor owns lives under the `serve` data-root class
(`packages/orchestration/serve_paths.py`), computed the same way by the
supervisor and by every client, so a client finds the socket exactly where its
own data root resolution says it is:

| File | Name | Purpose |
|---|---|---|
| socket | `serve.sock` | the unix socket the command line talks to |
| process id file | `serve.pid` | read only to send `stop`'s SIGTERM |
| token file | `serve.token` | the bearer token a client reads to talk to the socket |
| run registry | `runs/` | one `<job id>.json` record per run the supervisor started, plus its `.out`/`.err` logs |
| order registry | `orders/` | one `<order id>/` folder per order the supervisor started: its text (`order.md`), its record (`order.json`) and its `out.log`/`err.log` |

The `serve` directory, the socket and the token file are all created readable
by their owner only (mode `0700` for the directory, `0600` for the socket and
the token file). Access control is the file system: nothing beyond the
owner's permission to read the token can reach the socket's commands. A
supervisor counts as running exactly when its socket accepts a connection;
the process id file is read only to stop it, never to decide whether it runs.

Each order gets its own folder under `orders/`, also created readable by its
owner only (mode `0700`; F253 S5a, DECISION F253 D13). No route under
`/api/v1` starts an order yet — `remedy client order <order>` only reads a
record `OrderLauncher.start` already began, and only that launcher's own
tests call it, until S5b adds the route.

A data root whose socket path would exceed a unix socket's length limit (104
bytes on macOS, 108 on Linux, including the terminating NUL) is refused at
start with the setting to shorten, rather than silently placed somewhere a
client would not look (`socket_path_problem`).

## The socket is the cockpit's own write door

The supervisor answers its socket with a subclass of the cockpit's own
request handler (`_RemedyHandler` in `packages/orchestration/ui_server.py`),
built by `serve_daemon.socket_handler_class`. An envelope sent over the
socket therefore passes the exact same checks — token, CSRF header, the job,
the payload shape, the command catalog, the nonce and the rate limit — that a
command the cockpit's page sends passes, and no second write protocol exists.
The one difference from the cockpit's own server is the `source` an applied
effect is recorded with: `cli`, the word `SOCKET_EFFECT_SOURCE` names, instead
of `ui`. A command the socket does not accept is refused exactly as the door
refuses it.

## Client mode: four commands, everything else direct

While a supervisor answers, the command line is a client for exactly four
commands — `job stop`, `job pause`, `job unpause` and `job run` — and runs
every other command directly in both modes, the same way a command the door
does not carry already does (DECISION F200 D4).

For `job stop`, `job pause` and `job unpause`, everything before the write —
resolving the job id, and a refusal a read alone can decide — runs exactly as
it runs directly; only the write itself is sent to the supervisor as one F009
command envelope with a fresh nonce, and the printing below that point is the
same code in both modes (DECISION F200 D3, `apps/cli/serve_client.py`,
`forward_effect`). A `--source` the client names travels with the envelope
and is recorded as given; the cockpit's own handler always records `ui`.

`job run <job>` goes through the supervisor only when it is given with at
most `--json` and the job exists on this data root; with any other option, or
a job the data root does not hold, it runs directly, printing exactly what it
always printed (DECISION F200 D5). When it does go through the supervisor,
the command line sends `job.run`, the supervisor starts the job as a child
process and the command line follows that run's output to its end:
`serve_client.follow_run` copies the run's growing standard output and
standard error to its own, and exits with the run's real exit code once its
record names one. Every ending the exit-code table has no narrower code for —
Ctrl-C (which stops following and leaves the run going), a run a signal
ended, or a run whose process is gone with no end recorded within five
seconds — exits 1, `failed`.

`REMEDY_SERVE_DIRECT`, set to any non-empty value, forces direct mode
regardless of whether a supervisor answers. The supervisor sets it for every
run it starts, so a run it launched never sends a command back to the
supervisor that is waiting on it.

## Running a job through the supervisor

`job.run` is the one command the socket accepts beyond the cockpit door's own
set. The supervisor runs the job the way an operator would directly —
`remedy job run <job>`, through its own interpreter, with `REMEDY_SERVE_DIRECT`
set and its own data root — as a detached child process in its own session,
so the run outlives the supervisor if the supervisor ends
(`packages/orchestration/serve_runs.py`, `RunLauncher.start`). Its output
goes to `runs/<job id>.out` and `runs/<job id>.err`; its record,
`runs/<job id>.json`, is written when the run starts and again with its exit
code when it ends. A second `job.run` for a job whose run has not ended is
refused with `job_already_running`; nothing is queued.

## Restart settling

When the supervisor starts, before it serves any request on its socket, it
reconciles every run its registry still names as open — one whose record was
never written an end (DECISION F200 D7, `RunLauncher.resume_registered`):

- **adopted** — the run's process is still alive and is still running that
  job (checked through `/proc/<pid>/cmdline` on Linux, so a reused process id
  is not mistaken for the run); a second `job.run` of it is refused exactly
  as for a child this launcher started itself, and a background thread
  records its end, with no exit code, once the process is gone;
- **run again** — the process is gone, but the job's own record still reads
  `running`; the supervisor starts it again as a fresh run with fresh logs;
- **failed** — a run-again attempt that could not even launch; the stale
  record is left as it was, for the next start to try again;
- **lost** — neither of the above; the record is written with an end and no
  exit code.

`tests/orchestration/test_serve_restart_kill.py` is this behaviour's proof:
it SIGKILLs a real supervisor process and the run it started mid-task, starts
a second supervisor on the same data root, and reads from the on-disk cycle
evidence that every task ran exactly once and the job completed, matching
F047's own kill-and-resume proof for a direct run.

## Lifecycle artifacts

Two files let an operator run the supervisor as a managed service instead of
a foreground command:

- `scripts/serve/remedy-serve.service` is a systemd **user** unit
  (`~/.config/systemd/user/remedy-serve.service`) that runs `remedy serve
  start` in the foreground (`Type=simple`), restarts it on failure, and stops
  it with SIGTERM. It sets `KillMode=process`, so a stop or a restart ends
  only the supervisor and never the runs it started — the same foreground
  behaviour `run_supervisor` always has, and what lets the restart settling
  above adopt or resume those runs. Its data root comes from the operator's
  normal configuration, or from an `Environment=REMEDY_DATA_DIR=...` line the
  operator adds.
- `scripts/serve/container-entrypoint.sh` runs `remedy serve start` with
  `exec`, so the supervisor receives the container's own stop signal
  directly rather than a shell relaying it. It requires `REMEDY_DATA_DIR` and
  refuses with a plain message and exit 2 when it is unset, creates that
  directory if it is missing, and passes any arguments it is given after
  `serve start`. `REMEDY_BIN` names another `remedy` executable to exec
  instead of the one resolved on PATH. A container built from it needs an
  init process (`docker run --init`), because a run the supervisor starts
  spawns helper processes of its own, and only an init process reaps the
  ones that outlive their parent.

`tests/orchestration/test_serve_artifacts.py` parses the unit file's fields
and runs the entrypoint against a stub `remedy` executable, proving the
`exec` replacement, the argument passthrough and the `REMEDY_DATA_DIR`
refusal.

## What is not built

- **The scheduler loop and parallelism.** F048's job queue was retired with
  no successor (DECISIONs F261 D14 and D22) and F049 is unbuilt; the
  supervisor runs exactly the jobs it is handed, each as its own process,
  and keeps no waiting line.
- **A cockpit thread inside the supervisor.** Serving the cockpit's page from
  the supervisor itself is F201's remote-access work, not this feature's.
- **The notify and audit-export workers.** Neither exists anywhere in the
  codebase today, so the supervisor hosts neither.
- **A localhost HTTP client channel.** The unix socket, access-controlled by
  owner-only file permissions, is the one client channel; a second listening
  port is out of scope here.
- **A door clause for every write command.** Only `job.stop`, `job.pause`,
  `job.unpause` and `job.run` travel through the socket in client mode;
  every other write command runs directly in both modes (DECISION F200
  D4) — both the ones the cockpit's door carries (`job.veto-task`,
  `job.steer`, `chat.send`, `job.edit-task` and the rest) and the ones it
  does not. Carrying the rest through the socket is the headless API's
  work (F253).

## Related

- `docs/roadmap/features/T12_F200.md` — the target spec, its Amendment
  section and DECISIONs F200 D1–D7.
- [operator-cockpit-v1.md](operator-cockpit-v1.md) — the cockpit's own write
  door, which the supervisor's socket answers with.
- `tests/orchestration/test_serve_daemon.py`, `test_serve_paths.py`,
  `test_serve_runs.py`, `test_serve_restart_kill.py`,
  `test_serve_artifacts.py` — the supervisor's own proof.
- `tests/cli/test_serve_cmd.py`, `test_serve_client_parity.py` — the command
  line's client mode, run in both modes.
