# Claude CLI worker launch v1: what a worker loads before it does any work

> Status (F302, 2026-10-10): being built. DECISIONs F302 D1 to D4 in `.agent/decisions.md` hold
> the rules this page states; the feature is `docs/roadmap/features/T3_F302.md`. Built: the lean
> start, its two keys, the measurement before and after it, and `remedy stats calls`. A job's
> record does not yet name the configuration its calls ran under; finding R-1235 carries that to
> F297.

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

## Before and after
`.agent/f302_after.md` holds the same fixed question asked with the command line before F302 and
with the lean start: in an empty repository its call read 21,533 tokens before and 7,051 after,
and in a worktree of Remedy 28,056 before and 7,407 after. One small real repair ran as a job each
way and passed its review in two calls with the same change; its builder's first call read 725,658
tokens before and 435,183 after.

## Reading the tokens: `remedy stats calls`
`remedy stats calls` prints, by role and provider, how many provider calls the run records hold,
how many of them reported their tokens, and the mean tokens per call of each kind: input, output,
cache creation and cache read. Its last line divides the tokens of all those calls by the number
of jobs among them whose `remedy job apply` landed, which is what one landed change cost, failed
attempts included. A figure no call reported prints `unmeasured`, never 0. `--since` keeps the
calls whose task run finished at or after a time, `--job` the calls of one job, and `--json`
answers the same figures as data; the code is `packages/orchestration/call_tokens.py`.
