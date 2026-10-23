# Handback — F151 round 8

## Session

SESSION 1 of feature F151 · round 8 · rounds so far 8.

Context self-assessment: both prepared top-level digests (`block.md`, `digests.txt`) and all seven
files `digests.txt` listed under `.remedy-wt/f151-r8/prep/` were checked against `digests.txt` with
a Python sha256 reader before any file was used, the block was read in full before any commit, and
the one full suite was run exactly once through `launch.py`/`wait.py`, read verbatim and committed
without edit, investigation or re-run.

Fortschritt: ~92 % (T001 to T003, the docs, the self-use run and the suite's repair done · the evidence, the package and the closing round remain) — Schätzung

Landed: R-1441 — the docs page `docs/system/worker-adapter-contract-v1.md` named `remedy workers
--json`, a command the operator-facing catalog does not carry; corrected to `remedy worker list
--json`, `7e32f147e`.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | three prepared paths copied and proved byte-identical; `block.md` confirmed 119 lines, sha256 `5214af6b...776`; staged and committed alone |
| C2 | done | one prepared docs path copied and proved byte-identical; `git show --numstat` read `1	1`; staged and committed alone |
| C3 | done — suite GREEN | `launch.py`/`wait.py suite` exit 0, wall 367.7s; no bad node id; reflog unchanged during the run; cost script exit 0; transcript rewritten in full and committed alone |
| C4 | done | this handback |
| R-1441 | done | repaired in C2, verified by the C3 suite no longer failing the node it named |
| Gate 1 | done — PASS | `git status --porcelain` empty; `verify.py` every line `True`, `C4` read `absent` at gate time, last line `ALL True` |
| Gate 2 | done — PASS | suite exit 0, summary line `23670 passed, 11 skipped, 1 warning in 366.73s (0:06:06)`, no bad node ids |
| Gate 3 | done — PASS | `integrity check --json` → `fail_count` 0, six checks all `pass`; `open_finding_ids` → the twelve ids exactly |

## Range

Review of `bbc8a9c60`..`HEAD` (`HEAD` is this handback's own commit).

## Commits

### `e1c1a2794` F151 R8 C1: book round 7, register R-1441, the plan and the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f151-r8.md` | +119/-0 (new) | byte copy of this round's own block, proved equal to it |
| `.agent/live_review.md` | +4/-0 | round 7's VERDICT FAIL gate entry booked, with R-1441 registered |
| `.agent/plan.md` | +3/-3 | rewritten: current step round 8's repair, next steps the evidence and closing rounds |

### `7e32f147e` F151 R8 C2: the docs page names the catalog's worker list command

| Path | +/- | Reason |
|---|---|---|
| `docs/system/worker-adapter-contract-v1.md` | +1/-1 | `remedy workers --json` corrected to `remedy worker list --json`, the R-1441 repair |

### `addc1a5c1` F151 R8 C3: the closure's one full suite on the repaired tree and its CPU cost

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f151-closure-suite.txt` | +20/-21 | the suite's transcript rewritten in full: command, exit code, wall time, summary line, no bad node id, leftover processes NONE, tree/reflog lines, the cost script's command, exit code and every line it printed |

### This commit (C4) — handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this file, per `docs/agents/handback_template.md` |

## External actions

- `git push origin feature/f151-worker-adapter-contract` — run once, immediately after this commit.
- No pull request was opened (none is open for this branch; the Open PR Gate's precondition held
  `[]` before this round started). No worktree was added or removed by this worker. No merge, no
  rebase, no amend, no stash. No provider call was made this round.

## Verification

Interpreter: the repository's configured Python 3 (`python3`, system install). All three gates were
run once each, after C3 and before C4, per the block.

Gate 1 — `git status --porcelain` → empty (no output). `python3 .remedy-wt/f151-r8/prep/verify.py .`
→ every line `True`: all three commits single-parent and under 500 insertions (126, 1, 20), each
carries an `F151 R8 Cn` subject, on `feature/f151-worker-adapter-contract`; C1's three paths exact
and byte-equal to their `c1-*` snapshots; C2's one path exact and byte-equal to its `c2-*` snapshot;
C3 is the transcript alone and holds no machine path; `C4` read `absent` (not yet committed at gate
time); the ledger holds no `Landed`/`Done` line for R-1441; the saved block equals `block.md`; last
line `ALL True`.

Gate 2 — the suite of C3, as the transcript records it: exit code `0`; summary line
`23670 passed, 11 skipped, 1 warning in 366.73s (0:06:06)`; bad node ids (failed + errors): `NONE`.

Gate 3 — `python3 -m apps.cli.main integrity check --json` →
`{"check_count": 6, "checks": [{"message": "handlers=197", "name": "handler_import", "status":
"pass"}, {"message": "last Gate verdict FAIL", "name": "live_review_verdict", "status": "pass"},
{"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"},
{"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message":
"no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status":
"pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status":
"pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}`.
`python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
→ `['R-1246', 'R-1281', 'R-1326', 'R-1351', 'R-1353', 'R-1418', 'R-1421', 'R-1425', 'R-1426',
'R-1427', 'R-1428', 'R-1441']` — the twelve ids exactly.

## Closure suite

`.agent/authored/f151-closure-suite.txt`, whole and verbatim:

```
command: python3 -m pytest -n auto -q
real exit code: 0
wall time: 367.7s (the launcher's reading); pytest's own reported wall time: 366.73s (0:06:06)
summary line: 23670 passed, 11 skipped, 1 warning in 366.73s (0:06:06)
bad node ids (failed + errors): NONE
leftover processes: NONE
tree it ran on: 7e32f147e (F151 R8 C2: the docs page names the catalog's worker list command)
tree note: the repair of round 7's one bad node; C1 changed only .agent/ files and C2 one docs page
reflog before: 7e32f147e HEAD@{2026-10-23 17:19:31 +0200}: commit: F151 R8 C2: the docs page names the catalog's worker list command
reflog after: 7e32f147e HEAD@{2026-10-23 17:19:31 +0200}: commit: F151 R8 C2: the docs page names the catalog's worker list command
reflog unchanged during the run: yes
cost command: python3 scripts/closure_suite_cost.py --feature F151 --record ~/.remedy-loop/test_load.jsonl
cost exit code: 0
Test load: 1300.34 CPU seconds, 366.77 wall seconds, 23681 tests collected, exit status 0, recorded 2026-10-23T15:25:45Z
This closure's suite used 1300.34 CPU seconds, 7.2 percent less than F133's 1401.83, within the 10 percent limit.
The limit is the larger of 10 percent and the largest spread between full-suite runs of the record that collected the same tests, 0 percent.
The test modules whose CPU time rose most since F133's closure run:
  +3.55 s  tests/orchestration/test_disk_floor.py (1.04 -> 4.59)
  +1.18 s  tests/orchestration/test_client_diff.py (3.87 -> 5.05)
  +1.16 s  tests/contracts/test_adapter_import_guard.py (0.00 -> 1.16)
  +0.93 s  tests/orchestration/test_subtree_rerun_prepare.py (10.60 -> 11.53)
  +0.87 s  tests/orchestration/test_review_reports.py (3.40 -> 4.27)
  +0.66 s  tests/orchestration/test_do_then_story.py (4.52 -> 5.18)
  +0.66 s  tests/orchestration/test_run_manifest_call_task_binding.py (5.36 -> 6.02)
  +0.63 s  tests/cli/test_job_run_session_resume.py (1.83 -> 2.46)
  +0.62 s  tests/orchestration/test_run_manifest_task_lifecycle_binding.py (3.07 -> 3.69)
  +0.57 s  tests/cli/test_pytest_runner.py (9.56 -> 10.13)
```

## Authored-text proofs

C1's one new file and two rewrites, and C2's one path, are reviewer-authored or reviewer-produced
text applied this round. Each was copied from its prepared `c1-*`/`c2-*` file under
`.remedy-wt/f151-r8/prep/` by a dedicated `python3` script under `.remedy-wt/f151-r8-worker/`, which
compared source and destination bytes immediately after each copy; all four pairs read equal.
`block.md` itself (saved as `.agent/authored/f151-r8.md`) was separately confirmed equal to the
prepared `block.md` by its sha256 (given in the prompt, checked before any file was used), again by
line count (119) and sha256 directly against `block.md`, and a third time by `verify.py`'s own check
for that path. `.agent/authored/f151-closure-suite.txt` (C3) is NOT reviewer-authored text — it is
this worker's own output from the block's instructions — so no disk-to-disk comparison applies to
it.

## Deviations & assumptions

None.

## Next

1. Phase 1 rule 1: check whether `.agent/STOP` exists (absent at the time of this handback).
2. Rule 2, the Open PR Gate: no pull request is open for this branch yet.
3. The reviewer reviews round 8 and books its verdict in the next round's first commit.
4. The evidence bundle and the review package.
5. The closing round: the Built State, the rotation, the STATUS line, the README and the pull
   request.

Operator questions open: 0. Open findings: 12, gate 3 printed.

## For the operator, in plain sentences

The first run of the whole test collection, in the previous round, found one wrong command name on
the new documentation page; this round corrected it. The run on the corrected code passed all
roughly twenty-three thousand seven hundred tests, with none failing, taking a little over six
minutes. The cost reading said this run's computer time was somewhat lower than the previous
feature's, comfortably inside the allowed margin.
