# F275 round 99 — the flip's tenth overlay, part 1 of 1

What the tenth overlay changes. `_job_snapshot_reference` in `checkpoints.py` reads a job's
snapshot at `job_record_path(job_id)`, the unified record's own path, and returns that path
relative to `resolve_data_root()` beside its unchanged digest, where it read and named the
classic flat file `jobs/<job id>.json`. Thirteen f-strings in the tests that delete, corrupt,
read or check a job's record follow it to `jobs/<job id>/job.json`. The three subprocess job
fixtures of `tests/cli/test_mission_cmd.py` build a `JobPlan` and save it with `save_job_plan`,
reading `job.job_id`, and the readiness double there names its id `job_id`. In
`tests/test_data_paths.py` the classic-store guard ranges over `storage` alone, and its
comments say `checkpoints.py` called `jobs_dir` until the flip moved its snapshot.

This part holds 10 whole file diffs, `packages/orchestration/checkpoints.py` through `tests/test_data_paths.py`.

Base: `844a7f21`. The flipped tree is that commit checked out and then built exactly as G4 of
`.agent/authored/f275-r99.md` orders: the committed generator re-derives the TIP re-keyed set from
the two pinned round 77 JSON files, the guarded transform runs over the checkout with that set, its
owners file and `r61_status.json`, and the result is staged.

The TENTH overlay is formed by 1 part, and this is part 1. The parts apply after
`.agent/authored/f275-r98-overlay-1.md`: `.agent/authored/f275-r90-overlay.md`, then
`.agent/authored/f275-r91-overlay.md`, then `.agent/authored/f275-r92-overlay-1.md` through
`-4.md`, then `.agent/authored/f275-r93-overlay-1.md` and `-2.md`, then
`.agent/authored/f275-r94-overlay-1.md` and `-2.md`, then `.agent/authored/f275-r95-overlay-1.md`
through `-4.md`, then `.agent/authored/f275-r96-overlay-1.md`, then
`.agent/authored/f275-r97-overlay-1.md`, then `.agent/authored/f275-r98-overlay-1.md` are applied
to the staged flipped tree overlay by overlay, each overlay staged in turn, and the tenth
overlay's diff was taken against that state. The parts apply in `<k>` order, part 1 first;
joined in that order their fences are that one diff.

How to apply this part, inside the flipped tree with every earlier overlay applied and staged and
every part before this one applied:

1. Extract the fence below: the lines strictly between the line of three backticks followed by
   `diff` and the closing line of three backticks, each line kept with its newline.
2. Run `git apply --check <extracted file>` and require exit 0.
3. Run `git apply <extracted file>`.

```diff
diff --git a/packages/orchestration/checkpoints.py b/packages/orchestration/checkpoints.py
index 5f06a7f1..38028d15 100644
--- a/packages/orchestration/checkpoints.py
+++ b/packages/orchestration/checkpoints.py
@@ -222,13 +222,14 @@ def _job_snapshot_reference(job_id: str) -> tuple[str, str]:
     could not measure the snapshot says so rather than inventing a digest.
     """
     try:
-        from packages.orchestration.data_paths import jobs_dir
+        from packages.orchestration.data_paths import job_record_path, resolve_data_root
 
-        path = jobs_dir() / f"{job_id}.json"
+        path = job_record_path(job_id)
         data = path.read_bytes()
+        relative = path.relative_to(resolve_data_root()).as_posix()
     except (OSError, ValueError):
         return ("", "")
-    return (f"jobs/{job_id}.json", "sha256:" + hashlib.sha256(data).hexdigest())
+    return (relative, "sha256:" + hashlib.sha256(data).hexdigest())
 
 
 def resolve_worktree_head(job_id: str) -> str:
diff --git a/tests/cli/test_job_report.py b/tests/cli/test_job_report.py
index 97244a3b..93ce428c 100644
--- a/tests/cli/test_job_report.py
+++ b/tests/cli/test_job_report.py
@@ -286,4 +286,4 @@ def _headings(text: str) -> list[str]:
 def _job_file(job: JobPlan) -> Path:
     from packages.orchestration.data_paths import jobs_dir
 
-    return jobs_dir() / f"{job.job_id}.json"
+    return jobs_dir() / job.job_id / "job.json"
diff --git a/tests/cli/test_mission_cmd.py b/tests/cli/test_mission_cmd.py
index 96f7199b..79b78eeb 100644
--- a/tests/cli/test_mission_cmd.py
+++ b/tests/cli/test_mission_cmd.py
@@ -72,13 +72,13 @@ def _link_job(data_root: Path, project_id: str, mission_id: str, *,
     """Persist a job in the given state and link it into the mission's chain."""
     script = (
         "import sys; sys.path.insert(0, '.');"
-        "from packages.core.models import Job, RunState;"
-        "from packages.orchestration.storage import save_job;"
+        "from packages.core.models import RunState;"
+        "from packages.orchestration.pingpong_job import JobPlan, save_job_plan;"
         "from packages.orchestration.mission_state import link_job_to_mission;"
-        f"job = Job(name='fixture', state=RunState({state!r}));"
-        "save_job(job);"
-        f"link_job_to_mission({project_id!r}, {mission_id!r}, str(job.id), {role!r});"
-        "print(job.id)"
+        f"job = JobPlan(job_title='fixture', state=RunState({state!r}));"
+        "save_job_plan(job);"
+        f"link_job_to_mission({project_id!r}, {mission_id!r}, job.job_id, {role!r});"
+        "print(job.job_id)"
     )
     proc = subprocess.run(
         [sys.executable, "-c", script], cwd=str(REPO_ROOT), capture_output=True,
@@ -244,7 +244,7 @@ class TestShow:
         data_root, project_id = project
         mission_id = _start(data_root, project_id, "Keep it working")
         job_id = _link_job(data_root, project_id, mission_id, role="initial")
-        (data_root / "jobs" / f"{job_id}.json").unlink()
+        (data_root / "jobs" / job_id / "job.json").unlink()
 
         proc = _run(["mission", "show", mission_id, "--project", project_id],
                     data_root)
@@ -323,16 +323,16 @@ def _pending_plan_job(repo: Path, data_root: Path, goal: str,
     """Persist a job with a pending flight plan and the given intake hint."""
     script = (
         "import sys; sys.path.insert(0, '.');"
-        "from packages.core.models import Job, RunState;"
-        "from packages.orchestration.storage import save_job;"
+        "from packages.core.models import RunState;"
+        "from packages.orchestration.pingpong_job import JobPlan, save_job_plan;"
         "from packages.orchestration.project_registry import resolve_project;"
         f"project = resolve_project({str(repo)!r});"
-        f"job = Job(name='fixture', mission={goal!r}, project_id=str(project.id),"
+        f"job = JobPlan(job_title='fixture', mission={goal!r}, project_id=str(project.id),"
         f"  intake={{'schema_v': 'ji1', 'goal': {goal!r},"
         f"           'mission_candidate': {mission_candidate!r}}},"
         "   flight_plan={'schema_v': 'flight_plan_v1', '_approval': 'pending'},"
         "   state=RunState.PLANNED);"
-        "save_job(job); print(job.id)"
+        "save_job_plan(job); print(job.job_id)"
     )
     proc = subprocess.run(
         [sys.executable, "-c", script], cwd=str(REPO_ROOT), capture_output=True,
@@ -467,7 +467,7 @@ class TestPlainDoFlowCreatesNoMission:
         out = _run_in(repo, ["do", "Maintain the CI pipeline continuously",
                              "--no-llm", "--json"], data_root).stdout
         job_id = json.loads(out)["job_id"]
-        job = json.loads((data_root / "jobs" / f"{job_id}.json").read_text())
+        job = json.loads((data_root / "jobs" / job_id / "job.json").read_text())
 
         assert job["intake"]["mission_candidate"] is True
         assert _missions_on_disk(data_root) == []
@@ -503,14 +503,14 @@ class TestContinue:
                    *, command: str = "check the importer") -> str:
         script = (
             "import sys; sys.path.insert(0, '.');"
-            "from packages.core.models import Job, RunState;"
-            "from packages.orchestration.storage import save_job;"
+            "from packages.core.models import RunState;"
+            "from packages.orchestration.pingpong_job import JobPlan, save_job_plan;"
             "from packages.orchestration.mission_state import link_job_to_mission;"
-            f"job = Job(name='job one', state=RunState('completed'),"
+            f"job = JobPlan(job_title='job one', state=RunState('completed'),"
             f"  project_id={project_id!r}, metadata={{'verify_command': {command!r}}});"
-            "save_job(job);"
-            f"link_job_to_mission({project_id!r}, {mission_id!r}, str(job.id), 'initial');"
-            "print(job.id)"
+            "save_job_plan(job);"
+            f"link_job_to_mission({project_id!r}, {mission_id!r}, job.job_id, 'initial');"
+            "print(job.job_id)"
         )
         proc = subprocess.run(
             [sys.executable, "-c", script], cwd=str(REPO_ROOT),
@@ -1402,7 +1402,7 @@ class TestMissionReadinessIsWiredToTheCarriedModule:
         from packages.orchestration.ui_server import _build_overnight_section
 
         class _Job:
-            id = "11111111-2222-3333-4444-555555555555"
+            job_id = "11111111-2222-3333-4444-555555555555"
 
         section = _build_overnight_section(_Job(), Path(".data"))
 
diff --git a/tests/orchestration/test_checkpoints.py b/tests/orchestration/test_checkpoints.py
index b65ffbd5..99ec3956 100644
--- a/tests/orchestration/test_checkpoints.py
+++ b/tests/orchestration/test_checkpoints.py
@@ -62,7 +62,7 @@ def make_checkpoint(index: int, *, job_id: str = JOB_ID, head: str = "abc123"
     return Checkpoint(
         cycle_index=index,
         job_id=job_id,
-        job_snapshot_path=f"jobs/{job_id}.json",
+        job_snapshot_path=f"jobs/{job_id}/job.json",
         job_snapshot_sha256="sha256:" + "0" * 64,
         worktree_head=head,
         budget_spent_tokens=100 * index,
@@ -146,7 +146,7 @@ class TestWriting:
         job = JobPlan(job_title="cp-job", tasks=[TaskEntry(title="d")])
         save_job_plan(job)
         checkpoint = build_checkpoint(str(job.job_id), 1, now=T0)
-        assert checkpoint.job_snapshot_path == f"jobs/{job.job_id}.json"
+        assert checkpoint.job_snapshot_path == f"jobs/{job.job_id}/job.json"
         assert checkpoint.job_snapshot_sha256.startswith("sha256:")
         assert checkpoint.created_at == T0.isoformat()
 
@@ -364,7 +364,7 @@ class TestCycleBoundaryWiring:
         job = _job()
         _run_one_cycle(job)
         loaded = load_latest_valid(str(job.job_id))
-        assert loaded.job_snapshot_path == f"jobs/{job.job_id}.json"
+        assert loaded.job_snapshot_path == f"jobs/{job.job_id}/job.json"
         assert loaded.job_snapshot_sha256.startswith("sha256:")
 
     def test_a_failed_checkpoint_write_does_not_break_the_cycle(self, monkeypatch):
diff --git a/tests/orchestration/test_handoff.py b/tests/orchestration/test_handoff.py
index b803fc7a..125bec60 100644
--- a/tests/orchestration/test_handoff.py
+++ b/tests/orchestration/test_handoff.py
@@ -111,7 +111,7 @@ def _seed_job_checkpoint(root, mission, job_id: str, *,
     checkpoint = Checkpoint(
         cycle_index=cycle_index,
         job_id=job_id,
-        job_snapshot_path=f"jobs/{job_id}.json",
+        job_snapshot_path=f"jobs/{job_id}/job.json",
         job_snapshot_sha256="sha256:" + "a" * 64,
         worktree_head="c0ffee" + "0" * 34,
         budget_spent_tokens=1234,
diff --git a/tests/orchestration/test_long_run_executor.py b/tests/orchestration/test_long_run_executor.py
index a0967989..0e9f7255 100644
--- a/tests/orchestration/test_long_run_executor.py
+++ b/tests/orchestration/test_long_run_executor.py
@@ -556,7 +556,7 @@ class TestDefaultTaskStep:
         assert provider.calls == 2
         assert result.terminal_status == TERMINAL_ALL_GREEN
         assert all(t.status == RunState.COMPLETED for t in job.tasks)
-        assert (isolate_data_root / "jobs" / f"{job.job_id}.json").is_file()
+        assert (isolate_data_root / "jobs" / job.job_id / "job.json").is_file()
 
     def test_provider_failure_is_recorded_and_the_task_stays_pending(
         self, isolate_data_root, control_root
diff --git a/tests/orchestration/test_mission_state.py b/tests/orchestration/test_mission_state.py
index 110146ee..2ae6eda9 100644
--- a/tests/orchestration/test_mission_state.py
+++ b/tests/orchestration/test_mission_state.py
@@ -435,7 +435,7 @@ class TestMissionChainRendering:
         mission = create_mission(_PROJECT, "Ship the importer", root=tmp_path)
         linked = link_job_to_mission(_PROJECT, mission.id, str(job.job_id),
                                      MISSION_ROLE_INITIAL, root=tmp_path)
-        (tmp_path / "jobs" / f"{job.job_id}.json").unlink()
+        (tmp_path / "jobs" / job.job_id / "job.json").unlink()
 
         rendered = "\n".join(render_mission_chain(linked))
 
@@ -450,7 +450,7 @@ class TestMissionChainRendering:
         mission = create_mission(_PROJECT, "Ship the importer", root=tmp_path)
         linked = link_job_to_mission(_PROJECT, mission.id, str(job.job_id),
                                      MISSION_ROLE_INITIAL, root=tmp_path)
-        (tmp_path / "jobs" / f"{job.job_id}.json").write_text("{ not json")
+        (tmp_path / "jobs" / job.job_id / "job.json").write_text("{ not json")
 
         rendered = "\n".join(render_mission_chain(linked))
 
@@ -861,7 +861,7 @@ class TestTwoJobFixtureEndToEnd:
     def test_a_gone_previous_job_refuses_rather_than_verifying_blind(self, tmp_path):
         mission, job_one = self._mission_with_a_green_first_job(
             tmp_path, "check the importer")
-        (tmp_path / "jobs" / f"{job_one.job_id}.json").unlink()
+        (tmp_path / "jobs" / job_one.job_id / "job.json").unlink()
 
         with pytest.raises(MissionError) as exc:
             continue_mission(_PROJECT, mission.id, "Add the CSV path",
diff --git a/tests/orchestration/test_resume_cli.py b/tests/orchestration/test_resume_cli.py
index f1342910..b5ad25cc 100644
--- a/tests/orchestration/test_resume_cli.py
+++ b/tests/orchestration/test_resume_cli.py
@@ -65,7 +65,7 @@ def put_checkpoint(job: JobPlan, index: int = 1, *, head: str = "") -> Checkpoin
     checkpoint = Checkpoint(
         cycle_index=index,
         job_id=str(job.job_id),
-        job_snapshot_path=f"jobs/{job.job_id}.json",
+        job_snapshot_path=f"jobs/{job.job_id}/job.json",
         job_snapshot_sha256="sha256:" + "0" * 64,
         worktree_head=head,
         budget_spent_tokens=42,
diff --git a/tests/orchestration/test_resume_kill.py b/tests/orchestration/test_resume_kill.py
index 2c03cacc..4a75bfe4 100644
--- a/tests/orchestration/test_resume_kill.py
+++ b/tests/orchestration/test_resume_kill.py
@@ -217,7 +217,7 @@ class TestKillAndResume:
         assert checkpoint is not None, "no checkpoint survived the kill"
         # Cycles 1..KILL_ON_CYCLE-1 committed; the killed one never did.
         assert checkpoint.cycle_index == KILL_ON_CYCLE - 1
-        assert checkpoint.job_snapshot_path == f"jobs/{job_id}.json"
+        assert checkpoint.job_snapshot_path == f"jobs/{job_id}/job.json"
 
     def test_the_in_flight_task_was_never_recorded_as_executed(
             self, killed_run, data_dir):
diff --git a/tests/test_data_paths.py b/tests/test_data_paths.py
index 73183baa..bd813065 100644
--- a/tests/test_data_paths.py
+++ b/tests/test_data_paths.py
@@ -552,14 +552,15 @@ class TestMintIds:
 # ``jobs_dir() / <id> / 'evidence'`` onto the one spelling" — so a later reader
 # knows what earns a place here rather than guessing from the list.
 #
-# ``packages/orchestration/checkpoints.py`` and ``packages/orchestration/
-# storage.py`` are DELIBERATELY EXCLUDED and correctly keep their ``jobs_dir``
-# calls. They name the CLASSIC job store, ``<data_root>/jobs/<uuid>.json``,
-# which is one FILE per job and a different concept from a job's evidence
-# DIRECTORY; that store is deleted in F260 T004, not here. The reason is written
-# down because an exclusion a later reader cannot justify is one a later reader
-# deletes — or, worse, "fixes" by migrating the classic store onto an evidence
-# path it was never meant to share.
+# ``packages/orchestration/storage.py`` is DELIBERATELY EXCLUDED and correctly
+# keeps its ``jobs_dir`` calls. It names the CLASSIC job store,
+# ``<data_root>/jobs/<uuid>.json``, which is one FILE per job and a different
+# concept from a job's evidence DIRECTORY; that store is deleted in F260 T004,
+# not here. ``packages/orchestration/checkpoints.py`` called ``jobs_dir`` too
+# until the flip moved its job snapshot onto ``data_paths.job_record_path``.
+# The reason is written down because an exclusion a later reader cannot justify
+# is one a later reader deletes — or, worse, "fixes" by migrating the classic
+# store onto an evidence path it was never meant to share.
 _JOB_EVIDENCE_OWNING_MODULES = (
     "packages.orchestration.pingpong_job",
     "packages.orchestration.job_evidence",
@@ -789,9 +790,9 @@ class TestJobAndRunLayout:
         back. Only reading the module itself sees it, which is why BOTH readings
         ship rather than either one alone.
 
-        ``checkpoints.py`` and ``storage.py`` are not in this set on purpose:
-        they name the CLASSIC store ``<data_root>/jobs/<uuid>.json``, a file per
-        job rather than a job's evidence directory, and F260 T004 deletes it.
+        ``storage.py`` is not in this set on purpose: it names the CLASSIC
+        store ``<data_root>/jobs/<uuid>.json``, a file per job rather than a
+        job's evidence directory, and F260 T004 deletes it.
         """
         import importlib
 
@@ -823,16 +824,17 @@ class TestJobAndRunLayout:
             assert Path(module.__file__).is_file(), f"{modname} has no source file"
 
     def test_the_classic_store_modules_still_call_jobs_dir(self):
-        """The excluded pair must keep naming the classic store, not lose it quietly.
+        """The excluded module must keep naming the classic store, not lose it quietly.
 
         This is the other half of the non-vacuity reading: if ``jobs_dir`` had
         simply been deleted everywhere, the absence guard above would pass for
-        the wrong reason. ``checkpoints.py`` and ``storage.py`` are the modules
-        that legitimately still call it, until F260 T004 deletes that store.
+        the wrong reason. ``storage.py`` is the module that legitimately still
+        calls it, until F260 T004 deletes that store. ``checkpoints.py`` called
+        it too until the flip moved its job snapshot onto ``job_record_path``.
         """
-        from packages.orchestration import checkpoints, storage
+        from packages.orchestration import storage
 
-        for module in (checkpoints, storage):
+        for module in (storage,):
             hits = self._jobs_dir_references(module)
             assert hits, (
                 f"{module.__name__} no longer references jobs_dir; the classic "
```
