"""F258 T002 — tests for running a planned self-use item to the approval gate.

The load-bearing tests here are
:meth:`TestRunNextSelfUseItem.test_it_runs_the_planned_item_to_completion`,
which pins that a real run happens (not merely a plan), and
:meth:`TestRunNextSelfUseItem.test_a_blocked_plan_raises_rather_than_running`,
which pins that a curation defect is refused loudly rather than run anyway.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from packages.orchestration.pingpong_job import JOB_COMPLETED
from packages.orchestration.pingpong_provider import FakeProvider
from packages.orchestration.role_config import RoleConfig
from packages.orchestration.self_use_runner import SelfUseRunError, run_next_self_use_item
import packages.orchestration.self_use_runner as self_use_runner

_PENDING_ITEM = {
    "id": "SU-042",
    "title": "A curated item",
    "why": "Because the track must run on something.",
    "job_markdown": (
        "# Job: Demo\n\n## Task 1\nDo the thing.\n\nAcceptance:\n- it is done\n"
    ),
    "consumed_by": "",
    "provenance": "operator-curated (fixture)",
}

_BLOCKED_ITEM = {
    "id": "SU-043",
    "title": "A malformed item",
    "why": "Because a curation defect must be caught, not run.",
    "job_markdown": "# Job: Empty job\n\nThis file has no task headings.\n",
    "consumed_by": "",
    "provenance": "operator-curated (fixture)",
}


def _pass_provider() -> FakeProvider:
    return FakeProvider(pass_on_round=1, fail_on_round=99)


@pytest.fixture
def isolate_data_root(tmp_path: Path, monkeypatch) -> Path:
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=str(repo), capture_output=True, text=True, check=True
    ).stdout


@pytest.fixture
def demo_repo(tmp_path: Path) -> Path:
    """A real git repo, so the run takes the ISOLATED WORKTREE path (T002's own words)."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@e.com")
    _git(repo, "config", "user.name", "T")
    _git(repo, "config", "commit.gpgsign", "false")
    (repo / "README.md").write_text("# Demo\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "init")
    return repo


def _write_queue(tmp_path: Path, items: list[dict]) -> Path:
    path = tmp_path / "self_use_queue.json"
    body = {"schema_version": 2, "description": "fixture queue", "items": items}
    path.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
    return path


class TestRunNextSelfUseItem:
    """Planning happens once, running happens once, promotion never happens."""

    def test_it_runs_the_planned_item_to_completion(self, tmp_path, isolate_data_root, demo_repo):
        queue_path = _write_queue(tmp_path, [dict(_PENDING_ITEM)])
        entry, job_file_path, result = run_next_self_use_item(
            tmp_path / "jobs",
            str(demo_repo),
            queue_path=queue_path,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
        )
        assert entry.id == "SU-042"
        assert job_file_path.exists()
        assert result.status == JOB_COMPLETED
        assert result.isolation_mode == "worktree"

    def test_it_attaches_the_small_budget(self, tmp_path, isolate_data_root, demo_repo):
        queue_path = _write_queue(tmp_path, [dict(_PENDING_ITEM)])
        _entry, _path, result = run_next_self_use_item(
            tmp_path / "jobs",
            str(demo_repo),
            queue_path=queue_path,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
        )
        assert result.budgets["max_provider_calls"] == 6
        assert result.budgets["max_cost_usd"] == 0.50

    def test_it_never_mutates_the_target_repo(self, tmp_path, isolate_data_root, demo_repo):
        queue_path = _write_queue(tmp_path, [dict(_PENDING_ITEM)])
        before = _git(demo_repo, "status", "--porcelain")
        run_next_self_use_item(
            tmp_path / "jobs",
            str(demo_repo),
            queue_path=queue_path,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
        )
        after = _git(demo_repo, "status", "--porcelain")
        assert before == after == ""

    def test_it_never_marks_the_queue_item_consumed(self, tmp_path, isolate_data_root, demo_repo):
        queue_path = _write_queue(tmp_path, [dict(_PENDING_ITEM)])
        before = queue_path.read_text(encoding="utf-8")
        run_next_self_use_item(
            tmp_path / "jobs",
            str(demo_repo),
            queue_path=queue_path,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
        )
        assert queue_path.read_text(encoding="utf-8") == before

    def test_a_blocked_plan_raises_rather_than_running(self, tmp_path, isolate_data_root, demo_repo):
        queue_path = _write_queue(tmp_path, [dict(_BLOCKED_ITEM)])
        with pytest.raises(SelfUseRunError) as excinfo:
            run_next_self_use_item(tmp_path / "jobs", str(demo_repo), queue_path=queue_path)
        assert "SU-043" in str(excinfo.value)

    def test_an_exhausted_queue_raises_the_planning_error(self, tmp_path, isolate_data_root, demo_repo):
        consumed = dict(_PENDING_ITEM, id="SU-041", consumed_by="F256")
        queue_path = _write_queue(tmp_path, [consumed])
        from packages.orchestration.self_use_job import SelfUseJobError

        with pytest.raises(SelfUseJobError):
            run_next_self_use_item(tmp_path / "jobs", str(demo_repo), queue_path=queue_path)


class TestUnflaggedProviderResolution:
    """R-0757: an unflagged run must resolve the product's REAL default
    provider (role_config.DEFAULT_PROVIDER), never silently inherit
    run_job's own raw "fake" fallback."""

    def test_it_resolves_the_real_default_provider_when_unflagged(
        self, tmp_path, isolate_data_root, demo_repo, monkeypatch
    ):
        queue_path = _write_queue(tmp_path, [dict(_PENDING_ITEM)])
        captured: dict = {}

        def _stub_run_job(job_id, **kwargs):
            captured.update(kwargs)
            return "STUB_RESULT"

        monkeypatch.setattr(self_use_runner, "run_job", _stub_run_job)

        _entry, _path, result = run_next_self_use_item(
            tmp_path / "jobs", str(demo_repo), queue_path=queue_path
        )

        assert result == "STUB_RESULT"
        assert captured["builder_name"] == "ollama"
        assert captured["reviewer_name"] == "ollama"

    def test_it_refuses_rather_than_run_fake_when_resolution_names_fake(
        self, tmp_path, isolate_data_root, demo_repo, monkeypatch
    ):
        queue_path = _write_queue(tmp_path, [dict(_PENDING_ITEM)])

        def _fake_resolve(role, *args, **kwargs):
            return RoleConfig(role=role, provider="fake", model="m", effort="medium")

        monkeypatch.setattr(self_use_runner, "resolve_role_config", _fake_resolve)

        called = {"run_job": False}

        def _stub_run_job(job_id, **kwargs):
            called["run_job"] = True
            return "SHOULD_NOT_RUN"

        monkeypatch.setattr(self_use_runner, "run_job", _stub_run_job)

        with pytest.raises(SelfUseRunError, match="no usable real provider"):
            run_next_self_use_item(tmp_path / "jobs", str(demo_repo), queue_path=queue_path)

        assert called["run_job"] is False

    def test_explicit_fake_name_bypasses_resolution(
        self, tmp_path, isolate_data_root, demo_repo, monkeypatch
    ):
        queue_path = _write_queue(tmp_path, [dict(_PENDING_ITEM)])
        captured: dict = {}

        def _stub_run_job(job_id, **kwargs):
            captured.update(kwargs)
            return "STUB_RESULT"

        monkeypatch.setattr(self_use_runner, "run_job", _stub_run_job)

        run_next_self_use_item(
            tmp_path / "jobs",
            str(demo_repo),
            queue_path=queue_path,
            builder_name="fake",
            reviewer_name="fake",
        )

        assert captured["builder_name"] == "fake"
        assert captured["reviewer_name"] == "fake"

    def test_explicit_provider_object_bypasses_resolution(
        self, tmp_path, isolate_data_root, demo_repo, monkeypatch
    ):
        queue_path = _write_queue(tmp_path, [dict(_PENDING_ITEM)])
        captured: dict = {}

        def _stub_run_job(job_id, **kwargs):
            captured.update(kwargs)
            return "STUB_RESULT"

        monkeypatch.setattr(self_use_runner, "run_job", _stub_run_job)

        run_next_self_use_item(
            tmp_path / "jobs",
            str(demo_repo),
            queue_path=queue_path,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
        )

        assert "builder_name" not in captured
        assert "reviewer_name" not in captured
        assert isinstance(captured["builder_provider"], FakeProvider)


class TestGenerateThenRunEndToEnd:
    """The Acceptance criterion in ``docs/roadmap/features/T5_F258.md``: one full
    generate → plan → run cycle, proved end-to-end by a test fixture."""

    def test_a_generated_item_plans_and_runs(self, tmp_path, isolate_data_root, demo_repo):
        from packages.orchestration.self_use_generator import generate_and_append_if_empty

        queue_path = _write_queue(tmp_path, [])
        ledger_path = tmp_path / "live_review.md"
        ledger_path.write_text(
            "- R-0001 — Low, A TEST FINDING FOR THE FIXTURE. Fix the thing "
            "described here.\n",
            encoding="utf-8",
        )
        generated = generate_and_append_if_empty(queue_path=queue_path, ledger_path=ledger_path)
        assert generated is not None
        assert generated.provenance.startswith("generated (self-use-generator tier 1")

        entry, job_file_path, result = run_next_self_use_item(
            tmp_path / "jobs",
            str(demo_repo),
            queue_path=queue_path,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
        )
        assert entry.id == generated.id
        assert job_file_path.exists()
        assert result.status == JOB_COMPLETED
