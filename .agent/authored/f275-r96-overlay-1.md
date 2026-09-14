# F275 round 96 — the flip's seventh overlay, part 1 of 1

What the seventh overlay changes. `job show` prints the unified record as its exporter writes
it, `json.dumps(_export_job(job), indent=2)`, where it called a pydantic method `JobPlan` does
not have. Tests that round-tripped a record through pydantic dumps and validates restore it
through `_export_job` and `_import_job`, and a deep copy is `copy.deepcopy`. An old record a
test loads has the unified record's minimal shape, `job_id` and `job_title`. Budget tests hand
the record the serialized dict `JobPlan.budgets` holds and read its keys. The runtime fixture of
the context-inspect tests saves its record with `save_job_plan`. A record's `created_at` is the
ISO string it stores, so six test constructions pass `.isoformat()`. And the fulfillment
record's `created_at`, a `datetime`, is formatted again in `export_job_fulfillment_json`.

This part holds 10 whole file diffs, `apps/cli/commands/job.py` through `tests/test_grouped_cli.py`.

Base: `844a7f21`. The flipped tree is that commit checked out and then built exactly as G4 of
`.agent/authored/f275-r96.md` orders: the committed generator re-derives the TIP re-keyed set from
the two pinned round 77 JSON files, the guarded transform runs over the checkout with that set, its
owners file and `r61_status.json`, and the result is staged.

The SEVENTH overlay is formed by 1 part, and this is part 1. The parts apply after
`.agent/authored/f275-r95-overlay-4.md`: `.agent/authored/f275-r90-overlay.md`, then
`.agent/authored/f275-r91-overlay.md`, then `.agent/authored/f275-r92-overlay-1.md` through
`-4.md`, then `.agent/authored/f275-r93-overlay-1.md` and `-2.md`, then
`.agent/authored/f275-r94-overlay-1.md` and `-2.md`, then `.agent/authored/f275-r95-overlay-1.md`
through `-4.md` are applied to the staged flipped tree overlay by overlay, each overlay staged in
turn, and the seventh overlay's diff was taken against that state. The parts apply in `<k>`
order, part 1 first; joined in that order their fences are that one diff.

How to apply this part, inside the flipped tree with every earlier overlay applied and staged and
every part before this one applied:

1. Extract the fence below: the lines strictly between the line of three backticks followed by
   `diff` and the closing line of three backticks, each line kept with its newline.
2. Run `git apply --check <extracted file>` and require exit 0.
3. Run `git apply <extracted file>`.

```diff
diff --git a/apps/cli/commands/job.py b/apps/cli/commands/job.py
index fc024395..feb97c7c 100644
--- a/apps/cli/commands/job.py
+++ b/apps/cli/commands/job.py
@@ -186,13 +186,17 @@ def _scope_label(job: JobPlan, scope: ProjectScope, known_ids: set[str]) -> str:
 
 
 def _cmd_show_job(job_id_str: str) -> None:
+    import json
+
+    from packages.orchestration.pingpong_job import _export_job
+
     job_id = resolve_job_id(job_id_str)
     try:
         job = require_job_plan(job_id)
     except JobNotFoundError as exc:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(1)
-    print(job.model_dump_json(indent=2))
+    print(json.dumps(_export_job(job), indent=2))
     if job.intake:
         _print_intake_block(job.intake)
 
diff --git a/packages/orchestration/job_fulfillment.py b/packages/orchestration/job_fulfillment.py
index 3c3daf95..d9506c96 100644
--- a/packages/orchestration/job_fulfillment.py
+++ b/packages/orchestration/job_fulfillment.py
@@ -229,7 +229,7 @@ def export_job_fulfillment_json(record: JobFulfillmentRecord) -> dict[str, Any]:
         "staged_files": record.staged_files,
         "promotion_files": record.promotion_files,
         "changed_target_files": record.changed_target_files,
-        "created_at": record.created_at,
+        "created_at": record.created_at.isoformat(),
         "updated_at": record.updated_at.isoformat(),
     }
 
diff --git a/tests/cli/test_context_inspect_runtime.py b/tests/cli/test_context_inspect_runtime.py
index 842a953b..c74ef97f 100644
--- a/tests/cli/test_context_inspect_runtime.py
+++ b/tests/cli/test_context_inspect_runtime.py
@@ -16,7 +16,7 @@ from pathlib import Path
 from uuid import uuid4
 
 from packages.core.models import Artifact, ArtifactKind
-from packages.orchestration.pingpong_job import JobPlan, TaskEntry
+from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan
 
 # ---------------------------------------------------------------------------
 # Helpers
@@ -38,9 +38,7 @@ def _create_temp_job(tmp_path: Path, repo_path: Path, tasks: list[TaskEntry] | N
         tasks=tasks or [task],
         artifacts=[art],
     )
-    jobs_dir = tmp_path / "jobs"
-    jobs_dir.mkdir(parents=True, exist_ok=True)
-    (jobs_dir / f"{job.job_id}.json").write_text(job.model_dump_json(indent=2))
+    save_job_plan(job, tmp_path)
     return job
 
 
diff --git a/tests/cli/test_golden_path.py b/tests/cli/test_golden_path.py
index 62a61490..4d01ea61 100644
--- a/tests/cli/test_golden_path.py
+++ b/tests/cli/test_golden_path.py
@@ -127,11 +127,11 @@ class TestDoMission:
 
     def test_old_job_json_without_mission_loads(self, tmp_path):
         """Pre-F147 job JSON without mission field must still load."""
-        from packages.orchestration.pingpong_job import JobPlan
+        from packages.orchestration.pingpong_job import _import_job
 
         old_json = json.dumps({
-            "id": "00000000-0000-0000-0000-000000000001",
-            "name": "legacy job",
+            "job_id": "0000000000000001",
+            "job_title": "legacy job",
             "user_prompt": "do something",
             "created_at": "2026-01-01T00:00:00Z",
             "tasks": [],
@@ -140,8 +140,8 @@ class TestDoMission:
             "budget": {},
             "metadata": {},
         })
-        job = JobPlan.model_validate_json(old_json)
-        assert job.mission is None
+        job = _import_job(json.loads(old_json))
+        assert job.mission == ""
         assert job.job_title == "legacy job"
 
     def test_long_mission_stored_fully(self, tmp_path):
@@ -868,7 +868,7 @@ class TestShortIdResolution:
         )
         assert result.returncode == 0, result.stderr
         data = json.loads(result.stdout)
-        assert data["id"] == job_id
+        assert data["job_id"] == job_id
 
     def test_decision_list_accepts_short_id(self, tmp_path):
         """remedy decision list <short> resolves to full UUID."""
diff --git a/tests/orchestration/test_fence_e2e.py b/tests/orchestration/test_fence_e2e.py
index 53c38c72..ada9e3af 100644
--- a/tests/orchestration/test_fence_e2e.py
+++ b/tests/orchestration/test_fence_e2e.py
@@ -437,8 +437,8 @@ class TestJobFencesField:
         assert job.fences is None
 
     def test_backward_compatible_load(self):
-        data = {"name": "old-job", "id": str(uuid4())}
-        job = JobPlan.model_validate(data)
+        from packages.orchestration.pingpong_job import _import_job
+        job = _import_job({"job_id": uuid4().hex[:16], "job_title": "old-job"})
         assert job.fences is None
 
     def test_set_fences(self):
@@ -450,16 +450,16 @@ class TestJobFencesField:
 
     def test_round_trip_json(self):
         from packages.core.models import JobFences
+        from packages.orchestration.pingpong_job import _export_job, _import_job
         job = JobPlan(job_title="test", fences=JobFences(allow=["src/**"], deny=[]))
-        data = job.model_dump()
-        restored = JobPlan.model_validate(data)
+        restored = _import_job(json.loads(json.dumps(_export_job(job))))
         assert restored.fences is not None
         assert restored.fences.allow == ["src/**"]
 
     def test_fences_none_round_trip(self):
+        from packages.orchestration.pingpong_job import _export_job, _import_job
         job = JobPlan(job_title="test")
-        data = job.model_dump()
-        restored = JobPlan.model_validate(data)
+        restored = _import_job(json.loads(json.dumps(_export_job(job))))
         assert restored.fences is None
 
     def test_closed_type_rejects_extra_fields(self):
diff --git a/tests/orchestration/test_job_budgets.py b/tests/orchestration/test_job_budgets.py
index 6c007e88..340a0a49 100644
--- a/tests/orchestration/test_job_budgets.py
+++ b/tests/orchestration/test_job_budgets.py
@@ -1,6 +1,7 @@
 """F018 T001 — JobBudgets model, config, CLI precedence, RunManifest snapshot."""
 from __future__ import annotations
 
+import json
 from datetime import datetime, timedelta, timezone
 
 import pytest
@@ -131,22 +132,27 @@ class TestJobBudgetsModel:
         assert b.deadline == datetime(2027, 1, 1, 1, 0, 0, tzinfo=timezone.utc)
 
     def test_backward_compatible_old_job_fixture(self):
-        data = {"name": "old-job", "id": "00000000-0000-0000-0000-000000000001"}
-        job = JobPlan.model_validate(data)
+        from packages.orchestration.pingpong_job import _import_job
+        job = _import_job({"job_id": "0000000000000001", "job_title": "old-job"})
         assert job.budgets is None
         assert job.job_title == "old-job"
 
     def test_job_with_budgets_serializes(self):
+        from packages.orchestration.pingpong_job import _export_job, _import_job
         dl = datetime(2026, 12, 31, tzinfo=timezone.utc)
         job = JobPlan(
             job_title="budgeted",
-            budgets=JobBudgets(max_total_tokens=100_000, deadline=dl),
+            budgets=JobBudgets(max_total_tokens=100_000, deadline=dl).model_dump(mode="json"),
         )
-        d = job.model_dump()
+        d = _export_job(job)
         assert d["budgets"]["max_total_tokens"] == 100_000
         assert d["budgets"]["deadline"] is not None
+        job2 = _import_job(d)
+        assert job2.budgets["max_total_tokens"] == 100_000
+        assert job2.budgets["deadline"] is not None
 
     def test_job_with_budgets_roundtrips(self):
+        from packages.orchestration.pingpong_job import _export_job, _import_job
         dl = datetime(2026, 12, 31, tzinfo=timezone.utc)
         job = JobPlan(
             job_title="budgeted",
@@ -154,13 +160,13 @@ class TestJobBudgetsModel:
                 max_total_tokens=100_000,
                 max_provider_calls=10,
                 deadline=dl,
-            ),
+            ).model_dump(mode="json"),
         )
-        d = job.model_dump(mode="json")
-        job2 = JobPlan.model_validate(d)
+        d = _export_job(job)
+        job2 = _import_job(d)
         assert job2.budgets is not None
-        assert job2.budgets.max_total_tokens == 100_000
-        assert job2.budgets.max_provider_calls == 10
+        assert job2.budgets["max_total_tokens"] == 100_000
+        assert job2.budgets["max_provider_calls"] == 10
 
     def test_float_rejected_for_int_field(self):
         with pytest.raises(Exception):
@@ -183,12 +189,14 @@ class TestJobBudgetsModel:
             JobBudgets(max_wall_clock_minutes="30")
 
     def test_json_roundtrip_preserves_strict_types(self):
-        b = JobBudgets(max_total_tokens=100, max_provider_calls=3)
-        job = JobPlan(job_title="strict-test", budgets=b)
-        json_str = job.model_dump_json()
-        job2 = JobPlan.model_validate_json(json_str)
-        assert job2.budgets.max_total_tokens == 100
-        assert isinstance(job2.budgets.max_total_tokens, int)
+        from packages.orchestration.pingpong_job import _export_job, _import_job
+        job = JobPlan(
+            job_title="strict-test",
+            budgets=JobBudgets(max_total_tokens=100, max_provider_calls=3).model_dump(mode="json"),
+        )
+        job2 = _import_job(json.loads(json.dumps(_export_job(job))))
+        assert job2.budgets["max_total_tokens"] == 100
+        assert isinstance(job2.budgets["max_total_tokens"], int)
 
     def test_config_only_budgets_persist_on_job(self, tmp_path, monkeypatch):
         toml = tmp_path / "remedy.toml"
diff --git a/tests/orchestration/test_long_run_executor.py b/tests/orchestration/test_long_run_executor.py
index 2c1cf85b..a0967989 100644
--- a/tests/orchestration/test_long_run_executor.py
+++ b/tests/orchestration/test_long_run_executor.py
@@ -8,6 +8,7 @@ clock and deadlines go through an injected clock.
 """
 from __future__ import annotations
 
+import copy
 import json
 from datetime import datetime, timedelta, timezone
 from pathlib import Path
@@ -744,7 +745,9 @@ def _single_pass(job: JobPlan, provider) -> None:
 
 def _normalize(job: JobPlan) -> dict:
     """Job JSON with the randomly generated artifact ids replaced by ordinals."""
-    payload = json.loads(job.model_dump_json())
+    from packages.orchestration.pingpong_job import _export_job
+
+    payload = json.loads(json.dumps(_export_job(job)))
     mapping: dict[str, str] = {}
     for i, artifact in enumerate(payload.get("artifacts", [])):
         mapping[artifact["id"]] = f"artifact-{i}"
@@ -759,8 +762,8 @@ class TestSinglePassRegression:
         self, isolate_data_root, control_root
     ):
         job = make_job(3)
-        single = job.model_copy(deep=True)
-        cycled = job.model_copy(deep=True)
+        single = copy.deepcopy(job)
+        cycled = copy.deepcopy(job)
 
         _single_pass(single, FakeProvider())
         single_workspace = sorted(
diff --git a/tests/orchestration/test_loop_run.py b/tests/orchestration/test_loop_run.py
index be8cb9a9..f58ca7be 100644
--- a/tests/orchestration/test_loop_run.py
+++ b/tests/orchestration/test_loop_run.py
@@ -332,9 +332,9 @@ def test_manual_trigger_yields_no_notice(tmp_path: Path) -> None:
 
 def test_last_run_for_loop_returns_the_most_recent_run_or_none(tmp_path: Path) -> None:
     older = _stored_job("older run", loop_ref="nightly-tidy",
-                        created_at=datetime(2026, 8, 11, tzinfo=timezone.utc))
+                        created_at=datetime(2026, 8, 11, tzinfo=timezone.utc).isoformat())
     newer = _stored_job("newer run", loop_ref="nightly-tidy",
-                        created_at=datetime(2026, 8, 13, tzinfo=timezone.utc))
+                        created_at=datetime(2026, 8, 13, tzinfo=timezone.utc).isoformat())
     pingpong_job.save_job_plan(older, tmp_path)
     pingpong_job.save_job_plan(newer, tmp_path)
 
@@ -344,9 +344,9 @@ def test_last_run_for_loop_returns_the_most_recent_run_or_none(tmp_path: Path) -
 
 def test_last_run_for_loop_ignores_another_loops_run(tmp_path: Path) -> None:
     mine = _stored_job("mine", loop_ref="nightly-tidy",
-                       created_at=datetime(2026, 8, 11, tzinfo=timezone.utc))
+                       created_at=datetime(2026, 8, 11, tzinfo=timezone.utc).isoformat())
     theirs = _stored_job("theirs", loop_ref="weekly-review",
-                         created_at=datetime(2026, 8, 13, tzinfo=timezone.utc))
+                         created_at=datetime(2026, 8, 13, tzinfo=timezone.utc).isoformat())
     pingpong_job.save_job_plan(mine, tmp_path)
     pingpong_job.save_job_plan(theirs, tmp_path)
 
diff --git a/tests/orchestration/test_run_contract.py b/tests/orchestration/test_run_contract.py
index c0185524..00e6e105 100644
--- a/tests/orchestration/test_run_contract.py
+++ b/tests/orchestration/test_run_contract.py
@@ -369,9 +369,8 @@ class TestContractPersistence:
         job = _make_job()
         c = ensure_contract(job)
         # Simulate save_job / load_job roundtrip
-        json_str = job.model_dump_json()
-        from packages.orchestration.pingpong_job import JobPlan
-        restored = JobPlan.model_validate_json(json_str)
+        from packages.orchestration.pingpong_job import _export_job, _import_job
+        restored = _import_job(json.loads(json.dumps(_export_job(job))))
         loaded = load_contract(restored)
         assert loaded is not None
         assert loaded.contract_id == c.contract_id
@@ -649,9 +648,8 @@ class TestUsageLedger:
         job = _make_job()
         u = RunUsage(loops_used=5, tokens_used=1000)
         save_usage(job, u)
-        json_str = job.model_dump_json()
-        from packages.orchestration.pingpong_job import JobPlan
-        restored = JobPlan.model_validate_json(json_str)
+        from packages.orchestration.pingpong_job import _export_job, _import_job
+        restored = _import_job(json.loads(json.dumps(_export_job(job))))
         loaded = load_usage(restored)
         assert loaded.loops_used == 5
         assert loaded.tokens_used == 1000
diff --git a/tests/test_grouped_cli.py b/tests/test_grouped_cli.py
index 63829eae..ab3a0015 100644
--- a/tests/test_grouped_cli.py
+++ b/tests/test_grouped_cli.py
@@ -658,9 +658,9 @@ class TestJobListCLI:
         monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
         from datetime import datetime, timedelta, timezone
         older = JobPlan(job_id=mint_job_id(), job_title="older", user_prompt="x",
-                    created_at=datetime.now(timezone.utc) - timedelta(days=1))
+                    created_at=(datetime.now(timezone.utc) - timedelta(days=1)).isoformat())
         newer = JobPlan(job_id=mint_job_id(), job_title="newer", user_prompt="x",
-                    created_at=datetime.now(timezone.utc))
+                    created_at=datetime.now(timezone.utc).isoformat())
         save_job_plan(older)
         save_job_plan(newer)
         from apps.cli.commands.job import _cmd_list_jobs
```
