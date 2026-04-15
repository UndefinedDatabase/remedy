"""
Smoke tests: verify that core models and contracts import without errors.
"""

import sys
import os

# Allow imports from the packages directory without installation
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


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


def test_interfaces_are_protocols():
    from packages.contracts.interfaces import LLMWorker, MemoryGateway, RuntimeProvider, Verifier
    from typing import Protocol
    # All four are Protocols (runtime_checkable)
    for iface in (LLMWorker, MemoryGateway, RuntimeProvider, Verifier):
        assert issubclass(iface, Protocol)
