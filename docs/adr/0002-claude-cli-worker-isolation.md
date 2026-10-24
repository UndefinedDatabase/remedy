# ADR-0002 — How the claude-cli worker keeps the operator's configuration out of a run

> **Status: RESEARCH RECORD, partly verified.** This is a research record under DECISION F152 D2:
> it pins what local evidence shows about the claude-cli tool's configuration surfaces, carries no
> diff, and needs no human apply step.

- Date: 2026-10-24
- Feature: T8_F152 — Worker config isolation
- Tool version read: 2.1.296 (from the captured help text)

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
| Environment variables | n/a | None found — the captured text names no environment variable that selects, adds or suppresses configuration; the only env vars present are two OUTPUTS the flags set (`CLAUDE_CODE_SAFE_MODE`, `CLAUDE_CODE_SIMPLE`) and `ANTHROPIC_API_KEY` as one accepted auth input | VERIFIED as an absence from this captured text (whole text read); UNVERIFIED as a claim about the real binary, since help text is not behavior (`.agent/f152_inventory.md` §4's own caveat). |

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
5. Whether the OAuth/keychain login path `--bare`'s text implies is reachable from a non-interactive
   `-p` call at all, or needs an interactive session first. Probe: run `claude -p` once from a shell
   holding a working OAuth login and once from a shell with only `ANTHROPIC_API_KEY` set, and
   compare the two outcomes. Needs the real binary — waits on Q26.
6. Whether `env=<explicit dict>` really reaches the child without `scrub_child_env`'s floor removing
   a key the dict carries but the allowlist does not name. Probe: a unit test calling
   `plan_child_spawn` with a policy whose `env` includes a `FORBIDDEN_ENV_KEYS` member and whose
   `env_allowlist` does not name it, asserting the key survives into the returned `child_env`. No
   real binary and no cost — Remedy's own code, provable in T001's own unit tests.

## Consequences

**T001** builds the `isolation()` contract member returning `method="clean_env"`, `adr_ref` pointing
here, the throwaway-home create/remove pair, the per-call `worker_isolation` evidence field (shaped
like `capability_decisions.jsonl`, `.agent/f152_inventory.md` §5), and the unit test for probe 6 —
all buildable without the real binary, with the declaration's exact shape frozen by DECISION
F152 D3 from this reviewed record.

**T002** builds the enforcement that wires the method into `_cli_exec_policy`/`_stream_exec_policy`,
the `--strict-mcp-config` flag addition, the stub-executable A/B proof that runs in every selection
(probe 4), and the real-binary A/B proof behind the Q26 switch (probe 3) — plus probes 1, 2 and 5,
which this feature's own research must still close before this record's rows can read fully
VERIFIED rather than "partly verified".

**T003** builds the `worker.doctor` check (`apps/cli/commands/worker.py:248-311`, not any
`doctor_*.py` file — `.agent/f152_inventory.md` §7), the conformance kit's `adr_ref` requirement,
and the docs.

**Re-verification.** This record is pinned to tool version `2.1.296`. A version bump that changes
any VERIFIED row above requires a fresh capture of `claude --version`/`--help` and a new round
reading this record against it — the feature file's own words, "tools change flags", are the reason
the Tool version read bullet exists at all, and it is the first thing a later session checks before
trusting any VERIFIED row here.
