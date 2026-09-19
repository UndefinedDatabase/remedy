
## DECISION F273 D6 (2026-09-19, reviewer, round 6) — persisted actuals carry money as version 2; the door refuses a blank answer as a shape error; its import guard reads the transitive closure
CONTEXT: DECISION F273 D5 (5) ruled R-0753 onto the route its text names. T008 (R-0745, R-0685)
and T014 (R-0374, R-0378) were prototyped by research helpers and re-measured by the reviewer at
`6c87c133`: R-0374 was repaired at `0d798e4f`; R-0745, R-0685 and R-0378 are live. T009's R-0568
is live too and needs a ruling on which guard trips become a class, so it is taken by the next round
with that ruling and its patch together (amend0917-throughput rule 3).
CHOSEN: (1) R-0753. `budget_guard.py` adds persisted actuals version `2.0.0`, whose closed field set
adds `measured_cost_usd` (null when unpriced, never 0.0), `priced_call_count` and
`unpriced_call_count`; `1.0.0` keeps decoding with its money absent, an unknown field is still
rejected, and corrupt money is rejected at the decode. `run_job` persists the money of the counters
its latest safe point evaluated and reads no ledger to do it; `counters_from_persisted` carries the
money, so the digest's cost basis reaches `actual` and `lower_bound`, and the run report gains a
`- Money:` line. `remedy job budget` with a cost limit now always reads the ledger, the fresher
figure, and falls back to the persisted money only when that read fails. What stays unreached is
registered as R-0986, owned by F273: the live counters hold money only for a job with a cost limit
and only for runs already mirrored. (2) R-0745. `TestCommandDoorImportGuard` gains a test walking
the door's transitive module-level closure and asserting its intersection with the forbidden set
EQUALS a recorded accepted set, `packages.common.secure_fs` and `shutil`, each with its route; the
`subprocess` import in `packages/orchestration/evidence_index.py` moves into its two `_git`
helpers, so the closure no longer reaches it. (3) R-0685. The door's `_read_command_payload`
refuses a `decision.resolve` whose string answer is blank as a 400 on field `answer`, audited
`rejected_shape`, before any decision is read, so an open decision is never answered "not open";
`answer_task_decision` refuses a blank answer too and leaves the decision open, as the defence for
every other caller, with its own unit test. An absent or non-string answer still degrades to "" and
keeps its pinned 409. (4) R-0374 is booked as repaired by `0d798e4f`. (5) R-0378. A one-line WHY
above `is_reject` names the `provider_error:` prefix dependency, and a seam test proves a prefixed
reviewer rate limit is retried.
ALTERNATIVES: a reader-side ledger composition for R-0753, rejected in D5; a 409 carrying a new
message for R-0685, rejected because a blank answer is malformed input, not a state conflict.
REVERSE: restore `budget_guard.py`, `pingpong_job.py`, `run_report.py`, `job.py`,
`evidence_index.py`, `escalation.py`, `ui_server.py`, `pingpong_loop.py` and the two `apps/ui/src/api`
files from `6c87c133`, drop the tests this round added or changed, and delete this paragraph.
