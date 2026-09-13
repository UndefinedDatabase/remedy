# F275 round 91 — the flip's second overlay

What it changes. An artifact id the unified task record holds becomes the artifact's id as a string:
`run_next_task` in `packages/orchestration/task_runner.py` appends `str(artifact.id)` to
`task.output_artifact_ids`, which `TaskEntry` declares `list[str]`. The five lookups of an artifact
by an id read back from that list compare `str(a.id)` with it: in `finalize_task` and
`materialize_task_output` of `task_runner.py`, in `verify_task_output` of
`packages/orchestration/verifier.py`, and twice in `_cmd_run_next_task_local` of
`apps/cli/commands/job.py`. The artifact itself keeps its `UUID`. In nine test files, a `JobPlan` or
`TaskEntry` constructed, assigned, appended to or saved with a `UUID` object in `job_id`, `task_id`
or a member of `output_artifact_ids` receives the string form, and a comparison of such a field with
a `UUID` object, or a prefix derived from it with `.hex`, uses the string form. No test is added or
deleted. `repository_snapshot.revert_repository_apply` and
`test_execution_service.execute_test_run` keep their `UUID(...)` parses and are not touched here.

Base: `844a7f21`. The flipped tree is that commit checked out and then built exactly as G4 of
`.agent/authored/f275-r91.md` orders: the committed generator re-derives the TIP re-keyed set from
the two pinned round 77 JSON files, the guarded transform runs over the checkout with that set, its
owners file and `r61_status.json`, and the result is staged.

This is the SECOND overlay. It applies after `.agent/authored/f275-r90-overlay.md`, the first,
which is applied to the staged flipped tree and staged in turn; this diff was taken against that
state. Every later overlay applies after both, in round order.

How to apply it, inside the flipped tree with the first overlay applied and staged:

1. Extract the fence below: the lines strictly between the line of three backticks followed by
   `diff` and the closing line of three backticks, each line kept with its newline.
2. Run `git apply --check <extracted file>` and require exit 0.
3. Run `git apply <extracted file>`.

```diff
diff --git a/apps/cli/commands/job.py b/apps/cli/commands/job.py
index 4016a00c..84e7ab4b 100644
--- a/apps/cli/commands/job.py
+++ b/apps/cli/commands/job.py
@@ -578,7 +578,7 @@ def _cmd_run_next_task_local(job_id_str: str) -> None:
             task_obj = next(t for t in result.job.tasks if t.task_id == result.task_id)
             if task_obj.output_artifact_ids:
                 artifact_id = task_obj.output_artifact_ids[0]
-                artifact = next((a for a in result.job.artifacts if a.id == artifact_id), None)
+                artifact = next((a for a in result.job.artifacts if str(a.id) == artifact_id), None)
                 if artifact is not None:
                     repo_applied = check_and_apply_to_repo(job, artifact, repo_root)
                     if repo_applied:
@@ -605,7 +605,7 @@ def _cmd_run_next_task_local(job_id_str: str) -> None:
         pi_task_obj = next(t for t in result.job.tasks if t.task_id == result.task_id)
         if pi_task_obj.output_artifact_ids:
             pi_artifact_id = pi_task_obj.output_artifact_ids[0]
-            pi_artifact = next((a for a in result.job.artifacts if a.id == pi_artifact_id), None)
+            pi_artifact = next((a for a in result.job.artifacts if str(a.id) == pi_artifact_id), None)
             if pi_artifact is not None:
                 pi_task_type = pi_artifact.metadata.get("task_type", "unknown")
                 pi_task_index = next(i for i, t in enumerate(result.job.tasks) if t.task_id == result.task_id)
diff --git a/packages/orchestration/task_runner.py b/packages/orchestration/task_runner.py
index 81e897f1..3e869b60 100644
--- a/packages/orchestration/task_runner.py
+++ b/packages/orchestration/task_runner.py
@@ -245,7 +245,7 @@ def run_next_task(
 
     # Task intentionally stays RUNNING here — finalize_task() will mark it
     # COMPLETED only after verify_task_output() passes (Step 7 verifier gate).
-    task.output_artifact_ids.append(artifact.id)
+    task.output_artifact_ids.append(str(artifact.id))
     job.artifacts.append(artifact)
 
     return RunTaskResult(job=job, task_id=task.task_id, changed=True)
@@ -363,7 +363,7 @@ def finalize_task(result: RunTaskResult, vr: VerificationResult) -> None:
         # Locate the current attempt's artifact by ID (not by task_id scan —
         # multiple failed artifacts share the same task_id).
         artifact = next(
-            (a for a in result.job.artifacts if a.id == current_artifact_id),
+            (a for a in result.job.artifacts if str(a.id) == current_artifact_id),
             None,
         )
         if artifact is None:
@@ -464,7 +464,7 @@ def materialize_task_output(
         )
     artifact_id = task_obj.output_artifact_ids[0]
     artifact = next(
-        (a for a in result.job.artifacts if a.id == artifact_id),
+        (a for a in result.job.artifacts if str(a.id) == artifact_id),
         None,
     )
     if artifact is None:
diff --git a/packages/orchestration/verifier.py b/packages/orchestration/verifier.py
index 9d6d8e03..eeb797c4 100644
--- a/packages/orchestration/verifier.py
+++ b/packages/orchestration/verifier.py
@@ -181,7 +181,7 @@ def verify_task_output(
 
         # Check 2: referenced artifact exists
         artifact_id = task.output_artifact_ids[0]
-        artifact = next((a for a in job.artifacts if a.id == artifact_id), None)
+        artifact = next((a for a in job.artifacts if str(a.id) == artifact_id), None)
         artifact_exists = artifact is not None
         checks.append(
             VerificationCheckResult(
diff --git a/tests/cli/test_patch_cmd.py b/tests/cli/test_patch_cmd.py
index adbe25de..833ed78e 100644
--- a/tests/cli/test_patch_cmd.py
+++ b/tests/cli/test_patch_cmd.py
@@ -108,7 +108,7 @@ def isolated(tmp_path, monkeypatch) -> Path:
 
 
 def _job(job_id: UUID | None = None) -> JobPlan:
-    job = JobPlan(job_id=job_id or uuid4(), job_title="hunk decision job",
+    job = JobPlan(job_id=str(job_id or uuid4()), job_title="hunk decision job",
               metadata={"unrelated": "kept"})
     save_job_plan(job)
     return job
@@ -333,7 +333,7 @@ class TestTheEvidenceDirectoryComesFromTheRESOLVEDJobId:
         """The prefix form is why `resolve_job_id` exists, and it must reach the index."""
         job = _job()
         self._premise(tmp_path, job)
-        prefix = job.job_id.hex[:8]
+        prefix = job.job_id[:8]
         assert resolve_job_id(prefix) == str(job.job_id), \
             "the fixture's prefix must name THIS job"
 
diff --git a/tests/orchestration/test_escalation.py b/tests/orchestration/test_escalation.py
index a89f00f1..f13d3b56 100644
--- a/tests/orchestration/test_escalation.py
+++ b/tests/orchestration/test_escalation.py
@@ -111,7 +111,7 @@ class TestEnqueue:
         record = escalate(job)
 
         assert record["decision_id"].startswith(DECISION_ID_PREFIX)
-        assert job.tasks[0].task_id.hex[:8] in record["decision_id"]
+        assert job.tasks[0].task_id[:8] in record["decision_id"]
 
     def test_a_second_decision_for_the_same_task_gets_its_own_id(self):
         job = make_job()
diff --git a/tests/storage/test_persistence.py b/tests/storage/test_persistence.py
index f7f50d1b..167fba7f 100644
--- a/tests/storage/test_persistence.py
+++ b/tests/storage/test_persistence.py
@@ -47,7 +47,7 @@ def _make_job(*, project_id: str | None = None, target_repo: str | None = None)
 
 def _make_job_s68(**overrides) -> JobPlan:
     defaults = {
-        "job_id": uuid4(),
+        "job_id": str(uuid4()),
         "job_title": "test-job",
         "user_prompt": "test prompt",
         "tasks": [
@@ -62,7 +62,7 @@ def _make_job_s68(**overrides) -> JobPlan:
 
 def _make_job_s71(**overrides) -> JobPlan:
     defaults = {
-        "job_id": uuid4(),
+        "job_id": str(uuid4()),
         "job_title": "test-job",
         "user_prompt": "test prompt",
         "tasks": [TaskEntry(title="task 1", status=RunState.COMPLETED)],
diff --git a/tests/test_cli_main.py b/tests/test_cli_main.py
index 31d6469a..e332d8cb 100644
--- a/tests/test_cli_main.py
+++ b/tests/test_cli_main.py
@@ -328,7 +328,7 @@ class TestPatchIntentErrorsCLI:
             task_id=str(task.task_id),
             metadata={"task_type": "write_readme", "summary": "Update readme"},
         )
-        task.output_artifact_ids.append(artifact.id)
+        task.output_artifact_ids.append(str(artifact.id))
         job.tasks.append(task)
         job.artifacts.append(artifact)
         save_job_plan(job)  # saved with task in PENDING status
@@ -427,7 +427,7 @@ class TestPatchIntentErrorsCLI:
             task_id=str(task.task_id),
             metadata={"task_type": "write_readme", "summary": "Update readme"},
         )
-        task.output_artifact_ids.append(artifact.id)
+        task.output_artifact_ids.append(str(artifact.id))
         job.tasks.append(task)
         job.artifacts.append(artifact)
         save_job_plan(job)  # saved with task in PENDING status
@@ -559,7 +559,7 @@ class TestPatchIntentRisksCLI:
             task_id=str(task.task_id),
             metadata={"task_type": "write_readme", "summary": "Update readme"},
         )
-        task.output_artifact_ids.append(artifact.id)
+        task.output_artifact_ids.append(str(artifact.id))
         job.tasks.append(task)
         job.artifacts.append(artifact)
         save_job_plan(job)
diff --git a/tests/test_run_log_cli.py b/tests/test_run_log_cli.py
index d72229ee..0272bfbc 100644
--- a/tests/test_run_log_cli.py
+++ b/tests/test_run_log_cli.py
@@ -302,7 +302,7 @@ def _build_success_mocks(tmp_path, job: JobPlan, task: TaskEntry):
         kind=ArtifactKind.BUILDER_PROPOSAL,
         metadata={"task_type": task.inputs.get("task_type", "unknown"), "summary": "done"},
     )
-    task.output_artifact_ids.append(artifact.id)
+    task.output_artifact_ids.append(str(artifact.id))
     job.artifacts.append(artifact)
 
     ws_file = tmp_path / "fake_ws.txt"
@@ -442,7 +442,7 @@ class TestRunNextTaskVerificationFailure:
             kind=ArtifactKind.BUILDER_PROPOSAL,
             metadata={"task_type": "write_readme", "summary": "done"},
         )
-        task.output_artifact_ids.append(artifact.id)
+        task.output_artifact_ids.append(str(artifact.id))
         job.artifacts.append(artifact)
         task.status = RunState.RUNNING
 
@@ -562,7 +562,7 @@ class TestRunNextTaskRepoPermissionDenied:
             kind=ArtifactKind.BUILDER_PROPOSAL,
             metadata={"task_type": "write_readme", "summary": "done"},
         )
-        task.output_artifact_ids.append(artifact.id)
+        task.output_artifact_ids.append(str(artifact.id))
         job.artifacts.append(artifact)
 
         ws_file = tmp_path / "fake_ws.txt"
@@ -650,7 +650,7 @@ class TestRunNextTaskPatchIntentCreated:
             kind=ArtifactKind.BUILDER_PROPOSAL,
             metadata={"task_type": "write_readme", "summary": "done"},
         )
-        task.output_artifact_ids.append(artifact.id)
+        task.output_artifact_ids.append(str(artifact.id))
         job.artifacts.append(artifact)
 
         ws_file = tmp_path / "fake_ws.txt"
@@ -766,7 +766,7 @@ class TestRunNextTaskPatchIntentCreated:
             kind=ArtifactKind.BUILDER_PROPOSAL,
             metadata={"task_type": "write_readme", "summary": "done"},
         )
-        task.output_artifact_ids.append(artifact.id)
+        task.output_artifact_ids.append(str(artifact.id))
         job.artifacts.append(artifact)
 
         ws_file = tmp_path / "fake_ws.txt"
diff --git a/tests/test_task_runner.py b/tests/test_task_runner.py
index f5a1ba95..579b9a34 100644
--- a/tests/test_task_runner.py
+++ b/tests/test_task_runner.py
@@ -136,7 +136,7 @@ def test_context_includes_prior_task_summaries():
             metadata={"task_type": f"type_{i}", "summary": f"done task {i + 1}"},
         )
         job.artifacts.append(art)
-        t.output_artifact_ids.append(art.id)
+        t.output_artifact_ids.append(str(art.id))
 
     run_next_task(job, capturing_builder)  # task 2 — receives summaries from 0 and 1
 
@@ -224,7 +224,7 @@ def test_output_artifact_ids_updated():
     run_next_task(job, _stub_builder)
     task = job.tasks[0]
     assert len(task.output_artifact_ids) == 1
-    assert task.output_artifact_ids[0] == job.artifacts[-1].id
+    assert task.output_artifact_ids[0] == str(job.artifacts[-1].id)
 
 
 def test_artifact_name_contains_task_type():
@@ -518,7 +518,7 @@ def test_finalize_task_failed_artifact_remains_in_job_artifacts():
     finalize_task(result, _failing_vr(result.task_id, "workspace file missing"))
 
     # Artifact stays in job.artifacts even though task no longer references it
-    assert any(a.id == failed_artifact_id for a in job.artifacts)
+    assert any(str(a.id) == failed_artifact_id for a in job.artifacts)
 
 
 def test_finalize_task_records_failure_in_artifact_metadata():
@@ -581,14 +581,14 @@ def test_consecutive_failures_annotate_each_artifact_separately():
     finalize_task(result2, _failing_vr(result2.task_id, "second failure reason"))
 
     # artifact1: has metadata from FIRST failure
-    artifact1 = next(a for a in job.artifacts if a.id == artifact1_id)
+    artifact1 = next(a for a in job.artifacts if str(a.id) == artifact1_id)
     assert artifact1.metadata["verification_passed"] is False
     assert any("first failure reason" in f for f in artifact1.metadata["verification_failures"])
     # artifact1 must NOT have been overwritten with second failure data
     assert not any("second failure reason" in f for f in artifact1.metadata["verification_failures"])
 
     # artifact2: has metadata from SECOND failure
-    artifact2 = next(a for a in job.artifacts if a.id == artifact2_id)
+    artifact2 = next(a for a in job.artifacts if str(a.id) == artifact2_id)
     assert artifact2.metadata["verification_passed"] is False
     assert any("second failure reason" in f for f in artifact2.metadata["verification_failures"])
 
@@ -618,7 +618,7 @@ def test_consecutive_failures_both_artifacts_preserved_in_job():
     artifact2_id = job.tasks[0].output_artifact_ids[0]
     finalize_task(result2, _failing_vr(result2.task_id, "fail 2"))
 
-    artifact_ids_in_job = {a.id for a in job.artifacts}
+    artifact_ids_in_job = {str(a.id) for a in job.artifacts}
     assert artifact1_id in artifact_ids_in_job
     assert artifact2_id in artifact_ids_in_job
 
@@ -669,6 +669,6 @@ def test_finalize_task_raises_if_artifact_not_found_in_job_artifacts():
     result = run_next_task(job, _stub_builder)
     # Replace artifact ID in task with a dangling UUID so the lookup fails
     phantom_id = _uuid4()
-    job.tasks[0].output_artifact_ids[0] = phantom_id
+    job.tasks[0].output_artifact_ids[0] = str(phantom_id)
     with pytest.raises(RuntimeError, match="not found in job.artifacts"):
         finalize_task(result, _failing_vr(result.task_id, "some failure"))
diff --git a/tests/test_verifier.py b/tests/test_verifier.py
index 39894d78..31dbdef3 100644
--- a/tests/test_verifier.py
+++ b/tests/test_verifier.py
@@ -130,7 +130,7 @@ def test_verify_fails_when_artifact_id_not_in_job_artifacts():
     """output_artifact_ids references a UUID not in job.artifacts."""
     job = _make_planned_job()
     task = job.tasks[0]
-    task.output_artifact_ids.append(uuid4())  # dangling reference
+    task.output_artifact_ids.append(str(uuid4()))  # dangling reference
     vr = verify_task_output(job, task.task_id)
     assert vr.passed is False
     assert any(c.check == "artifact_exists" and not c.passed for c in vr.checks)
@@ -153,7 +153,7 @@ def test_verify_fails_when_artifact_task_id_does_not_match():
         metadata={},
     )
     job.artifacts.append(wrong_artifact)
-    task.output_artifact_ids.append(wrong_artifact.id)
+    task.output_artifact_ids.append(str(wrong_artifact.id))
 
     vr = verify_task_output(job, task.task_id)
     assert vr.passed is False
@@ -178,7 +178,7 @@ def test_verify_fails_when_workspace_file_key_missing():
         # no 'workspace_file' key
     )
     job.artifacts.append(artifact)
-    task.output_artifact_ids.append(artifact.id)
+    task.output_artifact_ids.append(str(artifact.id))
 
     vr = verify_task_output(job, task.task_id)
     assert vr.passed is False
@@ -207,7 +207,7 @@ def test_verify_fails_when_workspace_file_does_not_exist(tmp_path):
         },
     )
     job.artifacts.append(artifact)
-    task.output_artifact_ids.append(artifact.id)
+    task.output_artifact_ids.append(str(artifact.id))
 
     vr = verify_task_output(job, task.task_id)
     assert vr.passed is False
@@ -238,7 +238,7 @@ def test_verify_fails_when_workspace_file_is_empty(tmp_path):
         },
     )
     job.artifacts.append(artifact)
-    task.output_artifact_ids.append(artifact.id)
+    task.output_artifact_ids.append(str(artifact.id))
 
     vr = verify_task_output(job, task.task_id)
     assert vr.passed is False
@@ -269,7 +269,7 @@ def test_verify_fails_when_no_proposed_change_lines(tmp_path):
         },
     )
     job.artifacts.append(artifact)
-    task.output_artifact_ids.append(artifact.id)
+    task.output_artifact_ids.append(str(artifact.id))
 
     vr = verify_task_output(job, task.task_id)
     assert vr.passed is False
@@ -453,7 +453,7 @@ def _setup_artifact_with_content(
         },
     )
     job.artifacts.append(artifact)
-    task.output_artifact_ids.append(artifact.id)
+    task.output_artifact_ids.append(str(artifact.id))
     return artifact
 
 
@@ -508,7 +508,7 @@ class TestGenericProfileVerification:
             metadata={"task_type": "write_readme", "summary": "done"},
         )
         job.artifacts.append(artifact)
-        task.output_artifact_ids.append(artifact.id)
+        task.output_artifact_ids.append(str(artifact.id))
 
         vr = verify_task_output(
             job, task.task_id, contract=TaskContract(require_workspace_file=False)
diff --git a/tests/test_workspace.py b/tests/test_workspace.py
index 72e23aa5..37e0e199 100644
--- a/tests/test_workspace.py
+++ b/tests/test_workspace.py
@@ -459,7 +459,7 @@ def test_materialize_filename_includes_short_task_id(tmp_path, monkeypatch):
     mf = materialize_task_output(result, runtime)
     assert mf is not None
     task = next(t for t in result.job.tasks if t.task_id == result.task_id)
-    short_id = task.task_id.hex[:8]
+    short_id = task.task_id[:8]
     assert short_id in mf.path.name
 
 
diff --git a/tests/ui_contracts/test_responsive.py b/tests/ui_contracts/test_responsive.py
index 0edf1b40..012f6b34 100644
--- a/tests/ui_contracts/test_responsive.py
+++ b/tests/ui_contracts/test_responsive.py
@@ -27,7 +27,7 @@ UI_ROOT = ROOT / "apps" / "ui"
 
 def _make_job(**overrides) -> JobPlan:
     defaults = {
-        "job_id": uuid4(),
+        "job_id": str(uuid4()),
         "job_title": "test-job",
         "user_prompt": "test prompt",
         "tasks": [TaskEntry(title="task 1", status=RunState.COMPLETED)],
@@ -43,7 +43,7 @@ def _make_job(**overrides) -> JobPlan:
 
 def _make_job_s74(**overrides) -> JobPlan:
     defaults = {
-        "job_id": uuid4(),
+        "job_id": str(uuid4()),
         "job_title": "test-job",
         "user_prompt": "test prompt",
         "tasks": [TaskEntry(title="task 1", status=RunState.COMPLETED)],
```
