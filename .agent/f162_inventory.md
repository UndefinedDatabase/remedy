# F162 inventory — every place a worker process's limits are set or could be

Read-only findings pass, round 1 (DECISION F162 D1). Every factual sentence names `path:line` at
`39beac4e1` or the command whose output it read on this machine. Section 10 ends with a PROPOSAL
for DECISION F162 D2, not a decision.

## 1. The exec guard

`packages/orchestration/exec_guard.py` is 1000 lines (`wc -l`), at the structure ledger's file
limit, with no file-level row (`docs/system/structure-ledger-v1.md`); its `run_guarded` has a
122-line ledger row (`structure-ledger-v1.md:410`).

`ExecGuardPolicy` (`exec_guard.py:174-213`) fields: `cpu_seconds` (RLIMIT_CPU soft; hard is
`cpu_seconds + cpu_grace_seconds`, default grace 2s, so SIGXCPU precedes SIGKILL), `address_space_bytes`
(RLIMIT_AS), `open_files` (RLIMIT_NOFILE), `core_file_bytes` (RLIMIT_CORE, default 0),
`wall_timeout_seconds` (the guard's own deadline, parent-side), `stream_drain_grace_seconds`
(default 5.0s, total for both pumps), `output_cap_bytes` (per stream, enforced while reading),
`cwd`, `env`/`env_allowlist` (env reaches the child unchanged while `env_allowlist` is `None`;
otherwise rebuilt by `scrub_child_env`), `deny_network` (written after the scrub, `exec_guard.py:388-393`),
`sandbox` (a `SandboxSpec`, `None` runs on the host), `cancel_check`, `stdout_observer`.

`_plan_rlimits` (`exec_guard.py:326-362`) resolves each requested rlimit via
`getattr(resource, _RLIMIT_ATTRS[name], None)` (`exec_guard.py:94-99,348`); a missing constant or a
`getrlimit` that raises `OSError`/`ValueError` is recorded `unsupported`, never dropped silently; a
hard limit above the inherited hard is clamped down (`exec_guard.py:357-359`), never raised.
`plan_child_spawn` (`exec_guard.py:365-404`) builds the `preexec_fn` that applies those rlimits
between fork and exec, builds the child env (`scrub_child_env`, `exec_guard.py:163-171`, which always
drops `FORBIDDEN_ENV_KEYS`, `exec_guard.py:104-110`, even if the allowlist names them), overlays
`DENIED_NETWORK_ENV` (`exec_guard.py:151-160`) when `deny_network`, and — only when the policy keeps
the network — calls `require_permission("external_call", ...)` (`exec_guard.py:395-397`).
`scrub_child_env` and `run_guarded` are the only two sites `FORBIDDEN_ENV_KEYS` applies to.
`run_guarded` (`exec_guard.py:455-576`) spawns argv (never `shell=True`), in its own session so a
wall-timeout kill reaches the whole process group (`_kill_process_group`, `exec_guard.py:407-414`),
reaps with `os.wait4`, drains both stream pumps under one shared grace deadline, and classifies the
outcome (`resource_limit`/`cancelled`/`ok`/`failed`); `address_space_bytes` trips are enforced but
never named in `tripped_limit` (`exec_guard.py:36-42`, restated `exec-guard-limitations-v0.md:68-74`) —
an exit-1 with no signal is indistinguishable from any other failure.

Six `*_exec_policy` factories, one per T2_F085 command class:
- `test_command_exec_policy` (`exec_guard.py:585-639`): wall timeout, output cap 16 MiB
  (`TEST_COMMAND_OUTPUT_CAP_BYTES`, `exec_guard.py:130`), cwd pin, core 0, explicit env allowlist
  (`TEST_COMMAND_ENV_ALLOWLIST`, `exec_guard.py:117-122`), `deny_network=True`, and
  `sandbox=SandboxSpec(...)` **unless** `sandboxed=False` (`exec_guard.py:638`) — the one knob that
  turns the tool sandbox off, used only by Remedy's own `ci_run`/`integrity_gate` over the
  operator's own checkout. `cpu_seconds`/`address_space_bytes`/`open_files` stay `None`; the one
  stated reason (`exec_guard.py:601-610`) is that no per-project value has been measured yet.
- `dod_process_exec_policy` (`exec_guard.py:693-739`): same shape, `sandbox=SandboxSpec(...)` always
  (`exec_guard.py:738`, no off-switch), `deny_network=True`.
- `dod_app_exec_policy` (`exec_guard.py:781-815`): `wall_timeout_seconds=None`,
  `output_cap_bytes=None` (the caller owns both), **no `sandbox=` field set** — unsandboxed.
- `runtime_build_exec_policy` (`exec_guard.py:894-917`): wall timeout kept, network **kept**
  (package-registry fetch), **no sandbox**.
- `runtime_server_exec_policy` (`exec_guard.py:960-1000`): `wall_timeout_seconds=None` (Amendment
  F085 D8: must not hold a clock), `output_cap_bytes=None`, **no sandbox**.
- (the CLI-provider seams, `_cli_exec_policy`/`_stream_exec_policy`, are not one of these six; see
  §3 — they are the seventh, deliberately un-denied, policy builder in `pingpong_provider.py`.)

`docs/system/exec-guard-limitations-v0.md` already declares unenforced: the network posture is a
PROXY posture, defeated by any binary that ignores proxy env vars or uses raw sockets/DNS/a unix
socket (`exec-guard-limitations-v0.md:16-33`); only `builder`, `test`, `dod-process` default-deny of
the six guarded classes, and `git` (24 call sites), `packaging` (11) and `other` (8) are not
stage-1 classes at all and still spawn unsupervised (`:37-51`); an allowlist bounds the parent only,
never a CPython child's own `LC_CTYPE` locale coercion (`:53-57`); an output cap bounds only what
the guard reads through its own pipe, never a file a child writes itself (`:60-66`);
`address_space_bytes` is enforced but never classified (`:68-74`); there is no filesystem fence
(`:76-79`); a stream still blocked at the grace deadline leaks one fd and one daemon thread
(`:81-86`).

Tests pinning this: `tests/orchestration/test_exec_guard.py` (56 `test_*` functions) cover the
rlimits, the env scrub and floor, every `*_exec_policy` factory's own row (deny/keep network,
wall-timeout presence, allowlist membership), the seam translations
(`run_guarded_test_command`/`_dod_process_command`/`_runtime_build_command`), and the network
proxy posture including the loopback exemption.

## 2. The tool sandbox

`packages/orchestration/tool_sandbox.py` (613 lines, `wc -l`; no structure-ledger row). `SandboxSpec`
(`tool_sandbox.py:192-266`) builds one `bwrap` argv: `--unshare-all` (every namespace),
`--die-with-parent`, `--new-session`; read-only `_SYSTEM_DIRS` (`/usr`,`/bin`,`/sbin`,`/lib*`,`/nix`,
`tool_sandbox.py:60`) and a short `_ETC_ENTRIES` list (`:62-65`); the workspace is the one `--bind`
(writable, `:245`); `/tmp` is `--tmpfs /tmp` and `HOME` is a `--dir` under it (`SANDBOX_HOME =
"/tmp/home"`, `:54,232`) — both private and memory-backed; a git worktree's metadata is exposed
read-only only when its `gitdir` link points back at the workspace (`_git_metadata_dirs`,
`:110-133`); the environment is `--clearenv` plus an explicit `--setenv` per key (`:262-264`), never
the parent's whole environment. `require_sandbox` (`:272-295`) refuses on a non-Linux `sys.platform`
(`:277-279`), a missing `bwrap` binary, or a failed probe run — three distinct `SandboxUnavailable`
states (`SANDBOX_MISSING`/`SANDBOX_UNSUPPORTED`/`SANDBOX_FAILED`, `:48-51`) — and never a silent
unconfined fallback. `sandbox_relay.py` (79 lines) is the stdlib-only, Remedy-import-free script
that runs first inside the sandbox (per its own docstring, `sandbox_relay.py:1-13`), listens on
`127.0.0.1:11434` and carries every byte to the host's `ProviderRelay` Unix socket
(`tool_sandbox.py:349-440`), which admits only `POST /v1/chat/completions` and `GET /v1/models`
(`admit_provider_request`, `:313-333`) and 403s everything else.

Callers: `packages/orchestration/pi_provider.py` (the only call to `provider_sandbox`,
`pi_provider.py:688`) and `exec_guard.py` itself (`plan_child_spawn`'s `policy.sandbox.wrap(...)`,
`exec_guard.py:477`, used when `test_command_exec_policy`/`dod_process_exec_policy` set `sandbox=`).
No other module calls `SandboxSpec(` directly (checked with `rg -n "SandboxSpec\(" packages apps
scripts`, three hits: `pi_provider.py`, `sandbox_relay.py`'s own docstring reference, `exec_guard.py`,
`tool_sandbox.py` itself).

`bwrap --version` (run via a `python3 -I` subprocess, this machine): `bubblewrap 0.6.1`. `bwrap
--help` lists `--tmpfs DEST` with **no size argument** — this version of bwrap has no flag to cap a
tmpfs mount's size; `docs/system/tool-sandbox-v1.md:172` already states `/tmp` and `HOME` inside
"are memory-backed with the kernel's default tmpfs size." A `tmp_quota_mb` dimension (feature file's
design) has no bwrap-level enforcement mechanism in this version; it would need either an
out-of-band size-capped mount Remedy builds itself or a later bwrap version, neither of which
exists in the tree today (UNVERIFIED whether a later version adds a `--tmpfs` size option; this
machine's `bwrap --help` is the only evidence read).

Refusal states and self-test: `sandbox_self_test()` (`tool_sandbox.py:577-612`) runs 11 named checks
(`_SELF_TEST_NAMES`, `:524-534`) against synthetic files, feeding `remedy doctor health` and `remedy
worker doctor` (`tool-sandbox-v1.md:132-140`). Tests: `tests/orchestration/test_tool_sandbox.py` (19
`test_*` functions) run against the real kernel boundary — workspace writability, secret/other-repo
unreachability, no host/external network, the relay's admit-list, detached-child cleanup, cancel
behaviour, a missing/broken sandbox refusing cleanly, the self-test itself, and a real Pi harness run.

## 3. The worker spawn paths

Four provider classes a role can be built with (`role_provider_factory.create_role_provider`,
`role_provider_factory.py:28-127`; `create_provider`, `pingpong_provider.py:1556-1570`):

| Class | Spawn point | `ExecGuardPolicy`? | Sandbox? | Enforced today |
|---|---|---|---|---|
| `claude-cli` | `_guarded_cli_run`→`run_guarded`, `pingpong_provider.py:854-876`, policy from `_cli_exec_policy` (`:811-823`)/`_stream_exec_policy` (`:826-839`) | yes, but `cpu_seconds`/`address_space_bytes`/`open_files` all `None`, `deny_network` unset | no `sandbox=` field set | wall timeout (non-stream call only), `cwd` pin, zero core, F152's declared/cleaned env (`adapter_child_env`) |
| `claude` (Anthropic API) | `ClaudeProvider._get_client`, `pingpong_provider.py:370-379`, the `anthropic` SDK over HTTPS | none — no child process | none | only the SDK's own request semantics; no guard, no cap, no limit Remedy sets |
| `ollama` | `OllamaPingPongProvider`, `pingpong_provider_ollama.py:33-123`, `ollama.Client(host=..., timeout=float(timeout_sec))` (`:123`) | none — no child process | none | the client's own request `timeout_sec` only |
| `pi` | `make_pi_provider`→`PiProvider.call`, `pi_provider.py:687-696`, `run_guarded([*relay_argv, *argv], ExecGuardPolicy(...))` inside `provider_sandbox(...)` | yes: `wall_timeout_seconds`, `output_cap_bytes=PI_STDOUT_CAP_BYTES` (64 MiB, `pi_provider.py:70`), `core_file_bytes=0`, `env=pi_child_env()` (`:411`) + `_PI_ENV_ALLOWLIST` (`:96`); `cpu_seconds`/`address_space_bytes`/`open_files` still `None` | **yes**, `sandbox=sandbox` from `provider_sandbox` (bwrap) | wall timeout, stdout cap, cwd pin, zero core, the whole bwrap boundary (§2), the model-endpoint relay admit-list, a loop-turn/token watchdog (`PiLoopWatch`) |

Plainly, per class, today: `claude-cli` has a wall deadline and a cleaned environment but **no**
filesystem fence beyond its `cwd` pin and **no** network denial. `claude` and `ollama` are plain
network clients with **no** process-level containment of any kind — nothing to contain, since
neither spawns a child. `pi` alone runs inside the full kernel boundary (§2): private filesystem,
network and process namespaces, with resource rlimits for CPU/memory/open-files still unset exactly
like every other class (the one stated reason, `exec_guard.py:601-610`, applies to all of them). A
fifth name, `fake` (`pingpong_provider.py:1558-1560`), is a deliverable test double with no process
and no network at all.

## 4. The adapter contract

`packages/contracts/adapter_contract.py`: `WorkerIsolation` (`:130-162`) is the one declared shape —
`method` (one of `ISOLATION_METHODS = ("tool_flag","clean_env","sandbox_reinforced")`, `:63`),
`adr_ref` (must match `docs/adr/NNNN-slug.md`, `_ADR_REF_PATTERN`, `:67`), `tool_args`,
`env_allowlist`, `throwaway_home`, `applies`. `WorkerAdapter` (`:165-198`) is a `runtime_checkable`
Protocol with `isolation()` (`:195-198`) among its six methods; `AdapterInvocation` is the sum type
`CliInvocation | HttpInvocation` (`:93-111,123`) — an adapter may declare an HTTP call, but no
adapter does today.

`packages/providers/adapters/adapter_registry.py`: `WORKER_ADAPTERS_BY_REF = {"claude-cli":
ClaudeCliReferenceAdapter}` (`:16-18`) — the **only** registered adapter.
`packages/providers/adapters/claude_cli_reference.py`'s `isolation()` (`:170-177`) declares method
`tool_flag`, `adr_ref="docs/adr/0002-claude-cli-worker-isolation.md"`, `tool_args=("--setting-sources",
"project,local","--strict-mcp-config")` (`:39`), `env_allowlist` naming the shell/process names,
`ANTHROPIC_API_KEY` and both proxy spellings (`:43-47`), `applies` off when the operator's own
`claude_cli.customizations` flag is set. The adapter never names a network endpoint explicitly — the
underlying `claude` binary's own reach (Anthropic's API) is outside the contract's declared surface,
since only a `CliInvocation` is built. No other adapter exists to ask "which endpoint", so this is
the whole answer today.

`packages/contracts/adapter_conformance_kit.py`'s `_check_isolation` (`:266-291`) refuses an
`isolation()` that is not a `WorkerIsolation`, whose `adr_ref` record is missing or has no `>
**Status:` line (`has_isolation_record`, `worker_isolation.py:77-82`), or whose built command line
drops its own declared `tool_args`. The kit's "transport" dimension (per
`docs/system/worker-adapter-contract-v2.md:54-61`) refuses any process/network/retry/timeout/sleep
spelling anywhere in an adapter's own class or its module's call-by-name functions.
`docs/system/worker-adapter-contract-v2.md:115-144` is the fuller narrative; `:116-123` restates the
declaration, `:137-144` restates the kit and doctor checks.

Tests: `tests/orchestration/test_worker_isolation.py`, `tests/contracts/test_adapter_contract.py`,
`tests/contracts/test_adapter_conformance_kit.py`, `tests/contracts/test_claude_cli_reference.py`.

## 5. Configuration and the policy minimum

Loader: `packages/orchestration/config.py`. Precedence stated at `config.py:5-7`: environment, then
project `./remedy.toml` (`_DEFAULT_PROJECT_PATH`, `:1119`), then user
`~/.config/remedy/remedy.toml` (`_DEFAULT_USER_PATH`, `:1120`), then built-in default.
`RemedyConfig` (`:1271`), built by `get_config()` (`:1384`); `project_raw`/`project_flat` read at
`:1347-1350`. Tests: `tests/orchestration/test_config.py`, `tests/cli/test_config_cmd.py`.

`rg -n "policy_pack" .` (whole repo) returns **zero** hits — no "policy pack" mechanism exists.
`policy_packs` (plural) appears only in `docs/roadmap/ROADMAP.md:179` and `docs/roadmap/features/
T9_F172.md` — a **different**, unbuilt feature (enterprise policy packs), unrelated to F162's
"policy minimum." `rg -n "tighten" packages apps` returns one hit outside docs,
`packages/orchestration/run_manifest.py:1205` ("a completed episode's tightened sets gain
`vetoed`") — unrelated to profiles. **No tighten-only comparator and no project-tightening-of-a-
profile mechanism exists anywhere in code today.**

The air-gap feature naming F162: `docs/roadmap/features/T9_F173.md` ("Air-gap mode"), which depends
on F162 (`:2`) and states "local profiles (F162) express net=deny and localhost allowlists" (`:24`)
as its own assumption of what F162 will provide — not yet true. Per AGENTS.md's Do-not-touch, this
file is read, not changed.

## 6. Platform reach

This machine (`python3 -I -c "import sys,os;print(sys.platform,os.name)"`): `sys.platform == "linux"`,
`os.name == "posix"`. VERIFIED. `resource` module's `RLIMIT_*` names on this machine (same command,
`dir(resource)`): `AS, CORE, CPU, DATA, FSIZE, MEMLOCK, MSGQUEUE, NICE, NOFILE, OFILE, RSS, RTPRIO,
RTTIME, SIGPENDING, STACK` — every constant `_RLIMIT_ATTRS` (`exec_guard.py:94-99`) uses (`CPU`,
`AS`, `NOFILE`, `CORE`) is present. VERIFIED.

`exec_guard.py:70` does `import resource` unconditionally, with no `try`/`except` and no platform
branch anywhere in the file (`rg -n "sys.platform|os.name" exec_guard.py` — zero hits). The
`resource` module is POSIX-only per the standard library's own documented availability. UNVERIFIED
(inferred, not tested on this machine — there is no Windows host here): on native Windows this
`import` would raise before any class in the module loads, which would make the whole orchestration
layer that imports `exec_guard` unimportable, not merely the sandboxed Pi path.
`tool_sandbox.py:277-279` is the file's only platform branch: `require_sandbox` raises
`SandboxUnavailable(SANDBOX_UNSUPPORTED, ...)` for any `sys.platform` not starting with `"linux"`.
VERIFIED from code. `docs/system/tool-sandbox-v1.md:142-149`'s platform table: Linux supported and
tested (Pop!_OS 22.04, kernel 6.17, bwrap 0.6.1 — matches this machine's own `bwrap --version`
reading in §2); Ubuntu 23.10+ needs an AppArmor profile, not tested; Windows via WSL2 only, not
tested; macOS has no supported backend at all. VERIFIED (doc text, not independently re-tested
here). Because `resource` is POSIX, macOS can still import `exec_guard` and get real rlimits — only
the bwrap boundary is Linux-only there.

## 7. Container tools

`docker --version` (via `python3 -I` subprocess, this machine): exit 0, `Docker version 29.1.3,
build 29.1.3-0ubuntu3~22.04.2`. `podman --version`: `FileNotFoundError` — podman is not installed.
`docker info`: exit 0 (the daemon is reachable from this account). All three VERIFIED by command
output on this machine; neither tells anything about the operator's eventual deployment host.

Existing container-adjacent code (`rg -n -i "docker|podman" packages apps scripts`, 11 files):
`packages/providers/docker_runtime/__init__.py` (15 lines) is a **reserved, empty namespace** —
its own docstring: "Reserved namespace — no implementation in this step... Future layer: Docker
container runtime backend (planned Step 40+)." Every other hit is unrelated to a worker sandbox:
project-file classifiers that recognize a `Dockerfile`/`docker-compose.yml` as a project artifact
(`context_inspector.py:65`, `task_deliverables.py:61`, `study.py:337`, `do_lane.py:75`); a
dangerous-command detector that flags `docker run --privileged` (`command_discovery.py:165,174`);
negative docstring mentions ("no ... Docker ... execution", `brain_viewer.py:15`,
`brain_detail.py:10`, `runtime_cmd.py:33`); and `scripts/serve/container-entrypoint.sh`, which runs
**Remedy's own served application** inside a container (the `runtime-server` class, §1), not a
worker sandbox. **No code implements a container runner for a worker call today.**

`pyproject.toml:15-18`, `[project.optional-dependencies]`: `dev`, `ollama`, `anthropic` — no
`docker`/`podman` extra is declared.

## 8. Evidence and doctor

Per-run evidence precedent: `worker_isolation.py`'s `record_worker_isolation` (`:211-223`) appends
one JSON line, `{"role","provider","model", **record}`, to `WORKER_ISOLATION_FILENAME =
"worker_isolation.jsonl"` (`:34`) under the run's evidence dir — one line per claude-cli provider
**build**, never per call, written only from `role_provider_factory.create_role_provider`
(`role_provider_factory.py:88-89`). A `worker_sandbox` record would sit beside it the same way, from
the same seam, shaped like `worker_isolation_record` (`worker_isolation.py:193-206`).

`apps/cli/commands/worker.py`'s `_cmd_worker_doctor` (`:248-321`): builds a flat `checks` list via a
local `_check(name, ok, detail)` closure (`:266-267`); for each `available` spec it probes the
executable with `shutil.which` (`:278-281`) and, only once that executable is found and the spec
names an `adapter_ref`, calls `isolation_doctor_checks(adapter, provider_id=...)` (`:287-290`,
defined `worker_isolation.py:100-173`), which appends four checks —
`isolation_<id>_declaration/_record/_home/_flags`. `docs/system/tool-sandbox-v1.md:132-140`
documents a separate, already-existing `tool_sandbox`-named doctor line (`sandbox_self_test()`,
`tool_sandbox.py:577-612`) with states `ready`/`missing_prerequisite`/`unsupported_configuration`/
`failed_self_test`. A `worker_sandbox` doctor check would follow the four-isolation-checks pattern:
a new call appended inside the same `if found and spec.adapter_ref:` block
(`apps/cli/commands/worker.py:284`), gated on the adapter's (future) sandbox declaration the way
isolation is gated on `declared_isolation`.

## 9. Guards, ledgers and the walk precedent

`tests/orchestration/import_reachability_allowlist.txt` is GENERATED (never hand-typed, file header
`:1-4`) by `tests/orchestration/test_import_reachability.py`'s `reachable_closure` over six
`ENTRY_POINTS` (`test_import_reachability.py:42-48`: `do_cmd`, `job`, `mission_cmd`,
`self_use_runner`, `teacher_cmd`, `serve_http_handler`). It already lists `exec_guard` (`:223`),
`pingpong_provider`/`_call`/`_fake`/`_ollama` (`:319-322`) and `tool_sandbox` (`:438`) as reachable.
A new `sandbox_profiles.py` module must be imported from something inside that closure, or the
generated allowlist (and `tests/test_no_orphan_modules.py`'s `test_no_module_is_an_orphan`,
`:250`) will flag it — the allowlist's own "allowed unwired" escape
(`test_every_allowed_unwired_entry_carries_a_reason`, `:295`) requires a stated reason, not a free pass.

`docs/system/structure-ledger-v1.md` rows a T001-T003 round would touch: `exec_guard.py`'s
`run_guarded`, 122 lines, row at `:410`; `pingpong_provider.py`'s file row, 1570 lines, at `:475`,
plus its `ClaudeCliProvider._call_reviewer_structured` (130 lines, `:396`) and `._review_impl` (103
lines, `:453`). `tool_sandbox.py` (613 lines) has **no row** — under both the 100-line function and
1000-line file thresholds today (`rg -n "exec_guard.py|tool_sandbox.py|pingpong_provider.py"
structure-ledger-v1.md`, three files, no `tool_sandbox.py` hit). Growing any ledgered function past
its row, or `tool_sandbox.py` past 1000 lines, needs the DECISION the ledger's "The rule"
(`:33-36`) requires; `tests/test_structure_ratchet.py` pins row count and line sums and never lets
either rise.

`tests/workers/` does **not exist** (`test -d tests/workers` → absent) — the feature file's
suggested `tests/workers/test_sandbox_profiles.py` (`T8_F162.md:86`) names a directory nothing has
created yet.

The F043 audit pattern the feature file names (`T8_F162.md:49`, "the F043 audit pattern"):
`docs/roadmap/features/T5_F043.md`'s T002, built as `apps/ui/src/api/terminologyAudit.ts` +
`components/term/termAudit.test.ts` (`T5_F043.md:110-115`) — a two-direction walk: every rendered
`data-term` must be a catalog key, and every catalog key must be used somewhere, with drift
fixtures proving both directions fail red. This is a TypeScript/DOM precedent; F162's honesty-doc
row-to-test walk (a markdown table, not rendered markup) would need its own, analogous two-direction
reader rather than reusing this one directly.

ADR convention: `docs/adr/NNNN-slug.md`, four-digit number (`_ADR_REF_PATTERN`,
`adapter_contract.py:67`), header `# ADR-NNNN — <title>` (`docs/adr/0002-claude-cli-worker-isolation.md:1`),
a line starting `> **Status:` that `has_isolation_record` reads literally (`worker_isolation.py:77-82`).
Two ADRs exist today: `0001-raise-cycle-safety-cap.md` and
`0002-claude-cli-worker-isolation.md` — a T003 container-stage ADR would be `0003-*`.

`docs/README.md` indexes a doc twice: a one-row entry in the quick-find table near the top (e.g.
`:43-44` for the exec guard and tool-sandbox pages, `:90` for the structure ledger) and a fuller
per-category table with a one-line description (`:122-123`, `:169`), plus a dedicated "Architecture
Decision Records" section header (`:240`) that ADRs register under. A new `sandbox-model.md` (which
does not exist yet — `test -f docs/system/sandbox-model.md` → absent) and a new ADR would need rows
in both tables.

## 10. Names and a draft — PROPOSAL for DECISION F162 D2, not a decision

Vocabulary grep (`rg` over the whole repo, excluding `.git`), read before any code is authored:
`sandbox_profiles` — not free: `docs/roadmap/ROADMAP.md:177`, `T8_F162.md:6,86` (this feature's own
planning prose only, no code). `SandboxProfile` — **zero hits**, free. `worker_sandbox` — one hit,
`T8_F162.md:42` (planning prose only), otherwise free. `tmp_quota` — one hit, `T8_F162.md:37`
(planning prose), otherwise free. `sandbox-model` — two hits, `T16_F237.md:34` and `T8_F162.md:11`
(both reference the doc by name; the file itself is absent, confirmed above), otherwise free.

A proposed shape, for DECISION F162 D2 to accept, amend or reject — nothing here binds T001:

- **Home**: a new `packages/orchestration/sandbox_profiles.py` (schema, built-ins, the tighten-only
  comparator), named exactly as `ROADMAP.md:177`'s own example list already spells it; wired into
  the import-reachability closure (§9) rather than left an orphan.
- **Per-dimension comparator, mapped to what enforces it today** (so a profile never names a limit
  nothing applies):
  - `fs_scope`: enforced only inside the bwrap boundary (§2, pi/test/dod-process classes);
    `claude-cli`/`claude`/`ollama` have no filesystem fence beyond a `cwd` pin (§3) — a real gap,
    not a wording gap.
  - `net` (`deny`/allowlist): `exec_guard`'s proxy posture for guarded classes (weak — defeated by a
    binary that ignores proxy vars, `exec-guard-limitations-v0.md:16-33`) or bwrap's private netns +
    relay admit-list for Pi (strong, but scoped to Pi/test/dod-process by DECISION amend1016sb
    D1/D4) — `claude`/`claude`-API/`ollama` have neither today.
  - `ulimits` (`cpu_s`, `mem_mb`, `nofile`): the wiring already exists (`_plan_rlimits`,
    `_RLIMIT_ATTRS`, §1/§6) end to end; every policy factory simply passes `None` today, for the
    one stated reason (`exec_guard.py:601-610`) that no per-project value is measured yet — T002's
    gap is VALUES, not plumbing.
  - `allowed_binaries`: no existing mechanism names a binary; the closest proxy, bwrap's
    PATH-derived toolchain-directory allowlist (`tool_sandbox.py:136-160`), allows directories, not
    binaries by name.
  - `tmp_quota_mb`: no enforcement exists in this bwrap version (§2) — a real gap.
- **Evidence**: a `worker_sandbox` record beside `worker_isolation.jsonl` (§8), written by the same
  per-build seam.
- **Where the feature file's design does not match the tree** (marked as such, not decided):
  (a) the design's "`net deny` maps to the no-network posture" undersells that only `builder`,
  `test`, `dod-process` of exec_guard's six classes default-deny, and that posture is a proxy, never
  kernel, outside bwrap (§1); (b) "stage 2's container runner ... same profile TOML compiles to
  container flags" presumes detection/compilation code that does not exist beyond the reserved empty
  `docker_runtime` namespace (§7); (c) the suggested test path `tests/workers/test_sandbox_profiles.py`
  names a directory that does not exist (§9); (d) the design never mentions `tool_sandbox.py`
  explicitly even though it is the ONLY existing per-process kernel fence in the tree — any profile
  schema that ignores it would duplicate, not extend, the Do-not-touch's "exec-guard internals
  extended, not forked."
