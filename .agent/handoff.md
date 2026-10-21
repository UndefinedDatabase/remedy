# Handback — F141 round 2: the builder's context leaves `run_pingpong`, a job keeps its level, and the `read` seam

## Session

SESSION 1 of feature F141 · round 2 · rounds so far 2

Context self-assessment: this worker verified every prepared digest, did the structural move exactly as spelled out, wrote the pin and the `read` seam and their tests from the block's given sentences, ran all six gates, and the context was far from exhausted.

Fortschritt: ~30 % (T001, the pinned level and the read seam landed · the other seams and T003 open) — Schätzung

## Range

Review of `029010d08`..`HEAD` on `feature/f141-permission-matrix` (base: round 1's handback).

## Commits

### b25a50175 F141 R2 C1: book round 1, register R-1395, DECISION F141 D2, the plan and the block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f141-r2.md` | +197/-0 | new: the block of this round |
| `.agent/decisions.md` | +10/-0 | DECISION F141 D2 |
| `.agent/live_review.md` | +4/-0 | R-1395 registered |
| `.agent/plan.md` | +12/-11 | re-headed for round 2 |

### 5457caf41 F141 R2 C2: the builder's context moves to builder_context.py (structure step)
| Path | +/- | Reason |
|---|---|---|
| `docs/system/structure-ledger-v1.md` | +4/-3 | step (5) sentence; both rows' sizes lowered |
| `packages/orchestration/builder_context.py` | +68/-0 | new: `build_builder_context`, moved unchanged bar one indent level |
| `packages/orchestration/pingpong_loop.py` | +8/-47 | `run_pingpong` now calls the moved function; one sorted import added |
| `tests/orchestration/import_reachability_allowlist.txt` | +1/-0 | `packages.orchestration.builder_context`, now reachable |
| `tests/test_structure_ratchet.py` | +2/-2 | `MAX_FUNCTION_LINES` and `MAX_FILE_LINES` lowered by the same two differences |

### b8724e6f2 F141 R2 C3: a job keeps the level of its first context, and the read seam (DECISION F141 D2)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/builder_context.py` | +13/-0 | the `read` check before anything else in the body |
| `packages/orchestration/permission_matrix.py` | +54/-4 | `JOB_LEVEL_FILENAME`, `pinned_job_level`, `pin_job_level`; R-1395: `cells` now carries citations |
| `packages/orchestration/pingpong_loop.py` | +1/-1 | the call now forwards `job_id` |
| `tests/orchestration/import_reachability_allowlist.txt` | +1/-0 | `packages.orchestration.permission_matrix`, now reachable from production code |
| `tests/test_no_orphan_modules.py` | +0/-2 | stale `ALLOWED_UNWIRED` entry removed |

### de3e3a496 F141 R2 C4: tests of the pinned level, the read seam and the citations
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_builder_context.py` | +134/-0 | new: the default path, the denied read, the `run_pingpong` mirror, no-job-id |
| `tests/orchestration/test_permission_matrix.py` | +110/-2 | citation assertions on `verdict.cells`; `pinned_job_level`/`pin_job_level` tests |

Exception (self-reference), per `docs/agents/handback_template.md`: this commit, which writes
`.agent/handoff.md`, is not tabled here — its own diff never appears in this file.

## External actions

- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` at session start: `[]` (no open pull request; the Open PR Gate passed without a merge).
- The push after this commit: result in the worker's final reply (the handoff cannot hold the result of the commit that writes it).
- No provider call, no rotation, no worktree, no merge, no pull request created.

## Verification

Preconditions: `git rev-parse HEAD` read `029010d08ddb2fe51f86cb5d2c78f5e8525e13a5` on `feature/f141-permission-matrix`, clean `git status --porcelain`, before any write. `gh pr list --state open ...` read `[]`. Every prepared digest (`block.md` 197 lines, and `verify.py`, `run_selection.py`, `selection.txt`, `digests.txt`, each by its own sha256) matched the prompt before use; the four `c1-*` files then matched `digests.txt` before being copied.

1. `git status --porcelain` (before C5): empty. `python3 .remedy-wt/f141-r2/prep/verify.py .`: every line `True`, `absent	C5`, last line `ALL True`.
2. `python3 -m ruff check` over every Python file C2, C3 and C4 touched (`pingpong_loop.py`, `builder_context.py`, `test_structure_ratchet.py`, `permission_matrix.py`, `test_no_orphan_modules.py`, `test_permission_matrix.py`, `test_builder_context.py`): `All checks passed!`.
3. `python3 .remedy-wt/f141-r2/prep/run_selection.py . .remedy-wt/f141-r2-worker/selection-output.txt`: `paths 83`, `exit 0`, `3987 passed, 2 skipped in 115.20s (0:01:55)`, no FAILED or ERROR line, no `process(es) behind` line. SKIPPED: `tests/test_agent_tooling.py:43` (D12 quarantine, F252), `tests/test_install_smoke.py:175` (install smoke is opt-in).
4. `python3 -m apps.cli.main integrity check --json`: exit 1, `fail_count` 1, the one failing check `high_blockers_open`: `12 open blocker/high: R-1335, R-1336, R-1337, R-1338, R-1345, R-1346, R-1348, R-1349, R-1359, R-1360, R-1361, R-1362` — the same twelve as before this round.
5. `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"`: `88`.
6. `git show --numstat --format=%h HEAD~1 HEAD~2` restricted to `pingpong_loop.py`: C3 (`HEAD~1`) `1	1`; C2 (`HEAD~2`) `8	47`.

Structure measurements (DECISION F141 D2 (1), the structural step): `run_pingpong` fell from 1314 to 1274 lines (−40); `packages/orchestration/pingpong_loop.py` fell from 5231 to 5192 lines (−39). Both pins fell by exactly those two differences: `MAX_FUNCTION_LINES` 28744 → 28704, `MAX_FILE_LINES` 64216 → 64177. After C3 both measures are unchanged from C2 (confirmed: the one `pingpong_loop.py` line C3 touches only adds `job_id=job_id` to an existing call line, no line added or removed).

## Authored-text proofs

C1: each of the four prepared files (`c1-.agent__authored__f141-r2.md`, `c1-.agent__decisions.md`, `c1-.agent__live_review.md`, `c1-.agent__plan.md`) is a byte copy, proven by a Python sha256 equality at copy time (all `True`) and again by `verify.py`'s own byte comparison (all `True`). Every prepared digest was checked before use and every one matched.

C2, C3, C4: none applied. The block gave the exact move boundaries, the function signature, every refusal sentence and every WHY comment's substance by its literal text, and the test behaviours by their given sentences — there was no prepared `.agent/authored/` file to byte-copy against for these commits, only the block's own prose, checked by hand against it while writing.

## Deviations & assumptions

- C2's "one indentation level less" (block §C2.1) is read as: the moved code's own `try:` wrapper (around the `if use_compiled_context: ... else: ...`) is dropped — exception handling now lives in `run_pingpong`'s caller-side `try`/`except` around the call — and the `if`/`else` body shifts left by the one level that wrapper held. The alternative reading (shifting every moved line left by one level regardless of content) produces a syntactically invalid function body, since the block's own quoted span ends mid-`try` with no matching `except`. Recorded because the block's literal instruction is terse; the chosen reading is the only one that parses and it preserves exact behaviour, confirmed by the full existing `pingpong`/`worktree_cleanup` test suites passing unchanged.
- C3's atomic write for `pin_job_level` reuses the repository's one existing path-based atomic writer, `packages.common.secure_fs.durable_write_json` (temp file via `tempfile.mkstemp` in the destination directory, then `os.replace`), rather than hand-rolling a second `os.replace` call site. The block names the mechanism ("a temporary file in the same folder, then `os.replace`") but not the call; reusing the audited helper is the "one spelling per concept" reading of `AGENTS.md`'s discoverability conventions.
- C4's two `verdict.cells` assertions and the `pinned_job_level`/`pin_job_level` test names are the worker's own choice of location and naming; the block gave the behaviours, not literal test source.

## For the operator, in plain sentences

This round moved a chunk of code out of the loop that runs one round of building and reviewing, into a function of its own, without changing anything it does — that is bookkeeping, not a feature. Then it added the piece a running job now keeps: the level it was allowed to run at gets written down the first time that job asks for its starting context, and every later check against that same job reads the same written answer back, so a person changing the global setting mid-run can never quietly change what an already-running job is allowed to do. The first of the eight checks this feature is building, "may Remedy read your files", now actually runs on that path, refusing before anything is read when the table says no. A small mismatch from last round, where two of the matrix's answers carried the wrong detail, is fixed. The whole relevant test collection ran and passed. Three questions from before this feature still wait for you.

## Next

1. Phase 1 rule 1: `.agent/STOP`.
2. Phase 1 rule 2: the Open PR Gate.
3. Book round 2's verdict in the next round's first commit.
4. Round 3: the structural step of `job_apply.py` and the write, commit and push seams.

Operator questions open: 3.
Open findings: 88 (R-1395 owned by F141, repaired in C3).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | `b25a50175` |
| C2 | done | `5457caf41` |
| C3 | done | `b8724e6f2` |
| C4 | done | `de3e3a496` |
| C5 | done | this commit |
| Gate 1 | done | ALL True |
| Gate 2 | done | All checks passed! |
| Gate 3 | done | exit 0, 3987 passed, 2 skipped |
| Gate 4 | done | fail_count 1, the twelve findings; 88 open |
| Gate 5 | done | 88 |
| Gate 6 | done | C3 `1 1`, C2 `8 47` |
