# Handback — F027 Task veto · Round 4

## Session

SESSION 1 of feature F027 · round 4 · rounds so far 4

Roughly a fifth of the session's context budget remained at the point this handback was
written. This round booked round 3's verdict, resolved R-1066, recorded DECISION F027 D4, and
completed T002: every veto files one `replan_proposal` decision (derived straight from the
control files, never stored in `job.json`) offering `replan_follow_up` or
`accept_reduced_scope`; an answer is a create-only control fact; a replan mints and saves an
unplanned follow-up `JobPlan` with no tasks; a run whose every veto is answered completes with
the reduced scope instead of blocking forever; and `remedy decision resolve <job> veto:<id>
--reason <option>` answers from the CLI. New `tests/orchestration/test_veto_proposal.py`, grown
`test_task_veto.py`/`test_task_veto_runner.py`/`test_decision_inbox.py`/`test_decision_cmd.py`,
and a mutation tool proving all thirteen mutations bite on the first sweep.

## Range

Review of c1c366568..HEAD

## Commits

### c6542e3e9 F027 R4 C1: copy round 4 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f027-r4-block.md | +271/-0 | copy of this round's block, verbatim (`shutil.copyfile`) |
| .agent/authored/f027-r4-plan.md | +32/-0 | copy of the plan.md payload |
| .agent/authored/f027-r4-records.diff | +104/-0 | copy of the records.diff payload |

407 insertions by `git show --numstat` — matches the block's stated expectation exactly (block
line count 271 plus 136), under the 500-line cap.

### 3358bc628 F027 R4 C2: book round 3, resolve R-1066, record D4
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +75/-0 | DECISION F027 D4 appended, verbatim from records.diff |
| .agent/live_review.md | +4/-0 | round 3's Gate entry and R-1066's `Done:` paragraph appended |
| .agent/plan.md | +11/-12 | rewritten whole to the plan.md payload |
| .agent/prose_slips.md | +1/-0 | one line appended (F027 round 3's mutation m6 slip) |

75/0 decisions.md, 4/0 live_review.md, 11/12 plan.md, 1/0 prose_slips.md by `git show --numstat`
— matches the block's stated expectation exactly. `git apply --check` on records.diff → exit 0;
the real `git apply` → exit 0.

### 7da286bf6 F027 R4 C3a: the veto answer files (part 1 of 2)
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/task_veto.py | +184/-0 | S1: `VETO_ANSWERS_DIRNAME`, `REPLAN_FOLLOW_UP`, `ACCEPT_REDUCED_SCOPE`, `REPLAN_PROPOSAL_OPTIONS`; the frozen `VetoAnswer` dataclass; `record_veto_answer` (create-only, named by the first 32 hex chars of the request id's sha256, refuses an invalid option or an unsafe request id, answers an existing entry unchanged with `False`); `veto_answers` (keyed by request id, raises on an untrustworthy entry) |

184 insertions by `git show --numstat`, under the 500-line cap.

### 121b65b1d F027 R4 C3b: file a replan proposal for every veto and record its answer (part 2 of 2)
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/veto_proposal.py | +351/-0 | NEW MODULE: `replan_proposal_decisions` (one card per unanswered qualifying veto entry); `answer_replan_proposal` (checks the id, the option, an existing answer, in order; mints the follow-up id before recording the answer, saves the job after — so a repeat call repairs a follow-up save that failed); `build_follow_up_job` (no tasks, state `pending`, copies repo/project, goal names the vetoed task, the reason verbatim and each unreachable task) |
| packages/orchestration/decision_queue.py | +14/-0 | S3: `"replan_proposal"` joins `DECISION_TYPES`; branch 9 extends `list_decisions` with `replan_proposal_decisions(job)`, wrapped like its neighbours and also catching `TaskVetoError` |
| packages/orchestration/decision_evidence.py | +1/-1 | S3: `"replan_proposal"` joins `TRIPLE_REQUIRED_TYPES` |
| packages/orchestration/event_names.py | +1/-0 | S6: `"veto_proposal_answered"` joins `EVENT_NAMES`, in sorted place |
| tests/orchestration/import_reachability_allowlist.txt | +1/-0 | S6: `packages.orchestration.veto_proposal` joins the allowlist, in sorted place |

368 insertions by `git show --numstat`, under the 500-line cap. See Deviations 1: S1/S2/S3
together would have reached 552 insertions, so the bundle was split at S1 (task_veto.py) / S2+S3
(everything else).

### e4cb8293e F027 R4 C4: complete a job whose every veto is answered, and answer from the CLI
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/pingpong_job.py | +60/-17 | S4: the veto terminal reads `task_veto.veto_answers`; when every vetoed task's request id (from `job.metadata["task_vetoes"]`) has an answer, `veto_terminal` records `settled: True` with each task's answered option and falls through to the ordinary completion path (`all_done` now counts `TASK_VETOED` beside applied/skipped/split); otherwise it blocks exactly as before, now naming `settled: False`; a `TaskVetoError` reading the answers blocks with `task_veto_control_error: <detail>` |
| apps/cli/commands/decision.py | +51/-0 | S5: the `veto:` route in `_cmd_decision_resolve` — `--reason` carries the option, actor `cli`; an accept/replan prints the outcome and (for a replan) the follow-up job's id; a refusal fails with the matching code at `fail()`'s default exit code 1 |
| packages/orchestration/run_manifest.py | +7/-3 | S4: `_COMPLETED_WORKED_STATUSES` gains `"vetoed"` for `EXPECT_EXECUTED`, `EXPECT_PRIOR_EPISODE` and `EXPECT_SKIPPED` |

118 insertions by `git show --numstat`, under the 500-line cap.

### e4c2d03e9 F027 R4 C5a: test the replan proposal decision and its answer (part 1 of 3)
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_veto_proposal.py | +401/-0 | NEW FILE: the decision's id/type/severity/summary/payload/evidence; one card per veto, none for an inert or answered one; each refusal (unknown id, unknown request id, invalid option) writing nothing; an accept (answer file, one event, no job); a replan (answer file, one event, exactly one new job, original `job.json` byte-identical); a repeated answer `already_answered` with no second write; the repair of a follow-up job whose save failed; two concurrent answers converging |

401 insertions by `git show --numstat`, under the 500-line cap.

### 05c6fd0e8 F027 R4 C5b: test the answer files, the settled completion and the widened vocabulary pins (part 2 of 3)
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_task_veto.py | +117/-0 | new `TestAnswerFiles` class: the answer file's digest name and content, a repeated record answering the first unchanged, a publication race converging, an invalid option, an unsafe request id, an empty root, keying by request id, an unparsable/unrecognised-option entry raising |
| tests/orchestration/test_task_veto_runner.py | +101/-1 | new `TestSettledCompletion` class: answered-before-the-run completes with the reduced scope (manifest validating); vetoed-but-unanswered still blocks, `settled` false; a blocked veto terminal answered and relaunched completes. The one pre-existing exact-equality `veto_terminal` assertion gained `"settled": False` |
| tests/orchestration/test_decision_inbox.py | +36/-1 | `"replan_proposal"` joins `PRODUCING_DECISION_TYPES` with `_fixture_replan_proposal` in `PRODUCING_FIXTURES`; excluded (with `task_decision`) from the zero-blocked parametrization; a new dedicated test pins its `blocked_count` to the veto's own unreachable count |
| tests/orchestration/test_decision_evidence.py | +1/-1 | THE ONE DECLARED WIDENING (constraint 3): the exact-equality `TRIPLE_REQUIRED_TYPES` pin gains `"replan_proposal"` |

255 insertions by `git show --numstat`, under the 500-line cap.

### b10e4622a F027 R4 C5c: test the CLI route, and the mutation tool (part 3 of 3)
| Path | +/- | Reason |
|---|---|---|
| tests/cli/test_decision_cmd.py | +61/-0 | new `TestDecisionResolveVetoAnswersJSONThroughTheDispatcher` class: an accept, a replan printing the follow-up job's id, and a refusal's exit code (1, matching the `proposal:` route's own) — through the real dispatcher over a real vetoed job. The pre-existing `TestTheTokenVocabularyJoinsTheProduct` pin needed no change: every `fail()` token the new branch uses (`decision_not_found`, `invalid_argument`, `decision_already_answered`) was already in the pinned set |
| .agent/authored/f027-r4-mutations.py | +251/-0 | NEW: the G5 mutation tool, 13 mutations over `task_veto.py`, `veto_proposal.py`, `pingpong_job.py` and `apps/cli/commands/decision.py` |

312 insertions by `git show --numstat`, under the 500-line cap. See Deviations 1: C5 would have
reached 968 insertions as one commit, so it was split into C5a/C5b/C5c.

## External actions

`git worktree add --detach .remedy-wt/f027-r4-mut b10e4622a` — worktree created for the G5 sweep
(exit 0).
`python3 -B .agent/authored/f027-r4-mutations.py .remedy-wt/f027-r4-mut` — run once; caught all
thirteen mutations on the first sweep.
`git worktree remove --force .remedy-wt/f027-r4-mut` (exit 0), `git worktree prune` (exit 0).
`git worktree add --detach .remedy-wt/f027-r4-baseline c1c366568` and later `git worktree remove
--force .remedy-wt/f027-r4-baseline` — a SCRATCH worktree used only to measure the round-start
collect-only counts for G4's accounting (see Verification below); not one of the block's ordered
worktrees, created and removed entirely within this round.
`git push -u origin feature/f027-task-veto` — outcome reported in the final reply, since C5/C6
cannot contain it.
No PR created, no merge, no branch checkout/deletion, no force-push, no stash — none of these ran.

## Verification

BEFORE ANYTHING ELSE:
- `ls .agent/STOP` → `ls: cannot access '.agent/STOP': No such file or directory` (absent, as
  required). `REAL_EXIT=2`.
- `pwd` → `/home/decodeux/Repos/remedy`; `git status --porcelain` → empty; `git branch
  --show-current` → `feature/f027-task-veto`; `git log --oneline -1` → `c1c366568 F027 R3 C6:
  rewrite handoff for round 3`. All three matched.
- Block bytes: measured line count 271, sha256
  `a2a338734bb08be082569b0278220927ce072558fcf25ffaac313315b76cc9cd` — both matched the
  delegation message's two readings exactly.
- `git worktree list` reported as found (the pre-round listing: the primary checkout plus the
  `f015-*`, `f020-*`, `f023-*`, `f024-*`, `f025-*`, `f027-r1-dry`, `f027-r2-dry`, `f027-r3-dry`,
  `f027-r4-dry`, `f284-*` and `job-*` worktrees — unchanged by this round, confirmed identical
  after the two scratch worktrees above were added and removed).

PAYLOADS (measured against the block's table, both matched):
| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 32 | 1207 | 37219603b525f36035e980556dcd98c65236b9603922c98f4c895e6838d062c0 |
| records.diff | 104 | 14004 | 81557e20692f57d5edb14099553dfd1fb80b76543ea6526897ae9f18d77ff64b |

`git apply --check` on records.diff → `REAL_EXIT=0`. The real `git apply` → `REAL_EXIT=0`.

G1 TRANSPORT — each `.agent/authored/f027-r4-*` copy compared byte for byte against its source,
read back with `git show c6542e3e9:<path>`:
- `f027-r4-block.md` == `.remedy-wt/f027-r4/block.md`: equal=True, sha256 matches the delegation
  message's stated hash exactly.
- `f027-r4-plan.md` == payload plan.md: equal=True
- `f027-r4-records.diff` == payload records.diff: equal=True

G2 THE RECORDS — each file's sha256, read with `git show 3358bc628:<path>`, against the
reviewer's table:
| path | bytes | sha256 | match |
|---|---|---|---|
| .agent/live_review.md | 303547 | 058976c45fc7088603912a1ee70fea43ba26b65ad76957403938544ae9e200ee | True |
| .agent/decisions.md | 2173285 | 714abd6ef4574b4528df338336df71aa7455edba90233758b42b4939b500caec | True |
| .agent/prose_slips.md | 368884 | 9a17eb60ce00d4322e3d01bb29505564a46c30232547a6425fe1f10ac65d030c | True |
| .agent/plan.md | 1207 | 37219603b525f36035e980556dcd98c65236b9603922c98f4c895e6838d062c0 | True |

Open finding ids via `open_finding_ids` (scripts/rotate_live_review.py) over the ledger's text at
3358bc628: `[]` — matches the reviewer's reading exactly (empty).

G3 THE CODE:
```
$ python3 -m ruff check packages/orchestration/task_veto.py packages/orchestration/veto_proposal.py packages/orchestration/decision_queue.py packages/orchestration/decision_evidence.py packages/orchestration/event_names.py packages/orchestration/pingpong_job.py packages/orchestration/run_manifest.py apps/cli/commands/decision.py tests/orchestration/test_veto_proposal.py tests/orchestration/test_task_veto.py tests/orchestration/test_task_veto_runner.py tests/orchestration/test_decision_evidence.py tests/orchestration/test_decision_inbox.py tests/cli/test_decision_cmd.py
All checks passed!
REAL_EXIT=0
```
(run at the last code commit, b10e4622a)

```
$ python3 -m apps.cli.main decision resolve --help
 Usage: remedy decision resolve [OPTIONS] JOB_ID DECISION_ID
 ...
╭─ Options ────────────────────────────────────────────────────────────────────╮
│  --reason      Reason text                                                   │
│  --answer      Answer one bundled clarification: --answer q1="use PostgreSQL"│
│                (repeatable)                                                  │
│  --as-mission  When approving: also create a mission for this goal and link  │
│                this job as its initial job                                   │
│  --json        Output as JSON                                                │
│  --help        Show this message and exit.                                   │
╰──────────────────────────────────────────────────────────────────────────────╯
REAL_EXIT=0
```

`ast` reading of `veto_proposal.py`'s imports: `__future__`, `json`, `packages.core.models`,
`packages.orchestration` (the `from ... import task_veto as _tv` form), `packages.orchestration.
data_paths`, `packages.orchestration.decision_evidence`, `packages.orchestration.decision_queue`,
`packages.orchestration.pingpong_job`, `packages.orchestration.run_log`, `typing`. None of
`subprocess`, `threading`, `signal` or `packages.orchestration.long_run_executor` — confirmed.

G4 THE TESTS — serial run in the primary checkout at the last code commit (b10e4622a), real exit
code:
```
$ python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_veto_proposal.py tests/cli/test_decision_answers.py tests/cli/test_decision_cmd.py tests/cli/test_open_decisions_view.py tests/cli/test_plan_approval.py tests/orchestration/test_approval_queue.py tests/orchestration/test_bundled_clarification.py tests/orchestration/test_decision_evidence.py tests/orchestration/test_decision_inbox.py tests/orchestration/test_escalation.py tests/orchestration/test_f018_authority_integration.py tests/orchestration/test_job_digest.py tests/orchestration/test_mission_state.py tests/orchestration/test_proposal_decision.py tests/ui_server/test_live_state.py tests/ui_contracts/test_decision_answer_wiring.py tests/ui_contracts/test_decision_urgency_parity.py tests/orchestration/test_task_veto.py tests/orchestration/test_task_veto_runner.py tests/orchestration/test_task_expectation_status_truth.py tests/orchestration/test_run_manifest.py tests/orchestration/test_run_manifest_zero_call_expectations.py tests/orchestration/test_event_names.py tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_block_lint.py tests/ui_server/test_dashboard_contract.py tests/cli/test_golden_path.py
1329 passed in 136.38s (0:02:16)
REAL_EXIT=0
```
No `SKIPPED` line was printed by `-rs` anywhere in this selection — zero skips.

`--collect-only -q`, per new/grown file, MEASURED against the SAME file at the round's start
(`c1c366568`, read via a scratch worktree `.remedy-wt/f027-r4-baseline`, added and removed
entirely within this round — see External actions):
- `tests/orchestration/test_veto_proposal.py`: 12 collected (NEW file, all 12 new)
- `tests/orchestration/test_task_veto.py`: 129 → 138 (9 new, `TestAnswerFiles`)
- `tests/orchestration/test_task_veto_runner.py`: 13 → 16 (3 new, `TestSettledCompletion`)
- `tests/orchestration/test_decision_inbox.py`: 43 → 46 (3 new: one parametrized case each on
  `test_card_appears_for_each_producing_type` and
  `test_answerable_key_matches_what_the_write_door_accepts`, plus the new dedicated
  `blocked_count` test)
- `tests/orchestration/test_decision_evidence.py`: 125 → 125 (0 new — an assertion changed, no
  test added)
- `tests/cli/test_decision_cmd.py`: 14 → 17 (3 new,
  `TestDecisionResolveVetoAnswersJSONThroughTheDispatcher`)
- `tests/cli/test_golden_path.py`: 42 (unchanged by this round; newly INCLUDED in this round's
  selection, whereas the reviewer's round-3 selection excluded it)

Accounting for the difference from the reviewer's `1257 passed` (same selection, WITHOUT
`test_veto_proposal.py` and WITHOUT `test_golden_path.py`, at `c1c366568`): `1257 + 9 (task_veto
growth) + 3 (task_veto_runner growth) + 3 (decision_inbox growth) + 3 (decision_cmd growth) + 12
(new veto_proposal file) + 42 (golden path, newly in-selection) = 1329` — matches the measured
total exactly.

```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [{"name": "handler_import", "status": "pass", ...}, {"name": "live_review_verdict", "status": "pass", ...}, {"name": "plan_consistency", "status": "pass", ...}, {"name": "relevant_untracked", "status": "pass", ...}, {"name": "repo_root_hygiene", "status": "pass", ...}, {"name": "high_blockers_open", "status": "pass", ...}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
REAL_EXIT=0
```
All six checks read `pass`, `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f027-r4-mut b10e4622a` (exit 0), then
`python3 -B .agent/authored/f027-r4-mutations.py .remedy-wt/f027-r4-mut`:
```
--- control run (unmutated, before) ---
control: exit=0
229 passed in 9.77s
m1 a proposal is derived for an answered veto: exit=1 failed=1 failing_node_ids=['tests/orchestration/test_veto_proposal.py::TestCardPresence::test_no_card_for_an_answered_veto']
restored byte-identical: True
m2 the summary drops the reason: exit=1 failed=1 failing_node_ids=['tests/orchestration/test_veto_proposal.py::TestDecisionShape::test_id_type_severity_summary_payload_and_evidence']
restored byte-identical: True
m3 the options are offered in the other order: exit=1 failed=1 failing_node_ids=['tests/orchestration/test_veto_proposal.py::TestDecisionShape::test_id_type_severity_summary_payload_and_evidence']
restored byte-identical: True
m4 the answer file is published without create_only, so a race overwrites: exit=1 failed=2 failing_node_ids=['tests/orchestration/test_task_veto.py::TestAnswerFiles::test_a_publication_race_converges_on_the_winner', 'tests/orchestration/test_veto_proposal.py::TestConcurrentAnswers::test_two_concurrent_answers_converge_on_the_winner']
restored byte-identical: True
m5 a replan saves no follow-up job: exit=1 failed=3 failing_node_ids=['tests/orchestration/test_veto_proposal.py::TestFollowUpRepair::test_a_repeated_answer_repairs_a_follow_up_job_whose_save_failed', 'tests/orchestration/test_veto_proposal.py::TestRepeatedAnswer::test_already_answered_writes_nothing_new', 'tests/orchestration/test_veto_proposal.py::TestReplan::test_creates_exactly_one_new_job_and_leaves_the_original_untouched']
restored byte-identical: True
m6 a replan also sets the original job completed and saves it: exit=1 failed=2 failing_node_ids=['tests/orchestration/test_veto_proposal.py::TestRepeatedAnswer::test_already_answered_writes_nothing_new', 'tests/orchestration/test_veto_proposal.py::TestReplan::test_creates_exactly_one_new_job_and_leaves_the_original_untouched']
restored byte-identical: True
m7 the follow-up job's goal leaves out the reason: exit=1 failed=1 failing_node_ids=['tests/orchestration/test_veto_proposal.py::TestReplan::test_creates_exactly_one_new_job_and_leaves_the_original_untouched']
restored byte-identical: True
m8 a repeated answer writes a second event: exit=1 failed=1 failing_node_ids=['tests/orchestration/test_veto_proposal.py::TestRepeatedAnswer::test_already_answered_writes_nothing_new']
restored byte-identical: True
m9 an option outside the two is recorded: exit=1 failed=2 failing_node_ids=['tests/cli/test_decision_cmd.py::TestDecisionResolveVetoAnswersJSONThroughTheDispatcher::test_a_refusals_exit_code_matches_the_proposal_routes_own', 'tests/orchestration/test_veto_proposal.py::TestRefusals::test_an_option_outside_the_two_is_invalid_option']
restored byte-identical: True
m10 the settled completion ignores the answers and always completes: exit=1 failed=10 failing_node_ids=['tests/orchestration/test_task_veto_runner.py::TestBlockThenVetoThenRelaunch::test_the_independent_task_returns_to_pending_and_runs', 'tests/orchestration/test_task_veto_runner.py::TestDiamondVetoBeforeTheRun::test_b_vetoed_before_the_run', 'tests/orchestration/test_task_veto_runner.py::TestEveryTaskVetoed::test_nothing_is_dispatched_and_the_error_names_them_all', 'tests/orchestration/test_task_veto_runner.py::TestGitInFlightVetoRestoresTheWorkspace::test_the_partial_file_is_gone_and_restored_is_true', 'tests/orchestration/test_task_veto_runner.py::TestGitWorktreeVetoRestoresTheWorkspace::test_a_veto_and_relaunch_removes_the_blocked_attempts_file', 'tests/orchestration/test_task_veto_runner.py::TestInFlightVetoOfTheRunningTask::test_bs_build_finishes_its_review_never_runs_and_the_run_continues', 'tests/orchestration/test_task_veto_runner.py::TestLegacyJobFileVeto::test_the_second_of_three_vetoed', 'tests/orchestration/test_task_veto_runner.py::TestSettledCompletion::test_a_blocked_veto_terminal_answered_and_relaunched_completes', 'tests/orchestration/test_task_veto_runner.py::TestSettledCompletion::test_vetoed_but_unanswered_still_blocks_settled_false', 'tests/orchestration/test_task_veto_runner.py::TestVetoDuringTheRun::test_a_veto_recorded_while_the_prior_task_runs_stops_the_next_one']
restored byte-identical: True
m11 the settled completion never completes: exit=1 failed=2 failing_node_ids=['tests/orchestration/test_task_veto_runner.py::TestSettledCompletion::test_a_blocked_veto_terminal_answered_and_relaunched_completes', 'tests/orchestration/test_task_veto_runner.py::TestSettledCompletion::test_answered_before_the_run_completes_with_the_reduced_scope']
restored byte-identical: True
m12 all_done leaves out TASK_VETOED, so a settled run ends as it began: exit=1 failed=2 failing_node_ids=['tests/orchestration/test_task_veto_runner.py::TestSettledCompletion::test_a_blocked_veto_terminal_answered_and_relaunched_completes', 'tests/orchestration/test_task_veto_runner.py::TestSettledCompletion::test_answered_before_the_run_completes_with_the_reduced_scope']
restored byte-identical: True
m13 the CLI route answers with --answer instead of --reason: exit=1 failed=2 failing_node_ids=['tests/cli/test_decision_cmd.py::TestDecisionResolveVetoAnswersJSONThroughTheDispatcher::test_a_replan_prints_the_follow_up_jobs_id', 'tests/cli/test_decision_cmd.py::TestDecisionResolveVetoAnswersJSONThroughTheDispatcher::test_an_accept_answers_the_envelope']
restored byte-identical: True
--- control run (unmutated, after) ---
control: exit=0
229 passed in 7.12s
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
REAL_EXIT=0. Every one of the 13 mutations was red with at least one failing node on this FIRST
sweep — none stayed green, no second sweep or repair test was needed. Every restoration was
byte-identical.

`git worktree remove --force .remedy-wt/f027-r4-mut` → exit 0. `git worktree prune` → exit 0.
`git worktree list` afterward: identical to the pre-round listing at step 4 — nothing added or
left behind.

CONSTRAINT 3 — round path set: `git diff --name-only c1c366568` (before C6) named exactly:
`.agent/authored/f027-r4-block.md`, `.agent/authored/f027-r4-mutations.py`,
`.agent/authored/f027-r4-plan.md`, `.agent/authored/f027-r4-records.diff`, `.agent/decisions.md`,
`.agent/live_review.md`, `.agent/plan.md`, `.agent/prose_slips.md`,
`apps/cli/commands/decision.py`, `packages/orchestration/decision_evidence.py`,
`packages/orchestration/decision_queue.py`, `packages/orchestration/event_names.py`,
`packages/orchestration/pingpong_job.py`, `packages/orchestration/run_manifest.py`,
`packages/orchestration/task_veto.py`, `packages/orchestration/veto_proposal.py`,
`tests/cli/test_decision_cmd.py`, `tests/orchestration/import_reachability_allowlist.txt`,
`tests/orchestration/test_decision_evidence.py`, `tests/orchestration/test_decision_inbox.py`,
`tests/orchestration/test_task_veto.py`, `tests/orchestration/test_task_veto_runner.py`,
`tests/orchestration/test_veto_proposal.py` — the block's whole named set, plus the ONE declared
widening (`test_decision_evidence.py`'s exact-equality pin), nothing extra (this file,
`.agent/handoff.md`, is added by C6 itself). None of the forbidden paths (`ui_server.py`,
`decision_inbox.py` production module, `long_run_executor.py`, `apps/cli/command_catalog.py`,
`apps/ui/`, `docs/`, `.agent/context.md`, `.agent/candidates.md`,
`.agent/operator_questions.md`) were touched.

G6 TREE AND PUSH — real readings reported in the final reply (this file cannot contain them,
since they are measured AFTER this commit).

## Authored-text proofs

Every `.agent/authored/f027-r4-*` copy was compared disk-to-disk against its committed source
and matched byte for byte (see G1 above): the block copy, the plan payload copy and the
records.diff payload copy. `f027-r4-mutations.py` is the worker's own tool, not a
reviewer-authored payload — no fidelity proof applies to it.

## Deviations & assumptions

1. Two of the block's named commits were split at the 500-insertion cap: C3 (S1+S2+S3 together
   would have reached 552 insertions) into C3a (S1, `task_veto.py`, 184) and C3b (S2+S3+guards,
   368); C5 (THE TESTS AND THE MUTATION TOOL together would have reached 968 insertions) into
   C5a (the new `test_veto_proposal.py`, 401), C5b (the grown `test_task_veto.py` /
   `test_task_veto_runner.py` / `test_decision_inbox.py` plus the one declared widening in
   `test_decision_evidence.py`, 255) and C5c (the grown `test_decision_cmd.py` plus the mutation
   tool, 312). Every part stayed under the cap.
2. The ONE declared widening constraint 3 allows was used: `tests/orchestration/
   test_decision_evidence.py`'s exact-equality `TRIPLE_REQUIRED_TYPES` pin gained
   `"replan_proposal"` — the type S3 itself adds to the production constant of the same name.
3. Where S1 to S6 left a choice open, the following were made:
   a. "The vetoed task's title and goal" (S2, S2's THE TESTS): `TaskEntry.title` ALREADY carries
      both — `job_plan.map_task_plan_to_tasks` titles a task `f"{pt.title}: {pt.goal}"` — so the
      follow-up job's prose and the decision's `task_title` payload key both read `task.title`
      alone rather than reconstructing a separate "goal" field that does not exist on the record.
   b. The decision's payload key names beyond the ones S2 names explicitly (`options`, `task_id`,
      `request_id`) were chosen as `task_title`, `reason`, `actor`, `requested_at` and
      `unreachable_task_ids` — plain, English-spelled, and matching the reading style
      `decision_queue.py`'s other seven branches already use for their own extra payload keys.
   c. `job.metadata["veto_terminal"]`'s settled shape adds a `"settled": bool` key to both
      branches and, for the settled case only, an `"answers": {task_id: option}` dict for "each
      task's answered option" — the block names the two required facts (`settled` and each
      answer) but not their exact key shape. The pre-existing exact-equality assertion in
      `test_task_veto_runner.py` (the not-settled diamond case) was updated in the same commit
      that changed the production shape, adding `"settled": False` to its expected dict.
   d. THE CLI REFUSAL EXIT CODE (S5 asks it named here): every refusal the `veto:` route can
      answer (`decision_not_found` for `unknown_decision`, `invalid_argument` for
      `invalid_option`, `decision_already_answered` for `already_answered`) reaches `fail()`
      with no `exit_code` override, so it exits **1** — the SAME default every refusal the
      `proposal:` route gives (`proposed_task_not_found`, `invalid_argument`,
      `proposed_task_invalid_state`, `proposed_task_operation_failed`) already exits at, since
      none of those calls override it either. No new exit code was needed.
   e. The CLI's print text for a successful answer (the follow-up job's id and the "plan it"
      command line for a replan; the "completes at its next run" sentence and the relaunch
      command line for an accept) is the worker's own wording within S5's description.
4. No other deviation from the block's ordered commit sequence, specification or constraints.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | |
| C3a | deviated | C3 split into C3a/C3b at the 500-line cap — see Deviations 1 |
| C3b | deviated | see C3a |
| C4 | done | |
| C5a | deviated | C5 split into C5a/C5b/C5c at the 500-line cap — see Deviations 1 |
| C5b | deviated | see C5a |
| C5c | deviated | see C5a |
| G1 TRANSPORT | done | |
| G2 THE RECORDS | done | |
| G3 THE CODE | done | |
| G4 THE TESTS | done | |
| G5 THE RED PROOFS | done | all 13 mutations caught on the first sweep, no repair needed |
| G6 TREE AND PUSH | done | reported in the final reply, not this file, per the block |

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 4, then the channel
commands — `job.veto-task` in the catalog, the CLI and the write door, and the door's answer of
a replan proposal. Open findings: 0. Operator questions: 5.
