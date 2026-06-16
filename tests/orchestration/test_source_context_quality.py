"""Tests: source context quality for real builder runs."""
from __future__ import annotations

from tests.orchestration.small_repo_fixtures import (
    create_missing_function_repo,
    create_repair_scenario_repo,
)


class TestSourceContextSelection:
    def test_missing_function_repo_selects_test_and_source(self, tmp_path):
        from packages.orchestration.source_context import select_relevant_files
        repo = create_missing_function_repo(tmp_path / "repo")
        files = select_relevant_files(repo, budget=4000)
        paths = [f.path for f in files]
        categories = [f.category for f in files]
        assert any("test_app" in p for p in paths), f"No test file selected: {paths}"
        assert any("app.py" in p for p in paths), f"No source file selected: {paths}"
        assert "test" in categories
        assert "source" in categories

    def test_repair_repo_selects_calc_and_test(self, tmp_path):
        from packages.orchestration.source_context import select_relevant_files
        repo = create_repair_scenario_repo(tmp_path / "repo")
        files = select_relevant_files(repo, budget=4000)
        paths = [f.path for f in files]
        assert any("calc.py" in p for p in paths)
        assert any("test_calc" in p for p in paths)


class TestSourceContextBudget:
    def test_budget_truncates_deterministically(self, tmp_path):
        from packages.orchestration.source_context import select_relevant_files
        repo = create_missing_function_repo(tmp_path / "repo")
        # Add extra files to push past budget
        for i in range(20):
            (repo / f"module_{i}.py").write_text(f"x = {i}\n" * 100, encoding="utf-8")

        files_small = select_relevant_files(repo, budget=200)
        files_large = select_relevant_files(repo, budget=4000)
        assert len(files_small) <= len(files_large)
        total_small = sum(f.estimated_tokens for f in files_small)
        assert total_small <= 200

    def test_same_repo_same_selection(self, tmp_path):
        from packages.core.models import Job
        from packages.orchestration.source_context import inject_source_context
        repo = create_missing_function_repo(tmp_path / "repo")
        job1 = Job(name="test1")
        job2 = Job(name="test2")
        ctx1 = inject_source_context(job1, repo, budget=4000)
        ctx2 = inject_source_context(job2, repo, budget=4000)
        assert ctx1.selection_hash == ctx2.selection_hash
        assert ctx1.file_count == ctx2.file_count


class TestSourceContextRedaction:
    def test_secret_like_files_excluded(self, tmp_path):
        from packages.orchestration.source_context import select_relevant_files
        repo = create_missing_function_repo(tmp_path / "repo")
        (repo / ".env").write_text("SECRET=abc123\n", encoding="utf-8")
        (repo / "creds.pem").write_text("-----BEGIN CERTIFICATE-----\n", encoding="utf-8")
        files = select_relevant_files(repo, budget=4000)
        paths = [f.path for f in files]
        assert not any(".env" in p for p in paths)
        assert not any(".pem" in p for p in paths)


class TestSourceContextMetadata:
    def test_inject_records_safe_metadata(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.core.models import Job
        from packages.orchestration.source_context import inject_source_context
        from packages.orchestration.timeline import load_run_events

        repo = create_missing_function_repo(tmp_path / "repo")
        job = Job(name="test")
        ctx = inject_source_context(job, repo, data_dir=str(tmp_path / "data"))

        assert ctx.file_count > 0
        assert ctx.estimated_tokens > 0
        assert ctx.selection_hash != ""
        assert ctx.mode == "compact"

        events = load_run_events(tmp_path / "data", job.id)
        inject_events = [e for e in events if e["event"] == "source_context_injected"]
        assert len(inject_events) == 1
        meta = inject_events[0]["metadata"]
        assert "file_count" in meta
        assert "selection_hash" in meta
        assert "estimated_tokens" in meta
        # No raw file content in events
        for key, val in meta.items():
            if isinstance(val, str):
                assert "def hello" not in val
                assert "def add" not in val

    def test_no_raw_content_in_run_log(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.core.models import Job
        from packages.orchestration.source_context import inject_source_context
        from packages.orchestration.timeline import load_run_events

        repo = create_repair_scenario_repo(tmp_path / "repo")
        job = Job(name="test")
        inject_source_context(job, repo, data_dir=str(tmp_path / "data"))
        events = load_run_events(tmp_path / "data", job.id)
        for event in events:
            event_str = str(event)
            assert "return a - b" not in event_str
            assert "return a + b" not in event_str
