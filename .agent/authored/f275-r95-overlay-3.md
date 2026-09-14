# F275 round 95 — the flip's sixth overlay, part 3 of 4

What the sixth overlay changes. Production code under `packages/` and `apps/` that read `.id`
or `.name` off a job it loaded, under the local names `job`, `j` or `plan`, reads the unified
record's `job_id` and `job_title` (79 reads; the classic store's own module is untouched). The
job doubles tests hand that code spell the same: the `_FakeJob`, `_Job` and `_LoopJob` classes
carry `job_id` and `job_title`, the `SimpleNamespace` stubs of the `review list` tests pass
`job_id=`, and the tests read those names back. A handler test that doubles the job loader as
the first context manager of its `with` statement now also doubles, as the second, the
resolver the handler's module binds (`resolve_job_id` or `lookup_job_id`) with an identity, so
the handler still receives the id the test built (27 `with` statements).

This part holds 6 whole file diffs, `tests/cli/test_context_inspect_cli.py` through `tests/orchestration/test_project_summary.py`.

Base: `844a7f21`. The flipped tree is that commit checked out and then built exactly as G4 of
`.agent/authored/f275-r95.md` orders: the committed generator re-derives the TIP re-keyed set from
the two pinned round 77 JSON files, the guarded transform runs over the checkout with that set, its
owners file and `r61_status.json`, and the result is staged.

The 4 parts form the SIXTH overlay. They apply after
`.agent/authored/f275-r94-overlay-2.md`: `.agent/authored/f275-r90-overlay.md`, then
`.agent/authored/f275-r91-overlay.md`, then `.agent/authored/f275-r92-overlay-1.md` through
`-4.md`, then `.agent/authored/f275-r93-overlay-1.md` and `-2.md`, then
`.agent/authored/f275-r94-overlay-1.md` and `-2.md` are applied to the staged flipped tree
overlay by overlay, each overlay staged in turn, and the sixth overlay's diff was taken against
that state. The parts apply in `<k>` order, part 1 first; joined in that order their fences are
that one diff.

How to apply this part, inside the flipped tree with every earlier overlay applied and staged and
every part before this one applied:

1. Extract the fence below: the lines strictly between the line of three backticks followed by
   `diff` and the closing line of three backticks, each line kept with its newline.
2. Run `git apply --check <extracted file>` and require exit 0.
3. Run `git apply <extracted file>`.

```diff
diff --git a/tests/cli/test_context_inspect_cli.py b/tests/cli/test_context_inspect_cli.py
index 3d41db25..ba58a772 100644
--- a/tests/cli/test_context_inspect_cli.py
+++ b/tests/cli/test_context_inspect_cli.py
@@ -57,6 +57,7 @@ def test_handler_text_output(capsys):
     job_id = str(job.job_id)
 
     with patch("apps.cli.commands.context.require_job_plan", return_value=job), \
+         patch("apps.cli.commands.context.lookup_job_id", side_effect=lambda raw: raw), \
          patch("packages.orchestration.context_inspector._resolve_repo_root", return_value=None), \
          patch("packages.orchestration.data_paths.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=[]):
@@ -73,6 +74,7 @@ def test_handler_json_output(capsys):
     job_id = str(job.job_id)
 
     with patch("apps.cli.commands.context.require_job_plan", return_value=job), \
+         patch("apps.cli.commands.context.lookup_job_id", side_effect=lambda raw: raw), \
          patch("packages.orchestration.context_inspector._resolve_repo_root", return_value=None), \
          patch("packages.orchestration.data_paths.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=[]):
@@ -95,6 +97,7 @@ def test_handler_json_with_task_id(capsys):
     task_id = str(task.task_id)
 
     with patch("apps.cli.commands.context.require_job_plan", return_value=job), \
+         patch("apps.cli.commands.context.lookup_job_id", side_effect=lambda raw: raw), \
          patch("packages.orchestration.context_inspector._resolve_repo_root", return_value=None), \
          patch("packages.orchestration.data_paths.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=[]):
@@ -117,6 +120,7 @@ def test_handler_invalid_task_id():
     job_id = str(job.job_id)
 
     with patch("apps.cli.commands.context.require_job_plan", return_value=job), \
+         patch("apps.cli.commands.context.lookup_job_id", side_effect=lambda raw: raw), \
          pytest.raises(SystemExit) as exc_info:
         _cmd_context_inspect(job_id, task_id="not-a-uuid")
     assert exc_info.value.code == 1
@@ -128,6 +132,7 @@ def test_handler_no_traceback(capsys):
     job_id = str(job.job_id)
 
     with patch("apps.cli.commands.context.require_job_plan", return_value=job), \
+         patch("apps.cli.commands.context.lookup_job_id", side_effect=lambda raw: raw), \
          patch("packages.orchestration.context_inspector._resolve_repo_root", return_value=None), \
          patch("packages.orchestration.data_paths.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=[]):
@@ -144,6 +149,7 @@ def test_handler_output_bounded(capsys):
     job_id = str(job.job_id)
 
     with patch("apps.cli.commands.context.require_job_plan", return_value=job), \
+         patch("apps.cli.commands.context.lookup_job_id", side_effect=lambda raw: raw), \
          patch("packages.orchestration.context_inspector._resolve_repo_root", return_value=None), \
          patch("packages.orchestration.data_paths.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=[]):
@@ -176,6 +182,7 @@ def test_handler_task_not_in_job():
     fake_task_id = str(uuid4())  # valid UUID, not in job
 
     with patch("apps.cli.commands.context.require_job_plan", return_value=job), \
+         patch("apps.cli.commands.context.lookup_job_id", side_effect=lambda raw: raw), \
          pytest.raises(SystemExit) as exc_info:
         _cmd_context_inspect(job_id, task_id=fake_task_id)
     assert exc_info.value.code == 1
@@ -189,6 +196,7 @@ def test_handler_task_in_job_passes(capsys):
     task_id = str(task.task_id)
 
     with patch("apps.cli.commands.context.require_job_plan", return_value=job), \
+         patch("apps.cli.commands.context.lookup_job_id", side_effect=lambda raw: raw), \
          patch("packages.orchestration.context_inspector._resolve_repo_root", return_value=None), \
          patch("packages.orchestration.data_paths.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=[]):
@@ -205,6 +213,7 @@ def test_handler_json_budget_gate_assessed(capsys):
     job_id = str(job.job_id)
 
     with patch("apps.cli.commands.context.require_job_plan", return_value=job), \
+         patch("apps.cli.commands.context.lookup_job_id", side_effect=lambda raw: raw), \
          patch("packages.orchestration.context_inspector._resolve_repo_root", return_value=None), \
          patch("packages.orchestration.data_paths.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=[]):
diff --git a/tests/cli/test_project_summary_cli.py b/tests/cli/test_project_summary_cli.py
index 091b4563..4cd14da2 100644
--- a/tests/cli/test_project_summary_cli.py
+++ b/tests/cli/test_project_summary_cli.py
@@ -46,7 +46,7 @@ class TestProjectSummaryOutput:
 
     def _make_job(self, state="planned"):
         job = MagicMock()
-        job.id = uuid4()
+        job.job_id = uuid4()
         job.state.value = state
         job.state.__str__ = lambda s: state
         job.tasks = []
@@ -74,13 +74,13 @@ class TestProjectSummaryOutput:
         proj = self._make_project()
         j1 = self._make_job("completed")
         j2 = self._make_job("blocked")
-        proj.job_ids = [str(j1.id), str(j2.id)]
+        proj.job_ids = [str(j1.job_id), str(j2.job_id)]
 
         events = {
-            str(j1.id): [
+            str(j1.job_id): [
                 {"event": "task_created", "timestamp": "2026-06-01T00:00:00Z", "metadata": {}},
             ],
-            str(j2.id): [
+            str(j2.job_id): [
                 {"event": "stop_reason_recorded", "timestamp": "2026-06-02T00:00:00Z",
                  "outcome": "open", "metadata": {"stop_reason": "approval_required"}},
             ],
@@ -118,7 +118,7 @@ class TestProjectSummaryOutput:
         proj = self._make_project()
         job = self._make_job()
         job.metadata = {"secret": "sk-secret-key-12345"}
-        events = {str(job.id): [
+        events = {str(job.job_id): [
             {"event": "task_created", "timestamp": "2026-06-01T00:00:00Z",
              "metadata": {"raw_output": "SECRET_CONTENT", "command_output": "LEAKED"}},
         ]}
@@ -140,11 +140,11 @@ class TestProjectSummaryOutput:
         j1 = self._make_job()
         j2 = self._make_job()
         events = {
-            str(j1.id): [
+            str(j1.job_id): [
                 {"event": "stop_reason_recorded", "timestamp": "2026-06-01",
                  "metadata": {"stop_reason": "approval_required"}},
             ],
-            str(j2.id): [
+            str(j2.job_id): [
                 {"event": "stop_reason_recorded", "timestamp": "2026-06-02",
                  "metadata": {"stop_reason": "approval_required"}},
             ],
diff --git a/tests/cli/test_review_cmd.py b/tests/cli/test_review_cmd.py
index d0f8c2ef..5cbc774e 100644
--- a/tests/cli/test_review_cmd.py
+++ b/tests/cli/test_review_cmd.py
@@ -25,8 +25,8 @@ def _recs():
 def test_text_output_shows_created_date(capsys):
     from apps.cli.commands.review_cmd import _cmd_review_list
 
-    job_stub = SimpleNamespace(id=uuid4())
-    args = Namespace(job_id=str(job_stub.id), json=False)
+    job_stub = SimpleNamespace(job_id=uuid4())
+    args = Namespace(job_id=str(job_stub.job_id), json=False)
     with patch("packages.orchestration.pingpong_job.load_job_plan", return_value=job_stub), \
          patch("packages.orchestration.reviewer.list_recommendations", return_value=_recs()):
         _cmd_review_list(args)
@@ -38,8 +38,8 @@ def test_text_output_shows_created_date(capsys):
 def test_json_output_carries_created_at(capsys):
     from apps.cli.commands.review_cmd import _cmd_review_list
 
-    job_stub = SimpleNamespace(id=uuid4())
-    args = Namespace(job_id=str(job_stub.id), json=True)
+    job_stub = SimpleNamespace(job_id=uuid4())
+    args = Namespace(job_id=str(job_stub.job_id), json=True)
     with patch("packages.orchestration.pingpong_job.load_job_plan", return_value=job_stub), \
          patch("packages.orchestration.reviewer.list_recommendations", return_value=_recs()):
         _cmd_review_list(args)
@@ -51,13 +51,13 @@ def test_json_output_carries_created_at(capsys):
 def test_limit_caps_returned_recommendations(capsys):
     from apps.cli.commands.review_cmd import _cmd_review_list
 
-    job_stub = SimpleNamespace(id=uuid4())
+    job_stub = SimpleNamespace(job_id=uuid4())
     recs = [
         {"id": "rec1", "title": "A", "status": "pending", "created_at": "2026-09-01T00:00:00+00:00"},
         {"id": "rec2", "title": "B", "status": "pending", "created_at": "2026-09-02T00:00:00+00:00"},
         {"id": "rec3", "title": "C", "status": "pending", "created_at": "2026-09-03T00:00:00+00:00"},
     ]
-    args = Namespace(job_id=str(job_stub.id), json=True, limit="2")
+    args = Namespace(job_id=str(job_stub.job_id), json=True, limit="2")
     with patch("packages.orchestration.pingpong_job.load_job_plan", return_value=job_stub), \
          patch("packages.orchestration.reviewer.list_recommendations", return_value=recs):
         _cmd_review_list(args)
@@ -69,8 +69,8 @@ def test_limit_caps_returned_recommendations(capsys):
 def test_unknown_sort_field_exits_nonzero():
     from apps.cli.commands.review_cmd import _cmd_review_list
 
-    job_stub = SimpleNamespace(id=uuid4())
-    args = Namespace(job_id=str(job_stub.id), json=True, sort="bogus")
+    job_stub = SimpleNamespace(job_id=uuid4())
+    args = Namespace(job_id=str(job_stub.job_id), json=True, sort="bogus")
     with patch("packages.orchestration.pingpong_job.load_job_plan", return_value=job_stub), \
          patch("packages.orchestration.reviewer.list_recommendations", return_value=_recs()):
         with pytest.raises(SystemExit) as exc:
diff --git a/tests/orchestration/test_handoff.py b/tests/orchestration/test_handoff.py
index bf1277d1..b803fc7a 100644
--- a/tests/orchestration/test_handoff.py
+++ b/tests/orchestration/test_handoff.py
@@ -455,7 +455,7 @@ class _LoopJob:
     """The smallest thing the dispatch seam must return: an id and no plan."""
 
     def __init__(self, job_id: str = "job-0001"):
-        self.id = job_id
+        self.job_id = job_id
         self.flight_plan = None
 
 
diff --git a/tests/orchestration/test_orchestrator_loop.py b/tests/orchestration/test_orchestrator_loop.py
index 5da75afb..dae5f6ed 100644
--- a/tests/orchestration/test_orchestrator_loop.py
+++ b/tests/orchestration/test_orchestrator_loop.py
@@ -529,7 +529,7 @@ class _FakeJob:
     """The smallest thing the dispatch seam has to return: an id and no plan."""
 
     def __init__(self, job_id: str = "job-0001"):
-        self.id = job_id
+        self.job_id = job_id
         self.flight_plan = None
 
 
@@ -1498,7 +1498,7 @@ class TestTheLoopExecutesWhatItDispatches:
 
         self._run(tmp_path, mission, execute, dispatched)
         assert len(seen) == 1, "exactly one execution per dispatch"
-        assert str(seen[0].id) == "job-0001", "the job just created, not another"
+        assert str(seen[0].job_id) == "job-0001", "the job just created, not another"
 
     def test_what_execution_produced_is_on_the_ledger(self, tmp_path, mission,
                                                       dispatched):
diff --git a/tests/orchestration/test_project_summary.py b/tests/orchestration/test_project_summary.py
index 0a388fea..1e572ea6 100644
--- a/tests/orchestration/test_project_summary.py
+++ b/tests/orchestration/test_project_summary.py
@@ -26,15 +26,15 @@ from packages.orchestration.project_summary import (
 
 @dataclass
 class _FakeJob:
-    id: Any = None
+    job_id: Any = None
     state: Any = "planned"
     tasks: list = field(default_factory=list)
     artifacts: list = field(default_factory=list)
     metadata: dict = field(default_factory=dict)
 
     def __post_init__(self):
-        if self.id is None:
-            self.id = uuid4()
+        if self.job_id is None:
+            self.job_id = uuid4()
 
 
 @dataclass
@@ -75,8 +75,8 @@ class TestProjectSummary:
 
     def test_one_job_project(self):
         job = _FakeJob()
-        project = _FakeProject(job_ids=[str(job.id)])
-        events = {str(job.id): [
+        project = _FakeProject(job_ids=[str(job.job_id)])
+        events = {str(job.job_id): [
             {"event": "task_created", "timestamp": "2026-06-01T00:00:00Z", "metadata": {}},
         ]}
         summary = build_project_summary(project, [job], events)
@@ -87,7 +87,7 @@ class TestProjectSummary:
         j1 = _FakeJob(state="completed")
         j2 = _FakeJob(state="blocked")
         j3 = _FakeJob(state="planned")
-        project = _FakeProject(job_ids=[str(j.id) for j in [j1, j2, j3]])
+        project = _FakeProject(job_ids=[str(j.job_id) for j in [j1, j2, j3]])
         summary = build_project_summary(project, [j1, j2, j3], {})
         assert summary.completed_job_count == 1
         assert summary.blocked_job_count == 1
@@ -95,22 +95,22 @@ class TestProjectSummary:
 
     def test_blocked_job_appears_in_blockers(self):
         job = _FakeJob(state="blocked")
-        events = {str(job.id): [
+        events = {str(job.job_id): [
             {"event": "stop_reason_recorded", "timestamp": "2026-06-01T00:00:00Z",
              "outcome": "open", "metadata": {"stop_reason": "approval_required"}},
         ]}
-        project = _FakeProject(job_ids=[str(job.id)])
+        project = _FakeProject(job_ids=[str(job.job_id)])
         summary = build_project_summary(project, [job], events)
         assert len(summary.blockers) >= 1
         assert "approval_required" in summary.blockers[0]
 
     def test_no_raw_leaks(self):
         job = _FakeJob(metadata={"secret_key": "sk-12345"})
-        events = {str(job.id): [
+        events = {str(job.job_id): [
             {"event": "task_created", "timestamp": "2026-06-01T00:00:00Z",
              "metadata": {"raw_output": "SECRET DATA"}},
         ]}
-        project = _FakeProject(job_ids=[str(job.id)])
+        project = _FakeProject(job_ids=[str(job.job_id)])
         summary = build_project_summary(project, [job], events)
         data = export_project_summary_json(summary)
         full = json.dumps(data)
@@ -139,11 +139,11 @@ class TestPatternDetection:
         j1 = _FakeJob()
         j2 = _FakeJob()
         events = {
-            str(j1.id): [
+            str(j1.job_id): [
                 {"event": "stop_reason_recorded", "timestamp": "2026-06-01T00:00:00Z",
                  "metadata": {"stop_reason": "approval_required"}},
             ],
-            str(j2.id): [
+            str(j2.job_id): [
                 {"event": "stop_reason_recorded", "timestamp": "2026-06-02T00:00:00Z",
                  "metadata": {"stop_reason": "approval_required"}},
             ],
@@ -157,11 +157,11 @@ class TestPatternDetection:
         j1 = _FakeJob()
         j2 = _FakeJob()
         events = {
-            str(j1.id): [
+            str(j1.job_id): [
                 {"event": "patch_intent_applied", "timestamp": "2026-06-01",
                  "metadata": {"target_path": "app.py"}},
             ],
-            str(j2.id): [
+            str(j2.job_id): [
                 {"event": "patch_intent_applied", "timestamp": "2026-06-02",
                  "metadata": {"target_path": "app.py"}},
             ],
@@ -175,11 +175,11 @@ class TestPatternDetection:
         j1 = _FakeJob()
         j2 = _FakeJob()
         events = {
-            str(j1.id): [
+            str(j1.job_id): [
                 {"event": "builder_patch_parsed", "timestamp": "2026-06-01",
                  "metadata": {"parse_success": False, "error_kind": "prose_only"}},
             ],
-            str(j2.id): [
+            str(j2.job_id): [
                 {"event": "builder_patch_parsed", "timestamp": "2026-06-02",
                  "metadata": {"parse_success": False, "error_kind": "prose_only"}},
             ],
@@ -190,7 +190,7 @@ class TestPatternDetection:
 
     def test_single_occurrence_low_severity(self):
         job = _FakeJob()
-        events = {str(job.id): [
+        events = {str(job.job_id): [
             {"event": "stop_reason_recorded", "timestamp": "2026-06-01",
              "metadata": {"stop_reason": "test_failed_after_apply"}},
         ]}
@@ -199,7 +199,7 @@ class TestPatternDetection:
 
     def test_no_raw_leaks_in_patterns(self):
         j1 = _FakeJob()
-        events = {str(j1.id): [
+        events = {str(j1.job_id): [
             {"event": "stop_reason_recorded", "timestamp": "2026-06-01",
              "metadata": {"stop_reason": "test_failed", "raw_output": "LEAKED"}},
             {"event": "stop_reason_recorded", "timestamp": "2026-06-02",
@@ -321,11 +321,11 @@ class TestStrongerPatterns:
         j1 = _FakeJob()
         j2 = _FakeJob()
         events = {
-            str(j1.id): [
+            str(j1.job_id): [
                 {"event": "test_run_completed", "timestamp": "2026-06-01",
                  "metadata": {"status": "failed"}},
             ],
-            str(j2.id): [
+            str(j2.job_id): [
                 {"event": "test_run_completed", "timestamp": "2026-06-02",
                  "metadata": {"status": "failed"}},
             ],
@@ -339,11 +339,11 @@ class TestStrongerPatterns:
         j1 = _FakeJob()
         j2 = _FakeJob()
         events = {
-            str(j1.id): [
+            str(j1.job_id): [
                 {"event": "stop_reason_recorded", "timestamp": "2026-06-01",
                  "metadata": {"stop_reason": "permission_denied"}},
             ],
-            str(j2.id): [
+            str(j2.job_id): [
                 {"event": "stop_reason_recorded", "timestamp": "2026-06-02",
                  "metadata": {"stop_reason": "permission_denied"}},
             ],
@@ -356,11 +356,11 @@ class TestStrongerPatterns:
         j1 = _FakeJob()
         j2 = _FakeJob()
         events = {
-            str(j1.id): [
+            str(j1.job_id): [
                 {"event": "stop_reason_recorded", "timestamp": "2026-06-01",
                  "metadata": {"stop_reason": "provider_unavailable"}},
             ],
-            str(j2.id): [
+            str(j2.job_id): [
                 {"event": "stop_reason_recorded", "timestamp": "2026-06-02",
                  "metadata": {"stop_reason": "provider_unavailable"}},
             ],
@@ -372,7 +372,7 @@ class TestStrongerPatterns:
     def test_repeated_repair_exhaustion(self):
         j1 = _FakeJob()
         events = {
-            str(j1.id): [
+            str(j1.job_id): [
                 {"event": "repair_loop_stopped", "timestamp": "2026-06-01",
                  "metadata": {"reason": "repair_budget_exhausted"}},
                 {"event": "repair_loop_stopped", "timestamp": "2026-06-02",
@@ -385,7 +385,7 @@ class TestStrongerPatterns:
 
     def test_one_off_not_over_severity(self):
         job = _FakeJob()
-        events = {str(job.id): [
+        events = {str(job.job_id): [
             {"event": "test_run_completed", "timestamp": "2026-06-01",
              "metadata": {"status": "failed"}},
         ]}
```
