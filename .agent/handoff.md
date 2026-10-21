# Handback — F311 round 5

## Session

SESSION 1 of feature F311 · round 5 · rounds so far 5

Context self-assessment: this session verified every prepared file's digest before using it,
executed C1 to C6 exactly as the block ordered including the real self-use provider call and
the one full suite, and all four gates passed on their first run, with no stop condition met.

Fortschritt: ~90 % (T001 to T004 landed; the consolidation pass, the self-use run and the one
full suite done · the evidence, the package and the closing round remain) — Schätzung

## Range

Review of `d466e4395`..HEAD (C1 to C6 below, then this commit, C7, which also carries this
handback).

## Commits

### 4b36e0372 F311 R5 C1: book round 4, register R-1389, the plan
304 insertions, 10 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f311-r5.md` | +165 (new file) | byte copy of `block.md` |
| `.agent/authored/f311-r5-selfuse.py` | +127 (new file) | byte copy of `selfuse.py` |
| `.agent/plan.md` | +8/-10 | byte copy of `dry-plan.md` |
| `.agent/live_review.md` | +4 | byte copy appending `src-ledger.md` (round 4's PASS verdict, R-1389) |

### 7dad7366f F311 R5 C2: R-1389, the observability list names registered routes, tested
9 insertions.

| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_execution_options.py` | +9 | one test: every entry of `EXECUTION_OBSERVABILITY_ROUTES` is a GET route of `PUBLIC_API_ROUTES`, and both new routes are in the list |

### d2d6d21e3 F311 R5 C3: F311's Built State
43 insertions.

| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/features/T12_F311.md` | +43 | `src-built-state.md`'s bytes appended at the file's end |

### 204e1d724 F311 R5 C4: the checklist's consolidation pass for F311
13 insertions.

| Path | +/- | Reason |
|---|---|---|
| `docs/agents/planner_reviewer_prompt.md` | +13 | `src-consolidation.md`'s bytes inserted directly before "The next consolidation measures against 34."; `git show --numstat` reads `13	0` |

### 8e0b5c5da F311 R5 C5: the closure's self-use item run to its approval gate, never applied
134 insertions.

| Path | +/- | Reason |
|---|---|---|
| `scripts/self_use_queue.json` | +8 | the generator's one appended entry, `SU-067`, `consumed_by` empty |
| `.agent/selfuse_f311/` | +126 across 10 new files | the run's record: entry/job file, execution config, result state, timing, changed paths, full transcript, job diff, run defects, staleness after |

### 7c5aa6768 F311 R5 C6: the closure's one full suite and its CPU cost
28 insertions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f311-closure-suite.txt` | +28 (new file) | the one full-suite transcript plus the cost script's lines |

## External actions

`git branch --show-current` read `feature/f311-insight` before every commit. No `gh` command,
no worktree add/remove, no pull request (forbidden this round; none is open for this branch).
`python3 .remedy-wt/f311-r5/prep/launch.py selfuse .remedy-wt/f311-r5-worker` then
`python3 .remedy-wt/f311-r5/prep/wait.py selfuse .remedy-wt/f311-r5-worker 50` — ended on the
first wait, `exit 0 wall 68.0`. `python3 .remedy-wt/f311-r5/prep/launch.py suite
.remedy-wt/f311-r5-worker` then `python3 .remedy-wt/f311-r5/prep/wait.py suite
.remedy-wt/f311-r5-worker 50` — ended on the first wait, `exit 0 wall 353.9`. The push is
ordered to run after this commit, so its outcome is reported in the final reply only.

## Verification

Gates run once each, after C6 and before this commit.

1. `git status --porcelain` → empty. Then `python3 .remedy-wt/f311-r5/prep/verify.py .`: every
   line `True` except `absent	C7` (not yet made), last line `ALL True`.
2. The ten files under `.agent/selfuse_f311/`, each non-empty:
   `SU-067.md` 1034 bytes, `entry_and_job_file.txt` 381 bytes, `execution_config.txt` 1367 bytes,
   `result_state.txt` 866 bytes, `timing.txt` 104 bytes, `changed_paths.txt` 61 bytes,
   `full_transcript.txt` 1579 bytes, `staleness_after.txt` 200 bytes, `job_diff.txt` 1092 bytes,
   `run_defects.txt` 5 bytes.
3. The suite of C6: exit code 0; summary line `22092 passed, 11 skipped, 1 warning in 353.08s
   (0:05:53)`; bad node ids: `NONE`.
4. `python3 -m apps.cli.main integrity check --json` → exit 1, `fail_count` 1, the one failing
   check `high_blockers_open` naming exactly the twelve ids of DECISION F310 D7
   (`R-1335, R-1336, R-1337, R-1338, R-1345, R-1346, R-1348, R-1349, R-1359, R-1360, R-1361,
   R-1362`) and no other; and `python3 -c "import scripts.rotate_live_review as r;
   print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"` → `88` (the base's 87,
   plus R-1389).

## Authored-text proofs

All seven prepared files (`block.md`, `verify.py`, `digests.txt`, `selfuse.py`, `launch.py`,
`wait.py`, `dry-plan.md`, `src-ledger.md`, `src-built-state.md`, `src-consolidation.md`) matched
their stated/listed sha256 digests before use. C1's three byte copies and the ledger append were
each proved equal by a Python reader before commit, and `verify.py`'s own checks confirm the
same equality again: "C1 the block copy", "C1 the self-use script copy", "C1 the plan", "C1
`.agent/live_review.md` is the base plus `src-ledger.md`" all read `True`. C3's append
(`docs/roadmap/features/T12_F311.md` = parent + `src-built-state.md`) and C4's insertion
(`docs/agents/planner_reviewer_prompt.md` = parent with `src-consolidation.md` inserted before
the anchor line) are likewise confirmed `True` by `verify.py`.

## Self-use run

Entry `SU-067`, "Narrow the excused handler at apps/cli/commands/status_cmd.py:115" (generated,
tier 4: an excused handler the BLE001 ratchet counts). Job id `5020265346c049d1`. Builder and
reviewer: `claude-cli`, model `claude-sonnet-4-6`, effort `medium` (the `self_use` role's
configured provider, from `execution_config.txt`). Job state `completed`, no stop reason, no
error. Task T001: status `applied_to_job_workspace`, reviewer verdict `pass`, final status
`staged_review_passed`, 0 repair rounds used (from `result_state.txt`). Wall seconds: 63.8 (from
`timing.txt`). Changed paths (from `changed_paths.txt`): `apps/cli/commands/status_cmd.py`,
`tests/test_ble001_ratchet.py`.

Job diff (`job_diff.txt`), verbatim:
```
$ git diff HEAD...remedy/job-5020265346c049d1  (exit 0)
diff --git a/apps/cli/commands/status_cmd.py b/apps/cli/commands/status_cmd.py
index 9d824b069..e904acb7b 100644
--- a/apps/cli/commands/status_cmd.py
+++ b/apps/cli/commands/status_cmd.py
@@ -112,7 +112,7 @@ def _cmd_status(
         else:
             runtime_status = "unknown"
             runtime_warning = f"runtime state unreadable: {load.error or load.kind}"
-    except Exception:  # noqa: BLE001 — runtime-state read failure leaves status as unknown
+    except ImportError:
         pass
 
     first_active_short = None
diff --git a/tests/test_ble001_ratchet.py b/tests/test_ble001_ratchet.py
index 1fa195707..e1cce97e9 100644
--- a/tests/test_ble001_ratchet.py
+++ b/tests/test_ble001_ratchet.py
@@ -18,7 +18,7 @@ REASONED = re.compile(r"^ — \S")
 
 #: The number of excused blind handlers when BLE001 was turned on. Only ever falls: the
 #: commit that removes a mark lowers this number in the same commit, and it is never raised.
-MAX_EXCUSED = 282
+MAX_EXCUSED = 281
```

`run_defects.txt`, verbatim: `NONE`

## Closure suite

`.agent/authored/f311-closure-suite.txt`, whole and verbatim:
```
command: python3 -m pytest -n auto -q
real exit code: 0
wall time: 353.9s (the launcher's reading); pytest's own reported wall time: 353.08s (0:05:53)
summary line: 22092 passed, 11 skipped, 1 warning in 353.08s (0:05:53)
bad node ids (failed + errors):
  - NONE
leftover processes: NONE
tree it ran on: 8e0b5c5da (F311 R5 C5: the closure's self-use item run to its approval gate, never applied)
tree note: C1 to C5 changed only .agent/ files, one test file, the feature file, the checklist page and the self-use queue
reflog before: 8e0b5c5da HEAD@{2026-10-21 03:42:54 +0200}: commit: F311 R5 C5: the closure's self-use item run to its approval gate, never applied
reflog after: 8e0b5c5da HEAD@{2026-10-21 03:42:54 +0200}: commit: F311 R5 C5: the closure's self-use item run to its approval gate, never applied
reflog unchanged during the run: yes
cost command: python3 scripts/closure_suite_cost.py --feature F311 --record ~/.remedy-loop/test_load.jsonl
cost exit code: 0
Test load: 1310.31 CPU seconds, 353.09 wall seconds, 22103 tests collected, exit status 0, recorded 2026-10-21T01:48:53Z
This closure's suite used 1310.31 CPU seconds, 1.2 percent more than F312's 1294.96, within the 10 percent limit.
The limit is the larger of 10 percent and the largest spread between full-suite runs of the record that collected the same tests, 0 percent.
The test modules whose CPU time rose most since F312's closure run:
  +4.55 s  tests/runtimes/test_supervisor_portability.py (45.04 -> 49.59)
  +3.90 s  tests/ui_server/test_public_api.py (11.96 -> 15.86)
  +2.20 s  tests/orchestration/test_job_worktree_integrity.py (10.35 -> 12.55)
  +1.91 s  tests/cli/test_mission_cmd.py (43.99 -> 45.90)
  +1.88 s  tests/orchestration/test_self_use_runner.py (3.76 -> 5.64)
  +1.87 s  tests/orchestration/test_run_manifest_call_task_binding.py (3.48 -> 5.35)
  +1.81 s  tests/orchestration/test_review_manual_completion_shapes.py (1.79 -> 3.60)
  +1.73 s  tests/cli/test_client_insight_cmd.py (0.00 -> 1.73)
  +1.40 s  tests/orchestration/test_legacy_manifest_presence.py (3.57 -> 4.97)
  +1.37 s  tests/cli/test_do_order_file.py (8.82 -> 10.19)
```

## Deviations & assumptions

None. C1 to C6 landed exactly as the block ordered, with no deviation from the commit sequence,
the paths per commit, or the gate order. The self-use run and the full suite each ran exactly
once through `launch.py`/`wait.py`, each ending on the first `wait.py` call. The reviewer's
`staleness_after.txt` reading on the job branch (docs/README.md's Guides section not yet linking
`docs/guides/http-clients.md`) is reported above verbatim and not registered as a finding by this
worker, per the block's own instruction.

## Next

In order: Phase 1 rule 1 (`.agent/STOP`) — absent, no action needed; rule 2, the Open PR Gate —
no pull request is open for this branch yet; the reviewer reviews round 5, books its verdict,
resolves R-1389 and registers every self-use run defect in the next round's first commit; then
the evidence bundle and the review package (the suite is green); then the closing round: the
STATUS line, the README and the pull request. Operator questions open: 1. Open findings: 88
(gate 4, rule `open_finding_ids`, this commit).

## For the operator, in plain sentences

Before this feature closes, Remedy ran one real piece of work on itself with a paid model: it
was asked to narrow an overly broad exception handler so it only catches the specific error it
needs to, and it finished that change and passed its own review, without that change being
applied anywhere yet. Then Remedy ran its whole test collection once on the code that will ship:
22,092 tests passed, 11 were intentionally skipped, and none failed; that run took about five
minutes and fifty-three seconds. The computer time that run used was about one percent more than
the previous feature's closure run, well inside the normal range.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | `4b36e0372` |
| C2 | done | `7dad7366f` |
| C3 | done | `d2d6d21e3` |
| C4 | done | `204e1d724` |
| C5 | done | `8e0b5c5da` |
| C6 | done | `7c5aa6768` |
| C7 | done | this commit |
| Gate 1 | done | every line `True`, last `ALL True` |
| Gate 2 | done | all ten files non-empty, sizes listed above |
| Gate 3 | done | exit 0, `22092 passed, 11 skipped, 1 warning`, bad node ids `NONE` |
| Gate 4 | done | `fail_count` 1 on the standing twelve; open findings `88` |
| R-1389 | done | repaired with a test in C2 (`test_the_observability_list_names_registered_get_routes`); the ledger resolution itself is the next round's first commit, per the block's own instruction |
| Push | pending | reported in the final reply only |
