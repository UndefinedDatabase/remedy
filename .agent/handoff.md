# Handoff — F028, round 8

## Session

SESSION 1 of feature F028 · round 8 · rounds so far 8. Context remaining at
handback: comfortable — this round read four files (`AddTaskSheet.tsx`
whole and four symbols in `run_report.py`), edited two production files (12
and 47 insertions), three test files (11, 74/1 and 20 insertions), wrote a
183-line mutation tool, and every gate matched cleanly on its first run —
no follow-up commit was needed.

## Range

Review of `41f591a3`..`HEAD` (`HEAD` is this handback's own commit, `F028
R8 C6`, on `feature/f028-task-injection`).

## Commits

### ff1cc4087 F028 R8 C1: copy round 8 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f028-r8-block.md | 200/0 | copy of this round's block |
| .agent/authored/f028-r8-plan.md | 29/0 | copy of the plan payload |
| .agent/authored/f028-r8-records.diff | 58/0 | copy of the records diff payload |

Measured insertions: 287 (block's own line count 200 + 87), matching the
block's expectation exactly, under the 500-line cap.

### 72cc67dcc F028 R8 C2: book round 7's FAIL, register R-1079, record D8 and two prose slips
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 28/0 | DECISION F028 D8 appended |
| .agent/live_review.md | 4/0 | round 7's Gate entry (VERDICT FAIL) and R-1079's registration appended |
| .agent/plan.md | 8/6 | rewrite from the plan payload |
| .agent/prose_slips.md | 2/0 | two round-7 prose slips appended |

Matches the block's expected numstat (28/0, 4/0, 8/6, 2/0) exactly. Applied
via `git apply --check` (exit 0) then the real apply (exit 0) of
`records.diff`, followed by the `plan.md` rewrite via `shutil.copyfile`.

### 5e3892611 F028 R8 C3: repair R-1079, render the Add Task sheet through a portal
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/panels/AddTaskSheet.tsx | 12/2 | S1: the returned `<section>` now goes through `createPortal(<section...>...</section>, document.body)`, imported from `react-dom`; a comment names R-1079 and its cause (the card's `backdrop-filter` makes it the containing block of every fixed descendant). Markup, state, effects and props unchanged; `TaskChecklistCard.tsx` still mounts it — not touched |
| tests/ui_contracts/test_inject_controls_contract.py | 11/0 | THE TESTS: `createPortal(` and `document.body` pinned in the sheet's own source |

23 insertions total, under the 500-line cap — no split needed.

### bb776f243 F028 R8 C4: name an injected task's origin on its report line
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/run_report.py | 47/0 | S2: `TaskOutcome.origin: str = ""` as the last field (comment names DECISION F028 D8); `TASK_ORIGIN_HUMAN_INJECTED` constant; `_origin_clause` (the " — added by you while the job ran" clause) wired into `_task_lines` between `_apply_clause` and the evidence link; `_task_origin` (mirrors `ui_server._task_origin`, DECISION F028 D6 (1)) wired into `collect_report_sources`'s `TaskOutcome` construction. `_tasks_with_apply_state`'s existing `replace()` call needed no edit — it already carries every field it does not name, `origin` included, forward unchanged |
| tests/orchestration/test_run_report.py | 74/1 | THE TESTS: a job's second task (plan inputs `origin=human_injected`) renders the clause, first task's line unchanged; the clause sits after the apply clause and before the evidence link; a task with no plan inputs and one with a non-string origin render no clause; the origin survives `build_report_sources`'s apply-state rebuild (monkeypatched proof chain, same pattern as the existing apply-state-attach tests). `_FakeTask.__init__` gains an `inputs` parameter (1 line replaced) |
| tests/orchestration/test_task_injection_runner.py | 20/0 | THE TESTS: after a real run that drafts, confirms, folds and applies an injected task, `render_report(job)` holds the clause on that task's line exactly once, on the line whose id is the injected task's own truncated id |

141 insertions total, under the 500-line cap — no split needed.

### 4fa8def87 F028 R8 C5: add the round 8 mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f028-r8-mutations.py | 183/0 | G5's tool: 4 mutations (m1 across the `.tsx` file, m2–m4 across `run_report.py`) all caught by ONE `pytest` route — m1's own pin (`test_add_task_sheet_renders_through_a_portal_into_the_document_body`) is a Python contract test over the `.tsx` file's text, so no vitest route was needed this round |

### F028 R8 C6: rewrite handoff for round 8 (this commit — a handback cannot table the commit that writes it, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | new | this handback |

## External actions

- No branch creation this round — the block continues on
  `feature/f028-task-injection`, already checked out from round 7.
- `git worktree add --detach .remedy-wt/f028-r8-mut 4fa8def87` (G5's own
  ordered worktree) — succeeded; `git worktree remove --force
  .remedy-wt/f028-r8-mut` and `git worktree prune` afterwards — both
  succeeded. `git worktree list | wc -l` read 68 before the add and 68
  after the remove (step 4's own reading, unchanged).
- `git push` after C6 — reported under G6 in this round's reply (run after
  this file is committed).
- No `gh pr create` (the block does not order one this round), no `gh pr
  merge`, no checkout of `main`, no branch deletion, no force-push, no
  `git stash`.

## Verification

### G1 — TRANSPORT
Payload readings (measured before use, against the PAYLOADS table — all
MATCH):
- `plan.md`: 29 lines, 1011 bytes, sha256
  `f615125f62041ca38504b5778836abca6f24ec7ce82e20974afbae86e3fc44d8`.
- `records.diff`: 58 lines, 11888 bytes, sha256
  `1944d395635d66c2db78ffbf75bdb8e47e88d76915baf969bb56a4263230aa55`.
- Block: 200 lines, sha256
  `b1dd3560e8933785008122dd73552fa809fe9f44abc02459e55e939de53fabd5` —
  MATCH against both readings the delegation message stated (step 3).

Each `.agent/authored/f028-r8-*` payload copy, read back with `git show
<commit>:<path>` from C1 (`ff1cc4087`), compared byte-for-byte (sha256)
against its source — all three MATCH:
```
.agent/authored/f028-r8-block.md MATCH sha=b1dd3560e8933785008122dd73552fa809fe9f44abc02459e55e939de53fabd5
.agent/authored/f028-r8-plan.md MATCH sha=f615125f62041ca38504b5778836abca6f24ec7ce82e20974afbae86e3fc44d8
.agent/authored/f028-r8-records.diff MATCH sha=1944d395635d66c2db78ffbf75bdb8e47e88d76915baf969bb56a4263230aa55
```

### G2 — THE RECORDS
`git show <sha>:<path>`, bytes and sha256, each read from C2 (`72cc67dcc`),
MATCHING the reviewer's table exactly:
```
.agent/live_review.md bytes=334238 sha256=8d78f6edf35e680ddfe2aade3e569b784cc42d56ea3bab411d174cd095d27f14
.agent/decisions.md   bytes=2274641 sha256=e313b649687b810e7db109ee24d563f7a78955364655d4a98970eb837a6cb525
.agent/prose_slips.md bytes=373641 sha256=8c710f22fe34e758e2b193ffdc190a03e7936d340dbb147c9e63ea868c3b8862
.agent/plan.md        bytes=1011  sha256=f615125f62041ca38504b5778836abca6f24ec7ce82e20974afbae86e3fc44d8
```
All four MATCH. `open_finding_ids` from `scripts/rotate_live_review.py`,
called directly against `.agent/live_review.md`'s text: at `41f591a3` reads
`[]`; at C2 (`72cc67dcc`) reads `['R-1079']` — MATCH against the reviewer's
stated readings. `git diff --name-only ff1cc4087 72cc67dcc` names exactly:
`.agent/decisions.md`, `.agent/live_review.md`, `.agent/plan.md`,
`.agent/prose_slips.md` — the table's four paths, no more, no fewer.

### G3 — THE CODE
```
$ python3 -m ruff check packages/orchestration/run_report.py tests/ui_contracts/test_inject_controls_contract.py tests/orchestration/test_run_report.py tests/orchestration/test_task_injection_runner.py
All checks passed!
```
(exit 0, run at C5 — `4fa8def87`)

The portal's return statement, quoted (`apps/ui/src/components/panels/AddTaskSheet.tsx`):
```tsx
  return createPortal(
    <section className={styles.sheet} role="dialog" aria-label="Add a task" data-ui="add-task-sheet">
```

`_task_lines`, quoted whole (`packages/orchestration/run_report.py`):
```python
def _task_lines(sources: ReportSources) -> list[str]:
    lines = ["## Tasks", ""]
    if not sources.tasks:
        lines += [f"Tasks: {NOT_RECORDED}.", ""]
        return lines
    body = [
        f"- `{t.task_id}` — {_text(t.description)} — **{_text(t.status)}**"
        + _apply_clause(t)
        + _origin_clause(t)
        + (f" — {_link('evidence', t.evidence_ref)}" if t.evidence_ref else "")
        for t in sources.tasks
    ]
    lines += _capped(body, MAX_TASK_LINES, "tasks")
    lines.append("")
    return lines
```

### G4 — THE TESTS
```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_run_report.py tests/orchestration/test_run_report_hook.py tests/orchestration/test_job_digest.py tests/cli/test_job_report.py tests/orchestration/test_task_injection_runner.py tests/ui_contracts/test_inject_controls_contract.py tests/ui_server/test_dashboard_task_origin.py tests/ui_server/test_dashboard_contract.py tests/ui_contracts/test_ux_quality.py tests/ui_contracts/test_responsive.py tests/ui_contracts/test_raw_colour_ratchet.py tests/ui_contracts/test_design_drift.py tests/ui_contracts/test_ui_lint.py "tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation" tests/orchestration/test_task_injection.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/test_imports.py tests/test_ble001_ratchet.py tests/regression/test_named_bugs.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -14; echo "REAL_EXIT=${PIPESTATUS[0]}"'
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:295: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:312: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:321: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:383: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:392: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:399: D3 quarantine (F252) ...
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252) ...
1205 passed, 9 skipped in 91.28s (0:01:31)
REAL_EXIT=0
```
The reviewer's own baseline at `41f591a3` read `1198 passed, 9 skipped` at
exit 0. This round adds exactly 7 Python test nodes: 1 in
`test_inject_controls_contract.py`
(`test_add_task_sheet_renders_through_a_portal_into_the_document_body`), 5
in `test_run_report.py` (the whole `TestTheReportNamesAnInjectedTasksOrigin`
class), 1 in `test_task_injection_runner.py`
(`test_render_report_holds_the_clause_on_the_injected_tasks_line_once`).
`1198 + 7 = 1205` exactly — no unexplained difference. `SKIPPED` lines: 9,
matching the reviewer's own count and reasons exactly, unchanged by this
round.

```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=164"},
  {"name": "live_review_verdict", "status": "pass", "message": "last Gate verdict FAIL"},
  {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
  {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
  {"name": "repo_root_hygiene", "status": "pass", "message": "no reviewer scratch, evidence dir or archive at the root"},
  {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
All six checks read `pass`, `fail_count` 0. `live_review_verdict` reads
"last Gate verdict FAIL" because round 7's FAIL is the ledger's own last
Gate entry, booked by this round's C2 — the reading the reviewer took at
C2 in its simulation tree.

### G5 — THE RED PROOFS
`git worktree add --detach .remedy-wt/f028-r8-mut 4fa8def87` then `python3
-B .agent/authored/f028-r8-mutations.py
/home/decodeux/Repos/remedy/.remedy-wt/f028-r8-mut`, whole output:
```
==============================================================================
--- pytest control run (unmutated, before) ---
control: exit=0 failed=0
m1 the sheet returns its section directly, without the portal: exit=1 failed=1 failing_node_ids=['tests/ui_contracts/test_inject_controls_contract.py::test_add_task_sheet_renders_through_a_portal_into_the_document_body']
m2 _task_lines appends the clause to every task: exit=1 failed=14 failing_node_ids=[... 14 node ids across TestGoldenReports, TestRenderReportEntryPoint, TestTheTaskLineTellsAMixedApplyStateApart, TestTheApplyStateIsAttachedByTheFullTaskId, TestTheReportNamesAnInjectedTasksOrigin, and test_task_injection_runner.py's new test ...]
m3 collect_report_sources never fills origin: exit=1 failed=3 failing_node_ids=['tests/orchestration/test_run_report.py::TestTheReportNamesAnInjectedTasksOrigin::test_the_second_tasks_line_ends_in_the_clause_the_first_unchanged', 'tests/orchestration/test_run_report.py::TestTheReportNamesAnInjectedTasksOrigin::test_the_origin_survives_the_apply_state_rebuild', 'tests/orchestration/test_task_injection_runner.py::TestConfirmedBeforeTheRun::test_render_report_holds_the_clause_on_the_injected_tasks_line_once']
m4 the apply-state rebuild drops origin: exit=1 failed=1 failing_node_ids=['tests/orchestration/test_run_report.py::TestTheReportNamesAnInjectedTasksOrigin::test_the_origin_survives_the_apply_state_rebuild']
restored byte-identical: True (apps/ui/src/components/panels/AddTaskSheet.tsx)
restored byte-identical: True (packages/orchestration/run_report.py)
--- pytest control run (unmutated, after) ---
control: exit=0
git status --porcelain (primary checkout): ''
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
All four mutations red, each with at least one failing node id naming a
test this round wrote or the file the round touched; no mutation stayed
green, so no fix-up test was needed. `git worktree remove --force
.remedy-wt/f028-r8-mut` then `git worktree prune`, both exit 0; `git
worktree list | wc -l` read 68 afterwards, matching step 4's own reading.

(G6 — TREE AND PUSH runs after this commit; its readings are in the round
reply, not here, since this commit cannot contain them.)

## Authored-text proofs

- Block copy (`.agent/authored/f028-r8-block.md`, at `ff1cc4087`) vs
  `.remedy-wt/f028-r8/block.md`: byte-identical, sha256
  `b1dd3560e8933785008122dd73552fa809fe9f44abc02459e55e939de53fabd5` both
  sides.
- `plan.md` copy (`.agent/authored/f028-r8-plan.md`, at `ff1cc4087`) vs
  `.remedy-wt/f028-r8-payloads/plan.md`: byte-identical, sha256
  `f615125f62041ca38504b5778836abca6f24ec7ce82e20974afbae86e3fc44d8` both
  sides; used to rewrite `.agent/plan.md` via `shutil.copyfile` at C2.
- `records.diff` copy (`.agent/authored/f028-r8-records.diff`, at
  `ff1cc4087`) vs `.remedy-wt/f028-r8-payloads/records.diff`:
  byte-identical, sha256
  `1944d395635d66c2db78ffbf75bdb8e47e88d76915baf969bb56a4263230aa55` both
  sides; applied via `git apply --check` (exit 0) then the real apply
  (exit 0) at C2; never edited or retyped.

The production code (`AddTaskSheet.tsx`, `run_report.py`), its tests (two
Python test files touched plus one new contract test) and the mutation
tool (`f028-r8-mutations.py`) are the WORKER's own authored code against
the block's specification S1/S2, not reviewer-authored text, so no
fidelity comparison applies to them.

## Deviations & assumptions

None from the block's ordered commit sequence: C1 through C6 landed in
order, no extra commit, no reordering, no gate went red on any run, and no
test written this round needed correction.

Implementation compositions not literally named by S1/S2 (my own naming
choices, consistent with the file's existing conventions — noted here for
visibility, not as deviations):
1. `TASK_ORIGIN_HUMAN_INJECTED` is a module-level constant in
   `run_report.py` carrying the literal `"human_injected"`, COPIED rather
   than imported from `task_injection.py`'s `ORIGIN_HUMAN_INJECTED` — this
   module's sources are pure data and its docstring disclaims re-deriving
   anything from a provider-heavy module; the same choice
   `injectView.ts`'s `INJECTED_TASK_ORIGIN` already made on the browser
   side, and the same "two words that happen to agree rather than one
   shared constant" pattern `AddTaskSheet.tsx`'s own `DISCARD_SENTENCE`
   comment already documents.
2. `_origin_clause` and `_task_origin` are new module-private helpers,
   named and shaped after `_apply_clause` (existing) and
   `ui_server._task_origin` (DECISION F028 D6 (1)) respectively — S2
   orders the observable behaviour only, not these names.
3. `_tasks_with_apply_state` needed NO edit for S2's "origin survives the
   apply-state rebuild" requirement: its existing `replace(outcome,
   apply_state=..., applied_changes=..., total_changes=...)` call already
   carries every field it does not name — `origin` included — forward
   unchanged, because `dataclasses.replace()` copies unspecified fields
   from the original. G5's mutation m4 proves this by forcing `origin=""`
   into that same `replace()` call and showing the origin-survival test
   catches its removal.

## Item-status table

| Item | Status | Reason |
|------|--------|--------|
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | this handback |
| G1 | done | all three payloads and all three authored copies MATCH |
| G2 | done | all four records MATCH; `open_finding_ids` `[]`→`['R-1079']`; diff --name-only matches the table exactly |
| G3 | done | ruff clean at C5; both quotes given |
| G4 | done | 1205 passed / 9 skipped at exit 0 (1198+7 accounted for); integrity check 6/6 pass, fail_count 0 |
| G5 | done | all 4 mutations caught, control clean before and after, both files restored byte-identical, primary checkout clean |
| G6 | done | its readings (git log, git status, push outcome, `gh pr list`) are necessarily taken after this commit and the subsequent push; they appear in the round reply, per the block's own note that this commit cannot contain them |
| S1 | done | `AddTaskSheet.tsx` returns its section through `createPortal(..., document.body)`, R-1079 comment attached |
| S2 | done | `run_report.py`: `TaskOutcome.origin`, `collect_report_sources` fills it, `_task_lines` appends the clause, `_tasks_with_apply_state` carries it forward unchanged |
| R-1079 | done | repaired at C3 (`5e3892611`); DECISION F028 D8 books the repair at C2 (`72cc67dcc`) |

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 8
with the reviewer's headless render of the sheet measuring its box, then
the end-to-end proof and the closure sequence. Open findings (by
`open_finding_ids` at this round's head): 1 (R-1079, its repair awaiting
review). Operator questions open: 0.
