# F275 round 98 — the flip's ninth overlay, part 1 of 1

What the ninth overlay changes. Thirteen job loads sit in a `try` whose `except Exception`
handler reports the job missing or unreadable, and the name each binds is read after that `try`
with no `None` test. They call `require_job_plan`, the unified store's raising loader, with the
same arguments in place of `load_job_plan`, which answers `None` for a missing job; the local
`pingpong_job` import of each function names `require_job_plan` in its place, and
`start_repair_loop_v0`, whose second load stays, imports both. The calls are in `contract_cmd.py`,
`repo.py`, `test_cmds.py`, `orchestrator_loop.py`, `real_test_execution.py`, `repair_loop.py` and
`watchdog.py`. `create_test_env` in `tests/cli/runtime_helpers.py` writes its job as
`jobs/<job id>/job.json` with the unified record's `job_id`, `job_title` and `status` keys and an
empty `user_prompt`, and the two readers of that file in `tests/cli/test_test_run_runtime.py`
follow the path.

This part holds 9 whole file diffs, `apps/cli/commands/contract_cmd.py` through `tests/cli/test_test_run_runtime.py`.

Base: `844a7f21`. The flipped tree is that commit checked out and then built exactly as G4 of
`.agent/authored/f275-r98.md` orders: the committed generator re-derives the TIP re-keyed set from
the two pinned round 77 JSON files, the guarded transform runs over the checkout with that set, its
owners file and `r61_status.json`, and the result is staged.

The NINTH overlay is formed by 1 part, and this is part 1. The parts apply after
`.agent/authored/f275-r97-overlay-1.md`: `.agent/authored/f275-r90-overlay.md`, then
`.agent/authored/f275-r91-overlay.md`, then `.agent/authored/f275-r92-overlay-1.md` through
`-4.md`, then `.agent/authored/f275-r93-overlay-1.md` and `-2.md`, then
`.agent/authored/f275-r94-overlay-1.md` and `-2.md`, then `.agent/authored/f275-r95-overlay-1.md`
through `-4.md`, then `.agent/authored/f275-r96-overlay-1.md`, then
`.agent/authored/f275-r97-overlay-1.md` are applied to the staged flipped tree overlay by overlay,
each overlay staged in turn, and the ninth overlay's diff was taken against that state. The parts
apply in `<k>` order, part 1 first; joined in that order their fences are that one diff.

How to apply this part, inside the flipped tree with every earlier overlay applied and staged and
every part before this one applied:

1. Extract the fence below: the lines strictly between the line of three backticks followed by
   `diff` and the closing line of three backticks, each line kept with its newline.
2. Run `git apply --check <extracted file>` and require exit 0.
3. Run `git apply <extracted file>`.

```diff
diff --git a/apps/cli/commands/contract_cmd.py b/apps/cli/commands/contract_cmd.py
index 068c5356..455de2d5 100644
--- a/apps/cli/commands/contract_cmd.py
+++ b/apps/cli/commands/contract_cmd.py
@@ -14,7 +14,7 @@ def _cmd_contract_inspect(args: Any) -> None:
         export_run_contract_json,
         summarize_run_contract,
     )
-    from packages.orchestration.pingpong_job import load_job_plan, save_job_plan
+    from packages.orchestration.pingpong_job import require_job_plan, save_job_plan
 
     job_id = getattr(args, "job_id", "")
     if not job_id:
@@ -22,7 +22,7 @@ def _cmd_contract_inspect(args: Any) -> None:
         sys.exit(1)
 
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except Exception:
         msg = f"Job {job_id[:8]} not found"
         if getattr(args, "json", False):
@@ -47,7 +47,7 @@ def _cmd_contract_check(args: Any) -> None:
         evaluate_run_action,
         export_run_action_decision_json,
     )
-    from packages.orchestration.pingpong_job import load_job_plan, save_job_plan
+    from packages.orchestration.pingpong_job import require_job_plan, save_job_plan
 
     job_id = getattr(args, "job_id", "")
     action = getattr(args, "action", "")
@@ -61,7 +61,7 @@ def _cmd_contract_check(args: Any) -> None:
         sys.exit(1)
 
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except Exception:
         msg = f"Job {job_id[:8]} not found"
         if getattr(args, "json", False):
@@ -98,7 +98,7 @@ def _cmd_contract_set(args: Any) -> None:
         save_contract,
         validate_run_contract,
     )
-    from packages.orchestration.pingpong_job import load_job_plan, save_job_plan
+    from packages.orchestration.pingpong_job import require_job_plan, save_job_plan
 
     job_id = getattr(args, "job_id", "")
     field_name = getattr(args, "field", "")
@@ -128,7 +128,7 @@ def _cmd_contract_set(args: Any) -> None:
         sys.exit(1)
 
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except Exception:
         msg = f"Job {job_id[:8]} not found"
         if getattr(args, "json", False):
diff --git a/apps/cli/commands/repo.py b/apps/cli/commands/repo.py
index 08a83998..0bc7eceb 100644
--- a/apps/cli/commands/repo.py
+++ b/apps/cli/commands/repo.py
@@ -167,11 +167,11 @@ def _cmd_commit_readiness(
     """Preview commit readiness — read-only, no git writes."""
     from packages.orchestration.data_paths import resolve_data_root
     from packages.orchestration.git_status import read_git_status
-    from packages.orchestration.pingpong_job import load_job_plan
+    from packages.orchestration.pingpong_job import require_job_plan
     from packages.orchestration.timeline import load_run_events
 
     try:
-        job = load_job_plan(lookup_job_id(job_id_str))
+        job = require_job_plan(lookup_job_id(job_id_str))
     except Exception:
         print(f"Error: job not found: {job_id_str}", file=sys.stderr)
         sys.exit(1)
diff --git a/apps/cli/commands/test_cmds.py b/apps/cli/commands/test_cmds.py
index 0aa93dcb..c8c632e7 100644
--- a/apps/cli/commands/test_cmds.py
+++ b/apps/cli/commands/test_cmds.py
@@ -102,8 +102,8 @@ def _cmd_discover_commands(job_id_str: str, *, as_json: bool) -> None:
         print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
         sys.exit(1)
     try:
-        from packages.orchestration.pingpong_job import load_job_plan
-        job = load_job_plan(job_id)
+        from packages.orchestration.pingpong_job import require_job_plan
+        job = require_job_plan(job_id)
     except Exception as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
diff --git a/packages/orchestration/orchestrator_loop.py b/packages/orchestration/orchestrator_loop.py
index ffff590f..8f716447 100644
--- a/packages/orchestration/orchestrator_loop.py
+++ b/packages/orchestration/orchestrator_loop.py
@@ -368,12 +368,12 @@ def open_mission_decisions(mission: Any) -> list[dict[str, Any]]:
     """
     from packages.orchestration.data_paths import normalize_job_id
     from packages.orchestration.escalation import open_task_decisions
-    from packages.orchestration.pingpong_job import load_job_plan
+    from packages.orchestration.pingpong_job import require_job_plan
 
     out: list[dict[str, Any]] = []
     for link in getattr(mission, "job_links", ()) or ():
         try:
-            job = load_job_plan(normalize_job_id(link.job_id))
+            job = require_job_plan(normalize_job_id(link.job_id))
         except Exception:
             # A job that cannot be read cannot be asked about its decisions.
             # Recorded as absent rather than raised: one unreadable job must
@@ -1726,7 +1726,7 @@ def collect_milestone_evidence(project_id: str, mission_id: str,
     """Read a milestone's evidence through the existing job and gate verbs."""
     from packages.orchestration.data_paths import normalize_job_id
     from packages.orchestration.dod_gate import load_gate_result
-    from packages.orchestration.pingpong_job import load_job_plan
+    from packages.orchestration.pingpong_job import require_job_plan
 
     job_id = dispatched_job_for(project_id, mission_id, milestone_id, root)
     if not job_id:
@@ -1735,7 +1735,7 @@ def collect_milestone_evidence(project_id: str, mission_id: str,
     state = ""
     handback: Any = None
     try:
-        job = load_job_plan(normalize_job_id(job_id))
+        job = require_job_plan(normalize_job_id(job_id))
     except Exception:
         # An unreadable job is an ABSENT observation, never a passing one.
         return MilestoneEvidence(job_id=job_id)
@@ -1919,7 +1919,7 @@ def escalate_repeated_refusal(project_id: str, mission_id: str, reason: str, *,
     from packages.orchestration.data_paths import normalize_job_id
     from packages.orchestration.escalation import enqueue_task_decision
     from packages.orchestration.mission_state import load_mission
-    from packages.orchestration.pingpong_job import load_job_plan, save_job_plan
+    from packages.orchestration.pingpong_job import require_job_plan, save_job_plan
 
     mission = load_mission(project_id, mission_id, root)
     link = mission.latest_link()
@@ -1927,7 +1927,7 @@ def escalate_repeated_refusal(project_id: str, mission_id: str, reason: str, *,
         return ("no job is linked to this mission, so the refusal cannot be "
                 "attached to a decision — a human has to look at the mission")
     try:
-        job = load_job_plan(normalize_job_id(link.job_id))
+        job = require_job_plan(normalize_job_id(link.job_id))
     except Exception as exc:
         return f"the mission's latest job could not be read to escalate: {exc}"
     tasks = list(getattr(job, "tasks", ()) or ())
diff --git a/packages/orchestration/real_test_execution.py b/packages/orchestration/real_test_execution.py
index d226e3f8..b1706a07 100644
--- a/packages/orchestration/real_test_execution.py
+++ b/packages/orchestration/real_test_execution.py
@@ -225,8 +225,8 @@ def resolve_allowed_command(
     ddir = _resolve_ddir(data_dir)
     try:
         from packages.orchestration.command_discovery import discover_commands
-        from packages.orchestration.pingpong_job import load_job_plan
-        job = load_job_plan(normalize_job_id(job_id), ddir)
+        from packages.orchestration.pingpong_job import require_job_plan
+        job = require_job_plan(normalize_job_id(job_id), ddir)
     except Exception:
         return False, None, "job not found or unloadable"
     repo = (job.metadata or {}).get("target_repo", "")
@@ -320,8 +320,8 @@ def list_test_runs(job_id: str, data_dir: Path | None = None) -> list[dict]:
     """List a job's persisted safe test records (job.metadata['test_runs']). No raw output."""
     ddir = _resolve_ddir(data_dir)
     try:
-        from packages.orchestration.pingpong_job import load_job_plan
-        job = load_job_plan(normalize_job_id(job_id), ddir)
+        from packages.orchestration.pingpong_job import require_job_plan
+        job = require_job_plan(normalize_job_id(job_id), ddir)
     except Exception:
         return []
     runs = (job.metadata or {}).get("test_runs", [])
@@ -332,13 +332,13 @@ def get_test_run(test_run_id: str, data_dir: Path | None = None) -> dict | None:
     ddir = _resolve_ddir(data_dir)
     # Scan all jobs' test_runs for the id.
     try:
-        from packages.orchestration.pingpong_job import list_job_plans, load_job_plan
+        from packages.orchestration.pingpong_job import list_job_plans, require_job_plan
         for jref in list_job_plans(ddir):
             jid = jref.get("id") if isinstance(jref, dict) else getattr(jref, "job_id", None)
             if jid is None:
                 continue
             try:
-                job = load_job_plan(normalize_job_id(str(jid)), ddir)
+                job = require_job_plan(normalize_job_id(str(jid)), ddir)
             except Exception:
                 continue
             for r in (job.metadata or {}).get("test_runs", []):
diff --git a/packages/orchestration/repair_loop.py b/packages/orchestration/repair_loop.py
index cffa4133..8024e37c 100644
--- a/packages/orchestration/repair_loop.py
+++ b/packages/orchestration/repair_loop.py
@@ -63,7 +63,7 @@ def start_repair_loop_v0(
     No real provider. No apply. No test execution. Stops before risky action.
     """
     from packages.orchestration.data_paths import resolve_data_root
-    from packages.orchestration.pingpong_job import load_job_plan, save_job_plan
+    from packages.orchestration.pingpong_job import load_job_plan, require_job_plan, save_job_plan
     from packages.orchestration.test_failure_artifact import (
         TestFailureArtifact,
         create_fix_task_from_failure,
@@ -81,7 +81,7 @@ def start_repair_loop_v0(
 
     # --- Phase: load ---
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except Exception:
         result.stop_reason = "job_not_found"
         result.stop_detail = f"Job {job_id[:8]} not found"
diff --git a/packages/orchestration/watchdog.py b/packages/orchestration/watchdog.py
index aeb409f7..c4bbc9d4 100644
--- a/packages/orchestration/watchdog.py
+++ b/packages/orchestration/watchdog.py
@@ -481,7 +481,7 @@ def act_on_trips(
         load_mission,
         set_mission_status,
     )
-    from packages.orchestration.pingpong_job import load_job_plan, save_job_plan
+    from packages.orchestration.pingpong_job import require_job_plan, save_job_plan
 
     ordered = list(trips)
     if not ordered:
@@ -519,7 +519,7 @@ def act_on_trips(
                       "be attached to a decision — a human has to look at "
                       "the mission"))
         try:
-            job = load_job_plan(normalize_job_id(link.job_id))
+            job = require_job_plan(normalize_job_id(link.job_id))
         except Exception as exc:
             return TripAction(
                 trip=trip,
diff --git a/tests/cli/runtime_helpers.py b/tests/cli/runtime_helpers.py
index 0cc2c3f2..137238be 100644
--- a/tests/cli/runtime_helpers.py
+++ b/tests/cli/runtime_helpers.py
@@ -57,20 +57,20 @@ def create_test_env(tmp_path: Path) -> tuple[Path, str]:
     """Create isolated data root with unique Job via direct JSON write."""
     root = tmp_path / "data"
     jid = str(uuid4())
-    jobs_dir = root / "jobs"
-    jobs_dir.mkdir(parents=True, exist_ok=True)
+    job_dir = root / "jobs" / jid
+    job_dir.mkdir(parents=True, exist_ok=True)
     job_data = {
-        "id": jid,
-        "name": "runtime-test",
-        "user_prompt": None,
+        "job_id": jid,
+        "job_title": "runtime-test",
+        "user_prompt": "",
         "created_at": datetime.now(timezone.utc).isoformat(),
         "tasks": [],
-        "state": "pending",
+        "status": "pending",
         "artifacts": [],
         "budget": {"max_steps": 10, "max_tokens": 0, "max_cost_usd": 0.0},
         "metadata": {},
     }
-    (jobs_dir / f"{jid}.json").write_text(json.dumps(job_data, indent=2))
+    (job_dir / "job.json").write_text(json.dumps(job_data, indent=2))
     # Always enable trace for runtime tests
     enable_trace(root)
     return root, jid
diff --git a/tests/cli/test_test_run_runtime.py b/tests/cli/test_test_run_runtime.py
index 60c1efc3..61b1c971 100644
--- a/tests/cli/test_test_run_runtime.py
+++ b/tests/cli/test_test_run_runtime.py
@@ -86,7 +86,7 @@ def _make_job_with_repo(
     max_test_runs: int = 3,
 ) -> None:
     """Patch a job JSON to add target_repo, permissions, and run_contract."""
-    job_file = data_root / "jobs" / f"{job_id}.json"
+    job_file = data_root / "jobs" / job_id / "job.json"
     job_data = json.loads(job_file.read_text())
 
     job_data["metadata"]["target_repo"] = str(repo_path)
@@ -421,7 +421,7 @@ class TestArchitectureGuards:
         """Missing target_repo directory must be handled gracefully."""
         data_root, job_id = create_test_env(tmp_path)
         # Set target_repo to a path that doesn't exist
-        job_file = data_root / "jobs" / f"{job_id}.json"
+        job_file = data_root / "jobs" / job_id / "job.json"
         job_data = json.loads(job_file.read_text())
         job_data["metadata"]["target_repo"] = str(tmp_path / "nonexistent_repo")
         job_data["metadata"].setdefault("permissions", {})
```
