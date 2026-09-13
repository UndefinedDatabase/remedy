# F275 round 94 — the flip's fifth overlay, part 1 of 2

What the fifth overlay changes. A `TaskEntry` built without an id mints one:
`data_paths.mint_task_id` is the field's default factory, as the classic `Task` minted a
`uuid4`, while a job file's tasks keep the `T001` ids the parser passes. A task id is read as a
string wherever code parsed it as a `UUID`: the failure artifact, the set of tasks waiting on a
decision (which keeps only ids of the job's own tasks), the decision inbox's blocked count and
the `context --task` check. `job context` reads a task's planned id from its flight-plan block
before its own id. The two constructions that passed the classic `acceptance_checks` list pass
`acceptance` text, `do_materialize` constructs its `TaskEntry` instead of calling
`model_validate`, and `inject_verify_first` uses `dataclasses.replace` instead of `model_copy`.
`execute_test_run`'s `job show` guidance reads `job.job_id`. The tests pin the new minter by
object identity and in `TestMintIds`, and the proposed-task tests set `REMEDY_DATA_DIR` in place
of the classic store's `_DATA_DIR`.

This part holds 13 whole file diffs, `apps/cli/commands/context.py` through `tests/orchestration/test_mint_call_sites.py`.

Base: `844a7f21`. The flipped tree is that commit checked out and then built exactly as G4 of
`.agent/authored/f275-r94.md` orders: the committed generator re-derives the TIP re-keyed set from
the two pinned round 77 JSON files, the guarded transform runs over the checkout with that set, its
owners file and `r61_status.json`, and the result is staged.

The 2 parts form the FIFTH overlay. They apply after
`.agent/authored/f275-r93-overlay-2.md`: `.agent/authored/f275-r90-overlay.md`, then
`.agent/authored/f275-r91-overlay.md`, then `.agent/authored/f275-r92-overlay-1.md` through
`-4.md`, then `.agent/authored/f275-r93-overlay-1.md` and `-2.md` are applied to the staged
flipped tree overlay by overlay, each overlay staged in turn, and the fifth overlay's diff was
taken against that state. The parts apply in `<k>` order, part 1 first; joined in that order
their fences are that one diff.

How to apply this part, inside the flipped tree with every earlier overlay applied and staged and
every part before this one applied:

1. Extract the fence below: the lines strictly between the line of three backticks followed by
   `diff` and the closing line of three backticks, each line kept with its newline.
2. Run `git apply --check <extracted file>` and require exit 0.
3. Run `git apply <extracted file>`.

```diff
diff --git a/apps/cli/commands/context.py b/apps/cli/commands/context.py
index 9e687b30..bf0d8f2a 100644
--- a/apps/cli/commands/context.py
+++ b/apps/cli/commands/context.py
@@ -6,7 +6,6 @@ import json as _json
 import sys
 from collections.abc import Callable
 from typing import TYPE_CHECKING
-from uuid import UUID
 
 from packages.orchestration.data_paths import lookup_job_id
 from packages.orchestration.storage import JobNotFoundError
@@ -35,11 +34,6 @@ def _cmd_context_inspect(
         sys.exit(1)
 
     if task_id is not None:
-        try:
-            UUID(task_id)
-        except ValueError:
-            print(f"Error: invalid task ID: {task_id!r}", file=sys.stderr)
-            sys.exit(1)
         task_ids = {str(t.task_id) for t in job.tasks}
         if task_id not in task_ids:
             print(f"Error: task {task_id!r} not found in job", file=sys.stderr)
diff --git a/apps/cli/commands/job_context_cmd.py b/apps/cli/commands/job_context_cmd.py
index f6904d6b..a448d00f 100644
--- a/apps/cli/commands/job_context_cmd.py
+++ b/apps/cli/commands/job_context_cmd.py
@@ -115,13 +115,18 @@ def _task_flight_inputs(task: Any) -> dict:
 
 
 def _task_planned_id(task: Any) -> str:
-    """The planned id (`T001`) `map_flight_plan_to_tasks` wrote, or ""."""
-    # A `TaskEntry` IS its planned id — it carries `T001` as its own field and
-    # no flight-plan block at all — so that spelling wins where it is present.
-    own = getattr(task, "task_id", "")
-    if own:
-        return str(own)
-    return str(_task_flight_inputs(task).get("planned_id") or "")
+    """The planned id (`T001`) `map_flight_plan_to_tasks` wrote, else the task's own id.
+
+    The flight-plan block wins because a task mapped from a flight plan mints its
+    own `task_id` beside the planned id, and `--task T001` names the plan's id.
+    """
+    planned = _task_flight_inputs(task).get("planned_id")
+    if planned:
+        # The flight-plan block wins: the minted `task_id` beside it is not the
+        # id the plan and its operator use. A job file's task has no such block
+        # and carries `T001` as its own id, which the fallback returns.
+        return str(planned)
+    return str(getattr(task, "task_id", "") or "")
 
 
 def _task_files_hint(task: Any) -> list[str]:
diff --git a/packages/orchestration/data_paths.py b/packages/orchestration/data_paths.py
index 2b032aeb..c01b0724 100644
--- a/packages/orchestration/data_paths.py
+++ b/packages/orchestration/data_paths.py
@@ -21,6 +21,7 @@ Public API::
     mint_job_id() -> str                     # a job id (16-hex, DECISION F260 D2)
     mint_run_id() -> str                     # a run id
     mint_episode_id() -> str                 # a run-episode id
+    mint_task_id() -> str                    # a task id no job file numbered
     job_dir(job_id, root: Path | None = None) -> Path
     job_record_path(job_id, root: Path | None = None) -> Path
     job_record_paths(root: Path | None = None) -> list[Path]
@@ -162,12 +163,12 @@ def control_dir(root: Path | None = None) -> Path:
 
 
 # DECISION F260 D2 (2026-09-06): every Remedy id is ``uuid4().hex[:16]``, but ONE
-# SHAPE IS NOT ONE FUNCTION. The same sixteen hex characters already name four
+# SHAPE IS NOT ONE FUNCTION. The same sixteen hex characters already name five
 # different kinds of thing, so passing a run id where a job id belongs is not a
 # type error and never will be. A name is the weakest distinction Python gives
 # away for free, and it is the one thing that makes such a swap greppable, so
 # each kind is minted by its own ``def`` below. ``safe_points.new_request_id``
-# is the fourth kind and stays where the stop request lives.
+# is the fifth kind and stays where the stop request lives.
 
 
 def mint_job_id() -> str:
@@ -185,6 +186,11 @@ def mint_episode_id() -> str:
     return uuid4().hex[:16]
 
 
+def mint_task_id() -> str:
+    """Mint the id of one TASK that no job file numbered — a task built by code, not parsed."""
+    return uuid4().hex[:16]
+
+
 # DECISION F260 D1 (2026-09-06): ONE ROOT PER JOB — the record at
 # ``<data_root>/jobs/<16hex>/job.json``, that job's evidence at
 # ``<data_root>/jobs/<16hex>/evidence/``, and runs keyed by RUN id under
diff --git a/packages/orchestration/decision_inbox.py b/packages/orchestration/decision_inbox.py
index 15ffd996..3b681fd3 100644
--- a/packages/orchestration/decision_inbox.py
+++ b/packages/orchestration/decision_inbox.py
@@ -23,7 +23,6 @@ from __future__ import annotations
 
 from datetime import datetime, timezone
 from typing import Any
-from uuid import UUID
 
 from packages.orchestration.dag_schedule import blocked_downstream
 from packages.orchestration.decision_queue import export_decision_json, list_decisions
@@ -65,12 +64,9 @@ def _blocked_subtree_size(job: Any, payload: Any) -> int:
     set makes ``blocked_downstream`` return the empty set by its own first
     branch, so every other type reports 0 with no special case here.
     """
-    seeds: set[UUID] = set()
-    if isinstance(payload, dict):
-        try:
-            seeds = {UUID(str(payload.get("task_id")))}
-        except (ValueError, TypeError):
-            seeds = set()
+    seeds: set[str] = set()
+    if isinstance(payload, dict) and payload.get("task_id"):
+        seeds = {str(payload["task_id"])}
     # ``list_decisions`` accepts a JobPlan too, and a JobPlan has no ``.tasks``.
     tasks = getattr(job, "tasks", None) or ()
     return len(blocked_downstream(tasks, seeds))
@@ -189,8 +185,8 @@ def build_decision_inbox(
     Additive over ``export_decision_json``: each card carries exactly three
     extra keys, ``age_seconds``, ``blocked_count`` and
     ``answerable_by_decision_resolve``.  No input makes this function
-    raise — an unreadable ``created_at`` gives a None age, a task id that is not
-    a UUID gives 0 blocked, and the card still renders.  Being honest about an
+    raise — an unreadable ``created_at`` gives a None age, a task id that names
+    no task gives 0 blocked, and the card still renders.  Being honest about an
     unreadable entry is the point; hiding it would lose the question.
     """
     moment = now or datetime.now(timezone.utc)
diff --git a/packages/orchestration/escalation.py b/packages/orchestration/escalation.py
index 6fdae93f..f19514f2 100644
--- a/packages/orchestration/escalation.py
+++ b/packages/orchestration/escalation.py
@@ -150,7 +150,7 @@ def answered_task_decisions(job: JobPlan | Any) -> list[dict[str, Any]]:
             if r.get("status") == ESCALATION_STATUS_ANSWERED]
 
 
-def awaiting_decision_task_ids(job: JobPlan | Any) -> set[UUID]:
+def awaiting_decision_task_ids(job: JobPlan | Any) -> set[str]:
     """Task ids whose branch is paused on an OPEN decision.
 
     This is what the executor withholds from the ready set: the tasks
@@ -159,12 +159,13 @@ def awaiting_decision_task_ids(job: JobPlan | Any) -> set[UUID]:
     bookkeeping, which is why the awaiting state is derived and never stored
     twice.
     """
-    awaiting: set[UUID] = set()
+    known = {str(task.task_id) for task in getattr(job, "tasks", ()) or ()}
+    awaiting: set[str] = set()
     for record in open_task_decisions(job):
-        try:
-            awaiting.add(UUID(str(record.get("task_id"))))
-        except (TypeError, ValueError):
-            continue                        # a malformed id blocks nothing
+        task_id = str(record.get("task_id") or "")
+        # An id naming no task of this job blocks nothing.
+        if task_id and task_id in known:
+            awaiting.add(task_id)
     return awaiting
 
 
diff --git a/packages/orchestration/flight_plan.py b/packages/orchestration/flight_plan.py
index f5879d5b..456857dd 100644
--- a/packages/orchestration/flight_plan.py
+++ b/packages/orchestration/flight_plan.py
@@ -12,7 +12,7 @@ from dataclasses import dataclass, field
 from pathlib import Path
 from typing import Any
 
-from packages.core.models import AcceptanceCheck, RunState
+from packages.core.models import RunState
 from packages.orchestration.pingpong_job import TaskEntry
 from packages.orchestration.prompt_facts import repo_facts_block
 from packages.orchestration.prompt_segments import (
@@ -522,9 +522,7 @@ def map_flight_plan_to_tasks(plan: FlightPlan) -> list[TaskEntry]:
     for pt in plan.tasks:
         task = TaskEntry(
             title=f"{pt.title}: {pt.goal}",
-            acceptance_checks=[
-                AcceptanceCheck(description=ac) for ac in pt.acceptance
-            ],
+            acceptance="\n".join(pt.acceptance),
             inputs={
                 "flight": {
                     "planned_id": pt.id,
diff --git a/packages/orchestration/mission_state.py b/packages/orchestration/mission_state.py
index 1736b87d..6080cbb6 100644
--- a/packages/orchestration/mission_state.py
+++ b/packages/orchestration/mission_state.py
@@ -751,7 +751,7 @@ def build_verify_first_task(previous_job: Any) -> Any:
     of the world.  It is a task, not an instruction: it occupies position 0 of
     the plan and every other task depends on it.
     """
-    from packages.core.models import AcceptanceCheck, RunState
+    from packages.core.models import RunState
     from packages.orchestration.pingpong_job import TaskEntry
 
     previous_id = str(getattr(previous_job, "job_id", "") or "")
@@ -761,10 +761,9 @@ def build_verify_first_task(previous_job: Any) -> Any:
         title=(
             f"Verify the previous job's Definition of Done still holds "
             f"(job {previous_id}): {described}"),
-        acceptance_checks=[AcceptanceCheck(
-            description=(
-                "The previous job's recorded verification passes against the "
-                "current state before any follow-up work starts."))],
+        acceptance=(
+            "The previous job's recorded verification passes against the "
+            "current state before any follow-up work starts."),
         inputs={
             "task_type": MISSION_VERIFY_TASK_TYPE,
             "verify_command": command,
@@ -810,7 +809,7 @@ def inject_verify_first(previous_job: Any, follow_up_tasks: list[Any]) -> list[A
         flight.setdefault("files_hint", [])
         inputs = dict(task.inputs)
         inputs["flight"] = flight
-        planned.append(task.model_copy(update={"inputs": inputs}))
+        planned.append(replace(task, inputs=inputs))
     return planned
 
 
diff --git a/packages/orchestration/pingpong_job.py b/packages/orchestration/pingpong_job.py
index b966594c..15abd687 100644
--- a/packages/orchestration/pingpong_job.py
+++ b/packages/orchestration/pingpong_job.py
@@ -31,11 +31,12 @@ from typing import TYPE_CHECKING, Any
 # them at runtime from the job record's plain JSON.
 from packages.core.models import Artifact, Budget, JobFences, RunState
 
-# F260 D2: one minting function per KIND of id. This module names JOBs and
+# F260 D2: one minting function per KIND of id. This module names JOBs, TASKs and
 # EPISODEs, so it mints through data_paths rather than spelling uuid4 inline.
-# Module-level and not function-scoped: JobPlan's default_factory below is read
-# when the class body runs, which a local import could never reach.
-from packages.orchestration.data_paths import mint_episode_id, mint_job_id
+# Module-level and not function-scoped: the default_factory of JobPlan and of
+# TaskEntry below is read when the class body runs, which a local import could
+# never reach.
+from packages.orchestration.data_paths import mint_episode_id, mint_job_id, mint_task_id
 
 if TYPE_CHECKING:
     from packages.orchestration.schemas.models import PlannedTask
@@ -150,7 +151,10 @@ class TaskProofSummary:
 @dataclass
 class TaskEntry:
     """A single task within a job."""
-    task_id: str = ""          # T001, T002, ... (by parse order)
+    # A job file's tasks are numbered T001, T002, ... by parse order, and the
+    # parser passes those ids; a task built by code mints its id, as the classic
+    # Task did.
+    task_id: str = field(default_factory=mint_task_id)
     source_heading_number: int = 0  # Original ## Task N number
     title: str = ""
     task_class: str = TASK_CLASS_DEFAULT
diff --git a/packages/orchestration/proposed_tasks.py b/packages/orchestration/proposed_tasks.py
index a200ae27..bde59897 100644
--- a/packages/orchestration/proposed_tasks.py
+++ b/packages/orchestration/proposed_tasks.py
@@ -665,7 +665,8 @@ def do_materialize(job_id: str, task_id: str, root: Path | None = None) -> Propo
             raise ValueError(f"Already materialized: {ptask.id} → {ptask.materialized_task_id}")
 
         task_dict = materialize_approved_task(ptask)
-        real_task = TaskEntry.model_validate(task_dict)
+        real_task = TaskEntry(task_id=task_dict["id"], title=task_dict["description"], inputs=task_dict["inputs"],
+                              status=task_dict["status"])
 
         job.tasks.append(real_task)
         save_job_plan(job, root)
diff --git a/packages/orchestration/test_execution_service.py b/packages/orchestration/test_execution_service.py
index a9304c05..4acd3ad3 100644
--- a/packages/orchestration/test_execution_service.py
+++ b/packages/orchestration/test_execution_service.py
@@ -857,7 +857,7 @@ def execute_test_run(
             result.next_safe_action = (
                 f"remedy repair start {job.job_id} {result.failure_artifact_id} --json"
                 if result.failure_artifact_id
-                else f"remedy job show {job.id} --json"
+                else f"remedy job show {job.job_id} --json"
             )
         elif status == "passed":
             result.next_safe_action = f"remedy job show {job.job_id} --json"
diff --git a/packages/orchestration/test_failure_artifact.py b/packages/orchestration/test_failure_artifact.py
index a059eccd..27b2546e 100644
--- a/packages/orchestration/test_failure_artifact.py
+++ b/packages/orchestration/test_failure_artifact.py
@@ -20,7 +20,7 @@ from dataclasses import dataclass, field
 from datetime import datetime, timezone
 from pathlib import Path
 from typing import Any
-from uuid import UUID, uuid4
+from uuid import uuid4
 
 # ---------------------------------------------------------------------------
 # Failure kinds (Step 941)
@@ -321,7 +321,7 @@ def persist_failure_artifact(job: Any, failure: TestFailureArtifact) -> Any:
         name=f"test-failure-{failure.artifact_id}",
         content=safe_content,
         kind=ArtifactKind.VERIFICATION,
-        task_id=str(UUID(failure.task_id)) if failure.task_id else None,
+        task_id=failure.task_id or None,
         metadata={
             "test_failure": True,
             "failure_kind": failure.failure_kind,
diff --git a/tests/orchestration/test_flight_plan.py b/tests/orchestration/test_flight_plan.py
index 51cd96f1..efb92784 100644
--- a/tests/orchestration/test_flight_plan.py
+++ b/tests/orchestration/test_flight_plan.py
@@ -110,7 +110,7 @@ class TestMapFlightPlanToTasks:
             flight = task.inputs["flight"]
             assert flight["planned_id"] == f"T{i + 1:03d}"
             assert flight["title"] == f"Task {i + 1}"
-            assert f"Thing {i + 1} done" in task.acceptance_checks[0].description
+            assert task.acceptance.splitlines() == [f"Thing {i + 1} done"]
 
     def test_description_combines_title_and_goal(self):
         fp = FlightPlan(**json.loads(_valid_plan_json(1)))
diff --git a/tests/orchestration/test_mint_call_sites.py b/tests/orchestration/test_mint_call_sites.py
index 5facb8ec..57d1c573 100644
--- a/tests/orchestration/test_mint_call_sites.py
+++ b/tests/orchestration/test_mint_call_sites.py
@@ -1,4 +1,4 @@
-"""F260 D2: the JOB, RUN and EPISODE call sites mint through data_paths, not inline.
+"""F260 D2: the JOB, RUN, EPISODE and TASK call sites mint through data_paths, not inline.
 
 WHY THIS FILE EXISTS. Moving four ``uuid4().hex[:16]`` expressions onto
 ``mint_job_id``, ``mint_run_id`` and ``mint_episode_id`` changes no behaviour: a site
@@ -6,7 +6,7 @@ that drifts back to an inline mint still produces a correct-looking 16-hex id, s
 existing suite goes red on its own. DECISION F260 D2 is about WHICH FUNCTION names each
 kind, and that is only observable by reading the call sites. These tests are that reading.
 
-THE TWO DATACLASS DEFAULTS ARE PINNED BY OBJECT IDENTITY. ``default_factory is
+THE THREE DATACLASS DEFAULTS ARE PINNED BY OBJECT IDENTITY. ``default_factory is
 data_paths.mint_job_id`` runs against the shipped function object, and — unlike any text
 check — is NOT satisfied by a look-alike ``lambda: mint_job_id()``, which would pass every
 behavioural test while putting the inline-expression habit straight back.
@@ -50,6 +50,12 @@ class TestMintCallSites:
 
         assert factory is data_paths.mint_run_id
 
+    def test_task_entry_task_id_default_is_the_mint_function_itself(self) -> None:
+        """Same identity reading for the TASK kind: a task built by code mints its id."""
+        factory = pingpong_job.TaskEntry.__dataclass_fields__["task_id"].default_factory
+
+        assert factory is data_paths.mint_task_id
+
     def test_every_active_episode_id_assignment_calls_mint_episode_id(self) -> None:
         """Both in-body episode sites, read by AST because there is no object to compare."""
         assignments = [
```
