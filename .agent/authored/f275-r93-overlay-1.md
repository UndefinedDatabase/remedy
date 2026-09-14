# F275 round 93 — the flip's fourth overlay, part 1 of 2

What the fourth overlay changes. It edits test code under `tests/` only. Every dotted patch target
naming the classic store's `load_job`, `save_job` or `list_jobs_safe` names the function the code
under test calls in the flipped tree instead: `require_job_plan` or `save_job_plan` on a handler
module that binds that name, and `load_job_plan`, `save_job_plan` or `list_job_plans_safe` on
`packages.orchestration.pingpong_job` where the handler imports it inside its function. The three
`monkeypatch.setattr` calls by name follow the same rule, and the tests that read unified functions
off the classic `storage` module read them off `pingpong_job`. The guard in
`tests/orchestration/test_job_plan_state_reads.py` binds locals from `load_job_plan` and from
`require_job_plan`, and its planted-source test runs once per loader.

This part holds 7 whole file diffs, `tests/cli/test_change_proof_cli.py` through `tests/orchestration/test_job_plan_state_reads.py`.

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
diff --git a/tests/cli/test_change_proof_cli.py b/tests/cli/test_change_proof_cli.py
index eb798cf6..a6863293 100644
--- a/tests/cli/test_change_proof_cli.py
+++ b/tests/cli/test_change_proof_cli.py
@@ -81,7 +81,7 @@ def test_handler_text_output(capsys):
     job, _, _ = _make_test_job()
     job_id = str(job.job_id)
 
-    with patch("apps.cli.commands.change.load_job", return_value=job), \
+    with patch("apps.cli.commands.change.require_job_plan", return_value=job), \
          patch("apps.cli.commands.change.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=[]):
         _cmd_change_proof(job_id)
@@ -97,7 +97,7 @@ def test_handler_text_does_not_overclaim_verified(capsys):
     job, iid, events = _make_test_job(with_apply=True)  # no test
     job_id = str(job.job_id)
 
-    with patch("apps.cli.commands.change.load_job", return_value=job), \
+    with patch("apps.cli.commands.change.require_job_plan", return_value=job), \
          patch("apps.cli.commands.change.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=events):
         _cmd_change_proof(job_id)
@@ -111,7 +111,7 @@ def test_handler_json_output(capsys):
     job, _, _ = _make_test_job()
     job_id = str(job.job_id)
 
-    with patch("apps.cli.commands.change.load_job", return_value=job), \
+    with patch("apps.cli.commands.change.require_job_plan", return_value=job), \
          patch("apps.cli.commands.change.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=[]):
         _cmd_change_proof(job_id, json_output=True)
@@ -130,7 +130,7 @@ def test_handler_json_incomplete_when_test_order_unknown(capsys):
     events.append({"event": "test_run_completed", "metadata": {"status": "passed", "exit_code": 0}})
     job_id = str(job.job_id)
 
-    with patch("apps.cli.commands.change.load_job", return_value=job), \
+    with patch("apps.cli.commands.change.require_job_plan", return_value=job), \
          patch("apps.cli.commands.change.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=events):
         _cmd_change_proof(job_id, json_output=True)
@@ -146,7 +146,7 @@ def test_handler_text_incomplete_when_test_order_unknown(capsys):
     events.append({"event": "test_run_completed", "metadata": {"status": "passed", "exit_code": 0}})
     job_id = str(job.job_id)
 
-    with patch("apps.cli.commands.change.load_job", return_value=job), \
+    with patch("apps.cli.commands.change.require_job_plan", return_value=job), \
          patch("apps.cli.commands.change.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=events):
         _cmd_change_proof(job_id)
@@ -162,7 +162,7 @@ def test_change_show_does_not_display_unrelated_latest_global_test(capsys):
     events.append({"event": "test_run_completed", "metadata": {"status": "passed", "exit_code": 0}})
     job_id = str(job.job_id)
 
-    with patch("apps.cli.commands.change.load_job", return_value=job), \
+    with patch("apps.cli.commands.change.require_job_plan", return_value=job), \
          patch("apps.cli.commands.change.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=events):
         _cmd_change_show(job_id, iid)
@@ -178,13 +178,13 @@ def test_file_why_proof_status_agrees_with_change_proof_path(capsys):
     job, _iid, events = _make_test_job(with_apply=True, with_test=True)
     job_id = str(job.job_id)
 
-    with patch("apps.cli.commands.change.load_job", return_value=job), \
+    with patch("apps.cli.commands.change.require_job_plan", return_value=job), \
          patch("apps.cli.commands.change.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=events):
         _cmd_change_proof(job_id, path="src/auth.py", json_output=True)
     proof_data = json.loads(capsys.readouterr().out)
 
-    with patch("apps.cli.commands.file.load_job", return_value=job), \
+    with patch("apps.cli.commands.file.require_job_plan", return_value=job), \
          patch("apps.cli.commands.file.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=events):
         _cmd_file_why(job_id, "src/auth.py", json_output=True)
@@ -198,7 +198,7 @@ def test_handler_json_structured_next_action(capsys):
     job, _, _ = _make_test_job()
     job_id = str(job.job_id)
 
-    with patch("apps.cli.commands.change.load_job", return_value=job), \
+    with patch("apps.cli.commands.change.require_job_plan", return_value=job), \
          patch("apps.cli.commands.change.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=[]):
         _cmd_change_proof(job_id, json_output=True)
@@ -217,7 +217,7 @@ def test_handler_path_filter(capsys):
     job, _, _ = _make_test_job()
     job_id = str(job.job_id)
 
-    with patch("apps.cli.commands.change.load_job", return_value=job), \
+    with patch("apps.cli.commands.change.require_job_plan", return_value=job), \
          patch("apps.cli.commands.change.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=[]):
         _cmd_change_proof(job_id, path="src/auth.py", json_output=True)
@@ -231,7 +231,7 @@ def test_handler_path_traversal_rejected():
     from apps.cli.commands.change import _cmd_change_proof
     job_id = str(uuid4())
 
-    with patch("apps.cli.commands.change.load_job"), \
+    with patch("apps.cli.commands.change.require_job_plan"), \
          pytest.raises(SystemExit) as exc_info:
         _cmd_change_proof(job_id, path="../etc/passwd")
 
@@ -242,7 +242,7 @@ def test_handler_absolute_path_rejected():
     from apps.cli.commands.change import _cmd_change_proof
     job_id = str(uuid4())
 
-    with patch("apps.cli.commands.change.load_job"), \
+    with patch("apps.cli.commands.change.require_job_plan"), \
          pytest.raises(SystemExit) as exc_info:
         _cmd_change_proof(job_id, path="/etc/passwd")
 
@@ -264,7 +264,7 @@ def test_handler_no_traceback(capsys):
     job, _, _ = _make_test_job()
     job_id = str(job.job_id)
 
-    with patch("apps.cli.commands.change.load_job", return_value=job), \
+    with patch("apps.cli.commands.change.require_job_plan", return_value=job), \
          patch("apps.cli.commands.change.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=[]):
         _cmd_change_proof(job_id)
@@ -279,7 +279,7 @@ def test_handler_output_bounded(capsys):
     job, _, _ = _make_test_job()
     job_id = str(job.job_id)
 
-    with patch("apps.cli.commands.change.load_job", return_value=job), \
+    with patch("apps.cli.commands.change.require_job_plan", return_value=job), \
          patch("apps.cli.commands.change.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=[]):
         _cmd_change_proof(job_id)
diff --git a/tests/cli/test_context_inspect_cli.py b/tests/cli/test_context_inspect_cli.py
index 20456793..3d41db25 100644
--- a/tests/cli/test_context_inspect_cli.py
+++ b/tests/cli/test_context_inspect_cli.py
@@ -56,7 +56,7 @@ def test_handler_text_output(capsys):
     job, task = _make_test_job()
     job_id = str(job.job_id)
 
-    with patch("apps.cli.commands.context.load_job", return_value=job), \
+    with patch("apps.cli.commands.context.require_job_plan", return_value=job), \
          patch("packages.orchestration.context_inspector._resolve_repo_root", return_value=None), \
          patch("packages.orchestration.data_paths.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=[]):
@@ -72,7 +72,7 @@ def test_handler_json_output(capsys):
     job, task = _make_test_job()
     job_id = str(job.job_id)
 
-    with patch("apps.cli.commands.context.load_job", return_value=job), \
+    with patch("apps.cli.commands.context.require_job_plan", return_value=job), \
          patch("packages.orchestration.context_inspector._resolve_repo_root", return_value=None), \
          patch("packages.orchestration.data_paths.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=[]):
@@ -94,7 +94,7 @@ def test_handler_json_with_task_id(capsys):
     job_id = str(job.job_id)
     task_id = str(task.task_id)
 
-    with patch("apps.cli.commands.context.load_job", return_value=job), \
+    with patch("apps.cli.commands.context.require_job_plan", return_value=job), \
          patch("packages.orchestration.context_inspector._resolve_repo_root", return_value=None), \
          patch("packages.orchestration.data_paths.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=[]):
@@ -116,7 +116,7 @@ def test_handler_invalid_task_id():
     job, _ = _make_test_job()
     job_id = str(job.job_id)
 
-    with patch("apps.cli.commands.context.load_job", return_value=job), \
+    with patch("apps.cli.commands.context.require_job_plan", return_value=job), \
          pytest.raises(SystemExit) as exc_info:
         _cmd_context_inspect(job_id, task_id="not-a-uuid")
     assert exc_info.value.code == 1
@@ -127,7 +127,7 @@ def test_handler_no_traceback(capsys):
     job, _ = _make_test_job()
     job_id = str(job.job_id)
 
-    with patch("apps.cli.commands.context.load_job", return_value=job), \
+    with patch("apps.cli.commands.context.require_job_plan", return_value=job), \
          patch("packages.orchestration.context_inspector._resolve_repo_root", return_value=None), \
          patch("packages.orchestration.data_paths.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=[]):
@@ -143,7 +143,7 @@ def test_handler_output_bounded(capsys):
     job, _ = _make_test_job()
     job_id = str(job.job_id)
 
-    with patch("apps.cli.commands.context.load_job", return_value=job), \
+    with patch("apps.cli.commands.context.require_job_plan", return_value=job), \
          patch("packages.orchestration.context_inspector._resolve_repo_root", return_value=None), \
          patch("packages.orchestration.data_paths.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=[]):
@@ -175,7 +175,7 @@ def test_handler_task_not_in_job():
     job_id = str(job.job_id)
     fake_task_id = str(uuid4())  # valid UUID, not in job
 
-    with patch("apps.cli.commands.context.load_job", return_value=job), \
+    with patch("apps.cli.commands.context.require_job_plan", return_value=job), \
          pytest.raises(SystemExit) as exc_info:
         _cmd_context_inspect(job_id, task_id=fake_task_id)
     assert exc_info.value.code == 1
@@ -188,7 +188,7 @@ def test_handler_task_in_job_passes(capsys):
     job_id = str(job.job_id)
     task_id = str(task.task_id)
 
-    with patch("apps.cli.commands.context.load_job", return_value=job), \
+    with patch("apps.cli.commands.context.require_job_plan", return_value=job), \
          patch("packages.orchestration.context_inspector._resolve_repo_root", return_value=None), \
          patch("packages.orchestration.data_paths.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=[]):
@@ -204,7 +204,7 @@ def test_handler_json_budget_gate_assessed(capsys):
     job, _ = _make_test_job()
     job_id = str(job.job_id)
 
-    with patch("apps.cli.commands.context.load_job", return_value=job), \
+    with patch("apps.cli.commands.context.require_job_plan", return_value=job), \
          patch("packages.orchestration.context_inspector._resolve_repo_root", return_value=None), \
          patch("packages.orchestration.data_paths.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=[]):
diff --git a/tests/cli/test_loop_cmd.py b/tests/cli/test_loop_cmd.py
index ca793d91..c2d855fe 100644
--- a/tests/cli/test_loop_cmd.py
+++ b/tests/cli/test_loop_cmd.py
@@ -40,7 +40,7 @@ import pytest
 from apps.cli.command_catalog import CATALOG
 from apps.cli.commands import collect_all_handlers
 from packages.core.models import RunState
-from packages.orchestration import storage
+from packages.orchestration import pingpong_job
 from packages.orchestration.loop_run import LOOP_REF_METADATA_KEY, run_loop
 from packages.orchestration.loop_spec import INERT_TRIGGER_NOTICE, load_loop_specs
 
@@ -124,7 +124,7 @@ def _dispatch_with(command_id: str, **attributes: object) -> None:
 
 def _stored_jobs() -> list:
     """Every job actually PERSISTED, read back through the store the command wrote to."""
-    jobs, _degraded, _skipped = storage.list_job_plans_safe()
+    jobs, _degraded, _skipped = pingpong_job.list_job_plans_safe()
     return jobs
 
 
@@ -170,7 +170,7 @@ def test_after_one_real_firing_the_row_shows_that_run(project, capsys):
     _write_config(project, MANUAL_JOB_LOOP)
     (spec,) = load_loop_specs()
     outcome = run_loop(spec, project_id="remedy", date="2026-08-13", root=project)
-    stored = storage.load_job_plan(outcome.job.job_id, project)
+    stored = pingpong_job.load_job_plan(outcome.job.job_id, project)
 
     _dispatch_with("loop.list", json=False)
 
@@ -184,7 +184,7 @@ def test_json_output_carries_last_run_created_at_and_state(project, capsys):
     _write_config(project, MANUAL_JOB_LOOP)
     (spec,) = load_loop_specs()
     outcome = run_loop(spec, project_id="remedy", date="2026-08-13", root=project)
-    stored = storage.load_job_plan(outcome.job.job_id, project)
+    stored = pingpong_job.load_job_plan(outcome.job.job_id, project)
 
     _dispatch_with("loop.list", json=True)
 
diff --git a/tests/cli/test_patch_cmd.py b/tests/cli/test_patch_cmd.py
index 833ed78e..11088fe8 100644
--- a/tests/cli/test_patch_cmd.py
+++ b/tests/cli/test_patch_cmd.py
@@ -266,7 +266,7 @@ class TestItMintsNoRefusalVocabularyOfItsOwn:
         job = _job()
         _evidence(tmp_path, job)
         calls: list[object] = []
-        monkeypatch.setattr(CMD, "save_job", lambda saved: calls.append(saved))
+        monkeypatch.setattr(CMD, "save_job_plan", lambda saved: calls.append(saved))
 
         with pytest.raises(SystemExit):
             CMD._cmd_approve_hunks(str(job.job_id), reject=[HUNK_IDS[0]])
diff --git a/tests/cli/test_review_cmd.py b/tests/cli/test_review_cmd.py
index f061f1ef..d0f8c2ef 100644
--- a/tests/cli/test_review_cmd.py
+++ b/tests/cli/test_review_cmd.py
@@ -27,7 +27,7 @@ def test_text_output_shows_created_date(capsys):
 
     job_stub = SimpleNamespace(id=uuid4())
     args = Namespace(job_id=str(job_stub.id), json=False)
-    with patch("packages.orchestration.storage.load_job", return_value=job_stub), \
+    with patch("packages.orchestration.pingpong_job.load_job_plan", return_value=job_stub), \
          patch("packages.orchestration.reviewer.list_recommendations", return_value=_recs()):
         _cmd_review_list(args)
 
@@ -40,7 +40,7 @@ def test_json_output_carries_created_at(capsys):
 
     job_stub = SimpleNamespace(id=uuid4())
     args = Namespace(job_id=str(job_stub.id), json=True)
-    with patch("packages.orchestration.storage.load_job", return_value=job_stub), \
+    with patch("packages.orchestration.pingpong_job.load_job_plan", return_value=job_stub), \
          patch("packages.orchestration.reviewer.list_recommendations", return_value=_recs()):
         _cmd_review_list(args)
 
@@ -58,7 +58,7 @@ def test_limit_caps_returned_recommendations(capsys):
         {"id": "rec3", "title": "C", "status": "pending", "created_at": "2026-09-03T00:00:00+00:00"},
     ]
     args = Namespace(job_id=str(job_stub.id), json=True, limit="2")
-    with patch("packages.orchestration.storage.load_job", return_value=job_stub), \
+    with patch("packages.orchestration.pingpong_job.load_job_plan", return_value=job_stub), \
          patch("packages.orchestration.reviewer.list_recommendations", return_value=recs):
         _cmd_review_list(args)
 
@@ -71,7 +71,7 @@ def test_unknown_sort_field_exits_nonzero():
 
     job_stub = SimpleNamespace(id=uuid4())
     args = Namespace(job_id=str(job_stub.id), json=True, sort="bogus")
-    with patch("packages.orchestration.storage.load_job", return_value=job_stub), \
+    with patch("packages.orchestration.pingpong_job.load_job_plan", return_value=job_stub), \
          patch("packages.orchestration.reviewer.list_recommendations", return_value=_recs()):
         with pytest.raises(SystemExit) as exc:
             _cmd_review_list(args)
diff --git a/tests/cli/test_scoped_listings.py b/tests/cli/test_scoped_listings.py
index cb9886ca..76139103 100644
--- a/tests/cli/test_scoped_listings.py
+++ b/tests/cli/test_scoped_listings.py
@@ -352,7 +352,7 @@ class TestScopedJobsIntegration:
 
         scope = ProjectScope(project_id=_P1, all_projects=False, source="flag")
         with patch(
-            "packages.orchestration.storage.list_jobs_safe",
+            "packages.orchestration.pingpong_job.list_job_plans_safe",
             return_value=(mock_jobs, False, []),
         ), patch(
             "packages.orchestration.project_scope._project_count",
@@ -374,7 +374,7 @@ class TestScopedJobsIntegration:
 
         scope = ProjectScope(project_id=None, all_projects=True, source="flag")
         with patch(
-            "packages.orchestration.storage.list_jobs_safe",
+            "packages.orchestration.pingpong_job.list_job_plans_safe",
             return_value=(mock_jobs, True, ["bad.json"]),
         ):
             jobs, degraded, skipped = scoped_jobs(scope)
diff --git a/tests/orchestration/test_job_plan_state_reads.py b/tests/orchestration/test_job_plan_state_reads.py
index dd5ffcfd..a7c22d06 100644
--- a/tests/orchestration/test_job_plan_state_reads.py
+++ b/tests/orchestration/test_job_plan_state_reads.py
@@ -23,10 +23,10 @@ this file:
 
 This test is the standing guard the probe cannot be. It reads every tracked
 ``.py`` file under ``packages/`` and ``apps/`` with ``ast``, finds the locals
-bound from ``load_job_plan(...)`` in each function scope, and fails on any read
-of ``status`` off one of them — whether spelled as an attribute or as a
-``getattr`` string. A file is enumerated from ``git ls-files`` and never from a
-shell glob, per DECISION F272 D2.
+bound from ``load_job_plan(...)`` or ``require_job_plan(...)`` in each function
+scope, and fails on any read of ``status`` off one of them — whether spelled as
+an attribute or as a ``getattr`` string. A file is enumerated from
+``git ls-files`` and never from a shell glob, per DECISION F272 D2.
 """
 from __future__ import annotations
 
@@ -34,13 +34,15 @@ import ast
 import subprocess
 from pathlib import Path
 
+import pytest
+
 REPO_ROOT = Path(__file__).resolve().parents[2]
 
 #: The retired spelling. ``state`` is the live one.
 RETIRED_FIELD = "status"
 
-#: The loader whose return value is a ``JobPlan``.
-JOB_PLAN_LOADER = "load_job_plan"
+#: The loaders whose return value is a ``JobPlan``.
+JOB_PLAN_LOADERS = ("load_job_plan", "require_job_plan")
 
 
 def _tracked_production_python_files() -> list[Path]:
@@ -71,7 +73,7 @@ class _RetiredReadFinder(ast.NodeVisitor):
                 continue
             fn = call.func
             name = fn.attr if isinstance(fn, ast.Attribute) else getattr(fn, "id", "")
-            if name != JOB_PLAN_LOADER:
+            if name not in JOB_PLAN_LOADERS:
                 continue
             for target in sub.targets:
                 if isinstance(target, ast.Name):
@@ -134,11 +136,12 @@ class TestNoRetiredJobPlanStateReads:
         files = _tracked_production_python_files()
         assert len(files) > 300, f"corpus collapsed to {len(files)} files"
 
-    def test_the_scan_sees_a_retired_read_when_one_is_there(self) -> None:
-        """The discriminator: the finder is not vacuously empty."""
+    @pytest.mark.parametrize("loader", JOB_PLAN_LOADERS)
+    def test_the_scan_sees_a_retired_read_when_one_is_there(self, loader: str) -> None:
+        """The discriminator: the finder is not vacuously empty, for either loader."""
         source = (
             "def f(jid):\n"
-            "    j = load_job_plan(jid)\n"
+            f"    j = {loader}(jid)\n"
             "    return getattr(j, 'status', '')\n"
         )
         finder = _RetiredReadFinder("synthetic.py")
```
