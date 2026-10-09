# Handoff — F300 round 4: book round 3 and R-1160, the Built State, the consolidation pass, the self-use run and the one full suite

## Session

SESSION 1 of feature F300 · round 4 · rounds so far 4

Context self-assessment: the reviewer's context holds; the session continues with the closure sequence.

Fortschritt: ~88 % (building, the Built State, the consolidation pass, the self-use run and the one full suite done · the evidence, the package and the closing commit remain) — Schätzung

## Range

Review of `39bc4c755f742cdf8f72133830c14c22ed498b30`..HEAD (four commits on
`feature/f300-structure-ledger-size-ratchet` — C1, C2, C3, C4 — and this handback, C5).

## Commits

### `4733163ba` F300 R4 C1: book round 3 and R-1160, the Built State, the plan, save the block and the self-use script

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f300-r4.md` | 171/0 | NEW FILE — byte copy of `block.md`; sha256 `36f7835e7c00816396892a4116057f163fca1c3a5e68409df843781b0a4d46de`, 171 lines |
| `.agent/authored/f300-r4-selfuse.py` | 122/0 | NEW FILE — byte copy of `selfuse.py`; sha256 `c50026af265cf57466e2925eb8d5ac2f47a8a392adcbcb3d84a878e0c8c6fd31`, 122 lines |
| `.agent/live_review.md` | 4/0 | replaced with `dry-live_review.md`: re-headed at F300, books F299 R9, moves R-1160's owner to F300 |
| `.agent/plan.md` | 11/12 | replaced with `dry-plan.md`: round 4's goal and current step, the closure sequence |
| `docs/roadmap/features/T2_F300.md` | 41/0 | replaced with `dry-T2_F300.md`: the Built State section, T001-T004 as built |

### `252b0a075` F300 R4 C2: the checklist's consolidation pass for F300

| Path | +/- | Reason |
|---|---|---|
| `docs/agents/planner_reviewer_prompt.md` | 9/0 | the F300 consolidation paragraph: nothing joins, no two items merge, the list stays at 34 items |

### `fb23d424e` F300 R4 C3: the closure's self-use item run to its approval gate, never applied

| Path | +/- | Reason |
|---|---|---|
| `scripts/self_use_queue.json` | 8/0 | the generator's one appended entry, `SU-052`, `consumed_by` empty |
| `.agent/selfuse_f300/SU-052.md` | 13/0 | NEW FILE — the job markdown the runner produced |
| `.agent/selfuse_f300/changed_paths.txt` | 2/0 | NEW FILE — the two paths the job's branch changed |
| `.agent/selfuse_f300/entry_and_job_file.txt` | 5/0 | NEW FILE — entry id, title, provenance, consumed_by, job file path |
| `.agent/selfuse_f300/execution_config.txt` | 39/0 | NEW FILE — the `self_use` role's execution config as run |
| `.agent/selfuse_f300/full_transcript.txt` | 14/0 | NEW FILE — job id, title, state, stop reason, task summary |
| `.agent/selfuse_f300/job_diff.txt` | 27/0 | NEW FILE — `git diff HEAD...remedy/job-449935c821c54023` verbatim |
| `.agent/selfuse_f300/result_state.txt` | 12/0 | NEW FILE — job state, budgets, budget actuals, per-task status |
| `.agent/selfuse_f300/run_defects.txt` | 1/0 | NEW FILE — `describe_self_use_run_defects()`: `NONE` |
| `.agent/selfuse_f300/staleness_after.txt` | 2/0 | NEW FILE — the staleness catalog read from the job branch: `NONE` |
| `.agent/selfuse_f300/timing.txt` | 3/0 | NEW FILE — started, finished, wall seconds |

### `bd0081765` F300 R4 C4: the closure's one full suite and its CPU cost

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f300-closure-suite.txt` | 14/0 | NEW FILE — the suite's transcript in the shape of `f299-closure-suite.txt`: exit 0, `22289 passed, 22 skipped, 1 warning`, cost script exit 0, 8.4% over F299 |

### This commit — F300 R4 C5: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file |

## External actions

None yet. The push is ordered by the block AFTER this commit; its outcome is reported in the
worker's final reply, not in this file, because the handback is written and committed once, before
it. `gh pr list --state open --json number,headRefName,baseRefName,isDraft` read `[]` (checked
informationally; the block orders no PR this round). No `gh pr create`, no `gh pr merge`, no new
branch, no stash entry touched, no `git worktree add`/`remove` at any point this round.

## Verification

**Gate 1** (after C4, before C5): `git status --porcelain` empty; C1's and C2's byte proofs,
re-read from the committed objects with `git show <commit>:<path>` against each prepared file —
all six `True`:
```
4733163ba:.agent/authored/f300-r4.md == block.md: True
4733163ba:.agent/authored/f300-r4-selfuse.py == selfuse.py: True
4733163ba:.agent/live_review.md == dry-live_review.md: True
4733163ba:.agent/plan.md == dry-plan.md: True
4733163ba:docs/roadmap/features/T2_F300.md == dry-T2_F300.md: True
252b0a075:docs/agents/planner_reviewer_prompt.md == dry-planner_reviewer_prompt.md: True
```

**Gate 2**: the ten files under `.agent/selfuse_f300/`, each non-empty, byte sizes:
`SU-052.md` 945, `changed_paths.txt` 54, `entry_and_job_file.txt` 390, `execution_config.txt` 1203,
`full_transcript.txt` 1417, `job_diff.txt` 1150, `result_state.txt` 801, `run_defects.txt` 5,
`staleness_after.txt` 59, `timing.txt` 105.

**Gate 3**, the suite of C4 itself, as the transcript records it: real exit code **0**; summary
line verbatim `22289 passed, 22 skipped, 1 warning in 366.78s (0:06:06)`; bad node ids (failed +
errors): `NONE`.

**Gate 4**:
```
python3 -m apps.cli.main integrity check --json
```
Exit **0**. `fail_count: 0`, six checks, all `status: pass`.
```
python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"
```
Exit **0**. Output, verbatim:
```
['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1162', 'R-1172', 'R-1176', 'R-1196', 'R-1219', 'R-1220', 'R-1225', 'R-1230']
```
Matches the block's ordered list exactly.

**Self-use run and closure suite transcripts**: see the two dedicated sections below.

**After the push** (reported in the worker's final reply, not here): `git status --porcelain`
empty, `git log --oneline -n 6`, and the local tip equal to
`origin/feature/f300-structure-ledger-size-ratchet`.

## Authored-text proofs

`.agent/authored/f300-r4.md` (C1) equals `block.md` byte for byte: sha256
`36f7835e7c00816396892a4116057f163fca1c3a5e68409df843781b0a4d46de`, 171 lines, both at write time
and re-read from the committed object at gate 1.
`.agent/authored/f300-r4-selfuse.py` (C1) equals `selfuse.py` byte for byte: sha256
`c50026af265cf57466e2925eb8d5ac2f47a8a392adcbcb3d84a878e0c8c6fd31`, 122 lines, both at write time
and at gate 1.
`.agent/live_review.md` (C1) equals `dry-live_review.md` byte for byte: sha256
`f1e8701006e16b4b4f6cac6e60d3f496e818e5044575cd38d6d09820dbf7c891`, 217 lines, both at write time
and at gate 1.
`.agent/plan.md` (C1) equals `dry-plan.md` byte for byte: sha256
`c3efa52dc45749cf21b10f1105a1be1da7e61da82753c157c9c15db70465fbdd`, 25 lines, both at write time
and at gate 1.
`docs/roadmap/features/T2_F300.md` (C1) equals `dry-T2_F300.md` byte for byte: sha256
`a45028fb9c812d6865d2e7d36c54d7b5c0f8a75394ba8f5b28f643314e0381fb`, 125 lines, both at write time
and at gate 1.
`docs/agents/planner_reviewer_prompt.md` (C2) equals `dry-planner_reviewer_prompt.md` byte for
byte: sha256 `aca59958720ac302fb7a249430c39e027c51b6750a488d4cc2fa54f5148f0a8f`, 1643 lines, both at
write time and at gate 1.
`.agent/selfuse_f300/*` (C3) and `.agent/authored/f300-closure-suite.txt` (C4) are the worker's own
transcripts of a reviewer-prepared script's real run, not reviewer-authored text pasted verbatim;
no byte-identity proof applies to them, only that every value in `f300-closure-suite.txt` was read
from the launcher's and the cost script's own output, stated in the file as observed.

## Self-use run

Entry `SU-052`, "Narrow the excused handler at apps/cli/commands/job.py:1309", job id
`449935c821c54023`. Builder: `claude-cli`, model `claude-sonnet-4-6`, effort `medium`. Reviewer:
`claude-cli`, model `claude-sonnet-4-6`, effort `medium` (both from `execution_config.txt`). Job
state: `completed`; stop reason: (empty); stop source: (empty) (from `result_state.txt`). Task
`T001`: status `applied_to_job_workspace`; reviewer verdict `pass`; final status
`staged_review_passed`; repair rounds used `0` (from `result_state.txt`). Wall seconds: `205.1`
(from `timing.txt`). Changed paths (from `changed_paths.txt`):
```
apps/cli/commands/job.py
tests/test_ble001_ratchet.py
```
Job diff (from `job_diff.txt`), VERBATIM:
```
$ git diff HEAD...remedy/job-449935c821c54023  (exit 0)
diff --git a/apps/cli/commands/job.py b/apps/cli/commands/job.py
index 160b61157..ffcf1cb32 100644
--- a/apps/cli/commands/job.py
+++ b/apps/cli/commands/job.py
@@ -1306,7 +1306,7 @@ def _cmd_job_run_cycles(
     log = RunLogWriter(job_id=job.job_id)
     try:
         builder = OllamaBuilder()
-    except Exception as exc:  # noqa: BLE001 — builder construction failure is reported, not a crash
+    except (ValueError, KeyError) as exc:
         fail("builder_unavailable", f'builder unavailable — {exc}', json_output=json_output)
 
     limits = replace(limits, budgets=job.budgets)
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
This run was NEVER applied to the primary tree — the job's change lives only on its own
`remedy/job-449935c821c54023` branch; `scripts/self_use_queue.json`'s new entry carries an empty
`consumed_by`. No finding is registered by this worker for this run; the reviewer mints ids, if any,
from the verbatim quote above.

## Closure suite

`.agent/authored/f300-closure-suite.txt`, whole and verbatim:
```
command: python3 -m pytest -n auto -q
real exit code: 0
wall time: 367.6s (measured wrapper); pytest's own reported wall time 366.78s (0:06:06)
summary line: 22289 passed, 22 skipped, 1 warning in 366.78s (0:06:06)
bad node ids (failed + errors): NONE
leftover processes: NONE
tree it ran on: fb23d424e (F300 R4 C3: the closure's self-use item run to its approval gate, never applied)
reflog before: fb23d424e HEAD@{2026-10-09 23:25:07 +0200}: commit: F300 R4 C3: the closure's self-use item run to its approval gate, never applied
reflog after: fb23d424e HEAD@{2026-10-09 23:25:07 +0200}: commit: F300 R4 C3: the closure's self-use item run to its approval gate, never applied
reflog unchanged during the run: yes
cost command: python3 scripts/closure_suite_cost.py --feature F300 --record ~/.remedy-loop/test_load.jsonl
cost exit code: 0
Test load: 1264.11 CPU seconds, 366.80 wall seconds, 22311 tests collected, exit status 0, recorded 2026-10-09T21:31:22Z
This closure's suite used 1264.11 CPU seconds, 8.4 percent more than F299's 1166.53, within the 10 percent limit.
```

## Deviations & assumptions

One observation, not a deviation from the block's ordered sequence: C1's commit-message summary
line from `git commit` read "5 files changed, 363 insertions(+), 26 deletions(-)", while the
authoritative `git show --numstat` reading of that same commit is 349 insertions and 12 deletions
(122+171+4+11+41=349; 0+0+0+12+0=12) — both well under the 500-insertion cap either way, and the
table above uses the `--numstat` reading. Otherwise: None. C1 through C4 and gates 1 through 4 ran
exactly as the block ordered, each exactly once, in the block's sequence; no file outside each
commit's named paths was touched; the self-use run (C3) and the full suite (C4) each ran exactly
once, through the reviewer's launcher scripts, never a second time; no `pytest` ran outside C4; no
`REMEDY_TEST_MAX_WORKERS` was set and no larger `-n` was passed; no worktree of the worker's own was
created (the self-use script's own job-branch worktree add/remove, inside `.agent/authored/f300-r4-selfuse.py`,
is the reviewer-authored script's action, not the worker's); no mutation; no npm; `.agent/STOP` did
not appear at any point.

## Round verdicts

F300 round 3's PASS, with R-1160 resolved, is booked by C1 into `.agent/live_review.md`'s heading
and Steps. Round 4's verdict is the reviewer's, to be booked in the next round's first commit.

## For the operator, in plain sentences

Before a feature closes, Remedy runs one real piece of work on itself with a paid model, to show it
is used on itself, and then runs its whole test collection once on the code that will ship. The paid
run was asked to narrow one overly broad exception handler in the job command and tighten the test
that counts such handlers, and it finished with the reviewer's own check approving the change,
though the change itself was never merged into Remedy. It cost about one dollar. All 22,289 tests
passed and none failed, with 22 intentionally skipped. The whole run took about six minutes. The
cost script said this run used about 8 percent more computer time than the last feature's run,
which is still within the normal range. Nothing waits for the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`).
2. Phase 1 rule 2 (the Open PR Gate; no pull request is open for this branch yet).
3. The reviewer reviews round 4, books its verdict and registers every self-use run defect in the
   next round's first commit.
4. The evidence bundle and the review package (the suite was green).
5. The rotation, the STATUS line and the pull request.

Operator questions open: 0.
Open findings: 15 (R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176,
R-1196, R-1219, R-1220, R-1225 and R-1230, Low; all owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| Base check | done | HEAD and origin both `39bc4c755`, clean tree, correct branch, no STOP |
| C1: book round 3 and R-1160, the Built State, the plan, save the block and the self-use script | done | all five byte proofs `True`; committed `4733163ba` |
| C2: the checklist's consolidation pass for F300 | done | byte proof `True`; +9/-0; committed `252b0a075` |
| C3: the closure's self-use item run to its approval gate, never applied | done | exit 0, cost ~$1.00, never applied; committed `fb23d424e` |
| C4: the closure's one full suite and its CPU cost | done | suite exit 0, 22289 passed/22 skipped; cost script exit 0, 8.4% over F299; committed `bd0081765` |
| Gate 1 | passed | status clean; all six byte proofs `True` |
| Gate 2 | passed | all ten self-use files non-empty |
| Gate 3 | passed | exit 0, summary line verbatim, no bad node ids |
| Gate 4 | passed | integrity check fail_count 0; open findings match the block's list |
| C5: handback | done | this commit |
| Push | pending | reported in the worker's final reply, after this commit |
