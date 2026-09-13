# F275 round 94 — the flip's fifth overlay, part 2 of 2

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

This part holds 2 whole file diffs, `tests/orchestration/test_proposed_tasks.py` through `tests/test_data_paths.py`.

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
diff --git a/tests/orchestration/test_proposed_tasks.py b/tests/orchestration/test_proposed_tasks.py
index f29ca97c..62dd17cb 100644
--- a/tests/orchestration/test_proposed_tasks.py
+++ b/tests/orchestration/test_proposed_tasks.py
@@ -551,7 +551,7 @@ class TestMaterialization:
 
     def test_do_materialize_creates_real_job_task(self, tmp_path, monkeypatch):
         monkeypatch.setattr("packages.orchestration.proposed_tasks._STORE_DIR", tmp_path / "proposed_tasks")
-        monkeypatch.setattr("packages.orchestration.storage._DATA_DIR", tmp_path / "jobs")
+        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
         _create_real_job(tmp_path)
         t = ProposedTask(title="Materialize me", status=ProposedTaskStatus.APPROVED_FOR_BUILD)
         add_proposed_task(REAL_JOB_UUID, t)
@@ -566,7 +566,7 @@ class TestMaterialization:
 
     def test_do_materialize_rejects_non_approved(self, tmp_path, monkeypatch):
         monkeypatch.setattr("packages.orchestration.proposed_tasks._STORE_DIR", tmp_path / "proposed_tasks")
-        monkeypatch.setattr("packages.orchestration.storage._DATA_DIR", tmp_path / "jobs")
+        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
         _create_real_job(tmp_path)
         t = ProposedTask(title="Not ready", status=ProposedTaskStatus.EVALUATED)
         add_proposed_task(REAL_JOB_UUID, t)
@@ -575,7 +575,7 @@ class TestMaterialization:
 
     def test_do_materialize_rejects_already_materialized(self, tmp_path, monkeypatch):
         monkeypatch.setattr("packages.orchestration.proposed_tasks._STORE_DIR", tmp_path / "proposed_tasks")
-        monkeypatch.setattr("packages.orchestration.storage._DATA_DIR", tmp_path / "jobs")
+        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
         _create_real_job(tmp_path)
         t = ProposedTask(title="Done", status=ProposedTaskStatus.APPROVED_FOR_BUILD, materialized_task_id="existing")
         add_proposed_task(REAL_JOB_UUID, t)
@@ -597,7 +597,7 @@ class TestMaterialization:
 class TestEndToEndFlow:
     def test_full_proposed_task_lifecycle(self, tmp_path, monkeypatch):
         monkeypatch.setattr("packages.orchestration.proposed_tasks._STORE_DIR", tmp_path / "proposed_tasks")
-        monkeypatch.setattr("packages.orchestration.storage._DATA_DIR", tmp_path / "jobs")
+        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
         _create_real_job(tmp_path)
 
         t = propose_task_from_review_finding(REAL_JOB_UUID, title="New feature", reason="Reviewer found gap", risk="medium")
@@ -638,7 +638,7 @@ class TestEndToEndFlow:
 
     def test_full_lifecycle_with_materialize(self, tmp_path, monkeypatch):
         monkeypatch.setattr("packages.orchestration.proposed_tasks._STORE_DIR", tmp_path / "proposed_tasks")
-        monkeypatch.setattr("packages.orchestration.storage._DATA_DIR", tmp_path / "jobs")
+        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
         _create_real_job(tmp_path)
         t = propose_task_from_review_finding(REAL_JOB_UUID, title="Build it", risk="medium")
         evaluate_proposed_task(REAL_JOB_UUID, t.id)
@@ -677,7 +677,7 @@ class TestFileLocking:
 
     def test_approve_then_materialize_preserves_state(self, tmp_path, monkeypatch):
         monkeypatch.setattr("packages.orchestration.proposed_tasks._STORE_DIR", tmp_path / "proposed_tasks")
-        monkeypatch.setattr("packages.orchestration.storage._DATA_DIR", tmp_path / "jobs")
+        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
         _create_real_job(tmp_path)
         t = ProposedTask(title="Build", status=ProposedTaskStatus.EVALUATED)
         add_proposed_task(REAL_JOB_UUID, t)
@@ -756,14 +756,14 @@ class TestStoreRootResolution:
 class TestReconciliation:
     def test_consistent(self, tmp_path, monkeypatch):
         monkeypatch.setattr("packages.orchestration.proposed_tasks._STORE_DIR", tmp_path / "proposed_tasks")
-        monkeypatch.setattr("packages.orchestration.storage._DATA_DIR", tmp_path / "jobs")
+        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
         _create_real_job(tmp_path)
         report = reconcile_materialized(REAL_JOB_UUID)
         assert report["consistent"] is True
 
     def test_missing_job_task(self, tmp_path, monkeypatch):
         monkeypatch.setattr("packages.orchestration.proposed_tasks._STORE_DIR", tmp_path / "proposed_tasks")
-        monkeypatch.setattr("packages.orchestration.storage._DATA_DIR", tmp_path / "jobs")
+        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
         _create_real_job(tmp_path)
         t = ProposedTask(title="Ghost", status=ProposedTaskStatus.APPROVED_FOR_BUILD, materialized_task_id="nonexistent-task-id")
         add_proposed_task(REAL_JOB_UUID, t)
@@ -773,7 +773,7 @@ class TestReconciliation:
 
     def test_corrupt_store(self, tmp_path, monkeypatch):
         monkeypatch.setattr("packages.orchestration.proposed_tasks._STORE_DIR", tmp_path / "proposed_tasks")
-        monkeypatch.setattr("packages.orchestration.storage._DATA_DIR", tmp_path / "jobs")
+        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
         _create_real_job(tmp_path)
         pt_dir = tmp_path / "proposed_tasks"
         pt_dir.mkdir(parents=True, exist_ok=True)
@@ -786,7 +786,7 @@ class TestReconciliation:
 class TestBackendReadiness:
     def test_healthy_job_no_work(self, tmp_path, monkeypatch):
         monkeypatch.setattr("packages.orchestration.proposed_tasks._STORE_DIR", tmp_path / "proposed_tasks")
-        monkeypatch.setattr("packages.orchestration.storage._DATA_DIR", tmp_path / "jobs")
+        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
         _create_real_job(tmp_path)
         report = backend_readiness(REAL_JOB_UUID)
         assert report["storage_health"]["healthy"] is True
@@ -795,7 +795,7 @@ class TestBackendReadiness:
 
     def test_not_ready_with_unresolved(self, tmp_path, monkeypatch):
         monkeypatch.setattr("packages.orchestration.proposed_tasks._STORE_DIR", tmp_path / "proposed_tasks")
-        monkeypatch.setattr("packages.orchestration.storage._DATA_DIR", tmp_path / "jobs")
+        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
         _create_real_job(tmp_path)
         add_proposed_task(REAL_JOB_UUID, ProposedTask(title="Pending"))
         report = backend_readiness(REAL_JOB_UUID)
@@ -809,7 +809,7 @@ class TestBackendReadiness:
 
     def test_not_ready_corrupt_store(self, tmp_path, monkeypatch):
         monkeypatch.setattr("packages.orchestration.proposed_tasks._STORE_DIR", tmp_path / "proposed_tasks")
-        monkeypatch.setattr("packages.orchestration.storage._DATA_DIR", tmp_path / "jobs")
+        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
         _create_real_job(tmp_path)
         pt_dir = tmp_path / "proposed_tasks"
         pt_dir.mkdir(parents=True, exist_ok=True)
@@ -820,7 +820,7 @@ class TestBackendReadiness:
 
     def test_materialized_pending_task(self, tmp_path, monkeypatch):
         monkeypatch.setattr("packages.orchestration.proposed_tasks._STORE_DIR", tmp_path / "proposed_tasks")
-        monkeypatch.setattr("packages.orchestration.storage._DATA_DIR", tmp_path / "jobs")
+        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
         _create_real_job(tmp_path)
         t = propose_task_from_review_finding(REAL_JOB_UUID, title="Work", risk="medium")
         evaluate_proposed_task(REAL_JOB_UUID, t.id)
@@ -835,7 +835,7 @@ class TestBackendReadiness:
 
     def test_execution_health_section(self, tmp_path, monkeypatch):
         monkeypatch.setattr("packages.orchestration.proposed_tasks._STORE_DIR", tmp_path / "proposed_tasks")
-        monkeypatch.setattr("packages.orchestration.storage._DATA_DIR", tmp_path / "jobs")
+        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
         _create_real_job(tmp_path)
         report = backend_readiness(REAL_JOB_UUID)
         assert "execution_health" in report
@@ -844,7 +844,7 @@ class TestBackendReadiness:
 
     def test_corrupt_other_job_degrades_storage(self, tmp_path, monkeypatch):
         monkeypatch.setattr("packages.orchestration.proposed_tasks._STORE_DIR", tmp_path / "proposed_tasks")
-        monkeypatch.setattr("packages.orchestration.storage._DATA_DIR", tmp_path / "jobs")
+        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
         _create_real_job(tmp_path)
         corrupt_path = tmp_path / "jobs" / "corrupt-job.json"
         corrupt_path.write_text("not json")
@@ -856,7 +856,7 @@ class TestBackendReadiness:
 class TestOvernightReadiness:
     def test_never_ready_yet(self, tmp_path, monkeypatch):
         monkeypatch.setattr("packages.orchestration.proposed_tasks._STORE_DIR", tmp_path / "proposed_tasks")
-        monkeypatch.setattr("packages.orchestration.storage._DATA_DIR", tmp_path / "jobs")
+        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
         _create_real_job(tmp_path)
         report = overnight_readiness(REAL_JOB_UUID)
         assert report["ready"] is False
diff --git a/tests/test_data_paths.py b/tests/test_data_paths.py
index dc345cfd..73183baa 100644
--- a/tests/test_data_paths.py
+++ b/tests/test_data_paths.py
@@ -497,8 +497,8 @@ class TestMintIds:
     """
 
     def _minters(self) -> list:
-        from packages.orchestration.data_paths import mint_episode_id, mint_job_id, mint_run_id
-        return [mint_job_id, mint_run_id, mint_episode_id]
+        from packages.orchestration.data_paths import mint_episode_id, mint_job_id, mint_run_id, mint_task_id
+        return [mint_job_id, mint_run_id, mint_episode_id, mint_task_id]
 
     def test_each_mints_sixteen_lowercase_hex_chars(self):
         for mint in self._minters():
@@ -519,6 +519,13 @@ class TestMintIds:
         assert mint_job_id is not mint_episode_id
         assert mint_run_id is not mint_episode_id
 
+    def test_the_task_minter_is_a_fourth_distinct_function(self):
+        """The TASK kind gets its own function too, not an alias of the other three."""
+        from packages.orchestration.data_paths import mint_episode_id, mint_job_id, mint_run_id, mint_task_id
+        assert mint_task_id is not mint_job_id
+        assert mint_task_id is not mint_run_id
+        assert mint_task_id is not mint_episode_id
+
     def test_minted_ids_match_the_short_hex_pattern(self):
         """What lets the existing prefix resolvers accept a minted id at all."""
         from packages.orchestration import data_paths
```
