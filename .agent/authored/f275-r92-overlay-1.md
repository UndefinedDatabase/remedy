# F275 round 92 — the flip's third overlay, part 1 of 4

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

This part holds 9 whole file diffs, `apps/cli/commands/brain.py` through `apps/cli/commands/guide.py`.

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
diff --git a/apps/cli/commands/brain.py b/apps/cli/commands/brain.py
index f76dea32..6e59a96f 100644
--- a/apps/cli/commands/brain.py
+++ b/apps/cli/commands/brain.py
@@ -9,7 +9,7 @@ from typing import TYPE_CHECKING
 
 from packages.orchestration.data_paths import lookup_job_id, resolve_data_root
 from packages.orchestration.storage import JobNotFoundError
-from packages.orchestration.pingpong_job import load_job_plan
+from packages.orchestration.pingpong_job import require_job_plan
 
 if TYPE_CHECKING:
     import argparse
@@ -22,7 +22,7 @@ def _cmd_brain(job_id_str: str, *, json_output: bool = False) -> None:
         print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
         sys.exit(1)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
@@ -69,7 +69,7 @@ def _cmd_brain_node(job_id_str: str, node_id: str, *, json_output: bool = False)
         print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
         sys.exit(1)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
@@ -120,7 +120,7 @@ def _cmd_brain_view(job_id_str: str) -> None:
         print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
         sys.exit(1)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
@@ -173,7 +173,7 @@ def _prepare_viewer(job_id_str: str):
         print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
         sys.exit(1)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
@@ -286,7 +286,7 @@ def _cmd_context(job_id_str: str, *, json_output: bool = False) -> None:
         print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
         sys.exit(1)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
@@ -340,7 +340,7 @@ def _cmd_trust_report(job_id_str: str) -> None:
         print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
         sys.exit(1)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
@@ -365,7 +365,7 @@ def _cmd_timeline(job_id_str: str) -> None:
         print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
         sys.exit(1)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
@@ -386,7 +386,7 @@ def _cmd_cockpit(job_id_str: str) -> None:
         print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
         sys.exit(1)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
@@ -411,7 +411,7 @@ def _cmd_constitution(job_id_str: str) -> None:
         print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
         sys.exit(1)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
@@ -446,7 +446,7 @@ def _cmd_brain_continue(
         print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
         sys.exit(1)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
@@ -494,7 +494,7 @@ def _cmd_agent_loop(job_id_str: str) -> None:
         print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
         sys.exit(1)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
diff --git a/apps/cli/commands/change.py b/apps/cli/commands/change.py
index e07019be..effeed09 100644
--- a/apps/cli/commands/change.py
+++ b/apps/cli/commands/change.py
@@ -9,7 +9,7 @@ from typing import TYPE_CHECKING
 
 from packages.orchestration.data_paths import resolve_data_root, resolve_job_id
 from packages.orchestration.storage import JobNotFoundError
-from packages.orchestration.pingpong_job import load_job_plan
+from packages.orchestration.pingpong_job import require_job_plan
 
 if TYPE_CHECKING:
     import argparse
@@ -18,7 +18,7 @@ if TYPE_CHECKING:
 def _cmd_change_list(job_id_str: str, *, json_output: bool = False) -> None:
     job_id = resolve_job_id(job_id_str)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
@@ -43,7 +43,7 @@ def _cmd_change_list(job_id_str: str, *, json_output: bool = False) -> None:
 def _cmd_change_show(job_id_str: str, intent_id: str, *, json_output: bool = False) -> None:
     job_id = resolve_job_id(job_id_str)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
@@ -73,7 +73,7 @@ def _cmd_change_show(job_id_str: str, intent_id: str, *, json_output: bool = Fal
 def _cmd_change_proof(job_id_str: str, *, path: str | None = None, json_output: bool = False) -> None:
     job_id = resolve_job_id(job_id_str)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
diff --git a/apps/cli/commands/context.py b/apps/cli/commands/context.py
index 2dea199c..9e687b30 100644
--- a/apps/cli/commands/context.py
+++ b/apps/cli/commands/context.py
@@ -10,7 +10,7 @@ from uuid import UUID
 
 from packages.orchestration.data_paths import lookup_job_id
 from packages.orchestration.storage import JobNotFoundError
-from packages.orchestration.pingpong_job import load_job_plan
+from packages.orchestration.pingpong_job import require_job_plan
 
 if TYPE_CHECKING:
     import argparse
@@ -29,7 +29,7 @@ def _cmd_context_inspect(
         print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
         sys.exit(1)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
diff --git a/apps/cli/commands/dashboard_cmd.py b/apps/cli/commands/dashboard_cmd.py
index f9792b36..5d0b3898 100644
--- a/apps/cli/commands/dashboard_cmd.py
+++ b/apps/cli/commands/dashboard_cmd.py
@@ -17,7 +17,7 @@ def _cmd_dashboard_job(job_id_str: str, *, json_output: bool = False) -> None:
     from packages.orchestration.dashboard import build_job_dashboard, summarize_job_dashboard
     from packages.orchestration.data_paths import resolve_data_root
     from packages.orchestration.storage import JobNotFoundError
-    from packages.orchestration.pingpong_job import load_job_plan
+    from packages.orchestration.pingpong_job import require_job_plan
     from packages.orchestration.timeline import load_run_events
 
     try:
@@ -26,7 +26,7 @@ def _cmd_dashboard_job(job_id_str: str, *, json_output: bool = False) -> None:
         print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
         sys.exit(1)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
diff --git a/apps/cli/commands/decision.py b/apps/cli/commands/decision.py
index 43d06153..50dc533b 100644
--- a/apps/cli/commands/decision.py
+++ b/apps/cli/commands/decision.py
@@ -22,12 +22,12 @@ def _load_job_events(job_id_str: str):
     """Load job and events. Returns (job, events, job_id_str)."""
     from packages.orchestration.data_paths import resolve_data_root
     from packages.orchestration.storage import JobNotFoundError
-    from packages.orchestration.pingpong_job import load_job_plan
+    from packages.orchestration.pingpong_job import require_job_plan
     from packages.orchestration.timeline import load_run_events
 
     job_id = resolve_job_id(job_id_str)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
@@ -251,11 +251,11 @@ def _cmd_decision_resolve(
             find_task_decision,
         )
         from packages.orchestration.storage import JobNotFoundError
-        from packages.orchestration.pingpong_job import load_job_plan, save_job_plan
+        from packages.orchestration.pingpong_job import require_job_plan, save_job_plan
 
         job_id = _rji(job_id_str)
         try:
-            job = load_job_plan(job_id)
+            job = require_job_plan(job_id)
         except JobNotFoundError as exc:
             print(f"Error: {exc}", file=sys.stderr)
             sys.exit(1)
@@ -295,11 +295,11 @@ def _cmd_decision_resolve(
     elif decision_id.startswith("fp:"):
         from packages.orchestration.data_paths import resolve_job_id as _rji
         from packages.orchestration.storage import JobNotFoundError
-        from packages.orchestration.pingpong_job import load_job_plan
+        from packages.orchestration.pingpong_job import require_job_plan
 
         job_id = _rji(job_id_str)
         try:
-            job = load_job_plan(job_id)
+            job = require_job_plan(job_id)
         except JobNotFoundError as exc:
             print(f"Error: {exc}", file=sys.stderr)
             sys.exit(1)
diff --git a/apps/cli/commands/do_cmd.py b/apps/cli/commands/do_cmd.py
index 9184e39a..d357800b 100644
--- a/apps/cli/commands/do_cmd.py
+++ b/apps/cli/commands/do_cmd.py
@@ -2931,11 +2931,11 @@ def _cmd_do_replan(
     """Regenerate the flight plan for an existing job."""
     from packages.orchestration.data_paths import job_evidence_export_dir, resolve_job_id
     from packages.orchestration.storage import JobNotFoundError
-    from packages.orchestration.pingpong_job import load_job_plan, save_job_plan
+    from packages.orchestration.pingpong_job import require_job_plan, save_job_plan
 
     job_id = resolve_job_id(job_id_str)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
diff --git a/apps/cli/commands/event.py b/apps/cli/commands/event.py
index fedfc540..ce808aa1 100644
--- a/apps/cli/commands/event.py
+++ b/apps/cli/commands/event.py
@@ -17,7 +17,7 @@ def _load_job_events(job_id_str: str):
     """Load job and events, exit on error. Returns (job, events, job_id_str)."""
     from packages.orchestration.data_paths import resolve_data_root
     from packages.orchestration.storage import JobNotFoundError
-    from packages.orchestration.pingpong_job import load_job_plan
+    from packages.orchestration.pingpong_job import require_job_plan
     from packages.orchestration.timeline import load_run_events
 
     try:
@@ -26,7 +26,7 @@ def _load_job_events(job_id_str: str):
         print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
         sys.exit(1)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
diff --git a/apps/cli/commands/file.py b/apps/cli/commands/file.py
index 84e59775..cb28810b 100644
--- a/apps/cli/commands/file.py
+++ b/apps/cli/commands/file.py
@@ -9,7 +9,7 @@ from typing import TYPE_CHECKING
 
 from packages.orchestration.data_paths import lookup_job_id, resolve_data_root
 from packages.orchestration.storage import JobNotFoundError
-from packages.orchestration.pingpong_job import load_job_plan
+from packages.orchestration.pingpong_job import require_job_plan
 
 if TYPE_CHECKING:
     import argparse
@@ -22,7 +22,7 @@ def _cmd_file_why(job_id_str: str, path: str, *, json_output: bool = False) -> N
         print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
         sys.exit(1)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
diff --git a/apps/cli/commands/guide.py b/apps/cli/commands/guide.py
index 0f6627d4..8ccd84d9 100644
--- a/apps/cli/commands/guide.py
+++ b/apps/cli/commands/guide.py
@@ -9,7 +9,7 @@ from typing import TYPE_CHECKING
 
 from packages.orchestration.data_paths import lookup_job_id, resolve_data_root
 from packages.orchestration.storage import JobNotFoundError
-from packages.orchestration.pingpong_job import load_job_plan
+from packages.orchestration.pingpong_job import require_job_plan
 
 if TYPE_CHECKING:
     import argparse
@@ -22,7 +22,7 @@ def _cmd_guide_job(job_id_str: str, *, json_output: bool = False) -> None:
         print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
         sys.exit(1)
     try:
-        job = load_job_plan(job_id)
+        job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
```
