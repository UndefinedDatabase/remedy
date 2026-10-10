# Handback — F205 round 8: book round 7, the consolidation pass, F305's registration, the self-use run and the one full suite

## Session

SESSION 1 of feature F205 · round 8 · rounds so far 8

Context self-assessment: the reviewer's context holds; the session continues with the closure
sequence.

Fortschritt: ~88 % (building, the consolidation pass, F305's registration, the self-use run and the
one full suite done · the evidence, the package and the closing commit remain) — Schätzung

## Range

Review of `a796194fc`..`5221452d8` (5 commits on `feature/f205-multi-repo-missions` — C1
`5ece7e7ba`, C2 `f40595351`, C3 `b5e5b0768`, C4 `4956793d2`, C5 `5221452d8` — plus this handback,
C6).

## Commits

### `5ece7e7ba` F205 R8 C1: book round 7, the plan, save the block and the self-use script

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f205-r8-selfuse.py` | 122/0 | NEW FILE — byte copy of `selfuse.py` |
| `.agent/authored/f205-r8.md` | 189/0 | NEW FILE — byte copy of `block.md` |
| `.agent/live_review.md` | 2/0 | appended `src/ledger-append.txt` — books F205 R7 PASS |
| `.agent/plan.md` | 6/9 | rewritten with `prep/c1/.agent/plan.md` — round 8's goal, current step and next steps |

### `f40595351` F205 R8 C2: the checklist's consolidation pass for F205

| Path | +/- | Reason |
|---|---|---|
| `docs/agents/planner_reviewer_prompt.md` | 12/0 | the consolidation paragraph; nothing joined, the list stays at 34 items |

### `b5e5b0768` F205 R8 C3: register F305, the cockpit's chain band, directly after F205 (DECISION F205 D1 (5))

| Path | +/- | Reason |
|---|---|---|
| `README.md` | 2/2 | `136 of 305` counter; Tier 13 total `9` |
| `docs/roadmap/STATUS.md` | 1/0 | F305's `[ ]` line, directly after F205's |
| `docs/roadmap/features/T13_F206.md` | 1/1 | "Depends on" gains F305 |
| `docs/roadmap/features/T13_F207.md` | 1/1 | "Depends on" gains F305 |
| `docs/roadmap/features/T13_F305.md` | 32/0 | NEW FILE — F305's feature file |
| `tests/docs/test_docs_consistency.py` | 4/1 | `TOTAL_FEATURES = 305` with its comment |

### `4956793d2` F205 R8 C4: the closure's self-use item run to its approval gate, never applied

| Path | +/- | Reason |
|---|---|---|
| `.agent/selfuse_f205/SU-055.md` | 13/0 | NEW FILE — the generated job's markdown |
| `.agent/selfuse_f205/changed_paths.txt` | 2/0 | NEW FILE — the job's changed paths |
| `.agent/selfuse_f205/entry_and_job_file.txt` | 5/0 | NEW FILE — entry + job file pointer |
| `.agent/selfuse_f205/execution_config.txt` | 39/0 | NEW FILE — the run's execution config |
| `.agent/selfuse_f205/full_transcript.txt` | 14/0 | NEW FILE — the job's task summary |
| `.agent/selfuse_f205/job_diff.txt` | 27/0 | NEW FILE — the job branch's diff over HEAD |
| `.agent/selfuse_f205/result_state.txt` | 12/0 | NEW FILE — job/task state and budgets |
| `.agent/selfuse_f205/run_defects.txt` | 1/0 | NEW FILE — `describe_self_use_run_defects()`, empty |
| `.agent/selfuse_f205/staleness_after.txt` | 2/0 | NEW FILE — staleness catalog read from the job branch |
| `.agent/selfuse_f205/timing.txt` | 3/0 | NEW FILE — start/finish/wall seconds |
| `scripts/self_use_queue.json` | 8/0 | the generator's one appended entry, SU-055, `consumed_by` empty |

### `5221452d8` F205 R8 C5: the closure's one full suite and its CPU cost

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f205-closure-suite.txt` | 14/0 | NEW FILE — the suite transcript, exit 0, cost script's two lines |

### This commit — F205 R8 C6: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file |

## External actions

- `git -C /home/decodeux/Repos/remedy push origin feature/f205-multi-repo-missions` — reported in
  the worker's final reply only (runs after this commit).
- No `gh pr create`, no `gh pr list` run this round. No merge, no branch creation/move/deletion, no
  force-push, no stash entry touched, no worktree of the worker's own added or removed (the
  self-use script added and removed its own temporary job worktree, `.remedy-wt/f205-r8-jobtree`,
  internally — see the self-use run section).
- One `claude` invocation this round: the self-use run's own builder/reviewer calls in C4, through
  `self_use_runner.run_next_self_use_item`, via `claude-cli` — never started any other way.

## Verification

**Opening verification** (`verify_block.py`, run as `python3 -I <path>`, before the block was read
whole): `block.md` sha256 `034f72f1484e659d1fb6b4ef70e5b3f95ee0409d4847d6ef79838f85014a2e89`, 189
lines — both equal the order's stated values.

**Digest check** (`verify_digests.py`, before anything else was read): all 17 entries of
`digests.txt` checked against the file each names — 17 of 17 `True`.

**Preconditions**: `git rev-parse HEAD` read `a796194fcd75f1cf9177bccd24e20e55ad281d7c`, equal to
`origin/feature/f205-multi-repo-missions`; `git status --porcelain` empty; `.agent/STOP` absent. No
pull, no branch created, no stash touched. `git branch --show-current` re-run explicitly as a
command of its own immediately before C1, C2, C3 and C4, and read
`feature/f205-multi-repo-missions` every time.

**C1** (`c1_copy.py`, ran once; `c1_verify.py`, read-only): copied `block.md` to
`.agent/authored/f205-r8.md`, `selfuse.py` to `.agent/authored/f205-r8-selfuse.py`, and the two
`prep/c1/.agent/` files over their paths. Proofs: all four copies byte-equal to their prepared
file, `True` (4 of 4); `.agent/live_review.md` equal to `git show a796194fc:.agent/live_review.md`
followed by the bytes of `src/ledger-append.txt`, `True` (lengths 169327 + 1312 = 170639, matching
the actual file). `git status --porcelain` before commit showed exactly the four ordered paths (two
modified, two untracked). Committed as `5ece7e7ba`; `git show --numstat` matched (319 insertions, 9
deletions).

**C2** (`c2_copy.py`, ran once; `c2_verify.py`, read-only): copied the one prepared file over its
path. Proof: the copy byte-equal to the prepared file, `True`. `git diff` before commit showed 12
insertions and 0 deletions — the consolidation paragraph added, nothing else touched, nothing
joined and no two items merged (verified by reading the diff whole). `git status --porcelain`
before commit showed exactly the one ordered path. Committed as `f40595351`; `git show --numstat`
matched (12 insertions, 0 deletions).

**C3** (`c3_copy.py`, ran once; `c3_verify.py`, read-only): copied the six prepared files over
their paths. Proofs: all six copies byte-equal to their prepared file, `True` (6 of 6). `git
status --porcelain` before commit showed exactly the six ordered paths (one new file, five
modified) and nothing else. Checked: the STATUS line of F305 lands directly after F205's; `README.md`
reads `136 of 305` and Tier 13 total `9`; `TOTAL_FEATURES = 305` with its comment;
`T13_F206.md`/`T13_F207.md` "Depends on" lines gain F305. Committed as `b5e5b0768`; `git
show --numstat` matched (41 insertions, 5 deletions).

**C4** (self-use run): launched once via `launch_selfuse.py`, waited on via `wait_selfuse.py` (one
`running` read, then `exit 0`). `generate_and_append_if_empty()` answered `SU-055`, "Narrow the
excused handler at apps/cli/commands/job.py:1981", tier 4 — matching the block's stated prediction
exactly. The run went to `staged_review_passed` (reviewer verdict `pass`), never applied. After the
run, `git status --porcelain` showed exactly `scripts/self_use_queue.json` modified and
`.agent/selfuse_f205/` new (10 files, all non-empty); `git diff scripts/self_use_queue.json` showed
exactly one appended entry, id `SU-055`, `consumed_by` empty. Committed as `4956793d2`; `git
show --numstat` matched (126 insertions, 0 deletions).

**C5** (full suite): reflog before the run: `4956793d2 HEAD@{2026-10-10 17:55:24 +0200}: commit:
F205 R8 C4: the closure's self-use item run to its approval gate, never applied`. Launched once via
`launch_suite.py`, waited on via `wait_suite.py` (one `running` read, then `exit 0 wall 360.1`).
Reflog after the run: identical to the reflog before — the branch did not move during the run.
`grep -c '^FAILED'` and a case-insensitive `error` grep over the transcript both read `0`; no
"process(es) behind" line. Cost script run once:
`python3 scripts/closure_suite_cost.py --feature F205 --record ~/.remedy-loop/test_load.jsonl`,
exit 0, both printed lines recorded verbatim in the transcript file. Wrote
`.agent/authored/f205-closure-suite.txt` in the exact shape of
`.agent/authored/f302-closure-suite.txt`. `git status --porcelain` before commit showed exactly the
one ordered path. Committed as `5221452d8`; `git show --numstat` matched (14 insertions, 0
deletions).

**Gate 1** (`git status --porcelain` + `gate1_byteproofs.py`, after C5): status empty. The byte
proofs of C1, C2 and C3 re-run at this commit against `git show <commit>:<path>` for each commit's
own paths: 11 of 11 comparisons `True`.

**Gate 2** (`gate2_selfuse_files.py`, after C5): all ten files under `.agent/selfuse_f205/`
non-empty — `SU-055.md` 921B, `entry_and_job_file.txt` 366B, `execution_config.txt` 1203B,
`result_state.txt` 810B, `timing.txt` 105B, `changed_paths.txt` 54B, `full_transcript.txt` 1417B,
`staleness_after.txt` 59B, `job_diff.txt` 1139B, `run_defects.txt` 5B.

**Gate 3**: C5's own transcript: exit code 0, summary line `22462 passed, 22 skipped, 1 warning in
359.02s (0:05:59)`, bad node ids `NONE`.

**Gate 4** (`gate4.py`, run once, both calls through its `subprocess.run`):
```
python3 -m apps.cli.main integrity check --json
```
exit 0: six checks `pass` (`handler_import`, `live_review_verdict`, `plan_consistency`,
`relevant_untracked`, `repo_root_hygiene`, `high_blockers_open`), `"fail_count": 0`, `"ok": true`.
```
python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"
```
exit 0: `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1162', 'R-1172',
'R-1176', 'R-1196', 'R-1219', 'R-1220', 'R-1225', 'R-1230', 'R-1235']` — matches the block's ordered
list exactly.

**After the push** — reported in the worker's final reply only.

## Self-use run

- Entry id: `SU-055`.
- Title: "Narrow the excused handler at apps/cli/commands/job.py:1981".
- Job id: `0fcd1aef0852454d`.
- Builder: `claude-cli`, model `claude-sonnet-4-6`, effort `medium`.
- Reviewer: `claude-cli`, model `claude-sonnet-4-6`, effort `medium`.
- Job state: `completed`. Stop reason: (empty).
- Task `T001`: status `applied_to_job_workspace`; reviewer verdict `pass`; final status
  `staged_review_passed`; repair rounds used: 1.
- Wall seconds: `209.0`.
- Changed paths: `apps/cli/commands/job.py`, `tests/test_ble001_ratchet.py`.
- Job diff (`job_diff.txt`, VERBATIM):
```
$ git diff HEAD...remedy/job-0fcd1aef0852454d  (exit 0)
diff --git a/apps/cli/commands/job.py b/apps/cli/commands/job.py
index 160b61157..5c4eb730f 100644
--- a/apps/cli/commands/job.py
+++ b/apps/cli/commands/job.py
@@ -1978,7 +1978,7 @@ def _open_decisions_view(job: JobPlan) -> dict:
                                for d in open_decisions(decisions)],
             'next_action': open_decisions_next_action(decisions),
         }
-    except Exception:  # noqa: BLE001 — a read-only view never fails on this
+    except (ImportError, OSError, ValueError):
         return {'lines': [], 'open_decisions': [], 'next_action': ''}
 
 
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
- `run_defects.txt` (VERBATIM): `NONE`. No finding registered by the worker from this run; the
  reviewer mints ids from the quote above if it finds any.

## Closure suite

`.agent/authored/f205-closure-suite.txt`, quoted whole and verbatim:
```
command: python3 -m pytest -n auto -q
real exit code: 0
wall time: 360.1s (measured wrapper); pytest's own reported wall time 359.02s (0:05:59)
summary line: 22462 passed, 22 skipped, 1 warning in 359.02s (0:05:59)
bad node ids (failed + errors): NONE
leftover processes: NONE
tree it ran on: 4956793d2 (F205 R8 C4: the closure's self-use item run to its approval gate, never applied)
reflog before: 4956793d2 HEAD@{2026-10-10 17:55:24 +0200}: commit: F205 R8 C4: the closure's self-use item run to its approval gate, never applied
reflog after: 4956793d2 HEAD@{2026-10-10 17:55:24 +0200}: commit: F205 R8 C4: the closure's self-use item run to its approval gate, never applied
reflog unchanged during the run: yes
cost command: python3 scripts/closure_suite_cost.py --feature F205 --record ~/.remedy-loop/test_load.jsonl
cost exit code: 0
Test load: 1228.60 CPU seconds, 359.04 wall seconds, 22484 tests collected, exit status 0, recorded 2026-10-10T16:01:33Z
This closure's suite used 1228.60 CPU seconds, 1.3 percent more than F302's 1213.06, within the 10 percent limit.
```

## Authored-text proofs

`.agent/authored/f205-r8.md` = `block.md`, sha256 and line count both equal, proven in C1 and
re-proven at the opening check. `.agent/authored/f205-r8-selfuse.py` = `selfuse.py`, byte-equal,
proven in C1. `docs/agents/planner_reviewer_prompt.md`'s added paragraph, the six `prep/c3/` files,
and the two `prep/c1/.agent/` files were each applied by a plain byte copy and proven byte-equal
against the prepared file, not authored free text from the worker.

## Deviations & assumptions

None.

## Round verdicts

Round 7's PASS is booked by C1 (appended into `.agent/live_review.md` as the "Gate: F205 R7" entry,
part of `src/ledger-append.txt`). Round 8's verdict is the reviewer's, to be booked in the next
round's first commit.

## For the operator, in plain sentences

Before a feature closes, Remedy runs one real piece of work on itself with a paid model, to show it
is used on itself, and then runs its whole test collection once on the code that will ship. The
paid run was asked to narrow an overly broad error handler in the job command's decisions view down
to the specific exceptions it can actually raise, and it finished successfully, passing its
reviewer's check without being applied to the real codebase. That run made 4 provider calls and used
12,441 tokens. The test run passed 22,462 tests and skipped 22, with none failing, in just under six
minutes. The cost script found this feature's test run used about 1.3 percent more computer time
than the previous feature's, which is within the normal range. The part of this feature that draws
each project's repository as a chip in the cockpit's mission view was set aside as a feature of its
own, F305, next in line after this one. Nothing waits for you.

## Next

1. Phase 1 rule 1 (`.agent/STOP`).
2. Rule 2 (Open PR Gate; no pull request is open for this branch yet).
3. The reviewer reviews round 8, books its verdict and registers every self-use run defect in the
   next round's first commit.
4. The evidence bundle and the review package (a green suite).
5. The Built State, the rotation, the STATUS line and the pull request.

Operator questions open: 0.
Open findings: 16 (R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176,
R-1196, R-1219, R-1220, R-1225, R-1230 and R-1235, Low; all owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| Opening verification | done | sha256 and line count both matched |
| Digest check | done | 17 of 17 `True` |
| Preconditions | done | HEAD == base == origin; clean tree; no STOP; branch confirmed before every commit |
| C1: book round 7, the plan, save the block and the self-use script | done | 4 of 4 byte proofs `True`, 1 of 1 concatenation proof `True`; committed `5ece7e7ba` |
| C2: the checklist's consolidation pass for F205 | done | 1 of 1 byte proof `True`; 12 lines added, 0 deleted; committed `f40595351` |
| C3: register F305, the cockpit's chain band | done | 6 of 6 byte proofs `True`; committed `b5e5b0768` |
| C4: the closure's self-use item run to its approval gate, never applied | done | `SU-055` run to `staged_review_passed`, never applied; exit 0; committed `4956793d2` |
| C5: the closure's one full suite and its CPU cost | done | exit 0, `22462 passed, 22 skipped`, cost exit 0; committed `5221452d8` |
| Gate 1 | passed | status clean; 11 of 11 byte proofs re-run `True` |
| Gate 2 | passed | 10 of 10 selfuse files non-empty |
| Gate 3 | passed | exit 0, bad node ids `NONE` |
| Gate 4 | passed | integrity 6/6 `pass`, `fail_count 0`; open-findings list matches exactly |
| Push | pending | reported in the worker's final reply |
