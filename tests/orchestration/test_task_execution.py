"""Tests for task execution port, fixture executor, budget gate, retry boundary."""

from __future__ import annotations

from pathlib import Path
from uuid import UUID, uuid4

import pytest

from packages.orchestration.task_execution import (
    TaskExecutionRequest,
    TaskExecutionResult,
    FixtureTaskExecutor,
    NoneExecutor,
    execute_task,
    get_executor,
    BudgetGate,
    can_retry_task,
    ALLOWED_PROVIDERS,
)


class TestTaskExecutionRequest:
    def test_defaults(self):
        r = TaskExecutionRequest(job_id="j1", task_id="t1", task_description="Do thing")
        assert r.provider == "fixture"
        assert r.max_steps == 1

    def test_custom_provider(self):
        r = TaskExecutionRequest(job_id="j1", task_id="t1", task_description="X", provider="none")
        assert r.provider == "none"


class TestFixtureExecutor:
    def test_completes_normal_task(self):
        req = TaskExecutionRequest(job_id="j1", task_id="t1", task_description="Build feature",
                                   task_inputs={"task_type": "feature", "source": "reviewer"})
        result = FixtureTaskExecutor().execute(req)
        assert result.work_performed is True
        assert result.status == "completed"
        assert result.provider == "fixture"
        assert len(result.artifact_ids) == 1
        assert result.safe_summary.startswith("Fixture completed:")

    def test_blocked_fixture_type(self):
        req = TaskExecutionRequest(job_id="j1", task_id="t1", task_description="Blocked",
                                   task_inputs={"task_type": "blocked_fixture"})
        result = FixtureTaskExecutor().execute(req)
        assert result.work_performed is False
        assert result.status == "blocked"
        assert result.blocked_reason == "fixture_blocked_task_type"


class TestNoneExecutor:
    def test_returns_no_work(self):
        req = TaskExecutionRequest(job_id="j1", task_id="t1", task_description="X", provider="none")
        result = NoneExecutor().execute(req)
        assert result.work_performed is False
        assert result.status == "blocked"
        assert result.blocked_reason == "no_worker_selected"


class TestProviderSelection:
    def test_fixture_selected(self):
        ex = get_executor("fixture")
        assert isinstance(ex, FixtureTaskExecutor)

    def test_none_selected(self):
        ex = get_executor("none")
        assert isinstance(ex, NoneExecutor)

    def test_ollama_unavailable(self):
        ex = get_executor("ollama")
        assert ex is None

    def test_unknown_provider(self):
        ex = get_executor("fake_provider")
        assert ex is None

    def test_allowed_providers(self):
        assert "fixture" in ALLOWED_PROVIDERS
        assert "none" in ALLOWED_PROVIDERS
        assert "ollama" in ALLOWED_PROVIDERS


class TestExecuteTask:
    def test_fixture_execution(self):
        req = TaskExecutionRequest(job_id="j1", task_id="t1", task_description="Build it")
        result = execute_task(req)
        assert result.status == "completed"
        assert result.work_performed is True

    def test_unavailable_provider(self):
        req = TaskExecutionRequest(job_id="j1", task_id="t1", task_description="X", provider="ollama")
        result = execute_task(req)
        assert result.status == "blocked"
        assert result.outcome == "provider_unavailable"

    def test_unknown_provider(self):
        req = TaskExecutionRequest(job_id="j1", task_id="t1", task_description="X", provider="fake")
        result = execute_task(req)
        assert result.status == "blocked"


class TestBudgetGate:
    def test_no_budget(self):
        g = BudgetGate()
        ok, reason = g.can_execute()
        assert ok is False
        assert reason == "no_budget_set"

    def test_budget_allows(self):
        g = BudgetGate(max_steps=1)
        ok, _ = g.can_execute()
        assert ok is True

    def test_budget_exhausted(self):
        g = BudgetGate(max_steps=1)
        g.record_step()
        ok, reason = g.can_execute()
        assert ok is False
        assert reason == "max_steps_exhausted"

    def test_has_budget(self):
        assert BudgetGate(max_steps=5).has_budget is True
        assert BudgetGate().has_budget is False


class TestCanRetryTask:
    def test_completed_not_retryable(self, tmp_path, monkeypatch):
        monkeypatch.setattr("packages.orchestration.proposed_tasks._STORE_DIR", tmp_path / "proposed_tasks")
        monkeypatch.setattr("packages.orchestration.storage._DATA_DIR", tmp_path / "jobs")
        from packages.core.models import Job, Task, RunState
        job = Job(id=uuid4(), name="retry-test")
        task = Task(description="Done", status=RunState.COMPLETED)
        job.tasks.append(task)
        from packages.orchestration.storage import save_job
        save_job(job)
        result = can_retry_task(str(job.id), str(task.id))
        assert result["ready"] is False
        assert "already_completed" in result["blockers"]

    def test_pending_not_retryable(self, tmp_path, monkeypatch):
        monkeypatch.setattr("packages.orchestration.proposed_tasks._STORE_DIR", tmp_path / "proposed_tasks")
        monkeypatch.setattr("packages.orchestration.storage._DATA_DIR", tmp_path / "jobs")
        from packages.core.models import Job, Task, RunState
        job = Job(id=uuid4(), name="retry-test")
        task = Task(description="Pending", status=RunState.PENDING)
        job.tasks.append(task)
        from packages.orchestration.storage import save_job
        save_job(job)
        result = can_retry_task(str(job.id), str(task.id))
        assert result["ready"] is False
        assert "still_pending" in result["blockers"]

    def test_missing_job(self, tmp_store_monkeypatch=None):
        result = can_retry_task("00000000-0000-0000-0000-000000000099", "nope")
        assert result["ready"] is False
        assert "job_not_found" in result["blockers"]


class TestModularArchitectureGuards:
    def test_worker_queue_does_not_import_ollama_directly(self):
        src = Path("packages/orchestration/worker_queue.py").read_text()
        assert "import ollama" not in src
        assert "from ollama" not in src

    def test_task_execution_does_not_import_providers(self):
        src = Path("packages/orchestration/task_execution.py").read_text()
        assert "import ollama" not in src
        assert "from ollama" not in src

    def test_proposed_tasks_does_not_import_providers(self):
        src = Path("packages/orchestration/proposed_tasks.py").read_text()
        assert "import ollama" not in src
        assert "from ollama" not in src

    def test_storage_access_through_helpers(self):
        src = Path("packages/orchestration/proposed_tasks.py").read_text()
        assert "open(" not in src or "_atomic_write" in src

    def test_no_source_apply_bypass_from_executor(self):
        src = Path("packages/orchestration/task_execution.py").read_text()
        assert "source_apply" not in src
        assert "repo_applicator" not in src
