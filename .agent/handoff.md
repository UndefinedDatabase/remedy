# Handback — F307 round 8: book round 7, R-1311 landed in part and R-1413; T011, the mission reconcile (R-1295, R-1284, R-1283, R-1296)

## Session

SESSION 2 of feature F307 · round 8 · rounds so far 8

Context self-assessment: this worker verified every prepared digest before use, byte-copied the prepared files through one script, self-reviewed each staged diff before committing, ran each gate once and wrote this handback from what it read; context is ample and nothing was lost.

Fortschritt: ~45 % (T001 to T004, T010, T011, T014, R-1280, R-1290 and R-1292 landed · the rest open) — Schätzung

## Range

Review of `bec6c4cb5`..`HEAD` on `feature/f307-findings-paydown-v9`.

## Commits

### d23e827f6 F307 R8 C1: book round 7, R-1311 landed in part and R-1413, DECISION F307 D9, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f307-r8.md` | 108/0 | NEW FILE, this round's block, byte copy (108 lines, sha256 `a9f2859f50e3ec389d141968f610db8d262e0d15ae3bf30ff4807ab102a9fcbe`, equal to `block.md`) |
| `.agent/decisions.md` | 12/0 | prepared file, byte copy (DECISION F307 D9) |
| `.agent/live_review.md` | 6/0 | prepared file, byte copy (round 7's verdict, R-1311 landed in part, R-1413 resolved) |
| `.agent/plan.md` | 5/7 | prepared file, byte copy |

### 897756a53 F307 R8 C2: the reconcile folds each repository's duplicates and keeps a duplicate's current order (R-1295, R-1284)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/repo_mission.py` | 2/2 | prepared file, byte copy (`_seal` renamed `seal_current_order_batch`) |
| `packages/orchestration/repo_mission_reconcile.py` | 19/12 | prepared file, byte copy (groups per repository key; a duplicate's current order sealed before its batches merge) |
| `tests/orchestration/test_repo_mission_reconcile.py` | 71/0 | prepared file, byte copy (three new tests) |

### 9a20efea4 F307 R8 C3: reconcile backs up only the projects it writes, in a class it prunes, and hands a job over under the target project's lock (R-1283, R-1296)
| Path | +/- | Reason |
|---|---|---|
| `docs/system/mission-upkeep-v1.md` | 8/4 | prepared file, byte copy |
| `packages/orchestration/data_paths.py` | 9/0 | prepared file, byte copy (`reconcile-backups` class, `reconcile_backups_dir`) |
| `packages/orchestration/mission_state.py` | 2/2 | prepared file, byte copy (docstring) |
| `packages/orchestration/repo_mission_reconcile.py` | 92/43 | prepared file, byte copy (per-project backup with pruning, restore of exactly those directories, hand-over under the target's lock via `ensure_project_mission`) |
| `tests/orchestration/test_repo_mission.py` | 0/1 | prepared file, byte copy (the reconcile leaves the allowed list of mission creators) |
| `tests/orchestration/test_repo_mission_reconcile.py` | 123/0 | prepared file, byte copy (new tests) |

### (this commit) F307 R8 C4: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | base confirmed: HEAD and `origin/feature/f307-findings-paydown-v9` both `bec6c4cb5`, tree clean, no pull run |
| C1 | done | records commit `d23e827f6` |
| C2 | done | commit `897756a53` |
| C3 | done | commit `9a20efea4` |
| C4 | done | this handback commit |
| Gate 1 | done | `git status --porcelain` empty; `verify.py` every line `True`, `absent C4`, last line `ALL True` |
| Gate 2 | done | `ruff over 6 files: exit 0`, `All checks passed!` |
| Gate 3 | done | `paths 88`, `exit 0`, `4313 passed, 2 skipped in 47.29s`, no FAILED, ERROR or `process(es) behind` line |
| Gate 4 | done | `fail_count` 0, all six checks pass |
| Gate 5 | done | open findings count printed `37` |
| Push | pending | runs after this commit; reported in the session reply |

## External actions

No push, PR or `gh` command before this commit; the push follows it and is reported in the session reply. No worktree of my own, no provider call.

## Verification

1. `block.md` and `digests.txt` hashed first: `a9f2859f...ab102a9fcbe` and `75435058...fdf59df2e`, both equal to the delivering prompt. `apply.py` re-checked every prepared file's sha256 against `digests.txt` before copying and the copy's sha256 after.
2. C0: branch `feature/f307-findings-paydown-v9`; `git rev-parse HEAD` and `origin/feature/f307-findings-paydown-v9` both `bec6c4cb5d6fe16e5fe7d8442be87b3752059da8`; tree clean; `.agent/STOP` absent.
3. Gate 1: `git -C <root> status --porcelain` — empty. `python3 .remedy-wt/f307-r8/prep/verify.py <root>` — all lines `True` (three single-parent checks, `3 of 3` subjects, branch, every path-set and byte-equality line of C1 to C3, saved block equals `block.md`), `absent	C4`, `ALL True`.
4. Gate 2: `python3 .remedy-wt/f307-r8/prep/ruff_touched.py <root>` — `ruff over 6 files: exit 0`, `All checks passed!`.
5. Gate 3: `python3 .remedy-wt/f307-r8/prep/run_selection.py <root> .remedy-wt/f307-r8-worker/selection-output.txt` — `paths 88`, `exit 0`, `4313 passed, 2 skipped in 47.29s`. SKIPPED: `tests/test_agent_tooling.py:43` (D12 quarantine, F252) and `tests/test_install_smoke.py:175` (opt-in install smoke). A grep of the output for `FAILED|ERROR|process(es) behind` counted 0.
6. Gate 4: `python3 -m apps.cli.main integrity check --json` — `fail_count` 0; `handler_import` pass (handlers=194), `live_review_verdict` pass (last Gate verdict PASS), `plan_consistency` pass, `relevant_untracked` pass, `repo_root_hygiene` pass, `high_blockers_open` pass.
7. Gate 5: `rotate_live_review.open_finding_ids` count — `37`.

## Authored-text proofs

C1's four, C2's three and C3's six prepared files are byte copies, each proved equal by sha256 right after the copy and again by `verify.py`. `.agent/authored/f307-r8.md` equals `block.md`: 108 lines, sha256 `a9f2859f50e3ec389d141968f610db8d262e0d15ae3bf30ff4807ab102a9fcbe` on both sides.

## Deviations & assumptions

None in the commit sequence, paths or gate order. Minor: the gate scripts were called with the absolute repository root instead of `.` because the shell cwd is fixed there and `cd` is not allowed; no mutation or full-suite run, `REMEDY_TEST_MAX_WORKERS` not set, `.data` not read, no amend, rebase or force.

## For the operator, in plain sentences

This round changed how the clean-up of duplicate missions behaves. Duplicates of a second repository of the same project are now folded too, each into its own repository's mission, where before they were skipped or refused. A folded duplicate keeps its latest plan and contract instead of losing them. Its safety copies now hold only the projects the clean-up changes, live in a folder of their own that the data-usage report recognises, and are removed after 30 days. A mission it creates for another project is named after that project, and the job is handed over while holding that project's lock. The round also booked the previous round's verdict. All five required checks ran once each and came back as expected. No question waits for the operator.

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Rule 2: the Open PR Gate.
3. Review round 8's handback and book its verdict, with the resolutions of R-1283, R-1284, R-1295 and R-1296, in the next round's first commit.
4. T012, the mission's repositories and readers: R-1281, R-1297, R-1298 and R-1301.

Operator questions open: 0. Open findings count gate 5 printed: 37.
