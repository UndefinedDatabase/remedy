# F275 round 95 — the flip's sixth overlay, part 2 of 4

What the sixth overlay changes. Production code under `packages/` and `apps/` that read `.id`
or `.name` off a job it loaded, under the local names `job`, `j` or `plan`, reads the unified
record's `job_id` and `job_title` (79 reads; the classic store's own module is untouched). The
job doubles tests hand that code spell the same: the `_FakeJob`, `_Job` and `_LoopJob` classes
carry `job_id` and `job_title`, the `SimpleNamespace` stubs of the `review list` tests pass
`job_id=`, and the tests read those names back. A handler test that doubles the job loader as
the first context manager of its `with` statement now also doubles, as the second, the
resolver the handler's module binds (`resolve_job_id` or `lookup_job_id`) with an identity, so
the handler still receives the id the test built (27 `with` statements).

This part holds 7 whole file diffs, `packages/orchestration/project_registry.py` through `tests/cli/test_change_proof_cli.py`.

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
diff --git a/packages/orchestration/project_registry.py b/packages/orchestration/project_registry.py
index f3b8b272..ed19003c 100644
--- a/packages/orchestration/project_registry.py
+++ b/packages/orchestration/project_registry.py
@@ -785,7 +785,7 @@ def summarize_project(
     Redaction: no artifact content, no approval reasons, no event messages,
     no diff previews, no command output, no raw exception text.
     """
-    job_map = {str(j.id): j for j in jobs}
+    job_map = {str(j.job_id): j for j in jobs}
     lines: list[str] = []
     lines.append("Remedy Project Registry v0")
     lines.append(f"Project : {project.name}")
@@ -806,7 +806,7 @@ def summarize_project(
         for jid in project.job_ids:
             j = job_map.get(jid)
             if j is not None:
-                lines.append(f"  {jid[:8]}  {j.state.value:<12}  {j.name[:40]}")
+                lines.append(f"  {jid[:8]}  {j.state.value:<12}  {j.job_title[:40]}")
             else:
                 lines.append(f"  {jid[:8]}  (not loaded)")
     else:
diff --git a/packages/orchestration/project_summary.py b/packages/orchestration/project_summary.py
index d6eb5786..b6f30d75 100644
--- a/packages/orchestration/project_summary.py
+++ b/packages/orchestration/project_summary.py
@@ -74,7 +74,7 @@ def build_project_summary(
     pending_work: list[str] = []
 
     for job in jobs:
-        jid = str(job.id)
+        jid = str(job.job_id)
         state = job.state.value if hasattr(job.state, "value") else str(job.state)
         events = all_events.get(jid, [])
 
@@ -117,7 +117,7 @@ def build_project_summary(
                 total_tokens += est
 
     for job in jobs:
-        jid = str(job.id)
+        jid = str(job.job_id)
         events = all_events.get(jid, [])
         stop_events = [e for e in events if e.get("event") == "stop_reason_recorded"]
         for se in stop_events:
@@ -208,7 +208,7 @@ def detect_patterns(
     repair_exhaustions: list[tuple[str, str]] = []
 
     for job in jobs:
-        jid = str(job.id)
+        jid = str(job.job_id)
         events = all_events.get(jid, [])
 
         for ev in events:
diff --git a/packages/orchestration/provider_patch_material.py b/packages/orchestration/provider_patch_material.py
index 99f6ce3b..0a894127 100644
--- a/packages/orchestration/provider_patch_material.py
+++ b/packages/orchestration/provider_patch_material.py
@@ -376,7 +376,7 @@ def materialize_accepted_candidate(
     from packages.core.models import Artifact, ArtifactKind
     from packages.orchestration.approval_queue import get_patch_intent, make_intent_id
 
-    result = ProviderPatchMaterializationResult(job_id=str(job.id))
+    result = ProviderPatchMaterializationResult(job_id=str(job.job_id))
     candidate_hash = hashlib.sha256(raw_patch.encode("utf-8", errors="replace")).hexdigest()
 
     # Idempotency: same candidate hash → return the existing material/intent.
@@ -413,7 +413,7 @@ def materialize_accepted_candidate(
     entry = ProviderPatchMaterialEntry(target_path=ext.target_path, action=ext.action,
                                        line_count=len(ext.added_lines))
     material = ProviderPatchMaterial(
-        material_id=material_id, job_id=str(job.id), quarantine_id=report.quarantine_id,
+        material_id=material_id, job_id=str(job.job_id), quarantine_id=report.quarantine_id,
         trust_report_id=report.report_id, failure_artifact_id=report.failure_artifact_id,
         repair_attempt_id=report.repair_attempt_id, candidate_hash=candidate_hash,
         patch_format=candidate.patch_format, target_path_count=1, operation_count=1,
@@ -421,7 +421,7 @@ def materialize_accepted_candidate(
         entries=[entry], created_at=_now(),
     )
 
-    if not store_material(str(job.id), data_dir, material, raw_patch):
+    if not store_material(str(job.job_id), data_dir, material, raw_patch):
         result.state = MaterialState.FAILED
         result.reason = "material_store_failed"
         result.safe_summary = "Patch material could not be stored privately."
diff --git a/packages/orchestration/self_dogfood_execution.py b/packages/orchestration/self_dogfood_execution.py
index 512fee13..69ff5929 100644
--- a/packages/orchestration/self_dogfood_execution.py
+++ b/packages/orchestration/self_dogfood_execution.py
@@ -708,7 +708,7 @@ def _intent_proof_status(job: Any, intent_id: str, data_dir: Path) -> str:
     try:
         from packages.orchestration.proof_chain import build_proof_chain
         from packages.orchestration.timeline import load_run_events
-        events = load_run_events(data_dir, str(job.id))
+        events = load_run_events(data_dir, str(job.job_id))
         chain = build_proof_chain(job, events, data_dir=data_dir)
         change = next((c for c in chain.changes if c.intent_id == intent_id), None)
         if change is not None:
diff --git a/packages/orchestration/test_execution_service.py b/packages/orchestration/test_execution_service.py
index 4acd3ad3..3a566fb9 100644
--- a/packages/orchestration/test_execution_service.py
+++ b/packages/orchestration/test_execution_service.py
@@ -474,7 +474,7 @@ def _validate_linkage(
                 allowed=False,
                 gate="linkage",
                 reason=f"task_id {task_id!r} not found in job",
-                next_safe_action=f"remedy job show {job.id} --json",
+                next_safe_action=f"remedy job show {job.job_id} --json",
             )
     if intent_id:
         # Intent IDs live in artifacts / metadata — check metadata
@@ -487,7 +487,7 @@ def _validate_linkage(
                 allowed=False,
                 gate="linkage",
                 reason=f"intent_id {intent_id!r} not found in job",
-                next_safe_action=f"remedy job show {job.id} --json",
+                next_safe_action=f"remedy job show {job.job_id} --json",
             )
     if apply_id:
         known_applies: set[str] = set()
@@ -499,7 +499,7 @@ def _validate_linkage(
                 allowed=False,
                 gate="linkage",
                 reason=f"apply_id {apply_id!r} not found in job",
-                next_safe_action=f"remedy job show {job.id} --json",
+                next_safe_action=f"remedy job show {job.job_id} --json",
             )
     return None
 
@@ -630,7 +630,7 @@ def execute_test_run(
         result.status = "blocked"
         result.stop_reason = "target_repo_not_a_directory"
         result.safe_summary = "Target repository path does not exist."
-        result.next_safe_action = f"remedy job attach-repo {job.id} <repo_path>"
+        result.next_safe_action = f"remedy job attach-repo {job.job_id} <repo_path>"
         return result
 
     # ── Gate 4: Load and validate contract ──────────────────────────────────
@@ -641,7 +641,7 @@ def execute_test_run(
         result.status = "blocked"
         result.stop_reason = "contract_invalid"
         result.safe_summary = "Run contract failed validation."
-        result.next_safe_action = f"remedy contract inspect {job.id} --json"
+        result.next_safe_action = f"remedy contract inspect {job.job_id} --json"
         return result
 
     # ── Gate 5: Load usage ───────────────────────────────────────────────────
@@ -763,14 +763,14 @@ def execute_test_run(
             result.status = "blocked"
             result.stop_reason = "high_risk_command"
             result.safe_summary = "Discovered command has high risk rating — blocked."
-            result.next_safe_action = f"remedy test discover {job.id} --json"
+            result.next_safe_action = f"remedy test discover {job.job_id} --json"
             return result
 
         if candidate.argv[0] not in _EXECUTION_SAFE_EXECUTABLES:
             result.status = "blocked"
             result.stop_reason = "executable_not_in_safe_list"
             result.safe_summary = "Discovered executable not in safety allowlist."
-            result.next_safe_action = f"remedy test discover {job.id} --json"
+            result.next_safe_action = f"remedy test discover {job.job_id} --json"
             return result
 
         result.command_safe = candidate.display
@@ -786,7 +786,7 @@ def execute_test_run(
             result.status = "blocked"
             result.stop_reason = "no_runtime_remaining"
             result.safe_summary = "No runtime budget remaining in contract."
-            result.next_safe_action = f"remedy contract set {job.id} max_runtime_seconds <n>"
+            result.next_safe_action = f"remedy contract set {job.job_id} max_runtime_seconds <n>"
             return result
 
         # ── Gate 9: Execute ──────────────────────────────────────────────────
diff --git a/packages/orchestration/ui_server.py b/packages/orchestration/ui_server.py
index b0bf978d..20dd4754 100644
--- a/packages/orchestration/ui_server.py
+++ b/packages/orchestration/ui_server.py
@@ -600,7 +600,7 @@ def _build_snapshot_section(job: Any, data_dir: Path | None) -> dict[str, Any]:
         reverted = 0
         drift = False
         for aid in apply_ids:
-            truth = build_snapshot_truth(str(job.id), apply_id=aid, data_dir=data_dir)
+            truth = build_snapshot_truth(str(job.job_id), apply_id=aid, data_dir=data_dir)
             if (truth.apply_state == "applied"
                     and truth.snapshot_verified_now
                     and truth.recovery_material_available
@@ -698,7 +698,7 @@ def _build_repair_section(job: Any) -> dict[str, Any]:
                 resolved_failure_count += 1
     next_action = ""
     if pending_intent_id:
-        next_action = f"remedy patch approve {job.id} {pending_intent_id}"
+        next_action = f"remedy patch approve {job.job_id} {pending_intent_id}"
     return {
         "attempt_count": attempt_count,
         "pending_approval_count": pending_approval,
@@ -834,7 +834,7 @@ def _build_self_execution_section(job: Any) -> dict[str, Any]:
     Counts + latest state only. No buttons, no mutation, no raw content."""
     try:
         from packages.orchestration.self_dogfood_execution import list_attempts
-        attempts = [a for a in list_attempts() if a.get("job_id") == str(job.id)]
+        attempts = [a for a in list_attempts() if a.get("job_id") == str(job.job_id)]
         by_state: dict[str, int] = {}
         for a in attempts:
             by_state[a.get("state", "")] = by_state.get(a.get("state", ""), 0) + 1
@@ -1106,7 +1106,7 @@ def _build_job_plan_dashboard(job: Any) -> dict[str, Any]:
 
     return {
         "version": 3,
-        "job_id": str(job.id),
+        "job_id": str(job.job_id),
         "generated_at": generated_at,
         "source": "job_plan_adapter",
         "live": {
@@ -1600,12 +1600,12 @@ def _build_project_summary_section(job: Any) -> dict[str, Any] | None:
         from uuid import UUID
         project = load_project(UUID(project_id))
         all_jobs = list_job_plans()
-        linked_jobs = [j for j in all_jobs if str(j.id) in project.job_ids]
+        linked_jobs = [j for j in all_jobs if str(j.job_id) in project.job_ids]
 
         data_dir = resolve_data_root()
         all_events: dict[str, list[dict]] = {}
         for j in linked_jobs:
-            all_events[str(j.id)] = load_run_events(data_dir, j.id)
+            all_events[str(j.job_id)] = load_run_events(data_dir, j.job_id)
 
         summary = build_project_summary(project, linked_jobs, all_events)
         patterns = detect_patterns(linked_jobs, all_events)
@@ -2264,7 +2264,7 @@ def _build_events_since_json(job: Any, cursor: str) -> dict[str, Any]:
     ]
     return {
         "version": 1,
-        "job_id": str(job.id),
+        "job_id": str(job.job_id),
         "cursor": str(len(events)),
         "events": safe,
     }
@@ -2935,7 +2935,7 @@ class _RemedyHandler(BaseHTTPRequestHandler):
                 # are out the status line is spent and cannot say "not found".
                 self._send_json(*err)
                 return
-            if not acquire_sse_slot(str(job.id)):
+            if not acquire_sse_slot(str(job.job_id)):
                 # 429 for the same reason and in the same window: a refused
                 # stream must not consume the capacity it was refused.
                 self._send_json(*_safe_error(429, "too many streams for this job"))
@@ -2950,7 +2950,7 @@ class _RemedyHandler(BaseHTTPRequestHandler):
                 )
                 self._send_sse_stream(job, str(start))
             finally:
-                release_sse_slot(str(job.id))
+                release_sse_slot(str(job.job_id))
             return
 
         # /api/layers
@@ -3148,7 +3148,7 @@ class _RemedyHandler(BaseHTTPRequestHandler):
             except (OSError, RuntimeError, ValueError, TypeError):
                 # D18, clause four: an effect that RAISED is neither `accepted`,
                 # which would be false, nor unaudited, which would break D6.
-                self._audit_attempt(str(job.id), "rejected_effect", create=True,
+                self._audit_attempt(str(job.job_id), "rejected_effect", create=True,
                                     payload=payload)
                 self._send_json(*_safe_error(500, COMMAND_EFFECT_FAILED_MESSAGE))
                 return
@@ -3180,7 +3180,7 @@ class _RemedyHandler(BaseHTTPRequestHandler):
             except (OSError, RuntimeError, ValueError, TypeError):
                 # D18, clause four: an effect that RAISED is neither `accepted`,
                 # which would be false, nor unaudited, which would break D6.
-                self._audit_attempt(str(job.id), "rejected_effect", create=True,
+                self._audit_attempt(str(job.job_id), "rejected_effect", create=True,
                                     payload=payload)
                 self._send_json(*_safe_error(500, COMMAND_EFFECT_FAILED_MESSAGE))
                 return
diff --git a/tests/cli/test_change_proof_cli.py b/tests/cli/test_change_proof_cli.py
index a6863293..7ac8494d 100644
--- a/tests/cli/test_change_proof_cli.py
+++ b/tests/cli/test_change_proof_cli.py
@@ -82,6 +82,7 @@ def test_handler_text_output(capsys):
     job_id = str(job.job_id)
 
     with patch("apps.cli.commands.change.require_job_plan", return_value=job), \
+         patch("apps.cli.commands.change.resolve_job_id", side_effect=lambda raw: raw), \
          patch("apps.cli.commands.change.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=[]):
         _cmd_change_proof(job_id)
@@ -98,6 +99,7 @@ def test_handler_text_does_not_overclaim_verified(capsys):
     job_id = str(job.job_id)
 
     with patch("apps.cli.commands.change.require_job_plan", return_value=job), \
+         patch("apps.cli.commands.change.resolve_job_id", side_effect=lambda raw: raw), \
          patch("apps.cli.commands.change.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=events):
         _cmd_change_proof(job_id)
@@ -112,6 +114,7 @@ def test_handler_json_output(capsys):
     job_id = str(job.job_id)
 
     with patch("apps.cli.commands.change.require_job_plan", return_value=job), \
+         patch("apps.cli.commands.change.resolve_job_id", side_effect=lambda raw: raw), \
          patch("apps.cli.commands.change.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=[]):
         _cmd_change_proof(job_id, json_output=True)
@@ -131,6 +134,7 @@ def test_handler_json_incomplete_when_test_order_unknown(capsys):
     job_id = str(job.job_id)
 
     with patch("apps.cli.commands.change.require_job_plan", return_value=job), \
+         patch("apps.cli.commands.change.resolve_job_id", side_effect=lambda raw: raw), \
          patch("apps.cli.commands.change.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=events):
         _cmd_change_proof(job_id, json_output=True)
@@ -147,6 +151,7 @@ def test_handler_text_incomplete_when_test_order_unknown(capsys):
     job_id = str(job.job_id)
 
     with patch("apps.cli.commands.change.require_job_plan", return_value=job), \
+         patch("apps.cli.commands.change.resolve_job_id", side_effect=lambda raw: raw), \
          patch("apps.cli.commands.change.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=events):
         _cmd_change_proof(job_id)
@@ -163,6 +168,7 @@ def test_change_show_does_not_display_unrelated_latest_global_test(capsys):
     job_id = str(job.job_id)
 
     with patch("apps.cli.commands.change.require_job_plan", return_value=job), \
+         patch("apps.cli.commands.change.resolve_job_id", side_effect=lambda raw: raw), \
          patch("apps.cli.commands.change.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=events):
         _cmd_change_show(job_id, iid)
@@ -179,12 +185,14 @@ def test_file_why_proof_status_agrees_with_change_proof_path(capsys):
     job_id = str(job.job_id)
 
     with patch("apps.cli.commands.change.require_job_plan", return_value=job), \
+         patch("apps.cli.commands.change.resolve_job_id", side_effect=lambda raw: raw), \
          patch("apps.cli.commands.change.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=events):
         _cmd_change_proof(job_id, path="src/auth.py", json_output=True)
     proof_data = json.loads(capsys.readouterr().out)
 
     with patch("apps.cli.commands.file.require_job_plan", return_value=job), \
+         patch("apps.cli.commands.file.lookup_job_id", side_effect=lambda raw: raw), \
          patch("apps.cli.commands.file.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=events):
         _cmd_file_why(job_id, "src/auth.py", json_output=True)
@@ -199,6 +207,7 @@ def test_handler_json_structured_next_action(capsys):
     job_id = str(job.job_id)
 
     with patch("apps.cli.commands.change.require_job_plan", return_value=job), \
+         patch("apps.cli.commands.change.resolve_job_id", side_effect=lambda raw: raw), \
          patch("apps.cli.commands.change.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=[]):
         _cmd_change_proof(job_id, json_output=True)
@@ -218,6 +227,7 @@ def test_handler_path_filter(capsys):
     job_id = str(job.job_id)
 
     with patch("apps.cli.commands.change.require_job_plan", return_value=job), \
+         patch("apps.cli.commands.change.resolve_job_id", side_effect=lambda raw: raw), \
          patch("apps.cli.commands.change.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=[]):
         _cmd_change_proof(job_id, path="src/auth.py", json_output=True)
@@ -265,6 +275,7 @@ def test_handler_no_traceback(capsys):
     job_id = str(job.job_id)
 
     with patch("apps.cli.commands.change.require_job_plan", return_value=job), \
+         patch("apps.cli.commands.change.resolve_job_id", side_effect=lambda raw: raw), \
          patch("apps.cli.commands.change.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=[]):
         _cmd_change_proof(job_id)
@@ -280,6 +291,7 @@ def test_handler_output_bounded(capsys):
     job_id = str(job.job_id)
 
     with patch("apps.cli.commands.change.require_job_plan", return_value=job), \
+         patch("apps.cli.commands.change.resolve_job_id", side_effect=lambda raw: raw), \
          patch("apps.cli.commands.change.resolve_data_root", return_value="/tmp"), \
          patch("packages.orchestration.timeline.load_run_events", return_value=[]):
         _cmd_change_proof(job_id)
```
