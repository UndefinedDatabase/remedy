"""F266 T001 — Bounded repository study pass tests."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from packages.memory.local_gateway import list_memory
from packages.orchestration.study import _walk_repo, run_study, study_call_fn


def _hash_tree(root: Path) -> dict[str, str]:
    """Every file under root, mapped to sha256 of its bytes."""
    return {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


class TestStudyBasic:
    """Basic study functionality."""

    def test_run_study_writes_four_category_cards(self, tmp_path, monkeypatch) -> None:
        """Study writes four cards with correct provenance and auto-approval."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / ".remedy_data"))

        # Build fixture repo
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "README.md").write_text("# Example\n")
        (repo / "pyproject.toml").write_text("[project]\n")
        (repo / "src").mkdir()
        (repo / "src" / "main.py").write_text("print('hello')\n")
        (repo / "tests").mkdir()
        (repo / "tests" / "test_main.py").write_text("def test_it(): pass\n")

        # Run study with no call_fn
        result = run_study(str(repo), project_id="p1", call_fn=None)

        # Assert four cards written
        assert len(result.cards_written) == 4
        assert result.partial is False
        assert result.stopped_reason is None

        # Read cards back and verify provenance + approval
        cards = list_memory(project_id="p1", job_id=result.job_id)
        assert len(cards) == 4

        for card in cards:
            assert card.provenance == "machine-study"
            assert card.approved is True
            assert card.key.startswith("study:")

        # Verify all four categories present
        keys = {card.key for card in cards}
        assert "study:structure" in keys
        assert "study:core_modules" in keys
        assert "study:conventions" in keys
        assert "study:entry_points" in keys

    def test_run_study_respects_entry_cap_and_reports_partial(
        self, tmp_path, monkeypatch
    ) -> None:
        """Study respects max_entries cap and marks result as partial."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / ".remedy_data"))

        # Build fixture with more files than cap
        repo = tmp_path / "repo"
        repo.mkdir()
        for i in range(15):
            (repo / f"file_{i}.txt").write_text(f"content {i}\n")

        # Run with small cap
        result = run_study(str(repo), project_id="p1", max_entries=3)

        # Assert partial and cap reason
        assert result.partial is True
        assert "entry_cap_reached:3" in result.stopped_reason

        # Still assert 4 cards written (partial structure, not zero)
        cards = list_memory(project_id="p1", job_id=result.job_id)
        assert len(cards) == 4

    def test_run_study_is_read_only_against_studied_repo(
        self, tmp_path, monkeypatch
    ) -> None:
        """Study is read-only: repo must be identical before and after."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / ".remedy_data"))

        # Build fixture
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "README.md").write_text("# Test\n")
        (repo / "src").mkdir()
        (repo / "src" / "lib.py").write_text("def func(): pass\n")
        (repo / "tests").mkdir()
        (repo / "tests" / "test_lib.py").write_text("def test(): pass\n")

        # Hash before
        hash_before = _hash_tree(repo)

        # Run study
        result = run_study(str(repo), project_id="p1", call_fn=None)

        # Hash after
        hash_after = _hash_tree(repo)

        # Assert identical
        assert hash_before == hash_after
        assert len(result.cards_written) == 4

    def test_run_study_respects_provider_call_budget_and_falls_back_honestly(
        self, tmp_path, monkeypatch
    ) -> None:
        """Study respects max_provider_calls budget and uses heuristic fallback."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / ".remedy_data"))

        # Build fixture
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "README.md").write_text("# Test\n")
        (repo / "pyproject.toml").write_text("[project]\n")

        # call_fn that counts invocations
        call_count = [0]

        def counting_call_fn(prompt: str, max_tokens: int) -> str:
            call_count[0] += 1
            return f"narrated {call_count[0]}"

        # Run with budget of 2 calls
        result = run_study(
            str(repo),
            project_id="p1",
            call_fn=counting_call_fn,
            max_provider_calls=2,
        )

        # Assert budget was respected (at most 2 calls)
        assert call_count[0] <= 2

        # Assert partial and budget reason
        assert result.partial is True
        assert "budget_exhausted" in result.stopped_reason or "provider_calls" in result.stopped_reason

        # Assert all 4 cards written
        cards = list_memory(project_id="p1", job_id=result.job_id)
        assert len(cards) == 4

    def test_run_study_call_fn_exception_falls_back_to_heuristic(
        self, tmp_path, monkeypatch
    ) -> None:
        """Study handles call_fn exceptions and falls back to heuristic."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / ".remedy_data"))

        # Build fixture
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "README.md").write_text("# Test\n")
        (repo / "src").mkdir()
        (repo / "src" / "module.py").write_text("def func(): pass\n")
        (repo / "tests").mkdir()

        # call_fn that always raises
        def raising_call_fn(prompt: str, max_tokens: int) -> str:
            raise RuntimeError("boom")

        # Run with exception-raising call_fn
        result_exception = run_study(
            str(repo),
            project_id="p1_exc",
            call_fn=raising_call_fn,
        )

        # Run without call_fn (pure heuristic)
        result_heuristic = run_study(
            str(repo),
            project_id="p1_heur",
            call_fn=None,
        )

        # Read both sets of cards
        cards_exc = list_memory(project_id="p1_exc", job_id=result_exception.job_id)
        cards_heur = list_memory(project_id="p1_heur", job_id=result_heuristic.job_id)

        # Assert 4 cards in both cases
        assert len(cards_exc) == 4
        assert len(cards_heur) == 4

        # Sort by key and compare values
        cards_exc_sorted = sorted(cards_exc, key=lambda c: c.key)
        cards_heur_sorted = sorted(cards_heur, key=lambda c: c.key)

        for exc_card, heur_card in zip(cards_exc_sorted, cards_heur_sorted):
            assert exc_card.key == heur_card.key
            # When exception occurs, should fall back to exact same heuristic
            assert exc_card.value == heur_card.value

    def test_walk_repo_preserves_root_dotfile_names(self, tmp_path) -> None:
        """Root-level dotfiles are returned with leading dot intact (R-0958 regression)."""
        # Build fixture with a root-level .gitignore and README.md
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / ".gitignore").write_text("*.pyc\n")
        (repo / "README.md").write_text("# Example\n")

        # Walk the repo
        dirs, files, hit_cap = _walk_repo(str(repo), max_entries=2000)

        # Assert .gitignore is in files with its leading dot intact
        assert ".gitignore" in files
        assert "gitignore" not in files
        assert "README.md" in files
        assert not hit_cap

    def test_study_call_fn_returns_none_without_ollama(self) -> None:
        """study_call_fn returns None when Ollama is not available."""
        # tests/conftest.py::_no_live_ollama_reach (autouse) already refuses
        # a live Ollama connection for every unmarked test.
        assert study_call_fn() is None

    def test_study_call_fn_returns_callable_and_extracts_narrative(self, monkeypatch) -> None:
        """study_call_fn returns callable that extracts narrative from JSON."""
        import sys
        import types

        fake_ollama = types.ModuleType("ollama")

        class FakeClient:
            def __init__(self, host=None):
                pass

            def list(self):
                return []

            def chat(self, **kwargs):
                content = json.dumps({"narrative": "a test narrative"})
                msg = types.SimpleNamespace(content=content)
                return types.SimpleNamespace(message=msg)

        fake_ollama.Client = FakeClient
        monkeypatch.setitem(sys.modules, "ollama", fake_ollama)

        fn = study_call_fn()
        assert fn is not None
        result = fn("test prompt", 0)
        assert result == "a test narrative"


def _git_repo_with_one_commit(root: Path) -> tuple[Path, str]:
    """A git repository holding one committed file, and its HEAD commit id."""
    import subprocess

    root.mkdir()
    def git(*args: str) -> str:
        return subprocess.run(["git", *args], cwd=str(root), capture_output=True,
                              text=True, check=True).stdout.strip()
    git("init", "-q")
    git("config", "user.email", "t@e.com")
    git("config", "user.name", "T")
    git("config", "commit.gpgsign", "false")
    (root / "README.md").write_text("# r\n")
    git("add", "-A")
    git("commit", "-qm", "init")
    return root, git("rev-parse", "HEAD")


class TestRecordStudyPass:
    """DECISION F268 D3 — the one writer of `studied_at` / `studied_head`."""

    def test_writes_both_fields_on_the_saved_project_record(self, tmp_path, monkeypatch) -> None:
        from datetime import datetime, timezone

        from packages.orchestration.project_registry import (
            load_project,
            register_project_repo,
        )
        from packages.orchestration.study import record_study_pass

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        repo, head = _git_repo_with_one_commit(tmp_path / "repo")
        project = register_project_repo("repo", repo)
        now = datetime(2026, 9, 18, 12, 0, tzinfo=timezone.utc)

        returned = record_study_pass(str(project.id), str(repo), now=now)

        saved = load_project(project.id)
        assert saved.metadata["studied_at"] == "2026-09-18T12:00:00+00:00"
        assert saved.metadata["studied_head"] == head
        assert returned is not None
        assert returned.metadata == saved.metadata

    def test_a_repository_without_head_records_an_empty_head(self, tmp_path, monkeypatch) -> None:
        from packages.orchestration.project_registry import RemyProject, load_project, save_project
        from packages.orchestration.study import record_study_pass

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        plain = tmp_path / "plain"
        plain.mkdir()
        project = RemyProject(name="plain", slug="plain")
        save_project(project)

        record_study_pass(str(project.id), str(plain))

        saved = load_project(project.id)
        assert saved.metadata["studied_head"] == ""
        assert saved.metadata["studied_at"]

    def test_an_unregistered_project_id_writes_nothing(self, tmp_path, monkeypatch) -> None:
        from packages.orchestration.study import record_study_pass

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))

        assert record_study_pass(str(tmp_path / "not-a-uuid"), str(tmp_path)) is None
        assert record_study_pass("00000000-0000-0000-0000-000000000042", str(tmp_path)) is None
        assert not (tmp_path / "data" / "projects").exists()
