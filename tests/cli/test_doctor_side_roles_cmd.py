"""`remedy doctor side-roles [--check] [--json]` (F113 T003b, DECISION F113 D3): where each mapped side
role runs and why; `--check` spot-checks each, flips a role that fails and exits 1, and `remedy status`
shows the flip.

A temporary data root; the configuration from real TOML; the endpoint's model answers through a fake
`ollama` client.
"""
from __future__ import annotations

import json
import sys
import types
from types import SimpleNamespace

import pytest

from apps.cli.commands.status_cmd import _print_status_text
from apps.cli.grouped import main as grouped_main
from packages.orchestration.local_endpoints import LocalEndpointProbes
from packages.orchestration.side_role_quality import SUMMARY_SPOT_CHECKS
from tests.orchestration.test_local_endpoints import configure_toml

TABLES = ('[remedy.local_routing.endpoints.box]\nbase_url = "http://127.0.0.1:9"\nmodel = "muse-glimmer"\n'
          '[remedy.local_routing.side_roles]\nsummary = "box"\n')


@pytest.fixture
def mapped(monkeypatch, tmp_path):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    configure_toml(monkeypatch, tmp_path, TABLES)
    monkeypatch.setattr("packages.orchestration.local_endpoints.LOCAL_ENDPOINT_PROBES",
                        LocalEndpointProbes(list_models=lambda url: ["muse-glimmer:latest"]))


def model_answers(monkeypatch, *, drop: str) -> None:
    """The endpoint's model names every seeded fact of the case it is asked about, except `drop`."""
    class FakeClient:
        def __init__(self, host=None, timeout=None):
            pass

        def chat(self, **request):
            prompt = request["messages"][-1]["content"]
            facts = [f for case in SUMMARY_SPOT_CHECKS for f in case.facts if f in prompt and f != drop]
            content = json.dumps({"l1": "Touches " + ", ".join(facts), "l2": []})
            return types.SimpleNamespace(message=types.SimpleNamespace(content=content))

    module = types.ModuleType("ollama")
    module.Client = FakeClient
    monkeypatch.setitem(sys.modules, "ollama", module)


def status_text(capsys) -> list[str]:
    capsys.readouterr()
    _print_status_text(project_slug=None, scope=SimpleNamespace(all_projects=False), jobs=[], degraded=False,
                       by_state={}, skipped_files=[], jobs_next="-", decisions_open=0, decisions_next="-",
                       runtime_status="-", runtime_warning=None, runtime_next="-", stops_pending=0, stops_next="-")
    return capsys.readouterr().out.splitlines()


def test_without_a_check_it_names_each_role_and_writes_nothing(mapped, capsys, tmp_path):
    grouped_main(["doctor", "side-roles"])
    assert capsys.readouterr().out.splitlines() == [
        "Side roles:", "  summary on box (muse-glimmer): not spot-checked for this endpoint and model yet"]
    assert not (tmp_path / "data" / "side_roles").exists()


def test_a_failing_check_flips_the_role_exits_one_and_status_shows_it(mapped, monkeypatch, capsys):
    model_answers(monkeypatch, drop="retry_limit")
    with pytest.raises(SystemExit) as raised:
        grouped_main(["doctor", "side-roles", "--check"])
    assert raised.value.code == 1
    out = capsys.readouterr()
    assert "of summary on box (muse-glimmer): failed: failed cases: removed-setting" in out.out
    assert "FLIPPED to its own model" in out.out
    lines = status_text(capsys)
    assert lines[lines.index("Side roles:") + 1].startswith("  summary on box (muse-glimmer): FLIPPED")


def test_a_passing_check_exits_zero_and_records_it(mapped, monkeypatch, capsys):
    model_answers(monkeypatch, drop="")
    grouped_main(["doctor", "side-roles", "--check", "--json"])
    envelope = json.loads(capsys.readouterr().out)
    assert envelope["ok"] is True
    (record,) = envelope["checks"]
    assert (record["role"], record["outcome"]) == ("summary", "passed")
    assert envelope["side_roles"][0].startswith("summary on box (muse-glimmer): passing since spot check")


def test_a_failing_check_in_json_is_the_failure_envelope(mapped, monkeypatch, capsys):
    model_answers(monkeypatch, drop="compute_invoice_total")
    with pytest.raises(SystemExit) as raised:
        grouped_main(["doctor", "side-roles", "--check", "--json"])
    assert raised.value.code == 1
    envelope = json.loads(capsys.readouterr().out)
    assert (envelope["ok"], envelope["error"]) == (False, "spot_check_failed")
    assert envelope["checks"][0]["outcome"] == "failed"


def test_an_unmapped_project_says_so_and_status_prints_no_side_role_line(monkeypatch, tmp_path, capsys):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    configure_toml(monkeypatch, tmp_path, "")
    grouped_main(["doctor", "side-roles"])
    assert capsys.readouterr().out.splitlines() == ["Side roles: none is mapped to a local endpoint"]
    assert "Side roles:" not in status_text(capsys)
