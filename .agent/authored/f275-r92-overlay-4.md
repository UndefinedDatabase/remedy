# F275 round 92 — the flip's third overlay, part 4 of 4

What the third overlay changes. `packages/orchestration/pingpong_job.py` gains
`require_job_plan`, a raising loader over `load_job_plan_safe`: it raises `JobStoreError` for a
record that exists and cannot be read and `JobNotFoundError(job_id)` for a job with no record.
Every call of `load_job_plan` under `packages/` and `apps/` that lies in the body of a `try` whose
handler names `JobNotFoundError` calls `require_job_plan` instead, and its import follows; the
alias `_load_job` in `repository_snapshot.revert_repository_apply` imports it too. In
`apps/cli/commands/job_context_cmd.py` the second load of the same id, its duplicate import and
the comment sentence explaining its order are deleted. `revert_repository_apply` and
`test_execution_service.execute_test_run` check the id with `normalize_job_id` in place of
`UUID(...)`. Under `tests/`, `test_unified_store_parity.py` gains three tests of the new loader,
and the fixtures of `test_escalation.py` and `test_workspace.py` give their tasks ids.

This part holds 5 whole file diffs, `packages/orchestration/test_execution_service.py` through `tests/test_workspace.py`.

Base: `844a7f21`. The flipped tree is that commit checked out and then built exactly as G4 of
`.agent/authored/f275-r92.md` orders: the committed generator re-derives the TIP re-keyed set from
the two pinned round 77 JSON files, the guarded transform runs over the checkout with that set, its
owners file and `r61_status.json`, and the result is staged.

The 4 parts form the THIRD overlay. They apply after `.agent/authored/f275-r91-overlay.md`,
which applies after `.agent/authored/f275-r90-overlay.md`; each of those two is applied to the
staged flipped tree and staged in turn, and the third overlay's diff was taken against that state.
The parts apply in `<k>` order, part 1 first; joined in that order their fences are that one diff.

How to apply this part, inside the flipped tree with both earlier overlays applied and staged and
every part before this one applied:

1. Extract the fence below: the lines strictly between the line of three backticks followed by
   `diff` and the closing line of three backticks, each line kept with its newline.
2. Run `git apply --check <extracted file>` and require exit 0.
3. Run `git apply <extracted file>`.

```diff
diff --git a/packages/orchestration/test_execution_service.py b/packages/orchestration/test_execution_service.py
index 6fe5771c..a9304c05 100644
--- a/packages/orchestration/test_execution_service.py
+++ b/packages/orchestration/test_execution_service.py
@@ -52,7 +52,7 @@ from packages.orchestration.command_discovery import (
     discover_commands,
     select_best_test_candidate,
 )
-from packages.orchestration.data_paths import resolve_data_root
+from packages.orchestration.data_paths import normalize_job_id, resolve_data_root
 from packages.orchestration.exec_guard import ExecGuardPolicy, plan_child_spawn
 from packages.orchestration.permissions import Capability, is_allowed
 from packages.orchestration.run_contract import (
@@ -65,7 +65,7 @@ from packages.orchestration.run_contract import (
     validate_run_contract,
 )
 from packages.orchestration.storage import JobNotFoundError
-from packages.orchestration.pingpong_job import load_job_plan, save_job_plan
+from packages.orchestration.pingpong_job import load_job_plan, require_job_plan, save_job_plan
 from packages.orchestration.test_runner import _EXECUTION_SAFE_EXECUTABLES
 
 # ---------------------------------------------------------------------------
@@ -583,7 +583,7 @@ def execute_test_run(
 
     # ── Gate 1: Load job ────────────────────────────────────────────────────
     try:
-        job_id_parsed = UUID(request.job_id)
+        job_id_parsed = normalize_job_id(request.job_id)
     except ValueError:
         result.status = "blocked"
         result.stop_reason = "invalid_job_id"
@@ -592,7 +592,7 @@ def execute_test_run(
         return result
 
     try:
-        job = load_job_plan(job_id_parsed, data_dir)
+        job = require_job_plan(job_id_parsed, data_dir)
     except JobNotFoundError:
         result.status = "blocked"
         result.stop_reason = "job_not_found"
diff --git a/packages/orchestration/worker_queue.py b/packages/orchestration/worker_queue.py
index f3ad4599..2ae9dc67 100644
--- a/packages/orchestration/worker_queue.py
+++ b/packages/orchestration/worker_queue.py
@@ -430,7 +430,7 @@ def _run_via_task_execution(
     """Execute one pending Job.tasks item through the modular task_execution port."""
     from packages.core.models import RunState
     from packages.orchestration.storage import JobNotFoundError, JobStoreError
-    from packages.orchestration.pingpong_job import load_job_plan, save_job_plan
+    from packages.orchestration.pingpong_job import require_job_plan, save_job_plan
     from packages.orchestration.task_execution import BudgetGate, TaskExecutionRequest, execute_task
 
     root = Path(data_dir)
@@ -449,7 +449,7 @@ def _run_via_task_execution(
     result.budget_status = "ok"
 
     try:
-        job = load_job_plan(entry.job_id, root)
+        job = require_job_plan(entry.job_id, root)
     except JobNotFoundError:
         transition_state(entry.job_id, "blocked", data_dir, blocked_reason="job_not_found")
         result.last_lifecycle_state = "blocked"
@@ -582,8 +582,8 @@ def _run_via_legacy_autorun(
     try:
         from packages.orchestration.autorun import run_autorun
         from packages.orchestration.storage import JobNotFoundError
-        from packages.orchestration.pingpong_job import load_job_plan
-        job = load_job_plan(entry.job_id)
+        from packages.orchestration.pingpong_job import require_job_plan
+        job = require_job_plan(entry.job_id)
         ar = run_autorun(job, builder_provider=provider, data_dir=str(data_dir))
         stage = ar.stage if hasattr(ar, "stage") else ""
         stop = ar.stop_reason if hasattr(ar, "stop_reason") else ""
diff --git a/tests/orchestration/test_escalation.py b/tests/orchestration/test_escalation.py
index f13d3b56..e537ba40 100644
--- a/tests/orchestration/test_escalation.py
+++ b/tests/orchestration/test_escalation.py
@@ -62,7 +62,7 @@ def make_job(task_count: int = 2, *, name: str = "escalation-job") -> JobPlan:
     return JobPlan(
         job_title=name,
         user_prompt="build the thing",
-        tasks=[TaskEntry(title=f"task {i}", inputs={"task_type": "documentation"})
+        tasks=[TaskEntry(task_id=f"T{i + 1:03d}", title=f"task {i}", inputs={"task_type": "documentation"})
                for i in range(task_count)],
         state=RunState.PLANNED,
     )
diff --git a/tests/orchestration/test_unified_store_parity.py b/tests/orchestration/test_unified_store_parity.py
index dd4e4db3..68bb36aa 100644
--- a/tests/orchestration/test_unified_store_parity.py
+++ b/tests/orchestration/test_unified_store_parity.py
@@ -36,8 +36,10 @@ from packages.orchestration.pingpong_job import (
     list_job_plans_safe,
     load_job_plan,
     load_job_plan_safe,
+    require_job_plan,
     save_job_plan,
 )
+from packages.orchestration.storage import JobNotFoundError, JobStoreError
 
 
 def _plan(job_id: str, created_at: str = "2026-09-10T12:00:00+00:00") -> JobPlan:
@@ -156,6 +158,31 @@ class TestCorruptionVisibilityOfOneRecord:
         assert rotten_safe == (None, True)
 
 
+class TestTheRaisingLoader:
+    """The raising loader answers a caller that catches the way the classic loader did."""
+
+    def test_h2_an_absent_record_raises_job_not_found_naming_the_id_asked_for(
+        self, tmp_path: Path
+    ) -> None:
+        with pytest.raises(JobNotFoundError) as caught:
+            require_job_plan("dddd000000000001", tmp_path)
+
+        assert caught.value.job_id == "dddd000000000001"
+
+    def test_h3_an_unreadable_record_raises_job_store_error(self, tmp_path: Path) -> None:
+        _corrupt(tmp_path, "dddd000000000002")
+
+        with pytest.raises(JobStoreError):
+            require_job_plan("dddd000000000002", tmp_path)
+
+    def test_h4_a_saved_record_comes_back_equal_to_what_the_plain_reader_reads(
+        self, tmp_path: Path
+    ) -> None:
+        save_job_plan(_plan("dddd000000000003"), tmp_path)
+
+        assert require_job_plan("dddd000000000003", tmp_path) == load_job_plan("dddd000000000003", tmp_path)
+
+
 class TestListingTheUnifiedStore:
     """W3: the unified store can be enumerated, newest first, with skips named."""
 
diff --git a/tests/test_workspace.py b/tests/test_workspace.py
index 37e0e199..5197de44 100644
--- a/tests/test_workspace.py
+++ b/tests/test_workspace.py
@@ -31,7 +31,7 @@ from packages.orchestration.workspace import LocalWorkspaceRuntime, Materialized
 
 
 def _make_planned_job(task_type: str = "write_code") -> JobPlan:
-    task = TaskEntry(title="Do some work.", inputs={"task_type": task_type})
+    task = TaskEntry(task_id="T001", title="Do some work.", inputs={"task_type": task_type})
     return JobPlan(job_title="test-job", tasks=[task], state=RunState.PLANNED)
 
 
```
