# F275 round 95 — the flip's sixth overlay, part 4 of 4

What the sixth overlay changes. Production code under `packages/` and `apps/` that read `.id`
or `.name` off a job it loaded, under the local names `job`, `j` or `plan`, reads the unified
record's `job_id` and `job_title` (79 reads; the classic store's own module is untouched). The
job doubles tests hand that code spell the same: the `_FakeJob`, `_Job` and `_LoopJob` classes
carry `job_id` and `job_title`, the `SimpleNamespace` stubs of the `review list` tests pass
`job_id=`, and the tests read those names back. A handler test that doubles the job loader as
the first context manager of its `with` statement now also doubles, as the second, the
resolver the handler's module binds (`resolve_job_id` or `lookup_job_id`) with an identity, so
the handler still receives the id the test built (27 `with` statements).

This part holds 5 whole file diffs, `tests/test_cli_execution_loop_closure.py` through `tests/ui_server/test_sse_stream.py`.

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
diff --git a/tests/test_cli_execution_loop_closure.py b/tests/test_cli_execution_loop_closure.py
index 0780a912..13512cc6 100644
--- a/tests/test_cli_execution_loop_closure.py
+++ b/tests/test_cli_execution_loop_closure.py
@@ -181,6 +181,7 @@ class TestReviewerCliJsonOutput:
         """review run --fixture-reviewer --json returns structured output."""
         job = _make_job(tasks=[{"type": "test", "status": "completed"}])
         with patch("packages.orchestration.pingpong_job.load_job_plan", return_value=job), \
+             patch("apps.cli.commands.review_cmd.lookup_job_id", side_effect=lambda raw: raw), \
              patch("packages.orchestration.pingpong_job.save_job_plan"):
             import contextlib
             import io
@@ -216,6 +217,7 @@ class TestReviewerCliJsonOutput:
         store_recommendations(job, recs)
 
         with patch("packages.orchestration.pingpong_job.load_job_plan", return_value=job), \
+             patch("apps.cli.commands.review_cmd.lookup_job_id", side_effect=lambda raw: raw), \
              patch("packages.orchestration.pingpong_job.save_job_plan"):
             import contextlib
             import io
@@ -243,6 +245,7 @@ class TestReviewerCliJsonOutput:
         store_recommendations(job, recs)
 
         with patch("packages.orchestration.pingpong_job.load_job_plan", return_value=job), \
+             patch("apps.cli.commands.review_cmd.lookup_job_id", side_effect=lambda raw: raw), \
              patch("packages.orchestration.pingpong_job.save_job_plan"):
             import contextlib
             import io
@@ -308,7 +311,8 @@ class TestMemoryCandidateCliCommands:
         job.metadata = {}
         create_candidate(job, "repair_pattern", "Fixed mul")
 
-        with patch("packages.orchestration.pingpong_job.load_job_plan", return_value=job):
+        with patch("packages.orchestration.pingpong_job.load_job_plan", return_value=job), \
+             patch("apps.cli.commands.memory.lookup_job_id", side_effect=lambda raw: raw):
             import contextlib
             import io
 
@@ -328,6 +332,7 @@ class TestMemoryCandidateCliCommands:
         c = create_candidate(job, "test_command", "pytest works")
 
         with patch("packages.orchestration.pingpong_job.load_job_plan", return_value=job), \
+             patch("apps.cli.commands.memory.lookup_job_id", side_effect=lambda raw: raw), \
              patch("packages.orchestration.pingpong_job.save_job_plan"), \
              patch.dict("sys.modules", {"packages.orchestration.memory": MagicMock()}):
             import contextlib
@@ -348,6 +353,7 @@ class TestMemoryCandidateCliCommands:
         c = create_candidate(job, "test_command", "pytest works")
 
         with patch("packages.orchestration.pingpong_job.load_job_plan", return_value=job), \
+             patch("apps.cli.commands.memory.lookup_job_id", side_effect=lambda raw: raw), \
              patch("packages.orchestration.pingpong_job.save_job_plan"):
             import contextlib
             import io
diff --git a/tests/test_project_registry.py b/tests/test_project_registry.py
index e299a9c9..4675b9f8 100644
--- a/tests/test_project_registry.py
+++ b/tests/test_project_registry.py
@@ -32,11 +32,11 @@ def _make_project(**kwargs) -> RemyProject:
 
 class _FakeJob:
     def __init__(self, job_id: str, state: str = "pending", tasks=(), artifacts=()):
-        self.id = UUID(job_id)
+        self.job_id = UUID(job_id)
         self.state = type("S", (), {"value": state})()
         self.tasks = list(tasks)
         self.artifacts = list(artifacts)
-        self.name = f"Job {job_id[:8]}"
+        self.job_title = f"Job {job_id[:8]}"
 
 
 # ---------------------------------------------------------------------------
diff --git a/tests/ui_server/test_budget_tick_envelope.py b/tests/ui_server/test_budget_tick_envelope.py
index c76e418f..b7a2b459 100644
--- a/tests/ui_server/test_budget_tick_envelope.py
+++ b/tests/ui_server/test_budget_tick_envelope.py
@@ -210,7 +210,7 @@ class TestBothTransportsCarryTheSameTick:
         monkeypatch.setattr(mod, "_load_events", lambda job: events)
 
         class _Job:
-            id = "11111111-2222-3333-4444-555555555555"
+            job_id = "11111111-2222-3333-4444-555555555555"
 
         polled = mod._build_events_since_json(_Job(), "0")["events"]
         clock = _Clock()
diff --git a/tests/ui_server/test_event_seq.py b/tests/ui_server/test_event_seq.py
index 899a438b..cf0a7a1b 100644
--- a/tests/ui_server/test_event_seq.py
+++ b/tests/ui_server/test_event_seq.py
@@ -19,7 +19,7 @@ from packages.orchestration import ui_server as mod
 
 
 class _FakeJob:
-    id = "11111111-2222-3333-4444-555555555555"
+    job_id = "11111111-2222-3333-4444-555555555555"
 
 
 def _events(count: int) -> list[dict[str, Any]]:
diff --git a/tests/ui_server/test_sse_stream.py b/tests/ui_server/test_sse_stream.py
index de5c286e..bb8f08db 100644
--- a/tests/ui_server/test_sse_stream.py
+++ b/tests/ui_server/test_sse_stream.py
@@ -117,7 +117,7 @@ class TestFrameShape:
         monkeypatch.setattr(mod, "_load_events", lambda job: _events(3))
 
         class _Job:
-            id = "11111111-2222-3333-4444-555555555555"
+            job_id = "11111111-2222-3333-4444-555555555555"
 
         polled = mod._build_events_since_json(_Job(), "0")["events"]
         streamed = [json.loads(_parse(f)["data"])
@@ -173,7 +173,7 @@ class TestHeartbeatCadence:
 
 # A job the route can carry: `_load_job` is stubbed, so only the id is read.
 class _Job:
-    id = "11111111-2222-3333-4444-555555555555"
+    job_id = "11111111-2222-3333-4444-555555555555"
 
 
 class _Socket:
@@ -398,7 +398,7 @@ class TestStreamCapRoute:
 
     def test_the_stream_is_refused_with_429_beyond_the_cap(self, monkeypatch):
         for _ in range(mod.SSE_MAX_STREAMS_PER_JOB):
-            assert mod.acquire_sse_slot(_Job.id)
+            assert mod.acquire_sse_slot(_Job.job_id)
         answered, streamed = _dispatch(
             monkeypatch, "/api/jobs/J/events/stream?token=tok", _Job(), None)
         assert streamed == []
@@ -406,14 +406,14 @@ class TestStreamCapRoute:
 
     def test_a_refused_stream_does_not_consume_a_slot(self, monkeypatch):
         for _ in range(mod.SSE_MAX_STREAMS_PER_JOB):
-            mod.acquire_sse_slot(_Job.id)
+            mod.acquire_sse_slot(_Job.job_id)
         _dispatch(monkeypatch, "/api/jobs/J/events/stream?token=tok", _Job(), None)
         # Still exactly at the cap: the refusal took nothing.
-        assert mod._SSE_SLOTS_PER_JOB[_Job.id] == mod.SSE_MAX_STREAMS_PER_JOB
+        assert mod._SSE_SLOTS_PER_JOB[_Job.job_id] == mod.SSE_MAX_STREAMS_PER_JOB
 
     def test_a_served_stream_releases_its_slot(self, monkeypatch):
         _dispatch(monkeypatch, "/api/jobs/J/events/stream?token=tok", _Job(), None)
-        assert _Job.id not in mod._SSE_SLOTS_PER_JOB
+        assert _Job.job_id not in mod._SSE_SLOTS_PER_JOB
 
     def test_a_raising_stream_still_releases_its_slot(self, monkeypatch):
         monkeypatch.setattr(mod, "_load_job", lambda jid: (_Job(), None))
@@ -435,7 +435,7 @@ class TestStreamCapRoute:
             raised = True
         assert raised
         # The `finally` is the whole point: a crash must not leak capacity.
-        assert _Job.id not in mod._SSE_SLOTS_PER_JOB
+        assert _Job.job_id not in mod._SSE_SLOTS_PER_JOB
 
     def test_an_unknown_job_never_takes_a_slot(self, monkeypatch):
         _dispatch(
```
