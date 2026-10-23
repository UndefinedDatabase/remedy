"""F151 T003: the adapter registry linkage (DECISION F151 D5 (2))."""
from __future__ import annotations

from packages.contracts.adapter_contract import WorkerAdapter
from packages.orchestration.worker_adapters import list_worker_specs
from packages.providers.adapters.adapter_registry import resolve_worker_adapter


def test_every_non_empty_reference_resolves_to_its_own_adapter_id():
    for spec in list_worker_specs():
        if not spec.adapter_ref:
            continue
        adapter = resolve_worker_adapter(spec.adapter_ref)
        assert adapter is not None
        assert adapter.adapter_id == spec.adapter_ref
        assert isinstance(adapter, WorkerAdapter)


def test_resolve_worker_adapter_is_none_for_an_empty_reference():
    assert resolve_worker_adapter("") is None


def test_resolve_worker_adapter_is_none_for_an_unknown_reference():
    assert resolve_worker_adapter("no-such") is None
