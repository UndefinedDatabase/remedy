
## DECISION F273 D7 (2026-09-19, reviewer, round 7) — a guard trip on a non-provider subprocess is `resource_limit`; the self-use track stops re-selecting, stops escaping and says what it is
CONTEXT: T009's R-0568 needed a ruling on which guard trips become a class, taken in this round
together with its patch (amend0917-throughput rule 3). Measured by a research helper and re-measured
by the reviewer at `00b995e7`: `FailureClass` has no `resource_limit`, and every guard seam turns a
trip into a plain `subprocess.TimeoutExpired` or `CompletedProcess` before any post-mortem writer
sees it. T012 (R-0784, R-0785, R-0786) and the F273-owned R-0838 and R-0972 are live in
`self_use_generator.py`, `self_use_findings.py` and `scripts/self_use_queue.json`.
CHOSEN: (1) THE RULING. A trip the execution guard itself reports on a subprocess that is NOT a
provider call is classified `resource_limit`, a new `FailureClass` member whose reason is
`tripped_limit=<limit>`; a provider call's wall timeout keeps `provider_timeout`, which names it
more precisely and which the seams' "the mechanism changes, the outcome does not" rule protects.
The `classify` branch sits below the typed exception, so a provider's `TimeoutExpired` can never
become `resource_limit`, and above the terminal status, because `test_failed` says the layer gave
up, not that the guard's limit is why. (2) THE WIRING. `_completed_process_from_guarded` keeps the
stdlib types exactly and attaches the guard's `tripped_limit` as an attribute on what it returns
or raises; the one writer wired is the task post-mortem: a job task's failing test command carries
its trip through the round (`test_tripped_limit`) and the task (`TaskEntry.tripped_limit`, saved
and loaded, absent in older records) into `build_task_rollup`, whose `raw_reason` then names the
limit. The other seam callers carry the attribute and nothing reads it yet; an output-size trip on a
suite that failed for its own reasons reads `resource_limit`, which is the ruling taken literally.
(3) R-0785. `append_generated_item` writes with `ensure_ascii=False`, and `scripts/self_use_queue.json`
is re-serialised ONCE by that writer, which changes no parsed value, so the next append does not
rewrite every escape in the file. (4) R-0786. The queue file's description names both sources of
an item, the operator and `packages/orchestration/self_use_generator.py`. (5) R-0838. Tier 1 skips
any finding an existing queue entry already targets, read back from the provenance the generator
stamps; an operator-written item is not excluded, because nothing machine-readable names its
target. (6) R-0784 takes the documentation route its own text allows: the generator's module
docstring states that a generated item whose fix no builder can make blocks at the approval gate by
design, and with (5) such a finding costs the track one close, not every close after it. (7)
R-0972. `describe_self_use_run_defects` answers a defect for a `stopped` job quoting its
`stop_reason` and `stop_source`, and one per task whose `final_status` is `stopped` — the field the
stop writes, since a stopped task's `status` goes back to `pending`.
ALTERNATIVES: `resource_limit` for a provider's wall trip too, rejected as less precise than
`provider_timeout`; a subclass of `TimeoutExpired` to carry the trip, rejected because the
classifier matches the stdlib name; filtering reviewer-bound findings out of Tier 1 for R-0784,
rejected because no field says which fix binds the reviewer and a guess retires findings silently.
REVERSE: restore `exec_guard.py`, `failure_postmortem.py`, `pingpong_loop.py`, `pingpong_job.py`,
`self_use_generator.py`, `self_use_findings.py`, `scripts/self_use_queue.json` and `T2_F085.md` from
`00b995e7`, drop the tests this round added or changed, and delete this paragraph.
