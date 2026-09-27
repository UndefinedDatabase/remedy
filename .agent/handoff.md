# Handoff — F028, round 9

## Session

SESSION 1 of feature F028 · round 9 · rounds so far 9. Context remaining at
handback: ample — well under 2% of the session's token budget consumed by
this round's reads (`AGENTS.md`, both live e2e reference files whole,
`task_injection.py`, `ui_server.py`'s injection dispatch and dashboard,
`pingpong_job.py`'s fold, `run_report.py`'s clause, the CLI's inject command
and catalog entry, `test_task_injection_runner.py` and
`test_dashboard_task_origin.py`), one new test file (403 insertions) and one
new tool (170 insertions); every gate matched on its first run and no
correction round was needed.

## Range

Review of `beea934f`..`HEAD` (`HEAD` is this handback's own commit, `F028
R9 C5`, on `feature/f028-task-injection`).

## Commits

### a46f84697 F028 R9 C1: copy round 9 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f028-r9-block.md | 194/0 | copy of this round's block |
| .agent/authored/f028-r9-plan.md | 28/0 | copy of the plan payload |
| .agent/authored/f028-r9-records.diff | 12/0 | copy of the records diff payload |

Measured insertions: 234 (block's own line count 194 + 40), matching the
block's expectation exactly, under the 500-line cap.

### 18f013305 F028 R9 C2: book round 8, resolve R-1079
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 4/0 | round 8's Gate entry (VERDICT PASS) and R-1079's `Done:` paragraph appended |
| .agent/plan.md | 8/9 | rewrite from the plan payload |

Matches the block's expected numstat (4/0, 8/9) exactly. Applied via
`git apply --check` (exit 0) then the real apply (exit 0) of
`records.diff`, followed by the `plan.md` rewrite via `shutil.copyfile`.

### c3e9bd567 F028 R9 C3: prove an injection end to end through the door and the command line
| Path | +/- | Reason |
|---|---|---|
| tests/ui_server/test_task_injection_e2e_live.py | 403/0 | THE TEST: F028 T003 end to end, over an APPROVED two-task plan A then B (B depending on A), `_make_repo`'s fixture repo. (a) THE DOOR PATH: run 1 (`--tasks 1`) pauses the job after A; `job.inject` with `after` set to A's own task id answers 200 `drafted` with `placement.depends_on == ["A"]` and basis `stated`; `job.inject-confirm` answers 200 `confirmed`; the dashboard names no task `human_injected` yet; run 2 (`--tasks 0`) completes the job with three tasks applied, the new task's plan carrying `origin=human_injected` and `plan_rationale="placed after A because you named it"`, the edit log's last `plan_add_task` entry's `injection` block naming the draft with `confirmed_unseen` False, the run log holding exactly one `task_injected` event (`outcome=applied`, naming the new task's id), the `job show --full` report's markdown holding the origin clause exactly once on the new task's line, and — through a live door again — the dashboard naming only the new task `human_injected` and the events stream holding exactly one `task_injected` frame. (b) THE COMMAND LINE PATH: a fresh job, run 1 as in (a), then `apps.cli.grouped.main(["job", "inject", <id>, <text>, "--yes", "--json"])` in the test's own process (`REMEDY_DATA_DIR` via `monkeypatch.setenv`) exits without raising `SystemExit` and prints exactly one JSON document carrying `draft` and `confirmation`; run 2 completes the job with three tasks applied, the edit log's `injection` block reading `confirmed_unseen` True, and the report's clause exactly once. The planner is monkeypatched at `packages.orchestration.task_injection.injection_call_fn` to answer one valid `task_injection_draft_v1` object (`files_hint=["docs/README.md"]`), read by both the door's dispatch and the CLI's own `_cmd_inject`, both local imports of the same module attribute. |

No numstat was expected by the block for C3.

### 56275dcfd F028 R9 C4: add the round 9 probe tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f028-r9-probes.py | 170/0 | G5's tool: 3 probes (p1 `run_report.py`'s `_origin_clause` forced to answer `""`, p2 `ui_server.py`'s `_task_origin` forced to answer `""`, p3 `pingpong_job.py`'s `_fold_task_injections` forced to `return False` before it reads any confirmation) all caught by ONE `pytest` route over the new test file alone — no other test needed touching to catch any of the three |

### F028 R9 C5: rewrite handoff for round 9 (this commit — a handback cannot table the commit that writes it, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | new | this handback |

## External actions

- No branch creation this round — the block continues on
  `feature/f028-task-injection`, already checked out from round 8.
- `git worktree add --detach .remedy-wt/f028-r9-mut 56275dcfd` (G5's own
  ordered worktree) — succeeded; `git worktree remove --force
  .remedy-wt/f028-r9-mut` and `git worktree prune` afterwards — both
  succeeded. `git worktree list | wc -l` read 69 before the add and 69
  after the remove (step 4's own reading, unchanged).
- `git push` after C5 — reported under G6 in this round's reply (run after
  this file is committed).
- No `gh pr create` (the block does not order one this round), no `gh pr
  merge`, no checkout of `main`, no branch deletion, no force-push, no
  `git stash`.

## Verification

### G1 — TRANSPORT
Payload readings (measured before use, against the PAYLOADS table — both
MATCH):
- `plan.md`: 28 lines, 1049 bytes, sha256
  `cb4f63eaf6180c0bbd83009fb158cf8dad9d075b64649ddb1c415ab1a17bb369`.
- `records.diff`: 12 lines, 7510 bytes, sha256
  `b91ce50f4da5ea7f8676db12c0242e550a08eff7f9be4628f83fe4bd1448f283`.
- Block: 194 lines, sha256
  `c5dbe5b9154a2e6cf69a441c7d8191824422f0defec5d6c2d0b0060c012a1499` —
  MATCH against both readings the delegation message stated (step 3).

Each `.agent/authored/f028-r9-*` payload copy, read back with `git show
<commit>:<path>` from C1 (`a46f84697`), compared byte-for-byte (sha256)
against its source — all three MATCH:
```
.agent/authored/f028-r9-block.md MATCH sha=c5dbe5b9154a2e6cf69a441c7d8191824422f0defec5d6c2d0b0060c012a1499
.agent/authored/f028-r9-records.diff MATCH sha=b91ce50f4da5ea7f8676db12c0242e550a08eff7f9be4628f83fe4bd1448f283
.agent/authored/f028-r9-plan.md MATCH sha=cb4f63eaf6180c0bbd83009fb158cf8dad9d075b64649ddb1c415ab1a17bb369
```

### G2 — THE RECORDS
`git show <sha>:<path>`, bytes and sha256, each read from C2 (`18f013305`),
MATCHING the reviewer's table exactly:
```
.agent/live_review.md bytes=337093 sha256=038cc36f4b134dea3c13cbf4ee4fc8ae9c936b91ead44bda2b7039e9c2b61a16
.agent/plan.md         bytes=1049  sha256=cb4f63eaf6180c0bbd83009fb158cf8dad9d075b64649ddb1c415ab1a17bb369
```
Both MATCH. `open_finding_ids` from `scripts/rotate_live_review.py`, called
directly against `.agent/live_review.md`'s text: at `beea934f` reads
`['R-1079']`; at C2 (`18f013305`) reads `[]` — MATCH against the reviewer's
stated readings. `git diff --name-only a46f84697 18f013305` names exactly:
`.agent/live_review.md`, `.agent/plan.md` — the table's two paths, no more,
no fewer.

### G3 — THE CODE
```
$ python3 -m ruff check tests/ui_server/test_task_injection_e2e_live.py
All checks passed!
REAL_EXIT=0
```
(run at C4 — `56275dcfd`)

### G4 — THE TESTS
```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_server/test_task_injection_e2e_live.py tests/ui_server/test_task_veto_e2e_live.py tests/ui_server/test_task_edit_e2e_live.py tests/orchestration/test_task_injection_runner.py tests/cli/test_job_inject.py tests/ui_server/test_command_dispatch.py tests/orchestration/test_run_report.py tests/ui_server/test_dashboard_task_origin.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -20; echo "REAL_EXIT=${PIPESTATUS[0]}"'
........................................................................ [ 11%]
........................................................................ [ 23%]
........................................................................ [ 35%]
........................................................................ [ 47%]
........................................................................ [ 59%]
........................................................................ [ 70%]
........................................................................ [ 82%]
........................................................................ [ 94%]
.................................                                        [100%]
609 passed in 71.30s (0:01:11)
REAL_EXIT=0
```
No `SKIPPED` line appeared. The reviewer's own baseline at `beea934f` (this
same selection LESS the new file) read `607 passed` at real exit code 0.
This round adds exactly 2 Python test nodes, both in the new file
(`test_the_door_path_drafts_confirms_and_folds_the_injection`,
`test_the_command_line_path_yes_confirms_unseen`). `607 + 2 = 609` exactly —
no unexplained difference.

```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=164"},
  {"name": "live_review_verdict", "status": "pass", "message": "last Gate verdict PASS"},
  {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
  {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
  {"name": "repo_root_hygiene", "status": "pass", "message": "no reviewer scratch, evidence dir or archive at the root"},
  {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
All six checks read `pass`, `fail_count` 0. `live_review_verdict` now reads
"last Gate verdict PASS" because this round's own C2 just booked round 8's
PASS as the ledger's last Gate entry.

### G5 — THE REACH OF THE TEST
`git worktree add --detach .remedy-wt/f028-r9-mut 56275dcfd` then `python3
-B .agent/authored/f028-r9-probes.py
/home/decodeux/Repos/remedy/.remedy-wt/f028-r9-mut`, whole output:
```
==============================================================================
--- pytest control run (unmutated, before) ---
control: exit=0 failed=0
p1 _origin_clause answers "": exit=1 failed=2 failing_node_ids=['tests/ui_server/test_task_injection_e2e_live.py::TestTaskInjectionE2ELive::test_the_door_path_drafts_confirms_and_folds_the_injection', 'tests/ui_server/test_task_injection_e2e_live.py::TestTaskInjectionE2ELive::test_the_command_line_path_yes_confirms_unseen']
p2 the dashboard's _task_origin answers "": exit=1 failed=1 failing_node_ids=['tests/ui_server/test_task_injection_e2e_live.py::TestTaskInjectionE2ELive::test_the_door_path_drafts_confirms_and_folds_the_injection']
p3 _fold_task_injections answers False before it reads any confirmation: exit=1 failed=2 failing_node_ids=['tests/ui_server/test_task_injection_e2e_live.py::TestTaskInjectionE2ELive::test_the_door_path_drafts_confirms_and_folds_the_injection', 'tests/ui_server/test_task_injection_e2e_live.py::TestTaskInjectionE2ELive::test_the_command_line_path_yes_confirms_unseen']
restored byte-identical: True (packages/orchestration/pingpong_job.py)
restored byte-identical: True (packages/orchestration/run_report.py)
restored byte-identical: True (packages/orchestration/ui_server.py)
--- pytest control run (unmutated, after) ---
control: exit=0
git status --porcelain (primary checkout): ''
ALL PROBES CAUGHT AND RESTORED CLEANLY: True
```
All three probes red, each with at least one failing node id naming this
round's own test; no probe stayed green, so no fix-up test was needed.
`git worktree remove --force .remedy-wt/f028-r9-mut` then `git worktree
prune`, both exit 0; `git worktree list | wc -l` read 69 afterwards,
matching step 4's own reading.

(G6 — TREE AND PUSH runs after this commit; its readings are in the round
reply, not here, since this commit cannot contain them.)

## Authored-text proofs

- Block copy (`.agent/authored/f028-r9-block.md`, at `a46f84697`) vs
  `.remedy-wt/f028-r9/block.md`: byte-identical, sha256
  `c5dbe5b9154a2e6cf69a441c7d8191824422f0defec5d6c2d0b0060c012a1499` both
  sides.
- `plan.md` copy (`.agent/authored/f028-r9-plan.md`, at `a46f84697`) vs
  `.remedy-wt/f028-r9-payloads/plan.md`: byte-identical, sha256
  `cb4f63eaf6180c0bbd83009fb158cf8dad9d075b64649ddb1c415ab1a17bb369` both
  sides; used to rewrite `.agent/plan.md` via `shutil.copyfile` at C2.
- `records.diff` copy (`.agent/authored/f028-r9-records.diff`, at
  `a46f84697`) vs `.remedy-wt/f028-r9-payloads/records.diff`:
  byte-identical, sha256
  `b91ce50f4da5ea7f8676db12c0242e550a08eff7f9be4628f83fe4bd1448f283` both
  sides; applied via `git apply --check` (exit 0) then the real apply
  (exit 0) at C2; never edited or retyped.

The test (`tests/ui_server/test_task_injection_e2e_live.py`) and the probe
tool (`f028-r9-probes.py`) are the WORKER's own authored code against the
block's specification, not reviewer-authored text, so no fidelity
comparison applies to them.

## Deviations & assumptions

None from the block's ordered commit sequence: C1 through C5 landed in
order, no extra commit, no reordering, no gate went red on any run, and the
test written this round needed no correction before C5 — both its tests
passed on the first run and every G5 probe was caught on the first run of
the tool.

Implementation choices not literally named by THE TEST (my own decisions,
consistent with the two reference files' existing conventions — noted here
for visibility, not as deviations):
1. The two-task plan is named A/B rather than T1/T2, mirroring
   `test_task_veto_e2e_live.py`'s own diamond's task naming rather than
   `test_task_edit_e2e_live.py`'s — THE TEST says "an APPROVED two-task
   plan A then B", so the letters were already given.
2. The door path's `after` reads exactly A's own runtime `task_id`, which
   `resolve_after_ref` (DECISION F028 D5 (1)) resolves to the planned id
   `"A"` before `place_injected_task` runs — proving the door's own
   resolver, never the CLI's `_resolve_after`, which THE TEST never calls.
3. Neither test monkeypatches `task_injection.injection_budget_inputs`:
   both jobs are built with `job.budgets` left at its default `None`, and
   `budget_guard.predict_next_task_cost` reads a `None` limit as nothing to
   breach regardless of the repo's (absent) budget config, so every draft
   answers `drafted`, never `shortfall`, without needing the permissive
   stand-in `test_command_dispatch.py`'s own injection tests use.
4. The command-line path's assertion on `apps.cli.grouped.main`'s exit
   reads "no `SystemExit` raised" rather than "return code 0", because
   `emit_ok` deliberately never calls `sys.exit` (only `fail()` does) —
   the same reading `tests/ui_server/test_live_state.py`'s own successful
   `--json` calls rely on.

## Item-status table

| Item | Status | Reason |
|------|--------|--------|
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | this handback |
| G1 | done | both payloads and all three authored copies MATCH |
| G2 | done | both records MATCH; `open_finding_ids` `['R-1079']`→`[]`; diff --name-only matches the table exactly |
| G3 | done | ruff clean at C4 |
| G4 | done | 609 passed at exit 0 (607+2 accounted for, no SKIPPED line); integrity check 6/6 pass, fail_count 0 |
| G5 | done | all 3 probes caught, control clean before and after, all three files restored byte-identical, primary checkout clean |
| G6 | done | its readings (git log, git status, push outcome, `gh pr list`) are necessarily taken after this commit and the subsequent push; they appear in the round reply, per the block's own note that this commit cannot contain them |
| T003 | done | proved end to end through the door (`job.inject`/`job.inject-confirm`) and the command line (`job inject --yes`), provenance read back from the job record, the edit log, the run log, the dashboard, the events stream and the final report |
| R-1079 | done | resolved (booked) at C2 (`18f013305`), repaired in round 8 |

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 9,
then the closure sequence (docs/roadmap/STATUS_closure_protocol.md). Open
findings (by `open_finding_ids` at this round's head): 0. Operator
questions open: 0.
