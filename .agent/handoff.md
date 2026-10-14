# Handback — F308 round 2 — DECISION F308 D2, T001 to T003, and amendment 1's status-vocabulary repair

## Session

SESSION 1 of feature F308 · round 2 · rounds so far 2

Context self-assessment: C1 to C3 landed clean on the first attempt; gate 3 then caught a real
defect (a refusal message's words split across two f-string lines, so they no longer appeared
contiguously on disk) that was repaired by resetting to C1 and re-splitting the combined tree back
into corrected C2/C3 commits before anything was pushed, and separately a genuine pre-existing-test
conflict that the block did not anticipate, which the operator resolved with amendment 1; context
held comfortably throughout both repairs.

Fortschritt: ~65 % (T001 to T003 landed · the built-state record and the closure open) — Schätzung

## Range

Review of `f06b5c205`..`25aa71329`

## Commits

### f7aba0269 F308 R2 C1: book round 1, DECISION F308 D2 and the plan, save the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f308-r2.md` | +217/-0 | NEW FILE, byte copy of `block.md` (217 lines, sha256 `300aa26744022658fe0d11d01ed3cd2b6055c86566b0ae7b0db3447117c5f4d8`) |
| `.agent/decisions.md` | +12/-0 | DECISION F308 D2 appended, byte-identical to `dry-decisions.md` |
| `.agent/live_review.md` | +2/-0 | the F308 round 1 PASS verdict booked at the end, byte-identical to `dry-live_review.md` |
| `.agent/plan.md` | +6/-7 | rewritten for round 2 (Goal cites DECISION D2, Current Step and Next Steps updated), byte-identical to `dry-plan.md` |

### df93b18a2 F308 R2 C2: the run records its splits and the run manifest accepts them (T001, T002)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/run_task_list.py` | +223/-17 | `TASK_SPLITS_METADATA_KEY`/`TASK_SPLIT_FIELDS`, `record_task_split`, `task_ids_after_splits`, `episode_task_splits`, `checked_episode_task_list`, `task_split_problems`, `decode_task_splits_v1` added; `declared_job_input_task_ids` renamed `job_input_task_ids`, with a new `declared_job_input_task_ids` wrapper applying the manifest's own splits; `expect_task_without_run` and `task_list_chain_problems` updated per DECISION F308 D2; `split_task_over_class_cap` now calls `record_task_split` |
| `packages/orchestration/run_manifest.py` | +20/-25 | `VALID_TASK_STATUSES`, and the `EXPECT_SKIPPED` entry of `_TASK_EXPECTATION_ALLOWED_STATUSES`/`_COMPLETED_WORKED_STATUSES`, gain `"split"`; `RunManifestV1` gains `task_splits`; `to_json`, `decode_run_manifest_v1`, `_bind_artifact_refs` carry it; `build_run_manifest`'s inline F7 check becomes one call to `checked_episode_task_list`; `validate_run_manifest` extends its problems with `task_split_problems` |
| `docs/system/structure-ledger-v1.md` | +2/-2 | `run_manifest.py` file row 6212→6207; `_collect_calls` row moved to restore the table's descending order (a leftover from round 1) |
| `tests/test_structure_ratchet.py` | +1/-1 | `MAX_FILE_LINES` 73654→73649 |

### dc08a2ab2 F308 R2 C3: the proof through the real split path and the refusals (T003)

| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_job_task_runner.py` | +80/-0 | `TestClassBudgetCannotFitEscalation` gains two tests: a split job's run manifest names the split (`task_splits`, the expectation, the job's own metadata); the same job paused by `max_tasks` and resumed keeps a valid chain (`validate_index_and_tree == []`) |
| `tests/orchestration/test_run_manifest_call_task_binding.py` | +70/-0 | new class `TestASplitTheRunRecorded`: a recorded split finalizes and is named in the manifest; the same parts with no split record are refused ("no longer matches"); a split whose parent is not recorded `split` is refused; a split recorded for another episode is refused |
| `tests/orchestration/test_run_manifest_task_history_chain.py` | +20/-0 | `TestTheTaskListIsImmutable` gains two tests: a later episode may declare exactly the split the earlier one left; a later episode that declares less than the whole split is refused ("immutable across a job's episodes") |
| `tests/orchestration/test_run_task_list.py` | +144/-0 | NEW FILE (named after the module it covers): `task_ids_after_splits` on a split, two splits in order, and each problem of D2 (3); `decode_task_splits_v1` on a good list, a missing key, an extra key, a wrong type; manifest encoding with and without `task_splits`; `task_split_problems` on an episode mismatch and a wrongly-recorded parent status — 17 tests |

### 25aa71329 F308 R2 C3b: the closed status matrix and the job record's vocabulary name split (amendment 1)

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f308-r2-amend1.md` | +23/-0 | NEW FILE, byte copy of `block-amend1.md` (23 lines, sha256 `447e608a4cdcfc89057bb543e7a1fc1365052eecef56b144f10d04c9efa0b64c`) |
| `.agent/prose_slips.md` | +1/-0 | amendment's prose-slip entry appended, byte-identical to `dry-prose_slips.md` |
| `tests/orchestration/test_task_expectation_status_truth.py` | +3/-3 | per amendment 1, the only existing-test edit this round: `_ALLOWED[EXPECT_SKIPPED]` gains `"split"`; `test_the_status_vocabulary_matches_the_jobplan`'s set gains `PJ.TASK_SPLIT` after `PJ.TASK_VETOED`; `test_the_exhaustive_matrix`'s docstring "All 42 pairs" becomes "Every pair" (48 pairs with eight statuses) |

### (this commit) F308 R2 C4: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | full rewrite per `docs/agents/handback_template.md` |

## External actions

- No worktree added or removed (beyond the pre-existing `.remedy-wt/f308-r2-worker/` scratch
  directory the block told the worker to create for throwaway scripts; nothing under it is
  tracked or committed).
- No `gh pr merge`, `gh pr edit`, `gh pr create` (the block orders no PR this round).
- No branch created beyond the one already checked out.
- Push (`git push origin feature/f308-run-manifest-task-split`) runs after this commit; its
  outcome is reported in the session's final reply only, per the write-once rule — it did not
  exist when this file was written.

## Verification

Preconditions confirmed before C1: `git branch --show-current` read
`feature/f308-run-manifest-task-split`; `git rev-parse HEAD` read
`f06b5c2053beb9fcdc9c0bcf592bc6402bb28769`; the tree was clean. `block.md` was verified first:
217 lines, sha256 `300aa26744022658fe0d11d01ed3cd2b6055c86566b0ae7b0db3447117c5f4d8` — matches the
digest given in the prompt that delivered it. `verify.py`, `run_selection.py` and `selection.txt`
were each checked by `sha256sum` against the digests given in the prompt before any use; all three
matched.

C1: the block and the three `dry-*` files were copied, `cmp` printed nothing for each pair, and
`git diff --cached --numstat` named exactly the four paths the commit's own table above lists.

C2–C3: each commit's diff was read in full (`git diff --cached`) before committing, checked
against DECISION F308 D2 clause by clause (the record, the manifest field, the list arithmetic,
the F7 check, the status, the validator, the chain, the room) and against a direct read of every
named production function beforehand; ruff was run over every file the block names after each
edit, `All checks passed!` every time; `tests/test_structure_ratchet.py` and the directly touched
test files were run after each commit, all green, before the gates.

Gate 1 (after C3, before discovering the amendment's need): `git status --porcelain` — empty.
`python3 /home/decodeux/Repos/remedy/.remedy-wt/f308-r2/prep/verify.py /home/decodeux/Repos/remedy`
— every line `True`, last line `ALL True` (re-run after the C2/C3 re-split and again after C3b,
with the same result both times, confirmed against the SHAs current at each point).

Gate 2 (after C3, and again confirmed on the amended file after C3b):
`python3 -m ruff check packages/orchestration/run_task_list.py
packages/orchestration/run_manifest.py tests/test_structure_ratchet.py
tests/orchestration/test_run_task_list.py
tests/orchestration/test_run_manifest_call_task_binding.py
tests/orchestration/test_job_task_runner.py
tests/orchestration/test_run_manifest_task_history_chain.py` — exit 0, `All checks passed!`.
`python3 -m ruff check tests/orchestration/test_task_expectation_status_truth.py` (the amended
file) — exit 0, `All checks passed!`.

Gate 3, first run (after C3, before the amendment) — RED:
```
FAILED tests/orchestration/test_task_expectation_status_truth.py::TestEveryPairFollowsOneClosedMatrix::test_the_exhaustive_matrix[skipped-split]
FAILED tests/orchestration/test_task_expectation_status_truth.py::TestTheInputsThemselvesAreClosed::test_the_status_vocabulary_matches_the_jobplan
192 paths
2 failed, 7279 passed, 5 skipped in 88.60s (0:01:28)
exit 1
```
This is the exact pre-existing-test conflict amendment 1 names: that file's own closed-status
matrix and its JobPlan-vocabulary assertion predate DECISION F308 D2's `"split"` addition to
`VALID_TASK_STATUSES`, which T001/T002 require. The session stopped at this point (no C4, no
push) and reported the blocker, per the block's own instruction for exactly this situation; the
operator then issued amendment 1, applied above as C3b.

Gate 3, re-run after C3b — GREEN: `python3
/home/decodeux/Repos/remedy/.remedy-wt/f308-r2/prep/run_selection.py /home/decodeux/Repos/remedy
/home/decodeux/Repos/remedy/.remedy-wt/f308-r2-worker/selection-output.txt` — exit 0. Paths:
`192 paths`. Summary: `7281 passed, 5 skipped in 89.31s (0:01:29)`. No FAILED, ERROR or
`process(es) behind` line. Every SKIPPED line:
```
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
SKIPPED [1] tests/regression/test_f293_acceptance.py:191: main holds F293, so its own changes are history
SKIPPED [1] tests/regression/test_f294_acceptance.py:73: main holds F294, so its own changes are history
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
```

Gate 4: `python3 -m apps.cli.main integrity check --json` — exit 0:
```
{"check_count": 6, "checks": [{"message": "handlers=188", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
Six checks, all `pass`; `"fail_count": 0`.

Gate 5: `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
— exit 0, list `['R-1246', 'R-1252', 'R-1276', 'R-1277', ..., 'R-1313']` (R-1246, R-1252, then
R-1276 to R-1313 in order), length 40.

Gate 6: each test C3 added, cross-referenced against gate 3's re-run output above — none of the
25 node ids below appears among gate 3's FAILED/ERROR lines (there are none), and the summary's
`7281 passed` with zero failed proves every one of them passed. A supplementary `-v` run over
exactly these 25 node ids, serially, confirmed it explicitly:
```
tests/orchestration/test_run_task_list.py::TestTaskIdsAfterSplits::test_a_single_split_inserts_its_parts_after_the_parent PASSED
tests/orchestration/test_run_task_list.py::TestTaskIdsAfterSplits::test_two_splits_apply_in_order PASSED
tests/orchestration/test_run_task_list.py::TestTaskIdsAfterSplits::test_a_parent_not_in_the_list_is_a_problem PASSED
tests/orchestration/test_run_task_list.py::TestTaskIdsAfterSplits::test_a_parent_declared_twice_is_a_problem PASSED
tests/orchestration/test_run_task_list.py::TestTaskIdsAfterSplits::test_a_parent_already_split_is_a_problem PASSED
tests/orchestration/test_run_task_list.py::TestTaskIdsAfterSplits::test_empty_parts_are_a_problem PASSED
tests/orchestration/test_run_task_list.py::TestTaskIdsAfterSplits::test_repeated_parts_are_a_problem PASSED
tests/orchestration/test_run_task_list.py::TestTaskIdsAfterSplits::test_parts_already_in_the_list_are_a_problem PASSED
tests/orchestration/test_run_task_list.py::TestTaskIdsAfterSplits::test_a_malformed_split_is_a_problem PASSED
tests/orchestration/test_run_task_list.py::TestDecodeTaskSplitsV1::test_a_good_list_decodes PASSED
tests/orchestration/test_run_task_list.py::TestDecodeTaskSplitsV1::test_a_missing_key_raises PASSED
tests/orchestration/test_run_task_list.py::TestDecodeTaskSplitsV1::test_an_extra_key_raises PASSED
tests/orchestration/test_run_task_list.py::TestDecodeTaskSplitsV1::test_a_wrong_type_raises PASSED
tests/orchestration/test_run_task_list.py::TestManifestEncodingOfTaskSplits::test_a_manifest_without_splits_encodes_with_no_task_splits_key PASSED
tests/orchestration/test_run_task_list.py::TestManifestEncodingOfTaskSplits::test_a_manifest_with_a_split_round_trips_through_the_strict_decoder PASSED
tests/orchestration/test_run_task_list.py::TestTaskSplitProblems::test_an_episode_mismatch_is_a_problem PASSED
tests/orchestration/test_run_task_list.py::TestTaskSplitProblems::test_a_parent_recorded_with_another_status_is_a_problem PASSED
tests/orchestration/test_job_task_runner.py::TestClassBudgetCannotFitEscalation::test_a_split_job_writes_its_run_manifest_naming_the_split PASSED
tests/orchestration/test_job_task_runner.py::TestClassBudgetCannotFitEscalation::test_a_split_job_paused_by_its_task_cap_and_resumed_keeps_a_valid_chain PASSED
tests/orchestration/test_run_manifest_call_task_binding.py::TestASplitTheRunRecorded::test_a_recorded_split_finalizes_and_the_manifest_names_it PASSED
tests/orchestration/test_run_manifest_call_task_binding.py::TestASplitTheRunRecorded::test_the_same_parts_with_no_split_record_are_refused PASSED
tests/orchestration/test_run_manifest_call_task_binding.py::TestASplitTheRunRecorded::test_a_split_record_whose_parent_is_not_recorded_split_is_refused PASSED
tests/orchestration/test_run_manifest_call_task_binding.py::TestASplitTheRunRecorded::test_a_split_record_of_another_episode_is_refused PASSED
tests/orchestration/test_run_manifest_task_history_chain.py::TestTheTaskListIsImmutable::test_a_later_episode_may_declare_the_split_the_earlier_one_left PASSED
tests/orchestration/test_run_manifest_task_history_chain.py::TestTheTaskListIsImmutable::test_a_later_episode_must_declare_the_whole_split PASSED
```
25 passed in 2.06s.

## Authored-text proofs

- `.agent/authored/f308-r2.md` against `block.md`: byte-equal, 217 lines, sha256
  `300aa26744022658fe0d11d01ed3cd2b6055c86566b0ae7b0db3447117c5f4d8`.
- `.agent/live_review.md` (C1) against `dry-live_review.md`: byte-equal.
- `.agent/decisions.md` (C1) against `dry-decisions.md`: byte-equal.
- `.agent/plan.md` (C1) against `dry-plan.md`: byte-equal.
- `.agent/authored/f308-r2-amend1.md` against `block-amend1.md`: byte-equal, 23 lines, sha256
  `447e608a4cdcfc89057bb543e7a1fc1365052eecef56b144f10d04c9efa0b64c`.
- `.agent/prose_slips.md` (C3b) against `dry-prose_slips.md`: byte-equal.
- C2, C3 and C3b's production/test edits wrote no prepared reviewer-authored text beyond the
  files above (the code and tests were the worker's own, written from DECISION F308 D2 and
  amendment 1); nothing further to compare there.

## Deviations & assumptions

1. C2, as first committed, left `task_list_chain_problems`'s refusal message with the words
   "immutable " ending one f-string line and "across a job's episodes" starting the next, so the
   contiguous phrase `verify.py`'s gate 1 checks for no longer appeared in the file's raw bytes
   (it only joins at runtime, after Python concatenates the adjacent literals). Nothing had been
   pushed, so rather than amend a committed commit, the tree was reset with `git reset --soft` to
   C1 and the combined C2+C3 changes (with the one-line wording fix applied) were re-split back
   into two commits with their original messages and file sets, reproducing C2 and C3 exactly as
   originally intended but with the words on one line. The replacement SHAs are the ones in the
   Commits section above; the first (buggy) C2/C3 pair never left this checkout.
2. While attempting to diff against BASE for an unrelated check, `git stash` (a no-op, nothing
   local to stash) was followed by `git stash pop`, which popped an unrelated leftover stash entry
   from a prior, different F277 session and produced a merge conflict in `.agent/plan.md` and
   `.agent/live_review.md`. This was not resolved as a merge: `git checkout HEAD -- .agent/plan.md
   .agent/live_review.md` discarded the conflict markers, and `git stash list` confirmed
   afterward that the F277 entry (and all other pre-existing entries) remained in the stash,
   untouched and undropped. No data was lost; this session's own tree was unaffected once
   reverted. Per the coordinator's explicit instruction this round, no further stash command was
   run.
3. The round stopped once, exactly as the block's own constraint ordered: gate 3's first run (see
   Verification) found two pre-existing tests red for a reason outside this round's named paths,
   and the only repair available edited an existing test — the block's named stop condition. No
   C4 was written and nothing was pushed at that point; the operator's amendment 1 then
   authorized exactly the two edits (three statement-level changes) in
   `tests/orchestration/test_task_expectation_status_truth.py`, applied as C3b, and the round
   continued from there per the amendment's own instruction (gate 3 again, then gates 4–6, then
   C4).

No other departure from the block's ordered commit sequence occurred.

## For the operator, in plain sentences

This round wrote down, as a decision, exactly how Remedy remembers a task that got split into
smaller pieces while a job was running, and taught the job's run record to accept that split
instead of refusing it as if someone had edited the task list by hand. A real job that splits one
task now finishes with a written, valid record naming the split, and the same is true when the
split job is paused partway through and continued later. Partway through this round, one existing
check elsewhere in the test suite turned out to assume the very thing this change was correcting,
so the session stopped and reported it rather than quietly reshaping that check itself; the
operator then confirmed the two small, specific edits that check needed and the round finished
from there. Every test that existed before this round and was not named by that one correction is
still passing, by the same count as before.

## Next

1. Phase 1 rule 1: `.agent/STOP` — absent at this handoff.
2. The Open PR Gate, which runs at the start of the next session.
3. Booking round 2's verdict in the next round's first commit.
4. The built-state record.
5. The closure sequence.

Operator questions open: 0.
Open findings: 40 (R-1252 owned by F308, the rest by F307).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | re-split after a wording-contiguity fix (deviation 1); final SHA `df93b18a2` |
| C3 | done | re-split alongside C2 (deviation 1); final SHA `dc08a2ab2` |
| C3b | done | amendment 1 applied exactly: the two `_ALLOWED`/vocabulary edits and the docstring word |
| C4 | done | this handback |
| Gate 1 | done | `git status --porcelain` empty; `verify.py` all `True`, `ALL True` |
| Gate 2 | done | `All checks passed!`, on the round's files and on the amended file |
| Gate 3 | done | red once (2 failed, the pre-existing-test conflict), green after C3b: exit 0, 192 paths, 7281 passed, 5 skipped |
| Gate 4 | done | exit 0, six checks `pass`, `fail_count` 0 |
| Gate 5 | done | open set is R-1246, R-1252, R-1276 to R-1313, length 40 |
| Gate 6 | done | all 25 tests C3 added found passing in gate 3's output, confirmed individually |
| Push | pending | runs after this commit; outcome reported in the session's final reply only |
