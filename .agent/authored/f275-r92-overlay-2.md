# F275 round 92 — the flip's third overlay, part 2 of 4

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

This part holds 8 whole file diffs, `apps/cli/commands/job.py` through `apps/cli/commands/readiness.py`.

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
diff --git a/apps/cli/commands/job.py b/apps/cli/commands/job.py
index 84e7ab4b..3e2b49ea 100644
--- a/apps/cli/commands/job.py
+++ b/apps/cli/commands/job.py
@@ -14,7 +14,7 @@ from packages.orchestration.pingpong_job import JobPlan, TaskEntry
 from packages.orchestration.data_paths import resolve_data_root, resolve_job_id
 from packages.orchestration.job_runner import PlanJobResult
 from packages.orchestration.storage import JobNotFoundError
-from packages.orchestration.pingpong_job import load_job_plan, save_job_plan
+from packages.orchestration.pingpong_job import require_job_plan, save_job_plan
 
 if TYPE_CHECKING:
     import argparse
@@ -188,7 +188,7 @@ def _scope_label(job: JobPlan, scope: ProjectScope, known_ids: set[str]) -> str:
 def _cmd_show_job(job_id_str: str) -> None:
     job_id = resolve_job_id(job_id_str)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
@@ -234,7 +234,7 @@ def _print_intake_block(intake: dict) -> None:
 def _cmd_plan_job_local(job_id_str: str) -> None:
     job_id = resolve_job_id(job_id_str)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
@@ -369,7 +369,7 @@ def _cmd_plan_job_local(job_id_str: str) -> None:
 def _cmd_attach_repo(job_id_str: str, repo_path_str: str) -> None:
     job_id = resolve_job_id(job_id_str)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
@@ -392,7 +392,7 @@ def _cmd_attach_repo(job_id_str: str, repo_path_str: str) -> None:
 def _cmd_set_permission(job_id_str: str, action: str, capability_str: str) -> None:
     job_id = resolve_job_id(job_id_str)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
@@ -422,7 +422,7 @@ def _cmd_set_permission(job_id_str: str, action: str, capability_str: str) -> No
 def _cmd_show_permissions(job_id_str: str) -> None:
     job_id = resolve_job_id(job_id_str)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
@@ -437,7 +437,7 @@ def _cmd_show_permissions(job_id_str: str) -> None:
 def _cmd_run_next_task_local(job_id_str: str) -> None:
     job_id = resolve_job_id(job_id_str)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
@@ -759,7 +759,7 @@ def _cmd_job_run_cycles(
 
     job_id = resolve_job_id(job_id_str)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
@@ -986,7 +986,7 @@ def _cmd_job_resume(
 
     job_id = resolve_job_id(job_id_str)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
@@ -1095,7 +1095,7 @@ def _cmd_job_assumptions(job_id_str: str) -> None:
     """
     job_id = resolve_job_id(job_id_str)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
@@ -1118,7 +1118,7 @@ def _cmd_job_summary(job_id_str: str, *, json_output: bool = False) -> None:
 
     job_id = resolve_job_id(job_id_str)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
@@ -1207,7 +1207,7 @@ def _cmd_resume(
 
     job_id = resolve_job_id(job_id_str)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
@@ -1566,7 +1566,7 @@ def _cmd_job_status(job_id_str: str, *, json_output: bool = False) -> None:
 
     job_id = resolve_job_id(job_id_str)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError:
         if json_output:
             print(_json.dumps({'error': 'job_not_found', 'job_id': job_id_str}))
@@ -1684,7 +1684,7 @@ def _cmd_job_run_report(job_id_str: str, *, interim: bool = False,
 
     job_id = resolve_job_id(job_id_str)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError:
         # A clean error, never a traceback: an unknown id is a normal thing for
         # a human to type.
@@ -1724,7 +1724,7 @@ def _cmd_job_report(job_id_str: str, *, json_output: bool = False) -> None:
 
     job_id = resolve_job_id(job_id_str)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError:
         if json_output:
             print(_json.dumps({'error': 'job_not_found', 'job_id': job_id_str}))
@@ -1833,7 +1833,7 @@ def _cmd_job_digest(job_id_str: str, *, json_output: bool = False) -> None:
 
     job_id = resolve_job_id(job_id_str)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError:
         # A clean error, never a traceback: an unknown id is a normal thing
         # for a human to type (the same shape _cmd_job_report uses above).
@@ -1888,7 +1888,7 @@ def _cmd_job_dod(job_id_str: str, *, json_output: bool = False) -> None:
 
     job_id = resolve_job_id(job_id_str)
     try:
-        load_job_plan(job_id)
+        require_job_plan(job_id)
     except JobNotFoundError:
         if json_output:
             print(_json.dumps({'error': 'job_not_found', 'job_id': job_id_str}))
@@ -1965,7 +1965,7 @@ def _cmd_job_fulfill(
         sys.exit(1)
 
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError:
         if json_output:
             print(_json.dumps({'error': 'job_not_found', 'job_id': job_id_str}))
@@ -2010,7 +2010,7 @@ def _cmd_job_fences(job_id_str: str, *, json_output: bool = False) -> None:
     )
 
     try:
-        job = load_job_plan(resolve_job_id(job_id_str))
+        job = require_job_plan(resolve_job_id(job_id_str))
     except JobNotFoundError:
         print(f"Job not found: {job_id_str}", file=sys.stderr)
         sys.exit(1)
@@ -2116,7 +2116,7 @@ def _cmd_job_budget(
     import json as _json
 
     from packages.orchestration.budget_guard import evaluate_budget
-    from packages.orchestration.pingpong_job import load_job_plan
+    from packages.orchestration.pingpong_job import load_job_plan, require_job_plan
 
     _job_display_id = job_id
     _budgets = None
@@ -2172,7 +2172,7 @@ def _cmd_job_budget(
 
     if _found_as is None:
         try:
-            job = load_job_plan(job_id)
+            job = require_job_plan(job_id)
         except JobNotFoundError:
             print(f"Error: job {job_id!r} not found.", file=sys.stderr)
             sys.exit(1)
diff --git a/apps/cli/commands/job_context_cmd.py b/apps/cli/commands/job_context_cmd.py
index 4dd13088..f6904d6b 100644
--- a/apps/cli/commands/job_context_cmd.py
+++ b/apps/cli/commands/job_context_cmd.py
@@ -260,9 +260,8 @@ def _cmd_job_context(
         export_omitted_context_json,
     )
     from packages.orchestration.data_paths import resolve_any_job_id
-    from packages.orchestration.pingpong_job import load_job_plan
+    from packages.orchestration.pingpong_job import require_job_plan
     from packages.orchestration.storage import JobNotFoundError
-    from packages.orchestration.pingpong_job import load_job_plan
 
     try:
         # Resolving across BOTH stores is what lets this command answer for a
@@ -270,13 +269,9 @@ def _cmd_job_context(
         # resolvers, `resolve_job_id` searched the classic store alone and so
         # answered "no job matches prefix" for every one of them; the two names
         # are now one function, and this call site keeps `resolve_any_job_id`
-        # because that name states what it needs. WHY the unified record is read
-        # FIRST: it is the same order
-        # `apps/cli/commands/job_stop_cmd.py::_load_job` already reads in.
+        # because that name states what it needs.
         resolved = resolve_any_job_id(job_id_str)
-        job = load_job_plan(resolved)
-        if job is None:
-            job = load_job_plan(resolved)
+        job = require_job_plan(resolved)
     except JobNotFoundError:
         print(f"Job not found: {job_id_str}", file=sys.stderr)
         sys.exit(1)
diff --git a/apps/cli/commands/memory.py b/apps/cli/commands/memory.py
index c4bf8f64..7bfb67fb 100644
--- a/apps/cli/commands/memory.py
+++ b/apps/cli/commands/memory.py
@@ -139,7 +139,7 @@ def _cmd_memory_learn(
     json_output: bool = False,
 ) -> None:
     from packages.orchestration.storage import JobNotFoundError
-    from packages.orchestration.pingpong_job import load_job_plan
+    from packages.orchestration.pingpong_job import require_job_plan
 
     try:
         job_id = lookup_job_id(job_id_str)
@@ -147,7 +147,7 @@ def _cmd_memory_learn(
         print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
         sys.exit(1)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
diff --git a/apps/cli/commands/patch.py b/apps/cli/commands/patch.py
index cc0c2235..afa3d44c 100644
--- a/apps/cli/commands/patch.py
+++ b/apps/cli/commands/patch.py
@@ -9,7 +9,7 @@ from typing import TYPE_CHECKING
 
 from packages.orchestration.data_paths import resolve_job_id
 from packages.orchestration.storage import JobNotFoundError
-from packages.orchestration.pingpong_job import load_job_plan, save_job_plan
+from packages.orchestration.pingpong_job import require_job_plan, save_job_plan
 
 if TYPE_CHECKING:
     import argparse
@@ -27,7 +27,7 @@ def _cmd_list_patch_intents(
 ) -> None:
     job_id = resolve_job_id(job_id_str)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
@@ -63,7 +63,7 @@ def _cmd_list_patch_intents(
 def _cmd_show_patch_intent(job_id_str: str, intent_id: str) -> None:
     job_id = resolve_job_id(job_id_str)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
@@ -92,7 +92,7 @@ def _cmd_show_patch_intent(job_id_str: str, intent_id: str) -> None:
 def _cmd_approve_patch_intent(job_id_str: str, intent_id: str, reason: str | None) -> None:
     job_id = resolve_job_id(job_id_str)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
@@ -121,7 +121,7 @@ def _cmd_approve_patch_intent(job_id_str: str, intent_id: str, reason: str | Non
 def _cmd_reject_patch_intent(job_id_str: str, intent_id: str, reason: str | None) -> None:
     job_id = resolve_job_id(job_id_str)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
@@ -150,7 +150,7 @@ def _cmd_reject_patch_intent(job_id_str: str, intent_id: str, reason: str | None
 def _cmd_apply_patch_intent(job_id_str: str, intent_id: str, *, json_output: bool = False) -> None:
     job_id = resolve_job_id(job_id_str)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
@@ -187,7 +187,7 @@ def _cmd_revert_patch_intent(
     """
     job_id = resolve_job_id(job_id_str)
     try:
-        load_job_plan(job_id)
+        require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
@@ -318,7 +318,7 @@ def _cmd_approve_hunks(
     """
     job_id = resolve_job_id(job_id_str)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
diff --git a/apps/cli/commands/policy.py b/apps/cli/commands/policy.py
index f69cd658..3aaf2a21 100644
--- a/apps/cli/commands/policy.py
+++ b/apps/cli/commands/policy.py
@@ -9,7 +9,7 @@ from typing import TYPE_CHECKING
 
 from packages.orchestration.data_paths import lookup_job_id
 from packages.orchestration.storage import JobNotFoundError
-from packages.orchestration.pingpong_job import load_job_plan
+from packages.orchestration.pingpong_job import require_job_plan
 
 if TYPE_CHECKING:
     import argparse
@@ -22,7 +22,7 @@ def _cmd_run_contract(job_id_str: str, *, json_output: bool = False) -> None:
         print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
         sys.exit(1)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
@@ -57,7 +57,7 @@ def _cmd_token_policy(job_id_str: str, *, json_output: bool = False) -> None:
         print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
         sys.exit(1)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
diff --git a/apps/cli/commands/project.py b/apps/cli/commands/project.py
index 6d1b97a9..10702dc6 100644
--- a/apps/cli/commands/project.py
+++ b/apps/cli/commands/project.py
@@ -10,7 +10,7 @@ from uuid import UUID
 
 from packages.orchestration.data_paths import lookup_job_id
 from packages.orchestration.storage import JobNotFoundError
-from packages.orchestration.pingpong_job import list_job_plans, load_job_plan, save_job_plan
+from packages.orchestration.pingpong_job import list_job_plans, require_job_plan, save_job_plan
 
 if TYPE_CHECKING:
     import argparse
@@ -156,7 +156,7 @@ def _cmd_attach_project_job(project_id_str: str, job_id_str: str) -> None:
         sys.exit(1)
     try:
         job_id = lookup_job_id(job_id_str)
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except (ValueError, JobNotFoundError):
         print(f"ERROR: job not found: {job_id_str}", file=sys.stderr)
         sys.exit(1)
@@ -452,7 +452,7 @@ def _cmd_project_adopt(
     resolved_id = resolve_job_id(job_id_str)
 
     try:
-        job = load_job_plan(resolved_id)
+        job = require_job_plan(resolved_id)
     except JobNotFoundError:
         print(f"Error: job not found: {resolved_id[:8]}", file=sys.stderr)
         sys.exit(3)
diff --git a/apps/cli/commands/propose_cmd.py b/apps/cli/commands/propose_cmd.py
index e835472d..a4b4194f 100644
--- a/apps/cli/commands/propose_cmd.py
+++ b/apps/cli/commands/propose_cmd.py
@@ -40,9 +40,9 @@ def _require_job(job_id: str, args: Any) -> bool:
     """
     try:
         from packages.orchestration.storage import JobNotFoundError, JobStoreError
-        from packages.orchestration.pingpong_job import load_job_plan
+        from packages.orchestration.pingpong_job import require_job_plan
         uid = lookup_job_id(job_id)
-        load_job_plan(uid)
+        require_job_plan(uid)
         return True
     except (ValueError, TypeError):
         msg = f"Invalid job ID: {job_id}"
diff --git a/apps/cli/commands/readiness.py b/apps/cli/commands/readiness.py
index ba815c1a..0267c237 100644
--- a/apps/cli/commands/readiness.py
+++ b/apps/cli/commands/readiness.py
@@ -10,7 +10,7 @@ from uuid import UUID
 
 from packages.orchestration.data_paths import lookup_job_id
 from packages.orchestration.storage import JobNotFoundError
-from packages.orchestration.pingpong_job import load_job_plan
+from packages.orchestration.pingpong_job import require_job_plan
 
 if TYPE_CHECKING:
     import argparse
@@ -23,7 +23,7 @@ def _cmd_readiness_job(job_id_str: str, *, json_output: bool = False) -> None:
         print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
         sys.exit(1)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
```
