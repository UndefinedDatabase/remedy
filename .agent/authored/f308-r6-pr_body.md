**What changed.** When a run splits a task whose context is too large into parts, the job's run
manifest — Remedy's record of what an episode ran — is now written and valid instead of being lost
(finding R-1252, which hit five closures' self-use runs in a row). The run records each split in
the job's own record (`metadata["task_splits"]`: the parent, the parts, the episode and the reason);
the F7 check accepts a task list equal to the definition's with this episode's recorded splits
applied and still refuses every other change; the manifest carries the episode's splits as
`task_splits`, written only when there are any, so every older manifest keeps its exact bytes; the
strict decoder, the validators and the check across a job's episodes accept the split, and a split
parent is `skipped` with the status `split`.

**Why.** A split is Remedy's own change to the task list, not an edit from outside, so refusing
it lost the record of every episode that split a task.

**Key decisions.** DECISION F308 D1: three structural steps first, into the new module
`packages/orchestration/run_task_list.py`, because every function the repair touches is on the
structure ledger and may not grow. DECISION F308 D2: the record's shape and where each reader
applies it. Two defects the round 2 gate found (R-1314, a part split again in the same episode;
R-1315, the refusal's wording) were repaired in round 3.

**How to review.** `docs/roadmap/features/T2_F308.md` (Built State),
`docs/roadmap/features/T0_F012.md` (section "A task the run splits"), then
`packages/orchestration/run_task_list.py` and the `Gate: F308 R1` to `R5` entries in
`.agent/live_review.md`. The branch merged nothing in; its fork point is `1622c16d7`.

**Verdict.** Rounds 1 to 5 PASS, booked in the ledger; round 6's verdict is the reviewer's and is
booked in the next feature's first commit. Live review PASS: every finding F308 owned is resolved.

**Open findings.** 39, all owned by the rolling paydown F307 (R-1246 and R-1276 to R-1313).

**Local evidence (amend1011-manual-hosted-ci).** Interpreter: Python 3.10.12, `/usr/bin/python3`.
- The one full suite, `python3 -m pytest -n auto -q`, on the tree of `0b87b714b` (the tree that
  ships but for records and docs): `23032 passed, 22 skipped, 1 warning in 344.69s`, exit 0
  (`.agent/authored/f308-closure-suite.txt`).
- The evidence job `f308r5e1001`, `python3 .agent/authored/f308-r5-create_f308_evidence.py`, on the
  accepted head `63ca6c280075c146bf6bbd102f1e99fd04e1625b`: 8028 passed, 9 skipped, exit 0.
- Review package `remedy-review-20261014-142527-READY_FOR_REVIEW.zip`, SHA-256
  `b00824ae07ec3d974e55bc50ab4a16a4724b25f469099ca60ec0f63462eeeb25`, in
  `/home/decodeux/Repos/remedy-history/zips`.

**Runtime actuals.** 6 delegated rounds in one session; wall clock and model tokens not measured
for the rounds themselves; the closure's self-use run used four provider calls and 10823 tokens.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
