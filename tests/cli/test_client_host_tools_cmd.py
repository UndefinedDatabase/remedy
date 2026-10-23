"""`remedy client show`, `grant-host-tools` and `revoke-host-tools`: the operator's client registry on
this machine's command line (operator amendment amend1023-universe-trust, DECISION amend1023 D6)."""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from apps.cli.commands.client_cmd import _cmd_client_host_tools, _cmd_client_show
from packages.orchestration.api_clients import api_clients_path
from packages.orchestration.public_api import PUBLIC_API_EXCLUDED_COMMANDS
from packages.orchestration.public_api_routes import PUBLIC_API_ROUTES

TOKEN = "s" * 40


@pytest.fixture()
def registry(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    path = api_clients_path(tmp_path)
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps({"clients": [
        {"name": "orb-universe", "token": TOKEN, "projects": ["universe-chat"],
         "max_total_tokens": None, "max_provider_calls": None, "may_apply": True}]}), encoding="utf-8")
    os.chmod(path, 0o600)
    return path


def test_show_lists_the_policy_and_the_fingerprint_never_the_token(registry, capsys):
    _cmd_client_show(None, json_output=True)
    out = capsys.readouterr().out
    [entry] = json.loads(out)["clients"]
    assert entry["name"] == "orb-universe" and entry["host_tools"] is False
    assert entry["token_fp"].startswith("tf:") and TOKEN not in out


def test_grant_then_revoke_is_what_show_reads(registry, capsys):
    _cmd_client_host_tools("orb-universe", granted=True, json_output=True)
    assert json.loads(capsys.readouterr().out)["client"]["host_tools"] is True
    _cmd_client_show("orb-universe", json_output=False)
    assert "host_tools true" in capsys.readouterr().out
    _cmd_client_host_tools("orb-universe", granted=False, json_output=False)
    assert capsys.readouterr().out.strip() == "orb-universe: host_tools false"
    assert "host_tools" not in registry.read_text(encoding="utf-8")


def test_an_unknown_client_exits_3_and_changes_nothing(registry, capsys):
    before = registry.read_bytes()
    with pytest.raises(SystemExit) as exited:
        _cmd_client_host_tools("orb-nobody", granted=True, json_output=True)
    assert exited.value.code == 3
    assert json.loads(capsys.readouterr().out)["error"] == "client_not_found"
    assert registry.read_bytes() == before
    with pytest.raises(SystemExit) as shown:
        _cmd_client_show("orb-nobody", json_output=True)
    assert shown.value.code == 3


def test_the_property_is_never_granted_over_http():
    assert {"client.grant-host-tools", "client.revoke-host-tools"} <= set(PUBLIC_API_EXCLUDED_COMMANDS)
    assert not any(route.twin.startswith("client.") and "host-tools" in route.twin
                   for route in PUBLIC_API_ROUTES)
