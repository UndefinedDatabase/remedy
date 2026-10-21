# Handback — F078 round 8: the closure's first repair round (R-1392, R-1393, the one full suite again)

## Session

SESSION 2 of feature F078 · round 8 · rounds so far 8

Context self-assessment: this worker copied prepared files, ran the suite through the helpers and wrote text, and the context was far from exhausted.

Fortschritt: ~94 % (T001 to T003 landed, contract 1.23, self-use run done; the suite taken again on the repaired tree · the evidence, the package and the closing round remain) — Schätzung

## Range

Review of `84f74d812`..`HEAD` on `feature/f078-autonomy-levels-2` (base: round 7's handback commit `84f74d812`).

## Commits

### 9fb8826d1 F078 R8 C1: book round 7, register R-1392 and R-1393, DECISION F078 D7 and the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f078-r8.md` | +128/-0 | new: the block of this round |
| `.agent/live_review.md` | +6/-0 | round 7 booked, R-1392 and R-1393 registered |
| `.agent/decisions.md` | +10/-0 | DECISION F078 D7 |
| `.agent/plan.md` | +6/-6 | rewritten |

### 388558dc8 F078 R8 C2: the autonomy records' names join the event vocabulary (R-1393)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/event_names.py` | +5/-0 | `deferred`, `started`, `taken` in their alphabetical places, two-line comment above the first |

### 0d7044307 F078 R8 C3: the context names its steps again (R-1392)
| Path | +/- | Reason |
|---|---|---|
| `.agent/context.md` | +3/-0 | the `## Steps` section restored |

### 82f53a225 F078 R8 C4: the closure's one full suite again, on the repaired tree
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f078-closure-suite.txt` | +27/-30 | transcript replaced in full |

### (this commit) F078 R8 C5: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | full rewrite | this handback |

## External actions

- No provider call, no pull request opened or created.
- `git push origin feature/f078-autonomy-levels-2` after this commit: result in the worker's final reply.

## Verification

1. Preconditions: `git rev-parse --short=9 HEAD` `84f74d812`, equal to the remote branch tip; `git status --porcelain` empty; `.agent/STOP` absent. All prepared digests matched (block.md 128 lines, sha256 `f507275ad99767c0b26579e47a78b2687581347c70a6220948de79faecbffd73`).
2. C2 `git diff --cached`: three names added in their alphabetical places and a two-line comment above the first. C3 `git diff --cached`: only the appended `## Steps` section.
3. Suite (C4): `launch.py suite` then `wait.py suite 50`: `exit 0 wall 362.2`; `22188 passed, 11 skipped, 1 warning in 361.45s (0:06:01)`. Reflog unchanged during the run. Cost script exit 0.
4. Gate 1: `git status --porcelain` empty; `verify.py .`: every line `True`, C5 `absent`, last line `ALL True`.
5. Gate 2: suite exit 0, summary `22188 passed, 11 skipped, 1 warning in 361.45s (0:06:01)`, bad node ids NONE.
6. Gate 3: `python3 -m apps.cli.main integrity check --json`: exit 1, `fail_count` 1, the one failing check `high_blockers_open`: `12 open blocker/high: R-1335, R-1336, R-1337, R-1338, R-1345, R-1346, R-1348, R-1349, R-1359, R-1360, R-1361, R-1362`. `open_finding_ids` count: `89`.

## Closure suite

Quoting `.agent/authored/f078-closure-suite.txt` whole:

```
command: python3 -m pytest -n auto -q
real exit code: 0
wall time: 362.2s (the launcher's reading); pytest's own reported wall time: 361.45s (0:06:01)
summary line: 22188 passed, 11 skipped, 1 warning in 361.45s (0:06:01)
bad node ids (failed + errors): NONE
leftover processes: NONE
tree it ran on: 0d7044307 (F078 R8 C3: the context names its steps again (R-1392))
tree note: the repaired tree of round 8; round 7's transcript stays in git history at 1287824bc
reflog before: 0d7044307 HEAD@{2026-10-21 06:49:57 +0200}: commit: F078 R8 C3: the context names its steps again (R-1392)
reflog after: 0d7044307 HEAD@{2026-10-21 06:49:57 +0200}: commit: F078 R8 C3: the context names its steps again (R-1392)
reflog unchanged during the run: yes
cost command: python3 scripts/closure_suite_cost.py --feature F078 --record ~/.remedy-loop/test_load.jsonl
cost exit code: 0
Test load: 1304.28 CPU seconds, 361.46 wall seconds, 22199 tests collected, exit status 0, recorded 2026-10-21T04:56:02Z
This closure's suite used 1304.28 CPU seconds, 0.0 percent less than F313's 1304.91, within the 10 percent limit.
The limit is the larger of 10 percent and the largest spread between full-suite runs of the record that collected the same tests, 0 percent.
The test modules whose CPU time rose most since F313's closure run:
  +3.72 s  tests/cli/test_do_scale_matrix.py (37.13 -> 40.85)
  +2.74 s  tests/orchestration/test_self_use_runner.py (6.09 -> 8.83)
  +2.37 s  tests/cli/test_scoped_listings.py (10.09 -> 12.46)
  +2.07 s  tests/orchestration/test_worktrees.py (1.65 -> 3.72)
  +1.92 s  tests/orchestration/test_review_zip_hygiene.py (37.85 -> 39.77)
  +1.82 s  tests/orchestration/test_autonomy_seams.py (0.00 -> 1.82)
  +1.39 s  tests/orchestration/test_persisted_run_call_schema.py (1.86 -> 3.25)
  +1.19 s  tests/runtimes/test_runtime_lifecycle_safety.py (2.88 -> 4.07)
  +1.17 s  tests/orchestration/test_task_deliverables.py (3.05 -> 4.22)
  +1.05 s  tests/cli/test_golden_path.py (18.57 -> 19.62)
```

The bad set is empty, strictly smaller than round 7's three nodes, and no node is newly bad.

## Authored-text proofs

C1, C2, C3: each prepared file is a byte copy, proven by a Python equality over bytes at copy time (all True) and again by `verify.py` (all `True`). All prepared digests were checked before use and every one matched.

## Deviations & assumptions

None. (The helpers `launch.py` and `wait.py` and the cost script were run through a small wrapper script that sets the repository root as the working directory; the cost record path was written out as the home directory's `.remedy-loop/test_load.jsonl` because the shell does not expand `~` inside a wrapper argument, and the transcript shows the block's `~` form. Gate 3 exits 1 by design.)

## For the operator, in plain sentences

The first whole test run before closing found three small mistakes of this feature: two lists that did not name the autonomy level's own records and one note file that had lost a heading a test reads. They were repaired, and the second whole run passed: 22188 tests passed, none failed, 11 were skipped on purpose, and it took about six minutes.

## Next

1. Phase 1 rule 1: `.agent/STOP`.
2. Phase 1 rule 2: the Open PR Gate; no pull request is open for this branch yet.
3. The reviewer reviews round 8 and books its verdict and the resolutions of R-1392 and R-1393 in the next round's first commit.
4. The evidence bundle and the review package (the suite is green).
5. The closing round: the STATUS line, the README and the pull request.

Operator questions open: 2.
Open findings: 89 (rule: `scripts.rotate_live_review.open_finding_ids` over `.agent/live_review.md`, gate 3 at commit `82f53a225`).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | `9fb8826d1` |
| C2 | done | `388558dc8` |
| C3 | done | `0d7044307` |
| C4 | done | `82f53a225`, suite green |
| C5 | done | this commit |
| Gate 1 | done | ALL True |
| Gate 2 | done | exit 0, 22188 passed, no bad node |
| Gate 3 | done | fail_count 1, the twelve findings; 89 open |
