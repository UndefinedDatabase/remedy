"""CLI subprocess tests for `remedy config` commands."""

from __future__ import annotations

import json
import subprocess
import sys

import pytest

_CLI = [sys.executable, "-m", "apps.cli.grouped"]


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
        data = json.loads(r.stdout)
        assert isinstance(data, list)
        keys = {e["key"] for e in data}
        assert "ollama.host" in keys
        assert "data_dir" in keys

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
        r = subprocess.run([*_CLI, "config", "init"], capture_output=True, text=True, timeout=30, cwd=str(tmp_path))
        assert r.returncode == 1
        assert "already exists" in r.stderr
