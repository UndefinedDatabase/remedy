# Handoff — F152 round 8 (the closure's first repair round)

## Session

SESSION 1 of feature F152 · round 8 · rounds so far 8. This session read every digest before
touching a file, applied the two prepared FROM/TO byte copies exactly, ran the one full suite
once on the repaired tree, and found it fully green with no deviation of consequence.

Fortschritt: ~92 % (T001 to T003 landed; the self-use run and the suite on the repaired tree done ·
the evidence, the package and the closing round remain) — Schätzung.

## Range

Review of `d358214ee`..`1a58fee4a` (C1 to C3; C4 — this file — is the commit that carries it, per
the handback template's self-reference exception).

## Commits

### b58326c00 F152 R8 C1: book round 7's FAIL, register R-1463, the plan and the block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f152-r8.md` | +103/-0 | NEW FILE — this round's block, the authored-text proof, byte-copied from the prepared `c1-` file |
| `.agent/live_review.md` | +4/-0 | round 7's FAIL verdict booked as a Gate entry; R-1463 registered as the last paragraph |
| `.agent/plan.md` | +5/-5 | rewritten: Current Step/Next Steps to round 8 |

### 7d328380b F152 R8 C2: the A/B marker leaves the REMEDY_ namespace
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/worker_isolation.py` | +1/-1 | `ISOLATION_POISON_ENV`'s value renamed from `REMEDY_ISOLATION_POISON` to `WORKER_ISOLATION_POISON`, repairing R-1463 |
| `tests/orchestration/test_worker_isolation.py` | +1/-1 | the stand-in `claude`'s docstring updated to the new spelling |

### 1a58fee4a F152 R8 C3: the one full suite on the repaired tree and its CPU cost
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f152-closure-suite.txt` | +20/-21 | rewritten whole — the one full-suite transcript and the cost script's reading on the repaired tree |

### (this commit) F152 R8 C4: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this file — carried alone, per the handback template's self-reference exception (R-0149) |

## External actions

`gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`, run before C4's
gates. No pull request created, edited or merged. No `git worktree` command run by me. No stash
entry touched. No `claude` binary invoked by me; no provider call this round.
`git push origin feature/f152-worker-config-isolation` runs once, immediately after this commit.

## Verification

**Gate 1.** `git status --porcelain` → empty (exit 0). Then
`python3 .remedy-wt/f152-r8/prep/verify.py .` (the repository root):

```
True	b58326c00 single parent
True	b58326c00 subject carries a F152 R8 Cn tag: F152 R8 C1: book round 7's FAIL, register R-1463, the plan and the blo
True	b58326c00 adds no machine path
True	7d328380b single parent
True	7d328380b subject carries a F152 R8 Cn tag: F152 R8 C2: the A/B marker leaves the REMEDY_ namespace
True	7d328380b adds no machine path
True	1a58fee4a single parent
True	1a58fee4a subject carries a F152 R8 Cn tag: F152 R8 C3: the one full suite on the repaired tree and its CPU cost
True	1a58fee4a adds no machine path
True	on feature/f152-worker-config-isolation
True	C1 paths ['.agent/authored/f152-r8.md', '.agent/live_review.md', '.agent/plan.md']
True	C1 .agent/authored/f152-r8.md equals c1-.agent__authored__f152-r8.md
True	C1 .agent/live_review.md equals c1-.agent__live_review.md
True	C1 .agent/plan.md equals c1-.agent__plan.md
True	C2 paths ['packages/orchestration/worker_isolation.py', 'tests/orchestration/test_worker_isolation.py']
True	C2 packages/orchestration/worker_isolation.py equals c2-packages__orchestration__worker_isolation.py
True	C2 tests/orchestration/test_worker_isolation.py equals c2-tests__orchestration__test_worker_isolation.py
True	C3 paths ['.agent/authored/f152-closure-suite.txt']
True	C3 the transcript names C2's tree
absent	C4
True	the saved block equals block.md
ALL True
```

Every line `True` (C4 correctly `absent` before this commit exists); the last line `ALL True`.

**Gate 2.** C3's suite: command `python3 -m pytest -n auto -q`, real exit code `0`, wall `412.3s`
(launcher) / `411.37s (0:06:51)` (pytest). Summary line verbatim:

```
23941 passed, 11 skipped, 1 warning in 411.37s (0:06:51)
```

Bad node ids (failed + errors): NONE. The suite is fully green on the repaired tree.

**Gate 3.** `python3 -m apps.cli.main integrity check --json`, run once:

```
{"check_count": 6, "checks": [{"message": "handlers=201", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict FAIL", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```

`fail_count` 0, all six checks `pass` (`live_review_verdict`'s message correctly still names round
7's FAIL, since round 8's own verdict is the next round's first commit to book).

**Gate 4.**
`python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
→ `['R-1246', 'R-1281', 'R-1351', 'R-1353', 'R-1426', 'R-1428', 'R-1448', 'R-1450', 'R-1463']` —
exactly the eight F316-owned ids plus R-1463, nine ids total.

## Authored-text proofs

C1's byte copy (`.remedy-wt/f152-r8-worker/c1_copy.py`) read `True` for all three targets
immediately after copying: `.agent/authored/f152-r8.md`, `.agent/live_review.md`, `.agent/plan.md`.
`block.md`'s own line count and sha256 — `103` lines,
`f34d17873c9cb6aaccc7a32db638185bbfbffe749d6720f452a120a7e525e6f2` — were independently computed
directly against the prepared `block.md` and against `.agent/authored/f152-r8.md` and matched both.
C2's byte copy (`.remedy-wt/f152-r8-worker/c2_copy.py`) read `True` for both
`packages/orchestration/worker_isolation.py` and `tests/orchestration/test_worker_isolation.py`.
Gate 1's `verify.py` run independently re-confirmed every `C1 ... equals c1-...` and
`C2 ... equals c2-...` line `True`, and `the saved block equals block.md` `True`.

## Closure suite

`.agent/authored/f152-closure-suite.txt` whole and verbatim:

```
command: python3 -m pytest -n auto -q
real exit code: 0
wall time: 412.3s (the launcher's reading); pytest's own reported wall time: 411.37s (0:06:51)
summary line: 23941 passed, 11 skipped, 1 warning in 411.37s (0:06:51)
bad node ids (failed + errors): NONE
leftover processes: NONE
tree it ran on: 7d328380b (F152 R8 C2: the A/B marker leaves the REMEDY_ namespace)
tree note: C1 changed only .agent/ files; C2 renamed the A/B marker in one module and one test docstring
reflog before: 7d328380b HEAD@{2026-10-24 10:25:59 +0200}: commit: F152 R8 C2: the A/B marker leaves the REMEDY_ namespace
reflog after: 7d328380b HEAD@{2026-10-24 10:25:59 +0200}: commit: F152 R8 C2: the A/B marker leaves the REMEDY_ namespace
reflog unchanged during the run: yes
cost command: python3 scripts/closure_suite_cost.py --feature F152 --record ~/.remedy-loop/test_load.jsonl
cost exit code: 0
Test load: 1526.77 CPU seconds, 411.40 wall seconds, 23952 tests collected, exit status 0, recorded 2026-10-24T08:33:00Z
This closure's suite used 1526.77 CPU seconds, 8.0 percent more than F157's 1413.16, within the 10 percent limit.
The limit is the larger of 10 percent and the largest spread between full-suite runs of the record that collected the same tests, 0 percent.
The test modules whose CPU time rose most since F157's closure run:
  +7.69 s  tests/orchestration/test_job_worktree_integrity.py (6.93 -> 14.62)
  +5.62 s  tests/cli/test_scoped_listings.py (11.11 -> 16.73)
  +5.18 s  tests/cli/test_do_order_budget.py (4.75 -> 9.93)
  +4.93 s  tests/orchestration/test_persisted_call_ownership.py (9.76 -> 14.69)
  +4.88 s  tests/orchestration/test_subtree_rerun_prepare.py (12.21 -> 17.09)
  +4.85 s  tests/cli/test_mission_cmd.py (48.30 -> 53.15)
  +4.56 s  tests/orchestration/test_self_use_runner.py (4.74 -> 9.30)
  +4.18 s  tests/cli/test_do_flags.py (4.73 -> 8.91)
  +4.15 s  tests/orchestration/test_persisted_call_episode_membership.py (3.51 -> 7.66)
  +4.11 s  tests/orchestration/test_job_apply_history.py (7.79 -> 11.90)
```

## Deviations & assumptions

1. The block's C3 step 4 spells the cost script's record path as `~/.remedy-loop/test_load.jsonl`,
   a shell tilde the sandbox's forbidden `cd`/no-shell-expansion constraint meant I could not type
   literally into an interactive shell command; I ran the script through a small `python3`
   `subprocess.run(..., cwd=repo_root)` wrapper under `.remedy-wt/f152-r8-worker/` instead, passing
   the already-expanded path under this account's own home directory — the exact path a shell
   would have expanded that tilde to — as the `--record` argument. The command run and its effect
   are otherwise identical to the block's literal text.
2. `git show --numstat` of C3 reports `20 21` for `.agent/authored/f152-closure-suite.txt` rather
   than the `27 28` git's own commit-time summary first printed; both `git show --stat` and
   `git diff --stat` against the parent commit, run independently afterward, agree at `20
   insertions(+), 21 deletions(-)`, which is the number this handback's Commits table uses. The
   discrepancy is git's own "rewrite" heuristic in the terse commit-creation message, not a defect
   in the committed diff.

No other departure from the block's ordered commit sequence: no split, no correction commit, no
file touched outside the paths named per commit, no second test command, no
`REMEDY_TEST_MAX_WORKERS`, a single `-n auto`, no `claude` binary invoked by me, no worktree of my
own, no mutation beyond the two ordered byte copies.

## For the operator, in plain sentences

The repair renamed an internal test marker that had accidentally been spelled like one of the
product's own settings names, so the check that watches for that no longer flags it. Across the
whole test collection, 23,941 tests passed and none failed this time.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | three files byte-equal to the prepared snapshots; block.md 103 lines, sha256 matched |
| C2 | done | numstat `1 1` for each of the two paths, repairing R-1463 |
| C3 | done | one full suite run (green, zero bad node ids), cost script exit 0 within budget |
| C4 | done | this handback |
| R-1463 | done | repaired by C2; the reviewer books its resolution in the next round's first commit |
| Gate 1 | done | every line `True`, last line `ALL True` |
| Gate 2 | done | exit 0, summary line verbatim, zero bad node ids |
| Gate 3 | done | `fail_count` 0, all six checks pass |
| Gate 4 | done | nine open ids, matching the eight F316-owned ids plus R-1463 |
| Push | pending | runs once immediately after this commit |

## Next

1. Phase 1 rule 1: check `.agent/STOP` before any new work.
2. Phase 1 rule 2: the Open PR Gate — no pull request is open for this branch yet.
3. The reviewer reviews round 8, books its verdict and resolves R-1463 in the next round's first
   commit.
4. The evidence bundle and the review package.
5. The closing round.

Operator questions open: 3.
Open findings: 9.
