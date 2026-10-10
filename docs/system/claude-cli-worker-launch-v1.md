# Claude CLI worker launch v1: what a worker loads before it does any work

> Status (F302, 2026-10-10): being built. DECISIONs F302 D1 to D3 in `.agent/decisions.md` hold
> the rules this page states; the feature is `docs/roadmap/features/T3_F302.md`. Built so far: the
> lean start and its two keys. The measurement before and after comes next. A job's record does
> not yet name the configuration its calls ran under; finding R-1235 carries that to F297.

Remedy starts Claude Code as a worker for every builder, reviewer and planner call of the
`claude-cli` provider: `claude -p <prompt> --output-format json`, with the model, the reviewer's
schema, a resumed session and the builder's write mode. A Claude Code session loads more than that
prompt. Its context carries the description of every built-in tool, the operator's and the
project's customizations — `CLAUDE.md`, skills, plugins, hooks, MCP servers, auto memory — and the
settings files. The code is `packages/orchestration/claude_cli_command.py`.

## What was measured
`.agent/f302_attribution.md` holds twenty calls of one fixed question that needs no tool, made
through the same path every builder call takes: once with everything loaded and once with each
source left out, in an empty repository and in a worktree of Remedy. Left out alone, the built-in
tools a builder does not use saved about 9,100 tokens in both places; safe mode, which loads none of
the customizations, saved about 4,300 in the empty repository and about 10,400 in Remedy's, whose
own instruction files and skills it also leaves out. Leaving out the MCP servers alone saved about
800, the settings files about 500, and moving the per-user context out of the system prompt about
150. Turning off skills and commands with `--disable-slash-commands` raised the count by about
1,900, and `--bare` ended at once, because it does not use a subscription's sign-in.

## The lean start
`build_claude_cli_args` ends every command line with the switches `claude_cli_launch_switches`
answers for the call's write mode:

| Write mode | Switches |
|---|---|
| `none` (a reviewer or a planner) | `--safe-mode --tools Read,Glob,Grep` |
| `allowed-tools` (a builder that may edit) | `--safe-mode --tools Read,Glob,Grep,Edit,Write,MultiEdit` |
| `dangerous-skip` (a builder that may run commands) | `--safe-mode` |

A builder started with `dangerous-skip` keeps every tool, because the operator gave it the right to
run commands. The settings files still load: they may carry the sign-in helper or a proxy, and
leaving them out saved little.

## Turning a source back on
Each source the lean start leaves out has a key that turns it back on, in `remedy.toml` or its
environment variable; both are false unless set.

| Key | Variable | True means |
|---|---|---|
| `claude_cli.customizations` | `REMEDY_CLAUDE_CLI_CUSTOMIZATIONS` | no `--safe-mode`: the worker loads `CLAUDE.md`, skills, plugins, hooks, MCP servers and auto memory |
| `claude_cli.all_tools` | `REMEDY_CLAUDE_CLI_ALL_TOOLS` | no `--tools`: the worker gets every built-in tool |

With both true, the command line is the one Remedy used before F302. The keys are read through the
process's cached configuration, `get_config()`, so every call one Remedy process makes reads the
same values.
