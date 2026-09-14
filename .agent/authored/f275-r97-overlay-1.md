# F275 round 97 — the flip's eighth overlay, part 1 of 1

What the eighth overlay changes. `_as_uuid` is deleted from `orchestrator_loop.py`: the
orchestrator loop's three job loads and the watchdog's one pass the job id through
`normalize_job_id`, the disk-free shape check that accepts a UUID and a sixteen-hex id alike,
imported from `packages.orchestration.data_paths` inside each function that calls it.
`emit_important_event` checks a job id with `normalize_job_id(str(job_id))` where it parsed a
`UUID`, and no longer imports `UUID`. Code reading a task taken from a job's tasks reads the
unified task record's `task_id` and `title`, in `_cmd_mission_continue`,
`escalate_repeated_refusal`, `_build_job_plan_dashboard`, `_build_live_state_json` and
`build_checklist`.

This part holds 6 whole file diffs, `apps/cli/commands/mission_cmd.py` through `packages/orchestration/watchdog.py`.

Base: `844a7f21`. The flipped tree is that commit checked out and then built exactly as G4 of
`.agent/authored/f275-r97.md` orders: the committed generator re-derives the TIP re-keyed set from
the two pinned round 77 JSON files, the guarded transform runs over the checkout with that set, its
owners file and `r61_status.json`, and the result is staged.

The EIGHTH overlay is formed by 1 part, and this is part 1. The parts apply after
`.agent/authored/f275-r96-overlay-1.md`: `.agent/authored/f275-r90-overlay.md`, then
`.agent/authored/f275-r91-overlay.md`, then `.agent/authored/f275-r92-overlay-1.md` through
`-4.md`, then `.agent/authored/f275-r93-overlay-1.md` and `-2.md`, then
`.agent/authored/f275-r94-overlay-1.md` and `-2.md`, then `.agent/authored/f275-r95-overlay-1.md`
through `-4.md`, then `.agent/authored/f275-r96-overlay-1.md` are applied to the staged flipped
tree overlay by overlay, each overlay staged in turn, and the eighth overlay's diff was taken
against that state. The parts apply in `<k>` order, part 1 first; joined in that order their
fences are that one diff.

How to apply this part, inside the flipped tree with every earlier overlay applied and staged and
every part before this one applied:

1. Extract the fence below: the lines strictly between the line of three backticks followed by
   `diff` and the closing line of three backticks, each line kept with its newline.
2. Run `git apply --check <extracted file>` and require exit 0.
3. Run `git apply <extracted file>`.

```diff
diff --git a/apps/cli/commands/mission_cmd.py b/apps/cli/commands/mission_cmd.py
index f4f6881f..3c6a2e07 100644
--- a/apps/cli/commands/mission_cmd.py
+++ b/apps/cli/commands/mission_cmd.py
@@ -353,17 +353,17 @@ def _cmd_mission_continue(mission_id: str, next_step: str, *,
             "job_id": str(job.job_id),
             "role": job.metadata.get("mission_role", ""),
             "verify_first_task": (
-                {"description": verify.description,
+                {"description": verify.title,
                  "verify_command": verify.inputs.get("verify_command", "")}
                 if verify is not None else None),
-            "tasks": [t.description for t in job.tasks],
+            "tasks": [t.title for t in job.tasks],
         }, sort_keys=True))
         return
 
     print(str(job.job_id))
     print(f"  Mission: {mission.id[:12]}  ({job.metadata.get('mission_role', '')})")
     if verify is not None:
-        print(f"  Task 1 (injected): {verify.description}")
+        print(f"  Task 1 (injected): {verify.title}")
         print("  The follow-up work cannot start until that task completes.")
     else:
         print("  First job of this mission — there is no previous state to verify.")
diff --git a/packages/orchestration/event_persistence.py b/packages/orchestration/event_persistence.py
index 413b0df4..bdd3afd4 100644
--- a/packages/orchestration/event_persistence.py
+++ b/packages/orchestration/event_persistence.py
@@ -52,11 +52,10 @@ def emit_important_event(
     if eligible is not None and event_type not in eligible:
         return EventPersistenceResult(event_type, "skipped", "not_eligible")
     try:
-        from uuid import UUID
-
+        from packages.orchestration.data_paths import normalize_job_id
         from packages.orchestration.timeline import append_run_event
         try:
-            UUID(str(job_id))
+            normalize_job_id(str(job_id))
         except (ValueError, TypeError):
             return EventPersistenceResult(event_type, "failed", "invalid_job_id")
         append_run_event(str(data_dir), job_id, event=event_type, metadata=metadata)
diff --git a/packages/orchestration/orchestrator_loop.py b/packages/orchestration/orchestrator_loop.py
index 37d8bf69..ffff590f 100644
--- a/packages/orchestration/orchestrator_loop.py
+++ b/packages/orchestration/orchestrator_loop.py
@@ -366,13 +366,14 @@ def open_mission_decisions(mission: Any) -> list[dict[str, Any]]:
     answering a decision between two iterations is picked up by the next one
     with no bookkeeping here.
     """
+    from packages.orchestration.data_paths import normalize_job_id
     from packages.orchestration.escalation import open_task_decisions
     from packages.orchestration.pingpong_job import load_job_plan
 
     out: list[dict[str, Any]] = []
     for link in getattr(mission, "job_links", ()) or ():
         try:
-            job = load_job_plan(_as_uuid(link.job_id))
+            job = load_job_plan(normalize_job_id(link.job_id))
         except Exception:
             # A job that cannot be read cannot be asked about its decisions.
             # Recorded as absent rather than raised: one unreadable job must
@@ -382,12 +383,6 @@ def open_mission_decisions(mission: Any) -> list[dict[str, Any]]:
     return out
 
 
-def _as_uuid(raw: Any) -> Any:
-    from uuid import UUID
-
-    return raw if isinstance(raw, UUID) else UUID(str(raw))
-
-
 # ---------------------------------------------------------------------------
 # The decision ledger — append-only
 # ---------------------------------------------------------------------------
@@ -1729,6 +1724,7 @@ def collect_milestone_evidence(project_id: str, mission_id: str,
                                milestone_id: str,
                                root: Path | None = None) -> MilestoneEvidence:
     """Read a milestone's evidence through the existing job and gate verbs."""
+    from packages.orchestration.data_paths import normalize_job_id
     from packages.orchestration.dod_gate import load_gate_result
     from packages.orchestration.pingpong_job import load_job_plan
 
@@ -1739,7 +1735,7 @@ def collect_milestone_evidence(project_id: str, mission_id: str,
     state = ""
     handback: Any = None
     try:
-        job = load_job_plan(_as_uuid(job_id))
+        job = load_job_plan(normalize_job_id(job_id))
     except Exception:
         # An unreadable job is an ABSENT observation, never a passing one.
         return MilestoneEvidence(job_id=job_id)
@@ -1920,6 +1916,7 @@ def escalate_repeated_refusal(project_id: str, mission_id: str, reason: str, *,
     ``escalation.enqueue_task_decision`` attaches to; a mission with no job yet
     has nowhere to attach one, and that is reported rather than papered over.
     """
+    from packages.orchestration.data_paths import normalize_job_id
     from packages.orchestration.escalation import enqueue_task_decision
     from packages.orchestration.mission_state import load_mission
     from packages.orchestration.pingpong_job import load_job_plan, save_job_plan
@@ -1930,7 +1927,7 @@ def escalate_repeated_refusal(project_id: str, mission_id: str, reason: str, *,
         return ("no job is linked to this mission, so the refusal cannot be "
                 "attached to a decision — a human has to look at the mission")
     try:
-        job = load_job_plan(_as_uuid(link.job_id))
+        job = load_job_plan(normalize_job_id(link.job_id))
     except Exception as exc:
         return f"the mission's latest job could not be read to escalate: {exc}"
     tasks = list(getattr(job, "tasks", ()) or ())
@@ -1938,7 +1935,7 @@ def escalate_repeated_refusal(project_id: str, mission_id: str, reason: str, *,
         return (f"job {link.job_id} has no task to attach the decision to")
     record = enqueue_task_decision(
         job,
-        task_id=tasks[0].id,
+        task_id=tasks[0].task_id,
         question=(f"The orchestrator's move was refused twice in a row: "
                   f"{reason}. How should this mission proceed?"),
         options=("replan the mission", "abandon the mission"),
diff --git a/packages/orchestration/ui_server.py b/packages/orchestration/ui_server.py
index 20dd4754..1ff55df1 100644
--- a/packages/orchestration/ui_server.py
+++ b/packages/orchestration/ui_server.py
@@ -1054,8 +1054,8 @@ def _build_job_plan_dashboard(job: Any) -> dict[str, Any]:
     for idx, t in enumerate(job.tasks):
         tstat = t.status.value if hasattr(t.status, "value") else str(t.status)
         task_items.append({
-            "id": str(t.id),
-            "title": t.description[:80] if t.description else f"Task {idx + 1}",
+            "id": str(t.task_id),
+            "title": t.title[:80] if t.title else f"Task {idx + 1}",
             "status": tstat,
             "source": "job_plan",
         })
@@ -2147,9 +2147,9 @@ def _build_live_state_json(job: Any) -> dict[str, Any]:
     for t in job.tasks:
         tstat = t.status.value if hasattr(t.status, "value") else str(t.status)
         if tstat == "running":
-            active_task_id = str(t.id)
+            active_task_id = str(t.task_id)
         if tstat == "completed":
-            latest_completed_task_id = str(t.id)
+            latest_completed_task_id = str(t.task_id)
 
     # Repair loop detection
     repair_loop_used = any(
diff --git a/packages/orchestration/ui_view_model.py b/packages/orchestration/ui_view_model.py
index 1236f61c..ae736684 100644
--- a/packages/orchestration/ui_view_model.py
+++ b/packages/orchestration/ui_view_model.py
@@ -1000,7 +1000,7 @@ def build_checklist(job: Any, events: list[dict[str, Any]]) -> dict[str, Any]:
     # Task items
     for task in job.tasks:
         t_status = task.status.value if hasattr(task.status, "value") else str(task.status)
-        desc = task.description if len(task.description) <= 50 else task.description[:47] + "..."
+        desc = task.title if len(task.title) <= 50 else task.title[:47] + "..."
 
         if t_status == "completed":
             cl_state = "done"
@@ -1021,13 +1021,13 @@ def build_checklist(job: Any, events: list[dict[str, Any]]) -> dict[str, Any]:
             cl_state = "suggested"
 
         items.append({
-            "id": str(task.id),
-            "label": desc if desc and desc != str(task.id) else human_label("task"),
+            "id": str(task.task_id),
+            "label": desc if desc and desc != str(task.task_id) else human_label("task"),
             "state": cl_state,
             "kind": "task",
             "checked": checked,
             "muted": cl_state in ("pending", "suggested"),
-            "node_id": str(task.id),
+            "node_id": str(task.task_id),
             "next_action": {},
         })
 
diff --git a/packages/orchestration/watchdog.py b/packages/orchestration/watchdog.py
index 5f9334a9..aeb409f7 100644
--- a/packages/orchestration/watchdog.py
+++ b/packages/orchestration/watchdog.py
@@ -473,6 +473,7 @@ def act_on_trips(
     from datetime import datetime, timezone
 
     from packages.orchestration import orchestrator_loop
+    from packages.orchestration.data_paths import normalize_job_id
     from packages.orchestration.escalation import enqueue_task_decision
     from packages.orchestration.mission_state import (
         MISSION_STATUS_ACTIVE,
@@ -518,7 +519,7 @@ def act_on_trips(
                       "be attached to a decision — a human has to look at "
                       "the mission"))
         try:
-            job = load_job_plan(orchestrator_loop._as_uuid(link.job_id))
+            job = load_job_plan(normalize_job_id(link.job_id))
         except Exception as exc:
             return TripAction(
                 trip=trip,
```
