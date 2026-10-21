# Plan — F141 Permission matrix per autonomy level

## Goal
What running work may DO becomes one enforced table: eight actions by F078's levels `L2` to `L5`,
answered by one check in `packages/orchestration/permission_matrix.py` that every seam calls, with
a test per cell, answers that cite their cell, audited approvals of an instance, a table rendered
from the constant, and no bypass parameter (docs/roadmap/features/T7_F141.md; DECISIONs F141 D1
to D5).

## Current Step
Round 5 (session 1) BLOCKED after C4. C1-C4 are committed: the records, the `expensive` seam at
the cost prompt (`confirm_cost_preview`, `job.py`, `job_rerun_cmd.py`), the `external_call` seam at
`plan_child_spawn`, the prompt's own approval kind, and the tests, R-1399's included. Gates 1, 2, 4,
5 and 6 are green; gate 3 (the selection run) reds one test OUTSIDE this round's named paths:
`tests/orchestration/test_long_run_executor.py::TestJobRunCommand::
test_the_gate_sees_an_unavailable_estimate_and_yes_or_unattended` — its own `fake_confirm` stand-in
for `confirm_cost_preview` does not accept the `yes_flag` keyword C2 added to the real call in
`job.py`. The block names no repair commit for this file, so per its own rule ("repair it in a NEW
commit only if the block names one; otherwise stop and report") this round stops here.

## Next Steps
1. A repair, authorized by the next round's first commit: give `fake_confirm` in
   `test_long_run_executor.py` the same `job_id=None, yes_flag="--yes"` keywords (or `**_kw`), then
   re-run gate 3 and, once green, C5 and the push this round could not reach.
2. Round 6 (T003): the table rendered in the docs from the constant, the guard against bypass
   parameters, the import guard over the seams, the fate of `permissions.py` and of the builder
   bridge's integer level, and a fixture per level.
3. Round 7 (T003): the matrix in the UI, rendered from the constant.
4. The closure sequence.

## Risks
- `job_apply.py`, `job.py` and `exec_guard.py` are at or above the structure ledger's limits; every
  edit there stays line-neutral.
- The integrity check fails on High findings F141 does not own (DECISION F310 D7, Q20).
- A seam's call-site signature change can silently break a caller's own test double elsewhere in
  the suite; a round changing a shared helper's signature should grep every caller's test file
  before committing, not only the files a prepared block names.
