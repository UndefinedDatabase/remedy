# Handoff — F276 Data-root hygiene & disk budget · Round 4

## Session

SESSION 1 of feature F276 · round 4 · rounds so far 4

Context self-assessment: the worker read the step block and verified its sha256 before anything else, then AGENTS.md in full, `docs/agents/handback_template.md`, `docs/roadmap/features/T2_F276.md`, the `decisions.md` payload (DECISION F276 D5, which rules where the block is terser), the `ledger.md` payload carrying round 3's verdict and the reviewer's `Done: R-1002`, and the whole 1082-line code diff before applying a single slice of it, and held all of it without loss; every numeral below is the output of a command run in this round, not a recollection.

## Range

Review of 543863a0..HEAD — branch `feature/f276-data-root-hygiene`.

## Summary

Round 4 books round 3's verdict, resolves R-1002 with the reviewer's own text, and builds T003.
- C1 books round 3's PASS over the five commits of `94441e34`..`543863a0`, applies the reviewer's `Done: R-1002` paragraph, appends DECISION F276 D5 and rewrites the plan to this round; the four reviewer payloads are saved byte-exact under `.agent/authored/`.
- C2 lands `release_staging_workspace` plus the copy's two new filters — one `git check-ignore --stdin -z` pass guarded by the target's own `.git`, and the 16 MiB per-file backstop — and exports `child_deletion_refusal` and `job_state_refusal` so the release reuses the reclaim command's rules instead of respelling them.
- C3 wires the hook: `_finalize_job_workspace`'s no-handle branch, which IS the copy case, releases only under the very condition it already applies to a worktree; the tests pin both layers.
- C4 adds the architecture section and the feature-file amendment. C5 is this handoff. No pull request was opened.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | |
| C2 the release and the copy filters | done | |
| C3 the hook and its two layers | done | |
| C4 the docs | done | |
| C5 handoff | done | |
| G1 transport + state | done | 12 readings, every one True |
| G2 code transport | done | four object ids as ordered; six paths and no other |
| G3 targeted suite | done | `583 passed in 176.72s`, exit 0, 0 failed |
| G4 ruff | done | `All checks passed!`, exit 0 |
| G5 mutation red-proofs | done | control green; all three mutations red; none stayed green |
| G6 push + clean tree | done | reported in the round report; it follows this commit |
| R-1002 | done | resolved by the reviewer's own `Done:` paragraph, applied byte-exact at C1 |

## Commits

### bc8b15b2 F276 R4 C1: the round 4 bookkeeping

| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f276-r4-block.md | 104/0 | byte copy of the step block |
| .agent/authored/f276-r4-decisions.md | 60/0 | byte copy of the D5 payload |
| .agent/authored/f276-r4-ledger.md | 4/0 | byte copy of the ledger payload |
| .agent/authored/f276-r4-plan.md | 32/0 | byte copy of the plan payload |
| .agent/decisions.md | 60/0 | `543863a0` bytes + the D5 payload |
| .agent/live_review.md | 4/0 | `543863a0` bytes + the ledger payload: round 3's PASS and `Done: R-1002` |
| .agent/plan.md | 15/14 | rewritten to the plan payload |

Insertions 279.

### 92d4c38b F276 R4 C2: the release and the copy's two new filters

| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/data_reclaim.py | 32/6 | `_deletion_refusal`/`_job_state` exported, `STAGING_DIR_PREFIX` imported |
| packages/orchestration/staging_workspace.py | 300/34 | the release, the enumerate-then-filter copy, the ignore pass, the ceiling |

Insertions 332.

### f7d668d9 F276 R4 C3: the hook and its two layers

| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/pingpong_job.py | 75/0 | `_release_job_workspace_copy`, the hook's copy branch, the two log lines |
| tests/orchestration/test_staging_lifecycle.py | 326/0 | both layers, the no-op second release, the symlink refusal, the two filters |

Insertions 401.

### 127d31ea F276 R4 C4: the docs

| Path | +/- | Reason |
|------|-----|--------|
| docs/roadmap/features/T2_F276.md | 51/0 | the round 4 amendment to T003 |
| docs/system/architecture.md | 52/0 | the lifecycle, the two layers, what the copy leaves behind |

Insertions 103.

### C5 — this handoff

`.agent/handoff.md` alone. A handoff cannot table the commit that writes it (R-0149 pattern).

Every commit is under the 500-insertion cap of AGENTS.md Commit Discipline; none was declared oversize.

## External actions

- `git worktree add --detach /home/decodeux/Repos/remedy/.remedy-wt/f276-r4-mut 127d31ea` — exit 0, created for G5 only.
- `git worktree remove --force /home/decodeux/Repos/remedy/.remedy-wt/f276-r4-mut` — exit 0, as G5's last action. `git worktree list` afterwards shows the primary checkout and the operator's `job-468c8e62a2cc4fac` and nothing else.
- `git push origin feature/f276-data-root-hygiene` — reported in the round report; it follows this commit.
- No pull request created, edited or merged. No branch created or deleted. No `gh` command run.

## Verification

- G1 transport + state — `python3 -B .remedy-wt/f276-r4/g1_transport.py` → exit 0. Five payload digests True (`ledger.md`, `decisions.md`, `plan.md`, `block.md`, `f276-r4.diff`), four `.agent/authored/f276-r4-*` copies equal their payload True, `.agent/live_review.md` == `543863a0` bytes + ledger.md True, `.agent/decisions.md` == `543863a0` bytes + decisions.md True, `.agent/plan.md` == plan.md True. `READINGS 12 ALL TRUE True`. Saved block 104 lines sha256 `a60c8b28e63704fca3f289b90a0256373f412b805478ee7288ea3856588857c9`; source block 104 lines, same sha256.
- G2 code transport — `git rev-parse 127d31ea:packages 127d31ea:apps 127d31ea:tests 127d31ea:docs` → exit 0, `1cb7b9cf47cdcda2eb5b0c617f2a8673e45b416d`, `c6512f5298473ca4de84e8c8dbb811283c8e0f60`, `9ec093b7cefa773b20f9440f73a1f65a8001b43a`, `67a539fe31ec58b441a21b1366a9c280526caff8` — the four objects the block ordered, `apps` being the base's unchanged object. `git diff --name-only bc8b15b2 127d31ea` → exit 0, length 6, exactly: `docs/roadmap/features/T2_F276.md`, `docs/system/architecture.md`, `packages/orchestration/data_reclaim.py`, `packages/orchestration/pingpong_job.py`, `packages/orchestration/staging_workspace.py`, `tests/orchestration/test_staging_lifecycle.py`.
- G3 targeted suite — the block's fifteen paths, serial, no `-n`, in the primary checkout → `583 passed in 176.72s (0:02:56)`, exit 0, 0 failed.
- G4 ruff — `python3 -m ruff check packages/orchestration/staging_workspace.py packages/orchestration/data_reclaim.py packages/orchestration/pingpong_job.py tests/orchestration/test_staging_lifecycle.py` → `All checks passed!`, exit 0.
- G5 mutation red-proofs — in the disposable worktree at `127d31ea`; imported `packages.orchestration.staging_workspace` resolved to `/home/decodeux/Repos/remedy/.remedy-wt/f276-r4-mut/packages/orchestration/staging_workspace.py`, so no editable install shadowed it. Control `77 passed in 1.80s`, exit 0. (a) the hook's condition line and the `_release_job_workspace_copy(job)` line under it deleted, each counted 1 occurrence: exit 1, `1 failed, 76 passed`, FAILED `tests/orchestration/test_staging_lifecycle.py::test_terminal_copy_job_is_released_by_the_hook`. (b) that same condition line replaced by `if job_is_terminal(job.state):`, 1 occurrence: exit 1, `2 failed, 75 passed`, FAILED `test_failed_copy_job_keeps_its_staging_copy_through_the_hook` and `test_the_hook_keeps_every_copy_job_that_did_not_complete[cancelled]` — exactly the two states where the hook's vocabulary and `job_is_terminal`'s differ, as DECISION F276 D5 (7) predicts. (c) `MAX_COPY_FILE_BYTES: int = 16 * 1024 * 1024` replaced by `1 << 62`, 1 occurrence: exit 1, `2 failed, 75 passed`, FAILED `test_the_ceiling_has_the_value_its_measurement_chose` and `test_file_over_the_ceiling_is_skipped_even_when_git_does_not_ignore_it`. No mutation stayed green. Both files restored byte-identically — `pingpong_job.py` `368f3fb8011655ccbf01acbbea56d1c935ffa8ed4cf575aa1a719a0b1ecc1d1b`, `staging_workspace.py` `ded8a7c00247c3dcdd55615a1624756f511048057f29788dd886d24733e753aa`, both matching their pre-mutation readings — and the worktree's `git status --porcelain` was empty before removal.
- G6 push + clean tree — follows this commit; reported in the round report.
- Per-commit greens (constraint 7): C2 alone `130 passed in 94.50s` exit 0 over the reclaim, data-cmd, class-registry, data-paths and job-fulfillment tests, with ruff green on both edited modules; C3 alone `18 passed in 84.56s` exit 0 on the new lifecycle file with no skips, so the sandbox did not refuse `git init`; C4 touches documentation only and is covered by G3's `tests/docs` leg.
- Full suite: NOT run, per the block (amend0917-throughput rule 1).

## Open findings

14 by `scripts/rotate_live_review.py::count_open_findings` and 14 by distinct id, measured on `.agent/live_review.md` as committed at `bc8b15b2`: R-0499, R-0622, R-0662, R-0819, R-0820, R-0829, R-0866, R-0880, R-0892, R-0950, R-0984, R-0998, R-0999, R-1000. Round 3 left 15 by both readings; R-1002 is resolved by the reviewer's own `Done:` paragraph applied at C1, which is the one change to the count. No open High remains.

## Authored-text proofs

All four reviewer payloads were copied with `shutil.copyfile` and never retyped. Disk-to-disk byte comparison against the committed `.agent/authored/` copy, all True (G1): `f276-r4-block.md` `a60c8b28e63704fca3f289b90a0256373f412b805478ee7288ea3856588857c9` (104 lines), `f276-r4-ledger.md` `9b2e50af972c9b0b40cf7de5ec0a2d87d119dea501ba3801fd19eda2c31622b4` (4 lines), `f276-r4-decisions.md` `989e18eb9651c333cf026324bd1c7e2d50d887b9a708d4ba0ed974c56153208d` (60 lines), `f276-r4-plan.md` `51d8c896418fbf90029c21d3db930dc4d569dbd91520c6c83325ab593b1d9a49` (32 lines). The code diff `f276-r4.diff` verified at `a8262b6302b6a5c4036e8a87c056d68b44eba9796a105898a39f46c2cb774fe1` before the first `git apply`, and applied in three disjoint `--include` slices, never whole and never edited.

## Deviations & assumptions

- No departure from the block's ordered commit sequence: C1 to C5 in order, one commit each, none added, none dropped, none reordered.
- The `Done: R-1002` paragraph in this round's ledger append is the REVIEWER'S text, applied byte-exact as part of the ledger payload. The worker wrote no `Done:` paragraph of its own and no `Landed:` line anywhere this round.
- The diff leaves one stale doc cross-reference the worker did not repair, because a hunk may not be edited: `packages/orchestration/data_reclaim.py` line 123 still reads ``(see :func:`_job_state`)`` in the comment above `ORPHAN_JOB_STATE`, while the function is now `job_state_refusal`. It is a comment, not code; no gate reads it; ruff is green over the file. Reported rather than fixed.
- MEASURED AND SURPRISING: pytest session start in the PRIMARY checkout costs about 83 s before any test runs, while the identical tree in a fresh worktree starts in under 2 s. `--collect-only` on `tests/orchestration/test_staging_lifecycle.py` read `18 tests collected in 83.22s`, and `--durations=8` showed the tests themselves at 0.11 s setup and 0.01 s per call. The cause is the repository's own R-0803 guard: `tests/conftest.py::pytest_configure` calls `_data_root_fingerprint(resolve_data_root())`, which `os.walk`s and `lstat`s every entry under the configured data root — in the primary checkout that is the operator's 923 GB `.data`, and in a worktree it does not exist and returns `None` at once. This is pre-existing, is not caused by this round, and changes no gate's colour; it is why G3's wall-clock is dominated by a constant.
- Consequent assumption, stated rather than hidden: the worker never read, listed, wrote or deleted anything under `.data/` itself. The block-ordered pytest commands do stat it, through that R-0803 guard, which is the repository's own deliberate mechanism and not a probe of the worker's.
- The `__pycache__` purge before every G5 run reported `purged __pycache__ dirs: 0` on all four runs. That is not a purge that failed: `python3 -B` writes no bytecode and `-p no:cacheprovider` writes no pytest cache, so there was nothing to remove. The purge ran and found the worktree already clean.
- G5's `-rf` short summary is the source of every FAILED node id quoted above; no node id was inferred from a test name.
- `.agent/STOP` was checked from disk before the handoff and does not exist.
- Every test and probe used a tmp root set in-process through the suite's own `root` fixture with `monkeypatch`; no `REMEDY_DATA_DIR` was ever set as a shell assignment.
- Nothing under `.remedy-wt/` entered a commit; it is gitignored scratch.

## Next

1. Phase 1 rule 1 of `docs/agents/self_drive_protocol.md` — re-read `.agent/STOP` from disk; if it exists, write the handoff and end the session, doing nothing else.
2. The review of round 4: re-run G1 to G6 independently and read `git diff 543863a0..HEAD` bottom-up, then book the verdict.
3. T004 — `min_free_disk_bytes` on `JobBudgets` behind an injectable probe, a `free_disk` limit in `budget_guard.evaluate_budget`, checked at job start and every safe point, exhaustion taking the STOPPED path with post-mortem reason `disk_exhausted`, and a `doctor` disk section.

Operator questions open: 5
