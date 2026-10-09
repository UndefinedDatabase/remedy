## What and why

F300 gives Remedy's structure a measure, a ledger and a ratchet. Measured at the claim on
`b25d87a24` (`.agent/f300_inventory.md`): 162 functions in `packages/`, `apps/` and `scripts/` were
longer than 100 lines and 40 files longer than 1,000, and `run_job` had grown from the 1,522 lines
registered two days earlier to 1,665. Nothing stopped that growth, and one of its costs was already
an open finding: `run_job` wrote its stop check out at four safe points, and one of them forgot the
pause (R-1160).

Now:
- **T001, the measure (DECISION F300 D1).** `remedy integrity structure` and
  `packages/orchestration/structure_measure.py` measure the files git tracks under a folder of any
  repository: every Python function from its `def` line to its last line by Python's syntax tree,
  every text file by its lines. Functions above 100 lines and files above 1,000 are named, largest
  first, in text or `--json`; the limits are options; it reads only and exits 0 whatever it lists.
  F301 will use it on every project Remedy builds.
- **T002, the ledger and the ratchet (DECISION F300 D2).** `docs/system/structure-ledger-v1.md`
  lists Remedy's 162 large functions and 39 large files (npm's lockfile aside) with their sizes,
  and the boundary and steps of the 29 largest. `tests/test_structure_ratchet.py` holds every row
  to its measure and pins each table's row count and sum of lines: a size may fall, and the commit
  that lowers it lowers its row; a size that rises, and a new function or file above the limit,
  fail.
- **T003, the rule.** The section "The structure rule" of `docs/agents/self_drive_protocol.md`:
  the rolling findings paydown after every fifth accepted feature measures and takes one
  structural step; a feature that touches a listed function draws its boundary first; a replaced
  structure is deleted; a structural step changes no behaviour.
- **T004, the first step.** R-1160 repaired first, in its own commit with its red-proof: a pause
  read after a task is applied now parks the job instead of blocking it as a budget stop. Then
  every safe point of `run_job` settles its signal through one nested function,
  `_settle_safe_point`; `run_job` fell to 1,652 lines and no test changed its expectation.

## Key decisions
- DECISION F300 D1: the measure is a third read-only command of `integrity`, limits 100 and 1,000
  as options, tracked files only, a measure and not a gate; R-1160 moved to F300.
- DECISION F300 D2: the page is the record, held row for row with pins on each table's count and
  sum; the scope is `packages/`, `apps/` and `scripts/`; the rule lives in one protocol section.

## How to review
Read `packages/orchestration/structure_measure.py` and `_cmd_integrity_structure`, then
`tests/test_structure_ratchet.py` against the page's two tables, then the after-task safe point
and `_settle_safe_point` in `run_job` (`packages/orchestration/pingpong_job.py`) with
`TestR1160APauseWhileATaskIsApplied` in `tests/orchestration/test_pause_resume.py`.

## Changed files (at the accepted head `c5ebe4d34`, against the fork point `b25d87a24`)

| Path | Lines |
|---|---|
| `apps/cli/command_catalog.py` | +20 / -0 |
| `apps/cli/commands/integrity_cmd.py` | +41 / -0 |
| `docs/README.md` | +2 / -0 |
| `docs/agents/planner_reviewer_prompt.md` | +9 / -0 |
| `docs/agents/self_drive_protocol.md` | +21 / -0 |
| `docs/guides/exit-codes.md` | +1 / -0 |
| `docs/roadmap/STATUS.md` | +1 / -1 |
| `docs/roadmap/features/T2_F300.md` | +52 / -0 |
| `docs/system/structure-ledger-v1.md` | +353 / -0 |
| `packages/orchestration/pingpong_job.py` | +36 / -49 |
| `packages/orchestration/structure_measure.py` | +220 / -0 |
| `scripts/self_use_queue.json` | +8 / -0 |
| `tests/orchestration/import_reachability_allowlist.txt` | +1 / -0 |
| `tests/orchestration/test_job_stop_integration.py` | +22 / -0 |
| `tests/orchestration/test_pause_resume.py` | +44 / -0 |
| `tests/orchestration/test_structure_measure.py` | +334 / -0 |
| `tests/test_structure_ratchet.py` | +181 / -0 |
| `.agent/` (25 files: blocks, ledger, decisions, plan, inventory, self-use record, closure suite) | +1886 / -204 |

The closing round adds the ledger's rotation, the STATUS line, the README sync, SU-052's
`consumed_by` and the handoff.

## Verification
- The closure's one full suite on the tree that ships: `22289 passed, 22 skipped`, exit 0
  (`.agent/authored/f300-closure-suite.txt`), 1264.11 CPU seconds, 8.4 percent above F299's.
- Evidence job `f300r5e1001` on `c5ebe4d34`: 2287 node ids, 2283 passed, 4 skipped,
  `is_valid_current_run True`.
- Package `remedy-review-20261009-234617-READY_FOR_REVIEW.zip`, SHA-256
  `9fa8f77003f4fb19f4793907ec4cacedc0f8fe7fce93d96a005f21877f6dff5a`, `READY_FOR_REVIEW`, review
  subject `b25d87a24`..`c5ebe4d34`, in `/home/decodeux/Repos/remedy-history/zips`.
- Every production change was mutation-proved by the reviewer in a disposable worktree; the
  ratchet's acceptance mutations — a listed function one line longer, a new 101-line function —
  each turn it red.

## Latest verdict and findings
Rounds 1 to 5 reviewed; round 6, the closing round, is reviewed on this pull request. F300 is
accepted PASS_WITH_RISKS: its own findings R-1160 and R-1232 are resolved, and 15 findings stay
open, all owned by the findings paydown F297.

## Runtime actuals
Six delegated rounds in one session on 2026-10-09; the self-use job measured 2 provider calls and
11510 tokens on `claude-cli` with `claude-sonnet-4-6`; the session's own model calls are not
measured by Remedy's ledger.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
