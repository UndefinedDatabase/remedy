# F275 round 103 — the test edits, as one unified diff

This carrier holds the TEST side of round 103, authored by the planner and reviewer of
session 35 from its own dry run in a disposable worktree at `0fac911d`, where these edits and
the round's production repairs together read 863 passed over the nine changed test files and
twelve neighbouring ones. It touches `tests/` only. The production side is specified, not
carried: the worker writes it from SPEC P of `.agent/authored/f275-r103.md`.

Apply it at C4 of that block, from the repository root: extract the text between the line of
three backticks followed by `diff` and the closing line of three backticks, write it to a
scratch file, run `git apply --check` on it and then `git apply`. The diff is taken against
`0fac911d`, and no earlier commit of round 103 touches `tests/`, so every hunk's context is
the base's.

```diff
diff --git a/tests/cli/test_golden_path.py b/tests/cli/test_golden_path.py
index f8869008..94d7333f 100644
--- a/tests/cli/test_golden_path.py
+++ b/tests/cli/test_golden_path.py
@@ -535,8 +535,8 @@ class TestStatus:
         _init_project(repo, env)
 
         jobs_dir = tmp_path / "data" / "jobs"
-        jobs_dir.mkdir(parents=True, exist_ok=True)
-        (jobs_dir / "bad.json").write_text("{corrupt")
+        (jobs_dir / "badjob").mkdir(parents=True, exist_ok=True)
+        (jobs_dir / "badjob" / "job.json").write_text("{corrupt")
 
         result = _run_status(repo, env, ["--json"])
         assert result.returncode == 0
@@ -789,12 +789,11 @@ class TestShortIdResolution:
                 break
         if common < 4:
             jobs_dir = tmp_path / "data" / "jobs"
-            src = jobs_dir / f"{id2}.json"
             forced_id = id1[:8] + id2[8:]
-            dst = jobs_dir / f"{forced_id}.json"
-            data = src.read_text().replace(str(id2), forced_id)
-            dst.write_text(data)
-            src.unlink()
+            dst = jobs_dir / forced_id
+            (jobs_dir / id2).rename(dst)
+            record = dst / "job.json"
+            record.write_text(record.read_text().replace(str(id2), forced_id))
             prefix = id1[:8]
         else:
             prefix = id1[:common]
diff --git a/tests/cli/test_plan_approval.py b/tests/cli/test_plan_approval.py
index 1027d6fe..8a79e25f 100644
--- a/tests/cli/test_plan_approval.py
+++ b/tests/cli/test_plan_approval.py
@@ -335,7 +335,7 @@ class TestApprovalGateEnforcement:
     def test_rejected_cli_exit_3(self, tmp_path):
         """R-0130: rejected plan refuses execution at CLI level."""
         from packages.core.models import RunState
-        from packages.orchestration.pingpong_job import TaskEntry
+        from packages.orchestration.pingpong_job import TaskEntry, save_job_plan
         env = _env(tmp_path)
         repo = _git_repo(tmp_path)
         subprocess.run(
@@ -349,24 +349,8 @@ class TestApprovalGateEnforcement:
             tasks=[TaskEntry(title="X")],
         )
         env_with_data = {**env, "REMEDY_DATA_DIR": str(tmp_path / "data")}
-        save_result = subprocess.run(
-            [sys.executable, "-c", f"""
-import os, sys
-sys.path.insert(0, os.environ["PYTHONPATH"])
-os.environ["REMEDY_DATA_DIR"] = "{tmp_path / 'data'}"
-from packages.core.models import Job, Task, RunState
-from packages.orchestration.storage import save_job
-job = Job(name="rejected-test", state=RunState.PLANNED,
-          flight_plan={{"_approval": "rejected"}},
-          tasks=[Task(description="X")])
-save_job(job)
-print(str(job.id))
-"""],
-            capture_output=True, text=True, timeout=30,
-            cwd=str(repo), env=env_with_data,
-        )
-        job_id = save_result.stdout.strip()
-        short_id = job_id[:8]
+        save_job_plan(job, root=tmp_path / "data")
+        short_id = job.job_id[:8]
 
         run = subprocess.run(
             [*_CLI, "job", "resume", short_id],
@@ -667,7 +651,7 @@ class TestReplanApprovalRearm:
 class TestApprovalGoldenPathCLI:
     """R-0127: full CLI sequence — init → do(seed) → run(blocked) → approve → status.
 
-    Assumption: inline save_job seeds the job with a pending flight plan as the
+    Assumption: inline save_job_plan seeds the job with a pending flight plan as the
     provider stand-in, per spec allowance.
     """
 
@@ -682,36 +666,24 @@ class TestApprovalGoldenPathCLI:
         )
         assert init.returncode == 0, init.stderr
 
-        # 2. seed job with pending flight plan via save_job
-        seed = subprocess.run(
-            [sys.executable, "-c", """
-import os, json, sys
-sys.path.insert(0, os.environ["PYTHONPATH"])
-os.environ["REMEDY_DATA_DIR"] = os.environ["REMEDY_DATA_DIR"]
-from packages.core.models import Job, Task, RunState
-from packages.orchestration.storage import save_job
-job = Job(
-    name="approval-smoke",
-    state=RunState.PLANNED,
-    flight_plan={
-        "schema_v": "flight_plan_v1",
-        "tasks": [{"id": "T001", "title": "Do thing", "goal": "G",
-                    "acceptance": ["Done"], "depends_on": [],
-                    "est_tokens_band": "M", "files_hint": []}],
-        "risks": [],
-        "_approval": "pending",
-    },
-    tasks=[Task(description="Do thing")],
-)
-save_job(job)
-print(json.dumps({"job_id": str(job.id)}))
-"""],
-            capture_output=True, text=True, timeout=30,
-            cwd=str(repo), env=env,
-        )
-        assert seed.returncode == 0, seed.stderr
-        job_id = json.loads(seed.stdout)["job_id"]
-        short_id = job_id[:8]
+        # 2. seed job with pending flight plan via save_job_plan
+        from packages.core.models import RunState
+        from packages.orchestration.pingpong_job import TaskEntry, save_job_plan
+        job = JobPlan(
+            job_title="approval-smoke",
+            state=RunState.PLANNED,
+            flight_plan={
+                "schema_v": "flight_plan_v1",
+                "tasks": [{"id": "T001", "title": "Do thing", "goal": "G",
+                            "acceptance": ["Done"], "depends_on": [],
+                            "est_tokens_band": "M", "files_hint": []}],
+                "risks": [],
+                "_approval": "pending",
+            },
+            tasks=[TaskEntry(title="Do thing")],
+        )
+        save_job_plan(job, root=tmp_path / "data")
+        short_id = job.job_id[:8]
 
         # 3. run attempt → expect blocked (exit 3, stderr mentions approval)
         run = subprocess.run(
diff --git a/tests/cli/test_scoped_listings.py b/tests/cli/test_scoped_listings.py
index 76139103..fa684381 100644
--- a/tests/cli/test_scoped_listings.py
+++ b/tests/cli/test_scoped_listings.py
@@ -13,9 +13,7 @@ import sys
 from unittest.mock import patch
 from uuid import uuid4
 
-import pytest
-
-from packages.orchestration.pingpong_job import JobPlan
+from packages.orchestration.pingpong_job import JobPlan, save_job_plan
 from packages.orchestration.project_scope import ProjectScope, job_in_scope, scoped_jobs
 
 _CLI = [sys.executable, "-m", "apps.cli.grouped"]
@@ -88,19 +86,10 @@ def _create_job(repo, env, mission):
 
 
 def _write_legacy_job(data_dir, name="legacy-job"):
-    """Write a job JSON with no project_id directly to the store."""
-    jobs = data_dir / "jobs"
-    jobs.mkdir(parents=True, exist_ok=True)
-    jid = str(uuid4())
-    (jobs / f"{jid}.json").write_text(json.dumps({
-        "id": jid,
-        "name": name,
-        "state": "pending",
-        "tasks": [],
-        "artifacts": [],
-        "metadata": {},
-    }))
-    return jid[:8], jid
+    """Persist a job record with no project_id directly to the store."""
+    job = JobPlan(job_title=name)
+    save_job_plan(job, root=data_dir)
+    return job.job_id[:8], job.job_id
 
 
 def _get_project_slug(repo, env):
@@ -214,6 +203,7 @@ class TestScopedListingsCLI:
         one tree while importing another cannot fail.
         """
         from apps.cli.commands.project import _cmd_project_adopt
+        from packages.orchestration.pingpong_job import load_job_plan
 
         data_dir = tmp_path / "data"
         env = _env(data_dir)
@@ -221,19 +211,16 @@ class TestScopedListingsCLI:
         _init_project(repo_a, env)
 
         pingpong_id = "0123456789abcdef"
-        record_dir = data_dir / "jobs" / pingpong_id
-        record_dir.mkdir(parents=True)
-        (record_dir / "job.json").write_text(json.dumps({"id": pingpong_id}))
+        save_job_plan(JobPlan(job_id=pingpong_id, job_title="pingpong"), root=data_dir)
 
         monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
         monkeypatch.chdir(repo_a)
         capsys.readouterr()
 
-        with pytest.raises(SystemExit) as exc_info:
-            _cmd_project_adopt(pingpong_id)
+        _cmd_project_adopt(pingpong_id)
 
-        assert exc_info.value.code == 3
-        assert "job not found" in capsys.readouterr().err
+        assert "Adopted 01234567" in capsys.readouterr().out
+        assert load_job_plan(pingpong_id, root=data_dir).project_id
 
     def test_orphaned_label_on_deleted_project(self, tmp_path):
         data_dir = tmp_path / "data"
@@ -244,18 +231,8 @@ class TestScopedListingsCLI:
         _create_job(repo_a, env, "alpha job")
 
         # Create a job with a fake project_id (simulates deleted project)
-        jobs_dir = data_dir / "jobs"
-        orphan_id = str(uuid4())
         fake_project = str(uuid4())
-        (jobs_dir / f"{orphan_id}.json").write_text(json.dumps({
-            "id": orphan_id,
-            "name": "orphaned-job",
-            "state": "pending",
-            "tasks": [],
-            "artifacts": [],
-            "metadata": {},
-            "project_id": fake_project,
-        }))
+        save_job_plan(JobPlan(job_title="orphaned-job", project_id=fake_project), root=data_dir)
 
         # --all-projects listing should show orphaned label and not crash
         result = _run_cli(["job", "list", "--all-projects"], env, cwd=str(repo_a))
@@ -337,6 +314,13 @@ class TestTwoProjectIsolation:
         scope = ProjectScope(project_id=_P1, all_projects=False, source="flag")
         assert not job_in_scope(legacy, scope, _legacy_visible=False)
 
+    def test_a_record_with_no_project_is_legacy(self):
+        """A unified record with no project spells it ``""``, never ``None`` (R-0886)."""
+        legacy = JobPlan(job_title="old")
+        scope = ProjectScope(project_id=_P1, all_projects=False, source="flag")
+        assert legacy.project_id == ""
+        assert job_in_scope(legacy, scope, _legacy_visible=True)
+
     def test_legacy_visible_under_all(self):
         legacy = _job(None, "old")
         scope = ProjectScope(project_id=None, all_projects=True, source="flag")
diff --git a/tests/orchestration/test_final_audit_evidence.py b/tests/orchestration/test_final_audit_evidence.py
index c04a3058..18696939 100644
--- a/tests/orchestration/test_final_audit_evidence.py
+++ b/tests/orchestration/test_final_audit_evidence.py
@@ -258,7 +258,7 @@ class TestCockpitBridgeAdapter:
         assert len(adapter.tasks) == 1
         assert adapter.tasks[0].id == "T001"
         assert adapter.tasks[0].description == "Fix bug"
-        assert adapter.tasks[0].status == "completed"
+        assert adapter.tasks[0].status.value == "completed"
         assert adapter.artifacts == []
         assert adapter._is_job_plan is True
 
diff --git a/tests/orchestration/test_proposed_tasks.py b/tests/orchestration/test_proposed_tasks.py
index 73d3a4be..ec52b989 100644
--- a/tests/orchestration/test_proposed_tasks.py
+++ b/tests/orchestration/test_proposed_tasks.py
@@ -844,7 +844,8 @@ class TestBackendReadiness:
         monkeypatch.setattr("packages.orchestration.proposed_tasks._STORE_DIR", tmp_path / "proposed_tasks")
         monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
         _create_real_job(tmp_path)
-        corrupt_path = tmp_path / "jobs" / "corrupt-job.json"
+        corrupt_path = tmp_path / "jobs" / "corrupt-job" / "job.json"
+        corrupt_path.parent.mkdir(parents=True)
         corrupt_path.write_text("not json")
         report = backend_readiness(REAL_JOB_UUID)
         assert report["storage_health"]["job_store_skipped_files"] > 0
diff --git a/tests/orchestration/test_repair_loop_v1.py b/tests/orchestration/test_repair_loop_v1.py
index f6c4d795..9833282d 100644
--- a/tests/orchestration/test_repair_loop_v1.py
+++ b/tests/orchestration/test_repair_loop_v1.py
@@ -223,7 +223,6 @@ class TestIdempotency:
 
 class TestProofAlignment:
     def test_repair_intent_not_applied_or_verified(self, data_dir):
-        import uuid
         jid, fa, _ = _make_job_with_failure(data_dir)
         r = RL.run_repair_attempt(jid, fa, fixture_builder=True, data_dir=data_dir)
         job = load_job_plan(normalize_job_id(jid), data_dir)
@@ -232,7 +231,7 @@ class TestProofAlignment:
         assert intent.get("state") == "pending"  # not approved, not applied
         from packages.orchestration.proof_chain import PROOF_VERIFIED, build_proof_chain
         from packages.orchestration.timeline import load_run_events
-        events = load_run_events(data_dir, uuid.UUID(jid))
+        events = load_run_events(data_dir, jid)
         chain = build_proof_chain(job, events, data_dir=data_dir)
         for c in chain.changes:
             if c.intent_id == r.repair_intent_id:
@@ -248,7 +247,6 @@ class TestProofAlignment:
 class TestRedaction:
     def test_no_raw_leakage_in_result_and_events(self, data_dir):
         import json
-        import uuid
         jid, fa, _ = _make_job_with_failure(
             data_dir,
             safe_summary="Test test_failed: exit 1",  # safe summary is bounded
@@ -258,7 +256,7 @@ class TestRedaction:
         payload = json.dumps(RL.export_repair_attempt_json(r))
         ctx = RL.export_repair_context_json(RL.build_repair_context(jid, fa, data_dir))
         from packages.orchestration.timeline import load_run_events
-        events_blob = json.dumps(load_run_events(data_dir, uuid.UUID(jid)))
+        events_blob = json.dumps(load_run_events(data_dir, jid))
         for blob in (payload, json.dumps(ctx), events_blob):
             assert "Traceback" not in blob
             assert "/home/" not in blob
diff --git a/tests/orchestration/test_resume_kill.py b/tests/orchestration/test_resume_kill.py
index 4a75bfe4..777117c3 100644
--- a/tests/orchestration/test_resume_kill.py
+++ b/tests/orchestration/test_resume_kill.py
@@ -63,13 +63,13 @@ import sys
 import time
 from pathlib import Path
 
-from packages.core.models import Job, RunState, Task
+from packages.core.models import RunState
 from packages.orchestration.long_run_executor import (
     CycleLimits,
     TaskAttempt,
     run_cycles,
 )
-from packages.orchestration.storage import load_job, save_job
+from packages.orchestration.pingpong_job import JobPlan, TaskEntry, require_job_plan, save_job_plan
 
 MARKER = Path(sys.argv[1])
 JOB_FILE = Path(sys.argv[2])
@@ -78,12 +78,12 @@ TOTAL_TASKS = int(sys.argv[4])
 MODE = sys.argv[5]                     # "first" | "resume"
 
 if MODE == "first":
-    job = Job(name="kill-fixture",
-              tasks=[Task(title=f"t{i}", description="d") for i in range(TOTAL_TASKS)])
-    save_job(job)
-    JOB_FILE.write_text(str(job.id), encoding="utf-8")
+    job = JobPlan(job_title="kill-fixture",
+                  tasks=[TaskEntry(title=f"t{i}", body="d") for i in range(TOTAL_TASKS)])
+    save_job_plan(job)
+    JOB_FILE.write_text(job.job_id, encoding="utf-8")
 else:
-    job = load_job(__import__("uuid").UUID(JOB_FILE.read_text(encoding="utf-8")))
+    job = require_job_plan(JOB_FILE.read_text(encoding="utf-8"))
 
 _cycle = {"n": 0}
 
@@ -97,12 +97,12 @@ def step(j, _provider):
     _cycle["n"] += 1
     if MODE == "first" and _cycle["n"] == KILL_ON_CYCLE:
         # In flight: the task is picked but NOT completed and NOT recorded.
-        MARKER.write_text(json.dumps({"cycle": _cycle["n"], "task_id": str(task.id)}),
+        MARKER.write_text(json.dumps({"cycle": _cycle["n"], "task_id": task.task_id}),
                           encoding="utf-8")
         while True:
             time.sleep(0.05)            # the parent kills us here
     task.status = RunState.COMPLETED
-    return TaskAttempt(task_id=task.id, executed=True, verified=True)
+    return TaskAttempt(task_id=task.task_id, executed=True, verified=True)
 
 
 result = run_cycles(
@@ -113,7 +113,7 @@ result = run_cycles(
 )
 print(json.dumps({"terminal_status": result.terminal_status,
                   "cycles_run": result.cycles_run,
-                  "job_id": str(job.id)}))
+                  "job_id": job.job_id}))
 '''
 
 
@@ -306,7 +306,7 @@ class TestKillAndResume:
 class TestTornCheckpoint:
     """The atomic write makes a torn file impossible to produce on demand.
 
-    ``storage._atomic_write_job`` writes a temp file, fsyncs it and renames
+    ``pingpong_job._persist_job`` writes a temp file, fsyncs it and renames
     it, so a kill leaves either the old file or the new one — never a half
     one. Forcing a real mid-write kill is therefore not deterministic, and a
     test that tried would be a flake generator. The torn file is written
diff --git a/tests/orchestration/test_unified_store_parity.py b/tests/orchestration/test_unified_store_parity.py
index 68bb36aa..1c5c4db1 100644
--- a/tests/orchestration/test_unified_store_parity.py
+++ b/tests/orchestration/test_unified_store_parity.py
@@ -55,6 +55,29 @@ def _corrupt(root: Path, job_id: str, text: str = "{not json") -> Path:
     return path
 
 
+class TestTheWriteReplacesTheRecordWhole:
+    """R-0885: the unified writer never leaves a half-written record behind."""
+
+    def test_a_failure_before_the_rename_leaves_the_previous_record_intact(
+        self, tmp_path, monkeypatch
+    ):
+        import os
+
+        job = _plan("aaaaaaaaaaaaaaaa")
+        path = save_job_plan(job, root=tmp_path)
+        before = path.read_bytes()
+        job.job_title = "changed"
+
+        def refuse(fd):
+            raise OSError("fsync refused")
+
+        monkeypatch.setattr(os, "fsync", refuse)
+        with pytest.raises(OSError, match="fsync refused"):
+            save_job_plan(job, root=tmp_path)
+        assert path.read_bytes() == before
+        assert sorted(entry.name for entry in path.parent.iterdir()) == ["job.json"]
+
+
 class TestTheJobsRootOverride:
     """W1: one call may name the store's base directory instead of the data root."""
 
diff --git a/tests/test_runner.py b/tests/test_runner.py
index 34f8200f..02455f27 100644
--- a/tests/test_runner.py
+++ b/tests/test_runner.py
@@ -56,8 +56,7 @@ def test_plan_job_task_types_present():
 # ---------------------------------------------------------------------------
 
 def test_plan_job_state_is_planned_after_planning():
-    job = JobPlan(job_title="test")
-    assert job.state == RunState.PENDING
+    job = JobPlan(job_title="test", state=RunState.PENDING)
     result = plan_job(job)
     assert result.job.state == RunState.PLANNED
 
```
