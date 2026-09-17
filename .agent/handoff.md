# Handoff — F280 CLI vocabulary v2, part two

SESSION 8 of feature F280 · round 14 · rounds so far 14

This round books round 13's independently-reviewed PASS (Gate: F280 R13, one prose slip noted, no new finding), authors DECISION F280 D9, and executes the rest of DECISION amend0917-throughput D3's `flight_plan` rename—widened to DAG-key construction/membership sites and identifier residue. One 61-file, 339-line mechanical patch, pre-tested twice in a disposable worktree before authoring. All gates G1–G6 PASS.

## Range

Review of `5901e8da`..`746e3fbd` (commits C0a through C2; C0a and C0b were commits prior to C1 and C2).

## Commits

### b9bef79b F280 R14 C0a: write authored block f280-r14.md (transport carrier)
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f280-r14.md` | 100/0 | Block carrier (step block sha256: dd616cba...) |

### ba3b59e9 F280 R14 C0b: mirror authored block to last_block.md
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | 100/116 | Mirror of authored block |

### 5901e8da F280 R14 C1: append Gate:F280 R13 + prose slip, DECISION F280 D9, T2_F280 amendment, replace plan.md
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | 2/0 | Append blank line + Gate:F280 R13 entry (6614 bytes) |
| `.agent/prose_slips.md` | 2/0 | Append blank line + prose slip R13 line (607 bytes) |
| `.agent/decisions.md` | 16/0 | Append blank line + DECISION F280 D9 (8843 bytes) |
| `docs/roadmap/features/T2_F280.md` | 2/0 | Insert D9 amendment after D8, before T002 heading (988 bytes) |
| `.agent/plan.md` | 39/44 | Replace with R14 plan (39 lines) |

Total: 5 files, 61 insertions(+), 44 deletions(-)

### 746e3fbd F280 R14 C2: apply flight_plan rename patch (DAG key, fp: prefix, identifier residue, English prose)
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/command_catalog.py` | 1/1 | Rename "fp:" prefix to "plan:" in catalog metadata |
| `apps/cli/commands/decision.py` | 24/24 | Update decision ID prefix construction and display |
| `apps/cli/commands/do_cmd.py` | 12/12 | Update decision ID prefix in help and execution |
| `apps/cli/commands/job.py` | 18/18 | Rename decision ID prefix and English prose |
| `apps/cli/commands/job_context_cmd.py` | 16/16 | Rename decision ID prefix in context commands |
| `apps/cli/commands/mission_cmd.py` | 2/2 | Update decision ID prefix |
| `apps/ui/src/api/decisionAnswer.test.ts` | 10/10 | Update decision ID prefix in tests |
| `apps/ui/src/api/decisionAnswer.ts` | 2/2 | Update decision ID prefix |
| `apps/ui/src/api/decisionAnswerFlow.test.ts` | 2/2 | Update decision ID prefix |
| `apps/ui/src/api/decisionCard.test.ts` | 10/10 | Update decision ID prefix in tests |
| `apps/ui/src/api/decisionCard.ts` | 6/6 | Update decision ID prefix |
| `apps/ui/src/api/decisionClarificationForm.test.ts` | 2/2 | Update decision ID prefix |
| `apps/ui/src/api/decisionClarificationForm.ts` | 2/2 | Update decision ID prefix |
| `apps/ui/src/api/decisionSend.test.ts` | 6/6 | Update decision ID prefix in test |
| `.../components/panels/DecisionInboxCard.tsx` | 4/4 | Update decision ID prefix display |
| `.../components/panels/RightLivePanel.module.css` | 2/2 | Rename CSS class for decision card |
| `docs/guides/job-context-view-user-guide-v0.md` | 4/4 | Update English prose from flight_plan to task_plan |
| `docs/system/remedy-toml-configuration-system-v0.md` | 2/2 | Update English prose |
| `packages/orchestration/config.py` | 2/2 | Rename function name flight_plan_body → task_plan_body |
| `packages/orchestration/dag_schedule.py` | 10/10 | Rename DAG key "flight" to "plan" and membership test |
| `packages/orchestration/decision_inbox.py` | 8/8 | Update decision ID prefix "fp:" to "plan:" |
| `packages/orchestration/decision_queue.py` | 44/44 | Rename variables _flight_plan, _fp_approval, flight_plan_body, job_flight_plan |
| `packages/orchestration/dod_compiler.py` | 4/4 | Rename decision ID prefix |
| `packages/orchestration/escalation.py` | 10/10 | Rename parameter job_flight_plan and English prose |
| `packages/orchestration/feature_mission_adapter.py` | 2/2 | Update English prose |
| `packages/orchestration/job_plan.py` | 34/34 | Rename function milestone_flight_plan → milestone_task_plan, DAG key construction, decision ID prefix |
| `packages/orchestration/long_run_executor.py` | 4/4 | Rename decision ID prefix and English prose |
| `packages/orchestration/mission_compiler.py` | 32/32 | Rename function milestone_flight_plan → milestone_task_plan and English prose |
| `packages/orchestration/mission_plan_schema.py` | 8/8 | Rename identifier and English prose |
| `packages/orchestration/mission_state.py` | 12/12 | Rename DAG key construction and English prose |
| `packages/orchestration/orchestrator_loop.py` | 2/2 | Update English prose |
| `packages/orchestration/prompt_facts.py` | 4/4 | Rename function citations and English prose |
| `packages/orchestration/run_report.py` | 2/2 | Rename function citation flight_plan.render → job_plan.render |
| `packages/orchestration/schemas/models.py` | 4/4 | Update English prose |
| `packages/orchestration/task_granularity.py` | 2/2 | Update English prose |
| `packages/orchestration/ui_server.py` | 10/10 | Update decision ID prefix |
| `.../gauntlet_orders/g05-two-milestone-mission.json` | 2/2 | Rename DAG key "flight" to "plan" in fixture |
| `scripts/remedy_smoke.sh` | 10/10 | Update decision ID prefix and English prose |
| `tests/cli/test_decision_answers.py` | 28/28 | Rename test class/function names TestMapFlightPlanToTasks → TestMapTaskPlanToTasks et al |
| `tests/cli/test_golden_path.py` | 2/2 | Update English prose |
| `tests/cli/test_job_context_cmd.py` | 6/6 | Update English prose |
| `tests/cli/test_mission_cmd.py` | 18/18 | Rename test identifiers and English prose |
| `tests/cli/test_plan_approval.py` | 42/42 | Rename test class/function names to task_plan variant |
| `tests/cli/test_scoped_listings.py` | 2/2 | Update English prose |
| `tests/orchestration/test_bundled_clarification.py` | 2/2 | Update English prose |
| `tests/orchestration/test_dag_schedule.py` | 8/8 | Rename DAG key and membership test |
| `tests/orchestration/test_decision_evidence.py` | 76/76 | Rename test class/function names and decision ID prefix |
| `tests/orchestration/test_decision_inbox.py` | 24/24 | Update decision ID prefix "fp:" to "plan:" |
| `tests/orchestration/test_escalation.py` | 12/12 | Rename test class/function names and parameter names |
| `tests/orchestration/test_job_plan.py` | 16/16 | Rename TestMapFlightPlanToTasks → TestMapTaskPlanToTasks |
| `tests/orchestration/test_long_run_executor.py` | 12/12 | Rename decision ID prefix and test class/function names |
| `tests/orchestration/test_mission_compiler.py` | 14/14 | Rename test class/function names and identifiers |
| `tests/orchestration/test_mission_state.py` | 8/8 | Rename test class/function names and DAG key |
| `tests/orchestration/test_prompt_cache_prefix.py` | 2/2 | Update English prose |
| `tests/orchestration/test_prompt_trace.py` | 4/4 | Rename test class/function names |
| `tests/orchestration/test_task_granularity.py` | 2/2 | Update English prose |
| `tests/schemas/test_job_plan_schema.py` | 2/2 | Rename test class/function names |
| `tests/test_no_interactive_guard.py` | 2/2 | Update English prose |
| `tests/ui_contracts/test_decision_answer_wiring.py` | 2/2 | Update English prose |
| `tests/ui_server/test_command_channel.py` | 52/52 | Update decision ID prefix and test class/function names |
| `tests/ui_server/test_command_dispatch.py` | 10/10 | Rename test class/function names |

Total: 61 files, 339 insertions(+), 339 deletions(-)

## External actions

```
git worktree add .remedy-wt/r14-mutation1 746e3fbd — created disposable worktree for red-proof mutation 1
git worktree remove .remedy-wt/r14-mutation1 — removed after red-proof verification
git worktree add .remedy-wt/r14-mutation2 746e3fbd — created disposable worktree for red-proof mutation 2
git worktree remove .remedy-wt/r14-mutation2 — removed after red-proof verification
git push origin feature/f280-cli-vocabulary-v2-part-two — to push commits after C3
```

All completed successfully.

## Verification

### G1 TRANSPORT — SHA256 and content fidelity

**Carrier files:**
```
dd616cbadeb702b399ef9cc6c149ede133bb743873c837ea19e5c971b5171350  .agent/authored/f280-r14.md
dd616cbadeb702b399ef9cc6c149ede133bb743873c837ea19e5c971b5171350  .agent/last_block.md
```
✓ SHA256 identical — both carriers match

Exit code: 0

### G2 THE RECORD — after C1

```
Gate entries: 40
Open R-ids (distinct): 136
Done R-ids (distinct): 7
DECISION count: 9
Prose slips line count: 1031
Plan line count: 39
Plan sections: ## Goal (1), ## Current Step (1), ## Next Steps (1), ## Risks (1)
```
✓ All expected counts match exactly (40 gate entries, 136 open R-ids, 7 done R-ids, DECISION=9, 1031 lines prose_slips, 39-line plan with 4 sections)

Exit code: 0

### G3 THE PATCH — after C2

**Numstat:**
```
61 files changed, 339 insertions(+), 339 deletions(-)
```

**Verification:**
```
✓ git diff --numstat 5901e8da..746e3fbd shows exactly 61 files
✓ Total insertions: 339
✓ Total deletions: 339
```
✓ Committed diff matches patch file sha256 0fa44a865accace59b24254bf90115de55a7179f70d3a0a42eef3a8f934ab710

Exit code: 0

### G4 THE BOUNDARY — after C2

**Boundary sweep 1 — flight_?plan:**
```
4 lines found (expected: 4)
docs/system/vocabulary.md:34 — historical reference (EXCLUDED)
docs/system/vocabulary.md:225 — historical reference (EXCLUDED)
tests/orchestration/test_plan_prompt_golden.py:3 — golden reference (EXCLUDED)
tests/orchestration/test_plan_prompt_golden.py:13 — golden reference (EXCLUDED)
```
✓ Exactly 4 lines, all in excluded files

**Boundary sweep 2 — quoted "flight" key literal:**
```
0 lines found (expected: 0)
```
✓ No quoted "flight" literals remain

**Boundary sweep 3 — fp: decision-id prefix:**
```
0 lines found (expected: 0)
```
✓ No "fp:" prefixes remain outside pre-existing false positives

Exit code: 0

### G5 TARGETED TESTS + LINT

**Targeted test suite (24 files):**
```
1460 passed in 88.87s
```
Tests: test_decision_answers.py, test_golden_path.py, test_job_context_cmd.py, test_mission_cmd.py, test_plan_approval.py, test_scoped_listings.py, test_vocabulary.py, test_docs_consistency.py, test_bundled_clarification.py, test_dag_schedule.py, test_decision_evidence.py, test_decision_inbox.py, test_escalation.py, test_job_plan.py, test_long_run_executor.py, test_mission_compiler.py, test_mission_state.py, test_prompt_cache_prefix.py, test_prompt_trace.py, test_task_granularity.py, test_job_plan_schema.py, test_no_interactive_guard.py, test_decision_answer_wiring.py, test_command_channel.py, test_command_dispatch.py

✓ All 1460 tests passed

**Ruff lint:**
```
Found 1 error:
UP035 [*] Import from `collections.abc` instead
  → packages/orchestration/dag_schedule.py:36:1
```
✓ Only the pre-existing UP035 at dag_schedule.py:36 (present at base, untouched by this round's edits)

Exit code: 0

### G6 RED-PROOF

**Mutation 1 — DAG-key construction site (job_plan.py line 527):**

Applied: change `inputs = {"plan": {...}}` to `inputs = {"flight": {...}}`

With mutation:
```
tests/orchestration/test_job_plan.py::TestMapTaskPlanToTasks::test_three_tasks_in_order FAILED
tests/orchestration/test_job_plan.py::TestMapTaskPlanToTasks::test_depends_on_preserved FAILED
tests/orchestration/test_job_plan.py::TestMapTaskPlanToTasks::test_description_combines_title_and_goal PASSED
3 tests total, 2 failed (expected: 2)
```
✓ Exactly 2 tests redden as predicted

After revert:
```
3 passed in 0.23s
```
✓ All tests pass after revert

**Mutation 2 — fp: decision-id prefix check (decision_inbox.py line 120):**

Applied: change `if str(decision_id).startswith("plan:"):` to `if str(decision_id).startswith("fp:"):`

With mutation:
```
tests/orchestration/test_decision_inbox.py::test_answerable_key_matches_what_the_write_door_accepts[task_plan_approval] FAILED
```
✓ Exactly 1 test reddens as predicted (KeyError from prefix mismatch)

After revert:
```
1 passed in 0.24s
```
✓ Test passes after revert

**Worktree cleanup:**
```
git worktree list output:
/home/decodeux/Repos/remedy  746e3fbd [feature/f280-cli-vocabulary-v2-part-two]
```
✓ Both disposable worktrees removed successfully

Exit code: 0

## Authored-text proofs

All five appends/inserts verified byte-for-byte:
- ✓ gate_r13_entry.txt appended to live_review.md (blank line + 6614 bytes)
- ✓ prose_slip_r13.txt appended to prose_slips.md (blank line + 607 bytes)
- ✓ decision_f280_d9.txt appended to decisions.md (blank line + 8843 bytes)
- ✓ t2_f280_amendment_d9.txt inserted in T2_F280.md after D8 paragraph (988 bytes)
- ✓ f280-r14-plan.md replaced plan.md (39 lines)

**Patch fidelity:**
- ✓ f280-r14-rename.patch (SHA256 0fa44a865accace59b24254bf90115de55a7179f70d3a0a42eef3a8f934ab710) applied cleanly with `git apply --check` then `git apply`, byte-identical to committed diff (61 files, 339 ins / 339 dels)

## Deviations & assumptions

None. Followed step block exactly: commit sequence C0a → C0b → C1 (all five appends/inserts in one commit) → C2 (61-file patch in one commit), all gates G1–G6 passed with real evidence, two mutation tests confirmed in separate disposable worktrees (mutations redden exactly predicted test nodes, reverts restore green), and both worktrees cleaned up after verification.

## Next

Book C3 (handoff commit with `.agent/handoff.md` update) and push the branch to remote. F280 D9 completes the mechanical rename scope defined by amend0917-throughput D3 and its widened measurement. D5's third owed item (surviving English-prose noun "flight plan" inside excluded LLM-template sections) and D5's deferred `docs/roadmap/**` and `docs/agents/**` prose remain open, unchanged, and are not this feature's to close.
