# F275 round 93 — the flip's fourth overlay, part 2 of 2

What the fourth overlay changes. It edits test code under `tests/` only. Every dotted patch target
naming the classic store's `load_job`, `save_job` or `list_jobs_safe` names the function the code
under test calls in the flipped tree instead: `require_job_plan` or `save_job_plan` on a handler
module that binds that name, and `load_job_plan`, `save_job_plan` or `list_job_plans_safe` on
`packages.orchestration.pingpong_job` where the handler imports it inside its function. The three
`monkeypatch.setattr` calls by name follow the same rule, and the tests that read unified functions
off the classic `storage` module read them off `pingpong_job`. The guard in
`tests/orchestration/test_job_plan_state_reads.py` binds locals from `load_job_plan` and from
`require_job_plan`, and its planted-source test runs once per loader.

This part holds 6 whole file diffs, `tests/orchestration/test_loop_run.py` through `tests/ui_server/test_command_dispatch.py`.

Base: `844a7f21`. The flipped tree is that commit checked out and then built exactly as G4 of
`.agent/authored/f275-r93.md` orders: the committed generator re-derives the TIP re-keyed set from
the two pinned round 77 JSON files, the guarded transform runs over the checkout with that set, its
owners file and `r61_status.json`, and the result is staged.

The 2 parts form the FOURTH overlay. They apply after
`.agent/authored/f275-r92-overlay-4.md`: `.agent/authored/f275-r90-overlay.md`, then
`.agent/authored/f275-r91-overlay.md`, then `.agent/authored/f275-r92-overlay-1.md` through
`-4.md` are each applied to the staged flipped tree and staged in turn, and the fourth overlay's
diff was taken against that state. The parts apply in `<k>` order, part 1 first; joined in that
order their fences are that one diff.

How to apply this part, inside the flipped tree with every earlier overlay applied and staged and
every part before this one applied:

1. Extract the fence below: the lines strictly between the line of three backticks followed by
   `diff` and the closing line of three backticks, each line kept with its newline.
2. Run `git apply --check <extracted file>` and require exit 0.
3. Run `git apply <extracted file>`.

```diff
diff --git a/tests/orchestration/test_loop_run.py b/tests/orchestration/test_loop_run.py
index 7ee189a2..be8cb9a9 100644
--- a/tests/orchestration/test_loop_run.py
+++ b/tests/orchestration/test_loop_run.py
@@ -33,7 +33,7 @@ import pytest
 
 from packages.core.models import RunState
 from packages.orchestration.pingpong_job import JobPlan
-from packages.orchestration import mission_state, storage
+from packages.orchestration import mission_state, pingpong_job
 from packages.orchestration.builder_models import BuilderOutput, TaskExecutionContext
 from packages.orchestration.long_run_executor import (
     TERMINAL_ALL_GREEN,
@@ -335,8 +335,8 @@ def test_last_run_for_loop_returns_the_most_recent_run_or_none(tmp_path: Path) -
                         created_at=datetime(2026, 8, 11, tzinfo=timezone.utc))
     newer = _stored_job("newer run", loop_ref="nightly-tidy",
                         created_at=datetime(2026, 8, 13, tzinfo=timezone.utc))
-    storage.save_job_plan(older, tmp_path)
-    storage.save_job_plan(newer, tmp_path)
+    pingpong_job.save_job_plan(older, tmp_path)
+    pingpong_job.save_job_plan(newer, tmp_path)
 
     assert last_run_for_loop("nightly-tidy", root=tmp_path).job_id == newer.job_id
     assert last_run_for_loop("never-ran", root=tmp_path) is None
@@ -347,8 +347,8 @@ def test_last_run_for_loop_ignores_another_loops_run(tmp_path: Path) -> None:
                        created_at=datetime(2026, 8, 11, tzinfo=timezone.utc))
     theirs = _stored_job("theirs", loop_ref="weekly-review",
                          created_at=datetime(2026, 8, 13, tzinfo=timezone.utc))
-    storage.save_job_plan(mine, tmp_path)
-    storage.save_job_plan(theirs, tmp_path)
+    pingpong_job.save_job_plan(mine, tmp_path)
+    pingpong_job.save_job_plan(theirs, tmp_path)
 
     found = last_run_for_loop("nightly-tidy", root=tmp_path)
     assert found is not None
@@ -369,7 +369,7 @@ def test_mission_run_persists_the_mission_text_on_the_stored_job(
 
     expected_goal = render_goal_template(spec.action.mission, project="remedy",
                                          date="2026-08-13")
-    stored = storage.load_job_plan(outcome.job.job_id, tmp_path)
+    stored = pingpong_job.load_job_plan(outcome.job.job_id, tmp_path)
     assert stored.mission == expected_goal
 
 
@@ -512,5 +512,5 @@ def test_a_fixture_loop_runs_end_to_end_and_its_report_names_the_loop(
     text = written.read_text(encoding="utf-8")
     assert [line for line in text.splitlines() if line == expected_line] == [expected_line]
 
-    stored = storage.load_job_plan(job.job_id, isolated_data_root)
+    stored = pingpong_job.load_job_plan(job.job_id, isolated_data_root)
     assert stored.metadata[LOOP_REF_METADATA_KEY] == spec.name
diff --git a/tests/orchestration/test_project_scope.py b/tests/orchestration/test_project_scope.py
index 0bf84b8e..2e9021e5 100644
--- a/tests/orchestration/test_project_scope.py
+++ b/tests/orchestration/test_project_scope.py
@@ -182,7 +182,7 @@ class TestScopedJobs:
             _job(None, name="legacy"),
         ]
         monkeypatch.setattr(
-            "packages.orchestration.storage.list_jobs_safe",
+            "packages.orchestration.pingpong_job.list_job_plans_safe",
             lambda root=None: (jobs, True, ["bad.json"]),
         )
 
@@ -201,7 +201,7 @@ class TestScopedJobs:
             _job(None, name="legacy"),
         ]
         monkeypatch.setattr(
-            "packages.orchestration.storage.list_jobs_safe",
+            "packages.orchestration.pingpong_job.list_job_plans_safe",
             lambda root=None: (jobs, False, []),
         )
 
diff --git a/tests/orchestration/test_test_execution_service.py b/tests/orchestration/test_test_execution_service.py
index 27d6ed80..cba92efb 100644
--- a/tests/orchestration/test_test_execution_service.py
+++ b/tests/orchestration/test_test_execution_service.py
@@ -518,7 +518,7 @@ class TestExecuteTestRunGates:
 
         with patch("packages.orchestration.test_execution_service.resolve_data_root",
                    return_value=tmp_path):
-            with patch("packages.orchestration.test_execution_service.load_job") as mock_load:
+            with patch("packages.orchestration.test_execution_service.require_job_plan") as mock_load:
                 job = self._make_job_with_repo(tmp_path)
                 job.metadata = {"permissions": {"repo_test_run": "allow"}}  # no target_repo
                 mock_load.return_value = job
@@ -532,7 +532,7 @@ class TestExecuteTestRunGates:
 
         with patch("packages.orchestration.test_execution_service.resolve_data_root",
                    return_value=tmp_path):
-            with patch("packages.orchestration.test_execution_service.load_job") as mock_load:
+            with patch("packages.orchestration.test_execution_service.require_job_plan") as mock_load:
                 job = self._make_job_with_repo(tmp_path)
                 mock_load.return_value = job
                 with patch("packages.orchestration.test_execution_service.is_allowed",
@@ -549,7 +549,7 @@ class TestExecuteTestRunGates:
 
         with patch("packages.orchestration.test_execution_service.resolve_data_root",
                    return_value=tmp_path):
-            with patch("packages.orchestration.test_execution_service.load_job") as mock_load:
+            with patch("packages.orchestration.test_execution_service.require_job_plan") as mock_load:
                 job = self._make_job_with_repo(tmp_path)
                 mock_load.return_value = job
                 with patch("packages.orchestration.test_execution_service.is_allowed",
@@ -587,7 +587,7 @@ class TestExecuteTestRunGates:
         try:
             with patch("packages.orchestration.test_execution_service.resolve_data_root",
                        return_value=tmp_path):
-                with patch("packages.orchestration.test_execution_service.load_job",
+                with patch("packages.orchestration.test_execution_service.require_job_plan",
                            return_value=job):
                     with patch("packages.orchestration.test_execution_service.is_allowed",
                                return_value=True):
@@ -613,7 +613,7 @@ class TestExecuteTestRunGates:
 
         with patch("packages.orchestration.test_execution_service.resolve_data_root",
                    return_value=tmp_path):
-            with patch("packages.orchestration.test_execution_service.load_job") as mock_load:
+            with patch("packages.orchestration.test_execution_service.require_job_plan") as mock_load:
                 job = self._make_job_with_repo(tmp_path)
                 mock_load.return_value = job
                 with patch("packages.orchestration.test_execution_service.is_allowed",
@@ -658,7 +658,7 @@ class TestExecuteTestRunGates:
 
         with patch("packages.orchestration.test_execution_service.resolve_data_root",
                    return_value=tmp_path):
-            with patch("packages.orchestration.test_execution_service.load_job") as mock_load:
+            with patch("packages.orchestration.test_execution_service.require_job_plan") as mock_load:
                 job = self._make_job_with_repo(tmp_path)
                 mock_load.return_value = job
                 with patch("packages.orchestration.test_execution_service.is_allowed",
@@ -670,7 +670,7 @@ class TestExecuteTestRunGates:
                      patch("packages.orchestration.test_execution_service.load_usage",
                            return_value=RunUsage()), \
                      patch("packages.orchestration.test_execution_service.save_usage"), \
-                     patch("packages.orchestration.test_execution_service.save_job"), \
+                     patch("packages.orchestration.test_execution_service.save_job_plan"), \
                      patch("packages.orchestration.test_execution_service.discover_commands",
                            return_value=candidates), \
                      patch("packages.orchestration.test_execution_service._run_isolated_process",
@@ -722,7 +722,7 @@ class TestExecuteTestRunGates:
         save_usage_calls = []
         with patch("packages.orchestration.test_execution_service.resolve_data_root",
                    return_value=tmp_path):
-            with patch("packages.orchestration.test_execution_service.load_job") as mock_load:
+            with patch("packages.orchestration.test_execution_service.require_job_plan") as mock_load:
                 job = self._make_job_with_repo(tmp_path)
                 mock_load.return_value = job
                 with patch("packages.orchestration.test_execution_service.is_allowed",
@@ -768,7 +768,7 @@ class TestUsageAccounting:
 
         with patch("packages.orchestration.test_execution_service.resolve_data_root",
                    return_value=tmp_path):
-            with patch("packages.orchestration.test_execution_service.load_job") as mock_load:
+            with patch("packages.orchestration.test_execution_service.require_job_plan") as mock_load:
                 job = MagicMock()
                 job.id = uuid4()
                 job.metadata = {"target_repo": str(repo)}
@@ -785,7 +785,7 @@ class TestUsageAccounting:
                                        return_value=initial_usage):
                                 with patch("packages.orchestration.test_execution_service.save_usage",
                                            side_effect=mock_save_usage):
-                                    with patch("packages.orchestration.test_execution_service.save_job"):
+                                    with patch("packages.orchestration.test_execution_service.save_job_plan"):
                                         req = TestExecutionRequest(
                                             job_id=str(job.id),
                                             requested_timeout_seconds=30.0,
@@ -917,7 +917,7 @@ class TestCatalogValidation:
         try:
             with patch("packages.orchestration.test_execution_service.resolve_data_root",
                        return_value=tmp_path), \
-                 patch("packages.orchestration.test_execution_service.load_job",
+                 patch("packages.orchestration.test_execution_service.require_job_plan",
                        return_value=job), \
                  patch("packages.orchestration.test_execution_service.is_allowed",
                        return_value=True), \
diff --git a/tests/test_cli_execution_loop_closure.py b/tests/test_cli_execution_loop_closure.py
index 7adfe886..0780a912 100644
--- a/tests/test_cli_execution_loop_closure.py
+++ b/tests/test_cli_execution_loop_closure.py
@@ -180,8 +180,8 @@ class TestReviewerCliJsonOutput:
     def test_review_run_fixture_json(self):
         """review run --fixture-reviewer --json returns structured output."""
         job = _make_job(tasks=[{"type": "test", "status": "completed"}])
-        with patch("packages.orchestration.storage.load_job", return_value=job), \
-             patch("packages.orchestration.storage.save_job"):
+        with patch("packages.orchestration.pingpong_job.load_job_plan", return_value=job), \
+             patch("packages.orchestration.pingpong_job.save_job_plan"):
             import contextlib
             import io
             args = MagicMock()
@@ -215,8 +215,8 @@ class TestReviewerCliJsonOutput:
         recs = run_reviewer(job, reviewer_fn=_fixture_reviewer)
         store_recommendations(job, recs)
 
-        with patch("packages.orchestration.storage.load_job", return_value=job), \
-             patch("packages.orchestration.storage.save_job"):
+        with patch("packages.orchestration.pingpong_job.load_job_plan", return_value=job), \
+             patch("packages.orchestration.pingpong_job.save_job_plan"):
             import contextlib
             import io
             args = MagicMock()
@@ -242,8 +242,8 @@ class TestReviewerCliJsonOutput:
         recs = run_reviewer(job, reviewer_fn=_fixture_reviewer)
         store_recommendations(job, recs)
 
-        with patch("packages.orchestration.storage.load_job", return_value=job), \
-             patch("packages.orchestration.storage.save_job"):
+        with patch("packages.orchestration.pingpong_job.load_job_plan", return_value=job), \
+             patch("packages.orchestration.pingpong_job.save_job_plan"):
             import contextlib
             import io
             args = MagicMock()
@@ -308,7 +308,7 @@ class TestMemoryCandidateCliCommands:
         job.metadata = {}
         create_candidate(job, "repair_pattern", "Fixed mul")
 
-        with patch("packages.orchestration.storage.load_job", return_value=job):
+        with patch("packages.orchestration.pingpong_job.load_job_plan", return_value=job):
             import contextlib
             import io
 
@@ -327,8 +327,8 @@ class TestMemoryCandidateCliCommands:
         job.metadata = {}
         c = create_candidate(job, "test_command", "pytest works")
 
-        with patch("packages.orchestration.storage.load_job", return_value=job), \
-             patch("packages.orchestration.storage.save_job"), \
+        with patch("packages.orchestration.pingpong_job.load_job_plan", return_value=job), \
+             patch("packages.orchestration.pingpong_job.save_job_plan"), \
              patch.dict("sys.modules", {"packages.orchestration.memory": MagicMock()}):
             import contextlib
             import io
@@ -347,8 +347,8 @@ class TestMemoryCandidateCliCommands:
         job.metadata = {}
         c = create_candidate(job, "test_command", "pytest works")
 
-        with patch("packages.orchestration.storage.load_job", return_value=job), \
-             patch("packages.orchestration.storage.save_job"):
+        with patch("packages.orchestration.pingpong_job.load_job_plan", return_value=job), \
+             patch("packages.orchestration.pingpong_job.save_job_plan"):
             import contextlib
             import io
 
diff --git a/tests/test_data_paths.py b/tests/test_data_paths.py
index 5e91e8dc..dc345cfd 100644
--- a/tests/test_data_paths.py
+++ b/tests/test_data_paths.py
@@ -350,12 +350,12 @@ class TestRoutedHandler:
         """Raised by the ``load_job`` spy, so a handler stops right after its load."""
 
     def _spy_on_load_job(self, monkeypatch) -> list[str]:
-        """Replace the storage ``load_job`` with a spy recording ``str()`` of each id it is handed.
+        """Replace ``load_job_plan`` and ``require_job_plan`` with a spy recording ``str()`` of each id.
 
-        The handlers import ``load_job`` inside the function, so the module attribute
-        is the one they read at call time.
+        The handlers import the loader inside the function, so the ``pingpong_job`` module
+        attribute is the one they read at call time.
         """
-        from packages.orchestration import storage
+        from packages.orchestration import pingpong_job
 
         seen: list[str] = []
 
@@ -363,7 +363,8 @@ class TestRoutedHandler:
             seen.append(str(job_id))
             raise self._LoadJobReached(str(job_id))
 
-        monkeypatch.setattr(storage, "load_job", spy)
+        monkeypatch.setattr(pingpong_job, "load_job_plan", spy)
+        monkeypatch.setattr(pingpong_job, "require_job_plan", spy)
         return seen
 
     @pytest.mark.parametrize(
diff --git a/tests/ui_server/test_command_dispatch.py b/tests/ui_server/test_command_dispatch.py
index 47a8c301..cb17b6af 100644
--- a/tests/ui_server/test_command_dispatch.py
+++ b/tests/ui_server/test_command_dispatch.py
@@ -230,9 +230,9 @@ class TestFlightPlanApprovalDispatchEffects:
         one edit away from "fixing" it into a double write. Counting the calls
         is what makes the omission a decision rather than an oversight.
         """
-        from packages.orchestration import storage
+        from packages.orchestration import pingpong_job
 
-        real_save_job = storage.save_job
+        real_save_job = pingpong_job.save_job_plan
         saves = []
 
         def counting_save_job(job, *args, **kwargs):
@@ -240,7 +240,7 @@ class TestFlightPlanApprovalDispatchEffects:
             return real_save_job(job, *args, **kwargs)
 
         port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
-        monkeypatch.setattr(storage, "save_job", counting_save_job)
+        monkeypatch.setattr(pingpong_job, "save_job_plan", counting_save_job)
         status, body = self._approve(port, token, "nonce-fp-save-once")
 
         assert status == 200, body
```
