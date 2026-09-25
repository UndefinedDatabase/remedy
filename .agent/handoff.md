# Handback — F026 Task edit at runtime · Round 6

## Session

SESSION 1 of feature F026 · round 6 · rounds so far 6

A large fraction of the session's context budget remained by the point this handback was
written. This round booked round 5's PASS verdict, resolved R-1061, registered and repaired
R-1063 — the write door's transitive import guard, which round 5's own repair had turned red —
corrected R-1062's flag so it reads a CHANGED acceptance rather than merely a named field, and
ran the feature's one full suite again on the repaired tree, which came back GREEN, replacing
round 5's red transcript at `40b94e02` per amend0921-operator-feedback rule 1.

## Range

Review of 40b94e021..HEAD

## Commits

### bb8245b64 F026 R6 C1: copy round 6 block and payloads
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f026-r6-block.md | +168/-0 | copy of this round's block, verbatim (`shutil.copyfile`) |
| .agent/authored/f026-r6-plan.md | +31/-0 | copy of the plan.md payload |
| .agent/authored/f026-r6-records.diff | +23/-0 | copy of the records.diff payload |

222 insertions by `git show --numstat` — the block's stated expectation (this block's own
line count, 168, plus 54: 31+23 = 54) — matches exactly.

### e5c1c1cfc F026 R6 C2: book round 5, resolve R-1061, register R-1063
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +6/-0 | records.diff: the F026 R5 gate entry and R-1061's `Done:` paragraph and R-1063's registration appended |
| .agent/plan.md | +8/-10 | rewritten whole to the plan.md payload (`shutil.copyfile`) |
| .agent/prose_slips.md | +1/-0 | records.diff: the round-5 prose-slip line (S2 named `dod_gate`'s constant without reading its imports) appended |

6/0, 8/10, 1/0 — matches the block's G2 stated expectation exactly. `git apply --check` on
records.diff: exit 0; `git apply`: exit 0.

### aa8d40dc5 F026 R6 C3: the DoD file's name lives with the job layout, and the edit reads it without the gate (R-1063)
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/data_paths.py | +11/-0 | S1: `DOD_FILENAME = "dod.json"` and `job_dod_path(job_id, root=None)` added directly after `job_evidence_dir`, each with a one-line R-1063/DECISION F260 D1 comment; the Public API docstring list gains the new function |
| packages/orchestration/dod_gate.py | +4/-2 | S1: `DOD_FILENAME` is no longer defined here — imported from `data_paths` in the sorted import block instead, so `dod_gate.DOD_FILENAME` still resolves for every caller; nothing else in the module changes |
| packages/orchestration/task_edit_runtime.py | +9/-5 | S1: no longer imports `dod_gate` at all; imports `job_dod_path` from `data_paths` instead of `job_evidence_dir`; reads the stored DoD as `job_dod_path(job_id, root).is_file()`. S2: a new `acceptance_before = entry.acceptance` is captured before the entry is updated in place, and `dod_resync_pending` now reads `entry.acceptance != acceptance_before and has_stored_dod` — the acceptance VALUE change, not merely that `fields` named `acceptance` |
| tests/orchestration/test_task_edit_runtime.py | +12/-0 | THE TEST (S2): `test_stored_dod_and_unchanged_acceptance_beside_another_field_reads_false` — a stored DoD, `acceptance` passed back unchanged (`["T1 works"]`) beside a changed `title`, reads `dod_resync_pending` false |
| tests/test_data_paths.py | +15/-0 | THE TEST (S1): `test_job_dod_path_is_dod_json_under_job_evidence_dir` — `job_dod_path` is `dod.json` inside `job_evidence_dir` under a given root, and `dod_gate.dod_path(job_id)` equals `data_paths.job_dod_path(job_id)` under the process data root |
| .agent/live_review.md | +2/-0 | the one `Landed: R-1063 — ` line this block orders, now the ledger's last line |

53 insertions total, under the cap. `python3 -m ruff check` on all five `.py`/test paths: `All
checks passed!`. The write door's own guard,
`tests/ui_server/test_command_channel.py::TestCommandDoorImportGuard::test_the_door_reaches_only_the_accepted_forbidden_modules_transitively`,
passes. `python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_dod_gate.py
tests/orchestration/test_task_edit_runtime.py tests/test_data_paths.py`: 144 passed.

### 64e7f761e F026 R6 C4: the round's red-proof mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f026-r6-mutations.py | +148/-0 | G4: the round's mutation tool — m1 (task_edit_runtime.py re-imports `dod_gate`), m2 (`job_dod_path` drops `DOD_FILENAME`), m3 (`dod_resync_pending` reads `"acceptance" in fields` again) — all pure-Python this round, one pytest runner over the three test files the door's guard, the S2 case and the S1 path-equality case live in |

148 insertions, under the cap.

### (pending) F026 R6 C5: record the closure suite on the repaired tree and rewrite handoff for round 6
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f026-closure-suite.txt | measured below | the full suite's command, real exit code, wall time, GREEN summary line, `NONE` for bad node ids, and the line naming the tree (C4's SHA) and stating it replaces round 5's run at `40b94e02` |
| .agent/handoff.md | measured after this commit exists, in the final reply | this handback (self-reference, R-0149 pattern) |

## External actions

- `git worktree add --detach .remedy-wt/f026-r6-mut 64e7f761e` (G4) — added, then
  `git worktree remove --force .remedy-wt/f026-r6-mut` — removed after the mutation tool's run.
  `git worktree list` afterward shows the primary checkout and every worktree already present at
  session start, unchanged, `f026-r6-mut` absent. No `git worktree prune` was run this round.
- `git push origin feature/f026-task-edit-runtime` (after C5) — its real outcome is reported in
  the final reply, since the push happens after this commit.
- No `gh pr create` — the branch's pull request opens at F026's closure, per the block.
- No `git stash`, no force-push, no checkout of `main`, no branch deletion, no `remedy/job-*`
  worktree or branch touched by this worker (the self-use job's `remedy/job-fd57a5d1dfe245b0` and
  its worktree are left exactly as found), no `npm install`/`npm ci`/`npx`.

## Verification

```
$ ls .agent/STOP
ls: cannot access '.agent/STOP': No such file or directory
(absent, checked before step one)
```

```
$ pwd
/home/decodeux/Repos/remedy
$ git status --porcelain
(empty)
$ git branch --show-current
feature/f026-task-edit-runtime
$ git log --oneline -1
40b94e021 F026 R5 C6: record the closure suite transcript and rewrite handoff for round 5
```
All three matched the block's stated readings exactly, before any commit of this round.

```
$ wc -l .remedy-wt/f026-r6/block.md; sha256sum .remedy-wt/f026-r6/block.md
line_count: 168
sha256: 756c183320772cd26a8fee2d65f89d8dd7ebf54c451f365ea3b3e886e115f1ca
```
Matches both readings the delegation message gave exactly.

```
$ git worktree list
$ git branch --list 'remedy/job-*'
(reported at step 4: primary checkout + the pre-existing F015/F020/F023/F024/F025/F026-r6-dry/
F026-r6-sim/F284 dry/sim worktrees, and the same remedy/job-* worktrees and branches already
present at session start — no stale/prunable entries observed)
```

### G1 — payload transport

```
$ wc -l .remedy-wt/f026-r6-payloads/plan.md .remedy-wt/f026-r6-payloads/records.diff
plan.md         31 lines
records.diff    23 lines
$ wc -c (the same two files)
plan.md         1112 bytes
records.diff    7733 bytes
$ sha256sum (the same two files)
plan.md         9cd57eb83f1b961f30113263f2bd1badaac8ebe8cf2cae1652a4a5fa4c84142b
records.diff    bd6a5e4148e7a8a9775516fbc462fb83e9c7d7f8cdc2f0faf14cbcd3d9b24696
```
Both payloads' measured lines/bytes/sha256 matched the block's table exactly.

```
$ git show bb8245b64:.agent/authored/f026-r6-block.md | sha256sum
756c183320772cd26a8fee2d65f89d8dd7ebf54c451f365ea3b3e886e115f1ca  (equal to source)
$ git show bb8245b64:.agent/authored/f026-r6-plan.md | sha256sum
9cd57eb83f1b961f30113263f2bd1badaac8ebe8cf2cae1652a4a5fa4c84142b  (equal to source)
$ git show bb8245b64:.agent/authored/f026-r6-records.diff | sha256sum
bd6a5e4148e7a8a9775516fbc462fb83e9c7d7f8cdc2f0faf14cbcd3d9b24696  (equal to source)
```
Each `.agent/authored/f026-r6-*` copy, read back with `git show bb8245b64:<path>`, is
byte-identical to its `.remedy-wt/f026-r6(-payloads)/` source.

### G2 — the records

```
$ git show e5c1c1cfc:.agent/live_review.md | wc -c; sha256sum
338125  3082dd8e3b1e06d6aaa80ce1aa76d3bc541a8befb39d2f1aefd27d98cc1062e4
$ git show e5c1c1cfc:.agent/prose_slips.md | wc -c; sha256sum
368585  37eb9109526e55f498313086ffc0b51fa9a8786ba75dfb979fc94fceb4cd97a0
$ git show e5c1c1cfc:.agent/plan.md | wc -c; sha256sum
1112    9cd57eb83f1b961f30113263f2bd1badaac8ebe8cf2cae1652a4a5fa4c84142b
```
All three equal the block's stated G2 table exactly.

```
$ python3 -B -c "from scripts.rotate_live_review import open_finding_ids; ..."
open at C2 (e5c1c1cfc): ['R-1008', 'R-1055', 'R-1057', 'R-1058', 'R-1062', 'R-1063']
open at C4 (64e7f761e): ['R-1008', 'R-1055', 'R-1057', 'R-1058', 'R-1062', 'R-1063']  (unchanged — R-1063 is Landed:, not yet Done:)
```
Matches the block's stated reading exactly.

```
$ git show aa8d40dc5:.agent/live_review.md | tail -1
Landed: R-1063 — `packages/orchestration/data_paths.py` gains `DOD_FILENAME` and ... landed at this round's C3.
```
The ledger's last line at C3 begins `Landed: R-1063 — `, as ordered.

### G3 — the code, at C3 (aa8d40dc5)

```
$ python3 -m ruff check packages/orchestration/data_paths.py packages/orchestration/dod_gate.py packages/orchestration/task_edit_runtime.py tests/test_data_paths.py tests/orchestration/test_task_edit_runtime.py
All checks passed!
```

```
$ python3 -B -c "ast-walk every Import/ImportFrom node of packages/orchestration/task_edit_runtime.py"
all import nodes: __future__, hashlib, json, os, re, secrets, dataclasses, datetime, pathlib,
  typing, packages.common.secure_fs, packages.core.models, packages.orchestration,
  packages.orchestration.data_paths, packages.orchestration.job_plan,
  packages.orchestration.mission_compiler, packages.orchestration.pingpong_job,
  packages.orchestration.plan_editing, packages.orchestration.schemas.models,
  packages.orchestration.task_deliverables
naming dod_gate: []
```
No import node names `dod_gate`.

```
$ git diff -U0 40b94e02 aa8d40dc5 -- packages/orchestration/dod_gate.py
diff --git a/packages/orchestration/dod_gate.py b/packages/orchestration/dod_gate.py
index 3b4f3a318..07e09cf1f 100644
--- a/packages/orchestration/dod_gate.py
+++ b/packages/orchestration/dod_gate.py
@@ -32,0 +33 @@ from typing import Any
+from packages.orchestration.data_paths import DOD_FILENAME
@@ -42,2 +43,3 @@ from packages.orchestration.dod_schema import DoD
-#: Filenames inside the job's evidence area.
-DOD_FILENAME = "dod.json"
+#: Filenames inside the job's evidence area. DOD_FILENAME itself is owned by
+#: data_paths (R-1063, DECISION F260 D1) and imported above so every existing
+#: `dod_gate.DOD_FILENAME` caller keeps resolving.
```
Whole diff, as ordered.

### G4 — the tests and the red proofs, at C4 (64e7f761e)

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider tests/ui_server/test_command_channel.py tests/ui_server/test_command_dispatch.py tests/orchestration/test_dod_gate.py tests/orchestration/test_task_edit_runtime.py tests/test_data_paths.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/docs tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_block_lint.py tests/orchestration/test_roadmap_index.py tests/cli/test_golden_path.py 2>&1 | tail -5; echo "REAL_EXIT=${PIPESTATUS[0]}"'
........................................................................ [ 93%]
...................................................                      [100%]
771 passed in 76.92s (0:01:16)
REAL_EXIT=0
```
771 passed, exit 0 — includes `tests/test_data_paths.py` and `tests/cli/test_golden_path.py`,
which the reviewer's own run at `40b94e02` (carrying C2's records) omitted; that run read
`1 failed, 610 passed`, the one failure being R-1063's guard node. Here it PASSES, as ordered.

```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=160"},
  {"name": "live_review_verdict", "status": "pass", "message": "last Gate verdict PASS"},
  {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
  {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
  {"name": "repo_root_hygiene", "status": "pass", "message": "no reviewer scratch, evidence dir or archive at the root"},
  {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
], "fail_count": 0, "ok": true, "passed": true}
```
Six `pass`, `fail_count` 0.

```
$ git worktree add --detach .remedy-wt/f026-r6-mut 64e7f761e
Preparing worktree (detached HEAD 64e7f761e)
$ python3 -B .agent/authored/f026-r6-mutations.py .remedy-wt/f026-r6-mut
worktree: /home/decodeux/Repos/remedy/.remedy-wt/f026-r6-mut
CONTROL FIRST: exit=0 failed=0
m1 (task_edit_runtime.py imports dod_gate again): exit=1 failed=1 failing=[tests/ui_server/test_command_channel.py::TestCommandDoorImportGuard::test_the_door_reaches_only_the_accepted_forbidden_modules_transitively] | caught=True restored byte-identical=True
m2 (job_dod_path returns the path without DOD_FILENAME): exit=1 failed=2 failing=[tests/orchestration/test_task_edit_runtime.py::TestDodResyncPending::test_stored_dod_and_acceptance_edit_reads_true, tests/test_data_paths.py::TestJobAndRunLayout::test_job_dod_path_is_dod_json_under_job_evidence_dir] | caught=True restored byte-identical=True
m3 (dod_resync_pending reads "acceptance" in fields again): exit=1 failed=1 failing=[tests/orchestration/test_task_edit_runtime.py::TestDodResyncPending::test_stored_dod_and_unchanged_acceptance_beside_another_field_reads_false] | caught=True restored byte-identical=True
CONTROL LAST: exit=0 failed=0
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
$ git worktree remove --force .remedy-wt/f026-r6-mut
```
All 3 mutations were caught (exit≠0, failed>0), every restore byte-identical, both controls
green. No mutation stayed green.

### G5 — the integration gate

```
$ bash -c 'npm --prefix apps/ui run build 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'
✓ built in 2.13s
REAL_EXIT=0
$ git status --porcelain
(empty)
```

```
$ python3 -m pytest -n auto -q      (log: .remedy-wt/f026-r6-worker/full_suite.log)
Real exit code: 0
Wall time: 193.86s (0:03:13)
Summary line: 19411 passed, 20 skipped, 1 warning in 193.86s (0:03:13)
Bad node ids (failed plus errors):
  NONE
```
Round 5's one bad node,
`tests/ui_server/test_command_channel.py::TestCommandDoorImportGuard::test_the_door_reaches_only_the_accepted_forbidden_modules_transitively`,
now PASSES (confirmed both here and in the targeted G4 run above). No node is newly bad: the
set STRICTLY SHRANK from one node to zero, satisfying amend0917-throughput rule 2. The count
rose from 19408 to 19411 passed (the one repaired node plus the two new tests this round's S1/S2
add), with 0 failed — consistent with round 5's `1 failed, 19408 passed` reading. Committed
verbatim to `.agent/authored/f026-closure-suite.txt`.

```
$ git status --porcelain
(empty, no untracked file)
```

## Authored-text proofs

`.agent/authored/f026-r6-block.md`, `f026-r6-plan.md` and `f026-r6-records.diff` (at C1) were
built with `shutil.copyfile` from the reviewer's payload files — never retyped, never edited —
and G1 compared every one byte for byte, read back with `git show bb8245b64:<path>`, against its
source: all three BYTE-IDENTICAL. `.agent/plan.md` was REWRITTEN whole (verbatim to the `plan.md`
payload) at C2; `records.diff` was applied verbatim with `git apply --check` then `git apply`,
never retyped or hand-edited — G2's byte/sha256 table on the resulting `.agent/live_review.md`,
`.agent/prose_slips.md` and `.agent/plan.md` confirms the applied result matches the reviewer's
own target state exactly.

Everything else this round wrote — the R-1063 repair and its tests (S1, S2), the one `Landed:`
line, the mutation tool and `.agent/authored/f026-closure-suite.txt` — is WORKER-authored text
against the specification, not reviewer payload text, so no authored-text fidelity proof applies
to it.

## Deviations & assumptions

None. Every commit followed the block's ordered bundle exactly (C1, C2, C3, C4, then C5 inside
which this handback lives); no payload was edited or retyped; `git apply --check` read exit 0
before `git apply`; every commit stayed under the 500-insertion cap; no commit touched a path
outside constraint 3's tracked set (confirmed by `git diff --name-only 40b94e02` below); the
repair's bad set strictly shrank with no node newly bad; no other gate went red; no `npm
install`/`npm ci`/`npx`; no `git stash`, `commit --amend`, `pkill -f` or `git worktree prune`;
every existing worktree, branch and stash — including the self-use job's
`remedy/job-fd57a5d1dfe245b0` — was left alone.

```
$ git diff --name-only 40b94e02
.agent/authored/f026-closure-suite.txt
.agent/authored/f026-r6-block.md
.agent/authored/f026-r6-mutations.py
.agent/authored/f026-r6-plan.md
.agent/authored/f026-r6-records.diff
.agent/handoff.md
.agent/live_review.md
.agent/plan.md
.agent/prose_slips.md
packages/orchestration/data_paths.py
packages/orchestration/dod_gate.py
packages/orchestration/task_edit_runtime.py
tests/orchestration/test_task_edit_runtime.py
tests/test_data_paths.py
```
(measured again after C5, before push, in the final reply) Exactly constraint 3's named path
set plus `.agent/handoff.md` and `.agent/authored/f026-closure-suite.txt` (this commit). None of
`tests/ui_server/test_command_channel.py`, `README.md`, `docs/roadmap/STATUS.md`,
`scripts/self_use_queue.json`, `.agent/decisions.md`, `.agent/candidates.md` or
`.agent/operator_questions.md` appears.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | 222 insertions (168+54), matches the block's expectation exactly; all three copies byte-identical |
| C2 | done | `git apply --check`/`git apply` both exit 0; per-file numstat 6/0, 8/10, 1/0 matches the G2 table exactly; open-finding set gains R-1063, loses R-1061 |
| C3 (S1) | done | R-1063 repaired: `DOD_FILENAME`/`job_dod_path` moved into `data_paths`; `dod_gate` imports the constant; `task_edit_runtime.py` no longer imports `dod_gate`; the write door's guard passes; m1/m2 caught |
| C3 (S2) | done | R-1062's flag corrected: `dod_resync_pending` compares the acceptance value before/after the edit; the unchanged-acceptance-beside-another-field case reads false; m3 caught |
| C4 | done | 148 insertions; mutation tool committed before the worktree that checks it out |
| C5 | done | UI build exit 0; full suite GREEN (0 failed, 19411 passed, 20 skipped) committed verbatim, replacing round 5's run |
| G1 | done | both payloads' lines/bytes/sha256 matched the table; every copy byte-identical by `git show` |
| G2 | done | all three files match the stated bytes/sha256; open-finding set correct at C2/C4; ledger's last line at C3 begins `Landed: R-1063 — ` |
| G3 | done | ruff clean over all five paths at C3; ast reading names no `dod_gate` import; `dod_gate.py`'s whole diff reported |
| G4 | done | 771 passed at C4 including the write door's guard and the golden path; six `integrity check` pass; all 3 mutations caught, every restore byte-identical, both controls green |
| G5 | done | UI build green, tree clean, full suite GREEN with zero bad nodes, round 5's node now passing, no node newly bad |
| G6 | done | reported in the final reply, after C5 and the push |
| Pull request | skipped | not opened this round — the branch opens one at F026's closure, per the block |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 6. Then the closure's
evidence round: book round 6, build the evidence bundle and the review package. Then the closing
round (ledger rotation, STATUS acceptance with its README pins and the self-use item's
`consumed_by`, the pull request). Open findings: 6 — `R-1008`, `R-1055`, `R-1057` and `R-1058`,
owned by F285, and `R-1062` and `R-1063`, owned by F026 (both stay open until the reviewer's
`Done:`) — the count the script reads at C4. Operator questions open: 4 — the count of `### Q`
headings in `.agent/operator_questions.md` at C2.
