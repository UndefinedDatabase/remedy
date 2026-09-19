
## DECISION F273 D13 (2026-09-19, reviewer, round 13) — the loop stamps each entry it prints, `mission show` renders the ledger, `mission list` filters by status, tips name real ids, `replan` goes, and the dead event readers and the level-4 inspection signals go with it
CONTEXT: R-0930, R-0929, R-0904, R-0970, R-0915, R-0919, R-0920, R-0905 and R-0907 each needed a
choice between routes their texts allow, taken in the round that lands the patch (amend0917-throughput
rule 3). Measured by research helpers and re-measured by the reviewer's dry run at `b3baf7d5`:
the loop's `_record` appends an entry with no time, and only the disk copy is stamped; `mission show`
reads the ledger only for a paused mission's trips; `mission list` has no status filter while 25
feature files carry a `mission list --status planned` heir sentence; six tips print `<job_id>` or
`<intent_id>`; `job_plan.replan` has test callers only and the six rejected-plan refusals name no
next step; the cockpit reads `do_continue_stopped`, whose emitter F275 deleted; the event-name
recovery reads only an emit call's first argument; and nothing emits `git_status_read`,
`run_contract_inspected` or `token_policy_inspected` while readers and readiness level 4 still wait
for them.
CHOSEN: (1) R-0930. `_record` stamps `recorded_at` itself, so the printed and the stored entry carry
one time. (2) R-0929, the route its fix names: `mission show` renders the whole ledger after the
chain, and its JSON carries it; a mission never run prints nothing new. (3) R-0904. `mission list
--status` takes the four stored statuses and `planned`, which is derived at list time — an active
mission no linked job has started — so the heir sentence holds as written and no feature file
changes. (4) R-0970. Every tip in `timeline.py` and `trust_report.py` names the real job and intent
ids, one command per intent; the `do` tip, which has no id, names its value in words. (5) R-0915.
`replan` and `ReplanRejectedError` are deleted with their tests, and the six refusals print one
next step: give the order anew with `remedy do`, with `--plan-only` to read the new plan first. The
word `replan` survives only where it names a mission's plan, a different, living concept. (6)
R-0919. The cockpit continuation section keeps `available` and loses its event half, its client
fields and their fixtures. (7) R-0920. The recovery reads every positional string of an emit call,
a call whose name holds the word `emit`, and a module's own helper that forwards a parameter to one;
a test finds a name only a helper emits. (8) R-0905. The three readers of `git_status_read` are
deleted, and with them the `repo_dirty` decision type and the `dirty_repo_blocks_level` reason code
they produced, as the finding's text names. (9) R-0907. Both inspection signals are dropped from
readiness level 4 rather than given emitters, and the six test-only exports are deleted with their
tests; the architecture document says so, and still documents both events because old run logs
carry them. The coupling ceiling falls from 4 to 1, since no new dead name surfaced. (10) R-0989,
found in this round, is registered for the tips in `apps/cli/commands/job.py` and
`packages/orchestration/cockpit.py` and is the next round's.
ALTERNATIVES: a `--ledger` flag or a new word for R-0929, rejected because the finding names the
existing view; a stored `planned` status, rejected because nothing would ever write it; emitters
for the two inspection events, rejected because no surviving command inspects a contract or a
policy; keeping `repo_dirty` with no producer, rejected as a type nothing can create.
REVERSE: restore every file the two diffs touch from `b3baf7d5`, and delete this paragraph.
