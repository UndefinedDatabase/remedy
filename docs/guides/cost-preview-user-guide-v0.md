# Cost preview per command — user guide (v0)

Some commands can spend real money before they finish. `remedy job run` is the
first one Remedy wires to a cost preview (F114): before an expensive run
starts, it prints an estimate and, in attended mode, asks for confirmation
above a configured threshold. For the numbers Remedy prints AFTER a run, see
[cost-report-user-guide-v0.md](cost-report-user-guide-v0.md); this guide is
about the estimate shown BEFORE.

## What you see

```
$ remedy job run abc12345
estimated $0.0120-$0.0480 (basis: class defaults (low/medium token bands) x price_basis_usd_per_1k_tokens=0.003)
Continue running 'job.run'? [y/N]
```

The line always carries a `basis:` label — never a bare number — because a
number with no stated source cannot be checked. When the estimate cannot be
computed at all (an unrecognised task class, or no price basis configured),
the line says so instead of guessing:

```
estimated cost unavailable (basis: estimate_unavailable)
Continue running 'job.run'? [y/N]
```

An unavailable estimate is treated as expensive — A9 of
[T3_F114.md](../roadmap/features/T3_F114.md) is "unknown is treated as
expensive, never guessed" — so it always asks for confirmation, the same as a
real estimate above the threshold. Below the threshold, nothing prints a
question at all; cheap runs never interrupt.

## Skipping the prompt

- `--yes` skips the confirmation and proceeds, printing an audited line so the
  skip is visible in evidence:
  ```
  $ remedy job run abc12345 --yes
  estimated cost unavailable (basis: estimate_unavailable) - proceeding without prompt (--yes)
  ```
- `--unattended` (the loop's unattended mode, F051) skips it the same way —
  neither flag bypasses budget limits or the escalation log, only the
  cost-preview prompt itself.
- With neither flag, on a pipe (no terminal attached to stdin) the command
  never hangs waiting for an answer nobody can give. It exits immediately:
  ```
  $ echo | remedy job run abc12345
  Error: estimated cost unavailable (basis: estimate_unavailable). stdin is not a terminal, so there is nobody to confirm. Pass --yes to run 'job.run' without a prompt.
  $ echo $?
  2
  ```

## The confirmation threshold

`cost_preview.confirm_above_usd` sets the USD figure the estimate's high end
must exceed before a confirmation is required at all. Configure it like any
other Remedy setting:

- environment variable `REMEDY_COST_PREVIEW_CONFIRM_ABOVE_USD`
- `remedy.toml`:
  ```toml
  [remedy.cost_preview]
  confirm_above_usd = 0.5
  ```
- default: `0.5` (F114 Design: "around half a dollar")

A malformed or non-positive configured value falls back to the default rather
than blocking every command — this threshold is a UX setting, not a budget
limit, so a bad config value degrades safely instead of refusing every run.

## What is wired so far

Only `remedy job run` carries a cost preview today; it is the command the
catalog marks `is_expensive`. Real cost bands for `job.run` do not exist yet
either — its estimate is always `estimate_unavailable` until a future round
supplies real task-class data, which is why every example above shows the
unavailable case. Marking further commands `is_expensive` and giving `job.run`
a real band are both separate, later work.

## Related

- [T3_F114.md](../roadmap/features/T3_F114.md) — the feature brief (goal,
  design, acceptance).
- [token-economy-user-guide-v0.md](token-economy-user-guide-v0.md) — the
  budget estimates this preview's arithmetic shares with.
- [cost-report-user-guide-v0.md](cost-report-user-guide-v0.md) — the actuals
  report, for what a run really cost after it finished.
