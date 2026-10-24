# ADR-0003 — The container sandbox runner's trade-offs against the process one

> **Status: RESEARCH RECORD, fully verified 2026-10-24.** This record pins what the reviewer's
> probe measured about podman, docker and a local `python:3.12-slim` image; it carries no diff
> and needs no human apply step.

- Date: 2026-10-24
- Feature: T8_F162 — Sandbox profiles per adapter
- Runtime read: docker 29.1.3, daemon reachable; podman absent

## Context

`packages/orchestration/sandbox_profiles.py` compiles a `SandboxProfile` onto the process sandbox
(`tool_sandbox.py`). `packages/orchestration/sandbox_container.py` (DECISION F162 D7) compiles the
same profile onto podman or docker instead, as an optional second stage: inert without a runtime,
giving equivalent limits with one.

## Per dimension: the process runner against the container runner

| Dimension | Process runner (`tool_sandbox.py`) | Container runner (`sandbox_container.py`) |
|---|---|---|
| `fs_scope` | bwrap's read-only root; the workspace is the one writable tree | `--read-only` root; the workspace is the one `-v <ws>:<ws>:rw` mount |
| `net` (deny) | a private network namespace | `--network none` |
| `net` (allowlist) | shares the host network, unfiltered | `--network host`, unfiltered |
| `ulimits.cpu_s` | `RLIMIT_CPU` on the process tree | `--ulimit cpu=<n>:<n+2>` inside the container |
| `ulimits.mem_mb` | `RLIMIT_AS` on the process tree | `--memory`/`--memory-swap`, a cgroup limit |
| `ulimits.nofile` | `RLIMIT_NOFILE` on the process tree | `--ulimit nofile=<n>:<n>` inside the container |
| `allowed_binaries` | never filtered by name | never filtered by name |
| `tmp_quota_mb` | never sized | `--tmpfs /tmp:rw,size=<n>m`, sized |

## The daemon and who may reach it

Docker needs a daemon reachable over a local socket, normally rootful and reachable by any
process in the `docker` group — a wider trust boundary than the process runner's own unprivileged
bwrap, which needs no daemon and no group membership at all. Podman, when installed, runs
rootless with no daemon; `container_runtime_path` tries it first for that reason
(`CONTAINER_RUNTIME_NAMES = ("podman", "docker")`), though this host carries docker only.

## Image provenance and never pulling

Every run passes `--pull never` (`container_run_argv`); a missing runtime or a missing local
image refuses with `SandboxUnavailable`/`SANDBOX_MISSING` rather than reaching the network to
fetch one. The image is the operator's own to choose and pull; Remedy never does.

## Measured costs

Probed at `9805383c1`, local image `python:3.12-slim`, `--pull never`, a read-only root, the
workspace bound read-write, the caller's own user:

- `--ulimit cpu=1:3` on a busy loop exits 137 without `--init` and 152 with it;
- `--ulimit nofile=16:16` refuses the seventeenth open with `EMFILE`;
- `--memory 256m --memory-swap 256m` ends a 1 GiB allocation by exit 137 while 64 MiB succeeds;
- `--tmpfs /tmp:rw,size=64m` refuses a 100 MiB write with `ENOSPC`;
- a write outside the workspace fails read-only and leaves the host untouched;
- `--network none` refuses a listener on the host's loopback and `--network host` reaches it;
- a container starts and ends in 0.24 seconds.

`container_run_argv` always passes `--init`, so `run_in_container_with_sandbox_profile` reads the
152 exit, attributing it `resource_limit`/`cpu_seconds` the same way D3 (3) attributes it for the
process runner; a 137 exit is left unattributed, because a memory kill and any other kill read
the same.

## The killed-client cleanup

A client ended by its own wall timeout or a job stop can leave its container running after the
guard's own call returns; `run_in_container_with_sandbox_profile` runs `<runtime> rm -f <name>`
once whenever the result's `tripped_limit` is `wall_timeout` or `cancelled` — best effort, since
the container is already `--rm`.

## What each runner still leaves unenforced

Neither runner filters `allowed_binaries` by name. The process runner never sizes `/tmp`
(`tmp_quota_mb` is always `unenforced` there, per `sandbox_profiles.sandbox_profile_enforcement`);
the container runner is the one place that dimension is `enforced`, through its own sized
`tmpfs`. Both runners leave an allowlisted network unfiltered: the host network is shared, not
proxied or filtered by host name.

## Why no worker uses the container today

claude-cli keeps its login in the operator's own home (DECISION F162 D4 (2)), which a container
would hide the same way a throwaway `HOME` would — isolating it, not preserving it — so moving
that worker into a container buys nothing while losing its login. Every other process Remedy
spawns under a profile already runs inside the process sandbox. No configuration key selects
between the two runners, because a key would select nothing any run reads yet: R-1467 records
that gap, owned by F246, whose gate plugin run is the first process a container can hold.

## Reversal

Delete this file and its two `docs/README.md` index rows, delete
`packages/orchestration/sandbox_container.py` and its tests, remove its `ALLOWED_UNWIRED` entry
in `tests/test_no_orphan_modules.py`, and delete R-1467 and F246's Acceptance line.
