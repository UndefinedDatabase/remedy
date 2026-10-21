# Handback — F307 round 6: book round 5, R-1290, R-1292; the mission lock moves to mission_state.py and every writer holds it (R-1300); a changed batch is sealed again and legacy jobs take their batch (R-1285, R-1299)

## Session

SESSION 1 of feature F307 · round 6 · rounds so far 6

Context self-assessment: this worker verified every prepared digest, byte-copied the prepared files, self-reviewed each diff before committing, ran each gate once and wrote this handback from what it read; context is ample and nothing was lost.

Fortschritt: ~36 % (T001 to T004, T014, R-1280, R-1290, R-1292 and T010 but R-1311 landed · the rest open) — Schätzung

## Range

Review of `a1098e2e4`..`HEAD` on `feature/f307-findings-paydown-v9`.

## Commits

### c7218b8be F307 R6 C1: book round 5, R-1290 and R-1292, DECISION F307 D7, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f307-r6.md` | 104/0 | NEW FILE, this round's block, byte copy (104 lines, sha256 `46e917716f39e36a03ed0c61265e3aace6f9700a821c5de54ca2f7fa87cf9949`, equal to `block.md`) |
| `.agent/decisions.md` | 12/0 | prepared file, byte copy (DECISION F307 D7) |
| `.agent/live_review.md` | 6/0 | prepared file, byte copy (round 5's verdict and its two resolutions booked: R-1290, R-1292) |
| `.agent/plan.md` | 5/5 | prepared file, byte copy |

### 09e4f50cb F307 R6 C2: the per-project mission lock moves to mission_state.py, unchanged (R-1300)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/mission_state.py` | 24/0 | prepared file, byte copy (`repo_mission_lock` and `LOCK_FILENAME` moved in, unchanged) |
| `packages/orchestration/repo_mission.py` | 1/19 | prepared file, byte copy (`repo_mission_lock` and `LOCK_FILENAME` moved out; import added) |
| `packages/orchestration/repo_mission_reconcile.py` | 2/1 | prepared file, byte copy (`repo_mission_lock` import switched to `mission_state`) |

### a46caceac F307 R6 C3: every writer of a mission record holds the project's lock, which its holder may take again (R-1300)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/contract_templates.py` | 12/11 | prepared file, byte copy (`write_template_contract` holds the lock around its check and its write) |
| `packages/orchestration/mission_compiler.py` | 18/16 | prepared file, byte copy (`plan_mission` re-reads the version chain under the lock after the provider call) |
| `packages/orchestration/mission_state.py` | 80/53 | prepared file, byte copy (the lock remembers the holding thread's lock files and does not wait for itself; `_update_mission` added; `set_mission_status`, `set_mission_plan`, `set_mission_order`, `set_mission_contract` and `link_job_to_mission` now read-change-save under the lock) |
| `tests/orchestration/test_mission_compiler.py` | 18/0 | prepared file, byte copy (one new test: a plan saved during the provider call is kept as a version) |
| `tests/orchestration/test_mission_state.py` | 64/0 | prepared file, byte copy (new tests: a writer waits for the lock, the holding thread does not wait for itself, a writer of a missing mission makes no lock file) |

### 40dd644eb F307 R6 C4: a changed batch is sealed again and legacy jobs take their batch (R-1285, R-1299)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/repo_mission.py` | 20/8 | prepared file, byte copy (`_seal` also returns the job links; a legacy order's links take that batch's id; a sealed last batch is sealed again when its plan or contract changed) |
| `tests/orchestration/test_repo_mission.py` | 51/0 | prepared file, byte copy (three new tests: a contract written after a fold reseals, a sealed batch whose slots did not change stays as sealed, a legacy mission's jobs take the legacy batch id) |

### (this commit) F307 R6 C5: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | base confirmed: HEAD `a1098e2e4` equal to `origin/feature/f307-findings-paydown-v9`, tree clean, no pull run |
| C1 | done | records commit `c7218b8be` |
| C2 | done | lock-move refactor commit `09e4f50cb` |
| C3 | done | R-1300 behaviour commit `a46caceac` |
| C4 | done | R-1285/R-1299 behaviour commit `40dd644eb` |
| C5 | done | this handback commit |
| Gate 1 | done | `git status --porcelain` empty; `verify.py` printed `True` on every counted line, `absent C5` (not yet counted), last line `ALL True` |
| Gate 2 | done | `ruff check` over 8 files printed `All checks passed!`, exit 0 |
| Gate 3 | done | 108 paths, exit 0, `4991 passed, 2 skipped in 63.55s`, two SKIPPED lines, no FAILED, ERROR or `process(es) behind` line |
| Gate 4 | done | `fail_count` 0, all six checks pass |
| Gate 5 | done | open findings count printed `40` |
| Push | pending | runs after this commit; reported in the session reply |

## External actions

No push, PR or `gh` command before this commit; the push follows it and is reported in the session reply. No worktree of my own, no provider call, no rotation.

## Verification

1. Digests: a python check over the 19 lines of `digests.txt` — every prepared file's sha256 read `OK` against the listed digest, last line `ALL_OK`; `block.md` and `digests.txt` themselves were also hashed first and matched the values given in the delivering prompt.
2. C0: `git branch --show-current` read `feature/f307-findings-paydown-v9`; `git rev-parse HEAD` and `git rev-parse origin/feature/f307-findings-paydown-v9` both read `a1098e2e46cde899dc1e5c65e3a21fd5b07bf25a`; `git status --porcelain` was empty before any write.
3. Gate 1: `git status --porcelain` (through `git -C`) — empty. `python3 .remedy-wt/f307-r6/prep/verify.py .` — every counted line `True` (single-parent checks on all four commits, the Cn-subject count 4 of 4, the branch check, every C1 through C4 path-set and per-path equality check, and "the saved block equals block.md"); one line `absent C5` (not yet counted, C5 did not exist when the gate ran); last line `ALL True`.
4. Gate 2: `python3 .remedy-wt/f307-r6/prep/ruff_touched.py .`, run from the primary checkout — `ruff over 8 files: exit 0`, `All checks passed!`.
5. Gate 3: `python3 .remedy-wt/f307-r6/prep/run_selection.py . .remedy-wt/f307-r6-worker/selection-output.txt` — `paths 108`, `exit 0`, `4991 passed, 2 skipped in 63.55s (0:01:03)`. SKIPPED lines: `tests/test_install_smoke.py:175` (install smoke is opt-in: set `REMEDY_INSTALL_SMOKE=1` on a host with network access) and `tests/test_agent_tooling.py:43` (D12 quarantine, F252 — the read-only reviewer contract now lives on the split-workflow docs). No FAILED, no ERROR, no `process(es) behind` line.
6. Gate 4: `python3 -m apps.cli.main integrity check --json` exit 0 — `fail_count` 0; all six checks pass: `handler_import` ("handlers=194"), `live_review_verdict` ("last Gate verdict PASS"), `plan_consistency` ("unchecked=0, context_complete=False"), `relevant_untracked` ("untracked=0, relevant=0"), `repo_root_hygiene` ("no reviewer scratch, evidence dir or archive at the root"), `high_blockers_open` ("no open blocker/high findings").
7. Gate 5: `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"` — `40`.

## Authored-text proofs

C1's four prepared files, C2's three prepared files, C3's five prepared files and C4's two prepared files are byte copies of the prepared files; each was proved equal by a `sha256` comparison right after the copy, before staging, and `verify.py` re-proved every one of them (`True`). `.agent/authored/f307-r6.md` equals `block.md`: 104 lines, sha256 `46e917716f39e36a03ed0c61265e3aace6f9700a821c5de54ca2f7fa87cf9949` on both sides.

## Deviations & assumptions

None. The commit sequence, paths and gate commands followed the block exactly; no file outside the named paths per commit was touched; each gate ran exactly once, in order; no mutation or full-suite run was attempted; `REMEDY_TEST_MAX_WORKERS` was not set; `.data` was not read; every commit used `git -C <repo> commit -F <message file>`, never `cd` joined to another command; no amend, rebase or force was used.

## For the operator, in plain sentences

This round booked the previous round's closing verdict and its two resolutions into the running record, and recorded a decision covering three further repairs to the same shared mission record. First, a small piece of locking logic moved out of the module it used to share with another part of the program and into the module that actually owns the record it protects, with no change in what it does. Second, every part of the program that reads, changes and saves that shared record now holds the same lock while it does so, so two writers acting at once can no longer silently lose one of their changes, and a part of the program already holding the lock can safely ask for it again without waiting on itself. Third, a batch of work whose plan or reviewer criteria changed after it was already marked finished is now marked finished again to pick up that change, and the older work a repository already had before its first tracked request now stays correctly grouped under that first request instead of appearing to have no work at all. All five required checks ran once each and came back exactly as expected. No question waits for the operator.

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Rule 2: the Open PR Gate.
3. Book round 6's verdict in the next round's first commit.
4. R-1311, the mission leftovers.

Operator questions open: 0. Open findings count gate 5 printed: 40.
