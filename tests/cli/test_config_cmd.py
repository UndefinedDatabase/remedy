"""CLI subprocess tests for `remedy config` commands."""

from __future__ import annotations

import json
import os
import subprocess
import sys

import pytest

_CLI = [sys.executable, "-m", "apps.cli.grouped"]
_ENV = {**os.environ, "PYTHONPATH": os.getcwd()}


@pytest.mark.subprocess
class TestConfigCli:

    def test_config_list(self):
        r = subprocess.run([*_CLI, "config", "list"], capture_output=True, text=True, timeout=30)
        assert r.returncode == 0
        assert "ollama.host" in r.stdout
        assert "data_dir" in r.stdout

    def test_config_list_json(self):
        r = subprocess.run([*_CLI, "config", "list", "--json"], capture_output=True, text=True, timeout=30)
        assert r.returncode == 0
        body = json.loads(r.stdout)
        # F283 R19 C5 (DECISION F283 D10 (4)) — the old bare list is now the
        # envelope's `entries` key.
        assert body["schema_version"] == 1
        assert body["ok"] is True
        entries = body["entries"]
        assert isinstance(entries, list)
        keys = {e["key"] for e in entries}
        assert "ollama.host" in keys
        assert "data_dir" in keys
        assert "ui.host" in keys

    def test_config_show_alias(self):
        r = subprocess.run([*_CLI, "config", "show", "--json"], capture_output=True, text=True, timeout=30)
        assert r.returncode == 0
        body = json.loads(r.stdout)
        entries = body["entries"]
        assert isinstance(entries, list)
        assert any(e["key"] == "ollama.host" for e in entries)

    def test_config_get(self):
        r = subprocess.run([*_CLI, "config", "get", "ollama.host"], capture_output=True, text=True, timeout=30)
        assert r.returncode == 0
        assert "ollama.host" in r.stdout
        assert "http://localhost:11434" in r.stdout

    def test_config_get_json(self):
        r = subprocess.run([*_CLI, "config", "get", "ollama.host", "--json"], capture_output=True, text=True, timeout=30)
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert data["key"] == "ollama.host"
        assert data["value"] == "http://localhost:11434"

    def test_config_get_unknown_key(self):
        r = subprocess.run([*_CLI, "config", "get", "nonexistent.key"], capture_output=True, text=True, timeout=30)
        assert r.returncode != 0

    def test_config_get_unknown_key_text_mode_bytes_are_unchanged(self):
        """F283 R12 C4 (DECISION F283 D7) — text mode is UNTOUCHED: the bare sentence
        this line always printed, with no `Error: ` prefix, byte for byte."""
        r = subprocess.run([*_CLI, "config", "get", "nonexistent.key"], capture_output=True, text=True, timeout=30)
        assert r.returncode == 1
        assert r.stdout == ""
        assert r.stderr == "Unknown config key: nonexistent.key\n"

    def test_config_get_unknown_key_json_answers_the_envelope(self):
        """F283 R12 C4 (DECISION F283 D7) — under `--json` this line used to print the
        same bare sentence to stderr regardless of the flag; it now answers the
        envelope on stdout instead, token `unknown_config_key`."""
        r = subprocess.run(
            [*_CLI, "config", "get", "nonexistent.key", "--json"],
            capture_output=True, text=True, timeout=30,
        )
        assert r.returncode == 1
        assert r.stderr == ""
        data = json.loads(r.stdout)
        assert data["schema_version"] == 1
        assert data["ok"] is False
        assert data["error"] == "unknown_config_key"
        assert data["message"] == "Unknown config key: nonexistent.key"

    def test_config_sources(self):
        r = subprocess.run([*_CLI, "config", "sources"], capture_output=True, text=True, timeout=30)
        assert r.returncode == 0
        assert "project:" in r.stdout
        assert "user:" in r.stdout

    def test_config_sources_json(self):
        r = subprocess.run([*_CLI, "config", "sources", "--json"], capture_output=True, text=True, timeout=30)
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert "project_path" in data
        assert "user_path" in data

    def test_config_validate(self):
        r = subprocess.run([*_CLI, "config", "validate"], capture_output=True, text=True, timeout=30)
        assert r.returncode == 0
        assert "OK" in r.stdout or "warning" in r.stdout.lower()

    def test_config_validate_json(self):
        r = subprocess.run([*_CLI, "config", "validate", "--json"], capture_output=True, text=True, timeout=30)
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert "valid" in data
        assert "warnings" in data

    def test_config_init_refuses_existing(self, tmp_path):
        existing = tmp_path / "remedy.toml"
        existing.write_text("[remedy]\n")
        r = subprocess.run(
            [*_CLI, "config", "init", "--path", str(existing)],
            capture_output=True, text=True, timeout=30, env=_ENV,
        )
        assert r.returncode == 1
        assert "already exists" in r.stderr or "already exists" in r.stdout

    def test_config_init_refuses_existing_json_answers_the_envelope(self, tmp_path):
        """F283 R12 C4 (DECISION F283 D7) — `config_file_exists`, the second of the
        two already-branched hand-rolled-JSON sites this round moves onto `fail()`."""
        existing = tmp_path / "remedy.toml"
        existing.write_text("[remedy]\n")
        r = subprocess.run(
            [*_CLI, "config", "init", "--path", str(existing), "--json"],
            capture_output=True, text=True, timeout=30, env=_ENV,
        )
        assert r.returncode == 1
        assert r.stderr == ""
        data = json.loads(r.stdout)
        assert data["schema_version"] == 1
        assert data["ok"] is False
        assert data["error"] == "config_file_exists"
        assert "already exists" in data["message"]

    def test_config_init_json(self, tmp_path):
        target = tmp_path / "new_remedy.toml"
        r = subprocess.run(
            [*_CLI, "config", "init", "--path", str(target), "--json"],
            capture_output=True, text=True, timeout=30, env=_ENV,
        )
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert "created" in data
        assert target.exists()

    def test_config_set_rejects_unknown(self, tmp_path):
        """F283 R12 C4 (DECISION F283 D7) — the bare `print(str(exc))` line moves onto
        `fail()`; the envelope's `error` key is now the TOKEN `invalid_config_value`,
        and the sentence that used to fill it moves to `message`."""
        r = subprocess.run(
            [*_CLI, "config", "set", "bogus.key", "val", "--path", str(tmp_path / "r.toml"), "--json"],
            capture_output=True, text=True, timeout=30, env=_ENV,
        )
        assert r.returncode == 1
        assert r.stderr == ""
        data = json.loads(r.stdout)
        assert data["schema_version"] == 1
        assert data["ok"] is False
        assert data["error"] == "invalid_config_value"
        assert "Unknown" in data["message"]

    def test_config_set_json(self, tmp_path):
        target = tmp_path / "remedy.toml"
        r = subprocess.run(
            [*_CLI, "config", "set", "ollama.host", "http://custom:11434", "--path", str(target), "--json"],
            capture_output=True, text=True, timeout=30, env=_ENV,
        )
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert data["key"] == "ollama.host"
        assert data["value"] == "http://custom:11434"

    def test_config_list_limit(self):
        r = subprocess.run(
            [*_CLI, "config", "list", "--json", "--limit", "1"],
            capture_output=True, text=True, timeout=30,
        )
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert len(data["entries"]) == 1

    def test_config_list_unknown_sort_field_exits_nonzero(self):
        """F283 R12 C3 — `invalid_list_option` used to print to stderr regardless of
        `--json`; the plain rule now answers the envelope on stdout when the flag
        holds."""
        r = subprocess.run(
            [*_CLI, "config", "list", "--json", "--sort", "bogus"],
            capture_output=True, text=True, timeout=30,
        )
        assert r.returncode != 0
        assert r.stderr == ""
        data = json.loads(r.stdout)
        assert data["schema_version"] == 1
        assert data["ok"] is False
        assert data["error"] == "invalid_list_option"
        assert "unknown --sort field" in data["message"]
