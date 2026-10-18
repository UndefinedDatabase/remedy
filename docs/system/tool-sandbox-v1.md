# The tool sandbox (v1)

Since operator order amend1016sb (2026-10-16, DECISION amend1016sb D1 to D7) every Pi call and
every untrusted project command runs inside one operating-system boundary built by Bubblewrap
(`bwrap`). Code: `packages/orchestration/tool_sandbox.py`, the in-sandbox launcher
`packages/orchestration/sandbox_relay.py`, the hook in `exec_guard.run_guarded`, and the Pi
wiring in `pi_provider.py`. Tests against the real kernel boundary:
`tests/orchestration/test_tool_sandbox.py`.

## Why

On 2026-10-16 a local Pi builder ran `grep -r "HYG-replaced" /` for nine minutes in a lab job.
Nothing indicates a compromise: the model was local and offline, and the command was an
over-broad search. But Pi's working directory was never a boundary, its tools ran with the
operator's full rights, no single shell command had a deadline, and a job stop waited for the
running call to finish.

## What runs inside

| Runs inside the sandbox | Runs outside (trusted) |
|---|---|
| the whole Pi process: its read, edit, write, grep, find, ls and bash tools and every child | Remedy's orchestration, the planner, git operations Remedy itself runs |
| `test`-class commands (`exec_guard.run_guarded_test_command`): job tests, post-build and pre-apply tests, mission and bridge checks | Remedy's own CI (`ci_run`) and integrity gate, which run over the operator's Remedy checkout and pass `sandboxed=False` |
| `dod-process` checks (`run_guarded_dod_process_command`) | the provider relay that talks to the model endpoint |

The whole Pi process is inside, not only its shell: Pi's file tools run inside the Pi process
itself, so a boundary around `bash` alone would leave `read` and `write` unconfined.

## The boundary

A sandboxed process sees:

- **Read-only:** `/usr` and its merged links (`/bin`, `/lib`, ...), `/nix` when present, a short
  list of `/etc` entries (users, hosts, TLS roots, loader cache, time zone, `gitconfig`), the
  toolchain directories on the command's `PATH` that lie outside the system directories (each
  with its sibling `lib`, for `~/.local`, nvm or pyenv), and a git worktree's metadata
  (`<repo>/.git`), so `git diff` works.
- **Writable:** the job workspace (from Remedy's own job record, never from a model-written
  path) and a private `/tmp` with the private `HOME=/tmp/home`. Both temporary areas vanish with
  the call.
- **Nothing else.** The operator's home, other repositories, SSH keys, cloud credentials,
  `/run/user`, Remedy's data root and its tokens do not exist inside. A workspace symlink to a
  private file leads nowhere. `PATH` directories inside a git working tree (another
  repository's `bin` or virtual environment) are never exposed.
- The workspace's own `.git` link is mounted read-only over itself, so nothing inside can
  point Remedy's later host-side git commands at a planted repository.
- **Processes:** private PID, IPC, UTS and cgroup namespaces; no new privileges; a new terminal
  session. When the call ends, by exit, deadline or stop, the kernel ends every process in it,
  detached and `setsid` children included.
- **Environment:** only the caller's allowlist (`exec_guard` floors and allowlists), with `HOME`
  and `TMPDIR` replaced; `--clearenv` drops everything else.
- **Network:** a private network namespace with its own loopback only. A test suite can still
  start and probe its own server; host services and the internet are unreachable.

## The model connection

Pi needs its model endpoint, so a Pi sandbox has exactly one way out. Inside,
`sandbox_relay.py` listens on `127.0.0.1:11434` and carries each connection to a Unix socket in
a private per-call directory. On the host, `tool_sandbox.ProviderRelay` (trusted) accepts only
`POST /v1/chat/completions` and `GET /v1/models`, forces one request per connection, and talks
to the configured endpoint (`ollama.host`, local or remote, plain http). Everything else gets
a 403, so a model-controlled command cannot pull, delete or create models. Pi's `models.json`
names only the relay port; the real endpoint and any key stay outside. A model-controlled
command can reach the model endpoint too, for the two admitted requests only.

## Deadlines and stops

| Limit | Default | Setting |
|---|---|---|
| One shell command of a Pi tool call | 300 s | `pi.tool_timeout_seconds` (`REMEDY_PI_TOOL_TIMEOUT_SECONDS`) |
| One Pi call | 900 s, never longer than the job's remaining wall budget | the existing role timeout |
| A job stop reaching a running Pi call | about 1 s | none |
| Model turns of one Pi call's agent loop | 40 | `pi.max_turns_per_call` (`REMEDY_PI_MAX_TURNS_PER_CALL`) |
| Input tokens of one Pi call, summed over its turns | 400,000, never more than the job's remaining `max_total_tokens` | `pi.max_input_tokens_per_call` (`REMEDY_PI_MAX_INPUT_TOKENS_PER_CALL`) |

Remedy's tool shell (`/run/remedy/tool-shell.sh`, read-only, named in Pi's `settings.json`)
runs every bash command under `timeout`. When the command hits its deadline, the shell says
so, Pi gets exit 124 and goes on, and the command's process group is swept. A `remedy job stop`
is now also seen while a Pi call runs: the guard ends the sandbox (`pi_cancelled`) and the job
stops at its next safe point as before.

Pi has no turn or token limit of its own, so Remedy reads the event stream as it arrives and ends
the sandbox once the agent loop has used its turns or input tokens and asks for one more tool; a
final answer is never cut off. The call fails `pi_loop_limit` (never retried), the workspace keeps
what the loop wrote, the task ends `budget_exhausted`, and the turns, tool calls and tokens it used
are recorded in the run's `pi/<role>.jsonl` with the limits that applied (`loop_limits`). The limit
is checked about once a second, so a tool the model starts in that second may still run
(exec-1017 D4).

## Fail closed

There is no unsafe mode. A missing or broken sandbox refuses the work:

- `pi_preflight` raises `PiUnavailable`, so no Pi job starts;
- a sandboxed command returns exit 126 with `remedy: refused to run without the tool sandbox`
  and nothing is spawned.

A refusal is never read as a failed test (R-1343). A DoD test check records the reason
`sandbox_unavailable` and no exit code. A task's `--test-command` ends its run
`sandbox_unavailable` at once: no reviewer call, no repair round, the task's `test_passed` stays
unknown, and its post-mortem class is `sandbox_unavailable`, not `resource_limit`. The job's
verification then reads `not_run` with the reason, and its story's reason is `sandbox_unavailable`.

`remedy doctor health` (line `default_chain`) and `remedy worker doctor` (line `tool_sandbox`)
run the real self-test, which uses synthetic files and runs no model. They report one of:

| State | Meaning |
|---|---|
| `ready` | all 11 self-test checks passed |
| `missing_prerequisite` | `bwrap` is not installed |
| `unsupported_configuration` | not Linux, or the kernel refuses unprivileged user namespaces |
| `failed_self_test` | the sandbox started but one of its checks failed; do not run Pi jobs |

## Platforms

| Platform | Status |
|---|---|
| Linux | Supported. Tested on Pop!_OS 22.04 (kernel 6.17, bwrap 0.6.1). Needs `bwrap` and unprivileged user namespaces, which Debian, Ubuntu, Fedora, Arch and openSUSE allow by default. |
| Ubuntu 23.10 and later | Restricts unprivileged user namespaces through AppArmor. If the doctor says `unsupported_configuration`, add the profile below. Not tested here. |
| Windows | Run Remedy inside WSL2 (a Linux distribution); native Windows has no sandbox and Pi jobs are refused. Not tested here. |
| macOS | No supported sandbox backend; Pi jobs are refused with a clear reason. |

## Installation

    sudo apt install bubblewrap          # Fedora: dnf, Arch: pacman -S, openSUSE: zypper
    remedy doctor health

Ubuntu 23.10 and later, only when the doctor says `unsupported_configuration`: save this as
`/etc/apparmor.d/bwrap` and load it with `sudo apparmor_parser -r /etc/apparmor.d/bwrap`.

    abi <abi/4.0>,
    include <tunables/global>
    profile bwrap /usr/bin/bwrap flags=(unconfined) {
      userns,
      include if exists <local/bwrap>
    }

## Known limits

- Network precision: inside a Pi sandbox the model endpoint is reachable for the two admitted
  requests, by Pi and by its commands alike. Nothing else is reachable.
- Inside the sandbox the model may create nested user namespaces (bwrap 0.6 has no
  `--disable-userns`); they cannot reach any path the sandbox does not contain.
- `/tmp` and `HOME` inside are memory-backed with the kernel's default tmpfs size.
- Pi's own `grep` and `find` tools need ripgrep (`rg`) and fd on the system `PATH`; offline Pi
  does not download them, and a shell function or alias named `rg` does not exist inside the
  sandbox. Optional: `sudo apt install ripgrep fd-find` (Debian and Ubuntu install fd as
  `fdfind`, which Pi finds by that name too); without them the model searches through `bash`.
- Outside this boundary: the explicit `claude-cli` provider (Claude Code's own permission
  model), and the `runtime-server`, `runtime-build` and `dod-app` classes, which serve or build
  an app the operator opens from the host. The limits of those classes are in
  [exec-guard-limitations-v0.md](exec-guard-limitations-v0.md).
- A test command that needs a host-wide resource the sandbox hides (a database socket, a home
  configuration file, the internet) fails inside the sandbox and says so in its output.

## Rollback

Revert the merge commit of the sandbox branch on Remedy's `main` and restart the supervisor.
The previous state runs Pi unconfined, which this page explains is unsafe.
