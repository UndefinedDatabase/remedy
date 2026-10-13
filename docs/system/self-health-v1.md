# Self-health v1: Remedy checks its own health

> Status (F199, 2026-10-13): built in part. The command and its seven checks exist; the check
> `crash_reports` and the crash report are later slices of F199. DECISIONs F199 D1 and D2 in
> `.agent/decisions.md` hold the rules this page states; the feature is
> `docs/roadmap/features/T12_F199.md`.

## What it does

`remedy doctor health` looks at Remedy itself and prints one line per check, each PASS, WARN or
FAIL, with a one-line fix under every check that has something to fix. It only reads. It writes no
file, opens each cost ledger without the right to change it, and calls no provider and no network.

The exit code is 0 when no check is FAIL, whether the worst result is PASS or WARN, and 1 when any
check is FAIL. A WARN is told to the operator and never enforced. A CI step that runs the command
therefore stops on a FAIL and carries on past a WARN.

## The checks

The checks run in this order.

| Check | What it reads | WARN when | FAIL when | The hint |
|---|---|---|---|---|
| `config` | The settings Remedy resolves from `remedy.toml` and the environment | The loader reported a warning, for example an unknown key | A value does not have its declared type, or the settings cannot be read | Run `remedy config validate` to list every problem, then correct the named key |
| `ledgers` | Each project's token ledger under the data root | Never | SQLite's own integrity check finds a damaged ledger (the detail names it) | Move the named ledger aside, for example to `ledger.sqlite.bad`; Remedy starts an empty one and the moved file keeps the old cost history |
| `snapshots` | The 20 newest workspace snapshots under the data root: each manifest against its recorded hash and each recovery file against its recorded hash | Never | A snapshot's manifest does not match its hash, or a recovery file is missing or changed (the detail names the snapshot folder) | Run `remedy snapshot inspect <job id> <snapshot id>` for each named snapshot; a damaged snapshot cannot restore the files it recorded, so no revert should rely on it |
| `worktrees` | `git worktree list` of each registered project's repository on this machine | A worktree is prunable because its folder is gone, or git cannot read a repository (the detail names them) | Never | Run `git worktree prune` in each named repository; it forgets the worktrees whose folders are gone and changes no other file |
| `providers` | Whether the `claude` command, the `ANTHROPIC_API_KEY` variable and the `ollama` command are present; no provider is called and the key is never printed | None of the three is present | Never | Install the Claude Code command line or Ollama, or set `ANTHROPIC_API_KEY`; `remedy worker doctor` checks a worker's own tooling |
| `staging_copies` | The size of leftover staging copies that `remedy data reclaim --orphans` would free, against `data.reclaim_warn_gb` | The size is at or above the warning level, or cannot be measured | Never | Preview with `remedy data reclaim --orphans`, then free with `--apply` |
| `disk` | The free disk, as the budget guard reads it, against `budget.min_free_disk_bytes` | The free disk cannot be read | The free disk is below the configured floor | Free disk space under the data root, or lower the floor; `remedy data reclaim --orphans` previews what Remedy's own staging copies would free |

With no floor configured, the `disk` check passes and says so. With no ledger yet, the `ledgers`
check passes and says so; so do `snapshots` with no snapshot and `worktrees` with no registered
repository. A machine with no model service gets a WARN from `providers` and still exits 0, because
a machine that only builds and tests is healthy without one (DECISION F199 D2).

## Output

As text:

```
Remedy health: WARN
  [PASS] config: every configured value has its declared type
  [PASS] ledgers: no token ledger exists yet
  [PASS] snapshots: no workspace snapshot exists yet
  [PASS] worktrees: 1 repositories checked; no worktree is prunable
  [WARN] providers: no provider can be reached: claude-cli needs the claude command on the path; claude needs ANTHROPIC_API_KEY set; ollama needs the ollama command on the path
         fix: install the Claude Code command line (claude) or Ollama, or set ANTHROPIC_API_KEY; `remedy worker doctor` checks a worker's own tooling
  [WARN] staging_copies: 6.0 GB of staging copies can be freed, at or above the warning level of 5 GB
         fix: preview them with `remedy data reclaim --orphans`, then free them with `remedy data reclaim --orphans --apply`
  [PASS] disk: 52428800000 bytes free; no floor is configured (budget.min_free_disk_bytes)
```

With `--json`, the answer is one object. It carries `schema_version`, `ok`, `verdict` and `checks`;
each entry of `checks` has exactly the keys `check`, `level`, `detail` and `hint`. When a check is
FAIL, the object has `ok` false, `error` `health_failed` and a `message` such as `1 of 7 health
checks failed`, still carries `verdict` and `checks`, and the command exits 1.

## Not yet

These are later slices of F199 and do not exist today:

- the check `crash_reports`;
- the crash report, written when a Remedy command ends on an exception nothing caught;
- the supervisor's health route, which would answer the same checks over its socket.
