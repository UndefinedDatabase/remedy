"""
Tests for Step 37 — Worker Adapter Foundation v0.

Coverage:
  - WorkerProviderSpec dataclass is frozen
  - list_worker_specs returns tuple of specs
  - All specs have required fields
  - Expected providers exist (ollama, claude_code, pi_dev, copilot, openai_api)
  - export_worker_specs_json returns JSON-serializable list
  - summarize_worker_specs returns non-empty string
  - Provider-neutral: no network, no subprocess, no secrets
"""

from __future__ import annotations

import pytest

from packages.orchestration.worker_adapters import (
    WorkerProviderSpec,
    export_worker_specs_json,
    list_worker_specs,
    summarize_worker_specs,
)

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestWorkerProviderSpec:
    def test_frozen(self) -> None:
        specs = list_worker_specs()
        assert len(specs) > 0
        with pytest.raises(AttributeError):
            specs[0].provider_id = "hacked"  # type: ignore[misc]

    def test_all_fields_present(self) -> None:
        for spec in list_worker_specs():
            assert hasattr(spec, "provider_id")
            assert hasattr(spec, "display_name")
            assert hasattr(spec, "supported_roles")
            assert hasattr(spec, "execution_mode")
            assert hasattr(spec, "status")
            assert hasattr(spec, "notes")


class TestListWorkerSpecs:
    def test_returns_tuple(self) -> None:
        specs = list_worker_specs()
        assert isinstance(specs, tuple)

    def test_non_empty(self) -> None:
        specs = list_worker_specs()
        assert len(specs) >= 5

    def test_all_are_worker_provider_spec(self) -> None:
        for spec in list_worker_specs():
            assert isinstance(spec, WorkerProviderSpec)

    def test_expected_providers(self) -> None:
        ids = {s.provider_id for s in list_worker_specs()}
        assert "ollama" in ids
        assert "claude_code" in ids
        assert "pi_dev" in ids
        assert "copilot" in ids
        assert "openai_api" in ids

    def test_ollama_is_available(self) -> None:
        specs = {s.provider_id: s for s in list_worker_specs()}
        assert specs["ollama"].status == "available"

    def test_future_specs_are_future(self) -> None:
        specs = {s.provider_id: s for s in list_worker_specs()}
        for pid in ("claude_code", "pi_dev", "copilot", "openai_api"):
            assert specs[pid].status == "future"

    def test_all_have_roles(self) -> None:
        for spec in list_worker_specs():
            assert len(spec.supported_roles) > 0
            assert all(isinstance(r, str) for r in spec.supported_roles)

    def test_execution_modes_valid(self) -> None:
        valid_modes = {"local_process", "external_harness", "api", "future"}
        for spec in list_worker_specs():
            assert spec.execution_mode in valid_modes

    def test_unique_provider_ids(self) -> None:
        ids = [s.provider_id for s in list_worker_specs()]
        assert len(ids) == len(set(ids))


class TestExportWorkerSpecsJson:
    def test_returns_dict_with_version(self) -> None:
        result = export_worker_specs_json()
        assert isinstance(result, dict)
        assert result["version"] == 1
        assert "providers" in result

    def test_json_serializable(self) -> None:
        import json
        result = export_worker_specs_json()
        serialized = json.dumps(result)
        assert isinstance(serialized, str)

    def test_each_entry_has_required_keys(self) -> None:
        required = {"provider_id", "display_name", "supported_roles", "execution_mode", "status", "notes"}
        for entry in export_worker_specs_json()["providers"]:
            assert required.issubset(set(entry.keys()))

    def test_roles_are_lists(self) -> None:
        for entry in export_worker_specs_json()["providers"]:
            assert isinstance(entry["supported_roles"], list)


class TestSummarizeWorkerSpecs:
    def test_returns_string(self) -> None:
        summary = summarize_worker_specs()
        assert isinstance(summary, str)
        assert len(summary) > 50

    def test_contains_key_providers(self) -> None:
        summary = summarize_worker_specs()
        assert "Ollama" in summary
        assert "Claude Code" in summary
        assert "Worker Adapters" in summary


class TestWorkerAdaptersNoSubprocess:
    def test_no_subprocess_import(self) -> None:
        import packages.orchestration.worker_adapters as mod
        source = open(mod.__file__).read()
        assert "subprocess" not in source
        assert "os.system" not in source
        assert "shell=True" not in source

    def test_no_network_import(self) -> None:
        import packages.orchestration.worker_adapters as mod
        source = open(mod.__file__).read()
        assert "urllib" not in source
        assert "requests" not in source
        assert "httpx" not in source

    def test_no_hardcoded_secrets(self) -> None:
        """Verify no actual secret values or API key assignments exist."""
        for spec in list_worker_specs():
            assert "sk-" not in spec.notes
            assert "key=" not in spec.notes
            assert "password" not in spec.notes.lower()
