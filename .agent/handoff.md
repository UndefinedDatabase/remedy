# Handback — F306 round 8: book round 7, the consolidation pass, the closure's self-use item, and the one full suite

## Session

SESSION 2 of feature F306 · round 8 · rounds so far 8

Context self-assessment: the round ran its two long detached commands (the self-use job and the
full suite) back to back without needing a repeat `wait.py` poll for either — both finished inside
one 50-minute window — so the whole round fit comfortably in the context budget with room to spare
for the handback.

Fortschritt: ~92 % (T001 to T004 and T006 to T008 landed; the consolidation pass, the self-use run
and the one full suite done · the evidence, the package and the closing round remain) — Schätzung

## Range

Review of `548472ce2`..`cbb8729f7`

## Commits

### f4331c2a3 F306 R8 C1: book round 7, its prose slip and the plan, save the block and the self-use script

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f306-r8.md` | +161/-0 | NEW FILE, byte copy of `block.md` (161 lines, sha256 `2754b12b103290ca16dbe6e6ff03a6c4d58ab80df9d061a427a9d3803ff559ed`) |
| `.agent/authored/f306-r8-selfuse.py` | +122/-0 | NEW FILE, byte copy of `selfuse.py` |
| `.agent/plan.md` | +8/-8 | replaced by `dry-plan.md` |
| `.agent/live_review.md` | +2/-0 | round 7's PASS verdict appended, byte-identical to `append-live_review.txt` |
| `.agent/prose_slips.md` | +1/-0 | round 7's one-line prose slip appended, byte-identical to `append-prose_slips.txt` |

### ac98104df F306 R8 C2: the checklist's consolidation pass for F306

| Path | +/- | Reason |
|---|---|---|
| `docs/agents/planner_reviewer_prompt.md` | +10/-0 | byte copy of `dry-planner_reviewer_prompt.md` — a pure append of F306's consolidation paragraph; the list stays at 34 items |

### cb5f84574 F306 R8 C3: the closure's self-use item run to its approval gate, never applied

| Path | +/- | Reason |
|---|---|---|
| `scripts/self_use_queue.json` | +8/-0 | the generator's one appended entry, `SU-062`, `consumed_by` empty |
| `.agent/selfuse_f306/SU-062.md` | +17/-0 | NEW FILE, the job's own markdown |
| `.agent/selfuse_f306/changed_paths.txt` | +2/-0 | NEW FILE |
| `.agent/selfuse_f306/entry_and_job_file.txt` | +5/-0 | NEW FILE |
| `.agent/selfuse_f306/execution_config.txt` | +43/-0 | NEW FILE |
| `.agent/selfuse_f306/full_transcript.txt` | +14/-0 | NEW FILE |
| `.agent/selfuse_f306/job_diff.txt` | +31/-0 | NEW FILE |
| `.agent/selfuse_f306/result_state.txt` | +12/-0 | NEW FILE |
| `.agent/selfuse_f306/run_defects.txt` | +1/-0 | NEW FILE |
| `.agent/selfuse_f306/staleness_after.txt` | +2/-0 | NEW FILE |
| `.agent/selfuse_f306/timing.txt` | +3/-0 | NEW FILE |

### cbb8729f7 F306 R8 C4: the closure's one full suite and its CPU cost

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f306-closure-suite.txt` | +27/-0 | NEW FILE, the one full-suite transcript (RED — one bad node id) plus the cost script's reading, shaped like `.agent/authored/f297-closure-suite.txt` |

### (this commit) F306 R8 C5: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | full rewrite per `docs/agents/handback_template.md` |

## External actions

- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` is not yet run in this
  round (the block's step 5 "Open PR Gate; no pull request is open for this branch yet" is read
  from the block's own text, not re-checked here); the next round's bootstrap re-checks it.
- `python3 /home/decodeux/Repos/remedy/.remedy-wt/f306-r8/prep/launch.py selfuse ...` then
  `wait.py selfuse ... 50`: one detached run, exit 0, wall 54.0s (launcher's reading) / 50.3s (the
  script's own `timing.txt` reading of the inner job run) — see "Self-use run" below.
- `python3 /home/decodeux/Repos/remedy/.remedy-wt/f306-r8/prep/launch.py suite ...` then
  `wait.py suite ... 50`: one detached run, exit 1, wall 348.3s — see "Closure suite" below.
- Push after C5: `git -C /home/decodeux/Repos/remedy push origin feature/f306-findings-paydown-v8`
  — result in the session's final reply (with retry-on-500 up to three times per the block).
- No worktree added or removed by this session (the self-use runner opened and closed its own job
  worktree internally; nothing was left behind — `git worktree list` after C3 showed no
  `job-d477b678080e4742` entry). No `gh pr merge`, `gh pr edit` or `gh pr create`.

## Verification

Preconditions confirmed before C1: `git rev-parse HEAD` read `548472ce2b95db3cf1b56f4d8809259a8f0520aa`,
equal to `git rev-parse origin/feature/f306-findings-paydown-v8`; `git status --porcelain` was
empty; `.agent/STOP` was absent.

Every prepared-file digest matched before use (all nine files in the prep directory, each read in
full first): `append-live_review.txt`, `append-prose_slips.txt`, `block.md` (161 lines,
`2754b12b103290ca16dbe6e6ff03a6c4d58ab80df9d061a427a9d3803ff559ed`), `dry-plan.md`,
`dry-planner_reviewer_prompt.md`, `launch.py`, `selfuse.py`, `verify.py`, `wait.py`.

`git branch --show-current` read `feature/f306-findings-paydown-v8` immediately before every one
of C1 through C4's commits, as ordered.

C1: `c1_copy.py` wrote the five files, then `c1_proof.py` (reading only) printed `True` for every
one of the five byte-equality checks plus `ALL True`, and the block.md copy's own line count (161)
and sha256 (`2754b12b103290ca16dbe6e6ff03a6c4d58ab80df9d061a427a9d3803ff559ed`) matched the digest
given in the task. `git status --porcelain` before the commit showed exactly the five named paths
(three modified, two new) and nothing else.

C2: `c2_copy.py` wrote the one file, `c2_proof.py` printed `equal True` against
`dry-planner_reviewer_prompt.md`. Before committing, `diff` of the live file against the dry file
showed one pure 10-line insertion at line 663 with zero deletions — the pattern of every prior
consolidation paragraph in that file. `git show --numstat` of the commit read `10	0
docs/agents/planner_reviewer_prompt.md`, matching the block's requirement exactly.

Gate 1 (run once, after C2, to confirm C1/C2 before continuing to C3/C4): `git status --porcelain`
empty; `verify.py` →
```
C1 and C2 found in order True ['F306 R8 C1: book round 7, its prose slip and the plan, save the block and the self-use script', "F306 R8 C2: the checklist's consolidation pass for F306"]
C1 parent is the base True
equal f4331c2a3 .agent/authored/f306-r8.md True
equal f4331c2a3 .agent/authored/f306-r8-selfuse.py True
equal f4331c2a3 .agent/plan.md True
equal f4331c2a3 .agent/live_review.md True
equal f4331c2a3 .agent/prose_slips.md True
f4331c2a3 names exactly its paths True []
equal ac98104df docs/agents/planner_reviewer_prompt.md True
ac98104df names exactly its paths True []
ALL True
```

C3: `launch.py selfuse` started the detached run (pid 849222); `wait.py selfuse ... 50` returned
after one poll window with `exit 0 wall 54.0`. The script's own report (see "Self-use run" below)
matches. After the run, `git status --porcelain` showed exactly `scripts/self_use_queue.json`
modified and `.agent/selfuse_f306/` new, nothing else; `git diff scripts/self_use_queue.json`
showed exactly one appended entry, id `SU-062` (the id the script printed), `consumed_by` empty.
All ten files under `.agent/selfuse_f306/` existed and were non-empty before the commit (sizes
confirmed again at Gate 2 below).

C4 step 1: `git -C /home/decodeux/Repos/remedy reflog -n 1 --date=iso` read
`cb5f84574 HEAD@{2026-10-13 22:59:33 +0200}: commit: F306 R8 C3: the closure's self-use item run to its approval gate, never applied`.
C4 step 2: `launch.py suite` started the detached run (pid 850542); `wait.py suite ... 50` returned
after one poll window with `exit 1 wall 348.3` — RED, one failed node:
`tests/orchestration/test_model_routing.py::TestTheCallSiteInventoryIsChecked::test_the_swept_multiset_equals_the_declared_inventory`,
summary `1 failed, 22975 passed, 22 skipped, 1 warning in 347.58s (0:05:47)`. No "process(es)
behind" line and no other FAILED/ERROR line in the log. C4 step 3: the reflog was read again the
same way and read byte-identical to step 1's line — the branch did not move during the run, so no
stop was triggered by that clause. C4 step 4: `python3 scripts/closure_suite_cost.py --feature
F306 --record /home/decodeux/.remedy-loop/test_load.jsonl` → exit 0, four lines printed (quoted
verbatim in the transcript below) — the suite's CPU cost is within the limit, so this is a reading,
not a finding. C4 step 5: `.agent/authored/f306-closure-suite.txt` written in the
`f297-closure-suite.txt` shape, every field read from the run above. C4 step 6: because the suite
was RED, the transcript was committed exactly as read, with no re-run, investigation or fix — the
repair is the next round's reviewer-authored block, exactly as the block orders.

Gate 1 (run again, after C4, before C5): `git status --porcelain` empty; `verify.py` → the same
`ALL True` output shown above (C1/C2 are unaffected by C3/C4).

Gate 2: all ten files under `.agent/selfuse_f306/`, each non-empty —
`SU-062.md` 1028 bytes, `changed_paths.txt` 61 bytes, `entry_and_job_file.txt` 390 bytes,
`execution_config.txt` 1367 bytes, `full_transcript.txt` 1578 bytes, `job_diff.txt` 1424 bytes,
`result_state.txt` 800 bytes, `run_defects.txt` 5 bytes, `staleness_after.txt` 59 bytes,
`timing.txt` 104 bytes.

Gate 3: read from the committed transcript — exit code `1`; summary line
`1 failed, 22975 passed, 22 skipped, 1 warning in 347.58s (0:05:47)`; bad node ids: exactly one,
`tests/orchestration/test_model_routing.py::TestTheCallSiteInventoryIsChecked::test_the_swept_multiset_equals_the_declared_inventory`.

Gate 4: `python3 -m apps.cli.main integrity check --json` → exit 0:
```
{"check_count": 6, "checks": [{"message": "handlers=188", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
and `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
→ `['R-1235', 'R-1246', 'R-1252']`.

Gate 5: run after the push; its command, exit code and comparison are in the session's final
reply, not in this file (the push had not yet happened when this file was written, per the
write-once rule).

## Authored-text proofs

- `.agent/authored/f306-r8.md` against `block.md`: byte-equal, 161 lines, sha256
  `2754b12b103290ca16dbe6e6ff03a6c4d58ab80df9d061a427a9d3803ff559ed` (Gate 1's
  "equal f4331c2a3 .agent/authored/f306-r8.md True").
- `.agent/authored/f306-r8-selfuse.py` against `selfuse.py`: byte-equal (Gate 1).
- `.agent/plan.md` against `dry-plan.md`: byte-equal (Gate 1).
- `.agent/live_review.md` against the base plus `append-live_review.txt`: byte-equal (Gate 1).
- `.agent/prose_slips.md` against the base plus `append-prose_slips.txt`: byte-equal (Gate 1).
- `docs/agents/planner_reviewer_prompt.md` against `dry-planner_reviewer_prompt.md`: byte-equal
  (Gate 1), `10	0` numstat confirmed independently.

No other reviewer-authored text was applied this round. `.agent/authored/f306-closure-suite.txt`
is this session's own transcript of real tool output, not a prepared-file copy, so it carries no
digest proof — its content is quoted verbatim below instead.

## Self-use run

Entry id `SU-062`, title "Narrow the excused handler at apps/cli/commands/status_cmd.py:56",
provenance "generated (self-use-generator tier 4, excused handler,
apps/cli/commands/status_cmd.py:1:except Exception:  # noqa: BLE001 — slug lookup failure falls
back to a truncated id)". `generate_and_append_if_empty()` generated it (the queue held no pending
item); `next_self_use_item()` then answered the same entry.

Job id `d477b678080e4742`. Builder: provider `claude-cli`, model `claude-sonnet-4-6` (effort
`medium`, all sourced `cli`). Reviewer: provider `claude-cli`, model `claude-sonnet-4-6` (effort
`medium`, all sourced `cli`). `claude_cli_customizations` false (default), `claude_cli_all_tools`
false (default).

Job state `completed`, stop reason empty, stop source empty, error empty, run manifest error
empty. Task `T001`: status `applied_to_job_workspace`, reviewer verdict `pass`, final status
`staged_review_passed`, repair rounds used `0`.

Wall seconds (from `timing.txt`): `50.3`.

Changed paths (from `changed_paths.txt`): `apps/cli/commands/status_cmd.py`,
`tests/test_ble001_ratchet.py`.

Job diff (`job_diff.txt`), VERBATIM:
```
$ git diff HEAD...remedy/job-d477b678080e4742  (exit 0)
diff --git a/apps/cli/commands/status_cmd.py b/apps/cli/commands/status_cmd.py
index f535e879d..bd7049b34 100644
--- a/apps/cli/commands/status_cmd.py
+++ b/apps/cli/commands/status_cmd.py
@@ -50,10 +50,10 @@ def _cmd_status(
     if scope.project_id and scope.project_id != (str(project.id) if project else None):
         from uuid import UUID
 
-        from packages.orchestration.project_registry import load_project
+        from packages.orchestration.project_registry import ProjectNotFoundError, load_project
         try:
             project_slug = load_project(UUID(scope.project_id)).slug
-        except Exception:  # noqa: BLE001 — slug lookup failure falls back to a truncated id
+        except (ValueError, ProjectNotFoundError, OSError):
             project_slug = scope.project_id[:8]
 
     jobs, degraded, skipped_files = scoped_jobs(scope)
diff --git a/tests/test_ble001_ratchet.py b/tests/test_ble001_ratchet.py
index ff1f68ae3..cb21e641a 100644
--- a/tests/test_ble001_ratchet.py
+++ b/tests/test_ble001_ratchet.py
@@ -18,7 +18,7 @@ REASONED = re.compile(r"^ — \S")
 
 #: The number of excused blind handlers when BLE001 was turned on. Only ever falls: the
 #: commit that removes a mark lowers this number in the same commit, and it is never raised.
-MAX_EXCUSED = 285
+MAX_EXCUSED = 284
 
 
 def _marks() -> list[tuple[str, int, str]]:
```

`run_defects.txt`, VERBATIM:
```
NONE
```

Per the block: no finding is registered by this worker from the above; the reviewer mints ids from
this verbatim quote, and `run_defects.txt` reads `NONE` so there is nothing to register.

## Closure suite

`.agent/authored/f306-closure-suite.txt`, quoted whole and verbatim:
```
command: python3 -m pytest -n auto -q
real exit code: 1
wall time: 348.3s (the launcher's reading); pytest's own reported wall time: 347.58s (0:05:47)
summary line: 1 failed, 22975 passed, 22 skipped, 1 warning in 347.58s (0:05:47)
bad node ids (failed + errors):
  - tests/orchestration/test_model_routing.py::TestTheCallSiteInventoryIsChecked::test_the_swept_multiset_equals_the_declared_inventory
leftover processes: NONE
tree it ran on: cb5f84574 (F306 R8 C3: the closure's self-use item run to its approval gate, never applied)
reflog before: cb5f84574 HEAD@{2026-10-13 22:59:33 +0200}: commit: F306 R8 C3: the closure's self-use item run to its approval gate, never applied
reflog after: cb5f84574 HEAD@{2026-10-13 22:59:33 +0200}: commit: F306 R8 C3: the closure's self-use item run to its approval gate, never applied
reflog unchanged during the run: yes
cost command: python3 scripts/closure_suite_cost.py --feature F306 --record ~/.remedy-loop/test_load.jsonl
cost exit code: 0
Test load: 1115.89 CPU seconds, 347.59 wall seconds, 22998 tests collected, exit status 1, recorded 2026-10-13T21:05:36Z
This closure's suite used 1115.89 CPU seconds, 11.3 percent less than F203's 1257.35, within the 14.1 percent limit.
The limit is the larger of 10 percent and the largest spread between full-suite runs of the record that collected the same tests, 14.1 percent.
The test modules whose CPU time rose most since F203's closure run:
  +2.86 s  tests/orchestration/test_self_use_runner.py (4.02 -> 6.88)
  +0.40 s  tests/orchestration/test_review_authoritative_e2e.py (0.76 -> 1.16)
  +0.30 s  tests/orchestration/test_dod_runners.py (3.59 -> 3.89)
  +0.29 s  tests/orchestration/test_review_subject_artifact_integrity.py (1.84 -> 2.13)
  +0.25 s  tests/orchestration/test_autonomy.py (1.22 -> 1.47)
  +0.24 s  tests/cli/test_do_repo_catalog_order.py (0.82 -> 1.06)
  +0.24 s  tests/orchestration/test_mission_cockpit.py (0.63 -> 0.87)
  +0.21 s  tests/cli/test_chat_cmd.py (0.32 -> 0.53)
  +0.20 s  tests/cli/test_job_report.py (1.24 -> 1.44)
  +0.20 s  tests/orchestration/test_model_aliases.py (1.73 -> 1.93)
```

## Deviations & assumptions

None. C1 through C4 and every gate ran exactly as the block ordered, including C4's own
red-handling branch (step 6): the suite came back RED with one failed node, and this round
committed the transcript exactly as read, without re-running, investigating or fixing it — that
repair belongs to the next round's reviewer-authored block, per the block's explicit instruction.
The cost script's exit 0 is a reading within the limit, not a finding, so it needed no
registration either.

## Next

1. Phase 1 rule 1: check `.agent/STOP` first.
2. Phase 1 rule 2, the Open PR Gate: no pull request is open for this branch yet.
3. The reviewer reviews round 8, books its verdict and registers every self-use run defect in the
   next round's first commit.
4. A repair round naming every bad node id (the suite came back red this round).
5. The closing round: the Built State, the rotation, the next findings paydown, the STATUS line
   and the pull request.

Operator questions open: 0.
Open findings: 3 (R-1235, R-1246 and R-1252), all owned by F306.

## For the operator, in plain sentences

Before this feature closes, Remedy ran one real piece of paid work on itself: narrowing an overly
broad error handler in one command so it only catches the specific failures it was written for,
and that work was reviewed and accepted but deliberately not merged yet. Separately, Remedy's
whole test collection ran once on the code that will ship: 22,975 tests passed and 1 failed. The
full run took a little under six minutes. The cost script that compares computer time against the
last closed feature found this run used about 11 percent less computer time than that one, which
is within the normal range. Nothing new waits for you; the one failed test is now the next round's
job to repair.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | `f4331c2a3` |
| C2 | done | `ac98104df` |
| C3 | done | `cb5f84574` |
| C4 | done | `cbb8729f7` — suite RED (1 failed, 22975 passed, 22 skipped); transcript committed as read, no repair attempted per the block |
| C5 | done | this commit |
| Gate 1 | passed | `ALL True` (confirmed after C2 and again after C4) |
| Gate 2 | passed | all ten files non-empty, sizes listed above |
| Gate 3 | passed (reading red) | exit 1; one bad node id; read, not re-run |
| Gate 4 | passed | six checks pass, `fail_count` 0; open findings `['R-1235', 'R-1246', 'R-1252']` |
| Gate 5 | pending at write time | runs after this commit and the push; result in the session's final reply |
| Push | pending at write time | runs after this commit; result in the session's final reply |
