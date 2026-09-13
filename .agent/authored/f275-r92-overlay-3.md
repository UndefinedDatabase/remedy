# F275 round 92 — the flip's third overlay, part 3 of 4

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

This part holds 14 whole file diffs, `apps/cli/commands/repair_cmd.py` through `packages/orchestration/self_dogfood_execution.py`.

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
diff --git a/apps/cli/commands/repair_cmd.py b/apps/cli/commands/repair_cmd.py
index 9d2deefa..ac2159f9 100644
--- a/apps/cli/commands/repair_cmd.py
+++ b/apps/cli/commands/repair_cmd.py
@@ -47,7 +47,7 @@ def _cmd_repair_start(args: Any) -> None:
 def _cmd_failure_show(args: Any) -> None:
     """Show a test failure artifact."""
     from packages.orchestration.storage import JobNotFoundError, JobStoreError
-    from packages.orchestration.pingpong_job import load_job_plan
+    from packages.orchestration.pingpong_job import require_job_plan
     from packages.orchestration.test_failure_artifact import (
         TestFailureArtifact,
         export_failure_artifact_json,
@@ -55,7 +55,7 @@ def _cmd_failure_show(args: Any) -> None:
     )
 
     try:
-        job = load_job_plan(args.job_id)
+        job = require_job_plan(args.job_id)
     except (JobNotFoundError, JobStoreError):
         print(f"Error: job {args.job_id[:8]} not found", file=sys.stderr)
         sys.exit(1)
@@ -132,10 +132,10 @@ def _cmd_repair_status(args: Any) -> None:
     from packages.orchestration.approval_queue import get_patch_intent
     from packages.orchestration.repair_loop import load_repair_attempts
     from packages.orchestration.storage import JobNotFoundError, JobStoreError
-    from packages.orchestration.pingpong_job import load_job_plan
+    from packages.orchestration.pingpong_job import require_job_plan
 
     try:
-        job = load_job_plan(args.job_id)
+        job = require_job_plan(args.job_id)
     except (JobNotFoundError, JobStoreError):
         print(f"Error: job {str(args.job_id)[:8]} not found", file=sys.stderr)
         sys.exit(1)
@@ -215,9 +215,9 @@ def _cmd_repair_request(args: Any) -> None:
 def _cmd_repair_request_show(args: Any) -> None:
     from packages.orchestration.repair_request_builder import get_request_package
     from packages.orchestration.storage import JobNotFoundError
-    from packages.orchestration.pingpong_job import load_job_plan
+    from packages.orchestration.pingpong_job import require_job_plan
     try:
-        job = load_job_plan(args.job_id)
+        job = require_job_plan(args.job_id)
     except (JobNotFoundError, ValueError) as exc:
         print(f"Error: {type(exc).__name__}", file=sys.stderr)
         sys.exit(1)
diff --git a/apps/cli/commands/repo.py b/apps/cli/commands/repo.py
index cbdc17d2..c91acc32 100644
--- a/apps/cli/commands/repo.py
+++ b/apps/cli/commands/repo.py
@@ -54,14 +54,14 @@ def _cmd_repo_status(
     job = None
     if job_id_str:
         from packages.orchestration.storage import JobNotFoundError
-        from packages.orchestration.pingpong_job import load_job_plan
+        from packages.orchestration.pingpong_job import require_job_plan
         try:
             job_id = lookup_job_id(job_id_str)
         except ValueError:
             print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
             sys.exit(1)
         try:
-            job = load_job_plan(job_id)
+            job = require_job_plan(job_id)
         except JobNotFoundError as exc:
             print(f"Error: {exc}", file=sys.stderr)
             sys.exit(1)
diff --git a/apps/cli/commands/snapshot_cmds.py b/apps/cli/commands/snapshot_cmds.py
index ffcf69a5..71673ca2 100644
--- a/apps/cli/commands/snapshot_cmds.py
+++ b/apps/cli/commands/snapshot_cmds.py
@@ -19,7 +19,7 @@ def _cmd_snapshot_inspect(job_id_str: str, snapshot_id: str, *, as_json: bool =
     from packages.orchestration.data_paths import resolve_data_root
     from packages.orchestration.repository_snapshot import load_snapshot
     from packages.orchestration.storage import JobNotFoundError
-    from packages.orchestration.pingpong_job import load_job_plan
+    from packages.orchestration.pingpong_job import require_job_plan
 
     try:
         job_id = lookup_job_id(job_id_str)
@@ -31,7 +31,7 @@ def _cmd_snapshot_inspect(job_id_str: str, snapshot_id: str, *, as_json: bool =
         sys.exit(1)
 
     try:
-        load_job_plan(job_id)
+        require_job_plan(job_id)
     except JobNotFoundError:
         if as_json:
             print(_json.dumps({"error": "job_not_found", "job_id": job_id_str}))
@@ -96,7 +96,7 @@ def _cmd_snapshot_list_applies(job_id_str: str, *, as_json: bool = False) -> Non
     from packages.orchestration.data_paths import resolve_data_root
     from packages.orchestration.repository_snapshot import load_durable_apply_record
     from packages.orchestration.storage import JobNotFoundError
-    from packages.orchestration.pingpong_job import load_job_plan
+    from packages.orchestration.pingpong_job import require_job_plan
 
     try:
         job_id = lookup_job_id(job_id_str)
@@ -108,7 +108,7 @@ def _cmd_snapshot_list_applies(job_id_str: str, *, as_json: bool = False) -> Non
         sys.exit(1)
 
     try:
-        load_job_plan(job_id)
+        require_job_plan(job_id)
     except JobNotFoundError:
         if as_json:
             print(_json.dumps({"error": "job_not_found", "job_id": job_id_str}))
diff --git a/apps/cli/commands/test_cmds.py b/apps/cli/commands/test_cmds.py
index eee3323e..0aa93dcb 100644
--- a/apps/cli/commands/test_cmds.py
+++ b/apps/cli/commands/test_cmds.py
@@ -181,7 +181,7 @@ def _cmd_test_status(job_id_str: str, *, as_json: bool = False) -> None:
     from packages.orchestration.data_paths import resolve_data_root
     from packages.orchestration.run_contract import ensure_contract, export_usage_json, load_usage
     from packages.orchestration.storage import JobNotFoundError
-    from packages.orchestration.pingpong_job import load_job_plan
+    from packages.orchestration.pingpong_job import require_job_plan
 
     try:
         job_id = lookup_job_id(job_id_str)
@@ -193,7 +193,7 @@ def _cmd_test_status(job_id_str: str, *, as_json: bool = False) -> None:
         sys.exit(1)
 
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError:
         if as_json:
             print(_json.dumps({"error": "job_not_found", "job_id": job_id_str}))
diff --git a/packages/orchestration/do_continue.py b/packages/orchestration/do_continue.py
index 990990e8..cae5bcb2 100644
--- a/packages/orchestration/do_continue.py
+++ b/packages/orchestration/do_continue.py
@@ -348,14 +348,14 @@ def evaluate_continue_eligibility(
         evaluate_run_action,
     )
     from packages.orchestration.storage import JobNotFoundError
-    from packages.orchestration.pingpong_job import load_job_plan
+    from packages.orchestration.pingpong_job import require_job_plan
 
     data_dir = Path(data_dir) if data_dir is not None else resolve_data_root()
     elig = ContinueEligibility(eligible=False, job_id=job_id)
 
     # 1. Job exists.
     try:
-        job = load_job_plan(normalize_job_id(job_id), data_dir)
+        job = require_job_plan(normalize_job_id(job_id), data_dir)
     except (ValueError, JobNotFoundError):
         elig.blockers.append("job_not_found")
         elig.next_safe_action = "remedy job list --json"
diff --git a/packages/orchestration/mission_readiness.py b/packages/orchestration/mission_readiness.py
index 497e9fce..002150f2 100644
--- a/packages/orchestration/mission_readiness.py
+++ b/packages/orchestration/mission_readiness.py
@@ -183,10 +183,10 @@ def _gather_inputs(job_id: str, data_dir: Path) -> _Inputs | None:
     from packages.orchestration.repository_snapshot import build_snapshot_truth, list_durable_apply_ids
     from packages.orchestration.run_contract import ensure_contract, load_usage
     from packages.orchestration.storage import JobNotFoundError
-    from packages.orchestration.pingpong_job import load_job_plan
+    from packages.orchestration.pingpong_job import require_job_plan
 
     try:
-        job = load_job_plan(normalize_job_id(job_id), data_dir)
+        job = require_job_plan(normalize_job_id(job_id), data_dir)
     except (ValueError, JobNotFoundError):
         return None
 
diff --git a/packages/orchestration/mission_state.py b/packages/orchestration/mission_state.py
index f887304d..1736b87d 100644
--- a/packages/orchestration/mission_state.py
+++ b/packages/orchestration/mission_state.py
@@ -1027,7 +1027,7 @@ def continue_mission(project_id: str, mission_id: str, next_step: str, *,
     from packages.core.models import RunState
     from packages.orchestration.pingpong_job import JobPlan
     from packages.orchestration.storage import JobNotFoundError, JobStoreError
-    from packages.orchestration.pingpong_job import load_job_plan, save_job_plan
+    from packages.orchestration.pingpong_job import require_job_plan, save_job_plan
 
     text = str(next_step).strip()
     if not text:
@@ -1042,7 +1042,7 @@ def continue_mission(project_id: str, mission_id: str, next_step: str, *,
         role = MISSION_ROLE_INITIAL
     else:
         try:
-            previous_job = load_job_plan(normalize_job_id(previous.job_id))
+            previous_job = require_job_plan(normalize_job_id(previous.job_id))
         except (ValueError, JobNotFoundError) as exc:
             raise MissionError(
                 f"the previous job {previous.job_id} is gone, so its Definition "
diff --git a/packages/orchestration/orchestrator_brain.py b/packages/orchestration/orchestrator_brain.py
index 705bb2f2..81abf5df 100644
--- a/packages/orchestration/orchestrator_brain.py
+++ b/packages/orchestration/orchestrator_brain.py
@@ -305,9 +305,9 @@ def _gather_signals(job_id: str, data_dir: Path,
         "self_proposed_approved": [], "self_items": 0, "budget_exhausted": False,
     }
     from packages.orchestration.storage import JobNotFoundError
-    from packages.orchestration.pingpong_job import load_job_plan
+    from packages.orchestration.pingpong_job import require_job_plan
     try:
-        job = load_job_plan(normalize_job_id(job_id), data_dir)
+        job = require_job_plan(normalize_job_id(job_id), data_dir)
     except (ValueError, JobNotFoundError):
         refs.append(OrchestratorEvidenceRef("job", "missing"))
         return sig
diff --git a/packages/orchestration/pingpong_job.py b/packages/orchestration/pingpong_job.py
index d9bec6d1..b966594c 100644
--- a/packages/orchestration/pingpong_job.py
+++ b/packages/orchestration/pingpong_job.py
@@ -501,6 +501,25 @@ def load_job_plan_safe(job_id: str, root: Path | None = None) -> tuple[JobPlan |
         return (None, True)
 
 
+# WHY: every caller that catches ``JobNotFoundError`` needs the raise the classic ``storage.load_job`` gave it.
+def require_job_plan(job_id: str, root: Path | None = None) -> JobPlan:
+    """Load one JobPlan, or RAISE what the classic ``storage.load_job`` raised.
+
+    The contract: the plan ``load_job_plan_safe`` reads comes back; when there is no
+    plan, a record that exists and cannot be read raises ``JobStoreError``, and a job
+    with no record raises ``JobNotFoundError(job_id)``. Both are the classes the
+    classic loader's callers already catch. It never returns ``None``.
+    """
+    from packages.orchestration.storage import JobNotFoundError, JobStoreError
+
+    plan, degraded = load_job_plan_safe(job_id, root)
+    if plan is None:
+        if degraded:
+            raise JobStoreError(f"Unreadable job record for {job_id}")
+        raise JobNotFoundError(job_id)
+    return plan
+
+
 def list_job_plans_safe(root: Path | None = None) -> tuple[list[JobPlan], bool, list[str]]:
     """Every persisted JobPlan. Returns ``(plans, degraded, skipped_job_ids)``.
 
diff --git a/packages/orchestration/repair_loop.py b/packages/orchestration/repair_loop.py
index ba8ad714..cffa4133 100644
--- a/packages/orchestration/repair_loop.py
+++ b/packages/orchestration/repair_loop.py
@@ -603,13 +603,13 @@ def build_repair_context(
     """
     from packages.orchestration.data_paths import resolve_data_root
     from packages.orchestration.storage import JobNotFoundError
-    from packages.orchestration.pingpong_job import load_job_plan
+    from packages.orchestration.pingpong_job import require_job_plan
 
     ctx = RepairContextSummary(job_id=job_id, failure_artifact_id=failure_artifact_id)
     ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
 
     try:
-        job = load_job_plan(normalize_job_id(job_id), ddir)
+        job = require_job_plan(normalize_job_id(job_id), ddir)
     except (ValueError, JobNotFoundError):
         ctx.status = "blocked"
         ctx.blocker = "job_not_found"
@@ -785,14 +785,14 @@ def evaluate_repair_eligibility(
         evaluate_run_action,
     )
     from packages.orchestration.storage import JobNotFoundError
-    from packages.orchestration.pingpong_job import load_job_plan
+    from packages.orchestration.pingpong_job import require_job_plan
 
     ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
     elig = RepairEligibility(job_id=job_id, failure_artifact_id=failure_artifact_id)
 
     # 1. Job exists.
     try:
-        job = load_job_plan(normalize_job_id(job_id), ddir)
+        job = require_job_plan(normalize_job_id(job_id), ddir)
     except (ValueError, JobNotFoundError):
         elig.blockers.append("job_not_found")
         elig.next_safe_action = _na("List jobs", "remedy job list --json", "Job not found.")
@@ -1082,7 +1082,7 @@ def run_repair_attempt(
         evaluate_run_action,
     )
     from packages.orchestration.storage import JobNotFoundError
-    from packages.orchestration.pingpong_job import load_job_plan
+    from packages.orchestration.pingpong_job import require_job_plan
 
     ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
     phases: list[dict[str, str]] = []
@@ -1104,7 +1104,7 @@ def run_repair_attempt(
         )
 
     try:
-        job = load_job_plan(normalize_job_id(job_id), ddir)
+        job = require_job_plan(normalize_job_id(job_id), ddir)
     except (ValueError, JobNotFoundError):
         return RepairAttemptResult(
             job_id=job_id, failure_artifact_id=failure_artifact_id,
@@ -1406,12 +1406,12 @@ def reconcile_repair_after_continue(
     """
     from packages.orchestration.data_paths import resolve_data_root
     from packages.orchestration.storage import JobNotFoundError
-    from packages.orchestration.pingpong_job import load_job_plan
+    from packages.orchestration.pingpong_job import require_job_plan
 
     ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
     out = RepairReconcileResult()
     try:
-        job = load_job_plan(normalize_job_id(job_id), ddir)
+        job = require_job_plan(normalize_job_id(job_id), ddir)
     except (ValueError, JobNotFoundError):
         return out
 
diff --git a/packages/orchestration/repair_request_builder.py b/packages/orchestration/repair_request_builder.py
index 84246027..84fb19a0 100644
--- a/packages/orchestration/repair_request_builder.py
+++ b/packages/orchestration/repair_request_builder.py
@@ -455,7 +455,7 @@ def build_repair_request_package(
         evaluate_run_action,
     )
     from packages.orchestration.storage import JobNotFoundError
-    from packages.orchestration.pingpong_job import load_job_plan, save_job_plan
+    from packages.orchestration.pingpong_job import require_job_plan, save_job_plan
 
     ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
     label = (generator_label or "external").strip() or "external"
@@ -465,7 +465,7 @@ def build_repair_request_package(
         model_hint=hint, generator_label=label)
 
     try:
-        job = load_job_plan(normalize_job_id(job_id), ddir)
+        job = require_job_plan(normalize_job_id(job_id), ddir)
     except (ValueError, JobNotFoundError):
         result.stop_reason = RepairRequestStopReason.JOB_NOT_FOUND
         result.evidence_status = "unknown"
diff --git a/packages/orchestration/repository_snapshot.py b/packages/orchestration/repository_snapshot.py
index 08794f5b..e9429f3d 100644
--- a/packages/orchestration/repository_snapshot.py
+++ b/packages/orchestration/repository_snapshot.py
@@ -1367,8 +1367,7 @@ def revert_repository_apply(
     No revert if files changed after apply (drift detection).
     No caller-supplied permission booleans (Step 1137).
     """
-    from uuid import UUID as _UUID
-
+    from packages.orchestration.data_paths import normalize_job_id
     from packages.orchestration.permissions import (
         Capability as _Capability,
     )
@@ -1387,7 +1386,7 @@ def revert_repository_apply(
     from packages.orchestration.storage import (
         JobNotFoundError as _JobNotFoundError,
     )
-    from packages.orchestration.pingpong_job import load_job_plan as _load_job
+    from packages.orchestration.pingpong_job import require_job_plan as _load_job
 
     data_dir = data_dir or resolve_data_root()
     repo_root = repo_root.resolve()
@@ -1418,7 +1417,7 @@ def revert_repository_apply(
 
     # Gate 3a: Load job from storage — no bypass booleans (Step 1137)
     try:
-        _job_uuid = _UUID(job_id)
+        _job_uuid = normalize_job_id(job_id)
         _job = _load_job(_job_uuid, data_dir)
     except (ValueError, _JobNotFoundError):
         _emit_snapshot_event(data_dir, job_id, "revert_blocked", {
diff --git a/packages/orchestration/self_dogfood.py b/packages/orchestration/self_dogfood.py
index f77f527d..3cd04719 100644
--- a/packages/orchestration/self_dogfood.py
+++ b/packages/orchestration/self_dogfood.py
@@ -371,8 +371,8 @@ def build_self_dogfood_inspection(
     if job_id:
         try:
             from packages.orchestration.storage import JobNotFoundError
-            from packages.orchestration.pingpong_job import load_job_plan
-            job = load_job_plan(normalize_job_id(job_id), ddir)
+            from packages.orchestration.pingpong_job import require_job_plan
+            job = require_job_plan(normalize_job_id(job_id), ddir)
             insp.sources_checked.append(SelfImprovementSource("job", SourceStatus.AVAILABLE))
         except (ValueError, JobNotFoundError):
             insp.sources_checked.append(SelfImprovementSource("job", SourceStatus.MISSING))
@@ -464,13 +464,13 @@ def propose_self_improvement(
         evaluate_run_action,
     )
     from packages.orchestration.storage import JobNotFoundError
-    from packages.orchestration.pingpong_job import load_job_plan
+    from packages.orchestration.pingpong_job import require_job_plan
 
     ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
     result = SelfDogfoodResult(job_id=job_id)
 
     try:
-        load_job_plan(normalize_job_id(job_id), ddir)
+        require_job_plan(normalize_job_id(job_id), ddir)
     except (ValueError, JobNotFoundError):
         result.stop_reason = "job_not_found"
         result.evidence_status = "unknown"
diff --git a/packages/orchestration/self_dogfood_execution.py b/packages/orchestration/self_dogfood_execution.py
index 18276791..512fee13 100644
--- a/packages/orchestration/self_dogfood_execution.py
+++ b/packages/orchestration/self_dogfood_execution.py
@@ -432,7 +432,7 @@ def evaluate_self_execution_eligibility(
         evaluate_run_action,
     )
     from packages.orchestration.storage import JobNotFoundError
-    from packages.orchestration.pingpong_job import load_job_plan
+    from packages.orchestration.pingpong_job import require_job_plan
 
     ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
     elig = SelfExecEligibility(proposed_task_id=proposed_task_id)
@@ -472,7 +472,7 @@ def evaluate_self_execution_eligibility(
 
     # Contract gate.
     try:
-        job = load_job_plan(normalize_job_id(jid), ddir)
+        job = require_job_plan(normalize_job_id(jid), ddir)
     except (ValueError, JobNotFoundError):
         elig.blockers.append("no_job")
         elig.stop_reason = StopReason.NO_JOB
@@ -650,7 +650,7 @@ def reconcile_self_attempt(
     from packages.orchestration.approval_queue import APPROVAL_APPROVED, get_patch_intent
     from packages.orchestration.data_paths import resolve_data_root
     from packages.orchestration.storage import JobNotFoundError
-    from packages.orchestration.pingpong_job import load_job_plan
+    from packages.orchestration.pingpong_job import require_job_plan
 
     ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
     a = _load_attempt(attempt_id, ddir)
@@ -664,7 +664,7 @@ def reconcile_self_attempt(
         return _result_from_attempt(a)
 
     try:
-        job = load_job_plan(normalize_job_id(a.job_id), ddir)
+        job = require_job_plan(normalize_job_id(a.job_id), ddir)
     except (ValueError, JobNotFoundError):
         a.stop_reason = StopReason.NO_JOB
         save_attempt(a, ddir)
```
