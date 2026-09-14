── STEP T003 — F275 — ROUND 105 ──
Goal: Repair `R-0887` and `R-0888`. Book round 104's verdict; write the four production repairs
of SPEC P; apply slice TESTS105; red-prove each repair; run the full suite once, which must
read exit 0.

Base commit: `675dfcda`. Round type: SPLIT. Amendment amend0914-f275-sprint in
`docs/agents/self_drive_protocol.md` governs the suite run; read that paragraph first.

THE FRAME RULE, per item 37 of §3, stated as the property MEASURED over the final bytes: NO LINE
of this block outside slice TESTS105 is a run of a single repeated character, and every
box-drawing rule inside the STEP and SLICE header lines is exactly two characters long. Slice
TESTS105 is a unified diff, whose blank context lines are one space, and it is proved by its
digest rather than by eye.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f275-r105.md`, the block as received
C0b `.agent/last_block.md`, the block as received
C1 THE BOOKKEEPING COMMIT: `.agent/plan.md` gets slice PLAN105 as a full replacement;
   `.agent/live_review.md` gets slice RECORD105 appended; `.agent/prose_slips.md` gets slice
   SLIP105 appended
C2 SPEC P, the four production repairs
C3 slice TESTS105 applied, per SPEC T
C4 `.agent/authored/f275-r105-suite.txt`, per SPEC S
C5 `.agent/handoff.md`, the handback

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. No `Landed:` or `Done:` line is
written: the handback names the commit that repairs `R-0887` and `R-0888`.

## Change — exactly these paths and no others

The Bundle's `.agent/` paths; at C2 the four files SPEC P names; at C3 the four test files
slice TESTS105 names.

## SPEC P — the production repairs, written by the worker

P1 `packages/orchestration/ui_server.py`, `_build_dashboard`: the returned payload gains the
key `prompt_trace`, right after `phases`, whose value is `_build_prompt_trace` over the
directory `_resolve_evidence_dir` returns for the job's `job_id` as a string.
P2 `packages/orchestration/reviewer.py`, `run_reviewer`: the context's `job_name` is the job's
`job_title`, as a string, cut to 80 characters, and `""` for an object with no `job_title`.
P3 `packages/orchestration/test_failure_artifact.py`, `build_test_failure_artifact`: the
artifact's `job_id` is the job's `job_id` as a string, and `""` for an object with none.
P4 `packages/orchestration/mission_state.py`, `assert_verify_first`: both refusal messages
quote the task's `title` where they quote its `description`, keeping the `'?'` fallback.

## SPEC T — the tests, at C3

Write slice TESTS105's bytes to scratch and, from the repository root, run `git apply --check`
on that file and then `git apply`. No other edit.

## SPEC S — the suite, once, after the red-proofs and before C4

The round's FIRST AND ONLY full-suite run, from the primary checkout's root, serially:
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, with
`PYTHONPATH`, `REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed and `PYTHONDONTWRITEBYTECODE=1`,
stdout and stderr saved under `.remedy-wt/r105w/`. A bad node is the text after a line-initial
`FAILED ` or `ERROR ` up to the first ` - ` or the line's end. The transcript file holds: line 1
`EXIT=<pytest's return code>`; line 2 the run's last output line with its leading and trailing
`=` and spaces stripped; then every distinct bad node, sorted, one per line; nothing after the
last line's newline.

## Constraints

1. NO SLICE IS EDITED. PLAN105, RECORD105, SLIP105 and TESTS105 are used byte for byte; a
   discrepancy is DECLARED, never repaired.
2. READ `.agent/STOP` before C0a, before C2 and before C5, with real exit codes. If it appears,
   finish the commit in hand, write the handback and end.
3. No `.py` file under `.agent/`; scratch under `.remedy-wt/r105w/`, uncommitted, every scratch
   output path absolute. The reviewer's `.remedy-wt/r101/` is not opened.
4. The appends at C1 have a ZERO deletion column. Every commit stays under 500 insertions,
   counted per commit before it is made.
5. No `gh`, no `remedy`, no pull request, no branch created or deleted, no merge, NEVER a
   force-push, no history rewrite. Push after C1, C3, C4 and C5.
6. THE ONE WORKTREE is G3's, `git worktree add --detach` at C3 under `.remedy-wt/r105w/`,
   removed without `--force` and pruned before the suite runs.
7. THE BLOCK'S OWN SIZE, measured on its final bytes: 297 lines TOTAL and 161 lines of
   PROSE, against the caps of 490 and 400.
8. GATE ORDER. G1 runs at C1. G2 runs after C3. G3 runs after G2 and before the suite. G4 runs
   after the suite, with its committed-transcript reading at C4. G5 runs after C4 and before C5.
   No gate runs after C5; C5's own numbers are the reviewer's.
9. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and
   no subject carries a leading-slash token or an absolute path.

## Done when — the gates, each run for real and its exit code recorded

G1 TRANSPORT AND BOOKKEEPING, at C1. The sha256 of `.agent/authored/f275-r105.md` at C0a equals
the block digest received, and `.agent/last_block.md` at C0b is byte-identical to it. Extract
the slices by their markers, report how many were FOUND, and check each against its
BEGIN-marker sha256. `.agent/plan.md` at C1 is byte-identical to PLAN105, with at most 50 lines,
one `## Goal` and one `## Next Steps`. For each append, the blob `git show 675dfcda:<path>`
followed by the slice equals the file at C1; the blobs' lengths at `675dfcda` are 1185844 bytes
for `.agent/live_review.md` and 306668 for `.agent/prose_slips.md`. Lines matching
`^Gate: F\d+ R\d+ — ` read 126 at `675dfcda` and 127 at C1, with `Gate: F275 R104 — ` once. The
open set BY DISTINCT ID, the ids of `^- R-\d{4} — ` paragraphs minus the ids of `^Done: R-\d{4}`
lines, reads 91 at `675dfcda` and at C1 with identical membership.

G2 THE CODE, after C3. `git show --name-only` of C2 lists exactly P1 to P4's files and of C3
exactly the four test files TESTS105 names; `git apply --check` and `git apply` exit 0; and
`git rev-parse C3:tests` reads the reviewer's dry-run tree
791b3df60712287004bcc8ba7a5ce17a87dfed90. `ruff check` over the eight files: exit 0.
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider` in the primary checkout with SPEC
S's environment over those four test files and `tests/ui_server/test_dashboard_contract.py`,
`tests/ui_server/test_budget_final_section.py`, `tests/ui_server/test_dashboard_cockpit_truth.py`,
`tests/ui_server/test_dashboard_truth_v3.py`, `tests/ui_server/test_prompt_trace_lens.py`,
`tests/orchestration/test_final_audit_evidence.py`, `tests/test_repair_context_reviewer_memory.py`,
`tests/test_cli_execution_loop_closure.py` and `tests/cli/test_golden_path.py`: exit 0; the
reviewer's worktree read 491 passed and 2 skipped.

G3 THE RED-PROOFS, in G3's worktree at C3, one production file at a time: write that file's
blob at `675dfcda` over it, run the named test file from inside the worktree with SPEC S's
environment, report the bad node ids, then restore the file and show it byte-identical to C3's.
Each named node MUST be among the bad nodes; a named node that stays green is DECLARED with its
tally. The reviewer's dry run: P1 over `tests/ui_server/test_prompt_trace_payload.py`,
`TestTheDashboardCarriesThePromptTrace::test_the_dashboard_carries_the_jobs_prompt_trace`; P2
over `tests/orchestration/test_approval_queue.py`,
`TestReviewerLoop::test_the_reviewer_context_names_the_job_by_its_title`; P3 over
`tests/orchestration/test_test_failure_repair.py`,
`TestBuildFailureArtifact::test_the_artifact_carries_the_job_id`; P4 over
`tests/orchestration/test_mission_state.py`,
`TestVerifyFirstStructure::test_the_refusals_name_the_task_by_its_title`. Each read 1 failed.
Then remove and prune the worktree, per constraint 6.

G4 THE SUITE, per SPEC S. Report pytest's real exit code, the summary line and the count of
distinct bad nodes, each by node id with its last `E   ` line. Each bad node is re-run by its
node id ALONE three times with SPEC S's environment, and reported FLAKY with the three tallies
only if all three pass. Bad nodes less FLAKY: MUST be none. At C4 the committed transcript
equals the file rebuilt from the saved stdout, and before C4 `git status --porcelain` listed
only that file.

G5 TREE, CANARY, PATH SET, OPEN SET, CAP, after C4. `git status --porcelain` prints `''` and
`git worktree list` one row. The canary `python3 -B -m pytest tests/cli/test_golden_path.py -q`:
exit 0. The changed-path set of `675dfcda`..C4 against the union of the Bundle's `.agent/`
paths other than `.agent/handoff.md` and the paths of C2 and C3: MISSING and EXTRA by name.
`ruff check . --output-format concise`: 11 rows. The open set at C4 equals C1's. One row per
commit of `675dfcda`..C4 with insertions, deletions and staged path count, and the commits
reaching 500 insertions, named.

Handback: `.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 35 of feature F275 · round 105 · rounds so far 105`; the Commits table read from
`git show --numstat` and compared cell by cell against G5, C5's row carrying no numbers and
saying why; one Verification line per gate with its REAL exit code; External actions;
Authored-text proofs; Item-status; Deviations; one sentence of context self-assessment;
`## Next` stating `Operator questions open: 1`. NO SCOPE REPORT AND NO SESSION-LIMIT BANNER,
by amendment amend0911-f275-to-scope.

── SLICE PLAN105 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN105 sha256=3879c634907ec55da713644ff131d4bf8d8551c2d58e83913af6a04f2c8651ad
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001, T002 and T003 are DONE: the record flip landed in
round 101 and the classic store was deleted in round 104.

## Current Step

ROUND 105 REPAIRS `R-0887` AND `R-0888`, the two regressions the flip left that the suite did
not see. The one dashboard builder emits `prompt_trace` from `_build_prompt_trace` over the
job's evidence directory, so the cockpit's prompt trace lens shows each task's prompts again;
the reviewer's context names a job by its `job_title`, a test failure artifact carries the
job's `job_id`, and the verify-first refusals quote a task's `title`. Each repair has a test
that fails without it. The full suite runs once and must read exit 0.

## Next Steps

1. THE CLOSURE SEQUENCE of `docs/roadmap/STATUS_closure_protocol.md`: the integration gate
   with its full-suite runs, the evidence job and a fresh review package, the re-assignment of
   every open finding this feature does not resolve, the §3 checklist consolidation, the
   ledger rotation, and the STATUS line with its pins, then the pull request.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20
  sessions and 60 rounds without a replacement, so this feature closes only at full scope.
- A SERVER-START RACE: a command-channel test read its server's info file before the server
  wrote it once in the reviewer's full run after the flip and passed ten times alone.
- THE CLOSURE NEEDS COMMANDS THIS ENVIRONMENT DENIES: the `remedy` command line is refused
  here, so every closure step is run through the scripts and modules it calls.
- ONE ROUTED LOAD IS REACHED BY NO TEST until `R-0883` is repaired.
- The open set is 91 by distinct id at this round's base, with `R-0809`, `R-0880`, `R-0883`,
  `R-0884`, `R-0887` and `R-0888` open. Four are High — R-0803, R-0804, R-0806 and R-0807 —
  all F273's, per DECISION F272 D12.
END PLAN105

── SLICE RECORD105 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD105 sha256=b7b813a1ebab9062ba9f20b68b7dddcc3d0c78565863d456db19d2dd417af8df

Gate: F275 R104 — the F275 round 104 entry. VERDICT PASS. Written by the planner and reviewer of session 35 after reading the committed range `8cbef186`..`675dfcda` and re-deriving every reading that bears on a product path; the worker's report and its transcripts were evidence for no line below. It is booked here by the first commit of round 105 that writes the record, per operator amendment amend0827-process-diet rule 1. The round deleted the classic store.

WHAT THE TRANSPORT PROOF COVERS, per item 37 of §3. The committed `.agent/authored/f275-r104.md` and `.agent/last_block.md` equal the reviewer's original at 24618 bytes at `675dfcda`; `.agent/plan.md` equals PLAN104 from `e7ac568e` through `675dfcda`; the three appends at `e7ac568e` are exact, each file there equal to its blob at `8cbef186` followed by its slice. The open set stayed 91 by distinct id, with `R-0885` and `R-0886` resolved and `R-0887` and `R-0888` registered.

THE DELETION IS THE TREE THE REVIEWER READ AND RAN. `8601b92e` changes 82 paths, 473 insertions and 1434 deletions, deleting `packages/orchestration/storage.py`, `tests/test_model_construction_keywords.py` and `tests/test_storage.py` and adding `tests/orchestration/test_one_job_store.py`; its `packages`, `apps`, `tests`, `scripts` and `docs` trees equal those of the dry run the reviewer staged at `8cbef186`, whose production hunks the reviewer read and where 130 selected test files read 6034 passed, the 2 failures being tests that read that worktree's own uncommitted status. In that dry run, restoring the resolver's union with a matcher of `<id>.json` files made `test_only_a_directory_holding_a_job_json_resolves_as_a_job` of `tests/test_data_paths.py` fail, and planting the deleted `storage.py` back made `test_the_store_module_is_not_on_disk_and_does_not_import` of `tests/orchestration/test_one_job_store.py` fail. At `675dfcda` a case-insensitive `git grep` over `packages`, `apps`, `tests` and `scripts` for the storage module, `_atomic_write_job`, `resolve_any_job_id`, `TWO job stores`, the two adapters, `_is_job_plan`, `_classic_job_id_matches` and `storage.py` exits 1 with no line.

THE SUITE. The committed transcript `.agent/authored/f275-r104-suite.txt` reads exit 0 with 18438 passed and 23 skipped, and lists no bad node. The reviewer's re-run in the primary checkout at `675dfcda` read fifteen targeted test files and directories, the two status-reading tests among them, at 1408 passed and 2 skipped with exit 0, and `ruff check .` at 11 rows.

ONE DEFECT OF THE BLOCK, declared by the worker. SPEC D gave the deletion diff's size as 151 KB, the size of an earlier state of the reviewer's dry run, while the file it named by digest is 182232 bytes; the digest matched and the worker used the file. It is booked as one line in `.agent/prose_slips.md` by the commit that books this entry.
END RECORD105

── SLICE SLIP105 ── target `.agent/prose_slips.md` ── APPEND ──
BEGIN SLIP105 sha256=eb31906c68d15888a7ff40d2df3bf65b92ca14fd044f705fcd913385300d4b44

2026-09-14 · F275 R104 · SPEC D of the round 104 block gave the deletion diff as "151 KB" beside its sha256, a size measured before the reviewer's last two rulings changed the dry run, while the file under that digest was 182232 bytes; the worker used the file the digest named and declared it. THE RULE THAT FOLLOWS: a size stated beside a digest is measured on the same bytes in the same step, or left out.
END SLIP105

── SLICE TESTS105 ── target SPEC T, a unified diff for `git apply` ── DIFF INPUT ──
BEGIN TESTS105 sha256=a4ec648a73fa95e53d2a75b5680d3f803ceb3450b513fcb9b5cb590ba243dfdc
diff --git a/tests/orchestration/test_approval_queue.py b/tests/orchestration/test_approval_queue.py
index a0c2af46..84f555dc 100644
--- a/tests/orchestration/test_approval_queue.py
+++ b/tests/orchestration/test_approval_queue.py
@@ -494,6 +494,14 @@ class TestReviewerLoop:
         recs = run_reviewer(job)
         assert isinstance(recs, list)
 
+    def test_the_reviewer_context_names_the_job_by_its_title(self):
+        """R-0888: a unified record hands the reviewer its title, not an empty name."""
+        from packages.orchestration.pingpong_job import JobPlan
+        from packages.orchestration.reviewer import run_reviewer
+        seen = []
+        run_reviewer(JobPlan(job_title="named-job"), reviewer_fn=lambda ctx: seen.append(ctx) or [])
+        assert seen[0]["job_name"] == "named-job"
+
     def test_run_reviewer_with_custom_fn(self):
         from packages.orchestration.reviewer import run_reviewer
         job = _make_job_s101(2)
diff --git a/tests/orchestration/test_mission_state.py b/tests/orchestration/test_mission_state.py
index fd5ae159..94f4fb9d 100644
--- a/tests/orchestration/test_mission_state.py
+++ b/tests/orchestration/test_mission_state.py
@@ -625,6 +625,15 @@ class TestVerifyFirstStructure:
         with pytest.raises(MissionVerifyFirstError):
             assert_verify_first([build_follow_up_task("Add the CSV path")])
 
+    def test_the_refusals_name_the_task_by_its_title(self):
+        """R-0888: both refusals quote the task's title, never a '?' placeholder."""
+        with pytest.raises(MissionVerifyFirstError, match="Add the CSV path"):
+            assert_verify_first([build_follow_up_task("Add the CSV path")])
+        loose = build_follow_up_task("Add the JSON path")
+        loose.inputs["flight"] = {"planned_id": "M001", "depends_on": []}
+        with pytest.raises(MissionVerifyFirstError, match="Add the JSON path"):
+            assert_verify_first([build_verify_first_task(self._previous_job()), loose])
+
     def test_an_empty_plan_is_refused(self):
         with pytest.raises(MissionVerifyFirstError):
             assert_verify_first([])
diff --git a/tests/orchestration/test_test_failure_repair.py b/tests/orchestration/test_test_failure_repair.py
index e1b1293f..a3b29a3c 100644
--- a/tests/orchestration/test_test_failure_repair.py
+++ b/tests/orchestration/test_test_failure_repair.py
@@ -143,6 +143,13 @@ class TestBuildFailureArtifact:
         assert failure.failure_kind == FAILURE_TIMEOUT
         assert failure.exit_code == 137
 
+    def test_the_artifact_carries_the_job_id(self, tmp_path):
+        """R-0888: the artifact links back to its job by the unified record's id."""
+        from packages.orchestration.pingpong_job import JobPlan
+        job = JobPlan(job_title="test", user_prompt="t")
+        failure = build_test_failure_artifact(job, {"status": "failed", "exit_code": 1})
+        assert failure.job_id == job.job_id != ""
+
     def test_build_fallback(self, tmp_path):
         from packages.orchestration.pingpong_job import JobPlan
         job = JobPlan(job_title="test", user_prompt="t")
diff --git a/tests/ui_server/test_prompt_trace_payload.py b/tests/ui_server/test_prompt_trace_payload.py
index 8486eee9..9d640df9 100644
--- a/tests/ui_server/test_prompt_trace_payload.py
+++ b/tests/ui_server/test_prompt_trace_payload.py
@@ -179,3 +179,21 @@ class TestPromptTracePayload:
         assert section["missingReason"] == "some_reason"
         assert section["totalPrompts"] == 0
         assert section["items"] == []
+
+
+class TestTheDashboardCarriesThePromptTrace:
+    """R-0887: the one dashboard builder emits the section the cockpit's lens reads."""
+
+    def test_the_dashboard_carries_the_jobs_prompt_trace(self, tmp_path, monkeypatch):
+        from packages.orchestration import ui_server
+        from packages.orchestration.pingpong_job import JobPlan
+
+        job = JobPlan(job_title="traced")
+        _write_trace(tmp_path, "T001", [_base_record()])
+        seen = []
+        monkeypatch.setattr(ui_server, "_load_events", lambda j: [])
+        monkeypatch.setattr(ui_server, "_resolve_evidence_dir", lambda job_id: seen.append(job_id) or tmp_path)
+        section = ui_server._build_dashboard(job)["prompt_trace"]
+        assert seen == [job.job_id]
+        assert section["source"] == "prompt_trace_jsonl"
+        assert [item["taskId"] for item in section["items"]] == ["T001"]
END TESTS105
