# Self-health v1: Remedy checks its own health

> Status (F199, 2026-10-13): built in part. The command and four checks exist; the other checks
> and the crash report are later slices of F199. DECISION F199 D1 in `.agent/decisions.md` holds
> the rules this page states; the feature is `docs/roadmap/features/T12_F199.md`.

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
| `staging_copies` | The size of leftover staging copies that `remedy data reclaim --orphans` would free, against `data.reclaim_warn_gb` | The size is at or above the warning level, or cannot be measured | Never | Preview with `remedy data reclaim --orphans`, then free with `--apply` |
| `disk` | The free disk, as the budget guard reads it, against `budget.min_free_disk_bytes` | The free disk cannot be read | The free disk is below the configured floor | Free disk space under the data root, or lower the floor; `remedy data reclaim --orphans` previews what Remedy's own staging copies would free |

With no floor configured, the `disk` check passes and says so. With no ledger yet, the `ledgers`
check passes and says so.

## Output

As text:

```
Remedy health: WARN
  [PASS] config: every configured value has its declared type
  [PASS] ledgers: no token ledger exists yet
  [WARN] staging_copies: 6.0 GB of staging copies can be freed, at or above the warning level of 5 GB
         fix: preview them with `remedy data reclaim --orphans`, then free them with `remedy data reclaim --orphans --apply`
  [PASS] disk: 52428800000 bytes free; no floor is configured (budget.min_free_disk_bytes)
```

With `--json`, the answer is one object. It carries `schema_version`, `ok`, `verdict` and `checks`;
each entry of `checks` has exactly the keys `check`, `level`, `detail` and `hint`. When a check is
FAIL, the object has `ok` false, `error` `health_failed` and a `message` such as `1 of 4 health
checks failed`, still carries `verdict` and `checks`, and the command exits 1.

## Not yet

These are later slices of F199 and do not exist today:

- the checks `snapshots`, `worktrees`, `providers` and `crash_reports`;
- the crash report, written when a Remedy command ends on an exception nothing caught;
- the supervisor's health route, which would answer the same checks over its socket.
