# F152 inventory — every place a worker's environment and configuration reach a run

Read-only findings pass at `ef2b85f83`, written for review before any T001 code. Every factual
sentence names its `path:line`, or the command whose captured output it reads. Nothing here
decides a shape; §9 is explicitly a proposal.

## 1. The reserved slot

`WorkerAdapter.isolation(self) -> None` is declared at
`packages/contracts/adapter_contract.py:148-150`: "Reserved for F152; returns `None` until F152
shapes an isolation declaration." The only concrete adapter today, `ClaudeCliReferenceAdapter`,
answers it at `packages/providers/adapters/claude_cli_reference.py:146-148` — "reserved for F152
(D2 (3)) — every adapter answers `None` until that feature shapes it" — also returning `None`.

The conformance kit lists `"isolation"` as the sixth of seven `CONFORMANCE_DIMENSIONS`
(`packages/contracts/adapter_conformance_kit.py:34-36`) and checks it with `_check_isolation`
(lines 264-270): it calls `adapter.isolation()` and fails the dimension iff the result is not
`None` ("isolation() must return None, got …"). `test_conformance_dimensions_is_exactly_the_seven_in_order`
(`tests/contracts/test_adapter_conformance_kit.py:595-597`) pins the seven names and their order.

The test that actually PINS today's `None` contract — it reds on a non-`None` answer — is
`test_broken_case_fails_exactly_its_own_check` (`tests/contracts/test_adapter_conformance_kit.py:572`),
parametrized at line 561 with `_BrokenIsolationNotNoneToy` (lines 470-474, `isolation()` returns
`{"sandbox": "none"}`) and the expected failure fragment `"isolation() must return None"`. The
conforming path is exercised by `test_conforming_cli_toy_is_fully_conformant` /
`..._http_toy_..._conformant` (lines 163, 167), whose toys' `isolation()` (lines 82, 124) both
return `None` and must produce zero failures. `tests/contracts/test_adapter_contract.py:95` and
`:122` give two more toys with `isolation()` returning `None`, used only to exercise the
`WorkerAdapter` `runtime_checkable` `Protocol`'s member-presence check (`:126`, `:130`) — that
check tests member PRESENCE, not the return value, so it does not itself pin `None`.

`docs/system/worker-adapter-contract-v2.md:41` carries the row: `` `isolation()` | reserved for
the worker config isolation feature; `None` until that feature shapes it ``.

A bare grep for the word `isolation` under `packages apps tests` returns ~80 files, almost all of
them a different sense of the word — worktree isolation, test isolation. Narrowing to the literal
call `isolation(` leaves exactly the six files named above (the two production definitions, the
kit's check and name, and the two test files' toy methods) plus the conformance kit's `isolation`
string in `CONFORMANCE_DIMENSIONS`/the dimension dispatch table (`:384`).

## 2. The invocation seam

The seam is NOT a single function; it is a chain, and the environment decision is made once, deep
in it, never at the adapter:

1. `ClaudeCliProvider._adapter_argv` (`packages/orchestration/pingpong_provider.py:1056-1060`) —
   "every call's command line is the installed claude-cli adapter's (DECISION F315 D2)" — calls
2. `adapter_cli_argv` (`packages/orchestration/worker_adapter_slot.py:48-59`), which asks the
   installed factory for the adapter and calls `adapter.build_invocation(role, (prompt,), options)`.
3. For `claude-cli` this reaches `ClaudeCliReferenceAdapter.build_invocation`
   (`packages/providers/adapters/claude_cli_reference.py:91-102`), which "WRAPS today's claude-cli
   call path" (`:3`) by calling `build_claude_cli_args` (`packages/orchestration/claude_cli_command.py:66-113`,
   imported at `claude_cli_reference.py:27`) — this is the function that builds the ARGV
   (`-p`, `--output-format`, `--model`, `--json-schema`, `--resume`, `--allowedTools` /
   `--dangerously-skip-permissions`, `--safe-mode`/`--tools`). It returns a `CliInvocation`
   (`adapter_contract.py:84-88`); the sum type also carries `HttpInvocation` (`:91-102`) for
   Ollama's HTTP calls (`packages/orchestration/pingpong_provider_ollama.py:33`, which never
   spawns a process — no `subprocess`/`Popen`/`env=` token appears in that file).
4. The resulting argv is spawned by `_guarded_cli_run` (`pingpong_provider.py:854-876`), the
   provider's "single spawn point", which calls `run_guarded` (`packages/orchestration/exec_guard.py:455`)
   under a policy built by `_cli_exec_policy` (non-streamed, `:811-822`) or `_stream_exec_policy`
   (streamed, `:825-839`).

**Both policies set neither `env=` nor `env_allowlist=`.** Their own docstrings say why, in the
same words twice: *"`env_allowlist` stays `None` for a kindred reason: the child is the operator's
authenticated `claude` CLI and reads its credentials from the inherited environment. Both are
stage-1 gaps, owed to T003's limitations document."* (`:816-819`, repeated `:833-837`). With
`env=None` and `env_allowlist=None`, `plan_child_spawn` (`exec_guard.py:365-404`) leaves
`child_env = policy.env` i.e. `None`, which `Popen` reads as "inherit the parent's environment
whole" (`:383-387`, and the module docstring at `:23-27`: *"No environment scrubbing UNLESS the
policy asks for it… what a child inherits is that caller's decision, never this module's
default."*). Neither policy sets `sandbox=` either, so `ClaudeCliProvider` never runs through
`tool_sandbox` (§3). Neither policy overrides `HOME`; `ClaudeCliProvider.__init__`
(`pingpong_provider.py:887-919`) carries no `home`/`HOME` field at all.

**Plainly: every environment variable of the operator's own shell reaches a claude-cli worker
call today** — nothing is stripped, nothing is allowlisted, and the claude CLI's own config/home
discovery (§4) therefore runs exactly as it would for the operator typing `claude -p` by hand. The
only thing pinned is `cwd` (`self._cwd`, passed to both policies).

`pingpong_provider_ollama.py` (HTTP, no child process) and `role_provider_factory.create_role_provider`
(`packages/orchestration/role_provider_factory.py:26`, a provider-selecting factory with no
subprocess/env code of its own) carry nothing relevant to this seam. `pi_provider.py`'s own seam is
analyzed in §3, because it is the one existing example of a worker call that DOES isolate.

## 3. The environment machinery that exists

- **`exec_guard.py`** (F085 stage 1). `FORBIDDEN_ENV_KEYS` (`:104-110`) — API keys, proxy vars,
  cloud creds — is dropped even when a caller's allowlist names it; it is the one floor every
  allowlist obeys (`scrub_child_env`, `:163-171`). `TEST_COMMAND_ENV_ALLOWLIST` (`:117-122`) is
  the `test`-class allowlist (locale, PATH, temp dirs, `VIRTUAL_ENV`), consumed by
  `run_guarded_test_command` (`:642`, called from `packages/orchestration/test_runner.py:209` via
  the comment at `test_runner.py:24-28`). `DOD_PROCESS_ENV_ALLOWLIST`/`RUNTIME_*_ALLOWLIST` (near
  `:736`, `:813-814`, `:916`, `:998-999`) are the DoD-process and runtime-server/build classes —
  unrelated provider calls, each with its own tests (`tests/orchestration/test_exec_guard*.py`
  pattern, not read in detail here as out of scope for a worker call).
- **`tool_sandbox.py` / `SANDBOX_HOME`** (amend1016sb D1). `SANDBOX_HOME = "/tmp/home"`
  (`:54`). `SandboxSpec.wrap` (`:214-266`) builds a Bubblewrap argv whose environment is "EXPLICIT:
  the caller's allowlisted one … with the sandbox's own home and temp directory" (`:251-253`):
  `inner.update({"HOME": SANDBOX_HOME, "TMPDIR": "/tmp", ...})` (`:256`), then `--clearenv` plus
  one `--setenv` per key (`:262-264`). This is, today, exactly the "cleaned env allowlist plus a
  throwaway HOME" shape T8_F152.md's Design section asks for — already built, already tested
  (`tests/orchestration/test_tool_sandbox.py`), but wired only to the `test`/`dod-process` classes
  and to Pi (next bullet), never to `ClaudeCliProvider`.
- **`pi_provider.py`'s `_PI_ENV_ALLOWLIST`** (`:96-97`): `PATH, HOME, LANG, LC_ALL, LC_CTYPE,
  LOGNAME, SHELL, TMPDIR, TZ, USER, TERM`. Built by operator amendment amend1014b (module
  docstring, `:1`) and amend1016sb D1 (`:9-16`), whose own prose is the clearest existing
  statement of F152's goal applied to a DIFFERENT adapter: *"Remedy also does not copy the
  operator's Pi settings, credentials, extensions, MCP servers, skills, prompt templates or
  themes into a worker: the per-call agent directory holds Remedy's `models.json` and
  `settings.json` only"* (`:15-16`). `pi_child_env` (`:411-416`) builds the allowlisted env plus
  Pi's own switches; the one call site, `_call_streamed` (`:690-696`), passes it as `env=` AND
  passes `env_allowlist=_PI_ENV_ALLOWLIST + (...)` to `ExecGuardPolicy`, with `sandbox=sandbox`
  (the `provider_sandbox` context manager, `:688`). Because `sandbox` is set, `SandboxSpec.wrap`
  then OVERWRITES `HOME` to `SANDBOX_HOME` regardless of what `_PI_ENV_ALLOWLIST` let through
  (`tool_sandbox.py:256`) — the allowlist's own `HOME` entry is in practice moot once sandboxed;
  the real throwaway-HOME mechanism is the sandbox's `--clearenv`/`--setenv`, not the allowlist.
  Tests: `tests/orchestration/test_pi_timeouts.py`, `tests/orchestration/test_tool_sandbox.py`
  (sandbox side).
- **`test_execution_service.py`** (`_build_safe_env`, `:265-289`, `_ALWAYS_KEEP` `:255-262`,
  `_SAFE_ENV_PREFIXES` `:248-253`) and **`test_runner.py`** (consumes
  `TEST_COMMAND_ENV_ALLOWLIST` via `run_guarded_test_command`) both allowlist for running the
  REPOSITORY'S OWN test suite inside a job workspace — a different purpose (letting a project's
  build toolchain see `GOPATH`/`CARGO_HOME`/`XDG_*`), not a worker-model call.

**Which can the invocation seam call without breaking an import rule?** `exec_guard.py` and
`tool_sandbox.py` are already imported by `pingpong_provider.py`/`pi_provider.py` respectively —
calling either from `_cli_exec_policy`/`_stream_exec_policy` breaks no rule; the contract's one
import fence, `FORBIDDEN_PREFIX = "packages.providers.adapters"`
(`tests/contracts/test_adapter_import_guard.py:24`, asserted for orchestration by
`test_neither_guarded_tree_imports_a_concrete_adapter`, `:68`), is about adapters, not about
exec_guard/tool_sandbox. Reusing `pi_provider._PI_ENV_ALLOWLIST` or
`test_execution_service._ALWAYS_KEEP` directly would not break that fence either, but both are
private (`_`-prefixed) constants of another call class, built for a different purpose (Pi's own
switches; a project's build toolchain) — reuse would be a naming/semantic conflation, not an
import violation. Nothing under `packages apps` is actually FORBIDDEN to the seam by
`tests/orchestration/test_import_reachability.py`'s closure; a genuinely NEW module (§8) is the
one thing that needs an explicit addition there.

## 4. The claude command line's configuration surfaces

**Deviation, stated plainly**: this session's sandbox refused every attempt to run `claude`
locally — `claude --version`, `claude --help`, even `command -v claude` and `ls` of
`~/.claude` all answered "requires approval" / "blocked" with no channel for this worker to grant
it. Every VERIFIED claim below is therefore read from the cached capture at
`.agent/f302_claude_help.txt` (its own header: `=== claude --version (exit 0) ===`,
`=== claude --help (exit 0) ===`), not a fresh run this round — a deviation from the block's
"run locally", recorded again in the handback.

VERIFIED, `.agent/f302_claude_help.txt:1-2`: version `2.1.296 (Claude Code)`.

Configuration-selecting flags, VERIFIED from the help text:
- `--setting-sources <sources>` (`:228-229`) — "Comma-separated list of setting sources to load
  (user, project, local)" — SELECTS which configuration layers load.
- `--settings <file-or-json>` (`:230-231`) — ADDS a settings file or inline JSON.
- `--mcp-config <configs...>` (`:135-136`) — ADDS MCP servers from files/strings.
- `--strict-mcp-config` (`:232-233`) — SUPPRESSES every MCP source except `--mcp-config`'s own.
- `--safe-mode` (`:215-225`) — SUPPRESSES CLAUDE.md, skills, plugins, hooks, MCP servers, custom
  commands/agents, output styles, workflows, themes, keybindings; "Admin-managed (policy) settings
  still apply"; sets env var `CLAUDE_CODE_SAFE_MODE=1`. Already the switch Remedy's own
  `claude_cli_launch_switches` appends by default (`claude_cli_command.py:46-59`, unless
  `claude_cli.customizations` is true) — so every claude-cli worker call already requests this
  SUPPRESSION of the operator's own customizations, independent of F152.
  `_claude_cli_flag`/`claude_cli_launch_switches` (`:31-59`).
- `--bare` (`:44-61`) — SUPPRESSES hooks, LSP, plugin sync, attribution, auto-memory, background
  prefetches, keychain reads, CLAUDE.md auto-discovery; sets `CLAUDE_CODE_SIMPLE=1`; states "Anthropic
  auth is strictly `ANTHROPIC_API_KEY` or `apiKeyHelper` via `--settings` (OAuth and keychain are
  never read)" — the clearest statement in the captured text of where auth normally comes from
  (OAuth / keychain / `ANTHROPIC_API_KEY` / `apiKeyHelper`) and that `--bare` narrows it.
- `--restricted` (`:197-211`) — "ignores user, project and local settings files (managed settings
  and `--settings` still apply; add `--strict-mcp-config` to skip MCP servers too)".
- `--add-dir <directories...>` (`:13-14`) — adds tool-access directories, and per `--bare`'s own
  prose also names CLAUDE.md directories.
- `--disable-slash-commands` (`:83`) — disables all skills.
- `--plugin-dir`/`--plugin-url` (`:165-172`) — load a plugin for the session only.
- `--agent`/`--agents` (`:15-21`) — override the `agent` setting / define custom agents inline.
- `--no-session-persistence` (`:145-147`) — sessions are not written to disk at all (print mode only).
- `doctor` subcommand (`:278-282`) — "Reads settings files in the current directory without a
  trust prompt" — the CLI's OWN doctor, distinct from Remedy's (§7).

No environment variable that SELECTS, ADDS or SUPPRESSES configuration appears anywhere in the
captured `--help` text; the only env vars named are two OUTPUTS the flags themselves set
(`CLAUDE_CODE_SAFE_MODE`, `CLAUDE_CODE_SIMPLE`) and `ANTHROPIC_API_KEY` as one accepted auth
input. A "no-user-config" env var or a "config-dir" env var, if one exists, is UNVERIFIED —
absent from this text, and this session could not probe further.

Filesystem existence only (python `os.path.exists`/`os.listdir`, no file opened, no content read,
per the block's rule): `~/.claude` exists (a directory) and `~/.claude.json` exists;
`~/.config/claude` does NOT exist. Inside `~/.claude/` (names only): `.claude.json`,
`.credentials.json`, `settings.json`, `settings.json.bak`, `mcp-needs-auth-cache.json`,
`plugins/`, `skills/`, `projects/`, `sessions/`, `cache/`, `history.jsonl`, among others. UNVERIFIED
from this alone: that the binary derives this directory from `$HOME` rather than a hardcoded or
otherwise-resolved path — plausible by the conventional `~/.claude` spelling and by `--bare`'s own
reference to "keychain reads" and "CLAUDE.md auto-discovery" as things a flag can suppress, but
not confirmed by any flag or env var this session could read. A fresh `HOME` would, AS FAR AS THIS
READING SHOWS, very likely hide `~/.claude/.credentials.json` and `~/.claude/settings.json` from a
child process the same way it hides any other dotfile under `$HOME` — this is inference from the
path convention, not a verified mechanism, and T002's own research (not this round) must confirm
it against the installed binary rather than assume it.

## 5. Evidence today

The closest existing analogue to a per-call `worker_isolation` record is F157's
`record_capability_decisions` (`packages/orchestration/capability_routes.py:73-91`): one JSONL line
per provider build that decided anything, written beside the run/job evidence directory as
`capability_decisions.jsonl` (`CAPABILITY_DECISIONS_FILENAME`, `:26`), keyed by `role`/`provider`/
`model`, called from `routed_claude_cli_build` (`:100-117`) — itself called once per claude-cli
provider build. A `worker_isolation` evidence field could follow exactly this shape: a sibling
`worker_isolation.jsonl` (or a key inside the same file) written from the same call site, since
`routed_claude_cli_build` already runs once per build and already has `evidence_dir`.

The run manifest's own per-call seam is `on_call_finalized` (`packages/orchestration/run_manifest.py:202-211`),
the ONE place `FinalizedCall` records (`:138-187`) are appended to the manifest's call set — built
exclusively from calls at `packages/orchestration/pingpong_loop.py:2546` (`FinalizedCallContext(...)`)
and `:3009-3013` (`on_call_finalized(ctx, result.finalized_calls)`). `FinalizedCall` already carries
`identity`, `fingerprint`, `prepared_input`, `ok`, `artifact`/`artifact_sha256` — a `worker_isolation`
field (`method`, `home`, `env_digest`) would sit here too if the evidence belongs to the manifest's
own per-call record rather than beside it; the two call sites `pingpong_loop.py:2546`/`:3009` are
where it would have to be supplied from.

Reusable, redaction-respecting primitives, no values ever printed: `REDACTED = "[REDACTED]"`
(`run_manifest.py:110`) and `is_secret_key` (`packages/orchestration/job_input_definition.py:29`),
already composed by `config_snapshot`/`_environment_snapshot` (`run_manifest.py:586-610`, the
RUN-level, `REMEDY_`-prefixed env snapshot — not per-call, and not what an `env_digest` would be,
but the existing pattern for "redact before recording"). The digest pattern itself — canonical
sorted JSON bytes, then `hashlib.sha256(...).hexdigest()` — recurs repeatedly in this same file
(e.g. `FinalizedCall`-adjacent `canonical_artifact_bytes`/`artifact_sha256` plumbing at
`:174-184`, `:2793`, `:4214`, `:5524`, `:5958`); an `env_digest` is the same recipe applied to
`{key: name-or-REDACTED}` pairs instead of a call artifact, reusing `is_secret_key` to decide which
values are redacted before hashing, never printing a raw value.

## 6. Scratch and lifecycle

A job's own scratch is the git worktree `worktrees.py` manages: `create` (`packages/orchestration/worktrees.py:340-405`)
claims or re-attaches a worktree under `worktree_path_for` (`:141`), and detects a stale,
crash-left directory explicitly — "A stale directory left behind by a crash: git does not know it"
(`:357-362`), raising `WorktreeConflictError` rather than silently reusing it. `remove`
(`:829-861`) is the paired teardown: `git worktree remove --force`, `git worktree prune`, then
`shutil.rmtree` if anything remains, releasing the lock in a `finally` so a mid-failure never
blocks the job id from being reclaimed later. A throwaway HOME directory on real disk (the
non-sandboxed claude-cli path has none today, §2-3) would need an equivalent create/remove pair
and the same "is this stale, or is it currently held" check — nothing in `worktrees.py` manages
anything outside the worktree path itself, so a per-call HOME would be a NEW kind of path.

`data_reclaim.py`'s `plan_reclaim`/`_plan_class` (`packages/orchestration/data_reclaim.py:309-413`)
is the general sweep for orphaned data under the configured data root, by age and by a per-class
refusal rule (`job_state_refusal`, `:238-262`; `_orphan_verdict`, `:292-308`). A throwaway home that
is never registered as one of its classes (`_class_dir_names`, `:221-224`) would be invisible to
this sweep and would accumulate forever on every crash that skips its own cleanup — the sandbox's
own throwaway HOME (`tool_sandbox.py`'s `SANDBOX_HOME`, §3) has no such exposure because it is a
private tmpfs inside a Bubblewrap mount namespace that the kernel reclaims when the sandboxed
process group exits, with no file ever created on the real filesystem; that guarantee would NOT
automatically extend to a disk-backed throwaway home built for the unsandboxed `ClaudeCliProvider`
path.

## 7. Doctor

Remedy's own general health doctor is `remedy doctor health`
(`apps/cli/commands/doctor_health_cmd.py:11-43`), which calls `run_health_checks`
(`packages/orchestration/self_health.py:434-446`) — a fixed tuple of `check_*` functions, each
returning one `HealthCheckResult(check, level, detail, hint)` via `_result`
(`self_health.py:59-60`), PASS/WARN/FAIL (`HEALTH_PASS`/`WARN`/`FAIL`, `:36-39`); only a FAIL makes
the command exit non-zero (`health_exit_code`, `:459-460`). `check_providers` (`:271-295`) already
probes `shutil.which("claude")` and `ANTHROPIC_API_KEY` as a WARN-only reachability check, calling
no provider. Tests: `tests/orchestration/test_self_health.py`, `tests/cli/test_doctor_health_cmd.py`.

The block's own glob, `apps/cli/commands/doctor_*.py`, is INCOMPLETE for this feature's purpose:
the check that actually probes a worker's own tooling, `worker.doctor`, lives in
`apps/cli/commands/worker.py:248-311` (`_cmd_worker_doctor`, registered as `"worker.doctor"` at
`:330`), not in any `doctor_*.py` file. It already probes `shutil.which` for each `available`
worker spec's executable (`:270-284`) and the default chain's links (`:287-290`), with an explicit
"no doctor probe defined" answer for a spec it does not know how to check (`:281-284`) — the
natural extension point for "doctor catches a broken HOME strategy and a rejected flag", since it
is already per-adapter and already read-only. Catalog/vocabulary guards a new check's strings
would meet: `tests/cli/test_command_catalog.py` (command registration/catalog completeness) and
`tests/docs/test_vocabulary.py` (binding-word table, retired-synonym guard at `:248`) if any new
string becomes a documented binding word.

## 8. Guards and ledgers

`tests/orchestration/import_reachability_allowlist.txt` (468 lines) is GENERATED, never hand-typed
(`:1-5`, its own header): "the measured first-party closure of the six … entry points." A genuinely
new module under `packages/` that the invocation seam imports would need to land inside that
closure or be added to the allowlist in the same commit that adds the module —
`tests/orchestration/test_import_reachability.py` computes it. `tests/test_no_orphan_modules.py`
(`find_orphans`, `:211-238`; `test_no_module_is_an_orphan`, `:250`) separately fails any tracked
Python module no entry point reaches; a new module with no caller yet (e.g. an isolation-shape
module authored before its call site) would need an explicit allowlist entry there too.

`docs/system/structure-ledger-v1.md` pins every function over 100 lines and file over 1,000 lines
by exact line count (`tests/test_structure_ratchet.py`); rows already on this page that T001-T003
would touch include `packages/orchestration/exec_guard.py`'s `run_guarded` (122 lines, `:410`) and
several more `run_manifest.py` rows in the same size-sorted table (`_collect_calls` 274 lines
`:327`; `validate_run_manifest` 230 lines `:333`; `write_run_manifest` 125 lines `:413`;
`validate_input_snapshot` 159 lines `:364`; `validate_call_expectation` 137 lines `:391`;
`validate_call_ledgers` 135 lines `:393`; `validate_index_and_tree` 131 lines `:401`;
`_read_worktree_identity` 119 lines `:428`; `_verified_episode_export` 111 lines `:441`;
`validate_job_input_definition`/`validate_ledger_chain` 110 lines each `:444-445`). Growing any of
these functions to add an isolation field or an evidence write fails the ratchet test unless the
SAME commit raises that row's number — which the ledger's own rule (`docs/system/structure-ledger-v1.md:18-31`)
requires a DECISION for, never a hand edit, and the row may only rise alongside a measured growth,
never speculatively.

`docs/adr/` holds exactly one precedent: `0001-raise-cycle-safety-cap.md` (+ its `.diff`),
registered in `docs/README.md` twice — the quick-find table (`:10`) and the "Architecture Decision
Records" section table (`:240-250`, one row: file, one-line description, status). T002's ADR would
follow the same numbering (`0002-...`) and the same two-table registration, in the ADR's own round.
`docs/README.md:242-246` states the convention's own rule: a record is `PROPOSED` until a human
applies it and edits the status line themselves, shipped with a ready-to-apply diff beside it —
so `adr_ref` pointing at a record is not by itself proof the record is ACCEPTED; a conformance
check that gates on `adr_ref` alone, without reading that record's own status line, would certify
an adapter against a still-`PROPOSED` decision.

## 9. Names and a draft (a proposal for DECISION F152 D2, not a decision)

`worker_isolation` and `env_digest` grep to exactly two lines each, both inside
`docs/roadmap/features/T8_F152.md` itself (`:10-11`, `:34-35`, `:66`) — nowhere in code. `IsolationMethod`
and `isolation_adr` grep to NOTHING anywhere in the tree, including the feature file: the feature
file's own suggested shape (`T8_F152.md:39-41`) names the ADR field `adr_ref`, not `isolation_adr` —
the block's own proposed name list does not match the feature file's suggested shape on this one
name, worth resolving explicitly in D2 rather than carrying both spellings forward.

**A proposed shape** (proposal only): `isolation()` returns a frozen dataclass — `method` (one of
`tool_flag` / `clean_env` / `sandbox_reinforced`, matching the feature file's own vocabulary),
`home` (the throwaway-HOME strategy, `None` when the method needs none), and `adr_ref` (a required
string naming the `docs/adr/NNNN-*.md` file). The call builder (the invocation seam, §2) composes
it with `exec_guard.py`'s existing `ExecGuardPolicy.env_allowlist`/`env` machinery (§3) — reusing
the SAME policy fields `pi_provider.py` already sets, never inventing a second mechanism — and,
when the method calls for a throwaway HOME, a new create/remove pair modeled on `worktrees.py`'s
(§6), registered with `data_reclaim.py` so a crash-left one is swept. The evidence lands beside
`capability_decisions.jsonl` (§5), written from the same per-build call site
(`routed_claude_cli_build`-shaped), or as a new field on `FinalizedCall` if the review prefers the
manifest's own per-call record over a sibling file — an open choice for D2, not resolved here.

**The A/B proof without a paid call**: Remedy's OWN mechanics — that the throwaway HOME is built,
that `env_allowlist` actually strips a planted marker variable, that a poisoned `~/.claude/CLAUDE.md`-shaped
file placed in a FAKE home is not visible inside the sandboxed/allowlisted child's filesystem — can
all be proven with a stub executable on `PATH` named `claude` (a Python script print its own
environment/visible files) standing in for the real CLI, at zero cost and no network. What that
CANNOT prove: that the REAL `claude` binary's own documented flags (`--setting-sources`,
`--strict-mcp-config`, `--safe-mode`, …, §4) actually behave the way `--help`'s prose claims when
it is genuinely invoked — flags drift between CLI versions ("tools change flags", the feature
file's own words), and this inventory's own §4 VERIFIED/UNVERIFIED split exists exactly because
help text is not behavior. The feature's own Acceptance criterion — "marker present un-isolated,
absent isolated (the reference adapter)" — names a real invocation of the real CLI, which is a
paid call; a no-paid-call proof can cover the mechanism Remedy builds, never the CLI's own honesty
about it.

**Where the feature file's design does not match the tree**, beyond the `adr_ref`/`isolation_adr`
naming gap above: (a) the file's "Design" section imagines "the call builder" as a single place
that "applies the method" — the real seam is the four-hop chain of §2, and the environment
decision is made at `_guarded_cli_run`/`run_guarded`, two hops past `build_invocation`, not inside
the adapter at all; (b) the file's "doctor" bullet assumes `remedy doctor`, but the natural
per-adapter home is `worker.doctor` in `apps/cli/commands/worker.py` (§7), a file outside the
block's own `doctor_*.py` glob; (c) the file's edge-case note about "tools caching under XDG paths
beyond HOME" has a partial, untested answer already in the tree — `test_execution_service.py`'s
`_ALWAYS_KEEP`/`_SAFE_ENV_PREFIXES` (§3) already enumerate several `XDG_*`/`*_HOME` variables, but
for the test-command class, not for any worker call, so T002's per-tool research (§4's `claude`
CLI, specifically) starts from zero rather than from that list.
