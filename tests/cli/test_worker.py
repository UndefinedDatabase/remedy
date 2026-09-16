"""Tests for `apps/cli/commands/worker.py` — currently just `worker doctor`."""

from __future__ import annotations

import json

import pytest


class TestWorkerDoctorCatalog:
    def test_worker_doctor_in_catalog(self):
        from apps.cli.command_catalog import CATALOG
        ids = {c.command_id for c in CATALOG}
        assert "worker.doctor" in ids

    def test_worker_doctor_has_a_handler(self):
        from apps.cli.commands.worker import COMMAND_HANDLERS
        assert "worker.doctor" in COMMAND_HANDLERS
        assert callable(COMMAND_HANDLERS["worker.doctor"])

    def test_worker_doctor_is_read_only(self):
        from apps.cli.command_catalog import CATALOG
        entry = next(c for c in CATALOG if c.command_id == "worker.doctor")
        assert entry.action_class == "read_only"
        assert entry.supports_json is True


class TestWorkerDoctor:
    def test_ollama_on_path_reads_ready(self, monkeypatch, capsys):
        import shutil as _shutil
        monkeypatch.setattr(_shutil, "which", lambda name: "/usr/bin/ollama" if name == "ollama" else None)
        from apps.cli.commands.worker import _cmd_worker_doctor
        _cmd_worker_doctor(json_output=True)
        out = json.loads(capsys.readouterr().out)
        assert out["ready"] is True
        assert out["blockers"] == []
        check_names = {c["check"] for c in out["checks"]}
        assert "worker_specs" in check_names
        assert "provider_ollama" in check_names
        ollama_check = next(c for c in out["checks"] if c["check"] == "provider_ollama")
        assert ollama_check["ok"] is True

    def test_ollama_missing_from_path_is_a_blocker(self, monkeypatch, capsys):
        import shutil as _shutil
        monkeypatch.setattr(_shutil, "which", lambda name: None)
        from apps.cli.commands.worker import _cmd_worker_doctor
        _cmd_worker_doctor(json_output=True)
        out = json.loads(capsys.readouterr().out)
        assert out["ready"] is False
        assert "provider_ollama" in out["blockers"]

    def test_future_status_specs_are_never_probed(self, monkeypatch, capsys):
        """`claude_code`, `pi_dev`, `copilot`, `openai_api` are `status="future"`;
        only an `available` spec is checked at all."""
        import shutil as _shutil
        monkeypatch.setattr(_shutil, "which", lambda name: "/usr/bin/ollama" if name == "ollama" else None)
        from apps.cli.commands.worker import _cmd_worker_doctor
        from packages.orchestration.worker_adapters import list_worker_specs
        future_ids = {s.provider_id for s in list_worker_specs() if s.status != "available"}
        assert future_ids, "fixture assumption: at least one non-available spec exists"
        _cmd_worker_doctor(json_output=True)
        out = json.loads(capsys.readouterr().out)
        checked_ids = {c["check"] for c in out["checks"]}
        for provider_id in future_ids:
            assert f"provider_{provider_id}" not in checked_ids

    def test_text_output(self, monkeypatch, capsys):
        import shutil as _shutil
        monkeypatch.setattr(_shutil, "which", lambda name: "/usr/bin/ollama" if name == "ollama" else None)
        from apps.cli.commands.worker import _cmd_worker_doctor
        _cmd_worker_doctor(json_output=False)
        out = capsys.readouterr().out
        assert "Worker Doctor" in out
        assert "READY" in out

    @pytest.mark.parametrize("catalog_provider_id", ["claude_code", "pi_dev", "copilot", "openai_api"])
    def test_an_available_spec_with_no_probe_fails_rather_than_passing_silently(
        self, monkeypatch, capsys, catalog_provider_id,
    ):
        """A spec this doctor has no real probe for is reported FAIL, never a
        silent pass — the guard R-0939's neighbours in this feature keep
        naming: an unprobed `available` claim is worse than an honest FAIL."""
        import shutil as _shutil
        from dataclasses import replace

        from packages.orchestration import worker_adapters

        monkeypatch.setattr(_shutil, "which", lambda name: "/usr/bin/ollama" if name == "ollama" else None)
        real_specs = worker_adapters.list_worker_specs()
        mutated = tuple(
            replace(s, status="available") if s.provider_id == catalog_provider_id else s
            for s in real_specs
        )
        monkeypatch.setattr(worker_adapters, "list_worker_specs", lambda: mutated)
        from apps.cli.commands.worker import _cmd_worker_doctor
        _cmd_worker_doctor(json_output=True)
        out = json.loads(capsys.readouterr().out)
        assert out["ready"] is False
        assert f"provider_{catalog_provider_id}" in out["blockers"]
