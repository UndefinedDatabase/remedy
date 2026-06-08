"""
Domain tests: orchestration/test_source_apply.py
Migrated from step-numbered test files.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock
from uuid import UUID, uuid4
from uuid import uuid4
import json
import os
import pytest

from packages.core.models import (
    Artifact,
    ArtifactKind,
    Job,
    RunState,
    Task,
)
from packages.orchestration.storage import save_job

def _make_job(*, project_id: str | None = None, target_repo: str | None = None) -> Job:
    meta: dict = {}
    if project_id:
        meta["project_id"] = project_id
    if target_repo:
        meta["target_repo"] = target_repo
    return Job(
        id=uuid4(),
        name="test job",
        user_prompt="test prompt",
        state=RunState.RUNNING,
        tasks=[
            Task(
                id=uuid4(),
                description="task",
                status=RunState.PENDING,
                inputs={"task_type": "patch"},
                output_artifact_ids=[],
            ),
        ],
        artifacts=[],
        metadata=meta,
    )


def _make_job_s91():
    job = MagicMock()
    job.id = uuid4()
    job.name = "test-job"
    job.state.value = "active"
    job.tasks = []
    job.artifacts = []
    job.metadata = {}
    return job


def _make_job_s101(task_count: int = 3):
    job = MagicMock()
    job.id = uuid4()
    job.name = "test-job"
    job.state.value = "active"
    job.tasks = []
    job.artifacts = []
    job.metadata = {}
    for i in range(task_count):
        t = MagicMock()
        t.id = uuid4()
        t.task_type = "test_task"
        t.status.value = "completed" if i == 0 else "pending"
        t.metadata = {}
        job.tasks.append(t)
    return job


# ---------------------------------------------------------------------------
# Step 101 — Smoke/UX Contract Reset
# ---------------------------------------------------------------------------


def _make_job_with_intent(tmp_path: Path, monkeypatch) -> tuple[Job, str, Path]:
    """Create a job with an approved patch intent and attached repo."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))

    from packages.orchestration.approval_queue import (
        APPROVAL_APPROVED,
        make_intent_id,
        set_approval_state,
    )
    from packages.orchestration.permissions import Capability, set_permission

    repo = tmp_path / "repo"
    repo.mkdir()
    target = repo / "notes.md"
    target.write_text("# Original\n\nOriginal content.\n", encoding="utf-8")

    art_id = uuid4()
    intent_id = make_intent_id(art_id, 0)
    artifact = Artifact(
        id=art_id,
        kind=ArtifactKind.BUILDER_PROPOSAL,
        name="patch artifact",
        content="Summary:\nTest patch\nProposed Changes:\n  - Added line\nNotes:\nNone",
        metadata={
            "patch_intent_explanations": [
                {
                    "file": "notes.md",
                    "action": "modify",
                    "risk": "low",
                    "reason": "test intent",
                    "summary": "test",
                }
            ],
        },
    )

    job = Job(
        id=uuid4(),
        name="patch job",
        user_prompt="apply test",
        state=RunState.RUNNING,
        tasks=[],
        artifacts=[artifact],
        metadata={"target_repo": str(repo)},
    )
    set_approval_state(job, intent_id, APPROVAL_APPROVED)
    set_permission(job, Capability.repo_generated_write, allow=True)
    save_job(job)
    return job, intent_id, repo


# ===========================================================================
# Step 53.1: Continue-from-node project linking
# ===========================================================================


def _make_permitted_job():
    """Create a job with repo_generated_write permission granted."""
    job = _make_job()
    job.metadata["permissions"] = {"repo_generated_write": "allow"}
    return job


def _make_approved_job() -> tuple:
    """Create a job with permission + an approved patch intent. Returns (job, intent_id)."""
    job = _make_permitted_job()
    # Create artifact with patch intent explanation + approval
    artifact = MagicMock()
    artifact.id = uuid4()
    artifact.task_id = uuid4()
    intent_id = f"{artifact.id.hex[:8]}-0"
    artifact.metadata = {
        "patch_intent_explanations": [
            {"file": "test.py", "action": "create", "risk": "low", "reason": "test", "summary": "test"}
        ],
        "patch_intent_approvals": {
            intent_id: {
                "intent_id": intent_id,
                "state": "approved",
                "decided_at": "2026-01-01T00:00:00Z",
                "decided_by": "test",
            }
        },
    }
    job.artifacts = [artifact]
    return job, intent_id


# ---------------------------------------------------------------------------
# Step 91 — ELK Directional Layout
# ---------------------------------------------------------------------------




class TestPatchRevert:
    """Snapshot-backed revert for applied patch intents."""

    def test_apply_stores_snapshot(self, tmp_path, monkeypatch):
        job, intent_id, repo = _make_job_with_intent(tmp_path, monkeypatch)
        from packages.orchestration.patch_apply import apply_patch_intent
        result = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.state == "applied", f"blocked: {result.blocked_reason}"

        snap_dir = tmp_path / "workspaces" / str(job.id) / "patch_snapshots" / intent_id
        assert (snap_dir / "metadata.json").exists()

    def test_revert_restores_modified_file(self, tmp_path, monkeypatch):
        job, intent_id, repo = _make_job_with_intent(tmp_path, monkeypatch)
        target = repo / "notes.md"
        original = target.read_text()

        from packages.orchestration.patch_apply import apply_patch_intent
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert target.read_text() != original

        from packages.orchestration.patch_revert import revert_patch_intent
        # Reload job since apply_patch_intent saved it
        from packages.orchestration.storage import load_job
        job = load_job(job.id)
        result = revert_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.state == "reverted"
        assert target.read_text() == original

    def test_revert_deletes_created_file(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.approval_queue import APPROVAL_APPROVED, make_intent_id, set_approval_state
        from packages.orchestration.permissions import Capability, set_permission

        repo = tmp_path / "repo"
        repo.mkdir()

        art_id = uuid4()
        intent_id = make_intent_id(art_id, 0)
        artifact = Artifact(
            id=art_id, kind=ArtifactKind.BUILDER_PROPOSAL, name="create patch",
            content="Summary:\nCreate file\nProposed Changes:\n  - New content\nNotes:\nNone",
            metadata={
                "patch_intent_explanations": [{
                    "file": "new_file.md", "action": "create",
                    "risk": "low", "reason": "test", "summary": "test",
                }],
            },
        )
        job = Job(
            id=uuid4(), name="create job", user_prompt="create",
            state=RunState.RUNNING, tasks=[], artifacts=[artifact],
            metadata={"target_repo": str(repo)},
        )
        set_approval_state(job, intent_id, APPROVAL_APPROVED)
        set_permission(job, Capability.repo_generated_write, allow=True)
        save_job(job)

        from packages.orchestration.patch_apply import apply_patch_intent
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert (repo / "new_file.md").exists()

        from packages.orchestration.patch_revert import revert_patch_intent
        from packages.orchestration.storage import load_job
        job = load_job(job.id)
        result = revert_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.state == "reverted"
        assert not (repo / "new_file.md").exists()

    def test_second_revert_noop(self, tmp_path, monkeypatch):
        job, intent_id, repo = _make_job_with_intent(tmp_path, monkeypatch)

        from packages.orchestration.patch_apply import apply_patch_intent
        apply_patch_intent(job, intent_id, data_dir=tmp_path)

        from packages.orchestration.patch_revert import revert_patch_intent
        from packages.orchestration.storage import load_job
        job = load_job(job.id)
        revert_patch_intent(job, intent_id, data_dir=tmp_path)

        job = load_job(job.id)
        result2 = revert_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result2.state == "noop"
        assert result2.outcome == "already_reverted"

    def test_blocked_if_snapshot_missing(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job, intent_id, repo = _make_job_with_intent(tmp_path, monkeypatch)
        # Don't apply — no snapshot exists
        from packages.orchestration.patch_revert import revert_patch_intent
        result = revert_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.state == "blocked"
        assert result.blocked_reason == "snapshot_missing"

    def test_run_log_exact_schema(self, tmp_path, monkeypatch):
        job, intent_id, repo = _make_job_with_intent(tmp_path, monkeypatch)

        from packages.orchestration.patch_apply import apply_patch_intent
        apply_patch_intent(job, intent_id, data_dir=tmp_path)

        from packages.orchestration.patch_revert import revert_patch_intent
        from packages.orchestration.storage import load_job
        job = load_job(job.id)
        revert_patch_intent(job, intent_id, data_dir=tmp_path)

        from packages.orchestration.timeline import load_run_events
        events = load_run_events(tmp_path, job.id)
        revert_events = [e for e in events if e.get("event") == "patch_intent_reverted"]
        assert len(revert_events) >= 1
        meta = revert_events[0]["metadata"]
        required_keys = {
            "intent_id", "target_path", "action", "outcome",
            "existed_before", "bytes_written", "line_count",
            "before_sha256", "after_sha256",
        }
        assert required_keys <= set(meta.keys())

    def test_brain_has_patch_revert_node(self, tmp_path, monkeypatch):
        job, intent_id, repo = _make_job_with_intent(tmp_path, monkeypatch)

        from packages.orchestration.patch_apply import apply_patch_intent
        apply_patch_intent(job, intent_id, data_dir=tmp_path)

        from packages.orchestration.patch_revert import revert_patch_intent
        from packages.orchestration.storage import load_job
        job = load_job(job.id)
        revert_patch_intent(job, intent_id, data_dir=tmp_path)

        from packages.orchestration.timeline import load_run_events
        events = load_run_events(tmp_path, job.id)

        from packages.orchestration.project_brain import NT_PATCH_REVERT, build_project_brain
        graph = build_project_brain(job, events)
        types = {n.type for n in graph.nodes}
        assert NT_PATCH_REVERT in types

    def test_no_raw_content_in_revert_event(self, tmp_path, monkeypatch):
        job, intent_id, repo = _make_job_with_intent(tmp_path, monkeypatch)

        from packages.orchestration.patch_apply import apply_patch_intent
        apply_patch_intent(job, intent_id, data_dir=tmp_path)

        from packages.orchestration.patch_revert import revert_patch_intent
        from packages.orchestration.storage import load_job
        job = load_job(job.id)
        revert_patch_intent(job, intent_id, data_dir=tmp_path)

        from packages.orchestration.timeline import load_run_events
        events = load_run_events(tmp_path, job.id)
        for ev in events:
            if ev.get("event") == "patch_intent_reverted":
                meta_str = json.dumps(ev["metadata"])
                assert "Original content" not in meta_str


# ===========================================================================
# Step 55: Change Set
# ===========================================================================




class TestChangeSet:
    """Change Set / Review Board v0."""

    def test_derive_change_set(self, tmp_path, monkeypatch):
        job, intent_id, repo = _make_job_with_intent(tmp_path, monkeypatch)

        from packages.orchestration.change_set import derive_change_set
        changes = derive_change_set(job, [])
        assert len(changes) == 1
        assert changes[0].intent_id == intent_id
        assert changes[0].target_path == "notes.md"
        assert changes[0].status == "approved"

    def test_change_list_json_schema(self, tmp_path, monkeypatch):
        job, intent_id, repo = _make_job_with_intent(tmp_path, monkeypatch)

        from packages.orchestration.change_set import derive_change_set, export_change_list_json
        changes = derive_change_set(job, [])
        exported = export_change_list_json(str(job.id), changes)
        assert exported["version"] == 1
        assert "job_id" in exported
        assert "changes" in exported
        assert len(exported["changes"]) == 1

    def test_change_show_json_schema(self, tmp_path, monkeypatch):
        job, intent_id, repo = _make_job_with_intent(tmp_path, monkeypatch)

        from packages.orchestration.change_set import derive_change_set, export_change_show_json
        changes = derive_change_set(job, [])
        exported = export_change_show_json(str(job.id), changes[0])
        required = {"version", "job_id", "intent_id", "status", "target_path",
                     "risk", "approval", "apply", "proof", "test", "revert", "memory"}
        assert required <= set(exported.keys())

    def test_change_text_safe(self, tmp_path, monkeypatch):
        job, intent_id, repo = _make_job_with_intent(tmp_path, monkeypatch)

        from packages.orchestration.change_set import derive_change_set, summarize_change_list
        changes = derive_change_set(job, [])
        text = summarize_change_list(changes)
        assert intent_id in text
        assert "notes.md" in text

    def test_brain_has_change_set_node(self, tmp_path, monkeypatch):
        job, intent_id, repo = _make_job_with_intent(tmp_path, monkeypatch)

        from packages.orchestration.project_brain import NT_CHANGE_SET, build_project_brain
        graph = build_project_brain(job, [])
        types = {n.type for n in graph.nodes}
        assert NT_CHANGE_SET in types

    def test_no_raw_content_in_change_set(self, tmp_path, monkeypatch):
        job, intent_id, repo = _make_job_with_intent(tmp_path, monkeypatch)

        from packages.orchestration.change_set import derive_change_set, export_change_show_json
        changes = derive_change_set(job, [])
        exported = export_change_show_json(str(job.id), changes[0])
        exported_str = json.dumps(exported)
        assert "Original content" not in exported_str
        assert "Added line" not in exported_str


# ===========================================================================
# Step 56: Token Economy
# ===========================================================================




class TestSourceContext:
    def test_select_relevant_files(self, tmp_path):
        from packages.orchestration.source_context import select_relevant_files
        (tmp_path / "README.md").write_text("# Test")
        (tmp_path / "main.py").write_text("print('hi')")
        (tmp_path / "test_main.py").write_text("def test(): pass")
        (tmp_path / "package.json").write_text('{"name":"x"}')

        files = select_relevant_files(tmp_path, budget=1000)
        assert len(files) >= 3
        categories = {f.category for f in files}
        assert "manifest" in categories
        assert "readme" in categories

    def test_env_excluded(self, tmp_path):
        from packages.orchestration.source_context import select_relevant_files
        (tmp_path / ".env").write_text("SECRET=abc")
        (tmp_path / "main.py").write_text("x = 1")

        files = select_relevant_files(tmp_path, budget=1000)
        paths = [f.path for f in files]
        assert ".env" not in paths

    def test_budget_respected(self, tmp_path):
        from packages.orchestration.source_context import select_relevant_files
        (tmp_path / "big.py").write_text("x = 1\n" * 10000)

        files = select_relevant_files(tmp_path, budget=100)
        total = sum(f.estimated_tokens for f in files)
        assert total <= 100

    def test_node_modules_excluded(self, tmp_path):
        from packages.orchestration.source_context import select_relevant_files
        nm = tmp_path / "node_modules" / "pkg"
        nm.mkdir(parents=True)
        (nm / "index.js").write_text("module.exports = {}")

        files = select_relevant_files(tmp_path, budget=1000)
        paths = [f.path for f in files]
        assert not any("node_modules" in p for p in paths)

    def test_event_schema(self, tmp_path):
        from packages.orchestration.source_context import inject_source_context
        from packages.orchestration.data_paths import resolve_data_root
        (tmp_path / "main.py").write_text("x = 1")

        job = _make_job_s91()
        data_dir = resolve_data_root()
        ctx = inject_source_context(job, tmp_path, data_dir=data_dir)
        assert ctx.version == 1
        assert ctx.file_count >= 1
        assert ctx.selection_hash != ""


# ---------------------------------------------------------------------------
# Step 98 — Structured Code Patch Intent
# ---------------------------------------------------------------------------




class TestStructuredPatch:
    def test_parse_file_ops_json(self):
        from packages.orchestration.structured_patch import parse_structured_patch
        raw = """Here's the fix:
```json
{
  "file_ops": [
    {"path": "main.py", "action": "modify", "content": "print('fixed')", "summary": "Fix"}
  ]
}
```"""
        patch = parse_structured_patch(raw)
        assert patch.intent_kind == "file_ops"
        assert len(patch.file_ops) == 1
        assert patch.file_ops[0].path == "main.py"

    def test_parse_unified_diff(self):
        from packages.orchestration.structured_patch import parse_structured_patch
        raw = """--- a/main.py
+++ b/main.py
@@ -1,3 +1,3 @@
 def hello():
-    return "world"
+    return "fixed"
"""
        patch = parse_structured_patch(raw)
        assert patch.intent_kind == "unified_diff"
        assert len(patch.unified_diffs) == 1

    def test_parse_narrative_fallback(self):
        from packages.orchestration.structured_patch import parse_structured_patch
        patch = parse_structured_patch("Just update the README with better docs")
        assert patch.intent_kind == "markdown"
        assert patch.applicability == "not_applicable"

    def test_validate_path_traversal(self):
        from packages.orchestration.structured_patch import (
            FileOp, StructuredPatch, validate_structured_patch,
        )
        patch = StructuredPatch(
            intent_kind="file_ops",
            file_ops=(FileOp(path="../../../etc/passwd", action="create", content="bad"),),
            target_paths=("../../../etc/passwd",),
        )
        issues = validate_structured_patch(patch)
        assert len(issues) > 0
        assert any("traversal" in i for i in issues)

    def test_validate_env_blocked(self):
        from packages.orchestration.structured_patch import (
            FileOp, StructuredPatch, validate_structured_patch,
        )
        patch = StructuredPatch(
            intent_kind="file_ops",
            file_ops=(FileOp(path=".env", action="create", content="SECRET=x"),),
            target_paths=(".env",),
        )
        issues = validate_structured_patch(patch)
        assert len(issues) > 0


# ---------------------------------------------------------------------------
# Step 99 — Source Patch Apply
# ---------------------------------------------------------------------------




class TestSourceApply:
    def test_apply_simple_file_op(self, tmp_path):
        from packages.orchestration.source_apply import apply_structured_patch
        from packages.orchestration.structured_patch import FileOp, StructuredPatch

        job, intent_id = _make_approved_job()
        patch = StructuredPatch(
            intent_kind="file_ops",
            file_ops=(FileOp(path="hello.py", action="create", content="print('hi')"),),
            target_paths=("hello.py",),
        )
        result = apply_structured_patch(patch, tmp_path, job=job, intent_id=intent_id)
        assert result.success
        assert result.files_created == 1
        assert (tmp_path / "hello.py").read_text() == "print('hi')"

    def test_apply_modify(self, tmp_path):
        from packages.orchestration.source_apply import apply_structured_patch
        from packages.orchestration.structured_patch import FileOp, StructuredPatch

        job, intent_id = _make_approved_job()
        (tmp_path / "main.py").write_text("old content")
        patch = StructuredPatch(
            intent_kind="file_ops",
            file_ops=(FileOp(path="main.py", action="modify", content="new content"),),
            target_paths=("main.py",),
        )
        result = apply_structured_patch(patch, tmp_path, job=job, intent_id=intent_id)
        assert result.success
        assert result.files_modified == 1
        assert (tmp_path / "main.py").read_text() == "new content"

    def test_apply_blocks_env(self, tmp_path):
        from packages.orchestration.source_apply import apply_structured_patch
        from packages.orchestration.structured_patch import FileOp, StructuredPatch

        job, intent_id = _make_approved_job()
        patch = StructuredPatch(
            intent_kind="file_ops",
            file_ops=(FileOp(path=".env", action="create", content="SECRET=x"),),
            target_paths=(".env",),
        )
        result = apply_structured_patch(patch, tmp_path, job=job, intent_id=intent_id)
        assert not result.success
        # Failure must be path safety, not missing permission or approval
        assert any(".env" in e for e in result.errors)
        assert not any("permission denied" in e for e in result.errors)
        assert not any("approval" in e for e in result.errors)

    def test_apply_blocks_path_traversal(self, tmp_path):
        from packages.orchestration.source_apply import apply_structured_patch
        from packages.orchestration.structured_patch import FileOp, StructuredPatch

        job, intent_id = _make_approved_job()
        patch = StructuredPatch(
            intent_kind="file_ops",
            file_ops=(FileOp(path="../escape.py", action="create", content="bad"),),
            target_paths=("../escape.py",),
        )
        result = apply_structured_patch(patch, tmp_path, job=job, intent_id=intent_id)
        assert not result.success
        # Failure must be path traversal, not missing permission
        assert any("traversal" in e for e in result.errors)

    def test_snapshot_and_revert(self, tmp_path):
        from packages.orchestration.source_apply import apply_structured_patch, revert_apply
        from packages.orchestration.structured_patch import FileOp, StructuredPatch

        job, intent_id = _make_approved_job()
        (tmp_path / "orig.py").write_text("original")
        patch = StructuredPatch(
            intent_kind="file_ops",
            file_ops=(FileOp(path="orig.py", action="modify", content="modified"),),
            target_paths=("orig.py",),
        )
        result = apply_structured_patch(patch, tmp_path, job=job, intent_id=intent_id)
        assert result.success
        assert (tmp_path / "orig.py").read_text() == "modified"

        # Revert
        success = revert_apply(result.snapshots, tmp_path)
        assert success
        assert (tmp_path / "orig.py").read_text() == "original"

    def test_apply_blocks_binary(self, tmp_path):
        from packages.orchestration.source_apply import apply_structured_patch
        from packages.orchestration.structured_patch import FileOp, StructuredPatch

        job, intent_id = _make_approved_job()
        patch = StructuredPatch(
            intent_kind="file_ops",
            file_ops=(FileOp(path="data.bin", action="create", content="hello\x00world"),),
            target_paths=("data.bin",),
        )
        result = apply_structured_patch(patch, tmp_path, job=job, intent_id=intent_id)
        assert not result.success
        # Failure must be binary content, not missing permission
        assert any("binary" in e for e in result.errors)

    def test_apply_without_intent_blocked(self, tmp_path):
        """source_apply without intent_id is blocked."""
        from packages.orchestration.source_apply import apply_structured_patch
        from packages.orchestration.structured_patch import FileOp, StructuredPatch

        patch = StructuredPatch(
            intent_kind="file_ops",
            file_ops=(FileOp(path="x.py", action="create", content="x"),),
            target_paths=("x.py",),
        )
        result = apply_structured_patch(patch, tmp_path, job=_make_permitted_job())
        assert not result.success
        assert any("intent_id" in e for e in result.errors)

    def test_apply_with_pending_intent_blocked(self, tmp_path):
        """source_apply with pending (not approved) intent is blocked."""
        from packages.orchestration.source_apply import apply_structured_patch
        from packages.orchestration.structured_patch import FileOp, StructuredPatch

        job = _make_permitted_job()
        artifact = MagicMock()
        artifact.id = uuid4()
        artifact.task_id = uuid4()
        intent_id = f"{artifact.id.hex[:8]}-0"
        artifact.metadata = {
            "patch_intent_explanations": [
                {"file": "t.py", "action": "create", "risk": "low", "reason": "t", "summary": "t"}
            ],
            "patch_intent_approvals": {
                intent_id: {"intent_id": intent_id, "state": "pending"}
            },
        }
        job.artifacts = [artifact]

        patch = StructuredPatch(
            intent_kind="file_ops",
            file_ops=(FileOp(path="x.py", action="create", content="x"),),
            target_paths=("x.py",),
        )
        result = apply_structured_patch(patch, tmp_path, job=job, intent_id=intent_id)
        assert not result.success
        assert any("pending" in e for e in result.errors)


# ---------------------------------------------------------------------------
# Step 100 — Frontend Build / Smoke
# ---------------------------------------------------------------------------




class TestSourceContextFinalization:
    def test_text_binary_detection_exists(self):
        src = (Path(__file__).parent.parent.parent / "packages" / "orchestration" / "source_context.py").read_text()
        assert "_is_text_file" in src

    def test_inject_source_context_budget(self):
        from packages.orchestration.source_context import inject_source_context
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            (p / "main.py").write_text("x = 1\n")
            ctx = inject_source_context(_make_job_s101(), p, budget=100)
            assert ctx.estimated_tokens <= 200  # reasonable budget


# ---------------------------------------------------------------------------
# Step 110 — Structured Patch/Apply/Test Loop
# ---------------------------------------------------------------------------

