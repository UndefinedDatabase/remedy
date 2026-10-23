# Handback — F151 round 7

## Session

SESSION 1 of feature F151 · round 7 · rounds so far 7.

Context self-assessment: both prepared top-level digests (`block.md`, `digests.txt`) and all nine
files `digests.txt` listed under `.remedy-wt/f151-r7/prep/` were checked against `digests.txt` with
a Python sha256 reader before any file was used, the block was read in full before any commit, and
the self-use run and the one full suite were each run exactly once through `launch.py`/`wait.py`,
read verbatim and committed without edit, investigation or re-run.

Fortschritt: ~90 % (T001 to T003 and the docs landed; the consolidation pass, the self-use run and
the one full suite done · the evidence, the package and the closing round remain) — Schätzung

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | four prepared paths copied and proved byte-identical; `block.md` confirmed 155 lines, sha256 `073c38a0...e91`; staged and committed alone |
| C2 | done | one prepared docs path copied and proved byte-identical; `git show --numstat` read `10	0`; staged and committed alone |
| C3 | done | `launch.py`/`wait.py selfuse` exit 0, wall 64.7s; entry `SU-078` generated, run to the approval gate through `claude-cli`, task `T001` `applied_to_job_workspace`/verdict `pass`, never applied; queue gained exactly one entry with an empty `consumed_by`; ten files under `.agent/selfuse_f151/` written with `~`-substituted paths; committed alone |
| C4 | done — suite RED | `launch.py`/`wait.py suite` exit 1, wall 402.8s; one bad node id (`tests/cli/test_advertised_commands.py::test_every_operator_facing_advertised_command_exists_in_the_catalog`); reflog unchanged during the run; cost script exit 0; transcript committed exactly as read, no re-run or fix attempted per the block's step 6 |
| C5 | done | this handback |
| Gate 1 | done — PASS | `git status --porcelain` empty; `verify.py` every line `True`, `C5` read `absent` at gate time, last line `ALL True` |
| Gate 2 | done — PASS | all ten files under `.agent/selfuse_f151/` non-empty (sizes below) |
| Gate 3 | done — reports RED | suite exit 1, summary and bad node id as the transcript records them |
| Gate 4 | done — PASS | `integrity check --json` → `fail_count` 0, six checks all `pass`; `open_finding_ids` → the eleven ids exactly |

## Range

Review of `b095ddcc4`..`HEAD` (`HEAD` is this handback's own commit).

## Commits

### `0baaeeb0d` F151 R7 C1: book round 6, resolve R-1439 and R-1440, the plan, the block and the self-use script

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f151-r7.md` | +155/-0 (new) | byte copy of this round's own block, proved equal to it |
| `.agent/authored/f151-r7-selfuse.py` | +127/-0 (new) | byte copy of the reviewer-authored self-use script for C3 |
| `.agent/live_review.md` | +6/-0 | round 6's VERDICT PASS gate entry booked, with the `Done:` lines for R-1439 and R-1440 |
| `.agent/plan.md` | +6/-6 | rewritten: current step round 7's integration gate, next steps the evidence and closing rounds, risk naming a red suite or self-use defect |

### `a2bb7d566` F151 R7 C2: the checklist's consolidation pass for F151

| Path | +/- | Reason |
|---|---|---|
| `docs/agents/planner_reviewer_prompt.md` | +10/-0 | F151's consolidation paragraph appended; nothing joined, no two items merged, the list stays at 34 items |

### `931111795` F151 R7 C3: the closure's self-use item run to its approval gate, never applied

| Path | +/- | Reason |
|---|---|---|
| `scripts/self_use_queue.json` | +8/-0 | the generator's one appended entry, `SU-078`, `consumed_by` empty |
| `.agent/selfuse_f151/*` (10 files) | +126/-0 total | the run's record: `SU-078.md` (17), `changed_paths.txt` (2), `entry_and_job_file.txt` (5), `execution_config.txt` (43), `full_transcript.txt` (14), `job_diff.txt` (27), `result_state.txt` (12), `run_defects.txt` (1), `staleness_after.txt` (2), `timing.txt` (3) |

### `2ba072367` F151 R7 C4: the closure's one full suite and its CPU cost

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f151-closure-suite.txt` | +28/-0 (new) | the suite's transcript in the `f133-closure-suite.txt` shape: command, exit code, wall time, summary line, the one bad node id, leftover processes NONE, tree/reflog lines, the cost script's command, exit code and every line it printed |

### This commit (C5) — handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this file, per `docs/agents/handback_template.md` |

## External actions

- `git push origin feature/f151-worker-adapter-contract` — run once, immediately after this commit.
- No pull request was opened (none is open for this branch; the Open PR Gate's precondition held
  `[]` before this round started). No worktree was added or removed by this worker. No merge, no
  rebase, no amend, no stash. The self-use run's own provider calls (C3) are the round's only
  provider calls.

## Verification

Interpreter: the repository's configured Python 3 (`python3`, system install). All four gates were
run once each, after C4 and before C5, per the block.

Gate 1 — `git status --porcelain` → empty (no output). `python3 .remedy-wt/f151-r7/prep/verify.py .`
→ every line `True`: all four commits single-parent and under 500 insertions (294, 10, 134, 28),
each carries an `F151 R7 Cn` subject, on `feature/f151-worker-adapter-contract`; C1's four paths
exact and byte-equal to their `c1-*` snapshots; C2's one path exact and byte-equal to its `c2-*`
snapshot; C3's paths are exactly the queue and `.agent/selfuse_f151/`, the queue gained exactly one
entry (`SU-078`), and every `.agent/` path under C3 holds no machine path; C4 is the transcript
alone and holds no machine path; `C5` read `absent` (not yet committed at gate time); the saved
block equals `block.md`; last line `ALL True`.

Gate 2 — ten files under `.agent/selfuse_f151/`, each non-empty: `SU-078.md` 1077 bytes,
`entry_and_job_file.txt` 403 bytes, `execution_config.txt` 1367 bytes, `result_state.txt` 865 bytes,
`timing.txt` 104 bytes, `changed_paths.txt` 68 bytes, `full_transcript.txt` 1586 bytes,
`staleness_after.txt` 200 bytes, `job_diff.txt` 1301 bytes, `run_defects.txt` 5 bytes.

Gate 3 — the suite of C4, as the transcript records it: exit code `1`; summary line
`1 failed, 23669 passed, 11 skipped, 1 warning in 401.94s (0:06:41)`; bad node ids (failed + errors):
`tests/cli/test_advertised_commands.py::test_every_operator_facing_advertised_command_exists_in_the_catalog`.

Gate 4 — `python3 -m apps.cli.main integrity check --json` →
`{"check_count": 6, "checks": [{"message": "handlers=197", "name": "handler_import", "status":
"pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"},
{"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"},
{"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message":
"no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status":
"pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status":
"pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}`.
`python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
→ `['R-1246', 'R-1281', 'R-1326', 'R-1351', 'R-1353', 'R-1418', 'R-1421', 'R-1425', 'R-1426',
'R-1427', 'R-1428']` — the eleven ids exactly.

## Self-use run

- Entry id: `SU-078` — "Narrow the excused handler at
  apps/cli/commands/worker_facade_cmd.py:451" (provenance: generated, self-use-generator tier 4,
  excused handler).
- Job id: `40d734944254417e`, title the same as the entry.
- Builder: `claude-cli`, model `claude-sonnet-4-6`, effort `medium` (source `cli` for all three).
  Reviewer: `claude-cli`, model `claude-sonnet-4-6`, effort `medium` (source `cli` for all three).
- Job state: `completed`. Stop reason: (empty). Stop source: (empty).
- Task `T001`: status `applied_to_job_workspace`; reviewer verdict `pass`; final_status
  `staged_review_passed`; repair_rounds_used `0`; run_id `e3e58f74278c4202`.
- Wall seconds: `60.1` (started `2026-10-23T15:04:10.363268+00:00`, finished
  `2026-10-23T15:05:10.424802+00:00`).
- Paths (`changed_paths.txt`): `apps/cli/commands/worker_facade_cmd.py`,
  `tests/test_ble001_ratchet.py`.
- Job diff (`job_diff.txt`), verbatim:

```
$ git diff HEAD...remedy/job-40d734944254417e  (exit 0)
diff --git a/apps/cli/commands/worker_facade_cmd.py b/apps/cli/commands/worker_facade_cmd.py
index c22649d44..a16e70345 100644
--- a/apps/cli/commands/worker_facade_cmd.py
+++ b/apps/cli/commands/worker_facade_cmd.py
@@ -448,7 +448,7 @@ def doctor_core_report() -> DoctorCoreReport:
         _check("disk_floor", floor_met,
                f"{free_bytes} bytes free, floor "
                f"{'not configured' if floor_bytes is None else floor_bytes}")
-    except Exception as exc:  # noqa: BLE001 — a disk-floor read failure is that check's own result
+    except (ImportError, OSError, ValueError) as exc:
         disk["error"] = report_safe_text(exc, limit=120)
         _check("disk_floor", False, report_safe_text(exc, limit=120))
 
diff --git a/tests/test_ble001_ratchet.py b/tests/test_ble001_ratchet.py
index 1fa195707..e1cce97e9 100644
--- a/tests/test_ble001_ratchet.py
+++ b/tests/test_ble001_ratchet.py
@@ -18,7 +18,7 @@ REASONED = re.compile(r"^ — \S")
 
 #: The number of excused blind handlers when BLE001 was turned on. Only ever falls: the
 #: commit that removes a mark lowers this number in the same commit, and it is never raised.
-MAX_EXCUSED = 282
+MAX_EXCUSED = 281
 
 
 def _marks() -> list[tuple[str, int, str]]:
```

- `run_defects.txt`, verbatim: `NONE`

Do not register any finding from this section yourself — the reviewer registers every string
`describe_self_use_run_defects` returns in the next round's first commit; here it returned none.

## Closure suite

`.agent/authored/f151-closure-suite.txt`, whole and verbatim:

```
command: python3 -m pytest -n auto -q
real exit code: 1
wall time: 402.8s (the launcher's reading); pytest's own reported wall time: 401.94s (0:06:41)
summary line: 1 failed, 23669 passed, 11 skipped, 1 warning in 401.94s (0:06:41)
bad node ids (failed + errors):
  - tests/cli/test_advertised_commands.py::test_every_operator_facing_advertised_command_exists_in_the_catalog
leftover processes: NONE
tree it ran on: 931111795 (F151 R7 C3: the closure's self-use item run to its approval gate, never applied)
tree note: C1 to C3 changed only .agent/ files, the checklist page and the self-use queue
reflog before: 931111795 HEAD@{2026-10-23 17:05:32 +0200}: commit: F151 R7 C3: the closure's self-use item run to its approval gate, never applied
reflog after: 931111795 HEAD@{2026-10-23 17:05:32 +0200}: commit: F151 R7 C3: the closure's self-use item run to its approval gate, never applied
reflog unchanged during the run: yes
cost command: python3 scripts/closure_suite_cost.py --feature F151 --record ~/.remedy-loop/test_load.jsonl
cost exit code: 0
Test load: 1423.07 CPU seconds, 401.95 wall seconds, 23681 tests collected, exit status 1, recorded 2026-10-23T15:12:19Z
This closure's suite used 1423.07 CPU seconds, 1.5 percent more than F133's 1401.83, within the 10 percent limit.
The limit is the larger of 10 percent and the largest spread between full-suite runs of the record that collected the same tests, 0 percent.
The test modules whose CPU time rose most since F133's closure run:
  +7.88 s  tests/orchestration/test_subtree_rerun_prepare.py (10.60 -> 18.48)
  +7.63 s  tests/cli/test_do_sequence_cli.py (35.66 -> 43.29)
  +6.14 s  tests/cli/test_do_several_projects.py (9.75 -> 15.89)
  +5.06 s  tests/orchestration/test_token_ledger.py (8.45 -> 13.51)
  +4.50 s  tests/cli/test_status_cmd.py (7.38 -> 11.88)
  +3.64 s  tests/orchestration/test_disk_floor.py (1.04 -> 4.68)
  +3.30 s  tests/orchestration/test_task_deliverables.py (3.82 -> 7.12)
  +3.21 s  tests/orchestration/test_self_use_runner.py (5.02 -> 8.23)
  +3.00 s  tests/orchestration/test_run_manifest_zero_call_expectations.py (2.85 -> 5.85)
  +2.55 s  tests/orchestration/test_run_manifest_integrity.py (5.98 -> 8.53)
```

## Authored-text proofs

C1's two new files and two rewrites, and C2's one path, are reviewer-authored or reviewer-produced
text applied this round. Each was copied from its prepared `c1-*`/`c2-*` file under
`.remedy-wt/f151-r7/prep/` by a dedicated `python3` script under `.remedy-wt/f151-r7-worker/`, which
compared source and destination bytes immediately after each copy; all five pairs read equal.
`block.md` itself (saved as `.agent/authored/f151-r7.md`) was separately confirmed equal to the
prepared `block.md` by its sha256 (given in the prompt, checked before any file was used), again by
line count (155) and sha256 directly against `block.md`, and a third time by `verify.py`'s own check
for that path. `.agent/authored/f151-r7-selfuse.py` (C1) is the reviewer-authored self-use script,
copied and proved the same way, then run unedited in C3. `.agent/authored/f151-closure-suite.txt`
(C4) and `scripts/self_use_queue.json` / `.agent/selfuse_f151/*` (C3) are NOT reviewer-authored text
— they are this worker's and the self-use script's own output from the block's instructions — so no
disk-to-disk comparison applies to them.

## Deviations & assumptions

`python3 scripts/closure_suite_cost.py --feature F151 --record ~/.remedy-loop/test_load.jsonl` was
invoked twice: once directly (its output recorded above and in the transcript), and a second time
wrapped in a small `python3 subprocess.run(...)` call solely to read its exact process exit code,
because the sandbox refused the compound shell shape `cmd; echo $?`. Reading the script
(`scripts/closure_suite_cost.py`) first confirmed it only reads the JSONL record and prints — it
never appends a line itself (`tests/conftest.py` appends the run's own line during the pytest run,
which ran exactly once) — so the two invocations are idempotent reads; both printed byte-identical
output and exit code `0`. The block said "run once"; this is a declared deviation from that letter,
not of substance, since nothing on disk changed between the two reads.

The full suite (C4) came back RED: one failed test,
`tests/cli/test_advertised_commands.py::test_every_operator_facing_advertised_command_exists_in_the_catalog`,
reporting that `docs/system/worker-adapter-contract-v1.md:72` advertises `remedy workers`, an
invocation the operator-facing command catalog does not carry (added by round 6's docs commit,
`b160a2f2d`). Per the block's C4 step 6 and the Constraints section, the transcript was committed
exactly as read, with no re-run, no investigation and no fix attempted; the repair is the next
round's reviewer-authored block.

No other deviation. No mutation red-proof was run (none ordered). No worktree of this worker's own
was added or removed. No two test commands ran at the same time; `REMEDY_TEST_MAX_WORKERS` was never
set; no larger `-n` was passed. `git branch --show-current` was run as a standalone command, never
joined to another, immediately before every commit, and read
`feature/f151-worker-adapter-contract` every time.

## Next

1. Phase 1 rule 1: check whether `.agent/STOP` exists (absent at the time of this handback).
2. Rule 2, the Open PR Gate: no pull request is open for this branch yet.
3. The reviewer reviews round 7, books its verdict and registers every self-use run defect in the
   next round's first commit.
4. A repair round naming every bad node id (the suite came back red).
5. The closing round: the Built State, the rotation, the STATUS line, the README and the pull
   request.

Operator questions open: 0. Open findings: 11, gate 4 printed.

## For the operator, in plain sentences

The paid run was asked to narrow an overly broad exception handler in the worker's own health-check
code to the specific error types it can actually raise, and it finished successfully: the change was
reviewed and approved but left staged on its own branch, never merged into the code that ships. The
whole test collection then ran once, and one test out of roughly twenty-three thousand seven hundred
failed, taking a little under seven minutes. The cost reading said this run's computer time was
about one and a half percent higher than the previous feature's, well inside the allowed margin.
Remedy now has one written contract that every model backend must meet, a test kit that checks a
backend against it, and its current command-line backend wrapped to meet that contract without
changing how jobs run.
