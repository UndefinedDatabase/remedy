# Autonomy levels (v1)

The autonomy level says who may START work on Remedy's own initiative. It never says what a job may
do once it runs: every approval, fence, budget and watchdog applies at every level. It lives in
`packages/orchestration/autonomy_gate.py` (F078, DECISIONs F078 D1 to D3 and D5).

Its levels are spelled `L2` to `L5`. They are not the 0 to 7 scale of
`packages/orchestration/autonomy_readiness.py`, which measures infrastructure readiness.

## The levels and the one check

| Work that comes from | L2 | L3 | L4 | L5 |
|---|---|---|---|---|
| your own command (`manual`) | yes | yes | yes | yes |
| the mission loop (`orchestrator`) | no | yes | yes | yes |
| an order file started without you (`order-file`) | no | no | yes | yes |
| an idea draft (`idea`) | no | no | no | yes |

`AUTONOMY_START_MATRIX` is that table, and `autonomy_may_start(origin, level)` is the one check
every starting seam asks. Its answer carries a plain sentence either way; a denial names the lowest
level that would allow the start. Remedy has no scheduler for order files and no idea engine yet,
so nothing starts work from those two origins today; the matrix covers them so the seam a later
feature builds has one check to call, and for idea drafts that seam is ready: `claim_idea_start`,
below.

Your own commands do not ask the check. `remedy do`, `remedy job run` and the other commands you
start yourself are origin `manual`, which every level allows, so asking would add a configuration
read to every command and decide nothing.

## Setting the level

The level is set in `remedy.toml` under `[remedy.autonomy]`, project settings before user
settings, and never through the environment: a level change must leave a file edit behind.

| Key | Meaning |
|---|---|
| `autonomy.level` | `L2` (the default) to `L5` |
| `autonomy.gauntlet_evidence` | the `matrix.json` of a gauntlet attempt that passed; needed from `L3` |
| `autonomy.change_adr` | the file that records why the level last changed; needed for every change |
| `autonomy.idea_max_effort` | the largest effort band, `low` (the default), `medium` or `high`, of an idea draft `L5` starts by itself |
| `autonomy.idea_starts_per_day` | how many idea drafts `L5` starts by itself in one UTC day, a whole number of at least 0 (default 1) |
| `autonomy.idea_usd_per_day` | the estimated dollars of the idea drafts `L5` starts by itself in one UTC day, a number of at least 0 (default 1.0) |

A relative path is read from the folder of the config file that sets it. `load_autonomy_policy`
refuses, with a sentence naming what is wrong: a key set by an environment variable; a level
outside `L2` to `L5`; `L3` or higher without gauntlet evidence, with evidence that does not exist,
that Remedy cannot read as a gauntlet matrix, or that records a gauntlet that did not pass; and a
change of level without a decision record, or with one that does not exist.

A change is a level that differs from the last one recorded for the same config file. Each
accepted change is one line of `<data root>/autonomy/level_changes.jsonl`: when, which file, from,
to, the decision record and the source. A level that no file sets is the default `L2` and is never
a change.

## Seeing the level

`remedy status` ends with the level and where it is set, for example `Autonomy: level L2, the
default`. When starts wait, it adds how many and the command that takes the oldest:
`  1 start deferred by the autonomy level` and `  Next: remedy mission run <mission> --project
<project>`. A configuration the gate refuses is shown as `Autonomy: the configured level cannot be
used.` followed by the refusal's sentence. With `--json` the same reading is the key `autonomy`:
`level`, `config_path`, `error` and `deferred_starts`. `remedy status` reads the level without
writing anything, through `autonomy_status_summary`, so a change it sees is recorded only when a
command that starts work loads it.

`remedy mission run` prints `Autonomy level: <level>` under the mission's id and answers
`autonomy_level` with `--json`. It loads the level for the run it starts, so an accepted change of
level is recorded then.

## The mission loop

`remedy mission run` loads the level before the loop starts; a refused configuration ends the
command before any provider call. The command is your own start of the first job the run
dispatches. Every further dispatch in the same run comes from the mission loop and is checked
first in `dispatch_milestone_job`, before any job exists. At `L2` the run therefore starts one job
and then ends as `deferred_by_autonomy`, naming the command that starts the waiting job: the same
`remedy mission run <mission>` again. At `L3` and higher the loop starts its jobs as before.

Every refused start is one `deferred` line of `<data root>/autonomy/deferred_starts.jsonl`, and the
next start of the same mission writes one `taken` line that closes it; `open_deferred_starts` reads
the ones still waiting. A resume move is not a start: it continues a job an earlier start began.

Remedy deliberately does not check the gauntlet runner, which calls the loop outside a start
scope: its campaign is the evidence `L3` needs, and it runs only by your own command against its
own data root. `tests/orchestration/test_autonomy_seams.py` names
every caller of the loop and of the dispatch, so a new one cannot arrive unchecked.

## The caps of L5

`claim_idea_start(policy, idea_id, *, effort_band, estimated_usd)` is the one call an idea engine
makes before it starts an idea draft by itself. It asks the matrix first, so below `L5` the draft
waits with the matrix's sentence. At `L5` it applies the three caps in order, and the first that
refuses wins: the effort band against `autonomy.idea_max_effort`, the drafts already started
today against `autonomy.idea_starts_per_day`, and today's estimated dollars with this draft against
`autonomy.idea_usd_per_day`. A cap that is not a number of at least 0 is refused as a bad
configuration. Every refusal is one `deferred` line and every allowed start one `started` line of
`<data root>/autonomy/idea_starts.jsonl`, so a refused draft waits for you and is never lost.
Nothing calls it yet: the idea engine (F063) is not built.

## What the proof covers

`tests/orchestration/test_autonomy_levels.py` loads each level from a real `remedy.toml` and drives
both seams, so each level shows exactly the starts its row adds; `L4` behaves as `L3`, because its
increment, the recurring order file, has no starter yet, and a test there fails the day a module
other than the gate names that origin or the idea origin. It also re-runs the tests of the gates a
mission meets — the watchdog's pause, the iteration limit, your stop, the escalation after two
blocked completions and the audited approval of a waiting plan — inside a start scope at `L5`, and
each still fires with every start the check was asked about allowed. Budgets and fences are not
re-run there: they act inside one job's run, which the level never reaches, since it only decides
whether the job starts.
