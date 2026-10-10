# Handback — F302 round 6: book round 5, the consolidation pass, the closure's self-use item, and the integration gate

## Session

SESSION 1 of feature F302 · round 6 · rounds so far 6

Context self-assessment: the reviewer's context holds; the session continues with the closure
sequence.

Fortschritt: ~88 % (building, the consolidation pass, the self-use run and the one full suite done
· the evidence, the package and the closing commit remain) — Schätzung

## Range

Review of `73b14adbb`..`b084e1580` (four commits on `feature/f302-claude-cli-tokens` — C1
`34d8c3c46`, C2 `9884c4463`, C3 `047e3fd69`, C4 `b084e1580` — plus this handback, C5).

## Commits

### `34d8c3c46` F302 R6 C1: book round 5, a prose slip, the plan, save the block and the self-use script

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f302-r6-selfuse.py` | 122/0 | NEW FILE — byte copy of `selfuse.py` |
| `.agent/authored/f302-r6.md` | 176/0 | NEW FILE — byte copy of `block.md` |
| `.agent/live_review.md` | 2/0 | appended `src/ledger-append.txt` — books round 5's PASS verdict |
| `.agent/plan.md` | 7/5 | replaced with `src/plan.md` |
| `.agent/prose_slips.md` | 1/0 | appended `src/prose_slips-append.txt` — a prose slip |

### `9884c4463` F302 R6 C2: the checklist's consolidation pass for F302

| Path | +/- | Reason |
|---|---|---|
| `docs/agents/planner_reviewer_prompt.md` | 8/0 | replaced with `dry-planner_reviewer_prompt.md` — F302's consolidation paragraph; nothing joined, no two items merged, list stays at 34 |

### `047e3fd69` F302 R6 C3: the closure's self-use item run to its approval gate, never applied

| Path | +/- | Reason |
|---|---|---|
| `.agent/selfuse_f302/SU-054.md` | 13/0 | NEW FILE — the job's markdown |
| `.agent/selfuse_f302/changed_paths.txt` | 2/0 | NEW FILE |
| `.agent/selfuse_f302/entry_and_job_file.txt` | 5/0 | NEW FILE |
| `.agent/selfuse_f302/execution_config.txt` | 39/0 | NEW FILE |
| `.agent/selfuse_f302/full_transcript.txt` | 14/0 | NEW FILE |
| `.agent/selfuse_f302/job_diff.txt` | 27/0 | NEW FILE |
| `.agent/selfuse_f302/result_state.txt` | 12/0 | NEW FILE |
| `.agent/selfuse_f302/run_defects.txt` | 1/0 | NEW FILE |
| `.agent/selfuse_f302/staleness_after.txt` | 2/0 | NEW FILE |
| `.agent/selfuse_f302/timing.txt` | 3/0 | NEW FILE |
| `scripts/self_use_queue.json` | 8/0 | the generator's one appended entry, SU-054, `consumed_by` empty |

### `b084e1580` F302 R6 C4: the closure's one full suite and its CPU cost

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f302-closure-suite.txt` | 14/0 | NEW FILE — the transcript, in the shape of `.agent/authored/f301-closure-suite.txt` |

### This commit — F302 R6 C5: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file |

## External actions

- `git -C /home/decodeux/Repos/remedy push origin feature/f302-claude-cli-tokens` — runs once after
  this commit, per the block's THEN step; reported in the worker's final reply only.
- The self-use run (C3) is `.agent/authored/f302-r6-selfuse.py` run detached via the reviewer's
  `launch_selfuse.py`/`wait_selfuse.py`. The script itself ran its one real job through the
  `self_use` role's configured provider (2 provider calls, 11,815 total tokens, measured cost
  $0.5249043, job `752a279d6bd14359`), and, to read the staleness catalog after the run, added and
  removed one git worktree of its own (`remedy/job-752a279d6bd14359` at
  `.remedy-wt/f302-r6-jobtree`) — both reported in its own output, not invoked separately by the
  worker.
- The closure suite (C4) is `python3 -m pytest -n auto -q` run detached via the reviewer's
  `launch_suite.py`/`wait_suite.py`.
- No `gh` command ran this round. No merge, no branch creation, no force-push, no stash touched, no
  pull request opened. No worktree was added or removed by the worker directly.

## Verification

**Opening block check**: a Python script read `block.md`'s own sha256
(`3efd52cbca08b1b3dc7d19d10ed30d11bbc27d56219d703afa83f6057225fa52`) and line count (176) — both
equal the harness's stated values.

**Digest check** (all 13 entries of `digests.txt` against the files they name, one Python script):
13 of 13 comparisons `True` (`block.md`, `selfuse.py`, `launch_selfuse.py`, `wait_selfuse.py`,
`launch_suite.py`, `wait_suite.py`, the four `src/` files, `sim-live_review.md`,
`sim-prose_slips.md`, `dry-planner_reviewer_prompt.md`). `ALL_OK`.

**Pre-state** (before any write): `git rev-parse HEAD` read `73b14adbbd0a45e7182aca4de2372722769c7e7c`,
equal to `origin/feature/f302-claude-cli-tokens`'s tip; `git branch --show-current` read
`feature/f302-claude-cli-tokens`; `git status --porcelain` empty; `.agent/STOP` absent.
`git branch --show-current` was re-checked immediately before every one of the four commits C1-C4
and read `feature/f302-claude-cli-tokens` each time.

**C1's byte proofs** (before commit, by a read-only script, after a separate one-time
copy/append script): `.agent/authored/f302-r6.md` == `block.md` `True`;
`.agent/authored/f302-r6-selfuse.py` == `selfuse.py` `True`; `.agent/live_review.md` ==
`git show 73b14adbb:.agent/live_review.md` + `src/ledger-append.txt` `True`, and also ==
`sim-live_review.md` whole `True`; `.agent/prose_slips.md` == `git show 73b14adbb:.agent/prose_slips.md`
+ `src/prose_slips-append.txt` `True`, and also == `sim-prose_slips.md` whole `True`;
`.agent/plan.md` == `src/plan.md` `True`. Seven of seven `True`.
`git diff --cached --numstat` matched the Commits table above.

**C2's byte proof** (before commit): `docs/agents/planner_reviewer_prompt.md` ==
`dry-planner_reviewer_prompt.md` `True`. `git show --numstat 9884c4463`:
`docs/agents/planner_reviewer_prompt.md` 8/0 — adds exactly the consolidation paragraph's lines,
deletes none.

**C3** — the self-use run, launched once, waited to `exit 0`. `generate_and_append_if_empty()`
answered `SU-054`, matching the block's stated reading. After the run: `git status --porcelain`
showed only `scripts/self_use_queue.json` modified and `.agent/selfuse_f302/` new; `git diff
scripts/self_use_queue.json` showed exactly one appended entry, id `SU-054`, `consumed_by` empty.
The ten files under `.agent/selfuse_f302/` were all non-empty (sizes: `SU-054.md` 944,
`entry_and_job_file.txt` 389, `execution_config.txt` 1203, `result_state.txt` 801, `timing.txt`
105, `changed_paths.txt` 54, `full_transcript.txt` 1417, `staleness_after.txt` 59, `job_diff.txt`
1264, `run_defects.txt` 5 bytes).

**C4** — reflog before the suite: `047e3fd69 HEAD@{2026-10-10 10:43:33 +0200}: commit: F302 R6 C3:
the closure's self-use item run to its approval gate, never applied`. Suite launched once, waited
to `exit 0 wall 439.7`. Reflog after the suite: identical to reflog before — unchanged during the
run. The cost script ran once: exit 0,
`Test load: 1213.06 CPU seconds, 438.85 wall seconds, 22444 tests collected, exit status 0, recorded
2026-10-10T08:50:59Z` /
`This closure's suite used 1213.06 CPU seconds, 1.3 percent less than F301's 1228.95, within the 10
percent limit.` `.agent/authored/f302-closure-suite.txt` was then written in the shape of
`.agent/authored/f301-closure-suite.txt` and committed alone.

**Gate 1** (after C4): `git -C /home/decodeux/Repos/remedy status --porcelain` empty, `True`. C1's
and C2's byte proofs, re-run via `git show <commit>:<path>` against each prepared file: 6 of 6
`True`.

**Gate 2**: the ten files under `.agent/selfuse_f302/`, each non-empty — sizes as listed above.

**Gate 3**: the suite of C4 itself, read from the committed transcript — exit code 0, summary line
`22422 passed, 22 skipped, 1 warning in 438.84s (0:07:18)` verbatim, bad node ids `NONE`.

**Gate 4** (one saved script, two `subprocess.run` calls, explicit `cwd`):
```
python3 -m apps.cli.main integrity check --json
```
Exit 0:
```
{"check_count": 6, "checks": [{"message": "handlers=183", "name": "handler_import", "status":
"pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"},
{"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"},
{"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message":
"no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status":
"pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status":
"pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
Six of six checks `pass`, `fail_count 0`.
```
python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"
```
Exit 0:
```
['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1162', 'R-1172', 'R-1176',
'R-1196', 'R-1219', 'R-1220', 'R-1225', 'R-1230', 'R-1235']
```
Matches the block's ordered list exactly.

## Authored-text proofs

`.agent/authored/f302-r6.md` = `block.md` (sha256 and line count both equal, proven in C1).
`.agent/authored/f302-r6-selfuse.py` = `selfuse.py`, proven byte-equal in C1 (the script run in C3
was this committed copy, run in place as `.agent/authored/f302-r6-selfuse.py`). The two C1 appends
(`src/ledger-append.txt`, `src/prose_slips-append.txt`) each applied by byte append and proven equal
to `git show 73b14adbb:<path>` followed by the slice, and the resulting whole files also proven
equal to the reviewer's own simulation (`sim-live_review.md`, `sim-prose_slips.md`); `.agent/plan.md`
applied by a plain file copy of `src/plan.md` and proven byte-equal. `docs/agents/planner_reviewer_prompt.md`
applied by a plain file copy of `dry-planner_reviewer_prompt.md` and proven byte-equal. No other
reviewer-authored text carried a separate obligation this round.

## Self-use run

Entry `SU-054`, "Narrow the excused handler at apps/cli/commands/job.py:1818" (generated,
self-use-generator tier 4, excused handler). Job id `752a279d6bd14359`. From
`execution_config.txt`: builder `claude-cli` model `claude-sonnet-4-6` effort `medium`; reviewer
`claude-cli` model `claude-sonnet-4-6` effort `medium`. From `result_state.txt`: Job State
`completed`, Stop Reason empty, Stop Source empty, Error empty; Task `T001`: Status
`applied_to_job_workspace`, Reviewer Verdict `pass`, Final Status `staged_review_passed`,
repair_rounds_used `0`. Wall seconds (`timing.txt`): `184.4`. Paths (`changed_paths.txt`):
`apps/cli/commands/job.py`, `tests/test_ble001_ratchet.py`. Job diff (`job_diff.txt`), verbatim:

```
$ git diff HEAD...remedy/job-752a279d6bd14359  (exit 0)
diff --git a/apps/cli/commands/job.py b/apps/cli/commands/job.py
index 160b61157..166a2ddad 100644
--- a/apps/cli/commands/job.py
+++ b/apps/cli/commands/job.py
@@ -1815,7 +1815,7 @@ def _cmd_resume(
                 else:
                     out = _wtr.retain_worktree_resume(s, reason)
                     event = "worktree_retained"
-            except Exception as exc:  # noqa: BLE001 — a session's cleanup failure must not strand its lock
+            except (OSError, ValueError) as exc:
                 _wtr.W.release_lock(s.handle)      # never strand the lock
                 append_run_event(data_dir, job_id, event="worktree_retained", metadata={
                     "run_id": s.run_id,
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

`run_defects.txt`, verbatim:

```
NONE
```

No finding is registered by the worker from this; the reviewer mints ids from the verbatim quote
above.

## Closure suite

`.agent/authored/f302-closure-suite.txt`, whole and verbatim:

```
command: python3 -m pytest -n auto -q
real exit code: 0
wall time: 439.7s (measured wrapper); pytest's own reported wall time 438.84s (0:07:18)
summary line: 22422 passed, 22 skipped, 1 warning in 438.84s (0:07:18)
bad node ids (failed + errors): NONE
leftover processes: NONE
tree it ran on: 047e3fd69 (F302 R6 C3: the closure's self-use item run to its approval gate, never applied)
reflog before: 047e3fd69 HEAD@{2026-10-10 10:43:33 +0200}: commit: F302 R6 C3: the closure's self-use item run to its approval gate, never applied
reflog after: 047e3fd69 HEAD@{2026-10-10 10:43:33 +0200}: commit: F302 R6 C3: the closure's self-use item run to its approval gate, never applied
reflog unchanged during the run: yes
cost command: python3 scripts/closure_suite_cost.py --feature F302 --record ~/.remedy-loop/test_load.jsonl
cost exit code: 0
Test load: 1213.06 CPU seconds, 438.85 wall seconds, 22444 tests collected, exit status 0, recorded 2026-10-10T08:50:59Z
This closure's suite used 1213.06 CPU seconds, 1.3 percent less than F301's 1228.95, within the 10 percent limit.
```

## Deviations & assumptions

None. C1 through C4 ran in the block's exact order, each exactly once; every copy/append script ran
exactly once and every later proof used a separate read-only script; `git branch --show-current` was
checked before every commit and read `feature/f302-claude-cli-tokens` each time; the self-use script
and the suite were each launched exactly once by their own reviewer-prepared launcher and waited for
with the matching waiter, never re-run, never started by any other means; no other `claude` start of
any kind; no `REMEDY_TEST_MAX_WORKERS` set, no larger `-n` passed, no second test command; no `cd`,
no shell call joined two commands, every copy/hash/proof ran as a `cwd`-scoped Python script under
`.remedy-wt/f302-r6-worker/`; no file was written under `/tmp`; no file in `.remedy-wt/f302-r6/` was
modified; no mutation outside the paths each commit named; no stash entry touched, no branch other
than the existing one created, no worktree added or removed by the worker directly (the self-use
script's own internal worktree add/remove is reported in External actions); nothing merged, no
force-push; `.agent/STOP` did not appear at any point; commit subjects carry no leading-slash token
and no absolute path.

This section says nothing about this commit's own self-review, per the block; that is reported in
the worker's final reply only.

## Round verdicts

Round 5 PASS, booked by C1 (carried forward via the appended `.agent/live_review.md`). Round 6's
verdict is the reviewer's, to be booked in the next round's first commit.

## For the operator, in plain sentences

Before this feature closes, Remedy ran one real piece of paid work on itself: narrowing a
blind-exception guard in its own job-resume code and tightening the test that counts such guards,
and that work passed its own review and was never applied to the main tree, spending 2 provider
calls and 11,815 tokens in total. Then Remedy ran its whole test collection once on the exact code
that will ship: 22,422 tests passed and none failed, taking about 7 minutes 19 seconds. The cost
script said this run used about 1.3 percent less computer time than the previous feature's closure
run, well inside the allowed 10 percent. Nothing waits for the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`).
2. Rule 2 (Open PR Gate; no pull request is open for this branch yet).
3. The reviewer reviews round 6, books its verdict and registers every self-use run defect in the
   next round's first commit.
4. The evidence bundle and the review package (the suite is green).
5. The rotation, the STATUS line and the pull request.

Operator questions open: 0.
Open findings: 16 (R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176,
R-1196, R-1219, R-1220, R-1225, R-1230 and R-1235, Low; all owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| Pre-state checks | done | HEAD = origin tip = base `73b14adbb`; branch correct; status clean; STOP absent |
| Digest check | done | 13 of 13 `True` |
| C1: book round 5, a prose slip, the plan, save the block and the self-use script | done | 7 of 7 byte proofs `True`; committed `34d8c3c46` |
| C2: the checklist's consolidation pass for F302 | done | byte proof `True`; `git show --numstat` adds 8, deletes 0; committed `9884c4463` |
| C3: the closure's self-use item run to its approval gate, never applied | done | exit 0, SU-054, verdict pass, never applied; 10 files non-empty; committed `047e3fd69` |
| C4: the closure's one full suite and its CPU cost | done | exit 0, `22422 passed, 22 skipped`, no bad node ids; cost exit 0, 1.3% under F301; committed `b084e1580` |
| Gate 1 | passed | status clean; 6 of 6 byte proofs `True` |
| Gate 2 | passed | 10 of 10 files non-empty |
| Gate 3 | passed | exit 0, summary matches, bad node ids `NONE` |
| Gate 4 | passed | integrity 6/6 pass, fail_count 0; open findings list matches exactly |
| Push | pending | reported in the worker's final reply |
