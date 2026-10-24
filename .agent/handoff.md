# Handoff — F158 round 7

## Session

SESSION 2 of feature F158 · round 7 · rounds so far 7. This session verified the prepared digest
and every file's sha256 before touching anything, applied the five ordered commits exactly as the
block specified, and found all four gates green on the first and only run of each, with comfortable
context headroom throughout.

Fortschritt: ~92 % (T001 to T003 built; R-1471 repaired, the consolidation pass, the self-use run and the one full suite done · the evidence, the package and the closing round remain) — Schätzung.

## Range

Review of `02955645d`..`7a80b7611` (C1 to C5; C6 — this file — is the commit that carries it, per
the handback template's self-reference exception).

## Commits

### d0ecb839c F158 R7 C1: book round 6, register R-1471, the plan, the block and the self-use script
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f158-r7.md` | +165/-0 | NEW FILE — this round's block, the authored-text proof, byte-copied from the prepared `c1-` file |
| `.agent/authored/f158-r7-selfuse.py` | +224/-0 | NEW FILE — the reviewer-authored self-use script for this round, byte-copied |
| `.agent/live_review.md` | +4/-0 | round 6's PASS verdict booked and R-1471 registered, byte-copied |
| `.agent/plan.md` | +8/-8 | rewritten: Current Step/Next Steps moved to round 7, byte-copied |

### 9f50d3b6a F158 R7 C2: repair R-1471, the do guide names the cost object's dollar field
| Path | +/- | Reason |
|---|---|---|
| `docs/guides/do-run-v1.md` | +2/-2 | the sentence naming `cost.cost_usd` as a configuration key now names it as the `cost_usd` field of the `cost` object, byte-copied |

### e8ee05c84 F158 R7 C3: the checklist's consolidation pass for F158
| Path | +/- | Reason |
|---|---|---|
| `docs/agents/planner_reviewer_prompt.md` | +10/-0 | F158's consolidation paragraph appended: nothing joined, no two items merged, the list stays at 34 items, byte-copied |

### b16e6f296 F158 R7 C4: the closure's self-use item run to its approval gate, never applied
| Path | +/- | Reason |
|---|---|---|
| `scripts/self_use_queue.json` | +8/-0 | the generator's one appended entry, `SU-084`, `consumed_by` empty |
| `.agent/selfuse_f158/SU-084.md` | +11/-0 | NEW FILE — the job markdown |
| `.agent/selfuse_f158/entry_and_job_file.txt` | +5/-0 | NEW FILE |
| `.agent/selfuse_f158/execution_config.txt` | +43/-0 | NEW FILE |
| `.agent/selfuse_f158/result_state.txt` | +12/-0 | NEW FILE |
| `.agent/selfuse_f158/timing.txt` | +3/-0 | NEW FILE |
| `.agent/selfuse_f158/changed_paths.txt` | +1/-0 | NEW FILE |
| `.agent/selfuse_f158/full_transcript.txt` | +14/-0 | NEW FILE |
| `.agent/selfuse_f158/worker_isolation.txt` | +2/-0 | NEW FILE |
| `.agent/selfuse_f158/worker_sandbox.txt` | +2/-0 | NEW FILE |
| `.agent/selfuse_f158/valuations.txt` | +1/-0 | NEW FILE — `NONE` (no project ledger carries a row for this job) |
| `.agent/selfuse_f158/staleness_after.txt` | +2/-0 | NEW FILE |
| `.agent/selfuse_f158/job_diff.txt` | +145/-0 | NEW FILE |
| `.agent/selfuse_f158/run_defects.txt` | +1/-0 | NEW FILE — `NONE` |

### 7a80b7611 F158 R7 C5: the closure's one full suite and its CPU cost
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f158-closure-suite.txt` | +27/-0 | NEW FILE — the one full-suite transcript and the cost script's reading, in the shape of `f162-closure-suite.txt` |

### (this commit) F158 R7 C6: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this file — carried alone, per the handback template's self-reference exception (R-0149) |

## External actions

`gh pr list --state open --json number,headRefName,baseRefName,isDraft` run once before any write
→ `[]` (Open PR Gate). No other `gh` command run. No `git worktree` command run by me directly; the
reviewer-authored self-use script (C4) added and removed one detached worktree of the job branch
`remedy/job-e796fd1de2eb4516` itself, to read the job's post-run staleness catalog, and removed it
before exiting — that is the script's own documented action (`.agent/authored/f158-r7-selfuse.py`),
not a worktree of mine. No stash entry touched. No `claude` or `codex` binary invoked by me
directly; the self-use run's two provider calls were made by the `self_use` role's configured
provider through the run infrastructure the script calls, at the role's budget, exactly as the
block expected. No web fetch by me.
`git push origin feature/f158-cost-normalization` runs once, immediately after this commit, per
the block's push instruction; its real outcome is reported in the session reply, not in this file.

## Verification

**Gate 1.** `git -C <repo> status --porcelain` → empty (exit 0). Then
`python3 .remedy-wt/f158-r7/prep/verify.py <repo>`, run once from the primary checkout:
```
True	d0ecb839c single parent equal to the commit before it
True	d0ecb839c subject carries a F158 R7 Cn tag: F158 R7 C1: book round 6, register R-1471, the plan, the block and the
True	d0ecb839c adds no machine path
True	9f50d3b6a single parent equal to the commit before it
True	9f50d3b6a subject carries a F158 R7 Cn tag: F158 R7 C2: repair R-1471, the do guide names the cost object's dollar
True	9f50d3b6a adds no machine path
True	e8ee05c84 single parent equal to the commit before it
True	e8ee05c84 subject carries a F158 R7 Cn tag: F158 R7 C3: the checklist's consolidation pass for F158
True	e8ee05c84 adds no machine path
True	b16e6f296 single parent equal to the commit before it
True	b16e6f296 subject carries a F158 R7 Cn tag: F158 R7 C4: the closure's self-use item run to its approval gate, neve
True	b16e6f296 adds no machine path
True	7a80b7611 single parent equal to the commit before it
True	7a80b7611 subject carries a F158 R7 Cn tag: F158 R7 C5: the closure's one full suite and its CPU cost
True	7a80b7611 adds no machine path
True	on feature/f158-cost-normalization
True	C1 paths ['.agent/authored/f158-r7-selfuse.py', '.agent/authored/f158-r7.md', '.agent/live_review.md', '.agent/plan.md']
True	C1 .agent/authored/f158-r7-selfuse.py equals its c1- file
True	C1 .agent/authored/f158-r7.md equals its c1- file
True	C1 .agent/live_review.md equals its c1- file
True	C1 .agent/plan.md equals its c1- file
True	C2 the do guide alone
True	C2 guide equals the prepared copy
True	C2 numstat ['2\t2\tdocs/guides/do-run-v1.md']
True	C2 no doc_config_keys claim at HEAD: []
True	C3 the checklist page alone
True	C3 page equals the prepared copy
True	C3 numstat ['10\t0\tdocs/agents/planner_reviewer_prompt.md']
True	C4 paths: the queue and 13 file(s) under .agent/selfuse_f158/
True	C4 writes thirteen self-use files: 13
True	C4 writes entry_and_job_file.txt
True	C4 writes execution_config.txt
True	C4 writes result_state.txt
True	C4 writes timing.txt
True	C4 writes changed_paths.txt
True	C4 writes full_transcript.txt
True	C4 writes worker_isolation.txt
True	C4 writes worker_sandbox.txt
True	C4 writes valuations.txt
True	C4 writes staleness_after.txt
True	C4 writes job_diff.txt
True	C4 writes run_defects.txt
True	C4 queue gains exactly one appended entry: SU-084
True	C4 the new entry is not consumed
True	C4 writes the entry's own job file
True	C5 the transcript alone
True	C5 transcript carries 'command:'
True	C5 transcript carries 'real exit code:'
True	C5 transcript carries 'wall time:'
True	C5 transcript carries 'summary line:'
True	C5 transcript carries 'bad node ids (failed + errors):'
True	C5 transcript carries 'leftover processes:'
True	C5 transcript carries 'tree it ran on:'
True	C5 transcript carries 'reflog unchanged during the run:'
True	C5 transcript carries 'cost exit code:'
absent	C6
True	the saved block equals block.md
ALL True
```
Exit 0. Every line `True` (C6 correctly `absent`, since C6 had not committed yet when this gate
ran); last line `ALL True`.

**Gate 2.** The thirteen files under `.agent/selfuse_f158/`, each confirmed non-empty with a Python
byte-size read:
```
SU-084.md 898 bytes
entry_and_job_file.txt 287 bytes
execution_config.txt 1367 bytes
result_state.txt 866 bytes
timing.txt 105 bytes
changed_paths.txt 37 bytes
full_transcript.txt 1574 bytes
worker_isolation.txt 861 bytes
worker_sandbox.txt 1431 bytes
valuations.txt 5 bytes
staleness_after.txt 200 bytes
job_diff.txt 5292 bytes
run_defects.txt 5 bytes
```
All thirteen non-empty.

**Gate 3.** The suite of C5, as the committed transcript records it: real exit code 0, summary line
`24235 passed, 11 skipped, 1 warning in 364.35s (0:06:04)`, bad node ids (failed + errors) `NONE`.

**Gate 4.** `python3 -m apps.cli.main integrity check --json`, run once from the primary checkout:
```
{"check_count": 6, "checks": [{"message": "handlers=204", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
Exit 0, `fail_count` 0, all six checks `pass`. Then
`python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`:
```
['R-1246', 'R-1281', 'R-1351', 'R-1353', 'R-1426', 'R-1428', 'R-1448', 'R-1450', 'R-1464', 'R-1467', 'R-1471']
```
Exit 0, the eleven ids named by the block, in that order.

## Authored-text proofs

C1's byte copy and its disk-to-disk proof read `True`/`EQUAL` for all four targets immediately after
copying, before staging. The mandated proof, `.agent/authored/f158-r7.md` against `block.md`:
byte-identical, 165 lines, sha256 `5939c86b3d695e486c80b09330ed8e121714b2ee37f549353c9ed1bfb0aa12bc`
for both files — the exact digest `digests.txt` stated for `block.md`. Gate 1's independent
`verify.py` run re-confirmed every `C1 ... equals its c1- file`, `C2 ... equals the prepared copy`
and `C3 ... equals the prepared copy` line `True`. The reviewer-authored self-use script,
`.agent/authored/f158-r7-selfuse.py`, was copied once in C1 and run unmodified in C4 (invoked by
path through `launch.py`'s own command table); no edit was made to it between the copy and the run.
`None applied` beyond these — C2 and C3's files are prepared docs byte copies proved the same way,
not reviewer-authored findings or verdict prose under the fidelity protocol.

## Self-use run

- Entry id: `SU-084` — "Write the first tests for packages/orchestration/do_study.py" (generated,
  self-use-generator tier 5, untested module `packages/orchestration/do_study.py`; the queue held no
  pending item before this round's repair, so the generator supplied this one).
- Job id: `e796fd1de2eb4516`.
- Builder: provider `claude-cli`, model `claude-sonnet-4-6`, effort `medium` (source `cli`).
- Reviewer: provider `claude-cli`, model `claude-sonnet-4-6`, effort `medium` (source `cli`).
- Job state: `completed`; stop reason: (empty — the job ran to completion, not a stop).
- Task `T001`: status `applied_to_job_workspace`; reviewer verdict `pass`; final_status
  `staged_review_passed`; repair_rounds_used `0`; run_id `6cd9e46050ec4373`. Never applied to the
  project — the change lives only on the job's own branch.
- Wall seconds: `168.3`.
- Paths in `changed_paths.txt`: `tests/orchestration/test_do_study.py`.
- `valuations.txt` VERBATIM:
```
NONE
```
- `job_diff.txt` VERBATIM:
```
$ git diff HEAD...remedy/job-e796fd1de2eb4516  (exit 0)
diff --git a/tests/orchestration/test_do_study.py b/tests/orchestration/test_do_study.py
new file mode 100644
index 000000000..e959c8278
--- /dev/null
+++ b/tests/orchestration/test_do_study.py
@@ -0,0 +1,138 @@
+"""Tests for packages/orchestration/do_study.py — repo_has_committed_file and do_step_study."""
+from __future__ import annotations
+
+from unittest.mock import MagicMock, patch
+
+import packages.orchestration.do_study  # noqa: F401 — ensures the module is importable
+from packages.orchestration.do_context import (
+    DO_STEP_DONE,
+    DO_STEP_SKIPPED,
+    DO_STEP_STOPPED,
+    DoContext,
+)
+from packages.orchestration.do_study import do_step_study, repo_has_committed_file
+
+
+# ---------------------------------------------------------------------------
+# repo_has_committed_file
+# ---------------------------------------------------------------------------
+
+
+def test_repo_has_committed_file_returns_true_when_git_lists_files():
+    result = MagicMock()
+    result.returncode = 0
+    result.stdout = "README.md\nsrc/main.py\n"
+    with patch("subprocess.run", return_value=result) as mock_run:
+        assert repo_has_committed_file("/fake/repo") is True
+    mock_run.assert_called_once_with(
+        ["git", "ls-tree", "-r", "--name-only", "HEAD"],
+        cwd="/fake/repo",
+        capture_output=True,
+        text=True,
+        timeout=30,
+    )
+
+
+def test_repo_has_committed_file_returns_false_when_git_fails():
+    result = MagicMock()
+    result.returncode = 128
+    result.stdout = ""
+    with patch("subprocess.run", return_value=result):
+        assert repo_has_committed_file("/empty/repo") is False
+
+
+def test_repo_has_committed_file_returns_false_when_stdout_is_blank():
+    result = MagicMock()
+    result.returncode = 0
+    result.stdout = "   \n"
+    with patch("subprocess.run", return_value=result):
+        assert repo_has_committed_file("/empty/repo") is False
+
+
+# ---------------------------------------------------------------------------
+# do_step_study
+# ---------------------------------------------------------------------------
+
+
+def _make_ctx(**kwargs) -> DoContext:
+    project = MagicMock()
+    project.metadata = {}
+    project.id = "proj-id-1"
+    project.slug = "test-project"
+    ctx = DoContext(order="Add a README.", repo_root="/repo", project=project)
+    for k, v in kwargs.items():
+        setattr(ctx, k, v)
+    return ctx
+
+
+def _no_op_lane(hold: bool = False) -> MagicMock:
+    lane = MagicMock()
+    lane.hold = hold
+    lane.bounded = True
+    lane.reason = "test lane"
+    return lane
+
+
+def test_do_step_study_stops_when_lane_is_on_hold():
+    ctx = _make_ctx()
+    with patch("packages.orchestration.do_study.settle_do_lane", return_value=_no_op_lane(hold=True)):
+        status, detail = do_step_study(ctx)
+    assert status == DO_STEP_STOPPED
+    assert "nothing was planned or run" in detail
+
+
+def test_do_step_study_skips_when_already_studied_and_not_stale():
+    ctx = _make_ctx()
+    ctx.project.metadata = {"studied_at": "2026-01-01T00:00:00Z", "studied_head": "abc123"}
+    import packages.orchestration.study as study_mod
+    with (
+        patch("packages.orchestration.do_study.settle_do_lane", return_value=_no_op_lane()),
+        patch("packages.orchestration.do_study.repo_has_committed_file", return_value=True),
+        patch.object(study_mod, "study_stale_reason", return_value=""),
+    ):
+        status, detail = do_step_study(ctx)
+    assert status == DO_STEP_SKIPPED
+    assert "already studied" in detail
+
+
+def test_do_step_study_skips_when_repo_has_no_committed_file():
+    ctx = _make_ctx()
+    ctx.project.metadata = {}
+    with (
+        patch("packages.orchestration.do_study.settle_do_lane", return_value=_no_op_lane()),
+        patch("packages.orchestration.do_study.repo_has_committed_file", return_value=False),
+    ):
+        status, detail = do_step_study(ctx)
+    assert status == DO_STEP_SKIPPED
+    assert "no commit" in detail or "nothing to study" in detail
+
+
+def test_do_step_study_returns_done_after_a_successful_study():
+    ctx = _make_ctx()
+    ctx.project.metadata = {}
+    ctx.no_llm = True
+
+    study_result = MagicMock()
+    study_result.cards_written = ["card1", "card2"]
+    study_result.partial = False
+
+    updated_project = MagicMock()
+    updated_project.metadata = {}
+    updated_project.id = "proj-id-1"
+    updated_project.slug = "test-project"
+
+    with (
+        patch("packages.orchestration.do_study.settle_do_lane", return_value=_no_op_lane()),
+        patch("packages.orchestration.do_study.repo_has_committed_file", return_value=True),
+    ):
+        import packages.orchestration.study as study_mod
+        with (
+            patch.object(study_mod, "study_stale_reason", return_value=""),
+            patch.object(study_mod, "run_study", return_value=study_result),
+            patch.object(study_mod, "record_study_pass", return_value=updated_project),
+            patch.object(study_mod, "study_call_fn", return_value=None),
+        ):
+            status, detail = do_step_study(ctx)
+
+    assert status == DO_STEP_DONE
+    assert "2" in detail or "memory card" in detail
+```
- `run_defects.txt` VERBATIM:
```
NONE
```
No finding is registered by me for this run; the block reserves that for the next round's reviewer.

## Closure suite

`.agent/authored/f158-closure-suite.txt`, whole and verbatim:
```
command: python3 -m pytest -n auto -q
real exit code: 0
wall time: 365.2s (the launcher's reading); pytest's own reported wall time: 364.35s (0:06:04)
summary line: 24235 passed, 11 skipped, 1 warning in 364.35s (0:06:04)
bad node ids (failed + errors): NONE
leftover processes: NONE
tree it ran on: b16e6f296 (F158 R7 C4: the closure's self-use item run to its approval gate, never applied)
tree note: C1 to C4 changed only .agent/ files, one sentence of a guide, the checklist page and the self-use queue
reflog before: b16e6f296 HEAD@{2026-10-24 18:33:45 +0200}: commit: F158 R7 C4: the closure's self-use item run to its approval gate, never applied
reflog after: b16e6f296 HEAD@{2026-10-24 18:33:45 +0200}: commit: F158 R7 C4: the closure's self-use item run to its approval gate, never applied
reflog unchanged during the run: yes
cost command: python3 scripts/closure_suite_cost.py --feature F158 --record ~/.remedy-loop/test_load.jsonl
cost exit code: 0
Test load: 1421.53 CPU seconds, 364.38 wall seconds, 24246 tests collected, exit status 0, recorded 2026-10-24T16:39:56Z
This closure's suite used 1421.53 CPU seconds, 2.2 percent less than F162's 1453.59, within the 10 percent limit.
The limit is the larger of 10 percent and the largest spread between full-suite runs of the record that collected the same tests, 0 percent.
The test modules whose CPU time rose most since F162's closure run:
  +4.85 s  tests/cli/test_stats_valuation_cmd.py (0.00 -> 4.85)
  +3.12 s  tests/orchestration/test_job_worktree_handoff.py (7.76 -> 10.88)
  +2.31 s  tests/orchestration/test_run_manifest_integrity.py (5.73 -> 8.04)
  +2.18 s  tests/orchestration/test_job_stop_integration.py (3.35 -> 5.53)
  +2.12 s  tests/orchestration/test_run_manifest.py (5.92 -> 8.04)
  +2.09 s  tests/orchestration/test_job_task_runner.py (19.72 -> 21.81)
  +2.03 s  tests/orchestration/test_repo_mission.py (3.07 -> 5.10)
  +1.99 s  tests/orchestration/test_cost_currency.py (0.00 -> 1.99)
  +1.98 s  tests/cli/test_worker_pricing_cmd.py (0.00 -> 1.98)
  +1.90 s  tests/cli/test_test_run_runtime.py (8.41 -> 10.31)
```

## Deviations & assumptions

None. Every commit matched the block's ordered sequence and paths exactly; every numstat matched
the block's required numbers (`2\t2` for C2, `10\t0` for C3); the self-use run reached its approval
gate on the first and only attempt and was never applied; the full suite and the cost script each
ran exactly once and both exited 0; no file outside the paths named per commit was touched; no
`REMEDY_TEST_MAX_WORKERS` or extra `-n`; no second test command; no worktree of my own (the self-use
script's internal worktree add/remove, documented above, is the reviewer-authored script's own
action); no agent/fork/helper of any kind started; no `gh pr create/merge`, `git checkout`/`git
switch`, branch creation/move/deletion or force-push; no `--no-verify`; no `claude`/`codex` binary
invoked directly by me.

## For the operator, in plain sentences

Before this feature closes, Remedy ran one real piece of paid work on itself: it was asked to write
the first tests for a module nothing in the project's test collection covered yet, and that work
finished successfully, reviewed and approved, but it was deliberately not merged into the project.
The run's model calls were not given a recorded value in the new cost record, because no project
ledger on this machine carries a row for this particular job. Then Remedy ran its whole test
collection once on the code that will ship: every test passed, none failed, alongside a small,
unchanged number of tests that are skipped on purpose. That whole run took a little over six
minutes. The cost reading said this feature's computer time came in slightly lower than the
previous feature's, comfortably inside the margin allowed.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | four files byte-equal to prepared copies; round 6's PASS verdict and R-1471 booked, plan advanced |
| C2 | done | one file byte-equal; the do guide's `cost.cost_usd` sentence repaired, numstat `2 2` |
| C3 | done | one file byte-equal; the consolidation paragraph appended, list stays at 34, numstat `10 0` |
| C4 | done | the self-use item `SU-084` generated and run to its approval gate, never applied; thirteen files written |
| C5 | done | the one full suite (24235 passed, 0 failed) and the cost script (exit 0, within limit) transcribed |
| C6 | done | this handoff, committed alone per the self-reference exception |
| Gate 1 | done | every line `True`, last line `ALL True` (C6 correctly `absent`) |
| Gate 2 | done | all thirteen `.agent/selfuse_f158/` files confirmed non-empty |
| Gate 3 | done | exit 0, `24235 passed, 11 skipped, 1 warning in 364.35s (0:06:04)`, bad node ids `NONE` |
| Gate 4 | done | exit 0, `fail_count` 0, all six checks pass; eleven open ids match the block exactly |
| Push | pending | runs immediately after this commit; outcome reported in the reply |

## Next

1. Phase 1 rule 1: check `.agent/STOP` before any new work.
2. Phase 1 rule 2 — the Open PR Gate: this round opens no pull request, so the next session checks
   for open pull requests before starting anything new.
3. The reviewer reviews round 7, books its verdict and R-1471, and registers every self-use run
   defect in the next round's first commit.
4. The evidence bundle and the review package (the suite was green).
5. The closing round: the Built State, the rotation, the STATUS line, the README and the pull
   request.

Operator questions open: 3.
Open findings: 11 (the eleven ids gate 4 printed).
