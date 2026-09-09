"""Tests for worker facade + mission command facade CLI handlers."""

from __future__ import annotations

import argparse
import json
from unittest.mock import patch

import pytest

# ---------------------------------------------------------------------------
# Alias registry
# ---------------------------------------------------------------------------


class TestWorkerAliasRegistry:
    def test_known_aliases(self):
        from apps.cli.commands.worker_facade_cmd import _WORKER_ALIASES
        assert "claude" in _WORKER_ALIASES
        assert "claude-code" in _WORKER_ALIASES
        assert "fixture" in _WORKER_ALIASES
        assert "generic" in _WORKER_ALIASES

    def test_claude_alias_fields(self):
        from apps.cli.commands.worker_facade_cmd import _WORKER_ALIASES
        c = _WORKER_ALIASES["claude"]
        assert c["adapter_id"] == "claude-code-v0"
        assert c["template_id"] == "claude-code-repair-v0"
        assert c["kind"] == "claude_code"

    def test_resolve_case_insensitive(self):
        from apps.cli.commands.worker_facade_cmd import _resolve_alias
        assert _resolve_alias("Claude") is not None
        assert _resolve_alias("CLAUDE") is not None
        assert _resolve_alias(" claude ") is not None

    def test_resolve_unknown_returns_none(self):
        from apps.cli.commands.worker_facade_cmd import _resolve_alias
        assert _resolve_alias("nonexistent") is None


# ---------------------------------------------------------------------------
# Handler registry
# ---------------------------------------------------------------------------


class TestHandlerRegistry:
    def test_all_handlers_present(self):
        from apps.cli.commands.worker_facade_cmd import COMMAND_HANDLERS
        expected = {"worker.doctor", "worker.add", "worker.disable",
                    "mission.run", "doctor.core"}
        assert set(COMMAND_HANDLERS.keys()) == expected

    def test_all_handlers_callable(self):
        from apps.cli.commands.worker_facade_cmd import COMMAND_HANDLERS
        for key, fn in COMMAND_HANDLERS.items():
            assert callable(fn), f"{key} handler not callable"


# ---------------------------------------------------------------------------
# Catalog + contract integration
# ---------------------------------------------------------------------------


class TestCatalogIntegration:
    def test_mission_group_exists(self):
        from apps.cli.command_catalog import GROUPS
        assert "mission" in GROUPS

    def test_worker_facade_commands_in_catalog(self):
        from apps.cli.command_catalog import CATALOG
        ids = {c.command_id for c in CATALOG}
        for cmd_id in ("worker.doctor", "worker.add", "worker.disable",
                       "mission.run", "mission.report"):
            assert cmd_id in ids, f"{cmd_id} missing from catalog"

    def test_mission_commands_in_catalog(self):
        """The facade's own two commands live in the mission group.

        A subset, not the whole group: F056 added the persistent-goal
        commands (start/continue/list/show) to the same group, and this
        test guards the facade's entries, not the group's size.
        """
        from apps.cli.command_catalog import CATALOG
        ids = {c.command_id for c in CATALOG if c.group_id == "mission"}
        assert {"mission.run", "mission.report"} <= ids

    def test_all_facade_commands_have_handlers(self):
        from apps.cli.command_catalog import CATALOG
        from apps.cli.commands.worker_facade_cmd import COMMAND_HANDLERS
        facade_cmds = [c for c in CATALOG
                       if c.command_id in COMMAND_HANDLERS]
        assert len(facade_cmds) == 5
        for cmd in facade_cmds:
            assert cmd.command_id in COMMAND_HANDLERS


class TestContractActions:
    def test_facade_actions_exist(self):
        from packages.orchestration.run_contract import ContractAction
        for name in ("WORKER_DOCTOR", "WORKER_ADD", "WORKER_DISABLE",
                     "MISSION_RUN", "MISSION_REPORT"):
            assert hasattr(ContractAction, name)

    def test_facade_actions_in_defaults(self):
        from packages.orchestration.run_contract import (
            _DEFAULT_ALLOWED_ACTIONS,
            ContractAction,
        )
        for name in ("WORKER_DOCTOR", "WORKER_ADD", "WORKER_DISABLE",
                     "MISSION_RUN", "MISSION_REPORT"):
            val = getattr(ContractAction, name)
            assert val in _DEFAULT_ALLOWED_ACTIONS, f"{name} not in defaults"


# ---------------------------------------------------------------------------
# worker doctor
# ---------------------------------------------------------------------------


def _ns(**kwargs) -> argparse.Namespace:
    return argparse.Namespace(**kwargs)


_ADAPTER_PATCH = "packages.orchestration.main_builder_adapter.get_builder_adapter_spec"
_TMPL_PATCH = "packages.orchestration.managed_builder_execution.get_command_template"
_SAVE_ADAPTER = "packages.orchestration.main_builder_adapter.save_builder_adapter_spec"
_ENABLE_TMPL = "packages.orchestration.managed_builder_execution.enable_command_template"
_DISABLE_TMPL = "packages.orchestration.managed_builder_execution.disable_command_template"


class TestWorkerDoctor:
    @patch(_TMPL_PATCH)
    @patch(_ADAPTER_PATCH)
    @patch("shutil.which", return_value="/usr/bin/claude")
    def test_doctor_all_ready(self, mock_which, mock_adapter, mock_tmpl, capsys):
        mock_adapter.return_value = {"enabled": True, "mode": "operator_launched",
                                     "adapter_id": "claude-code-v0"}
        mock_tmpl.return_value = {"enabled": True, "template_id": "claude-code-repair-v0"}
        from apps.cli.commands.worker_facade_cmd import _cmd_worker_doctor
        _cmd_worker_doctor(_ns(worker="claude", json=True))
        out = json.loads(capsys.readouterr().out)
        assert out["ready"] is True
        assert out["blockers"] == []

    @patch(_TMPL_PATCH)
    @patch(_ADAPTER_PATCH)
    @patch("shutil.which", return_value=None)
    def test_doctor_binary_missing(self, mock_which, mock_adapter, mock_tmpl, capsys):
        mock_adapter.return_value = {"enabled": True, "mode": "operator_launched",
                                     "adapter_id": "claude-code-v0"}
        mock_tmpl.return_value = {"enabled": True, "template_id": "claude-code-repair-v0"}
        from apps.cli.commands.worker_facade_cmd import _cmd_worker_doctor
        _cmd_worker_doctor(_ns(worker="claude", json=True))
        out = json.loads(capsys.readouterr().out)
        assert out["ready"] is False
        assert any("binary" in b.lower() for b in out["blockers"])

    @patch(_TMPL_PATCH)
    @patch(_ADAPTER_PATCH)
    @patch("shutil.which", return_value="/usr/bin/claude")
    def test_doctor_adapter_disabled(self, mock_which, mock_adapter, mock_tmpl, capsys):
        mock_adapter.return_value = {"enabled": False, "mode": "disabled",
                                     "adapter_id": "claude-code-v0"}
        mock_tmpl.return_value = {"enabled": True, "template_id": "claude-code-repair-v0"}
        from apps.cli.commands.worker_facade_cmd import _cmd_worker_doctor
        _cmd_worker_doctor(_ns(worker="claude", json=True))
        out = json.loads(capsys.readouterr().out)
        assert out["ready"] is False
        assert any("adapter" in b.lower() for b in out["blockers"])
        assert "next_recommended_command" in out

    def test_doctor_unknown_worker(self):
        from apps.cli.commands.worker_facade_cmd import _cmd_worker_doctor
        with pytest.raises(SystemExit):
            _cmd_worker_doctor(_ns(worker="nonexistent", json=True))

    @patch(_TMPL_PATCH)
    @patch(_ADAPTER_PATCH)
    @patch("shutil.which", return_value="/usr/bin/claude")
    def test_doctor_text_output(self, mock_which, mock_adapter, mock_tmpl, capsys):
        mock_adapter.return_value = {"enabled": True, "mode": "operator_launched",
                                     "adapter_id": "claude-code-v0"}
        mock_tmpl.return_value = {"enabled": True, "template_id": "claude-code-repair-v0"}
        from apps.cli.commands.worker_facade_cmd import _cmd_worker_doctor
        _cmd_worker_doctor(_ns(worker="claude", json=False))
        out = capsys.readouterr().out
        assert "Claude Code" in out
        assert "ready: True" in out


# ---------------------------------------------------------------------------
# worker add
# ---------------------------------------------------------------------------


class TestWorkerAdd:
    @patch(_ENABLE_TMPL)
    @patch(_TMPL_PATCH)
    @patch(_SAVE_ADAPTER)
    @patch(_ADAPTER_PATCH)
    def test_add_enables_both(self, mock_get_adapter, mock_save, mock_get_tmpl,
                              mock_enable_tmpl, capsys):
        mock_get_adapter.return_value = {"enabled": False, "mode": "disabled",
                                         "adapter_id": "claude-code-v0",
                                         "kind": "claude_code"}
        mock_save.return_value = True
        mock_get_tmpl.return_value = {"enabled": False, "template_id": "claude-code-repair-v0"}
        mock_enable_tmpl.return_value = {"enabled": True}

        from apps.cli.commands.worker_facade_cmd import _cmd_worker_add
        _cmd_worker_add(_ns(worker="claude", json=True))
        out = json.loads(capsys.readouterr().out)
        assert out["ready"] is True
        assert out["adapter_enabled"] is True
        assert out["template_enabled"] is True
        assert "quickstart" in out
        assert len(out["quickstart"]) > 0
        assert "advanced" in out

    @patch(_ENABLE_TMPL)
    @patch(_TMPL_PATCH)
    @patch(_SAVE_ADAPTER)
    @patch(_ADAPTER_PATCH)
    def test_add_already_enabled(self, mock_get_adapter, mock_save, mock_get_tmpl,
                                  mock_enable_tmpl, capsys):
        mock_get_adapter.return_value = {"enabled": True, "mode": "operator_launched",
                                         "adapter_id": "claude-code-v0",
                                         "kind": "claude_code"}
        mock_get_tmpl.return_value = {"enabled": True, "template_id": "claude-code-repair-v0"}

        from apps.cli.commands.worker_facade_cmd import _cmd_worker_add
        _cmd_worker_add(_ns(worker="claude", json=True))
        out = json.loads(capsys.readouterr().out)
        assert out["ready"] is True
        mock_save.assert_not_called()
        mock_enable_tmpl.assert_not_called()

    def test_add_unknown_worker(self):
        from apps.cli.commands.worker_facade_cmd import _cmd_worker_add
        with pytest.raises(SystemExit):
            _cmd_worker_add(_ns(worker="nope", json=True))


# ---------------------------------------------------------------------------
# worker disable
# ---------------------------------------------------------------------------


class TestWorkerDisable:
    @patch(_DISABLE_TMPL)
    @patch(_SAVE_ADAPTER)
    @patch(_ADAPTER_PATCH)
    def test_disable_both(self, mock_get_adapter, mock_save, mock_disable_tmpl, capsys):
        mock_get_adapter.return_value = {"enabled": True, "mode": "operator_launched",
                                         "adapter_id": "claude-code-v0",
                                         "kind": "claude_code"}
        mock_save.return_value = True
        mock_disable_tmpl.return_value = {"enabled": False}

        from apps.cli.commands.worker_facade_cmd import _cmd_worker_disable
        _cmd_worker_disable(_ns(worker="claude", json=True))
        out = json.loads(capsys.readouterr().out)
        assert out["adapter_disabled"] is True
        assert out["template_disabled"] is True

    def test_disable_unknown_worker(self):
        from apps.cli.commands.worker_facade_cmd import _cmd_worker_disable
        with pytest.raises(SystemExit):
            _cmd_worker_disable(_ns(worker="nope", json=True))


# ---------------------------------------------------------------------------
# mission run facade
# ---------------------------------------------------------------------------


class TestMissionRun:
    def test_run_no_run_id(self):
        from apps.cli.commands.worker_facade_cmd import _cmd_mission_run
        with pytest.raises(SystemExit):
            _cmd_mission_run(_ns(run_id="", job_id="", max_steps=10,
                                 max_seconds=300, json=True))


# ---------------------------------------------------------------------------
# collect_all_handlers includes facade
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# doctor core
# ---------------------------------------------------------------------------


class TestDoctorCore:
    def test_core_all_ready(self, capsys):
        from apps.cli.commands.worker_facade_cmd import _cmd_doctor_core
        _cmd_doctor_core(_ns(json=True))
        out = json.loads(capsys.readouterr().out)
        assert out["ready"] is True
        assert out["blockers"] == []
        check_names = {c["check"] for c in out["checks"]}
        assert "worker_facade" in check_names
        assert "command_catalog" in check_names
        assert "run_contract" in check_names
        assert "fast_test_lane" in check_names

    def test_core_error_messages_safe(self, capsys):
        from apps.cli.commands.worker_facade_cmd import _cmd_doctor_core
        _cmd_doctor_core(_ns(json=True))
        out = json.loads(capsys.readouterr().out)
        raw = json.dumps(out)
        assert "/home/" not in raw, "Doctor core must not leak absolute home paths"
        assert "/root/" not in raw, "Doctor core must not leak root paths"
        for check in out["checks"]:
            detail = str(check.get("detail", ""))
            assert len(detail) <= 200, f"Detail too long: {detail[:50]}..."

    def test_core_text_output(self, capsys):
        from apps.cli.commands.worker_facade_cmd import _cmd_doctor_core
        _cmd_doctor_core(_ns(json=False))
        out = capsys.readouterr().out
        assert "Core Product Spine" in out
        assert "READY" in out


class TestDoctorCoreFromAnotherDirectory:
    """The doctor diagnoses the INSTALLATION, not the working directory.

    Operator dogfooding on 2026-08-25: run from ~/demo-remedy, `remedy doctor
    core` reported `fast_test_lane` and `full_test_lane` as blockers and the
    installation NOT READY, because both lanes were resolved as
    `Path("scripts/remedy_test_fast.sh")` — relative to the process working
    directory. The scripts were present in the Remedy checkout the whole time.
    """

    def test_lanes_resolve_outside_the_checkout(self, tmp_path, monkeypatch, capsys):
        monkeypatch.chdir(tmp_path)

        from apps.cli.commands.worker_facade_cmd import _cmd_doctor_core
        _cmd_doctor_core(_ns(json=True))
        out = json.loads(capsys.readouterr().out)

        by_name = {c["check"]: c for c in out["checks"]}
        assert by_name["fast_test_lane"]["ok"] is True
        assert by_name["full_test_lane"]["ok"] is True
        assert "fast_test_lane" not in out["blockers"]
        assert "full_test_lane" not in out["blockers"]

    def test_lane_detail_stays_installation_relative(self, tmp_path, monkeypatch, capsys):
        """An absolute detail would print the operator's home into `--json`."""
        monkeypatch.chdir(tmp_path)

        from apps.cli.commands.worker_facade_cmd import _cmd_doctor_core
        _cmd_doctor_core(_ns(json=True))
        out = json.loads(capsys.readouterr().out)

        by_name = {c["check"]: c for c in out["checks"]}
        assert by_name["fast_test_lane"]["detail"] == "scripts/remedy_test_fast.sh"
        assert by_name["full_test_lane"]["detail"] == "scripts/remedy_test_full.sh"


class TestDoctorCoreSafeErr:
    def test_private_paths_redacted(self, monkeypatch, capsys):
        import importlib
        orig = importlib.import_module

        def _boom(name, *a, **kw):
            if name == "apps.cli.commands.worker_facade_cmd":
                return orig(name, *a, **kw)
            if name == "packages.orchestration.run_contract":
                raise ImportError(
                    "No module at /home/alice/secret-project/packages/orchestration/run_contract"
                )
            return orig(name, *a, **kw)

        monkeypatch.setattr(importlib, "import_module", _boom)
        from apps.cli.commands.worker_facade_cmd import _cmd_doctor_core
        _cmd_doctor_core(_ns(json=True))
        out = json.loads(capsys.readouterr().out)
        raw = json.dumps(out)
        assert "/home/" not in raw
        assert "alice" not in raw

    def test_secrets_redacted(self, monkeypatch, capsys):
        import importlib
        orig = importlib.import_module

        def _boom(name, *a, **kw):
            if name == "apps.cli.commands.worker_facade_cmd":
                return orig(name, *a, **kw)
            if name == "packages.orchestration.config":
                raise ImportError("Failed: api_key=sk-live-abc123def token=tok_xyz")
            return orig(name, *a, **kw)

        monkeypatch.setattr(importlib, "import_module", _boom)
        from apps.cli.commands.worker_facade_cmd import _cmd_doctor_core
        _cmd_doctor_core(_ns(json=True))
        out = json.loads(capsys.readouterr().out)
        raw = json.dumps(out)
        assert "sk-live" not in raw
        assert "tok_xyz" not in raw
        assert "api_key=***" in raw

    def test_mnt_tmp_users_redacted(self, monkeypatch, capsys):
        import importlib
        orig = importlib.import_module

        def _boom(name, *a, **kw):
            if name == "apps.cli.commands.worker_facade_cmd":
                return orig(name, *a, **kw)
            if name == "packages.orchestration.run_contract":
                raise ImportError(
                    "Error at /mnt/data/x and /tmp/build/y and /Users/bob/.config/z"
                )
            return orig(name, *a, **kw)

        monkeypatch.setattr(importlib, "import_module", _boom)
        from apps.cli.commands.worker_facade_cmd import _cmd_doctor_core
        _cmd_doctor_core(_ns(json=True))
        out = json.loads(capsys.readouterr().out)
        raw = json.dumps(out)
        assert "/mnt/" not in raw
        assert "/tmp/" not in raw
        assert "/Users/" not in raw


# ---------------------------------------------------------------------------
# doctor core — F254 known-dead model ids
# ---------------------------------------------------------------------------

_ALIAS_TABLE_PATCH = "packages.orchestration.model_aliases.MODEL_ALIASES"
_GET_CONFIG_PATCH = "packages.orchestration.config.get_config"


def _dead_entry(model_id: str, reason: str = "retired by the provider",
                superseded: str = ""):
    from packages.orchestration.dead_model_list import DeadModelEntry
    return DeadModelEntry(id=model_id, reason=reason, superseded_by=superseded)


class _FakeConfig:
    """Only `get` — the one accessor the doctor uses on RemedyConfig."""

    def __init__(self, values):
        self._values = values

    def get(self, key):
        return self._values.get(key)


def a_builtin_model_id() -> str:
    """One model id that IS a built-in default of THIS build, read from the table.

    Not spelled as a literal. These tests make the doctor warn by declaring a
    built-in default dead, so the id has to be one the alias table currently
    holds. The F254 table is repointed whenever an operator retires a value —
    the first such repoint was 2026-08-25 — and a spelled id turned every one
    of these tests silently vacuous on that day: the fixture declared a string
    dead that no alias pointed at any more, so no warning fired.
    """
    from packages.orchestration.model_aliases import resolve_model_alias
    return resolve_model_alias("claude-flagship")


def _patch_dead_list(monkeypatch, entries, extra_ids=()):
    """Point the doctor's dead-model sources at fixtures.

    scripts/dead_models.json is shipped operator data and is never edited by a
    test; the loader is replaced instead, so the fixture cannot leak onto disk.
    """
    import packages.orchestration.dead_model_list as dml
    monkeypatch.setattr(dml, "load_dead_models", lambda path=None: tuple(entries))
    ids = frozenset(e.id for e in entries) | frozenset(extra_ids)
    monkeypatch.setattr(dml, "dead_model_ids", lambda path=None: ids)


class TestDoctorCoreDeadModels:
    @pytest.fixture(autouse=True)
    def _no_leaked_config_cache(self):
        """Leave the process-global config cache exactly as empty as found."""
        yield
        from packages.orchestration.config import reset_config
        reset_config()

    def test_warnings_key_present_and_is_a_list(self, capsys):
        from apps.cli.commands.worker_facade_cmd import _cmd_doctor_core
        _cmd_doctor_core(_ns(json=True))
        out = json.loads(capsys.readouterr().out)
        assert "warnings" in out
        assert isinstance(out["warnings"], list)

    def test_dead_id_leaves_ready_and_blockers_untouched(self, monkeypatch, capsys):
        """DECISION D13: a dead id warns, it never decides readiness.

        The comparison is against the SAME run with an empty dead list, so
        `ready` and `blockers` are pinned to what the other checks alone say.
        """
        from apps.cli.commands.worker_facade_cmd import _cmd_doctor_core

        _patch_dead_list(monkeypatch, [])
        _cmd_doctor_core(_ns(json=True))
        without_dead = json.loads(capsys.readouterr().out)

        _patch_dead_list(monkeypatch, [_dead_entry(a_builtin_model_id())])
        _cmd_doctor_core(_ns(json=True))
        with_dead = json.loads(capsys.readouterr().out)

        assert without_dead["warnings"] == []
        assert with_dead["warnings"], "a dead built-in default must warn"
        assert with_dead["ready"] == without_dead["ready"]
        assert with_dead["blockers"] == without_dead["blockers"]
        assert "dead_model_list" not in with_dead["blockers"]

    def test_dead_builtin_default_names_id_and_alias(self, monkeypatch, capsys):
        from apps.cli.commands.worker_facade_cmd import _cmd_doctor_core
        _patch_dead_list(monkeypatch, [_dead_entry("dead-flagship-id")])
        monkeypatch.setattr(_ALIAS_TABLE_PATCH, {
            "test-flagship": "dead-flagship-id",
            "test-workhorse": "live-id",
        })
        _cmd_doctor_core(_ns(json=True))
        out = json.loads(capsys.readouterr().out)
        hits = [w for w in out["warnings"] if w["warning"] == "dead_builtin_model"]
        assert len(hits) == 1
        assert "dead-flagship-id" in hits[0]["detail"]
        assert "test-flagship" in hits[0]["detail"], "must name the alias to repoint"
        assert "test-workhorse" not in hits[0]["detail"]
        # R-0215: the compact line carries the same three facts.
        assert "dead-flagship-id" in hits[0]["summary"]
        assert "test-flagship" in hits[0]["summary"], "must name the alias to repoint"
        assert "repoint" in hits[0]["summary"], "must name the fix"

    def test_dead_configured_id_names_the_config_key(self, monkeypatch, capsys):
        from apps.cli.commands.worker_facade_cmd import _cmd_doctor_core
        _patch_dead_list(monkeypatch, [_dead_entry("dead-configured-id")])
        monkeypatch.setattr(
            _GET_CONFIG_PATCH,
            lambda: _FakeConfig({"orchestrator.model": "dead-configured-id"}),
        )
        _cmd_doctor_core(_ns(json=True))
        out = json.loads(capsys.readouterr().out)
        hits = [w for w in out["warnings"] if w["warning"] == "dead_configured_model"]
        assert len(hits) == 1
        assert "orchestrator.model" in hits[0]["detail"]
        assert "dead-configured-id" in hits[0]["detail"]
        # R-0215: the compact line names the key that produced the id and the
        # fix, so text mode alone is enough to act on.
        assert "orchestrator.model" in hits[0]["summary"]
        assert "dead-configured-id" in hits[0]["summary"]
        assert "change orchestrator.model" in hits[0]["summary"]

    def test_unreadable_dead_list_is_a_failing_check_and_a_blocker(
            self, monkeypatch, capsys):
        """An unreadable list is a DEFECT, not an all-clear.

        "No dead models" and "I could not open the list" are opposite
        answers, so the read failure lands in `blockers`, not in `warnings`.
        """
        import packages.orchestration.dead_model_list as dml
        from apps.cli.commands.worker_facade_cmd import _cmd_doctor_core

        def _boom(path=None):
            raise dml.DeadModelListError("dead_models.json: unreadable")

        monkeypatch.setattr(dml, "load_dead_models", _boom)
        monkeypatch.setattr(dml, "dead_model_ids", _boom)
        _cmd_doctor_core(_ns(json=True))
        out = json.loads(capsys.readouterr().out)
        entry = [c for c in out["checks"] if c["check"] == "dead_model_list"]
        assert len(entry) == 1
        assert entry[0]["ok"] is False
        assert "dead_model_list" in out["blockers"]
        assert out["ready"] is False
        assert out["warnings"] == []

    def test_text_output_shows_warnings_without_claiming_not_ready(
            self, monkeypatch, capsys):
        from apps.cli.commands.worker_facade_cmd import _cmd_doctor_core
        _patch_dead_list(monkeypatch, [_dead_entry(a_builtin_model_id())])
        _cmd_doctor_core(_ns(json=False))
        out = capsys.readouterr().out
        assert "[WARN] dead_builtin_model:" in out
        assert a_builtin_model_id() in out
        assert "do not affect READY" in out
        assert "NOT READY" not in out

    def test_warning_states_operator_maintained_provenance(self, monkeypatch, capsys):
        """No false live indicator: the verdict is a data file, not a provider."""
        from apps.cli.commands.worker_facade_cmd import _cmd_doctor_core
        _patch_dead_list(monkeypatch, [_dead_entry(a_builtin_model_id())])
        _cmd_doctor_core(_ns(json=True))
        out = json.loads(capsys.readouterr().out)
        detail = out["warnings"][0]["detail"]
        assert "dead_models.json" in detail
        assert "operator-maintained" in detail
        assert "no provider was queried" in detail

    def test_provenance_survives_in_the_compact_text_rendering(
            self, monkeypatch, capsys):
        """R-0215: shortening the WORDING never drops the honesty clause.

        The compact summary is what text mode prints; a summary that omitted
        where the verdict came from would read as live provider knowledge,
        which is the one thing this feature must never imply.
        """
        from apps.cli.commands.worker_facade_cmd import _cmd_doctor_core
        _patch_dead_list(monkeypatch, [_dead_entry(a_builtin_model_id())])
        _cmd_doctor_core(_ns(json=True))
        out = json.loads(capsys.readouterr().out)
        summary = out["warnings"][0]["summary"]
        assert "dead_models.json" in summary
        assert "operator data" in summary
        assert "no provider queried" in summary

    def test_summary_is_materially_shorter_than_detail(self, monkeypatch, capsys):
        """R-0215: text mode is one compact line, not the whole record."""
        from apps.cli.commands.worker_facade_cmd import _cmd_doctor_core
        _patch_dead_list(monkeypatch, [
            _dead_entry(
                a_builtin_model_id(),
                reason="A May-2025 dated id several generations stale as of "
                       "Aug 2026; no replacement id is named here because "
                       "nothing in this repository states one.",
            ),
        ])
        _cmd_doctor_core(_ns(json=True))
        out = json.loads(capsys.readouterr().out)
        warning = out["warnings"][0]
        assert len(warning["summary"]) * 2 < len(warning["detail"]), (
            "the compact line must be far shorter than the full record"
        )

    def test_text_mode_prints_the_summary_and_not_the_recorded_reason(
            self, monkeypatch, capsys):
        """R-0215: the ~700-character wall stays out of the check list."""
        from apps.cli.commands.worker_facade_cmd import _cmd_doctor_core
        _patch_dead_list(monkeypatch, [
            _dead_entry(a_builtin_model_id(),
                        reason="RECORDED-REASON-SENTINEL"),
        ])
        _cmd_doctor_core(_ns(json=False))
        text = capsys.readouterr().out
        warn_lines = [ln for ln in text.splitlines() if "[WARN]" in ln]
        assert warn_lines
        assert "RECORDED-REASON-SENTINEL" not in text
        assert "--json" in text, "text mode must point at where the reason lives"
        assert max(len(ln) for ln in warn_lines) < 300, (
            "a warning line the operator cannot read is the defect R-0215 named"
        )

    def test_missing_replacement_is_not_repeated_after_the_reason(
            self, monkeypatch, capsys):
        """R-0215: say it once. The recorded reason already covers it.

        The reason is the authoritative statement; appending
        "No replacement id is recorded." after it said the same thing twice
        in one line. When there IS no reason to lean on, the statement is
        still made — see `test_config_extension_id_says_it_came_from_config`.
        """
        from apps.cli.commands.worker_facade_cmd import _cmd_doctor_core
        _patch_dead_list(monkeypatch, [
            _dead_entry(a_builtin_model_id(),
                        reason="retired; no replacement is named here",
                        superseded=""),
        ])
        _cmd_doctor_core(_ns(json=True))
        out = json.loads(capsys.readouterr().out)
        detail = out["warnings"][0]["detail"]
        assert "retired; no replacement is named here" in detail
        assert "No replacement id is recorded." not in detail

    def test_known_replacement_is_named(self, monkeypatch, capsys):
        from apps.cli.commands.worker_facade_cmd import _cmd_doctor_core
        _patch_dead_list(monkeypatch, [
            _dead_entry(a_builtin_model_id(), superseded="some-live-id"),
        ])
        _cmd_doctor_core(_ns(json=True))
        out = json.loads(capsys.readouterr().out)
        detail = out["warnings"][0]["detail"]
        assert "Recorded replacement: some-live-id." in detail
        assert "No replacement id is recorded." not in detail

    def test_config_extension_id_says_it_came_from_config(self, monkeypatch, capsys):
        """An id known dead only via doctor.dead_models has no shipped reason."""
        from apps.cli.commands.worker_facade_cmd import _cmd_doctor_core
        _patch_dead_list(monkeypatch, [], extra_ids=("dead-flagship-id",))
        monkeypatch.setattr(_ALIAS_TABLE_PATCH, {"test-flagship": "dead-flagship-id"})
        _cmd_doctor_core(_ns(json=True))
        out = json.loads(capsys.readouterr().out)
        detail = out["warnings"][0]["detail"]
        assert "doctor.dead_models" in detail
        assert "No replacement id is recorded." in detail

    def _dead_list_detail(self, out):
        entry = [c for c in out["checks"] if c["check"] == "dead_model_list"]
        assert len(entry) == 1
        return str(entry[0]["detail"])

    def test_dead_list_count_label_matches_what_it_counts(
            self, monkeypatch, capsys):
        """R-0215: the second number is config-ONLY ids, so say that.

        `dead_model_ids()` returns the UNION of shipped and configured, so
        subtracting the shipped count leaves the ids config added that were
        not shipped already. Calling that "configured dead ids" reported 0
        for an operator who had configured one.
        """
        from apps.cli.commands.worker_facade_cmd import _cmd_doctor_core

        # One shipped id, one config-only id: 1 + 1 = 2.
        _patch_dead_list(monkeypatch, [_dead_entry("shipped-dead-id")],
                         extra_ids=("config-dead-id",))
        _cmd_doctor_core(_ns(json=True))
        detail = self._dead_list_detail(json.loads(capsys.readouterr().out))
        assert detail == "1 shipped + 1 config-only dead ids (2 total)"

        # The operator re-lists an id Remedy already ships: it adds no id, and
        # the label now says so instead of claiming nothing was configured.
        _patch_dead_list(monkeypatch, [_dead_entry("shipped-dead-id")],
                         extra_ids=("shipped-dead-id",))
        _cmd_doctor_core(_ns(json=True))
        detail = self._dead_list_detail(json.loads(capsys.readouterr().out))
        assert detail == "1 shipped + 0 config-only dead ids (1 total)"


class TestShippedDefaultsAreNotOnTheShippedDeadList:
    """The shipped build warns about none of its OWN defaults.

    Operator decision 2026-08-25 (dogfooding): `claude-flagship` and
    `claude-workhorse` were repointed off the retired May-2025 ids that
    scripts/dead_models.json lists, so `remedy doctor core` no longer warns
    about Remedy's own built-in defaults. Read with the REAL loader and the
    REAL table — nothing is patched here — because the claim is about what
    this build ships, not about what a fixture can be made to say.
    """

    def test_no_builtin_default_is_on_the_shipped_dead_list(self):
        from packages.orchestration.dead_model_list import dead_model_ids
        from packages.orchestration.model_aliases import builtin_model_ids

        overlap = sorted(set(builtin_model_ids()) & set(dead_model_ids()))
        assert overlap == [], (
            f"built-in defaults still on the dead list: {overlap}"
        )

    def test_doctor_core_emits_no_dead_builtin_warning(self, capsys):
        from apps.cli.commands.worker_facade_cmd import _cmd_doctor_core

        _cmd_doctor_core(_ns(json=True))
        out = json.loads(capsys.readouterr().out)

        dead_builtin = [w for w in out["warnings"]
                        if w["warning"] == "dead_builtin_model"]
        assert dead_builtin == []

    def test_both_repointed_aliases_resolve_to_live_ids(self):
        from packages.orchestration.dead_model_list import dead_model_ids
        from packages.orchestration.model_aliases import resolve_model_alias

        dead = dead_model_ids()
        assert resolve_model_alias("claude-flagship") not in dead
        assert resolve_model_alias("claude-workhorse") not in dead


class TestCollectHandlers:
    def test_facade_in_collected(self):
        from apps.cli.commands import collect_all_handlers
        handlers = collect_all_handlers()
        for key in ("worker.doctor", "worker.add", "worker.disable",
                    "mission.run", "mission.report", "doctor.core"):
            assert key in handlers, f"{key} missing from collect_all_handlers"


class TestWorkerListOptions:
    def test_limit_caps_returned_workers(self, capsys):
        from apps.cli.commands import collect_all_handlers
        collect_all_handlers()["worker.list"](_ns(json=True, limit="1"))
        data = json.loads(capsys.readouterr().out)
        assert len(data["providers"]) == 1

    def test_unknown_sort_field_exits_nonzero(self):
        from apps.cli.commands import collect_all_handlers
        with pytest.raises(SystemExit) as exc:
            collect_all_handlers()["worker.list"](_ns(json=True, sort="bogus"))
        assert exc.value.code == 1
