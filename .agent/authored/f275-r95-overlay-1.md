# F275 round 95 — the flip's sixth overlay, part 1 of 4

What the sixth overlay changes. Production code under `packages/` and `apps/` that read `.id`
or `.name` off a job it loaded, under the local names `job`, `j` or `plan`, reads the unified
record's `job_id` and `job_title` (79 reads; the classic store's own module is untouched). The
job doubles tests hand that code spell the same: the `_FakeJob`, `_Job` and `_LoopJob` classes
carry `job_id` and `job_title`, the `SimpleNamespace` stubs of the `review list` tests pass
`job_id=`, and the tests read those names back. A handler test that doubles the job loader as
the first context manager of its `with` statement now also doubles, as the second, the
resolver the handler's module binds (`resolve_job_id` or `lookup_job_id`) with an identity, so
the handler still receives the id the test built (27 `with` statements).

This part holds 14 whole file diffs, `apps/cli/commands/decision.py` through `packages/orchestration/orchestrator_loop.py`.

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
diff --git a/apps/cli/commands/decision.py b/apps/cli/commands/decision.py
index 50dc533b..08450cce 100644
--- a/apps/cli/commands/decision.py
+++ b/apps/cli/commands/decision.py
@@ -181,9 +181,9 @@ def _create_mission_for_job(job: Any) -> None:
               "  Register one with: remedy init", file=sys.stderr)
         sys.exit(1)
 
-    existing = mission_for_job(str(job.id))
+    existing = mission_for_job(str(job.job_id))
     if existing is not None:
-        print(f"Error: job {str(job.id)[:8]} already belongs to mission "
+        print(f"Error: job {str(job.job_id)[:8]} already belongs to mission "
               f"{existing.id[:12]} — one job, one mission.", file=sys.stderr)
         sys.exit(1)
 
@@ -191,11 +191,11 @@ def _create_mission_for_job(job: Any) -> None:
     goal = ""
     if isinstance(intake, dict):
         goal = str(intake.get("goal", "") or "")
-    goal = goal or str(getattr(job, "mission", "") or "") or str(job.name)
+    goal = goal or str(getattr(job, "mission", "") or "") or str(job.job_title)
 
     try:
         mission = create_mission(project_id, goal)
-        link_job_to_mission(project_id, mission.id, str(job.id),
+        link_job_to_mission(project_id, mission.id, str(job.job_id),
                             MISSION_ROLE_INITIAL)
     except MissionError as exc:
         print(f"Error: could not start the mission: {exc}", file=sys.stderr)
diff --git a/apps/cli/commands/do_cmd.py b/apps/cli/commands/do_cmd.py
index d357800b..eef25e87 100644
--- a/apps/cli/commands/do_cmd.py
+++ b/apps/cli/commands/do_cmd.py
@@ -2993,7 +2993,7 @@ def _cmd_do_replan(
         )
         sys.exit(1)
 
-    ev_dir = job_evidence_export_dir(str(job.id))
+    ev_dir = job_evidence_export_dir(str(job.job_id))
     try:
         new_fp_dict, version = replan(
             fp, fp_result.plan, ev_dir,
@@ -3014,7 +3014,7 @@ def _cmd_do_replan(
     if replan_traces:
         from packages.orchestration.prompt_trace import append_trace_jsonl
         from packages.orchestration.run_log import RunLogWriter
-        log = RunLogWriter(job_id=job.id)
+        log = RunLogWriter(job_id=job.job_id)
         try:
             append_trace_jsonl(replan_traces, log.path.parent / "prompt_trace.jsonl")
         except OSError:
@@ -3022,12 +3022,12 @@ def _cmd_do_replan(
 
     if json_output:
         print(json.dumps({
-            "job_id": str(job.id),
+            "job_id": str(job.job_id),
             "version": version,
             "approval": new_fp_dict.get("_approval", "pending"),
         }, indent=2))
     else:
-        print(f"Replanned job {str(job.id)[:8]} → version {version} (awaiting approval)")
+        print(f"Replanned job {str(job.job_id)[:8]} → version {version} (awaiting approval)")
 
 
 COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
diff --git a/apps/cli/commands/failure_stats_cmd.py b/apps/cli/commands/failure_stats_cmd.py
index 109cdccf..db957d09 100644
--- a/apps/cli/commands/failure_stats_cmd.py
+++ b/apps/cli/commands/failure_stats_cmd.py
@@ -50,7 +50,7 @@ def _cmd_stats_failures(*, job: str = "", since: str = "",
         scope = resolve_scope(project_flag=project, all_projects=all_projects)
         if not scope.all_projects:
             jobs, _degraded, _skipped = scoped_jobs(scope)
-            scoped_ids = {str(j.id) for j in jobs}
+            scoped_ids = {str(j.job_id) for j in jobs}
 
     try:
         result = collect_failures(job=job or "", since=since, job_ids=scoped_ids)
diff --git a/apps/cli/commands/job.py b/apps/cli/commands/job.py
index 3e2b49ea..fc024395 100644
--- a/apps/cli/commands/job.py
+++ b/apps/cli/commands/job.py
@@ -144,7 +144,7 @@ def _cmd_list_jobs(
             sort=sort, desc=desc, since=since, until=until, limit=limit,
             sort_fields={
                 "created_at": lambda j: j.created_at,
-                "name": lambda j: j.name,
+                "name": lambda j: j.job_title,
                 "state": lambda j: j.state.value,
             },
             default_sort_field="created_at",
@@ -169,7 +169,7 @@ def _cmd_list_jobs(
     known = _known_project_ids()
     for job in jobs:
         label = _scope_label(job, scope, known)
-        print(f"{job.id}  {job.state.value:<12}  {job.created_at}  {job.name}{label}")
+        print(f"{job.job_id}  {job.state.value:<12}  {job.created_at}  {job.job_title}{label}")
     if skipped:
         print(f"  ({len(skipped)} unreadable job file(s) skipped)", file=sys.stderr)
 
@@ -386,7 +386,7 @@ def _cmd_attach_repo(job_id_str: str, repo_path_str: str) -> None:
     resolved = repo_path.resolve()
     job.metadata["target_repo"] = str(resolved)
     save_job_plan(job)
-    print(f"Job {job.id} | repo={resolved}")
+    print(f"Job {job.job_id} | repo={resolved}")
 
 
 def _cmd_set_permission(job_id_str: str, action: str, capability_str: str) -> None:
@@ -788,7 +788,7 @@ def _cmd_job_run_cycles(
 
     if not _perm_allowed(job, Capability.workspace_write):
         print(
-            f"Error: permission denied — workspace_write is not granted for job {job.id}",
+            f"Error: permission denied — workspace_write is not granted for job {job.job_id}",
             file=sys.stderr,
         )
         sys.exit(1)
@@ -1126,7 +1126,7 @@ def _cmd_job_summary(job_id_str: str, *, json_output: bool = False) -> None:
     from packages.orchestration.timeline import load_run_events
 
     data_dir = resolve_data_root()
-    events = load_run_events(data_dir, job.id)
+    events = load_run_events(data_dir, job.job_id)
 
     state = job.state.value if hasattr(job.state, "value") else str(job.state)
     task_count = len(job.tasks)
@@ -1136,8 +1136,8 @@ def _cmd_job_summary(job_id_str: str, *, json_output: bool = False) -> None:
     has_real_events = event_count > 0
 
     summary = {
-        "job_id": str(job.id),
-        "name": job.name,
+        "job_id": str(job.job_id),
+        "name": job.job_title,
         "state": state,
         "task_count": task_count,
         "done_count": done_count,
@@ -1152,8 +1152,8 @@ def _cmd_job_summary(job_id_str: str, *, json_output: bool = False) -> None:
         print(_json.dumps(summary, indent=2))
     else:
         mode_label = "LIVE" if has_real_events else "DEMO (no events yet)"
-        print(f"Job {job.id}")
-        print(f"  Name:    {job.name}")
+        print(f"Job {job.job_id}")
+        print(f"  Name:    {job.job_title}")
         print(f"  State:   {state}")
         print(f"  Mode:    {mode_label}")
         print(f"  Tasks:   {done_count}/{task_count} done, {pending_count} pending")
@@ -2177,7 +2177,7 @@ def _cmd_job_budget(
             print(f"Error: job {job_id!r} not found.", file=sys.stderr)
             sys.exit(1)
         _found_as = "core_job"
-        _job_display_id = str(job.id)
+        _job_display_id = str(job.job_id)
         _budgets = job.budgets
 
         if _budgets is None:
diff --git a/apps/cli/commands/memory.py b/apps/cli/commands/memory.py
index 7bfb67fb..5cc607c8 100644
--- a/apps/cli/commands/memory.py
+++ b/apps/cli/commands/memory.py
@@ -158,7 +158,7 @@ def _cmd_memory_learn(
     from packages.orchestration.timeline import load_run_events
 
     data_dir = resolve_data_root()
-    events = load_run_events(data_dir, job.id)
+    events = load_run_events(data_dir, job.job_id)
     result = learn_from_job(job, events, approved=approved)
 
     if json_output:
@@ -168,7 +168,7 @@ def _cmd_memory_learn(
         for e in result.entries:
             print(f"  {e['key']} = {e['value']} ({e['status']})")
 
-    log = RunLogWriter(job_id=job.id)
+    log = RunLogWriter(job_id=job.job_id)
     log.log(
         "memory_learned",
         learned_count=result.learned_count,
@@ -352,7 +352,7 @@ def _cmd_memory_approve_candidate(
         if json_output:
             print(_json.dumps({
                 "version": 1,
-                "job_id": str(job.id),
+                "job_id": str(job.job_id),
                 "candidate_id": candidate_id,
                 "approved": False,
                 "memory_created": False,
@@ -391,7 +391,7 @@ def _cmd_memory_reject_candidate(
         if json_output:
             print(_json.dumps({
                 "version": 1,
-                "job_id": str(job.id),
+                "job_id": str(job.job_id),
                 "candidate_id": candidate_id,
                 "rejected": False,
                 "memory_created": False,
diff --git a/apps/cli/commands/mission_cmd.py b/apps/cli/commands/mission_cmd.py
index 7af4c16e..f4f6881f 100644
--- a/apps/cli/commands/mission_cmd.py
+++ b/apps/cli/commands/mission_cmd.py
@@ -350,7 +350,7 @@ def _cmd_mission_continue(mission_id: str, next_step: str, *,
         print(_json.dumps({
             "version": 1,
             "mission_id": mission.id,
-            "job_id": str(job.id),
+            "job_id": str(job.job_id),
             "role": job.metadata.get("mission_role", ""),
             "verify_first_task": (
                 {"description": verify.description,
@@ -360,7 +360,7 @@ def _cmd_mission_continue(mission_id: str, next_step: str, *,
         }, sort_keys=True))
         return
 
-    print(str(job.id))
+    print(str(job.job_id))
     print(f"  Mission: {mission.id[:12]}  ({job.metadata.get('mission_role', '')})")
     if verify is not None:
         print(f"  Task 1 (injected): {verify.description}")
diff --git a/apps/cli/commands/project.py b/apps/cli/commands/project.py
index 10702dc6..4a1b0895 100644
--- a/apps/cli/commands/project.py
+++ b/apps/cli/commands/project.py
@@ -239,14 +239,14 @@ def _cmd_project_brain(project_id_str: str, *, json_output: bool = False) -> Non
         sys.exit(1)
 
     all_jobs = list_job_plans()
-    linked_jobs = [j for j in all_jobs if str(j.id) in project.job_ids]
+    linked_jobs = [j for j in all_jobs if str(j.job_id) in project.job_ids]
 
     data_dir = resolve_data_root()
     all_events: dict[str, list[dict]] = {}
     consts: dict[str, object | None] = {}
     for job in linked_jobs:
-        jid = str(job.id)
-        all_events[jid] = load_run_events(data_dir, job.id)
+        jid = str(job.job_id)
+        all_events[jid] = load_run_events(data_dir, job.job_id)
         target_repo = job.metadata.get("target_repo")
         if target_repo:
             try:
@@ -295,13 +295,13 @@ def _cmd_project_summary(project_id_str: str, *, json_output: bool = False) -> N
         sys.exit(1)
 
     all_jobs = list_job_plans()
-    linked_jobs = [j for j in all_jobs if str(j.id) in project.job_ids]
+    linked_jobs = [j for j in all_jobs if str(j.job_id) in project.job_ids]
 
     data_dir = resolve_data_root()
     all_events: dict[str, list[dict]] = {}
     for job in linked_jobs:
-        jid = str(job.id)
-        all_events[jid] = load_run_events(data_dir, job.id)
+        jid = str(job.job_id)
+        all_events[jid] = load_run_events(data_dir, job.job_id)
 
     summary = build_project_summary(project, linked_jobs, all_events)
     patterns = detect_patterns(linked_jobs, all_events)
@@ -466,7 +466,7 @@ def _cmd_project_adopt(
 
     job.project_id = str(project.id)
     save_job_plan(job)
-    attach_job(project, str(job.id))
+    attach_job(project, str(job.job_id))
     save_project(project)
     print(f"Adopted {resolved_id[:8]} into project {project.slug or project.id}.")
 
diff --git a/apps/cli/commands/readiness.py b/apps/cli/commands/readiness.py
index 0267c237..ab3494f1 100644
--- a/apps/cli/commands/readiness.py
+++ b/apps/cli/commands/readiness.py
@@ -38,7 +38,7 @@ def _cmd_readiness_job(job_id_str: str, *, json_output: bool = False) -> None:
     from packages.orchestration.timeline import load_run_events
 
     data_dir = resolve_data_root()
-    events = load_run_events(data_dir, job.id)
+    events = load_run_events(data_dir, job.job_id)
     report = assess_job_readiness(job, events, data_dir=data_dir)
 
     if json_output:
@@ -46,7 +46,7 @@ def _cmd_readiness_job(job_id_str: str, *, json_output: bool = False) -> None:
     else:
         print(summarize_readiness(report))
 
-    log = RunLogWriter(job_id=job.id)
+    log = RunLogWriter(job_id=job.job_id)
     log.log(
         "readiness_assessed",
         scope=report.scope,
@@ -88,7 +88,7 @@ def _cmd_readiness_project(project_id_str: str, *, json_output: bool = False) ->
         try:
             j = load_job_plan(lookup_job_id(jid))
             jobs.append(j)
-            all_events[jid] = load_run_events(data_dir, j.id)
+            all_events[jid] = load_run_events(data_dir, j.job_id)
         except Exception:
             continue
 
diff --git a/apps/cli/commands/repo.py b/apps/cli/commands/repo.py
index c91acc32..08a83998 100644
--- a/apps/cli/commands/repo.py
+++ b/apps/cli/commands/repo.py
@@ -82,7 +82,7 @@ def _cmd_repo_status(
         changed = len(status.modified_files) + len(status.untracked_files) + len(status.staged_files)
         raw = f"{status.current_branch}:{status.head_sha}:{status.is_clean}:{changed}"
         status_hash = hashlib.sha256(raw.encode()).hexdigest()[:16]
-        log = RunLogWriter(job_id=job.id)
+        log = RunLogWriter(job_id=job.job_id)
         log.log(
             "git_status_read",
             outcome="clean" if status.is_clean else "dirty",
diff --git a/apps/cli/commands/review_cmd.py b/apps/cli/commands/review_cmd.py
index ef907889..895114f8 100644
--- a/apps/cli/commands/review_cmd.py
+++ b/apps/cli/commands/review_cmd.py
@@ -90,7 +90,7 @@ def _cmd_review_list(args: Any) -> None:
     if getattr(args, "json", False):
         print(json.dumps({
             "version": 1,
-            "job_id": str(job.id),
+            "job_id": str(job.job_id),
             "recommendations": recs,
         }, indent=2))
     else:
@@ -128,7 +128,7 @@ def _cmd_review_accept(args: Any) -> None:
         if getattr(args, "json", False):
             print(json.dumps({
                 "version": 1,
-                "job_id": str(job.id),
+                "job_id": str(job.job_id),
                 "recommendation_id": args.recommendation_id,
                 "accepted": False,
                 "proposed_task_created": False,
@@ -162,7 +162,7 @@ def _cmd_review_reject(args: Any) -> None:
         if getattr(args, "json", False):
             print(json.dumps({
                 "version": 1,
-                "job_id": str(job.id),
+                "job_id": str(job.job_id),
                 "recommendation_id": args.recommendation_id,
                 "rejected": False,
                 "task_appended": False,
diff --git a/apps/cli/commands/status_cmd.py b/apps/cli/commands/status_cmd.py
index 519e9c63..d3131244 100644
--- a/apps/cli/commands/status_cmd.py
+++ b/apps/cli/commands/status_cmd.py
@@ -56,9 +56,9 @@ def _cmd_status(
     for j in jobs:
         state = j.state.value
         by_state[state].append({
-            "job_id": str(j.id),
-            "short_id": str(j.id)[:8],
-            "name": j.name,
+            "job_id": str(j.job_id),
+            "short_id": str(j.job_id)[:8],
+            "name": j.job_title,
             "state": state,
         })
 
@@ -69,7 +69,7 @@ def _cmd_status(
             from packages.orchestration.decision_queue import list_decisions
             from packages.orchestration.timeline import load_run_events
 
-            events = load_run_events(resolve_data_root(), j.id)
+            events = load_run_events(resolve_data_root(), j.job_id)
             decs = list_decisions(j, events)
             decisions_open += sum(1 for d in decs if d.status == "open")
         except Exception:
@@ -82,7 +82,7 @@ def _cmd_status(
             continue
         try:
             from packages.orchestration.safe_points import stop_requested
-            if stop_requested(str(j.id)) is not None:
+            if stop_requested(str(j.job_id)) is not None:
                 stops_pending += 1
         except Exception:
             pass
diff --git a/packages/orchestration/autorun.py b/packages/orchestration/autorun.py
index b9fdc854..9876e2f9 100644
--- a/packages/orchestration/autorun.py
+++ b/packages/orchestration/autorun.py
@@ -682,7 +682,7 @@ def _run_ollama_builder(
     except ImportError:
         result["stage"] = "provider_error"
         result["stop_reason"] = "provider_unavailable"
-        _emit(data_dir, job.id, "autorun_provider_error", {
+        _emit(data_dir, job.job_id, "autorun_provider_error", {
             "provider": "ollama",
             "error_kind": "import_error",
             "stop_reason": "provider_unavailable",
diff --git a/packages/orchestration/event_replay.py b/packages/orchestration/event_replay.py
index 4eff8697..48d77e26 100644
--- a/packages/orchestration/event_replay.py
+++ b/packages/orchestration/event_replay.py
@@ -425,7 +425,7 @@ def execute_resume_from_apply(
     from packages.orchestration.timeline import append_run_event
 
     result = ResumeResult(checkpoint_id=checkpoint_id, checkpoint_kind="source_apply_proven", resume_mode="from_apply")
-    jid = job.id
+    jid = job.job_id
 
     # Validate
     blocker = _validate_from_apply(job)
diff --git a/packages/orchestration/orchestrator_loop.py b/packages/orchestration/orchestrator_loop.py
index 5c64858f..37d8bf69 100644
--- a/packages/orchestration/orchestrator_loop.py
+++ b/packages/orchestration/orchestrator_loop.py
@@ -1490,14 +1490,14 @@ def execute_dispatched_job(job: Any, *,
     limits = replace(limits, budgets=getattr(job, "budgets", None))
     result = run_cycles(job, limits, OllamaBuilder().build,
                         task_step=default_task_step,
-                        log=RunLogWriter(job_id=job.id),
+                        log=RunLogWriter(job_id=job.job_id),
                         unattended=True)
     # Carried out rather than logged and forgotten: a run that went over the
     # rollout cap has to say so in its own evidence (R-0187).
     # R-0188: the gate runs at PRODUCTION job completion, here, once. It
     # persists its own verdict where load_gate_result reads it, so there is no
     # second store and the fixture-demo fulfillment spine stays untouched.
-    released, blocker = run_gate_for_job(str(job.id), worktree_root)
+    released, blocker = run_gate_for_job(str(job.job_id), worktree_root)
     return JobExecution(terminal_status=result.terminal_status,
                         job_status=result.job_status,
                         stop_reason=result.stop_reason,
@@ -1649,7 +1649,7 @@ def _auto_approve_if_gated(job: Any) -> bool:
     if not flight_plan_approval_open(job):
         return False
     job.flight_plan = auto_approve_flight_plan(
-        dict(job.flight_plan or {}), job_evidence_export_dir(str(job.id)))
+        dict(job.flight_plan or {}), job_evidence_export_dir(str(job.job_id)))
     save_job_plan(job)
     return True
 
```
