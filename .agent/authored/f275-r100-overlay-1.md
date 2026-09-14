# F275 round 100 — the flip's eleventh overlay, part 1 of 1

What the eleventh overlay changes, in tests only. The two self-dogfood execution test files hand
a proposed task's own `id` to the eligibility and start calls, where the transform had them read
its `job_id`. Two assertions of `tests/test_project_brain.py` read a brain node's `id`, which a
brain node has, where they read `job_id` and `task_id`. The two constructions that reached
`packages.core.models` through `__import__` build a `JobPlan` and a `TaskEntry`. And the
`MagicMock` job doubles of twelve test files set `job_id` and `job_title` in place of `id` and
`name`, with the two reads of such a double's id reading `job_id`.

This part holds 17 whole file diffs, `tests/cli/test_job_commands.py` through `tests/ui_server/test_live_state.py`.

Base: `844a7f21`. The flipped tree is that commit checked out and then built exactly as G4 of
`.agent/authored/f275-r100.md` orders: the committed generator re-derives the TIP re-keyed set from
the two pinned round 77 JSON files, the guarded transform runs over the checkout with that set, its
owners file and `r61_status.json`, and the result is staged.

The ELEVENTH overlay is formed by 1 part, and this is part 1. The parts apply after
`.agent/authored/f275-r99-overlay-1.md`: the ten overlays before it, from
`.agent/authored/f275-r90-overlay.md` through `.agent/authored/f275-r99-overlay-1.md`, are applied
to the staged flipped tree overlay by overlay in the order constraint 8 of
`.agent/authored/f275-r100.md` names, each overlay staged in turn, and the eleventh overlay's
diff was taken against that state. The parts apply in `<k>` order, part 1 first; joined in that
order their fences are that one diff.

How to apply this part, inside the flipped tree with every earlier overlay applied and staged and
every part before this one applied:

1. Extract the fence below: the lines strictly between the line of three backticks followed by
   `diff` and the closing line of three backticks, each line kept with its newline.
2. Run `git apply --check <extracted file>` and require exit 0.
3. Run `git apply <extracted file>`.

```diff
diff --git a/tests/cli/test_job_commands.py b/tests/cli/test_job_commands.py
index 86393aa8..b370b2d4 100644
--- a/tests/cli/test_job_commands.py
+++ b/tests/cli/test_job_commands.py
@@ -20,8 +20,8 @@ _ROOT = Path(__file__).resolve().parent.parent.parent
 
 def _make_job():
     job = MagicMock()
-    job.id = uuid4()
-    job.name = "test-job"
+    job.job_id = uuid4()
+    job.job_title = "test-job"
     job.state.value = "active"
     job.tasks = []
     job.artifacts = []
@@ -31,8 +31,8 @@ def _make_job():
 
 def _make_job_s101(task_count: int = 3):
     job = MagicMock()
-    job.id = uuid4()
-    job.name = "test-job"
+    job.job_id = uuid4()
+    job.job_title = "test-job"
     job.state.value = "active"
     job.tasks = []
     job.artifacts = []
diff --git a/tests/cli/test_self_dogfood_execution_cli.py b/tests/cli/test_self_dogfood_execution_cli.py
index 6fe1e754..c771d5ef 100644
--- a/tests/cli/test_self_dogfood_execution_cli.py
+++ b/tests/cli/test_self_dogfood_execution_cli.py
@@ -37,7 +37,7 @@ def _approved_task(data_dir):
     tasks = load_proposed_tasks(str(job.job_id), data_dir)
     transition_status(tasks[0], ProposedTaskStatus.APPROVED_FOR_BUILD, by="human")
     save_proposed_tasks(str(job.job_id), tasks, data_dir)
-    return str(job.job_id), tasks[0].job_id
+    return str(job.job_id), tasks[0].id
 
 
 @pytest.fixture()
diff --git a/tests/orchestration/test_approval_queue.py b/tests/orchestration/test_approval_queue.py
index 91467be2..53a2fad3 100644
--- a/tests/orchestration/test_approval_queue.py
+++ b/tests/orchestration/test_approval_queue.py
@@ -91,8 +91,8 @@ def _make_job_s68(**overrides) -> JobPlan:
 
 def _make_job_s101(task_count: int = 3):
     job = MagicMock()
-    job.id = uuid4()
-    job.name = "test-job"
+    job.job_id = uuid4()
+    job.job_title = "test-job"
     job.state.value = "active"
     job.tasks = []
     job.artifacts = []
@@ -561,7 +561,7 @@ class TestReviewerLoop:
         assert ok is True
         assert len(job.tasks) == initial_task_count  # No direct task — creates ProposedTask instead
         assert job.metadata["reviewer_recommendations"][0]["status"] == "accepted"
-        proposed = load_proposed_tasks(str(job.id))
+        proposed = load_proposed_tasks(str(job.job_id))
         assert len(proposed) == 1
         assert proposed[0].title == "Add docs"
 
diff --git a/tests/orchestration/test_autorun.py b/tests/orchestration/test_autorun.py
index 955fdd21..37fd8f4b 100644
--- a/tests/orchestration/test_autorun.py
+++ b/tests/orchestration/test_autorun.py
@@ -16,8 +16,8 @@ _ROOT = Path(__file__).resolve().parent.parent.parent
 
 def _make_job():
     job = MagicMock()
-    job.id = uuid4()
-    job.name = "test-job"
+    job.job_id = uuid4()
+    job.job_title = "test-job"
     job.state.value = "active"
     job.tasks = []
     job.artifacts = []
diff --git a/tests/orchestration/test_self_dogfood_execution.py b/tests/orchestration/test_self_dogfood_execution.py
index 4dd421a2..cb199ba7 100644
--- a/tests/orchestration/test_self_dogfood_execution.py
+++ b/tests/orchestration/test_self_dogfood_execution.py
@@ -70,7 +70,7 @@ def _approved_task(data_dir, *, failure=True, repo="."):
 class TestEligibility:
     def test_approved_self_task_eligible(self, env):
         job, pt = _approved_task(env)
-        e = SE.evaluate_self_execution_eligibility(pt.job_id, str(job.job_id), env)
+        e = SE.evaluate_self_execution_eligibility(pt.id, str(job.job_id), env)
         assert e.eligible and e.item_fingerprint
 
     def test_missing_task(self, env):
@@ -82,19 +82,19 @@ class TestEligibility:
         SD.propose_self_improvement(str(job.job_id), top=2, data_dir=env)
         tasks = load_proposed_tasks(str(job.job_id), env)
         unapproved = next(t for t in tasks if t.status == ProposedTaskStatus.PROPOSED)
-        e = SE.evaluate_self_execution_eligibility(unapproved.job_id, str(job.job_id), env)
+        e = SE.evaluate_self_execution_eligibility(unapproved.id, str(job.job_id), env)
         assert not e.eligible and e.stop_reason == SE.StopReason.NOT_APPROVED
 
     def test_main_branch_blocks(self, env, monkeypatch):
         monkeypatch.setattr(SE, "current_branch", lambda: "main")
         job, pt = _approved_task(env)
-        e = SE.evaluate_self_execution_eligibility(pt.job_id, str(job.job_id), env)
+        e = SE.evaluate_self_execution_eligibility(pt.id, str(job.job_id), env)
         assert not e.eligible and e.stop_reason == SE.StopReason.MAIN_BRANCH_UNSAFE
 
     def test_unknown_branch_blocks(self, env, monkeypatch):
         monkeypatch.setattr(SE, "current_branch", lambda: "")
         job, pt = _approved_task(env)
-        e = SE.evaluate_self_execution_eligibility(pt.job_id, str(job.job_id), env)
+        e = SE.evaluate_self_execution_eligibility(pt.id, str(job.job_id), env)
         assert not e.eligible and e.stop_reason == SE.StopReason.MAIN_BRANCH_UNSAFE
 
     def test_contract_blocked(self, env):
@@ -108,7 +108,7 @@ class TestEligibility:
         c = dataclasses.replace(c, allowed_actions=tuple(
             a for a in c.allowed_actions if a != ContractAction.SELF_EXECUTE_PREPARE))
         save_contract(job, c); save_job_plan(job, root=env)
-        e = SE.evaluate_self_execution_eligibility(pt.job_id, str(job.job_id), env)
+        e = SE.evaluate_self_execution_eligibility(pt.id, str(job.job_id), env)
         assert not e.eligible and e.stop_reason == SE.StopReason.CONTRACT_BLOCKED
 
 
@@ -120,22 +120,22 @@ class TestEligibility:
 class TestStartAndIdempotency:
     def test_execute_awaits_candidate(self, env):
         job, pt = _approved_task(env)
-        r = SE.start_self_execution(pt.job_id, str(job.job_id), env)
+        r = SE.start_self_execution(pt.id, str(job.job_id), env)
         assert r.state == SE.AttemptState.AWAITING_EXTERNAL_CANDIDATE
         assert r.request_package_id
         assert r.next_safe_action == "remedy self status --json"
 
     def test_execute_idempotent_resume(self, env):
         job, pt = _approved_task(env)
-        r1 = SE.start_self_execution(pt.job_id, str(job.job_id), env)
-        r2 = SE.start_self_execution(pt.job_id, str(job.job_id), env)
+        r1 = SE.start_self_execution(pt.id, str(job.job_id), env)
+        r2 = SE.start_self_execution(pt.id, str(job.job_id), env)
         assert r1.attempt_id == r2.attempt_id
         assert len(SE.list_attempts(env)) == 1
 
     def test_main_blocks_start(self, env, monkeypatch):
         monkeypatch.setattr(SE, "current_branch", lambda: "main")
         job, pt = _approved_task(env)
-        r = SE.start_self_execution(pt.job_id, str(job.job_id), env)
+        r = SE.start_self_execution(pt.id, str(job.job_id), env)
         assert r.state == SE.AttemptState.BLOCKED
         assert r.stop_reason == SE.StopReason.MAIN_BRANCH_UNSAFE
         assert SE.list_attempts(env) == []
@@ -212,7 +212,7 @@ class TestArchitectureGuards:
         # not a string this test supplies, which is what it used to assert.
         from packages.orchestration.do_run import validate_next_safe_action_command
         job, pt = _approved_task(env)
-        r = SE.start_self_execution(pt.job_id, str(job.job_id), env)
+        r = SE.start_self_execution(pt.id, str(job.job_id), env)
         assert r.next_safe_action
         assert validate_next_safe_action_command(r.next_safe_action)
         rec = SE.reconcile_self_attempt(r.attempt_id, env)
diff --git a/tests/orchestration/test_source_apply.py b/tests/orchestration/test_source_apply.py
index 11f92148..7493dd77 100644
--- a/tests/orchestration/test_source_apply.py
+++ b/tests/orchestration/test_source_apply.py
@@ -43,8 +43,8 @@ def _make_job(*, project_id: str | None = None, target_repo: str | None = None)
 
 def _make_job_s91():
     job = MagicMock()
-    job.id = uuid4()
-    job.name = "test-job"
+    job.job_id = uuid4()
+    job.job_title = "test-job"
     job.state.value = "active"
     job.tasks = []
     job.artifacts = []
@@ -54,8 +54,8 @@ def _make_job_s91():
 
 def _make_job_s101(task_count: int = 3):
     job = MagicMock()
-    job.id = uuid4()
-    job.name = "test-job"
+    job.job_id = uuid4()
+    job.job_title = "test-job"
     job.state.value = "active"
     job.tasks = []
     job.artifacts = []
diff --git a/tests/orchestration/test_test_execution_service.py b/tests/orchestration/test_test_execution_service.py
index cba92efb..fb0c8bd8 100644
--- a/tests/orchestration/test_test_execution_service.py
+++ b/tests/orchestration/test_test_execution_service.py
@@ -770,7 +770,7 @@ class TestUsageAccounting:
                    return_value=tmp_path):
             with patch("packages.orchestration.test_execution_service.require_job_plan") as mock_load:
                 job = MagicMock()
-                job.id = uuid4()
+                job.job_id = uuid4()
                 job.metadata = {"target_repo": str(repo)}
                 job.tasks = []
                 job.artifacts = []
@@ -787,7 +787,7 @@ class TestUsageAccounting:
                                            side_effect=mock_save_usage):
                                     with patch("packages.orchestration.test_execution_service.save_job_plan"):
                                         req = TestExecutionRequest(
-                                            job_id=str(job.id),
+                                            job_id=str(job.job_id),
                                             requested_timeout_seconds=30.0,
                                         )
                                         result = execute_test_run(req)
diff --git a/tests/orchestration/test_test_runner.py b/tests/orchestration/test_test_runner.py
index b935dd04..50b928cc 100644
--- a/tests/orchestration/test_test_runner.py
+++ b/tests/orchestration/test_test_runner.py
@@ -25,8 +25,8 @@ _ROOT = Path(__file__).resolve().parent.parent.parent
 
 def _make_job(task_count: int = 3):
     job = MagicMock()
-    job.id = uuid4()
-    job.name = "test-job"
+    job.job_id = uuid4()
+    job.job_title = "test-job"
     job.state.value = "active"
     job.tasks = []
     job.artifacts = []
diff --git a/tests/regression/test_named_bugs.py b/tests/regression/test_named_bugs.py
index e2624ea6..51060bf3 100644
--- a/tests/regression/test_named_bugs.py
+++ b/tests/regression/test_named_bugs.py
@@ -64,8 +64,8 @@ def _make_job(*, project_id: str | None = None, target_repo: str | None = None)
 
 def _make_job_s101(task_count: int = 3):
     job = MagicMock()
-    job.id = uuid4()
-    job.name = "test-job"
+    job.job_id = uuid4()
+    job.job_title = "test-job"
     job.state.value = "active"
     job.tasks = []
     job.artifacts = []
diff --git a/tests/test_patch_apply.py b/tests/test_patch_apply.py
index 620a03ab..e1d9b7d8 100644
--- a/tests/test_patch_apply.py
+++ b/tests/test_patch_apply.py
@@ -175,7 +175,7 @@ class TestPathSafety:
         except (OSError, NotImplementedError):
             pytest.skip("symlink creation not available on this platform")
 
-        job = __import__("packages.core.models", fromlist=["Job"]).Job(job_title="symlink test")
+        job = JobPlan(job_title="symlink test")
         job.metadata["target_repo"] = str(repo_dir)
 
         # Build an intent pointing at escape/file.md — passes path component checks
diff --git a/tests/test_project_brain.py b/tests/test_project_brain.py
index 2c3bbfc5..aa170adb 100644
--- a/tests/test_project_brain.py
+++ b/tests/test_project_brain.py
@@ -260,7 +260,7 @@ class TestBuildProjectBrain:
         graph = build_project_brain(job, [])
         job_nodes = [n for n in graph.nodes if n.type == NT_JOB]
         assert len(job_nodes) == 1
-        assert job_nodes[0].job_id == str(job.job_id)
+        assert job_nodes[0].id == str(job.job_id)
         assert job_nodes[0].status == "pending"
 
     def test_empty_job_always_has_placeholders(self):
@@ -295,7 +295,7 @@ class TestBuildProjectBrain:
         graph = build_project_brain(job, [])
         task_nodes = [n for n in graph.nodes if n.type == NT_TASK]
         assert len(task_nodes) == 1
-        assert task_nodes[0].task_id == str(task.task_id)
+        assert task_nodes[0].id == str(task.task_id)
         assert task_nodes[0].status == "pending"
         has_task_edges = [e for e in graph.edges if e.type == ET_HAS_TASK]
         assert len(has_task_edges) == 1
diff --git a/tests/ui_contracts/test_graph_architecture.py b/tests/ui_contracts/test_graph_architecture.py
index 411fa72a..c62fa9c2 100644
--- a/tests/ui_contracts/test_graph_architecture.py
+++ b/tests/ui_contracts/test_graph_architecture.py
@@ -55,8 +55,8 @@ def _make_job_s74(**overrides) -> JobPlan:
 
 def _make_job_s91():
     job = MagicMock()
-    job.id = uuid4()
-    job.name = "test-job"
+    job.job_id = uuid4()
+    job.job_title = "test-job"
     job.state.value = "active"
     job.tasks = []
     job.artifacts = []
@@ -66,8 +66,8 @@ def _make_job_s91():
 
 def _make_job_s101(task_count: int = 3):
     job = MagicMock()
-    job.id = uuid4()
-    job.name = "test-job"
+    job.job_id = uuid4()
+    job.job_title = "test-job"
     job.state.value = "active"
     job.tasks = []
     job.artifacts = []
diff --git a/tests/ui_contracts/test_responsive.py b/tests/ui_contracts/test_responsive.py
index 012f6b34..9fab3bb6 100644
--- a/tests/ui_contracts/test_responsive.py
+++ b/tests/ui_contracts/test_responsive.py
@@ -66,8 +66,8 @@ def _make_job_s80(**overrides: object) -> JobPlan:
 
 def _make_job_s91():
     job = MagicMock()
-    job.id = uuid4()
-    job.name = "test-job"
+    job.job_id = uuid4()
+    job.job_title = "test-job"
     job.state.value = "active"
     job.tasks = []
     job.artifacts = []
diff --git a/tests/ui_contracts/test_ux_quality.py b/tests/ui_contracts/test_ux_quality.py
index 6ef695e6..3ec74d10 100644
--- a/tests/ui_contracts/test_ux_quality.py
+++ b/tests/ui_contracts/test_ux_quality.py
@@ -67,8 +67,8 @@ def _make_job_s80(**overrides: object) -> JobPlan:
 
 def _make_job_s91():
     job = MagicMock()
-    job.id = uuid4()
-    job.name = "test-job"
+    job.job_id = uuid4()
+    job.job_title = "test-job"
     job.state.value = "active"
     job.tasks = []
     job.artifacts = []
@@ -78,8 +78,8 @@ def _make_job_s91():
 
 def _make_job_s101(task_count: int = 3):
     job = MagicMock()
-    job.id = uuid4()
-    job.name = "test-job"
+    job.job_id = uuid4()
+    job.job_title = "test-job"
     job.state.value = "active"
     job.tasks = []
     job.artifacts = []
diff --git a/tests/ui_server/test_brain_view_model.py b/tests/ui_server/test_brain_view_model.py
index 670cebc3..44b523e4 100644
--- a/tests/ui_server/test_brain_view_model.py
+++ b/tests/ui_server/test_brain_view_model.py
@@ -136,8 +136,8 @@ class TestBrainViewModel:
     def _make_job(self):
         # Use a minimal mock job
         job = MagicMock()
-        job.id = uuid4()
-        job.name = "test-job"
+        job.job_id = uuid4()
+        job.job_title = "test-job"
         job.state.value = "active"
         job.tasks = []
         job.artifacts = []
@@ -242,8 +242,8 @@ class TestBrainViewModel:
 class TestNodeDetail:
     def _make_job(self):
         job = MagicMock()
-        job.id = uuid4()
-        job.name = "test-job"
+        job.job_id = uuid4()
+        job.job_title = "test-job"
         job.state.value = "active"
         job.tasks = []
         job.artifacts = []
@@ -266,8 +266,8 @@ class TestNodeDetail:
     def test_detail_missing_node(self):
         from packages.orchestration.ui_view_model import build_node_detail
         job = MagicMock()
-        job.id = uuid4()
-        job.name = "test"
+        job.job_id = uuid4()
+        job.job_title = "test"
         job.state.value = "active"
         job.tasks = []
         job.artifacts = []
diff --git a/tests/ui_server/test_dashboard_cockpit_truth.py b/tests/ui_server/test_dashboard_cockpit_truth.py
index b0bb3274..ddc21502 100644
--- a/tests/ui_server/test_dashboard_cockpit_truth.py
+++ b/tests/ui_server/test_dashboard_cockpit_truth.py
@@ -10,7 +10,7 @@ from __future__ import annotations
 import json
 from pathlib import Path
 
-from packages.orchestration.pingpong_job import JobPlan
+from packages.orchestration.pingpong_job import JobPlan, TaskEntry
 from packages.orchestration import ui_server
 from packages.orchestration.ui_server import (
     _build_continuation_section,
@@ -133,7 +133,7 @@ class TestTaskTruthMaps:
         # A proof_collected event must NOT make a task "verified" — only the
         # authoritative chain does (R-0076). With no data root the per-task proof
         # is "unknown", never "verified".
-        job = JobPlan(job_title="t", tasks=[__import__("packages.core.models", fromlist=["Task"]).Task(title="x")])
+        job = JobPlan(job_title="t", tasks=[TaskEntry(title="x")])
         import packages.orchestration.ui_server as us
         # Force the unknown path (no data root): proof chain is None.
         orig = us._resolve_dashboard_data_dir
diff --git a/tests/ui_server/test_live_state.py b/tests/ui_server/test_live_state.py
index b38aa85e..3b43386f 100644
--- a/tests/ui_server/test_live_state.py
+++ b/tests/ui_server/test_live_state.py
@@ -37,8 +37,8 @@ def _make_job(**overrides: object) -> JobPlan:
 
 def _make_job_s91():
     job = MagicMock()
-    job.id = uuid4()
-    job.name = "test-job"
+    job.job_id = uuid4()
+    job.job_title = "test-job"
     job.state.value = "active"
     job.tasks = []
     job.artifacts = []
@@ -48,8 +48,8 @@ def _make_job_s91():
 
 def _make_job_s101(task_count: int = 3):
     job = MagicMock()
-    job.id = uuid4()
-    job.name = "test-job"
+    job.job_id = uuid4()
+    job.job_title = "test-job"
     job.state.value = "active"
     job.tasks = []
     job.artifacts = []
```
