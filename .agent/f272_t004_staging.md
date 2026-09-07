# F272 T004 — how the classic-store deletion is staged

Feature F272 (One world completion), task **T004 — delete the classic runner**.
Every reading below was COMPUTED at commit `81b2dc86` — the round 23 handback
commit — in the primary checkout with `git status --porcelain` empty. The
199-file consumer list it cross-references is not re-measured here: it is the
stored one in `.agent/f272_t004_deletion_inventory.md`, taken at `230c5f2c`, and
the cluster list is the one `docs/roadmap/features/T2_F260.md`'s Design section
carries. What is new here is the CROSS-REFERENCE between them and the readings
of the rail modules, both taken at `81b2dc86`.

This file answers the ONE question `.agent/f272_t004_deletion_inventory.md`
deliberately left open. That file measured WHAT references the classic job store
— 199 files — and closed by saying that "the division of T004 into rounds, the
order those rounds take, and which files travel together in a commit are the
NEXT BLOCK'S JOB". This is that answer, and it is a measurement rather than a
preference. It is recorded as DECISION F272 D14 in
`docs/roadmap/features/T2_F272.md`; this file carries the numbers that ruling
rests on.

## 1. Twelve of the 72 production consumers are deleted by T005 anyway

The cluster list in `docs/roadmap/features/T2_F260.md`'s Design section names 24
modules. Twelve of them are also classic-store consumers, so porting them onto
the unified record would be work thrown away by the round that deletes them:

```
DIES  packages/orchestration/builder_routing.py
DIES  packages/orchestration/candidate_quality.py
DIES  packages/orchestration/dogfood_run.py
DIES  packages/orchestration/external_builder_sandbox.py
DIES  packages/orchestration/local_candidate_generator.py
DIES  packages/orchestration/overnight_executor.py
DIES  packages/orchestration/overnight_mission.py
DIES  packages/orchestration/overnight_readiness.py
DIES  packages/orchestration/provider_trust.py
DIES  packages/orchestration/provider_trust_verification.py
DIES  packages/orchestration/repair_loop_v2.py
DIES  packages/orchestration/review_bundle.py
```

**72 production consumers minus those 12 leaves 60 that must MIGRATE**, beside
the 127 under `tests/`. That is the real remaining size of T004, and it is the
figure the next session's scope report should use rather than 199.

Twelve is not enough to reorder the tasks. T005 stays LAST, exactly as the
Orchestrator brief requires, because deleting the cluster first would shrink
T004 by 17 percent while breaking the brief's one hard rule.

## 2. The next-action rails are not blocked by the STORE

The eight modules carrying the sixteen `remedy job run-next` advertisements were
each checked against the store inventory. SIX OF THE EIGHT DO NOT TOUCH THE
CLASSIC STORE AT ALL:

```
cockpit.py            classic-store consumer: False
timeline.py           classic-store consumer: False
trust_report.py       classic-store consumer: False
dashboard.py          classic-store consumer: False
brain_detail.py       classic-store consumer: False
autonomy_loop.py      classic-store consumer: False
agent_loop.py         classic-store consumer: True
long_run_executor.py  classic-store consumer: True
```

They are handed a `Job` by their callers and render it. So what blocks them is
the RECORD TYPE their callers pass, not the store they never open. T004 is
therefore staged BY CALLER, not by module: a round takes a classic-store
consumer, moves it to `load_job_plan`, and adapts every renderer it feeds in the
same commit range.

The rails' coupling to the cluster is almost nil, which is why they can be moved
before T005 rather than after it:

```
cockpit              -> (none)
timeline             -> (none)
trust_report         -> (none)
dashboard            -> ['worker_recommend']
brain_detail         -> (none)
agent_loop           -> ['worker_recommend']
autonomy_loop        -> ['worker_recommend']
long_run_executor    -> (none)
```

`worker_recommend` is on the cluster list, so the three modules that reach it
lose that call in T005 and must not have it ported in T004.

## 3. Why `job.run-next` cannot die the way `job.run-loop` did

Rounds 20 through 22 deleted `job run-loop` and settled its advertisements by
REWORDING them — naming the deleted command without spelling it as an
invocation. That worked because every surviving `run-loop` site was PROSE: a
sentence in `docs/system/architecture.md` and a migration-table row in
`docs/guides/`, both of which describe history.

The sixteen `run-next` sites are not prose. Every one of them is LIVE OPERATOR
GUIDANCE — the string a cockpit, a dashboard or a brain view prints under
"Run the next pending task:" — and each is produced inside a function that has a
classic job in hand. Read at `81b2dc86`, `cockpit._derive_next_action` is typed
`(job: Job, signals)` and branches on `job.tasks` and `RunState.PENDING`;
`trust_report`, `brain_detail`, `dashboard` and `autonomy_loop` do the same.
Rewording those to avoid naming a command would leave a cockpit that tells the
operator to continue and then does not say how, which is a product regression
rather than a repair.

The round 23 plan's Next Step 2 said the store migration is "NOT a prerequisite"
for deleting `job.run-next`, citing the `run-loop` precedent. THAT SENTENCE IS
CORRECTED HERE: it is true only for advertisements that are prose, and none of
these sixteen is. `job.run-next` dies WITH the migration of the modules that
advertise it.

## 4. What this file does not decide

Which caller travels in which round, and in what order the 60 migrate. That is
per-round staging and it needs the caller graph read one consumer at a time,
which no single measurement settles. What is settled is the SHAPE — by caller,
not by module — the EXCLUSION of the twelve cluster-bound files, and the
ordering of `job.run-next` behind the rails rather than ahead of them.
