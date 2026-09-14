# F275 round 90 — the flip's first overlay

An OVERLAY is an edit that is right only once the classic job record is gone, carried as one unified
diff instead of being committed to the production tree. It is not applied to the repository as it
stands: its context lines are the bytes of the FLIPPED tree, and it holds only against that tree.

Base: `844a7f21`. The flipped tree is that commit checked out and then transformed exactly as G4 of
`.agent/authored/f275-r90.md` orders: the committed generator re-derives the TIP re-keyed set from the
two pinned round 77 JSON files, and the guarded transform runs over the checkout with that set, its
owners file and `r61_status.json`.

This is the FIRST overlay. Every later overlay is taken against the flipped tree with this one and
every overlay before it already applied, and is applied after them, in round order.

What it changes. `_load_job` in `packages/orchestration/ui_server.py` checks the id with
`normalize_job_id` and loads every well-formed id from the one store through `load_job_plan`, with no
`UUID(...)` call and no adapter; the module-level `from uuid import UUID` it left unused is deleted.
Eighteen string `getattr` reads of `id`, `name` or `description` on a job or a task, in nine modules,
take the transform's own names `job_id`, `job_title`, `task_id` and `title`. The two duck-typed doubles
of `tests/orchestration/test_run_report.py` carry the unified names.

How to apply it, inside the flipped tree:

1. Extract the fence below: the lines strictly between the line of three backticks followed by
   `diff` and the closing line of three backticks, each line kept with its newline.
2. Run `git apply --check <extracted file>` and require exit 0.
3. Run `git apply <extracted file>`.

```diff
diff --git a/apps/cli/commands/repo.py b/apps/cli/commands/repo.py
index 9195da45..cbdc17d2 100644
--- a/apps/cli/commands/repo.py
+++ b/apps/cli/commands/repo.py
@@ -29,7 +29,7 @@ def _safe_task_label(task: Any) -> str:
         if isinstance(val, str) and val.strip():
             return val.strip()[:60].replace("\n", " ")
 
-    desc = getattr(task, "description", None)
+    desc = getattr(task, "title", None)
     if isinstance(desc, str) and desc.strip():
         return desc.strip().split("\n")[0][:60]
 
diff --git a/packages/orchestration/diff_repair_apply.py b/packages/orchestration/diff_repair_apply.py
index ba5b9a7b..7ef73d78 100644
--- a/packages/orchestration/diff_repair_apply.py
+++ b/packages/orchestration/diff_repair_apply.py
@@ -152,7 +152,7 @@ def apply_diff_repair(
         patch,
         Path(repo_path),
         data_dir=str(data_dir) if data_dir else None,
-        job_id=getattr(job, "id", None),
+        job_id=getattr(job, "job_id", None),
         job=job,
         intent_id=intent_id,
     )
diff --git a/packages/orchestration/job_digest.py b/packages/orchestration/job_digest.py
index 5a61357c..f9b01af5 100644
--- a/packages/orchestration/job_digest.py
+++ b/packages/orchestration/job_digest.py
@@ -139,7 +139,7 @@ def _cost_counters(job: Any) -> Any | None:
         )
         from packages.orchestration.pingpong_job import load_job_plan
 
-        job_id = str(getattr(job, "id", "") or "")
+        job_id = str(getattr(job, "job_id", "") or "")
         plan = load_job_plan(job_id) if job_id else None
         actuals = getattr(plan, "budget_actuals", None) if plan is not None else None
         if actuals is None:
diff --git a/packages/orchestration/mission_state.py b/packages/orchestration/mission_state.py
index f461dae5..f887304d 100644
--- a/packages/orchestration/mission_state.py
+++ b/packages/orchestration/mission_state.py
@@ -754,7 +754,7 @@ def build_verify_first_task(previous_job: Any) -> Any:
     from packages.core.models import AcceptanceCheck, RunState
     from packages.orchestration.pingpong_job import TaskEntry
 
-    previous_id = str(getattr(previous_job, "id", "") or "")
+    previous_id = str(getattr(previous_job, "job_id", "") or "")
     command = resolve_verify_command(previous_job)
     described = command or "no verification command recorded"
     return TaskEntry(
diff --git a/packages/orchestration/patch_apply.py b/packages/orchestration/patch_apply.py
index 133edb2a..5d2a8bcb 100644
--- a/packages/orchestration/patch_apply.py
+++ b/packages/orchestration/patch_apply.py
@@ -200,7 +200,7 @@ def apply_patch_intent(
             repo_root,
             [_TouchedPath(path=target_path, operation=action, role="target")],
             applicator="patch_apply",
-            job_id=str(getattr(job, "id", "")),
+            job_id=str(getattr(job, "job_id", "")),
             intent_id=intent_id,
             evidence_dir=data_dir,
             job_fences=_job_fences,
diff --git a/packages/orchestration/real_test_execution.py b/packages/orchestration/real_test_execution.py
index ee58e819..d226e3f8 100644
--- a/packages/orchestration/real_test_execution.py
+++ b/packages/orchestration/real_test_execution.py
@@ -334,7 +334,7 @@ def get_test_run(test_run_id: str, data_dir: Path | None = None) -> dict | None:
     try:
         from packages.orchestration.pingpong_job import list_job_plans, load_job_plan
         for jref in list_job_plans(ddir):
-            jid = jref.get("id") if isinstance(jref, dict) else getattr(jref, "id", None)
+            jid = jref.get("id") if isinstance(jref, dict) else getattr(jref, "job_id", None)
             if jid is None:
                 continue
             try:
diff --git a/packages/orchestration/repo_applicator.py b/packages/orchestration/repo_applicator.py
index 2233a521..64823851 100644
--- a/packages/orchestration/repo_applicator.py
+++ b/packages/orchestration/repo_applicator.py
@@ -228,7 +228,7 @@ def check_and_apply_to_repo(
 
     from packages.orchestration.data_paths import resolve_data_root
     _evidence_dir = resolve_data_root()
-    _job_id = str(getattr(job, "id", "") or "")
+    _job_id = str(getattr(job, "job_id", "") or "")
 
     return apply_task_output_to_repo(
         artifact, repo_root,
diff --git a/packages/orchestration/run_report.py b/packages/orchestration/run_report.py
index a291053d..387d69e6 100644
--- a/packages/orchestration/run_report.py
+++ b/packages/orchestration/run_report.py
@@ -758,7 +758,7 @@ def _job_repo_root(job: Any) -> str:
     try:
         from packages.orchestration.pingpong_job import load_job_plan
 
-        plan = load_job_plan(str(getattr(job, "id", "") or ""))
+        plan = load_job_plan(str(getattr(job, "job_id", "") or ""))
     except Exception:  # noqa: BLE001 — a report must not depend on the plan store
         return ""
     return str(getattr(plan, "repo_path", "") or "") if plan is not None else ""
@@ -778,8 +778,8 @@ def collect_report_sources(job: Any) -> ReportSources:
 
     tasks = tuple(
         TaskOutcome(
-            task_id=str(getattr(t, "id", ""))[:8],
-            description=str(getattr(t, "description", "") or ""),
+            task_id=str(getattr(t, "task_id", ""))[:8],
+            description=str(getattr(t, "title", "") or ""),
             status=getattr(getattr(t, "status", None), "value",
                            str(getattr(t, "status", "") or "")),
         )
@@ -787,8 +787,8 @@ def collect_report_sources(job: Any) -> ReportSources:
     )
     metadata = getattr(job, "metadata", None) or {}
     return ReportSources(
-        job_id=str(getattr(job, "id", "") or ""),
-        job_name=str(getattr(job, "name", "") or ""),
+        job_id=str(getattr(job, "job_id", "") or ""),
+        job_name=str(getattr(job, "job_title", "") or ""),
         project_id=str(getattr(job, "project_id", "") or ""),
         mission=str(getattr(job, "mission", "") or ""),
         loop_ref=str(metadata.get(LOOP_REF_METADATA_KEY, "") or ""),
@@ -813,7 +813,7 @@ def _evidence_sources(job: Any) -> dict[str, Any]:
     report the others.  A source that cannot be read is simply absent, and
     absent renders "not recorded" — the same rule everywhere (P6).
     """
-    job_id = str(getattr(job, "id", "") or "")
+    job_id = str(getattr(job, "job_id", "") or "")
     extra: dict[str, Any] = {}
 
     try:
@@ -916,7 +916,7 @@ def _folded_apply_states(job: Any) -> dict[str, Any]:
         )
         from packages.orchestration.timeline import load_run_events
 
-        job_id = str(getattr(job, "id", "") or "")
+        job_id = str(getattr(job, "job_id", "") or "")
         if not job_id:
             return {}
         data_dir = resolve_data_root()
@@ -943,7 +943,7 @@ def _tasks_with_apply_state(job: Any, tasks: tuple[TaskOutcome, ...]
     folded = _folded_apply_states(job)
     if not folded or not tasks:
         return None
-    full_ids = [str(getattr(t, "id", "") or "")
+    full_ids = [str(getattr(t, "task_id", "") or "")
                 for t in (getattr(job, "tasks", None) or ())]
     if len(full_ids) != len(tasks):
         # The two iterations disagree, so the pairing is not knowable.  Saying
@@ -1004,7 +1004,7 @@ def write_final_report(job: Any, *, sources: ReportSources | None = None) -> Pat
     account of the run, and losing the account must not lose the run.
     """
     try:
-        job_id = str(getattr(job, "id", "") or "")
+        job_id = str(getattr(job, "job_id", "") or "")
         text = render_report_from_sources(
             sources if sources is not None else build_report_sources(job),
             mode=MODE_FINAL)
diff --git a/packages/orchestration/source_apply.py b/packages/orchestration/source_apply.py
index 3ca80338..c7b0715f 100644
--- a/packages/orchestration/source_apply.py
+++ b/packages/orchestration/source_apply.py
@@ -263,14 +263,14 @@ def apply_structured_patch(
         enforce_change_set(
             repo_root, touched,
             applicator="source_apply",
-            job_id=str(getattr(job, "id", None) or job_id or "unknown"),
+            job_id=str(getattr(job, "job_id", None) or job_id or "unknown"),
             intent_id=intent_id or "",
             evidence_dir=Path(data_dir) if data_dir else resolve_data_root(),
             job_fences=_job_fences,
         )
 
     data_dir_path = Path(data_dir) if data_dir else resolve_data_root()
-    job_id_str = str(getattr(job, "id", None) or job_id or "unknown")
+    job_id_str = str(getattr(job, "job_id", None) or job_id or "unknown")
 
     # Mandatory snapshot: derive path set, create, verify — block if any step fails
     path_set = build_snapshot_path_set(patch)
diff --git a/packages/orchestration/ui_server.py b/packages/orchestration/ui_server.py
index 9c8f4dac..b0bf978d 100644
--- a/packages/orchestration/ui_server.py
+++ b/packages/orchestration/ui_server.py
@@ -33,7 +33,6 @@ from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
 from pathlib import Path
 from typing import Any
 from urllib.parse import parse_qs, urlparse
-from uuid import UUID
 
 # ---------------------------------------------------------------------------
 # Path sanitization (no absolute path leaks in dashboard JSON)
@@ -230,39 +229,23 @@ def _safe_error(code: int, message: str) -> tuple[int, dict[str, Any]]:
 
 
 def _load_job(job_id_str: str) -> Any:
-    """Load a Job by UUID or JobPlan hex ID, return (job, error_tuple)."""
-    import re
+    """Load a job record by id, return (job, error_tuple)."""
+    from packages.orchestration.data_paths import JobIdInvalid, normalize_job_id
+    from packages.orchestration.pingpong_job import load_job_plan
 
-    uuid_was_valid = False
-    # Try core UUID job first
     try:
-        job_id = UUID(job_id_str)
-        uuid_was_valid = True
-        from packages.orchestration.storage import JobNotFoundError, JobStoreError
-        from packages.orchestration.pingpong_job import load_job_plan
+        job_id = normalize_job_id(job_id_str)
+    except JobIdInvalid:
+        if re.fullmatch(r"[0-9a-fA-F]+", job_id_str):
+            return None, _safe_error(404, "job not found")
+        return None, _safe_error(400, "invalid job id")
+    try:
         job = load_job_plan(job_id)
-        return job, None
-    except ValueError:
-        pass
-    except (FileNotFoundError, ImportError, JobNotFoundError, JobStoreError):
-        pass
-
-    # Valid UUID that wasn't found — 404 not 400
-    if uuid_was_valid:
+    except OSError:
+        job = None
+    if job is None:
         return None, _safe_error(404, "job not found")
-
-    # Try job-flow JobPlan short hex ID (must look like hex)
-    if re.fullmatch(r"[0-9a-fA-F]+", job_id_str):
-        try:
-            from packages.orchestration.pingpong_job import load_job_plan
-            plan = load_job_plan(job_id_str)
-            if plan is not None:
-                return _JobPlanAdapter(plan), None
-        except (ImportError, OSError):
-            pass
-        return None, _safe_error(404, "job not found")
-
-    return None, _safe_error(400, "invalid job id")
+    return job, None
 
 
 def _task_test_status(task_id: str, events: list[dict]) -> str:
diff --git a/tests/orchestration/test_run_report.py b/tests/orchestration/test_run_report.py
index 96b5c7b7..e7ae691d 100644
--- a/tests/orchestration/test_run_report.py
+++ b/tests/orchestration/test_run_report.py
@@ -974,7 +974,7 @@ class TestTheApplyStateIsAttachedByTheFullTaskId:
 
     def test_two_tasks_sharing_eight_id_characters_keep_their_own_state(
             self, monkeypatch):
-        """``TaskOutcome.task_id`` is ``str(t.id)[:8]`` — a TRUNCATION.
+        """``TaskOutcome.task_id`` is ``str(t.task_id)[:8]`` — a TRUNCATION.
 
         The fold keys on the FULL id. An attach that looked the state up by the
         truncated value would give these two tasks each other's answer (or, with
@@ -1102,17 +1102,17 @@ def _public_api_block(docstring: str) -> str:
 
 class _FakeTask:
     def __init__(self, task_id: str, description: str, status: str):
-        self.id = task_id
-        self.description = description
+        self.task_id = task_id
+        self.title = description
         self.status = status
 
 
 class _FakeJob:
-    """The duck-typed shape collect_report_sources reads off a core Job."""
+    """The duck-typed shape collect_report_sources reads off a job record."""
 
     def __init__(self):
-        self.id = "44444444-4444-4444-8444-444444444444"
-        self.name = "fake job"
+        self.job_id = "44444444-4444-4444-8444-444444444444"
+        self.job_title = "fake job"
         self.project_id = "remedy"
         self.mission = "Do the thing"
         self.state = "completed"
```
