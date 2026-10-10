# F302 T002 — what a claude-cli worker's first call reads, source by source

> Written by `.agent/authored/f302-r2-attribution.py render` from
> `.agent/f302_attribution.jsonl` alone; every figure below is computed, none typed.

Provider calls made: 20, of at most 20 (DECISION F302 D1 (2); the
feature file allows 40). The task: "This is a measurement call. Answer with the one word READY and nothing else. Use no tool.", with the
builder's write mode `allowed-tools` and model `claude-sonnet-4-6`, through `build_claude_cli_args` and
`_guarded_cli_run`, the path every job's builder call takes. Context is input plus cache
creation plus cache read: what the call's requests read, however much of it was cached.
A call of more than one turn read its context once per turn, so its row is marked.
Claude Code version: `not reported`.
Environment variables named `CLAUDE*` or `ANTHROPIC*` in the run (names only): `CLAUDECODE`, `CLAUDE_CODE_CHILD_SESSION`, `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS`, `CLAUDE_CODE_ENTRYPOINT`, `CLAUDE_CODE_EXECPATH`, `CLAUDE_CODE_MESSAGING_SOCKET`, `CLAUDE_CODE_MESSAGING_TOKEN`, `CLAUDE_CODE_SESSION_ATTENDED`, `CLAUDE_CODE_SESSION_ID`, `CLAUDE_CODE_SUBAGENT_MODEL`, `CLAUDE_CONFIG_DIR`, `CLAUDE_EFFORT`, `CLAUDE_PID`.

## In a scratch repository
Baseline context: mean 21,533, the two baselines 0 apart.

| Config | Switches | Exit | Turns | Input | Output | Cache creation | Cache read | Context | Context minus baseline |
|---|---|---|---|---|---|---|---|---|---|
| baseline | none | 0 | 1 | 3 | 5 | 21,530 | 0 | 21,533 | 0 |
| no-mcp | `--strict-mcp-config` | 0 | 1 | 3 | 5 | 3,754 | 16,940 | 20,697 | -836 |
| no-settings | `--setting-sources` `""` | 0 | 1 | 3 | 5 | 4,134 | 16,940 | 21,077 | -456 |
| no-skills | `--disable-slash-commands` | 0 | 1 | 3 | 5 | 23,483 | 0 | 23,486 | 1,953 |
| builder-tools | `--tools` `Read,Edit,Write,MultiEdit,Glob,Grep` | 0 | 1 | 3 | 5 | 12,425 | 0 | 12,428 | -9,105 |
| no-dynamic | `--exclude-dynamic-system-prompt-sections` | 0 | 1 | 3 | 5 | 21,385 | 0 | 21,388 | -145 |
| safe-mode | `--safe-mode` | 0 | 1 | 3 | 5 | 4,388 | 12,861 | 17,252 | -4,281 |
| bare | `--bare` | 1 | 1 | 0 | 0 | 0 | 0 | — | — |
| lean | `--strict-mcp-config` `--setting-sources` `""` `--disable-slash-commands` `--tools` `Read,Edit,Write,MultiEdit,Glob,Grep` `--exclude-dynamic-system-prompt-sections` | 0 | 1 | 3 | 5 | 9,896 | 0 | 9,899 | -11,634 |
| baseline-repeat | none | 0 | 1 | 3 | 5 | 0 | 21,530 | 21,533 | 0 |

`bare` ended with exit 1: Not logged in · Please run /login

## In a worktree of Remedy
Baseline context: mean 28,035, the two baselines 0 apart.

| Config | Switches | Exit | Turns | Input | Output | Cache creation | Cache read | Context | Context minus baseline |
|---|---|---|---|---|---|---|---|---|---|
| baseline | none | 0 | 1 | 3 | 5 | 15,171 | 12,861 | 28,035 | 0 |
| no-mcp | `--strict-mcp-config` | 0 | 1 | 3 | 5 | 10,271 | 16,925 | 27,199 | -836 |
| no-settings | `--setting-sources` `""` | 0 | 1 | 3 | 5 | 10,605 | 16,925 | 27,533 | -502 |
| no-skills | `--disable-slash-commands` | 0 | 1 | 3 | 5 | 13,020 | 16,883 | 29,906 | 1,871 |
| builder-tools | `--tools` `Read,Edit,Write,MultiEdit,Glob,Grep` | 0 | 1 | 3 | 5 | 11,772 | 7,073 | 18,848 | -9,187 |
| no-dynamic | `--exclude-dynamic-system-prompt-sections` | 0 | 1 | 3 | 5 | 11,176 | 16,711 | 27,890 | -145 |
| safe-mode | `--safe-mode` | 0 | 1 | 3 | 5 | 3,610 | 13,979 | 17,592 | -10,443 |
| bare | `--bare` | 1 | 1 | 0 | 0 | 0 | 0 | — | — |
| lean | `--strict-mcp-config` `--setting-sources` `""` `--disable-slash-commands` `--tools` `Read,Edit,Write,MultiEdit,Glob,Grep` `--exclude-dynamic-system-prompt-sections` | 0 | 1 | 3 | 5 | 7,391 | 8,961 | 16,355 | -11,680 |
| baseline-repeat | none | 0 | 1 | 3 | 5 | 0 | 28,032 | 28,035 | 0 |

`bare` ended with exit 1: Not logged in · Please run /login
