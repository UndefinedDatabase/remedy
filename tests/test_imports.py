"""
Smoke tests: verify that core models and contracts import without errors.
"""


def test_core_models_import():
    from packages.core.models import (
        Artifact,
        AcceptanceCheck,
        Budget,
        Job,
        RunState,
        Task,
    )
    assert Budget is not None
    assert AcceptanceCheck is not None
    assert Artifact is not None
    assert Task is not None
    assert RunState is not None
    assert Job is not None


def test_contracts_interfaces_import():
    from packages.contracts.interfaces import (
        LLMWorker,
        MemoryGateway,
        RuntimeProvider,
        Verifier,
    )
    assert LLMWorker is not None
    assert MemoryGateway is not None
    assert RuntimeProvider is not None
    assert Verifier is not None


def test_run_state_values():
    from packages.core.models import RunState
    assert RunState.PENDING == "pending"
    assert RunState.COMPLETED == "completed"
    assert RunState.FAILED == "failed"


def test_job_defaults():
    from packages.core.models import Job
    job = Job(name="test-job")
    assert job.name == "test-job"
    assert job.tasks == []
    assert job.artifacts == []


def test_task_lifecycle_defaults():
    from packages.core.models import Task, RunState
    task = Task(description="do something")
    assert task.status == RunState.PENDING
    assert task.output_artifact_ids == []


def test_artifact_provenance():
    from packages.core.models import Artifact
    # Without task_id (default)
    a = Artifact(name="out", content="hello")
    assert a.task_id is None
    # With task_id
    from uuid import uuid4
    tid = uuid4()
    b = Artifact(name="out2", content="world", task_id=tid)
    assert b.task_id == tid


def test_interfaces_are_protocols():
    from packages.contracts.interfaces import LLMWorker, MemoryGateway, RuntimeProvider, Verifier
    from typing import Protocol
    for iface in (LLMWorker, MemoryGateway, RuntimeProvider, Verifier):
        assert issubclass(iface, Protocol)
