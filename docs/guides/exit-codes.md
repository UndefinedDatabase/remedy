# Exit Codes

An exit code is the one signal a shell or a script sees without parsing
anything: the number a command hands back when it ends. Remedy gives every
code one meaning, so a caller can branch on the number alone instead of
scraping a message for a word that might get reworded. Two tables below carry
those meanings — one for the CLI as a whole, and one for the `runtime` group,
whose codes a process outside the CLI also reads (the supervisor subprocess
and the dev server it starts). A third table lists every command whose
handler can exit with a code above the shared floor, `0`, `1` and `2`, that
every command reaches regardless: the argument parser exits `2` on a
malformed invocation, and the dispatch boundary exits `1` on an unhandled
exception, before a single line of any handler runs.

This page is generated evidence, not prose written by hand: a test
(`tests/cli/test_exit_codes.py`) parses these three tables and asserts each
one equal to its source — the two tables in `apps/cli/exit_codes.py`, and the
command catalog's own `exit_codes` declarations above the floor. If this page
and the code ever disagree, the test is red.

## CLI Exit Codes

| Code | Name | Meaning |
|---|---|---|
| 0 | ok | The command did what it was asked, including finding nothing to do or honouring a pending stop request. |
| 1 | failed | The command ran and did not do what was asked — a refusal, a failed operation, a red check, drift found; the general failure and the code of every refusal no narrower meaning claims. |
| 2 | usage | The invocation itself is wrong — an unknown command, or a missing, invalid, unrecognised or conflicting argument — and nothing was attempted. |
| 3 | not_ready | The invocation is well formed, but what it names is absent or not in a state the command can act on. |
| 4 | environment | The machine lacks a prerequisite the command cannot supply, such as a git repository. |

## Runtime Group Exit Codes

The `runtime` group (`remedy runtime serve`, `probe`, `stop`) answers its own
contract instead of the CLI table above, because a process outside the CLI
reads its exit code directly. `0` and `1` mean what they mean everywhere, and
a malformed invocation of a runtime command still exits `2`.

| Code | Name | Meaning |
|---|---|---|
| 0 | ok | The command did what it was asked, including finding nothing to do or honouring a pending stop request. |
| 1 | failed | The command ran and did not do what was asked — a refusal, a failed operation, a red check, drift found; the general failure and the code of every refusal no narrower meaning claims. |
| 2 | config | The runtime configuration is missing or invalid. |
| 3 | start | The server did not start. |
| 4 | ready | It started and never answered ready. |
| 5 | state | A lifecycle or state failure such as a failed stop, surviving processes or an unreadable state file. |

## Commands With Codes Above The Floor

Every command not listed here exits only `0`, `1` or `2`.

| Command | Exit codes |
|---|---|
| `remedy init run` | 4 |
| `remedy job stop` | 3 |
| `remedy job pause` | 3 |
| `remedy job unpause` | 3 |
| `remedy job context` | 3 |
| `remedy job plan-show` | 3 |
| `remedy job plan-edit-task` | 3 |
| `remedy job edit-task` | 3 |
| `remedy job plan-delete-task` | 3 |
| `remedy job plan-reorder` | 3 |
| `remedy job plan-merge-tasks` | 3 |
| `remedy job plan-split-task` | 3 |
| `remedy job plan-edit-acceptance` | 3 |
| `remedy project current` | 3 |
| `remedy project attach` | 3 |
| `remedy project adopt` | 3 |
| `remedy mission run` | 3 |
| `remedy mission watchdog` | 3 |
| `remedy mission start` | 3 |
| `remedy mission list` | 3 |
| `remedy mission continue` | 3 |
| `remedy mission plan` | 3 |
| `remedy mission show` | 3 |
| `remedy mission contract` | 3 |
| `remedy mission achieve` | 3 |
| `remedy mission abandon` | 3 |
| `remedy mission pause` | 3 |
| `remedy mission resume` | 3 |
| `remedy job resume` | 3 |
| `remedy chat send` | 3 |
| `remedy chat show` | 3 |
| `remedy runtime serve` | 3, 4, 5 |
| `remedy runtime probe` | 3, 4, 5 |
| `remedy runtime stop` | 5 |

No existing exit-code site is renumbered by this taxonomy: a code is a
contract with every script that already reads it, so an older site that
answers a not-ready condition with `1`, for instance, keeps exiting `1`.
