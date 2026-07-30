# Handback — R0154 R2 (verdict + merge) & F050 R1 (T001+T002) — DONE

## Range
`c0e2bd1..HEAD` · feature/f050-dag-scheduling · 3 commits + 1 round-end.
Preceded by `1717fc8` on feature/r0154-closure-ordering (verdict), merged as
PR #162. F050 PR **#163** open, NOT merged.

## Commits
### 1717fc8 chore(r0154): persist the R1 PASS verdict — on feature/r0154-closure-ordering
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +14/-6 | authored r0154-r2-1 applied by copy — the R1 PASS verdict |
| .agent/last_block.md | rewrite | R2/R1 block guard + authored texts |
| .agent/authored/r0154-r2-1.md | +new | authored source, sha256-verified |

### 983709f chore(f050): claim F050 — state reset
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/STATUS.md | +1/-1 | `- [ ] F050` → `- [~] F050`, one line, nothing else |
| .agent/live_review.md · plan.md | +66/-32 | authored f050-r1-1 / f050-r1-2 applied by copy |
| .agent/authored/f050-r1-{1,2}.md | +new | authored sources, sha256-verified |

### 34aec75 feat(f050): dag_schedule pure module + table tests (T001)
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/dag_schedule.py | +185 | pure `ready_set` / `blocked_downstream` / `build_graph`; no I/O, clock, randomness or threading |
| tests/orchestration/test_dag_schedule.py | +300 | 34 table tests: diamond, chain, islands, legacy-linear, mixed, single-task, transitivity, determinism |

485 lines — under the 500 cap.

### cc79dcb feat(f050): DAG ready-set executor integration + diamond fixture (T002)
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/long_run_executor.py | +118/-… | DAG `ready_tasks(…, blocked_ids=)`, `skipped_blocked_tasks`, in-run `blocked_ids`, recompute after every task end, `CycleRecord.skipped_blocked_task_ids`, checkpoint intent skips blocked tasks |
| packages/orchestration/task_runner.py | +26/-… | additive `task_id=None` on `run_next_task` / `_find_next_pending` — DEVIATION, see below |
| tests/orchestration/test_long_run_executor.py | +283/-… | diamond fixture + 13 F050 tests + linear-regression class; one pre-F050 helper assertion updated |

402 lines — under the cap.

## External actions
`gh pr merge 162 --merge --delete-branch` (exit 0); 4 pushes; `gh pr create` →
**PR #163**. NOT merged. No worktree.

## Verification — raw
- Open PR Gate: `gh pr list …` → exactly one, `{"baseRefName":"main","headRefName":"feature/r0154-closure-ordering","isDraft":false,"number":162}`.
  Merged exit 0; `git checkout main && git pull --ff-only` → "Already up to date."
- `python3 -m pytest tests/docs/ -q` → exit **0**, `292 passed in 0.19s`.
- `python3 -m pytest tests/cli/test_golden_path.py -q` → exit **0**, `42 passed in 14.98s` (Slice 1) and `42 passed in 14.88s` (Slice 3).
- `python3 -m pytest tests/orchestration/test_dag_schedule.py -q` → exit **0**, `34 passed in 0.12s`.
- Slice-3 gate, `python3 -m pytest tests/orchestration/test_dag_schedule.py tests/orchestration/test_long_run_executor.py tests/orchestration/test_queue_executor_binding.py tests/orchestration/test_overnight_executor.py -q`
  → exit **0**, `144 passed in 0.54s`.
- Blast-radius runs for the two files outside the declared list:
  `python3 -m pytest tests/orchestration/ -q` → exit **0**, `8672 passed, 7 skipped in 598.74s`.
  `python3 -m pytest tests/test_task_runner.py tests/orchestration/test_resume_kill.py tests/orchestration/test_checkpoints.py tests/orchestration/test_resume_cli.py tests/orchestration/test_memory_execution.py tests/test_verifier.py -q`
  → exit **0**, `161 passed in 1.35s`.
- No threading: `git diff | grep -E '^\+.*(threading|Thread|concurrent\.futures|multiprocessing|asyncio)'` → no match.

## Authored-text proofs
On-disk `sha256sum` matched each BEGIN marker BEFORE any apply; applied by
copy; `cmp` authored vs target exit **0** for all three.

    800c9f15bf69fd222cfc6e13b1b51423580e000dcabf15e5516862104f7ebffb  .agent/authored/r0154-r2-1.md
    373c67edd96338b630eaedc7ab3c60a573712e9b24facc8c2809a20a4c5d1569  .agent/authored/f050-r1-1.md
    d019d7b347cb92468562c12acb5342cc585d627293aa8d1f5addd741bef744c7  .agent/authored/f050-r1-2.md

No `## Verdicts` written for F050 — `.agent/live_review.md` still reads
`(pending R1)`.

## STATUS grep proofs
`grep -cF -- '- [~] F050 — DAG scheduling'` = **1**;
`grep -cF -- '- [ ] F050 — DAG scheduling'` = **0**. One-line diff confirmed.

## Deviations & assumptions
- **`task_runner.py` touched (outside the declared Change list).** The feature
  is unreachable without it: `run_next_task` selected `_find_next_pending(job)`
  — the first PENDING task in plan order — so the ready set could only change
  HOW MANY tasks ran, never WHICH. In the diamond the blocked branch's task
  sorts before the healthy branch's, so the acceptance criterion was
  unsatisfiable. Fix: additive keyword `task_id=None` on `run_next_task` and
  `_find_next_pending` (6 lines of logic); default reproduces byte-identical
  behavior. Rejected alternative: duplicating `run_next_task`'s rollback
  semantics inside the executor. Blast radius covered by the two extra runs
  above.
- **One pre-F050 assertion updated**, `TestReadyBatch::test_linear_order_capped_at_batch_size`
  → `test_legacy_plan_releases_one_task_at_a_time` (+ a new
  `test_independent_tasks_fill_the_batch_up_to_its_cap`). It asserted the old
  helper contract (`ready_tasks` returns the first `batch_size` PENDING tasks),
  which is exactly what F050 replaces: under the legacy predecessor rule the
  ready set is one deep. Loop-level behavior for linear plans is unchanged —
  proved by `TestLinearPlansAreUnchanged` and by
  `test_batch_larger_than_remaining_tasks_is_fine` passing untouched.
- **Per-cycle iteration cap is `limits.batch_size`, not `len(batch)`.** First
  attempt used `len(batch)` and regressed legacy plans to one task per cycle
  (caught by the existing suite, fixed before commit). The batch is a cap; the
  ready set is recomputed after each task end.
- **Step seam kept 2-arg-compatible.** The target is passed only to callables
  declaring `task_id` (`_step_target_argument` via `inspect.signature`), so all
  30 existing `task_step=` injections run unchanged.
- **Round-end state in a second mechanical commit** (handoff + OUTCOME flip),
  as accepted in R0154 R1 — it can only be written after the PR exists.
- `.agent/plan.md` left byte-verbatim as authored: it describes this round
  (T001+T002), so it is not stale. Actual progress is reported here.

## Item status
| Item | Status | Reason |
|---|---|---|
| 1 last_block guard | done | flip to `executed` in the round-end commit |
| 2 verdict text + commit | done | sha256 + cmp 0 |
| 3 Open PR Gate (#162) | done | merged, main fast-forwarded |
| 4 branch feature/f050-dag-scheduling | done | |
| 5 f050 authored texts + apply | done | 2 × sha256 match, 2 × cmp 0 |
| 6 STATUS.md one-line claim | done | grep 1 / 0 |
| 7 Slice 1 gate + commit | done | 292 / 42, both exit 0 |
| 8 dag_schedule.py (T001) | done | pure; 185 lines |
| 9 test_dag_schedule.py | done | 34 tests, all 8 named shapes covered |
| 10 Slice 2 gate + commit | done | exit 0 |
| 11 executor integration | deviated | needed `task_runner.py` too — see Deviations |
| 12 T002 tests | done | diamond, recomputation (behavioral + counting stub), determinism, linear regression |
| 13 Slice 3 gate + canary | done | 144 / 42, both exit 0 |
| 14 PR, not merged | done | #163 |
| 15 handback | done | this file |

## Next
Reviewer R1 review of PR #163 → writes `## Verdicts` in `.agent/live_review.md`.
Open questions for the reviewer: (a) accept the `task_runner.py` deviation;
(b) accept the updated pre-F050 helper assertion. Then per the plan: the
integration-gate round, then closure per STATUS_closure_protocol.md v4 — own
rounds, never bundled.
