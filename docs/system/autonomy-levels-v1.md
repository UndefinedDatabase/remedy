# Autonomy levels (v1)

The autonomy level says who may START work on Remedy's own initiative. It never says what a job may
do once it runs: every approval, fence, budget and watchdog applies at every level. It lives in
`packages/orchestration/autonomy_gate.py` (F078, DECISIONs F078 D1 and D2).

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
feature builds has one check to call.

## Setting the level

The level is set in `remedy.toml` under `[remedy.autonomy]`, project settings before user
settings, and never through the environment: a level change must leave a file edit behind.

| Key | Meaning |
|---|---|
| `autonomy.level` | `L2` (the default) to `L5` |
| `autonomy.gauntlet_evidence` | the `matrix.json` of a gauntlet attempt that passed; needed from `L3` |
| `autonomy.change_adr` | the file that records why the level last changed; needed for every change |

A relative path is read from the folder of the config file that sets it. `load_autonomy_policy`
refuses, with a sentence naming what is wrong: a key set by an environment variable; a level
outside `L2` to `L5`; `L3` or higher without gauntlet evidence, with evidence that does not exist,
that Remedy cannot read as a gauntlet matrix, or that records a gauntlet that did not pass; and a
change of level without a decision record, or with one that does not exist.

A change is a level that differs from the last one recorded for the same config file. Each
accepted change is one line of `<data root>/autonomy/level_changes.jsonl`: when, which file, from,
to, the decision record and the source. A level that no file sets is the default `L2` and is never
a change.

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
