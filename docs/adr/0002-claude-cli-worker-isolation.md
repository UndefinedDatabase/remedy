# ADR-0002 — How the claude-cli worker keeps the operator's configuration out of a run

> **Status: RESEARCH RECORD, partly verified; checked against the real binary on 2026-10-24.**
> This is a research record under DECISION F152 D2: it pins what local evidence shows about the
> claude-cli tool's configuration surfaces, carries no diff, and needs no human apply step. The
> section "The real binary, 2026-10-24" records the real call operator amendment
> amend1024-one-real-order (D2) ordered, and replaces each UNVERIFIED that call proves.

- Date: 2026-10-24
- Feature: T8_F152 — Worker config isolation
- Tool version read: 2.1.296 (from the captured help text); 2.1.310 run for real on 2026-10-24

## Context

Today, every environment variable of the operator's own shell reaches a claude-cli worker call:
`_cli_exec_policy` and `_stream_exec_policy` (`packages/orchestration/pingpong_provider.py:811-822`,
`:825-839`) build the `ExecGuardPolicy` for every call and set neither `env=` nor
`env_allowlist=`; their own docstrings say why, in the same words twice (`:816-819`, `:833-837`):
the child is the operator's authenticated `claude` CLI and reads its credentials from the inherited
environment. With both fields `None`, `plan_child_spawn` (`packages/orchestration/exec_guard.py:365-404`)
leaves `child_env = policy.env`, i.e. `None`, which `Popen` reads as "inherit the parent's whole
environment" — nothing is stripped, nothing is allowlisted. Neither policy sets `sandbox=` either,
so a claude-cli call never runs through `tool_sandbox`, and `ClaudeCliProvider.__init__`
(`pingpong_provider.py:887-919`) carries no `home`/`HOME` field at all — the operator's own home,
and everything under it, is exactly what the child sees. The one thing Remedy already does to lean
the call out is `claude_cli_launch_switches` (`packages/orchestration/claude_cli_command.py:46-59`),
which appends `--safe-mode` to every call unless `claude_cli.customizations` is configured true —
already requesting the CLI's own customization suppression, independent of this feature.

## What the tool reads

| Surface | How the tool finds it | Switch that suppresses or redirects it | Verified? |
|---|---|---|---|
| User settings | UNVERIFIED — plausibly `~/.claude/settings.json` by the conventional spelling; not confirmed to derive from `$HOME` (`.agent/f152_inventory.md` §4) | `--setting-sources` selects which of user/project/local load; `--restricted` ignores user settings files | VERIFIED (switches): `.agent/f302_claude_help.txt:228-229`, `:197-211`. UNVERIFIED (location). |
| Project and local settings | UNVERIFIED — no path named in the captured text | `--setting-sources`; `--restricted` ignores project and local settings files | VERIFIED (switches): `:228-229`, `:197-211`. UNVERIFIED (location). |
| Managed settings | UNVERIFIED — "admin-managed (policy)"; no path named | None found — both `--safe-mode` and `--restricted` state it still applies | VERIFIED (survival): `:215-225` ("Admin-managed (policy) settings still apply"), `:197-211` ("managed settings ... still apply"). UNVERIFIED (location, and whether ANY switch suppresses it). |
| The instructions file (CLAUDE.md) | Auto-discovery, per `--bare`'s own text; exact search path UNVERIFIED | `--safe-mode` disables it as a customization; `--bare` skips "CLAUDE.md auto-discovery"; `--add-dir` re-adds CLAUDE.md directories explicitly | VERIFIED: `:215-225`, `:44-61`, `:13-14`. |
| MCP servers | UNVERIFIED default discovery location; explicit load is `--mcp-config` | `--safe-mode` disables MCP servers; `--strict-mcp-config` restricts to only `--mcp-config`'s own; `--restricted` + `--strict-mcp-config` together skip MCP entirely | VERIFIED: `:215-225`, `:232-233`, `:135-136`, `:197-211`. UNVERIFIED (default location). |
| Plugins and skills | UNVERIFIED default discovery; explicit load is `--plugin-dir`/`--plugin-url` | `--safe-mode` disables installed plugins and skills; `--disable-slash-commands` disables all skills; `--bare` skips plugin sync but states "Skills still resolve via /skill-name" | VERIFIED: `:215-225`, `:83`, `:44-61`, `:165-172`. |
| Hooks | UNVERIFIED — "those defined in settings and by installed plugins", per `--bare`'s own text; no path named | `--safe-mode` disables hooks; `--bare` skips hooks ("features built into Claude Code are unaffected") | VERIFIED: `:215-225`, `:44-61`. |
| The login | `~/.claude/.credentials.json` exists (filesystem existence only, not a help-text claim — `.agent/f152_inventory.md` §4); `$HOME`-derivation UNVERIFIED | None found that suppresses or redirects it; `--bare` NARROWS accepted auth to `ANTHROPIC_API_KEY` or `apiKeyHelper` via `--settings`, stating OAuth and keychain "are never read" under that flag — implying both are normally-available sources outside `--bare` | VERIFIED (the narrowing and its implication): `:44-61`. UNVERIFIED (storage location and mechanism). |
| Environment variables | `CLAUDE_CONFIG_DIR` selects the folder the login and the user configuration are read from; on this machine the operator's profile wrapper sets it | Passed through by the allowlist since amend1024 D1, so the worker keeps the account the operator's own session chose | VERIFIED (2026-10-24, real call): the call ran with the operator's `CLAUDE_CONFIG_DIR` and authenticated; the captured help text names no such variable, which stays true of that text. |

## The login

As far as local evidence shows: a filesystem check (`os.path.exists`/`os.listdir`, no content read)
found `~/.claude/.credentials.json` present; no code or help text read this round confirms the
binary derives that directory from `$HOME` specifically, though the conventional `~/.claude`
spelling makes it plausible. A fresh `HOME` would, on that inference alone, very likely hide this
file from a child process the same way it hides any other dotfile under `$HOME` — this is
inference from path convention, not a verified mechanism, and T002's own research must confirm it
against the real binary.

What that means for each of the three methods T8_F152.md names:

- **`tool_flag`.** A flag alone changes which CONFIGURATION layers load, not `HOME`. Nothing in the
  captured text suggests `--safe-mode` or `--restricted` touches login, and `--bare`'s own text
  shows OAuth and keychain ARE normally read outside `--bare` — so a tool-flag-only method, on this
  evidence, leaves the login exactly where it is today.
- **`clean_env`.** A throwaway `HOME` with a cleaned allowlist very likely hides
  `~/.claude/.credentials.json` (inference above). It also meets `exec_guard.py`'s
  `FORBIDDEN_ENV_KEYS` floor (`:104-110`), which `scrub_child_env` (`:163-171`) drops from ANY
  allowlist-built child environment even when the allowlist names it. If the operator's login rode
  on `ANTHROPIC_API_KEY` in the inherited environment, a naive `clean_env` method loses BOTH the
  hidden login directory and that one accepted env var, leaving the worker with no verified way to
  authenticate at all. Isolating the login and preserving it are two different goals; this is the
  central tension T001 must resolve, not a detail.
- **`sandbox_reinforced`.** `SandboxSpec.wrap` (`packages/orchestration/tool_sandbox.py:214-266`)
  sets `HOME` to `SANDBOX_HOME` unconditionally (`:256`), whatever the caller's allowlist says — the
  same consequence as `clean_env`, by the same mechanism (a different `HOME`), with the same
  `FORBIDDEN_ENV_KEYS` floor still sitting beneath whatever allowlist the caller composes.

## The chosen mechanism (declared by DECISION F152 D3)

**Method: `tool_flag`, not `clean_env`.** DECISION F152 D3 rejects this record's own
`clean_env`/throwaway-home proposal above: "The login" section just above shows a fresh `HOME`
very likely hides the operator's own login, which would make every paid worker call fail to
authenticate — isolating the login and preserving it are two different goals, and a throwaway
home serves only the first. D3 declares `tool_flag` instead: no new `HOME`, so the operator's
login stays exactly where it is.

**Exact flags.** Keep `--safe-mode` (already appended by `claude_cli_launch_switches`,
`claude_cli_command.py:46-59`, unrelated to this feature), and add `--setting-sources
project,local` (keeping the operator's own user-level settings and every MCP server not named on
the command line out, while the project's own settings still load) and `--strict-mcp-config` (a
second, independent closure of the MCP surface, since `--safe-mode`'s own claim to disable MCP
servers is one flag's prose and not yet proven against the real binary).

**Environment allowlist (names only, not counted):** `HOME`, `LANG`, `LC_ALL`, `LC_CTYPE`,
`LOGNAME`, `PATH`, `SHELL`, `TERM`, `TMPDIR`, `TZ`, `USER`, plus the names the tool needs to reach
its model the way it does today: `ANTHROPIC_API_KEY` and the proxy variables in both spellings
(`HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY`, `NO_PROXY` and their lower-case forms). `HOME` in this
list names the OPERATOR's own home, never a throwaway one. `packages/orchestration/worker_isolation.py`'s
`isolated_child_env` builds the child's environment from this list directly, and
`_cli_exec_policy`/`_stream_exec_policy` set it as `env=` with `env_allowlist` left `None`, so the
dict reaches the child exactly as built — never re-scrubbed by `exec_guard.py`'s
`FORBIDDEN_ENV_KEYS` floor, which would otherwise drop `ANTHROPIC_API_KEY` and the proxy
variables this method deliberately lets through.

**Throwaway home: no caller yet.** `create_throwaway_home`/`remove_throwaway_home` exist
(modeled on `worktrees.py`'s `create`/`remove` pair, `.agent/f152_inventory.md` §6), but
`adapter_child_env` refuses a declaration that asks for one, because `tool_flag` declares none
and no other call path provides one; T002's A/B proof utility is its first intended user.

**What this mechanism leaves reaching the run, stated plainly.** The allowlisted names above,
pointed at the operator's own, unchanged home; `--safe-mode`'s, `--setting-sources`'s and
`--strict-mcp-config`'s suppression (verified for what their text claims, unverified for
completeness against the real binary); and the operator's own login, wherever it lives, because
nothing in this method touches `HOME`. It does NOT leave reaching the run: any proxy variable,
cloud credential or other name this allowlist does not itself name; the operator's own
customizations, CLAUDE.md auto-discovery, skills, plugins or hooks, which `--safe-mode` already
suppresses independently of this feature; or any MCP server not named on the command line.

## The real binary, 2026-10-24

Operator amendment amend1024-one-real-order (D2) ordered one real call of this machine's `claude`
through the adapter: `scripts/claude_cli_real_binary_check.py` builds a `ClaudeCliProvider` builder
with `allowed-tools` in a fresh temporary folder and asks it to create one file. The record is
`evidence/current/claude_cli_real_binary_check.json`; it names every environment name the child got
and never a value.

- **Result.** `claude` 2.1.310 (found on PATH as the operator's profile wrapper), 6.8 seconds, the
  file created with exactly the asked content, 4 input and 166 output tokens beside 11,957 cached
  and 1,943 cache-written, two model turns. The isolation applied: method `tool_flag`, the
  operator's home, the argv ending with `--safe-mode`, `--tools Read,Glob,Grep,Edit,Write,MultiEdit,Bash`,
  `--setting-sources project,local` and `--strict-mcp-config`, and the builder's `Bash(<command>:*)`
  rules after `--allowedTools Edit,Write,MultiEdit`.
- **The environment the child got:** `CLAUDE_CONFIG_DIR`, `HOME`, `LANG`, `LOGNAME`, `PATH`, `SHELL`,
  `TERM` and `USER`; every other declared name is unset on this machine. No `ANTHROPIC_API_KEY` was
  set: the login is the operator's own Claude Code login, read by a non-interactive `-p` call.
- **The control with F152's list** (`evidence/current/claude_cli_real_binary_check_f152_control.json`,
  the same call without the twelve names amend1024 D1 added) also succeeded, in 11.4 seconds, with
  `CLAUDE_CONFIG_DIR` dropped. So no variable was missing for a working call on this machine: the
  operator's wrapper, which stands first on PATH, chooses its active profile itself when
  `CLAUDE_CONFIG_DIR` is absent. That choice is the wrapper's, not the session's: without the
  variable a worker may run on another of the operator's accounts than the session that started
  it, which is why D1 passes it.

What the call proves, and so no longer UNVERIFIED: the flags `--safe-mode`, `--tools`,
`--setting-sources project,local`, `--strict-mcp-config` and `--allowedTools` with `Bash(...)` rules
are accepted by the real binary 2.1.310; a non-interactive `-p` call reaches the operator's OAuth
login with `HOME` and `CLAUDE_CONFIG_DIR` alone (probe 5 below); and the allowlisted environment
reaches the child as built, without the floor removing a name it carries. What it does not prove,
and stays UNVERIFIED: where the settings files live, whether `--safe-mode` and
`--strict-mcp-config` suppress every customization of a real session (the poisoned A/B of probe 3),
and whether a throwaway `HOME` would hide the login.

## Verification owed

1. Whether `~/.claude` and its settings/credentials files are actually derived from `$HOME` rather
   than a hardcoded or otherwise-resolved path. Probe: launch the real binary with a throwaway
   `HOME` pointed at an empty directory and a planted marker in a FAKE `~/.claude/CLAUDE.md`-shaped
   file under the real home; a run that does not show the marker confirms the derivation. Needs the
   real binary — waits on Q26.
2. Where user, project and local settings files actually live on disk. Probe: run `claude doctor`,
   which the help text says "Reads settings files in the current directory without a trust prompt"
   (`:278-282`), inside a directory holding a planted settings file, and read its reported paths.
   Needs the real binary — waits on Q26.
3. Whether `--safe-mode` and `--strict-mcp-config` really suppress MCP/plugins/hooks/CLAUDE.md
   under a real session the way their help text claims. Probe: the feature's own poisoned-config
   A/B — plant a marker instruction in a fake personal config, run once un-isolated and once with
   the proposed flags, env and home, and diff the two outputs for the marker. Needs the real binary
   and one paid call — waits on Q26.
4. Whether a throwaway `HOME` really hides `~/.claude/.credentials.json` from the child's own
   filesystem view. Probe: a stub executable standing in for `claude` that prints what it can see
   under its own `$HOME`, run once against the real home and once against the throwaway one. No
   real binary and no cost — runs now, does not wait on Q26.
5. ANSWERED on 2026-10-24 for the OAuth half: a non-interactive `-p` call reaches the operator's
   OAuth login with no `ANTHROPIC_API_KEY` set ("The real binary, 2026-10-24"). The
   `ANTHROPIC_API_KEY`-only half was not run.
6. Whether `env=<explicit dict>` really reaches the child without `scrub_child_env`'s floor removing
   a key the dict carries but the allowlist does not name. Probe: a unit test calling
   `plan_child_spawn` with a policy whose `env` includes a `FORBIDDEN_ENV_KEYS` member and whose
   `env_allowlist` does not name it, asserting the key survives into the returned `child_env`. No
   real binary and no cost — Remedy's own code, provable in T001's own unit tests.

## Consequences

**T001**, closed under DECISION F152 D3: the `isolation()` contract member returns
`method="tool_flag"`, not this record's own rejected `clean_env` proposal above — "The chosen
mechanism" is the section that rules the method, and this section only reports what landed. It
built the claude-cli declaration (`adr_ref` pointing here, the exact flags and the environment
allowlist D3 (2) names), the throwaway-home create/remove pair (D3 (5), with no caller yet), the
per-build `worker_isolation.jsonl` evidence line (D3 (4)), and the unit test for probe 6 — all
without the real binary.

**T002**, under DECISION F152 D4: `declared_isolation` refuses an installed adapter that carries
no `isolation()` member or answers anything but a `WorkerIsolation`, closing the neutral fallback
R-1456 found; the reusable `run_isolation_ab` utility runs an adapter's own declared command line
twice, isolated and not, against one poisoned throwaway home, and its stand-in-`claude` proof and
two red controls run in every selection (probe 4). The real-binary A/B proof (probe 3) and probes
1, 2 and 5 all wait on the operator question that holds the real-binary proof, Q26 (D4 (4)); this
record's rows stay "partly verified" until that answer lets a session run them.

**T003** builds the `worker.doctor` check (`apps/cli/commands/worker.py:248-311`, not any
`doctor_*.py` file — `.agent/f152_inventory.md` §7), the conformance kit's `adr_ref` requirement,
and the docs.

**Re-verification.** This record is pinned to tool version `2.1.296`. A version bump that changes
any VERIFIED row above requires a fresh capture of `claude --version`/`--help` and a new round
reading this record against it — the feature file's own words, "tools change flags", are the reason
the Tool version read bullet exists at all, and it is the first thing a later session checks before
trusting any VERIFIED row here.
