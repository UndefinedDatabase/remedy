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
        import packages.orchestration.pi_provider as pi_provider
        monkeypatch.setattr(pi_provider, "default_chain_checks", lambda: [("pi_executable", True, "pi")])
        from apps.cli.commands.worker import _cmd_worker_doctor
        _cmd_worker_doctor(json_output=True)
        out = json.loads(capsys.readouterr().out)
        # F283 R19 C5 (DECISION F283 D10) — `emit_ok` adds `schema_version` and `ok`.
        assert out["schema_version"] == 1
        assert out["ok"] is True
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


class TestAWorkerRefusalIsShapedLikeTheCaller:
    """F277 T003 — the `worker` group migrated onto the shared `fail()`."""

    def test_an_unknown_provider_is_an_envelope_under_json(self, capsys):
        from apps.cli.commands.worker import _cmd_worker_show

        with pytest.raises(SystemExit) as exc:
            _cmd_worker_show("no-such-provider", json_output=True)
        assert exc.value.code == 1
        captured = capsys.readouterr()
        assert captured.err == ""
        body = json.loads(captured.out)
        assert body["ok"] is False and body["schema_version"] == 1
        assert body["error"] == "unknown_provider"
        assert "no-such-provider" in body["message"]

    def test_without_json_it_is_the_line_it_always_was(self, capsys):
        from apps.cli.commands.worker import _cmd_worker_show

        with pytest.raises(SystemExit) as exc:
            _cmd_worker_show("no-such-provider", json_output=False)
        assert exc.value.code == 1
        captured = capsys.readouterr()
        assert captured.out == ""
        assert captured.err == "Error: unknown provider: no-such-provider\n"

    def test_unload_without_a_target_names_both_flags(self, monkeypatch, capsys):
        # The refusal is the caller's, not the environment's: pin `ollama` on PATH
        # so the missing-argument branch is what this test reaches.
        import shutil as _shutil
        monkeypatch.setattr(_shutil, "which", lambda name: "/usr/bin/ollama" if name == "ollama" else None)
        from apps.cli.commands.worker import _cmd_worker_unload

        with pytest.raises(SystemExit) as exc:
            _cmd_worker_unload(json_output=True)
        assert exc.value.code == 1
        body = json.loads(capsys.readouterr().out)
        assert body["error"] == "missing_argument"
        assert "--model" in body["message"] and "--all" in body["message"]

    def test_unload_without_a_target_refuses_before_the_provider_probe(self, monkeypatch, capsys):
        # R-1019 — the missing-argument refusal must fire even when `ollama` is not on
        # PATH: pin `shutil.which` to `None` so a real, unpinned PATH read (finding
        # R-1018) can never make this test pass or fail by accident.
        import shutil as _shutil
        monkeypatch.setattr(_shutil, "which", lambda name: None)
        from apps.cli.commands.worker import _cmd_worker_unload

        with pytest.raises(SystemExit) as exc:
            _cmd_worker_unload(json_output=True)
        assert exc.value.code == 1
        body = json.loads(capsys.readouterr().out)
        assert body["error"] == "missing_argument"
        assert "--model" in body["message"] and "--all" in body["message"]


class TestWorkerShowAdapterLinkage:
    """F151 T003: `remedy worker show` as the product path to an adapter (DECISION F151 D5 (3))."""

    def test_claude_code_text_output_carries_adapter_and_capabilities(self, capsys):
        from apps.cli.commands.worker import _cmd_worker_show
        _cmd_worker_show("claude_code", json_output=False)
        out = capsys.readouterr().out
        assert "Adapter: claude-cli" in out
        assert "Capabilities: json_schema, session_resume, streaming, tool_use" in out

    def test_ollama_text_output_carries_neither_line(self, capsys):
        from apps.cli.commands.worker import _cmd_worker_show
        _cmd_worker_show("ollama", json_output=False)
        out = capsys.readouterr().out
        assert "Adapter:" not in out
        assert "Capabilities:" not in out

    def test_claude_code_json_answer_carries_adapter_ref(self, capsys):
        from apps.cli.commands.worker import _cmd_worker_show
        _cmd_worker_show("claude_code", json_output=True)
        body = json.loads(capsys.readouterr().out)
        entry = body["providers"][0]
        assert entry["adapter_ref"] == "claude-cli"

    def test_the_json_answer_carries_the_capabilities_the_text_prints(self, capsys):
        """amend1023 D4: the same flags as the text's `Capabilities:` line, and null without an adapter."""
        from apps.cli.commands.worker import _cmd_worker_show
        _cmd_worker_show("claude_code", json_output=True)
        entry = json.loads(capsys.readouterr().out)["providers"][0]
        assert entry["capabilities"] == {
            "vision": False, "json_schema": True, "session_resume": True, "streaming": True,
            "tool_use": True, "max_context_tokens": 0}
        _cmd_worker_show("ollama", json_output=True)
        assert json.loads(capsys.readouterr().out)["providers"][0]["capabilities"] is None

    def test_claude_code_text_output_shows_none_for_an_adapter_with_no_capability(self, monkeypatch, capsys):
        # R-1440 — the `none` line is held by no test; an adapter declaring no flag at all
        # must still print `  Capabilities: none` rather than an empty or missing line.
        from packages.contracts.adapter_contract import AdapterCapabilities
        from packages.providers.adapters import adapter_registry

        class _NoCapabilityAdapter:
            adapter_id = "claude-cli"

            def capabilities(self, model: str) -> AdapterCapabilities:
                return AdapterCapabilities(
                    vision=False, json_schema=False, session_resume=False,
                    streaming=False, tool_use=False, max_context_tokens=0,
                )

        monkeypatch.setattr(
            adapter_registry, "resolve_worker_adapter",
            lambda adapter_ref: _NoCapabilityAdapter(),
        )
        from apps.cli.commands.worker import _cmd_worker_show
        _cmd_worker_show("claude_code", json_output=False)
        out = capsys.readouterr().out
        assert "  Capabilities: none" in out
