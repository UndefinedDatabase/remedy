# F302 inventory — T001: the claude-cli worker's tokens per call, read from the records

> Written for `docs/roadmap/features/T3_F302.md` T001 on 2026-10-10, at `main` `6689c581e`. No
> provider call was made. Read by the reviewer's dry run (`collect.py` and `make_inventory.py`
> under `.remedy-wt/f302-r1/`), which wrote every figure below.

## How the records were read
The data root is closed to every agent of the build loop (`Read(./.data/**)` in
`.claude/settings.json`), so the records were read only through Remedy's own commands:
`remedy run list --json` names every persisted run, and `remedy run show <run> --json` answers a
run's `provider_evidence.provider_attempts` (one entry per provider call, with its role, round,
sequence and the four usage figures of the call), its `rounds` (each side's `session_id` and
`resume_used`) and its `finalized_calls` (each call's prompt length in bytes). The repo-scoped token
ledger (`remedy stats cost --all-projects --by role --json`) holds 8 calls in all, because a job
without a project writes no ledger row; the run records are therefore the source.

Of the 4,804 runs `remedy run list` names, every run whose goal reads `test goal` or `goal` is a
test fixture and was left out; the remaining runs were read whole. A call counts when its
`provider` is `claude-cli`.

## What a call is started with
`build_claude_cli_args` in `packages/orchestration/pingpong_provider.py` at `6689c581e` passes
`-p <prompt>`, `--output-format json` (or `stream-json --verbose` under stream evidence),
`--model`, `--json-schema` for the reviewer, `--resume <session>` for a resumed side, and the write
mode's `--allowedTools Edit,Write,MultiEdit` or `--dangerously-skip-permissions`. Nothing limits
the tool servers, the settings, skills and hooks of the operator and the project, or the project's
instruction files. Every call below ran in a job worktree of Remedy's own repository
(remedy-job-worktree: 91 calls), so `CLAUDE.md`, which points at `AGENTS.md`, is
in reach of every one of them.

## The switches the installed `claude` offers
The `claude` binary refused to run for the loop's agents in this session (`This command requires
approval`, for `--help` and `--version` alike), so the switches were read from Claude Code's own CLI
reference, https://code.claude.com/docs/en/cli-reference, fetched on 2026-10-10, which says that
`claude --help` does not list every flag. The versions that made the calls below are the ones the
records name. The candidates for T002, each a source a call loads today:
- `--strict-mcp-config` without `--mcp-config`: no MCP server from any other configuration.
- `--setting-sources <list>`: which of the `user`, `project` and `local` settings load.
- `--disable-slash-commands`: no skills and no commands.
- `--tools <list>`: restricts the built-in tools; it does not reach MCP tools.
- `--exclude-dynamic-system-prompt-sections`: per-user context moves out of the system prompt.
- `--bare`: no hooks, skills, commands, subagents, plugins, MCP servers, auto memory or `CLAUDE.md`.
- `--safe-mode`: all customizations off, `CLAUDE.md` included; built-in tools and permissions as usual.
Whether the installed version accepts each, and whether `--bare` keeps the subscription's sign-in,
is what T002's calls show; an unknown switch ends a call with an error the run record keeps.

## The calls
- Calls by `claude-cli`: 91, in 32 runs of 29 jobs, finished from 2026-09-20 to 2026-10-10.
- With all four token figures: 77. Without them: 14 (a call that failed, or a record older than the cache keys).
- By role, of the 77: builder 40, reviewer 37.
- Claude Code versions: `2.1.280 (Claude Code)` 4, `2.1.282 (Claude Code)` 3, `2.1.283 (Claude Code)` 6, `2.1.284 (Claude Code)` 4, `2.1.285 (Claude Code)` 8, `2.1.286 (Claude Code)` 14, `2.1.291 (Claude Code)` 18, `2.1.292 (Claude Code)` 4, `2.1.293 (Claude Code)` 4, `2.1.294 (Claude Code)` 4, `2.1.295 (Claude Code)` 6, `2.1.296 (Claude Code)` 4, `not recorded` 12.
- Models: `claude-sonnet-4-6` 91.

## Per role, first call of a session and resumed call
A call is the first of its session when its side did not resume one (`resume_used` false), and
resumed when it did; a call whose round record does not say is in neither row (6 calls).
Each cell is the median, then the smallest and the largest, over the calls of that row. Cache read
counts every turn of the session's own tool loop, each of which reads the cache again, so it grows
with the turns a task takes; cache creation is what the session wrote into the cache.

| Role | Session | Calls | Input | Output | Cache creation | Cache read |
|---|---|---|---|---|---|---|
| builder | first | 33 | 12 (5–82) | 4,213 (499–36,247) | 40,960 (11,886–115,123) | 280,965 (68,183–7,126,410) |
| builder | resumed | 3 | 6 (5–7) | 1,302 (430–2,213) | 2,867 (1,414–3,873) | 146,173 (124,985–258,299) |
| reviewer | first | 32 | 6 (4–24) | 3,130 (592–9,501) | 31,323 (8,347–39,271) | 93,240 (20,942–610,880) |
| reviewer | resumed | 3 | 3 (3–3) | 651 (186–685) | 1,570 (1,355–1,963) | 35,756 (33,201–37,576) |

## The share of cache creation in a session's first call
Share = cache creation ÷ (input + cache creation + cache read), the part of what the call read
that it first had to write into the cache.

| Role | First calls | Median share | Smallest | Largest |
|---|---|---|---|---|
| builder | 33 | 11.7% | 1.6% | 20.7% |
| reviewer | 32 | 17.5% | 3.4% | 53.7% |

## What a job's `total_tokens` leaves out
Over the 77 calls with all four figures: input plus output, the figure a job's Budget Actuals
report as `total_tokens`, is 363,368; cache creation is 2,729,228 and cache read 35,108,295; all four
together are 38,200,891, so `total_tokens` names 1.0% of the tokens the calls moved.

## Every call
`F` marks the first call of a session, `R` a resumed call and `—` a call whose record does not say.
Prompt is the length in bytes of the prompt Remedy itself wrote for the call.

| Run | Seq | Round | Role | F | Input | Output | Cache creation | Cache read | Prompt | Version |
|---|---|---|---|---|---|---|---|---|---|---|
| `9e1544e204ea4091` | 1 | 1 | builder | — | — | — | — | — | 18,539 | — |
| `9e1544e204ea4091` | 2 | 1 | builder | — | — | — | — | — | — | — |
| `9e1544e204ea4091` | 3 | 1 | builder | — | — | — | — | — | — | — |
| `3662fda0b0824e61` | 1 | 1 | builder | — | — | — | — | — | 18,526 | — |
| `3662fda0b0824e61` | 2 | 1 | builder | — | — | — | — | — | — | — |
| `3662fda0b0824e61` | 3 | 1 | builder | — | — | — | — | — | — | — |
| `73a48603ca65474c` | 1 | 1 | builder | — | — | — | — | — | 18,501 | — |
| `73a48603ca65474c` | 2 | 1 | builder | — | — | — | — | — | — | — |
| `73a48603ca65474c` | 3 | 1 | builder | — | — | — | — | — | — | — |
| `a320aed02c064f97` | 1 | 1 | builder | — | 14 | 4,419 | 63,919 | 555,333 | 17,059 | 2.1.280 |
| `a320aed02c064f97` | 2 | 1 | reviewer | — | 3 | 1,638 | 26,640 | 0 | 1,406 | 2.1.280 |
| `a320aed02c064f97` | 3 | 2 | builder | — | — | — | — | — | 16,632 | 2.1.280 |
| `a320aed02c064f97` | 4 | 2 | builder | — | 8 | 2,747 | 37,842 | 318,196 | — | 2.1.280 |
| `1ee973f19dbc4fd6` | 1 | 1 | builder | — | — | — | — | — | 18,274 | — |
| `1ee973f19dbc4fd6` | 2 | 1 | builder | — | — | — | — | — | — | — |
| `1ee973f19dbc4fd6` | 3 | 1 | builder | — | — | — | — | — | — | — |
| `bfa454f9cd914f96` | 1 | 1 | builder | — | 17 | 11,548 | 86,237 | 777,413 | 17,785 | 2.1.282 |
| `bfa454f9cd914f96` | 2 | 1 | reviewer | — | 4 | 1,223 | 31,528 | 29,543 | 6,984 | 2.1.282 |
| `4b0a5213c27a4ccf` | 1 | 1 | builder | — | 29 | 12,614 | 98,466 | 2,074,026 | 18,188 | 2.1.282 |
| `94eae4484e9f432f` | 1 | 1 | builder | F | 18 | 7,166 | 48,087 | 600,945 | 18,123 | 2.1.283 |
| `94eae4484e9f432f` | 2 | 1 | reviewer | F | 4 | 3,880 | 34,164 | 29,436 | 5,044 | 2.1.283 |
| `1f6f98f62e7348cb` | 1 | 1 | builder | F | 10 | 2,435 | 41,617 | 260,502 | 16,947 | 2.1.283 |
| `1f6f98f62e7348cb` | 2 | 1 | reviewer | F | 4 | 677 | 29,981 | 28,811 | 2,685 | 2.1.283 |
| `dc4b978959f643b6` | 1 | 1 | builder | F | 28 | 4,826 | 46,787 | 1,007,663 | 16,959 | 2.1.283 |
| `dc4b978959f643b6` | 2 | 1 | reviewer | F | 17 | 3,113 | 39,271 | 449,756 | 2,433 | 2.1.283 |
| `67061c2fcfec4657` | 1 | 1 | builder | F | 10 | 2,439 | 39,642 | 259,519 | 16,833 | 2.1.284 |
| `67061c2fcfec4657` | 2 | 1 | reviewer | F | 4 | 592 | 30,391 | 28,893 | 2,650 | 2.1.284 |
| `02104725384449a5` | 1 | 1 | builder | F | 21 | 12,816 | 57,948 | 861,946 | 18,648 | 2.1.284 |
| `02104725384449a5` | 2 | 1 | reviewer | F | 5 | 3,803 | 39,171 | 67,378 | 6,813 | 2.1.284 |
| `ac2f5b9ce6ca4e79` | 1 | 1 | builder | F | 12 | 2,898 | 45,000 | 365,058 | 17,070 | 2.1.285 |
| `ac2f5b9ce6ca4e79` | 2 | 1 | reviewer | F | 5 | 1,574 | 32,836 | 59,663 | 3,092 | 2.1.285 |
| `0c0b67a320af4c3a` | 1 | 1 | builder | F | 10 | 2,275 | 37,492 | 249,172 | 17,075 | 2.1.285 |
| `0c0b67a320af4c3a` | 2 | 1 | reviewer | F | 6 | 1,448 | 31,695 | 91,598 | 2,997 | 2.1.285 |
| `7cd531cdbe4545e6` | 1 | 1 | builder | F | 8 | 3,064 | 38,168 | 180,248 | 17,065 | 2.1.285 |
| `7cd531cdbe4545e6` | 2 | 1 | reviewer | F | 6 | 4,097 | 34,392 | 92,937 | 2,872 | 2.1.285 |
| `7cd531cdbe4545e6` | 3 | 2 | builder | F | 6 | 758 | 18,050 | 118,722 | 17,874 | 2.1.285 |
| `7cd531cdbe4545e6` | 4 | 2 | reviewer | F | 15 | 6,843 | 20,658 | 424,184 | 2,150 | 2.1.285 |
| `8b19e7b399e0455c` | 1 | 1 | builder | F | 8 | 2,461 | 37,506 | 179,123 | 17,031 | 2.1.286 |
| `8b19e7b399e0455c` | 2 | 1 | reviewer | F | 11 | 5,072 | 37,134 | 267,070 | 2,970 | 2.1.286 |
| `dff94259a2894e21` | 1 | 1 | builder | F | 7 | 2,020 | 37,162 | 142,330 | 17,036 | 2.1.286 |
| `dff94259a2894e21` | 2 | 1 | reviewer | F | 8 | 4,570 | 36,233 | 161,073 | 3,039 | 2.1.286 |
| `dff94259a2894e21` | 3 | 2 | builder | F | 5 | 499 | 17,924 | 84,511 | 17,532 | 2.1.286 |
| `dff94259a2894e21` | 4 | 2 | reviewer | F | 5 | 2,932 | 15,620 | 78,642 | 3,728 | 2.1.286 |
| `82ea0ee87b7e4146` | 1 | 1 | builder | F | 7 | 1,339 | 36,262 | 140,371 | 17,035 | 2.1.286 |
| `82ea0ee87b7e4146` | 2 | 1 | reviewer | F | 4 | 1,975 | 31,130 | 28,580 | 2,932 | 2.1.286 |
| `82ea0ee87b7e4146` | 3 | 2 | builder | F | 5 | 796 | 18,463 | 85,042 | 18,079 | 2.1.286 |
| `82ea0ee87b7e4146` | 4 | 2 | reviewer | F | 6 | 1,699 | 13,767 | 105,323 | 2,344 | 2.1.286 |
| `b6dc6558b1044ee3` | 1 | 1 | builder | F | 7 | 1,476 | 36,488 | 140,977 | 17,037 | 2.1.286 |
| `b6dc6558b1044ee3` | 2 | 1 | reviewer | F | 4 | 2,516 | 32,245 | 29,437 | 2,923 | 2.1.286 |
| `b6dc6558b1044ee3` | 3 | 2 | builder | F | 6 | 600 | 18,318 | 119,686 | 18,208 | 2.1.286 |
| `b6dc6558b1044ee3` | 4 | 2 | reviewer | F | 6 | 890 | 13,426 | 106,423 | 2,173 | 2.1.286 |
| `fd5b96c30e0b44b5` | 1 | 1 | builder | F | 7 | 1,439 | 28,754 | 109,996 | 17,031 | 2.1.291 |
| `fd5b96c30e0b44b5` | 2 | 1 | reviewer | F | 4 | 2,691 | 23,211 | 20,942 | 2,980 | 2.1.291 |
| `fd5b96c30e0b44b5` | 3 | 2 | builder | F | 5 | 767 | 11,886 | 68,183 | 17,813 | 2.1.291 |
| `fd5b96c30e0b44b5` | 4 | 2 | reviewer | F | 24 | 9,501 | 21,368 | 610,880 | 1,974 | 2.1.291 |
| `fd5b96c30e0b44b5` | 5 | 3 | builder | F | 37 | 8,505 | 45,446 | 1,419,056 | 16,427 | 2.1.291 |
| `fd5b96c30e0b44b5` | 6 | 3 | reviewer | F | 4 | 2,115 | 8,347 | 37,644 | 3,646 | 2.1.291 |
| `f080dc41b7d04cd3` | 1 | 1 | builder | F | 14 | 7,587 | 82,553 | 706,013 | 16,902 | 2.1.291 |
| `f080dc41b7d04cd3` | 2 | 1 | reviewer | F | 4 | 1,572 | 22,793 | 21,446 | 1,406 | 2.1.291 |
| `f080dc41b7d04cd3` | 3 | 2 | builder | F | 12 | 4,576 | 47,504 | 357,014 | 16,558 | 2.1.291 |
| `f080dc41b7d04cd3` | 4 | 2 | reviewer | F | 18 | 4,831 | 29,051 | 529,200 | 2,102 | 2.1.291 |
| `f080dc41b7d04cd3` | 5 | 3 | builder | F | 82 | 27,204 | 115,123 | 7,126,410 | 16,820 | 2.1.291 |
| `f080dc41b7d04cd3` | 6 | 3 | reviewer | F | 6 | 3,714 | 12,112 | 93,262 | 5,831 | 2.1.291 |
| `667704af8db3434b` | 1 | 1 | builder | F | 52 | 36,247 | 100,196 | 3,268,884 | 16,890 | 2.1.291 |
| `667704af8db3434b` | 2 | 1 | reviewer | F | 7 | 3,973 | 15,071 | 124,988 | 2,834 | 2.1.291 |
| `b6c76e7122ad4f4a` | 1 | 1 | builder | F | 34 | 15,901 | 80,221 | 2,617,968 | 67,886 | 2.1.291 |
| `b6c76e7122ad4f4a` | 2 | 1 | reviewer | F | 6 | 2,494 | 14,992 | 102,296 | 11,907 | 2.1.291 |
| `a4b62cc776f541a9` | 1 | 1 | builder | F | — | — | — | — | 17,192 | 2.1.291 |
| `a4b62cc776f541a9` | 2 | 1 | builder | F | 21 | 9,670 | 66,576 | 1,277,491 | — | 2.1.291 |
| `fa8f14d9fcbb451e` | 1 | 1 | builder | F | 12 | 4,414 | 35,372 | 276,347 | 17,026 | 2.1.292 |
| `fa8f14d9fcbb451e` | 2 | 1 | reviewer | F | 11 | 2,930 | 31,696 | 219,344 | 3,083 | 2.1.292 |
| `1c6a58b59b96464e` | 1 | 1 | builder | F | 9 | 1,990 | 30,459 | 170,227 | 17,050 | 2.1.292 |
| `1c6a58b59b96464e` | 2 | 1 | reviewer | F | 6 | 3,490 | 26,454 | 72,901 | 3,038 | 2.1.292 |
| `255353092c124b08` | 1 | 1 | builder | F | 12 | 4,213 | 35,236 | 280,965 | 17,041 | 2.1.293 |
| `255353092c124b08` | 2 | 1 | reviewer | F | 17 | 8,697 | 37,576 | 417,270 | 2,922 | 2.1.293 |
| `255353092c124b08` | 3 | 2 | builder | R | 6 | 1,302 | 2,867 | 146,173 | 2,072 | 2.1.293 |
| `255353092c124b08` | 4 | 2 | reviewer | R | 3 | 186 | 1,963 | 37,576 | 3,220 | 2.1.293 |
| `2712e01e06144752` | 1 | 1 | builder | F | 12 | 4,907 | 40,960 | 301,032 | 17,015 | 2.1.294 |
| `2712e01e06144752` | 2 | 1 | reviewer | F | 11 | 5,744 | 35,756 | 219,233 | 3,008 | 2.1.294 |
| `2712e01e06144752` | 3 | 2 | builder | R | 5 | 430 | 1,414 | 124,985 | 2,496 | 2.1.294 |
| `2712e01e06144752` | 4 | 2 | reviewer | R | 3 | 651 | 1,355 | 35,756 | 3,214 | 2.1.294 |
| `66a4cfb8a7bb45bb` | 1 | 1 | builder | F | 18 | 8,903 | 47,189 | 572,175 | 17,027 | 2.1.295 |
| `66a4cfb8a7bb45bb` | 2 | 1 | reviewer | F | 9 | 7,404 | 34,641 | 171,207 | 3,837 | 2.1.295 |
| `fd3cb3cf8d064595` | 1 | 1 | builder | F | 21 | 9,239 | 49,406 | 762,242 | 17,030 | 2.1.295 |
| `fd3cb3cf8d064595` | 2 | 1 | reviewer | F | 6 | 3,148 | 33,201 | 93,218 | 3,789 | 2.1.295 |
| `fd3cb3cf8d064595` | 3 | 2 | builder | R | 7 | 2,213 | 3,873 | 258,299 | 3,276 | 2.1.295 |
| `fd3cb3cf8d064595` | 4 | 2 | reviewer | R | 3 | 685 | 1,570 | 33,201 | 4,049 | 2.1.295 |
| `f9252f2b722f4bbd` | 1 | 1 | builder | F | 19 | 5,401 | 44,868 | 622,892 | 17,023 | 2.1.296 |
| `f9252f2b722f4bbd` | 2 | 1 | reviewer | F | 17 | 6,073 | 38,599 | 480,979 | 2,933 | 2.1.296 |
| `bc8d4e24cc4744e2` | 1 | 1 | builder | F | 20 | 8,130 | 46,392 | 661,227 | 17,009 | 2.1.296 |
| `bc8d4e24cc4744e2` | 2 | 1 | reviewer | F | 5 | 1,771 | 31,517 | 59,843 | 2,859 | 2.1.296 |

## What this decides for T002
A builder's first call wrote a median of 40,960 tokens into the cache,
while the prompt Remedy wrote for it was a median of 17,033 bytes. What a call loads besides
Remedy's prompt is the part T002 attributes. The calls above differ in task, turns and version, so
they cannot attribute it; T002 therefore runs one fixed task whose first call needs no tool, once with
everything loaded and once per source switched off, in a scratch repository and in a worktree of
Remedy, with a repeat of each baseline to measure the noise: at most twenty calls, half the forty
the feature file allows.
