
## DECISION F273 D16 (2026-09-19, reviewer, round 16) — the repair loop goes whole, the catalog contract reads forwarding helpers, `job evidence` refuses by name, and R-0977 waits for its defect
CONTEXT: DECISION F273 D15 (4) held the repair-loop prototype on two rulings, and the third session
measured both with research helpers and the reviewer's dry run at `b22fe3bc`. The "module stays whole"
clause R-0923 cites is DECISION F261 D17's rule that a F261 prune round deletes no package module; it
bound F261's rounds, and R-0923's own FIX names deleting the attempt store's readers and writer as its
second branch. The two cockpit labels the prototype dropped, `contract_decision` and
`repair_loop_stopped`, are still emitted by the `_emit` helpers of `test_execution_service.py` and
`builder_bridge.py`; the prototype dropped them only because the catalog contract cannot see a helper,
which R-0991 records.
CHOSEN: (1) R-0923, R-0925, R-0926, R-0918. `packages/orchestration/repair_loop.py` and
`packages/orchestration/repair_request_builder.py` are deleted with their tests, the attempt store's
readers in `mission_readiness.py` and `self_dogfood.py`, and the cockpit's `repair` and
`repair_request` sections with their fixtures; the statuses nothing set go with the module, and
`docs/system/repair-loop-v1.md` says a repair is only ever a phase of a run and an attempt has no
post-apply state. The edited readiness and self-dogfood lines gain tests that pin them. (2) R-0924.
With the store deleted no attempt exists whose approval state a surface could print, so its
Acceptance line in `T2_F273.md` gains that branch, naming this DECISION (§4 item 7). (3) R-0991. The
catalog contract recovers a name passed to a module's own forwarding helper, to a fixed point, and
counts `emit_important_event`; both labels stay, and every newly visible name gets a catalog entry in
the catalog's style. (4) R-0912. `_task_evidence_dir` raises `UnsafeTaskIdError`, a `ValueError`
carrying the id, and `job evidence` catches it and exits 1 naming the id; a CLI test exports a job
whose task carries the minted default. (5) R-0940, R-0954. `docs/agents/self_drive_protocol.md`
gains two worker-step rules: a block copy's line count and sha256 are compared with the given text
before the commit that saves it, and a disposable worktree is named under `.remedy-wt/` and removed
as its step's last action, with the reviewer's `git worktree list` at the verdict. (6) R-0977 is NOT
landed this round. Its FIX as written makes every `do` job block in a repository with no tests,
which DECISION F269 D6 measured; the non-blocking variant a helper prototyped lets the gate's pytest
write `__pycache__` files into the job worktree, which ends a `do` in any repository with a Python
suite `job_handoff_coverage_failed`. That defect is reproducible at `b22fe3bc` under
`--contract cli-tool`, and R-0977's round registers and repairs it first.
ALTERNATIVES: keeping `repair_loop.py` whole and giving the store a writer, rejected because no
surviving word starts a repair and a writer with no word is dead code; dropping the two labels,
rejected because their events are still emitted; landing R-0977 non-blocking now, rejected for (6).
REVERSE: restore the touched files from `b22fe3bc`, and delete this paragraph.
