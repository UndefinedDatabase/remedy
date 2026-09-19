
## DECISION F273 D17 (2026-09-19, reviewer, round 17) — the operator attestation writer and its export overlay go while the closure producer stays, and the queue, the goal-driven path and `worker status` go without raising a ceiling
CONTEXT: DECISION F273 D15 (4) held R-0914 and the worker queue. Research helpers measured both at
`b22fe3bc` and the reviewer re-ran them on its dry-run tree over `9e753ffc`. `attest_operator_repair`
in `packages/orchestration/repair_attest.py` has test callers only, but `create_manual_completion_bundle`
in `packages/orchestration/job_evidence.py`, the closure evidence producer
`docs/roadmap/STATUS_closure_protocol.md` names, reaches `manual_attestation.py` and the attestable-source
policy and safe-diff hashing of `repair_attest.py`. The export's attestation overlay in `job_evidence.py`
read only what `attest_operator_repair` wrote. For the queue, the deleted modules emitted event names that
surviving code still read, and the prototype held earlier raised `_COUPLING_CEILING` to declare them,
which this feature's Acceptance forbids.
CHOSEN: (1) R-0914. `attest_operator_repair` and every symbol only it or tests reached are deleted, with
the export's attestation overlay, its finalize step and the regression-coverage map only that step read,
and their tests; `manual_attestation.py` and everything `create_manual_completion_bundle` reaches stay,
and a scratch run of the producer still wrote a bundle the manifest validator accepted. An export of a job
with no persisted attestation is unchanged apart from timestamps. `docs/system/vocabulary.md` says an
operator repair is attested no longer, and R-0914's Acceptance line gains the branch that keeps the
module (§4 item 7). (2) R-0927, R-0928. `job run` and `job stop` replace the queue: `worker_queue.py`,
`task_execution.py`, `autorun.py` and `source_context.py`, which only `autorun.py` called, are deleted
with their tests, and so are `worker status`, the cockpit's worker section and its UI client. The readers
of the event names only those modules emitted go with them, in `event_replay.py`, `proof_chain.py`,
`ui_server.py`, `ui_view_model.py`, the humanize catalog and `actionClass.ts`; fields they alone fed read
as absent, and a test pins the project summary's confidence at `low`. `_COUPLING_CEILING` stays at 1.
The coupling ratchet and the catalog contract also read a name held in a local before it is emitted,
R-0991's class, which keeps `test_run_completed` and adds four catalog entries. The permission guard over
`apply_structured_patch` is re-pointed at its three surviving callers rather than dropped. (3) R-0992,
the memory-candidate store losing its only writer with `autorun.py`, is registered for this feature and
taken with R-0977.
ALTERNATIVES: deleting `manual_attestation.py` as R-0914's FIX first named, rejected because it would
break this feature's own closure; keeping the overlay, rejected because nothing writes its input; raising
the ceiling, rejected by the Acceptance; giving `worker status` a live source, rejected because no worker
exists to report on once the queue is gone.
REVERSE: restore the touched files from `9e753ffc`, and delete this paragraph.
