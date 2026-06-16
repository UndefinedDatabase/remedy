"""Tests for Context Inspector v1.

Covers:
- Path classification (protected, unsupported, large, symlink, traversal)
- Inclusion reasons (manifest, readme, task target, intent target, test, source, config)
- Token/budget estimation
- Policy gates
- Tooling awareness
- Readiness assessment
- Redaction (no raw content, no file bodies, no secrets, no MCP content)
- JSON export stability
- Edge cases (no repo, no tasks, empty job)
"""

from __future__ import annotations

import json
from pathlib import Path

from packages.core.models import Artifact, ArtifactKind, Job, Task
from packages.orchestration.context_inspector import (
    BUDGET_NEAR,
    BUDGET_OVER,
    BUDGET_UNKNOWN,
    BUDGET_WITHIN,
    READINESS_BLOCKED,
    READINESS_READY,
    READINESS_WARNINGS,
    ContextPathEntry,
    _classify_path,
    _collect_event_target_paths,
    _compute_budget,
    _detect_tooling,
    _is_path_traversal,
    _is_protected,
    _is_unsupported,
    export_context_inspection_json,
    inspect_context,
    summarize_context_inspection,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_job(*, tasks=None, artifacts=None, user_prompt="Fix the bug"):
    job = Job(name="test-job", user_prompt=user_prompt)
    if tasks:
        job.tasks = tasks
    if artifacts:
        job.artifacts = artifacts
    return job


def _make_repo(tmp_path: Path, files: dict[str, str] | None = None):
    """Create a temporary repo structure."""
    if files is None:
        files = {
            "pyproject.toml": "[project]\nname='test'",
            "README.md": "# Test",
            "src/main.py": "print('hello')",
            "tests/test_main.py": "def test_main(): pass",
            "config.yaml": "key: value",
        }
    for name, content in files.items():
        p = tmp_path / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
    return tmp_path


# ---------------------------------------------------------------------------
# Path classification (Step 867 / 873)
# ---------------------------------------------------------------------------


class TestPathClassification:

    def test_env_excluded(self):
        assert _is_protected(Path(".env")) is True

    def test_env_local_excluded(self):
        assert _is_protected(Path(".env.local")) is True

    def test_data_dir_excluded(self):
        assert _is_protected(Path(".data/secrets.json")) is True

    def test_git_dir_excluded(self):
        assert _is_protected(Path(".git/config")) is True

    def test_node_modules_excluded(self):
        assert _is_protected(Path("node_modules/foo/index.js")) is True

    def test_normal_file_not_protected(self):
        assert _is_protected(Path("src/main.py")) is False

    def test_binary_unsupported(self):
        assert _is_unsupported(Path("image.png")) is True
        assert _is_unsupported(Path("lib.so")) is True

    def test_pem_unsupported(self):
        assert _is_unsupported(Path("cert.pem")) is True

    def test_python_supported(self):
        assert _is_unsupported(Path("main.py")) is False

    def test_classify_protected_path(self):
        entry = _classify_path(
            Path(".env"), size_bytes=100, is_symlink=False,
            max_bytes=100_000, task_target_paths=frozenset(),
            intent_target_paths=frozenset(),
        )
        assert entry.included is False
        assert entry.reason == "protected_path"
        assert entry.category == "protected"

    def test_classify_unsupported_extension(self):
        entry = _classify_path(
            Path("image.png"), size_bytes=5000, is_symlink=False,
            max_bytes=100_000, task_target_paths=frozenset(),
            intent_target_paths=frozenset(),
        )
        assert entry.included is False
        assert entry.reason == "unsupported_extension"

    def test_classify_symlink_excluded(self):
        entry = _classify_path(
            Path("link.py"), size_bytes=0, is_symlink=True,
            max_bytes=100_000, task_target_paths=frozenset(),
            intent_target_paths=frozenset(),
        )
        assert entry.included is False
        assert entry.reason == "symlink_excluded"

    def test_classify_large_file_excluded(self):
        entry = _classify_path(
            Path("huge.py"), size_bytes=200_000, is_symlink=False,
            max_bytes=100_000, task_target_paths=frozenset(),
            intent_target_paths=frozenset(),
        )
        assert entry.included is False
        assert entry.reason == "over_size_limit"
        assert entry.category == "large"

    def test_classify_path_traversal(self):
        entry = _classify_path(
            Path("../etc/passwd"), size_bytes=100, is_symlink=False,
            max_bytes=100_000, task_target_paths=frozenset(),
            intent_target_paths=frozenset(),
        )
        assert entry.included is False
        assert entry.reason == "path_traversal"

    def test_classify_empty_file(self):
        entry = _classify_path(
            Path("empty.py"), size_bytes=0, is_symlink=False,
            max_bytes=100_000, task_target_paths=frozenset(),
            intent_target_paths=frozenset(),
        )
        assert entry.included is False
        assert entry.reason == "empty_file"

    def test_classify_manifest(self):
        entry = _classify_path(
            Path("pyproject.toml"), size_bytes=500, is_symlink=False,
            max_bytes=100_000, task_target_paths=frozenset(),
            intent_target_paths=frozenset(),
        )
        assert entry.included is True
        assert entry.reason == "manifest_file"
        assert entry.category == "manifest"

    def test_classify_readme(self):
        entry = _classify_path(
            Path("README.md"), size_bytes=200, is_symlink=False,
            max_bytes=100_000, task_target_paths=frozenset(),
            intent_target_paths=frozenset(),
        )
        assert entry.included is True
        assert entry.reason == "documentation_file"
        assert entry.category == "readme"

    def test_classify_task_target(self):
        entry = _classify_path(
            Path("src/auth.py"), size_bytes=1000, is_symlink=False,
            max_bytes=100_000, task_target_paths=frozenset({"src/auth.py"}),
            intent_target_paths=frozenset(),
        )
        assert entry.included is True
        assert entry.reason == "task_target_path"

    def test_classify_intent_target(self):
        entry = _classify_path(
            Path("src/fix.py"), size_bytes=800, is_symlink=False,
            max_bytes=100_000, task_target_paths=frozenset(),
            intent_target_paths=frozenset({"src/fix.py"}),
        )
        assert entry.included is True
        assert entry.reason == "patch_intent_target"

    def test_classify_test_file(self):
        entry = _classify_path(
            Path("tests/test_auth.py"), size_bytes=600, is_symlink=False,
            max_bytes=100_000, task_target_paths=frozenset(),
            intent_target_paths=frozenset(),
        )
        assert entry.included is True
        assert entry.reason == "related_test_file"
        assert entry.category == "test"

    def test_classify_source_file(self):
        entry = _classify_path(
            Path("src/main.py"), size_bytes=400, is_symlink=False,
            max_bytes=100_000, task_target_paths=frozenset(),
            intent_target_paths=frozenset(),
        )
        assert entry.included is True
        assert entry.reason == "source_file"
        assert entry.category == "source"

    def test_classify_config_file(self):
        entry = _classify_path(
            Path("config.yaml"), size_bytes=300, is_symlink=False,
            max_bytes=100_000, task_target_paths=frozenset(),
            intent_target_paths=frozenset(),
        )
        assert entry.included is True
        assert entry.reason == "config_file"
        assert entry.category == "config"


# ---------------------------------------------------------------------------
# Token/budget estimation (Step 869)
# ---------------------------------------------------------------------------


class TestBudgetEstimation:

    def test_within_budget(self):
        included = [
            ContextPathEntry(path="a.py", included=True, reason="source", category="source", size_bytes=400, estimated_tokens=100),
        ]
        budget = _compute_budget(included, 4000)
        assert budget.status == BUDGET_WITHIN
        assert budget.estimated_total_tokens == 100

    def test_near_budget(self):
        included = [
            ContextPathEntry(path="a.py", included=True, reason="source", category="source", size_bytes=14000, estimated_tokens=3500),
        ]
        budget = _compute_budget(included, 4000)
        assert budget.status == BUDGET_NEAR

    def test_over_budget(self):
        included = [
            ContextPathEntry(path="a.py", included=True, reason="source", category="source", size_bytes=20000, estimated_tokens=5000),
        ]
        budget = _compute_budget(included, 4000)
        assert budget.status == BUDGET_OVER

    def test_unknown_budget(self):
        budget = _compute_budget([], 0)
        assert budget.status == BUDGET_UNKNOWN

    def test_token_heuristic(self):
        """Token estimate is ceil(bytes/4)."""
        import math
        entry = _classify_path(
            Path("test.py"), size_bytes=100, is_symlink=False,
            max_bytes=100_000, task_target_paths=frozenset(),
            intent_target_paths=frozenset(),
        )
        assert entry.estimated_tokens == math.ceil(100 / 4)


# ---------------------------------------------------------------------------
# Policy gates (Step 870)
# ---------------------------------------------------------------------------


class TestPolicyGates:

    def test_all_gates_have_status(self):
        from packages.orchestration.context_inspector import _build_policy_gates
        gates = _build_policy_gates()
        assert len(gates) >= 5
        for g in gates:
            assert g.status in ("enforced", "assessed")

    def test_expected_gates_present(self):
        from packages.orchestration.context_inspector import _build_policy_gates
        gates = _build_policy_gates()
        names = {g.name for g in gates}
        assert "protected_paths_enforced" in names
        assert "token_budget_assessed" in names
        assert "raw_content_redaction" in names
        assert "no_shell_true" in names
        assert "no_mutation_from_inspect" in names
        assert "mcp_inactive_by_default" in names


# ---------------------------------------------------------------------------
# Tooling awareness (Step 876)
# ---------------------------------------------------------------------------


class TestToolingAwareness:

    def test_no_repo(self):
        t = _detect_tooling(None)
        assert t.pi_exists is False
        assert t.claude_exists is False
        assert t.mcp_exists is False

    def test_detects_pi_and_claude(self, tmp_path):
        (tmp_path / ".pi").mkdir()
        (tmp_path / ".claude").mkdir()
        t = _detect_tooling(tmp_path)
        assert t.pi_exists is True
        assert t.claude_exists is True

    def test_mcp_active_count(self, tmp_path):
        mcp = tmp_path / ".mcp.json"
        mcp.write_text(json.dumps({
            "mcpServers": {
                "active": {"command": "node"},
                "disabled": {"command": "node", "disabled": True},
            }
        }))
        t = _detect_tooling(tmp_path)
        assert t.mcp_exists is True
        assert t.mcp_active_servers == 1

    def test_mcp_empty_servers(self, tmp_path):
        mcp = tmp_path / ".mcp.json"
        mcp.write_text(json.dumps({"mcpServers": {}}))
        t = _detect_tooling(tmp_path)
        assert t.mcp_exists is True
        assert t.mcp_active_servers == 0

    def test_tooling_does_not_dump_content(self, tmp_path):
        """Tooling detection must not leak config content."""
        (tmp_path / ".pi").mkdir()
        (tmp_path / ".claude").mkdir()
        mcp = tmp_path / ".mcp.json"
        mcp.write_text(json.dumps({"mcpServers": {"s": {"command": "secret-binary", "args": ["--token=abc"]}}}))
        t = _detect_tooling(tmp_path)
        # Only boolean/count fields — no content
        assert isinstance(t.mcp_active_servers, int)
        assert not hasattr(t, "content")
        assert not hasattr(t, "config")


# ---------------------------------------------------------------------------
# Full inspection (Steps 871, 874)
# ---------------------------------------------------------------------------


class TestInspectContext:

    def test_empty_job_no_repo(self):
        job = _make_job()
        inspection = inspect_context(job, [])
        assert inspection.readiness.status == READINESS_BLOCKED
        assert "no_included_files" in inspection.readiness.blockers
        assert "repo_root_unknown" in inspection.missing_context

    def test_with_repo(self, tmp_path):
        repo = _make_repo(tmp_path)
        job = _make_job()
        inspection = inspect_context(job, [], repo_root=repo)
        assert len(inspection.included_paths) > 0
        assert inspection.readiness.status in (READINESS_READY, READINESS_WARNINGS)
        # Check manifest included
        manifests = [p for p in inspection.included_paths if p.category == "manifest"]
        assert len(manifests) >= 1

    def test_protected_files_excluded(self, tmp_path):
        repo = _make_repo(tmp_path, {
            "pyproject.toml": "[project]",
            ".env": "SECRET=abc123",
            ".env.local": "DB=postgres",
            "src/main.py": "x = 1",
        })
        job = _make_job()
        inspection = inspect_context(job, [], repo_root=repo)
        excluded_paths = {p.path for p in inspection.excluded_paths}
        assert ".env" in excluded_paths
        assert ".env.local" in excluded_paths
        assert ".env" in inspection.protected_paths

    def test_binary_excluded(self, tmp_path):
        repo = _make_repo(tmp_path, {"pyproject.toml": "x", "image.png": "\x89PNG"})
        # Write actual binary
        (tmp_path / "image.png").write_bytes(b"\x89PNG\r\n")
        job = _make_job()
        inspection = inspect_context(job, [], repo_root=repo)
        unsupported = {p.path for p in inspection.excluded_paths}
        assert "image.png" in unsupported

    def test_node_modules_excluded(self, tmp_path):
        repo = _make_repo(tmp_path, {
            "pyproject.toml": "x",
            "node_modules/foo/index.js": "module.exports = {}",
        })
        job = _make_job()
        inspection = inspect_context(job, [], repo_root=repo)
        excluded_paths = {p.path for p in inspection.excluded_paths}
        assert any("node_modules" in p for p in excluded_paths)

    def test_task_target_included(self, tmp_path):
        repo = _make_repo(tmp_path, {
            "pyproject.toml": "x",
            "src/auth.py": "def auth(): pass",
        })
        task = Task(description="Fix auth bug", inputs={"target_path": "src/auth.py"})
        job = _make_job(tasks=[task])
        inspection = inspect_context(job, [], repo_root=repo)
        included_paths = {p.path for p in inspection.included_paths}
        assert "src/auth.py" in included_paths

    def test_intent_target_included(self, tmp_path):
        repo = _make_repo(tmp_path, {
            "pyproject.toml": "x",
            "src/fix.py": "def fix(): pass",
        })
        task = Task(description="Fix bug")
        art = Artifact(
            name="patch-intent", content="", kind=ArtifactKind.PATCH_INTENT,
            task_id=task.id,
            metadata={
                "patch_intent_explanations": [{"file": "src/fix.py", "action": "modify", "risk": "low"}],
                "patch_intent_approvals": {},
            },
        )
        job = _make_job(tasks=[task], artifacts=[art])
        inspection = inspect_context(job, [], repo_root=repo)
        included_paths = {p.path for p in inspection.included_paths}
        assert "src/fix.py" in included_paths

    def test_related_tests_included(self, tmp_path):
        repo = _make_repo(tmp_path, {
            "pyproject.toml": "x",
            "tests/test_auth.py": "def test_auth(): pass",
        })
        job = _make_job()
        inspection = inspect_context(job, [], repo_root=repo)
        test_paths = [p for p in inspection.included_paths if p.category == "test"]
        assert len(test_paths) >= 1

    def test_agents_md_included(self, tmp_path):
        repo = _make_repo(tmp_path, {
            "pyproject.toml": "x",
            "AGENTS.md": "# Agent rules",
        })
        job = _make_job()
        inspection = inspect_context(job, [], repo_root=repo)
        included_paths = {p.path for p in inspection.included_paths}
        assert "AGENTS.md" in included_paths

    def test_task_id_filter(self, tmp_path):
        """task_id accepted without crash."""
        repo = _make_repo(tmp_path)
        task = Task(description="Task")
        job = _make_job(tasks=[task])
        inspection = inspect_context(job, [], task_id=str(task.id), repo_root=repo)
        assert inspection.task_id == str(task.id)

    def test_budget_respected(self, tmp_path):
        repo = _make_repo(tmp_path, {
            "pyproject.toml": "x" * 1000,
            "src/a.py": "y" * 50000,
            "src/b.py": "z" * 50000,
        })
        job = _make_job()
        inspection = inspect_context(job, [], repo_root=repo, budget_tokens=100)
        assert inspection.budget.status in (BUDGET_NEAR, BUDGET_OVER, BUDGET_WITHIN)

    def test_tooling_detected(self, tmp_path):
        repo = _make_repo(tmp_path, {"pyproject.toml": "x"})
        (tmp_path / ".pi").mkdir()
        (tmp_path / ".claude").mkdir()
        job = _make_job()
        inspection = inspect_context(job, [], repo_root=repo)
        assert inspection.tooling.pi_exists is True
        assert inspection.tooling.claude_exists is True

    def test_generated_at(self, tmp_path):
        repo = _make_repo(tmp_path)
        job = _make_job()
        inspection = inspect_context(job, [], repo_root=repo)
        assert inspection.generated_at


# ---------------------------------------------------------------------------
# Redaction (Step 873)
# ---------------------------------------------------------------------------


class TestRedaction:

    def test_no_raw_source_content(self, tmp_path):
        repo = _make_repo(tmp_path, {
            "pyproject.toml": "SECRET_KEY = 'abc123'",
            "src/main.py": "password = 'hunter2'",
        })
        job = _make_job()
        inspection = inspect_context(job, [], repo_root=repo)
        data = export_context_inspection_json(inspection)
        text = json.dumps(data)
        assert "SECRET_KEY" not in text
        assert "abc123" not in text
        assert "hunter2" not in text
        assert "password" not in text

    def test_no_file_bodies(self, tmp_path):
        repo = _make_repo(tmp_path, {"pyproject.toml": "lots of content here\n" * 100})
        job = _make_job()
        inspection = inspect_context(job, [], repo_root=repo)
        data = export_context_inspection_json(inspection)
        text = json.dumps(data)
        assert "lots of content here" not in text

    def test_no_mcp_config_content(self, tmp_path):
        repo = _make_repo(tmp_path, {"pyproject.toml": "x"})
        mcp = tmp_path / ".mcp.json"
        mcp.write_text(json.dumps({"mcpServers": {"s": {"command": "secret-cmd", "args": ["--key=TOKEN"]}}}))
        job = _make_job()
        inspection = inspect_context(job, [], repo_root=repo)
        data = export_context_inspection_json(inspection)
        text = json.dumps(data)
        assert "secret-cmd" not in text
        assert "TOKEN" not in text

    def test_no_stdout_stderr(self, tmp_path):
        repo = _make_repo(tmp_path)
        job = _make_job()
        inspection = inspect_context(job, [], repo_root=repo)
        data = export_context_inspection_json(inspection)
        # Check JSON keys — no stdout/stderr keys anywhere in structure
        def _all_keys(d):
            if isinstance(d, dict):
                for k, v in d.items():
                    yield k
                    yield from _all_keys(v)
            elif isinstance(d, list):
                for item in d:
                    yield from _all_keys(item)
        keys = set(_all_keys(data))
        assert "stdout" not in keys
        assert "stderr" not in keys

    def test_no_diff_key(self, tmp_path):
        repo = _make_repo(tmp_path)
        job = _make_job()
        inspection = inspect_context(job, [], repo_root=repo)
        data = export_context_inspection_json(inspection)
        def _all_keys(d):
            if isinstance(d, dict):
                for k, v in d.items():
                    yield k
                    yield from _all_keys(v)
            elif isinstance(d, list):
                for item in d:
                    yield from _all_keys(item)
        keys = set(_all_keys(data))
        assert "diff" not in keys

    def test_no_traceback_key(self, tmp_path):
        repo = _make_repo(tmp_path)
        job = _make_job()
        inspection = inspect_context(job, [], repo_root=repo)
        data = export_context_inspection_json(inspection)
        def _all_keys(d):
            if isinstance(d, dict):
                for k, v in d.items():
                    yield k
                    yield from _all_keys(v)
            elif isinstance(d, list):
                for item in d:
                    yield from _all_keys(item)
        keys = set(_all_keys(data))
        assert "traceback" not in keys

    def test_no_absolute_home_path(self, tmp_path):
        repo = _make_repo(tmp_path)
        job = _make_job()
        inspection = inspect_context(job, [], repo_root=repo)
        data = export_context_inspection_json(inspection)
        # repo_root_safe should be basename, not absolute
        assert not data["repo_root_safe"].startswith("/")
        # No absolute paths in included/excluded
        for p in data["included_paths"] + data["excluded_paths"]:
            assert not p["path"].startswith("/")

    def test_output_bounded(self, tmp_path):
        repo = _make_repo(tmp_path)
        job = _make_job()
        inspection = inspect_context(job, [], repo_root=repo)
        text = summarize_context_inspection(inspection)
        assert len(text) < 10000


# ---------------------------------------------------------------------------
# JSON export stability
# ---------------------------------------------------------------------------


class TestJsonExport:

    def test_json_roundtrip(self, tmp_path):
        repo = _make_repo(tmp_path)
        job = _make_job()
        inspection = inspect_context(job, [], repo_root=repo)
        data = export_context_inspection_json(inspection)
        text = json.dumps(data, sort_keys=True)
        data2 = json.loads(text)
        assert data2["version"] == 1
        assert "included_paths" in data2
        assert "excluded_paths" in data2
        assert "budget" in data2
        assert "policy_gates" in data2
        assert "tooling" in data2
        assert "readiness" in data2

    def test_json_has_all_fields(self, tmp_path):
        repo = _make_repo(tmp_path)
        job = _make_job()
        inspection = inspect_context(job, [], repo_root=repo)
        data = export_context_inspection_json(inspection)
        for field in (
            "version", "job_id", "task_id", "repo_root_safe",
            "included_paths", "excluded_paths", "protected_paths",
            "unsupported_paths", "budget", "policy_gates", "tooling",
            "readiness", "missing_context", "generated_at",
        ):
            assert field in data, f"Missing field: {field}"


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------


class TestSummary:

    def test_summary_contains_readiness(self, tmp_path):
        repo = _make_repo(tmp_path)
        job = _make_job()
        inspection = inspect_context(job, [], repo_root=repo)
        text = summarize_context_inspection(inspection)
        assert "Readiness:" in text
        assert "Budget:" in text
        assert "Policy Gates" in text

    def test_summary_shows_tooling(self, tmp_path):
        repo = _make_repo(tmp_path)
        (tmp_path / ".pi").mkdir()
        job = _make_job()
        inspection = inspect_context(job, [], repo_root=repo)
        text = summarize_context_inspection(inspection)
        assert ".pi" in text

    def test_summary_empty_job(self):
        job = _make_job()
        inspection = inspect_context(job, [])
        text = summarize_context_inspection(inspection)
        assert "blocked" in text.lower() or "no_included_files" in text


# ---------------------------------------------------------------------------
# Truth closure tests (Steps 881-890)
# ---------------------------------------------------------------------------


class TestEnvProtectionHardened:
    """Step 881: .env.* generic protection."""

    def test_env_exact(self):
        assert _is_protected(Path(".env")) is True

    def test_env_local(self):
        assert _is_protected(Path(".env.local")) is True

    def test_env_custom_suffix(self):
        """Any .env.* pattern is protected, not just named ones."""
        assert _is_protected(Path(".env.custom")) is True
        assert _is_protected(Path(".env.myapp")) is True
        assert _is_protected(Path(".env.ci")) is True

    def test_env_in_subdirectory(self):
        assert _is_protected(Path("config/.env.staging")) is True

    def test_env_not_false_positive(self):
        """Files that start with .env but aren't dotenv files."""
        assert _is_protected(Path("environment.py")) is False
        assert _is_protected(Path(".envrc")) is False


class TestPathTraversalFixed:
    """Step 882: Segment-based traversal, no false positives."""

    def test_actual_traversal(self):
        assert _is_path_traversal("../etc/passwd") is True

    def test_traversal_mid_path(self):
        assert _is_path_traversal("src/../../etc/passwd") is True

    def test_absolute_path(self):
        assert _is_path_traversal("/etc/passwd") is True

    def test_no_false_positive_dotdot_in_name(self):
        """Filenames containing '..' are NOT traversal."""
        assert _is_path_traversal("src/file..bak.py") is False
        assert _is_path_traversal("lib/v2..3/main.py") is False

    def test_normal_path_safe(self):
        assert _is_path_traversal("src/main.py") is False


class TestEventTargetPaths:
    """Step 884: Extract target paths from events."""

    def test_extracts_target_path_from_event(self):
        events = [
            {"event": "patch_intent_created", "metadata": {"target_path": "src/auth.py"}},
        ]
        paths = _collect_event_target_paths(events)
        assert "src/auth.py" in paths

    def test_skips_traversal_in_events(self):
        events = [
            {"event": "x", "metadata": {"target_path": "../etc/passwd"}},
        ]
        paths = _collect_event_target_paths(events)
        assert len(paths) == 0

    def test_empty_events(self):
        assert _collect_event_target_paths([]) == frozenset()

    def test_event_without_metadata(self):
        events = [{"event": "something"}]
        paths = _collect_event_target_paths(events)
        assert len(paths) == 0

    def test_event_target_classified(self, tmp_path):
        """Event targets appear as included with reason event_target_path."""
        repo = _make_repo(tmp_path, {
            "pyproject.toml": "x",
            "src/changed.py": "# changed",
        })
        events = [{"event": "patch_applied", "metadata": {"target_path": "src/changed.py"}}]
        job = _make_job()
        inspection = inspect_context(job, events, repo_root=repo)
        included = {p.path: p for p in inspection.included_paths}
        assert "src/changed.py" in included
        assert included["src/changed.py"].reason == "event_target_path"


class TestBudgetTruth:
    """Step 886: Budget gate is assessed, not enforced."""

    def test_budget_gate_is_assessed(self):
        from packages.orchestration.context_inspector import _build_policy_gates
        gates = {g.name: g for g in _build_policy_gates()}
        bg = gates["token_budget_assessed"]
        assert bg.status == "assessed"
        assert "trimming" not in bg.reason.lower() or "no" in bg.reason.lower()

    def test_over_budget_no_automatic_exclusion(self, tmp_path):
        """Over-budget files still included — budget is reported, not enforced."""
        repo = _make_repo(tmp_path, {
            "pyproject.toml": "x",
            "src/big.py": "y" * 80000,
        })
        job = _make_job()
        inspection = inspect_context(job, [], repo_root=repo, budget_tokens=100)
        assert inspection.budget.status == BUDGET_OVER
        included_paths = {p.path for p in inspection.included_paths}
        assert "src/big.py" in included_paths


class TestStableSorting:
    """Step 887: Deterministic sort with target priority."""

    def test_targets_before_generic_source(self, tmp_path):
        repo = _make_repo(tmp_path, {
            "pyproject.toml": "x",
            "src/alpha.py": "a = 1",
            "src/target.py": "t = 1",
            "src/zebra.py": "z = 1",
        })
        task = Task(description="Fix", inputs={"target_path": "src/target.py"})
        job = _make_job(tasks=[task])
        inspection = inspect_context(job, [], repo_root=repo)
        source_paths = [p for p in inspection.included_paths if p.category == "source"]
        source_order = [p.path for p in source_paths]
        # Target should come before generic source files
        assert source_order.index("src/target.py") < source_order.index("src/alpha.py")

    def test_sort_is_deterministic(self, tmp_path):
        repo = _make_repo(tmp_path)
        job = _make_job()
        i1 = inspect_context(job, [], repo_root=repo)
        i2 = inspect_context(job, [], repo_root=repo)
        assert [p.path for p in i1.included_paths] == [p.path for p in i2.included_paths]


class TestJsonContractSnapshot:
    """Step 889: JSON output has stable schema."""

    def test_json_top_level_keys(self, tmp_path):
        repo = _make_repo(tmp_path)
        job = _make_job()
        inspection = inspect_context(job, [], repo_root=repo)
        data = export_context_inspection_json(inspection)
        expected_keys = {
            "version", "job_id", "task_id", "repo_root_safe",
            "included_paths", "excluded_paths", "protected_paths",
            "unsupported_paths", "budget", "policy_gates", "tooling",
            "readiness", "missing_context", "generated_at",
        }
        assert set(data.keys()) == expected_keys

    def test_json_budget_keys(self, tmp_path):
        repo = _make_repo(tmp_path)
        job = _make_job()
        inspection = inspect_context(job, [], repo_root=repo)
        data = export_context_inspection_json(inspection)
        budget_keys = {"limit_tokens", "estimated_total_tokens", "estimated_total_bytes", "status", "file_count"}
        assert set(data["budget"].keys()) == budget_keys

    def test_json_path_entry_keys(self, tmp_path):
        repo = _make_repo(tmp_path)
        job = _make_job()
        inspection = inspect_context(job, [], repo_root=repo)
        data = export_context_inspection_json(inspection)
        for p in data["included_paths"]:
            assert "path" in p
            assert "included" in p
            assert "reason" in p
            assert "category" in p

    def test_json_tooling_keys(self, tmp_path):
        repo = _make_repo(tmp_path)
        job = _make_job()
        inspection = inspect_context(job, [], repo_root=repo)
        data = export_context_inspection_json(inspection)
        tooling_keys = {"pi_exists", "claude_exists", "mcp_exists", "mcp_active_servers", "vscode_mcp_exists", "vscode_mcp_active_servers"}
        assert set(data["tooling"].keys()) == tooling_keys


class TestCliTextHonesty:
    """Step 890: Summary text doesn't overclaim."""

    def test_no_enforced_budget_claim(self, tmp_path):
        repo = _make_repo(tmp_path)
        job = _make_job()
        inspection = inspect_context(job, [], repo_root=repo)
        text = summarize_context_inspection(inspection)
        # Budget gate should show "assessed" not "enforced"
        assert "[assessed] token_budget_assessed" in text

    def test_summary_has_budget_status(self, tmp_path):
        repo = _make_repo(tmp_path)
        job = _make_job()
        inspection = inspect_context(job, [], repo_root=repo)
        text = summarize_context_inspection(inspection)
        assert "Budget:" in text
        assert "tokens" in text
