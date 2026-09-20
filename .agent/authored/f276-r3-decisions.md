
## DECISION F276 D4 (2026-09-20, reviewer, round 3) — an orphaned staging copy is reclaimable only when the operator asks for it by name, and the verdict is taken twice
CONTEXT: R-1002, registered in this round's first commit, measures what T002 as built can actually
free on the machine the feature was written for: 284536286695 bytes of the 922931683643 in
`job_workspaces`, with 638395396948 refused because 1884 staging copies have no job record at all.
The feature file's own OPERATOR STEP expects `.data` under 10 GB afterwards. A research helper
prototyped the repair at `94441e34` in its own worktree; the reviewer re-applied it, re-ran the
gates and re-proved three of its mutations.
CHOSEN: (1) `remedy data reclaim --orphans`, a flag declared `is_flag=True` because `grouped.py`
special-cases only `--json` by name, default OFF. With it, a DIRECT CHILD of `job_workspaces` whose
name starts with `staging_`, whose remainder is non-empty, whose job id resolves to NO readable
record, and whose own mtime is at least `ORPHAN_MIN_AGE_DAYS` old becomes a candidate; without it,
nothing changes, which one test pins by comparing the serialised default JSON of a seeded root
byte for byte against the document it produced before. (2) The floor is 1.0 day, and it insures
against exactly one state: a staging directory CREATED while its record is still being written. A
directory that was just created has a fresh mtime of its own, so the child's own `lstat` is the
right reading and a subtree walk would answer a different question. An orphan under the floor is
refused under its own reason, `orphan_too_young`, so the operator sees it rather than losing it
from the report. (3) The orphan verdict is re-taken AT DELETION, not trusted from the plan: for a
candidate whose state reads `no_record`, `apply_reclaim` re-reads the record and the mtime and
refuses — `job_unresolved` if a record has appeared, `orphan_too_young` if the floor is no longer
met. Every other candidate keeps the path it had. This is the one verdict that authorises deleting
a directory nothing points at, so it is the last one to take on trust; the cost is one record read
and one `lstat` per orphan against hundreds of gigabytes of deletion. (4) The machine-readable
discriminator is the candidate's `job_state`, which reads `no_record` — a token no `RunState` member
spells, pinned by a test — rather than a new JSON key, because a new key would change the default
document the byte-identity test exists to protect. (5) The DEFAULT HUMAN preview gains one line
naming how many paths are refused as `job_unresolved`, their bytes, and that `--orphans` can
reclaim the ones no record owns; the JSON gains nothing. An operator looking at 638 GB of refusals
must not have to read the source to learn the flag exists. The line's count is of the refusals, not
a forecast of what `--orphans` would take, and its wording says so: forecasting would mean a second
walk of a 923 GB tree. (6) A record that EXISTS but cannot be parsed is never an orphan, so a
staging copy with a corrupt `job.json` keeps its scratch forever and no slice of F276 reaches it.
(7) Every numeral this round writes into prose names its date and its denominator, because the
93-per-cent and 98-per-cent readings of DECISION F276 D3 are both correct about different
denominators and nothing on the page said so.
ALTERNATIVES: making orphans candidates by default, rejected because "no record" is read from the
filesystem and a default that deletes what it cannot explain is the wrong default for a command
that frees hundreds of gigabytes; an `"orphan": true` key on every candidate, rejected under (4);
a subtree mtime walk, rejected under (2); leaving the backlog to a future feature, rejected because
R-1002 is High and the operator's disk is the reason the feature exists.
REVERSE: restore `packages/orchestration/data_reclaim.py`, `apps/cli/commands/data_cmd.py`,
`apps/cli/command_catalog.py`, `tests/cli/test_data_cmd.py`,
`tests/orchestration/test_data_reclaim.py`, `docs/system/architecture.md` and
`docs/roadmap/features/T2_F276.md` from `94441e34`, and delete this paragraph.
