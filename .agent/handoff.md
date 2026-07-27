# Handoff — F048 Job queue · round 1 (gate + claim + T001 + T002)

## Range
Review of `40c7e4d..HEAD` — 5 commits. Branch point `40c7e4d` = main after the F047 gate merge.

## Commits
### 739947d chore(f048): claim F048 job queue
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f048-r1-{1,2}.md | +15 | authored texts, sha256-verified before use |
| .agent/live_review.md | +14 −38 | full replace with the F048 ledger |
| .agent/plan.md | +40 −23 | rewritten for F048 |
| docs/roadmap/STATUS.md | +1 −1 | F048 `[ ]` → `[~]` |

### bd990c7 feat(f048): file-based job queue entry store (T001)
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/job_queue.py | +500 | new module; at the 500-line ceiling, tests split off |

### acf0728 test(f048): unit tests for the queue entry store (T001)
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_job_queue.py | +400 | 26 tests: ordering, claim lifecycle, transitions, restart, corruption, duplicates |

### 090903f test(f048): two-process claim proof (T002)
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_queue_concurrency.py | +185 | 24 entries, 2 subprocess consumers, 3 repeats |

### handoff commit (self-reference, R-0149 grouped table)
| Path | +/- | Reason |
|---|---|---|
| .agent/{handoff,plan}.md | rewrite | this file; plan ticks T001/T002/canary |

## External actions
- `gh pr merge 153 --merge --delete-branch` → FAILED: `not mergeable: the merge commit cannot be cleanly created` (CONFLICTING/DIRTY) on `.agent/{plan,live_review,handoff}.md` — PR #155 and the F047 closure both rewrote them. Operator ruling 2026-07-27 "take the newest AGENTS.md": resolved to main's side on feature/f047-checkpoint-resume (merge `6c94d23`, pushed `2d0301c..6c94d23`), then the same merge command → exit 0.
- `git checkout main && git pull --ff-only` → `Already up to date`, main `40c7e4d`.
- `git push -u origin feature/f048-job-queue` → new branch. NO PR this round (as ordered).

## Verification
    pytest tests/orchestration/test_job_queue.py -q         → 26 passed, exit 0
    pytest tests/orchestration/test_queue_concurrency.py -q →  6 passed, exit 0
    pytest tests/cli/test_golden_path.py -q                 → 42 passed, exit 0
    ruff check job_queue.py + both test files               → All checks passed
T002 falsified in scratch (not committed): the same scenario with the claim marker's `create_only` disabled → 22 double-claims. Real runs: splits 10/14, 11/13, 10/14, overlapping claim windows, 0 double-claims.

## Authored-text proofs
- f048-r1-1.md sha256 `10e9523…3b65` = BEGIN marker; `sed -n 33p docs/roadmap/STATUS.md | cmp - <file>` → exit 0; old `- [ ] F048 — Job queue` GONE (grep exit 1).
- f048-r1-2.md sha256 `f8e9648…a559c` = BEGIN marker; `cmp .agent/live_review.md .agent/authored/f048-r1-2.md` → exit 0.

## Deviations & assumptions
- Inspection (item 3): the primitive is `packages/common/secure_fs.py:532` `write_file_atomically(..., create_only=True)` — publishes with `os.link`, returns False on `FileExistsError`; used by `packages/orchestration/safe_points.py:372` (F011 stop request). T001 reuses it unchanged for `<entry-id>.claim`.
- Path scheme: `<data_root>/queue/<project_id>/<entry_id>.json` + sibling `<entry_id>.claim`; 0700 dirs / 0600 files opened through identity-verified directory fds (the F011 control-area posture).
- A9: higher priority value first, FIFO by `created_at` within equal priority, `id` as the same-microsecond tie-break; duplicate goal text allowed → two independent entries.
- `queue_root()` kept in job_queue.py (not data_paths.py) and `tests/conftest.py` SUBPROCESS_FILES left unextended for the new subprocess test — both outside the declared change set, so both are T003's call. T001's module commit was trimmed to exactly 500 lines rather than declaring an oversize exception.

## Next
Window 1 reviews `40c7e4d..HEAD`. T003 (CLI, reclaim, executor binding) is the next round.
