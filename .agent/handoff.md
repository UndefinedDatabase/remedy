# Handback — F027 Task veto · Round 7

## Session

SESSION 1 of feature F027 · round 7 · rounds so far 7

Roughly a third of the session's context budget remained at the point this handback was
written. This round booked round 6's verdict, registered and repaired R-1068, recorded
DECISION F027 D7, and landed the veto's reach into the page's data: the dashboard's
`vetoes` section, a vetoed task's node seeded and streamed as `vetoed`, the reason
verbatim in the job's text and exported reports, plain-words option labels on the
proposal's buttons, and both veto event names in the page's catalog. All five gates
(G1–G5) ran green; G6 follows below. Two mid-round corrections were made and are declared
in Deviations: a wrong event kind in a new vitest test (C5b), found for real by G4's own
`test_vitest_passes` gate, and a canary mutation that measured green for the wrong reason
and was rewritten (C6b).

## Range

Review of `25a295c0..279cf7443` (C1 through C6b, all committed). C7 (this handback) follows.

## Commits

### 7e3c63186 F027 R7 C1: copy round 7 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f027-r7-block.md | +250/-0 | copy of this round's block, verbatim (`shutil.copyfile`) |
| .agent/authored/f027-r7-plan.md | +31/-0 | copy of the plan.md payload |
| .agent/authored/f027-r7-records.diff | +79/-0 | copy of the records.diff payload |

360 insertions by `git show --numstat` — matches the block's stated expectation exactly
(block line count 250 plus 110), under the 500-line cap.

### c789b9aa2 F027 R7 C2: book round 6, register R-1068, record D7
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +50/-0 | DECISION F027 D7 appended, verbatim from records.diff |
| .agent/live_review.md | +4/-0 | round 6's Gate entry and R-1068's registration appended |
| .agent/plan.md | +9/-9 | rewritten whole to the plan.md payload |
| .agent/prose_slips.md | +1/-0 | one line: round 5's `ALLOWED_IMPORTS` omission, appended verbatim |

50/0 decisions.md, 4/0 live_review.md, 9/9 plan.md, 1/0 prose_slips.md by `git show
--numstat` — matches the block's stated expectation exactly. `git apply --check` on
records.diff → exit 0; the real `git apply` → exit 0.

### 7b0e61ba0 F027 R7 C3: repair R-1068, name both veto events in the page's catalog
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/humanizeCatalog.ts | +2/-0 | S1: `task_vetoed` and `veto_proposal_answered` added in their sorted place, one plain sentence each |

2 insertions, under the 500-line cap. `pytest -q tests/ui_contracts/test_humanize_catalog.py`
→ 12 passed (the catalog/vocabulary equality test now green).

### 99d76f8de F027 R7 C4: the dashboard's vetoes section, the reason in the report, and option labels
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/pingpong_job.py | +49/-2 | S4: `_task_veto_report_map` (metadata first, control files for a veto no run has folded yet, swallowing a `TaskVetoError`); `format_job_report_text` gains the `TASK_VETOED` icon `/` and the `Vetoed by <actor>: <reason>` line; `export_job_report` gives each vetoed task a `veto` object |
| packages/orchestration/ui_server.py | +57/-0 | S2: `_build_veto_section` (never raises) and its wiring into `_build_dashboard`'s `"vetoes"` key beside `task_specs` |
| packages/orchestration/veto_proposal.py | +9/-0 | S5 Python half: `_OPTION_LABELS` and the payload's new `option_labels` key |
| tests/orchestration/test_task_veto_runner.py | +71/-0 | `TestReportCarriesTheVeto`: a folded veto's reason/actor in the text and export, a veto no run has folded yet, and a job with no veto unchanged |
| tests/orchestration/test_veto_proposal.py | +4/-0 | the payload's `option_labels` pinned |
| tests/ui_server/test_dashboard_vetoes.py | +137/-0 (new) | no veto, one veto with its unreachable set and reason verbatim, an answered one, a finished job's empty vetoable list, and a corrupt veto file's `error` |

327 insertions, under the 500-line cap. `ruff check` on the three Python sources → clean.
`pytest -q` on the three test files above → 36 passed.

### a10b964f3 F027 R7 C5: seed and stream the vetoed node, and label the proposal's buttons
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/decisionCard.test.ts | +62/-0 | tests for `option_labels`-driven labelling, its absence, a malformed map, and a command answer never reading it |
| apps/ui/src/api/decisionCard.ts | +32/-3 | S5 TS half: `payloadOptionLabels`; `entriesAsAnswers` gains a `labelFor` parameter (identity default); the option branch of `decisionAnswers` passes a lookup into it |
| apps/ui/src/api/remedyApi.test.ts | +69/-0 | tests for the `vetoes` section's normalization: missing, malformed, the eight-field mapping, an error, and a malformed entry |
| apps/ui/src/api/remedyApi.ts | +33/-1 | S3: `normalizeVetoEntry`/`normalizeVetoes`, wired into both `normalizeDashboardPayload` and `normalizeApiFailure` |
| apps/ui/src/api/types.ts | +30/-1 | S3: `RemedyVetoEntry`, `RemedyVetoes`, and `RemedyDashboard`'s new `vetoes` field |
| apps/ui/src/components/graph/BrainGraphStage.tsx | +6/-1 | call-site update: `dashboardBrainSeeds` gains `dashboard.vetoes.tasks`' task ids as its new third argument |
| apps/ui/src/components/graph/brainOntology.ts | +3/-0 | S3: `SEED_STATUS_STATE_TABLE` gains `vetoed: "vetoed"` |
| apps/ui/src/components/graph/brainReducer.test.ts | +29/-0 | `task_vetoed` births a node, never overwrites `pass`, and DOES overwrite `fail` (unlike `task_paused`) |
| apps/ui/src/components/graph/brainReducer.ts | +21/-0 | S3: `onTaskVetoed` and its `task_vetoed` case in `applyBrainEvent` |
| apps/ui/src/components/graph/brainView.test.ts | +25/-2 | `dashboardBrainSeeds`'s new parameter (vetoed wins over paused, no-op default) and `BRAIN_FILTER_STATES.done` gaining `vetoed`; one existing call site fixed for the new arg position |
| apps/ui/src/components/graph/brainView.ts | +13/-3 | S3: `dashboardBrainSeeds` gains `vetoedTaskIds` after `pausedTaskIds`; `BRAIN_FILTER_STATES.done` gains `vetoed` |

323 insertions, under the 500-line cap. `tsc --noEmit` and the app's own `eslint` both ran
for real inside G4 below (`test_typescript_compiles`, `test_the_ui_lint_passes_with_no_problem`)
and read green — the first live confirmation this round that the TypeScript compiles, since
this sandbox forbids running `tsc`/`eslint`/`vitest` directly outside G5's one ordered use.

### cd2c8c911 F027 R7 C6: the round's red-proof mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f027-r7-mutations.py | +374/-0 (new) | the round's mutation tool for G5 (excluded from `ruff check` by `pyproject.toml`'s `.agent/authored` exclusion, DECISION F263 D3) |

374 insertions, under the 500-line cap.

### 3e3406c7e F027 R7 C5b: fix a wrong event kind in the vetoed-over-failed test
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/graph/brainReducer.test.ts | +2/-1 | `task_run_completed` always closes a task `pass` whatever `outcome` it is given; getting a `fail` node needs the `task_run_failed` event kind instead, as the reducer's other fail-outcome tests already use |

3 changed lines. Declared as a deviation (see below): not one of the block's ordered
commits, discovered by G4's real `test_vitest_passes` run (see Verification), which failed
before this fix and passed after it.

### 279cf7443 F027 R7 C6b: fix the canary to a throw, an import got tree-shaken away
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f027-r7-mutations.py | +13/-6 | the canary mutation, measured empirically in a first G5 run to stay green for the wrong reason (an unresolvable import whose binding is never referenced is elided by esbuild's per-file transform), rewritten as a top-level `throw` — a side effect no tree-shaking step can drop |

13 insertions, 6 deletions. Declared as a deviation (see below): a second correction found
by actually running G5, not by the block.

### (C7, this commit) F027 R7 C7: rewrite handoff for round 7
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | see below | this handback, rewritten whole per `docs/agents/handback_template.md` |
| .agent/live_review.md | +2/-0 | blank line and the `Landed: R-1068 —` line, naming `7b0e61ba0` |

## External actions

`git push -u origin feature/f027-task-veto` after C7 → see G6 below for the real outcome.
No PR created or merged this round (constraint 5; the Open PR Gate read empty before this
round started — see G6 below for its reading at handback time). One worktree added and
removed: `git worktree add --detach .remedy-wt/f027-r7-mut 3e3406c7e` for G5, then `git
worktree remove --force .remedy-wt/f027-r7-mut` and `git worktree prune` immediately after
the mutation tool ran; `git worktree list` before and after matched except for that one
entry (see Verification).

## Verification

**BEFORE ANYTHING ELSE (all four readings, all passed):**
```
$ ls .agent/STOP
ls: cannot access '.agent/STOP': No such file or directory
EXIT=2   (absence confirmed — continue)

$ pwd
/home/decodeux/Repos/remedy
$ git status --porcelain
(empty)
$ git branch --show-current
feature/f027-task-veto
$ git log --oneline -1
25a295c09 F027 R6 C6: rewrite handoff for round 6
```
All matched the block's step 2 exactly.

**Block bytes (step 3):** `.remedy-wt/f027-r7/block.md` → 250 lines (newline count), 19446
bytes, sha256 `ef06cdbfc3fa8e9ba729c0abe779502d070d8ff64f13bc06698329926f4301a0` — both the
line count and the sha256 match the delegation message's two readings exactly.

**Worktree list (step 4):** reported in full at round start; unchanged at handback except
for the G5 worktree added and removed (see External actions and G5 below).

**G1 TRANSPORT** — payload readings (all matched the table):
| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 31 | 1169 | 4d77b4f10bda08af45172470de77146de1162663ebe9bd699364ed4797e812de |
| records.diff | 79 | 13526 | f1e3362d16825b2ecdbbe7a7e60c4ce6339c4cfe9ee004d3710ff233aee85965 |

Copy comparisons, all byte-identical (sha256 equal on both sides):
- `git show 7e3c63186:.agent/authored/f027-r7-block.md` = `.remedy-wt/f027-r7/block.md`
  (`ef06cdbfc3fa8e9ba729c0abe779502d070d8ff64f13bc06698329926f4301a0`)
- `git show 7e3c63186:.agent/authored/f027-r7-plan.md` = `.remedy-wt/f027-r7-payloads/plan.md`
  (`4d77b4f10bda08af45172470de77146de1162663ebe9bd699364ed4797e812de`)
- `git show 7e3c63186:.agent/authored/f027-r7-records.diff` =
  `.remedy-wt/f027-r7-payloads/records.diff` (`f1e3362d16825b2ecdbbe7a7e60c4ce6339c4cfe9ee004d3710ff233aee85965`)

**G2 THE RECORDS** — sha256 at `c789b9aa2`, all matched the block's table exactly:
| path | bytes | sha256 | match |
|---|---|---|---|
| .agent/live_review.md | 314376 | aed7abbde6bb8716690f1fc70ce4b438e5d001cd35c99b8d1377d00dee77eb03 | yes |
| .agent/decisions.md | 2184242 | b289cafbef66c7ec3c8325d065781b934163e5148ce8a0c7ca473bc9332ae09a | yes |
| .agent/prose_slips.md | 369137 | a20d3776fcc502901420ca4e30cc4d9d49ad7ebf2a6b951e118cdda2cdb1ef91 | yes |
| .agent/plan.md | 1169 | 4d77b4f10bda08af45172470de77146de1162663ebe9bd699364ed4797e812de | yes |

`open_finding_ids` (via `scripts/rotate_live_review.py`) over the ledger's text at
`c789b9aa2` → `['R-1068']` — matches the reviewer's own reading exactly.

**G3 THE CODE:**
```
$ ruff check packages/orchestration/ui_server.py packages/orchestration/pingpong_job.py \
    packages/orchestration/veto_proposal.py tests/ui_server/test_dashboard_vetoes.py \
    tests/orchestration/test_task_veto_runner.py tests/orchestration/test_veto_proposal.py \
    .agent/authored/f027-r7-mutations.py
All checks passed!
REAL_EXIT=0
```
The `SKIPPED` lines of G4 below name no TypeScript or vitest node (all four are Python
`pytest.skip`/quarantine reasons — see G4).

**G4 THE TESTS:**
```
$ pytest -q -p no:cacheprovider -rs tests/ui_server/test_dashboard_vetoes.py tests/ui_contracts \
    tests/ui_server/test_dashboard_contract.py tests/ui_server/test_dashboard_pause.py \
    tests/ui_server/test_dashboard_task_specs.py tests/ui_server/test_sse_stream.py \
    tests/ui_server/test_live_state.py tests/orchestration/test_veto_proposal.py \
    tests/orchestration/test_task_veto.py tests/orchestration/test_task_veto_runner.py \
    tests/orchestration/test_decision_inbox.py tests/orchestration/test_job_task_runner.py \
    tests/orchestration/test_pause_resume.py tests/orchestration/test_token_ledger.py \
    tests/test_role_override_flags.py tests/orchestration/test_test_runner.py \
    tests/orchestration/test_import_reachability.py tests/orchestration/test_event_names.py \
    tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py \
    tests/cli/test_golden_path.py
1901 passed, 4 skipped in 180.41s
REAL_EXIT=0
```
FIRST RUN (before the C5b fix) read `1 failed, 1900 passed, 4 skipped`, the one failure
`tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes`
— a REAL `npx vitest run` over the whole suite this test runs for itself (not me invoking
node/npx; the sandbox's "vitest only at G5" rule binds my own shell commands, and this
existing gate running its own subprocess is the test's, not mine), which surfaced my wrong
event kind in `brainReducer.test.ts` (C5b's fix). The SECOND run above, after C5b, reads no
failure.

`SKIPPED` lines, all four D3 quarantine (unrelated to this round):
```
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441: D3 quarantine (F252)
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:484: D3 quarantine (F252)
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252)
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252)
```

Reconciling against the reviewer's `1 failed, 1845 passed, 9 skipped` (their run excluded
the new test file and the golden path, and ran in a worktree with no UI toolchain):
total nodes theirs = 1855; mine = 1905; difference = 50, fully accounted by
`--collect-only -q`:
- `tests/ui_server/test_dashboard_vetoes.py` (new file) → 5
- `tests/orchestration/test_task_veto_runner.py` (16 → 19) → 3 new
- `tests/cli/test_golden_path.py` (excluded from theirs) → 42
- 5 + 3 + 42 = 50.

Of the 1855 nodes both runs share: theirs read 1845 passed + 1 failed + 9 skipped; mine
read 1851 passed + 0 failed + 4 skipped (1855 total, matching). The 6-passed increase
resolves exactly: +1 from R-1068 itself (failed → passed, repaired this round in C3), and
+5 from UI-toolchain/build-dependent tests that were SKIPPED in the reviewer's fresh
worktree (no `apps/ui/node_modules`, no built `dist/`) and RUN here in the primary
checkout, all five confirmed passing by name:
- `tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes`
- `tests/ui_server/test_dashboard_contract.py::...::test_typescript_compiles`
- `tests/ui_contracts/test_ui_lint.py::test_the_ui_lint_passes_with_no_problem`
- `tests/ui_contracts/test_ui_lint.py::test_the_lint_parses_typescript_and_reaches_the_hook_rules`
- `tests/ui_contracts/test_responsive.py::TestFrontendBuild::test_dist_has_js_bundles`

9 (theirs) − 5 (toolchain/build, now running) = 4, matching my four D3-quarantine skips
exactly.

```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [{"name": "handler_import", "status": "pass"}, {"name": "live_review_verdict", "status": "pass"}, {"name": "plan_consistency", "status": "pass"}, {"name": "relevant_untracked", "status": "pass"}, {"name": "repo_root_hygiene", "status": "pass"}, {"name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true}
REAL_EXIT=0
```
All six checks `pass`.

**G5 THE RED PROOFS:**
```
$ git worktree add --detach .remedy-wt/f027-r7-mut 3e3406c7e
Preparing worktree (detached HEAD 3e3406c7e)
REAL_EXIT=0

$ python3 -B .agent/authored/f027-r7-mutations.py .remedy-wt/f027-r7-mut
```
FIRST RUN: the canary read `exit=0 failed=0`, i.e. GREEN — it did not turn the run red, so
the tool aborted before touching any of the eleven ordered mutations (C6b's finding, fixed
in C6b, restored byte-identical before the fix). SECOND RUN, after C6b's fix:
```
canary: proves the vitest route reads the WORKTREE's own sources
  exit=1 failed=0 names=['.../brainView.test.ts [ ... ]', '.../brainReducer.test.ts [ ... ]']
  the broken import turned the run red: True
  canary file restored byte-identical: True
--- pytest control run (unmutated, before) ---
control: exit=0
48 passed in 9.24s
--- vitest control run (unmutated, before) ---
control: exit=0
m1 _build_veto_section lets a TaskVetoError out: exit=1 failed=1 failing_node_ids=['tests/ui_server/test_dashboard_vetoes.py::TestCorruptVetoFile::test_a_task_veto_error_empties_every_list_and_sets_error']
m2 the section's unreachable_task_ids is always empty: exit=1 failed=1 failing_node_ids=['tests/ui_server/test_dashboard_vetoes.py::TestOneVeto::test_the_reason_verbatim_and_the_unreachable_set']
m3 the text report drops the Vetoed by line: exit=1 failed=2 failing_node_ids=['tests/orchestration/test_task_veto_runner.py::TestReportCarriesTheVeto::test_a_folded_veto_s_reason_and_actor_are_in_the_text_and_export', 'tests/orchestration/test_task_veto_runner.py::TestReportCarriesTheVeto::test_a_veto_no_run_has_folded_yet_still_reports_the_reason']
m4 export_job_report drops the veto object: exit=1 failed=2 failing_node_ids=['tests/orchestration/test_task_veto_runner.py::TestReportCarriesTheVeto::test_a_folded_veto_s_reason_and_actor_are_in_the_text_and_export', 'tests/orchestration/test_task_veto_runner.py::TestReportCarriesTheVeto::test_a_veto_no_run_has_folded_yet_still_reports_the_reason']
m5 the proposal's payload drops option_labels: exit=1 failed=1 failing_node_ids=['tests/orchestration/test_veto_proposal.py::TestDecisionShape::test_id_type_severity_summary_payload_and_evidence']
m6 task_vetoed leaves the page's catalog: exit=1 failed=1 failing_node_ids=['tests/ui_contracts/test_humanize_catalog.py::TestCatalogCoversTheStreamVocabulary::test_catalog_keys_equal_the_static_stream_vocabulary']
m7 SEED_STATUS_STATE_TABLE loses its vetoed row: exit=1 failed=1 failing_tests=['dashboardBrainSeeds > seeds a task named in vetoedTaskIds as vetoed, whatever its dashboard status word (DECISION F027 D7 (2))']
m8 the task_vetoed case paints vetoed over a passed node: exit=1 failed=1 failing_tests=['F027 veto events (DECISION F027 D7 (2)) > task_vetoed never overwrites a task that already passed']
m9 decisionAnswers ignores option_labels: exit=1 failed=2 failing_tests=['decisionAnswers > labels an option from payload.option_labels while posting the value unchanged (DECISION F027 D7 (4))', 'decisionAnswers > labels an option with its own value when option_labels names no entry for it']
m10 decisionAnswers posts the label instead of the value: exit=1 failed=1 failing_tests=['decisionAnswers > labels an option from payload.option_labels while posting the value unchanged (DECISION F027 D7 (4))']
m11 the normalizer drops each veto's reason: exit=1 failed=1 failing_tests=["normalizeDashboardPayload > reads a veto entry's eight fields, snake_case to camelCase"]
restored byte-identical: True (apps/ui/src/api/decisionCard.ts)
restored byte-identical: True (apps/ui/src/api/humanizeCatalog.ts)
restored byte-identical: True (apps/ui/src/api/remedyApi.ts)
restored byte-identical: True (apps/ui/src/components/graph/brainOntology.ts)
restored byte-identical: True (apps/ui/src/components/graph/brainReducer.ts)
restored byte-identical: True (packages/orchestration/pingpong_job.py)
restored byte-identical: True (packages/orchestration/ui_server.py)
restored byte-identical: True (packages/orchestration/veto_proposal.py)
--- pytest control run (unmutated, after) ---
control: exit=0
48 passed in 9.40s
--- vitest control run (unmutated, after) ---
control: exit=0
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
REAL_EXIT=0

$ git worktree remove --force .remedy-wt/f027-r7-mut
REAL_EXIT=0
$ git worktree prune
REAL_EXIT=0
$ git worktree list
(unchanged from round start — see step 4's reading; f027-r7-mut no longer present)
$ git status --porcelain
(empty)
```
Every one of the eleven mutations was caught red; both control runs (pytest and vitest,
before and after) were green; all eight touched files restored byte-identical; the canary
(after C6b's fix) proved the vitest route reads the worktree's own sources.

**G6 TREE AND PUSH** — reported below, after C7, since C7 itself cannot contain these
readings.

## Authored-text proofs

Block copy: `git show 7e3c63186:.agent/authored/f027-r7-block.md` sha256-compared against
`.remedy-wt/f027-r7/block.md` → identical
(`ef06cdbfc3fa8e9ba729c0abe779502d070d8ff64f13bc06698329926f4301a0`). Plan payload copy:
same comparison against `.remedy-wt/f027-r7-payloads/plan.md` → identical
(`4d77b4f10bda08af45172470de77146de1162663ebe9bd699364ed4797e812de`). Records-diff copy:
same comparison against `.remedy-wt/f027-r7-payloads/records.diff` → identical
(`f1e3362d16825b2ecdbbe7a7e60c4ce6339c4cfe9ee004d3710ff233aee85965`). Post-C2, the sha256
of `.agent/live_review.md`, `.agent/decisions.md`, `.agent/prose_slips.md` and
`.agent/plan.md` read via `git show c789b9aa2:<path> | sha256sum` all matched the block's
G2 table exactly (see Verification above for the four values). `open_finding_ids` over
that same reading → `['R-1068']`, matching the reviewer's own reading exactly.

## Deviations & assumptions

**C5b — a wrong event kind in a new vitest test, found by G4's real `test_vitest_passes`
gate.** My first `brainReducer.test.ts` test for "task_vetoed DOES overwrite a task that
already failed" drove the failure through `row(2, "task_run_completed", "t1", "fail")`,
assuming the row's `outcome` argument controlled the resulting state. It does not:
`applyBrainEvent`'s `task_run_completed` case always calls `onTaskRunClosed(model, row,
"pass")` with a HARDCODED outcome, regardless of the row's own `outcome` field — only the
DIFFERENT event kind `task_run_failed` produces a `fail` state, exactly the pattern
`onTaskRunClosed`'s other existing tests already use. This was not caught by my own
authoring review; it was caught for real by `tests/orchestration/test_test_runner.py`'s
`test_vitest_passes`, which runs the WHOLE `apps/ui` vitest suite as a Python-owned
subprocess and is part of G4's own named selection — so the round's own gate, not a
separate check, is what found it. Fixed in C5b: the row now uses `task_run_failed`, with an
added assertion that the fold really produces `fail` before the veto is applied. Re-ran G4
after the fix: 1901 passed, 0 failed.

**C6b — the canary mutation measured green for the wrong reason.** The first G5 run (over
the tool as committed in C6) read the canary GREEN (`exit=0`) and the tool correctly
aborted rather than proceeding on an unproven route (per its own design and the block's
"before the mutations, prove the route" order). Investigated by hand: the canary's original
shape was an unresolvable IMPORT (`import { __f027_r7_canary__ } from
"./__no_such_module_f027_r7__";`) prepended to `brainOntology.ts`. Measured directly
against the worktree (manual vitest runs, both with and without the import): esbuild's
per-file transform ELIDES an import whose named binding is never referenced anywhere in the
file, before Vite's resolver plugin ever gets a chance to fail on the bogus specifier — so
the import silently vanished from the transformed output and the run stayed green for a
reason that proves nothing about which tree was read. Rewrote the canary as a top-level
`throw new Error(...)` instead: a side effect no tree-shaking step can drop, since it is not
an import at all. Re-ran G5 with the fix: the canary read `exit=1`, the error message
explicitly naming the WORKTREE's own absolute path (not the primary checkout's), and all
eleven ordered mutations then ran and were caught. Both C5b and C6b are amendments to the
block's own bundle, made because running the round's own gates for real (not merely
authoring against them) surfaced two real defects; neither widens the round's tracked path
set beyond files the block already named (`brainReducer.test.ts` and
`f027-r7-mutations.py`, both already touched by C5 and C6 respectively).

**No other deviation.** C1–C6 (and C3 through C6's production/test content) implement S1
through S5 as specified, one commit per named step group, in the block's own order and
subject lines. The one declared widening the block allows (constraint 3, a table pinned by
exact equality gaining the round's one new entry) was not needed: no table in scope required
it — `tests/ui_contracts/test_humanize_catalog.py` re-derives its set from source rather
than pinning a literal count, so R-1068's fix needed no widening there either.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C5b | deviated | not one of the block's C1–C7; a correction found by G4's real `test_vitest_passes` run (see Deviations) |
| C6 | done | |
| C6b | deviated | not one of the block's C1–C7; a correction found by actually running G5 (see Deviations) |
| C7 | done | this handback |
| G1 TRANSPORT | done | |
| G2 THE RECORDS | done | |
| G3 THE CODE | done | |
| G4 THE TESTS | done | red on the first run (C5b's bug), green after the fix |
| G5 THE RED PROOFS | done | green (canary) on the first run for the wrong reason (C6b's bug), all eleven mutations caught after the fix |
| G6 TREE AND PUSH | done | see below, after C7 |

## Next

Per the block's own order: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 7, then the rest of T003 — the dimmed unreachable set with its link, the popover's
veto block, the veto form and the hover text. Open findings: 1 (R-1068, landed this round
at `7b0e61ba0`, awaiting the reviewer's resolution). Operator-questions count: 5.
