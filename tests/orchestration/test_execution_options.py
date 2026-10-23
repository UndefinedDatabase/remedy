"""`execution_options`: what a client may choose for an execution, decided and answered by the server (exec-1017 D6)."""
from __future__ import annotations

import json
import os

import pytest

from apps.cli.client_interface_execution import CLIENT_EXECUTION_ANSWER_KEYS
from packages.orchestration import execution_options as EO
from packages.orchestration.public_api_routes import PUBLIC_API_ROUTES


@pytest.fixture()
def offline_ollama(monkeypatch):
    """No test reaches a network: the Ollama endpoint answers two models, one an embedding."""
    monkeypatch.setattr("packages.orchestration.pi_provider._ollama_models",
                        lambda host: ["muse-glimmer:latest", "nomic-embed-text:latest"])


def test_the_offer_names_every_role_and_never_a_secret_or_the_home_directory(offline_ollama, monkeypatch, tmp_path):
    secret = "sk-ant-api03-" + "Q" * 40
    monkeypatch.setenv("ANTHROPIC_API_KEY", secret)
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))

    offer = EO.execution_capabilities()

    assert sorted(offer) == sorted(CLIENT_EXECUTION_ANSWER_KEYS)
    assert sorted(offer["roles"]) == ["builder", "planner", "repair", "reviewer"]
    text = json.dumps(offer)
    assert secret not in text and os.path.expanduser("~") not in text
    builder = {p["id"]: p for p in offer["roles"]["builder"]["providers"]}
    assert builder["claude"]["available"] is True                 # that a key is set, not the key
    assert builder["pi"]["models"] == ["muse-glimmer:latest"]     # embeddings serve no role
    assert offer["review_report"]["body_flag"] == "capture_review" and "capture_review" in offer["order_flags"]


def test_the_offer_names_both_budget_profiles_and_each_providers_class(offline_ollama, monkeypatch, tmp_path):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    for name in [n for n in os.environ if n.startswith("REMEDY_BUDGET_")]:
        monkeypatch.delenv(name)
    monkeypatch.setattr("packages.orchestration.config._DEFAULT_USER_PATH", tmp_path / "user.toml")
    monkeypatch.setattr("packages.orchestration.config._DEFAULT_PROJECT_PATH", tmp_path / "remedy.toml")

    offer = EO.execution_capabilities()

    assert offer["budgets"]["profiles"] == {
        "local": {"max_total_tokens": 1500000, "max_provider_calls": 200, "max_wall_clock_minutes": 480},
        "paid": {"max_total_tokens": None, "max_provider_calls": None, "max_wall_clock_minutes": None,
                 "max_cost_usd": None},
    }
    for role in offer["roles"].values():
        for provider in role["providers"]:
            assert provider["class"] == ("local" if provider["id"] in ("pi", "ollama") else "paid")


def test_the_claude_code_cli_is_never_offered_over_http_and_says_why(offline_ollama, tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    for role in ("builder", "reviewer", "repair", "planner"):
        [cli] = [p for p in EO.execution_capabilities()["roles"][role]["providers"] if p["id"] == "claude-cli"]
        assert cli["offered_over_http"] is False and cli["not_offered_reason"]
        assert "outside the tool sandbox" in cli["isolation"]


@pytest.mark.parametrize(("body", "fragment"), [
    ({"builder_provider": "claude-cli"}, "outside Remedy's tool sandbox"),
    ({"reviewer_provider": "claude-cli"}, "outside Remedy's tool sandbox"),
    ({"builder_provider": "ollama"}, "not a provider of this role"),
    ({"builder_provider": "claude"}, "not available on this server"),
])
def test_a_provider_that_cannot_serve_is_refused_before_anything_starts(monkeypatch, body, fragment):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    assert fragment in EO.remote_provider_refusal(body)


def test_an_offered_available_provider_and_no_provider_are_accepted():
    assert EO.remote_provider_refusal({"builder_provider": "fake", "reviewer_provider": "ollama"}) == ""
    assert EO.remote_provider_refusal({}) == ""


def test_the_route_answers_the_command(offline_ollama, tmp_path, monkeypatch):
    from packages.orchestration.public_api import answer_public_api_get

    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    status, body, _headers = answer_public_api_get("/api/v1/execution")[:3]
    assert status == 200 and body["ok"] is True and "roles" in body


def test_the_observability_list_names_registered_get_routes(offline_ollama):
    get_routes = {f"{r.method} {r.path}" for r in PUBLIC_API_ROUTES if r.method == "GET"}
    for entry in EO.EXECUTION_OBSERVABILITY_ROUTES:
        assert entry in get_routes
    assert "GET /api/v1/now" in EO.EXECUTION_OBSERVABILITY_ROUTES
    assert "GET /api/v1/jobs/{job}/insight" in EO.EXECUTION_OBSERVABILITY_ROUTES


# -- amend1023 D6: a client the operator granted `host_tools` ---------------------------------


def _client(host_tools: bool):
    from packages.orchestration.api_clients import ApiClient

    return ApiClient(name="orb-test", token="t" * 40, projects=("demo",), max_total_tokens=None,
                     max_provider_calls=None, may_apply=False, host_tools=host_tools)


def test_a_client_granted_host_tools_is_offered_the_claude_code_cli_and_the_planner(
        offline_ollama, tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    offer = EO.execution_capabilities(_client(True))
    assert offer["host_tools"] is True
    for role in ("builder", "reviewer", "repair", "planner"):
        [cli] = [p for p in offer["roles"][role]["providers"] if p["id"] == "claude-cli"]
        assert cli["offered_over_http"] is True and cli["not_offered_reason"] == ""
    assert offer["roles"]["planner"]["selectable_over_http"] is True
    assert offer["roles"]["repair"]["selectable_over_http"] is False
    assert [p["id"] for p in offer["roles"]["planner"]["providers"] if p["offered_over_http"]] == [
        "ollama", "claude-cli"]
    assert [p["id"] for p in offer["roles"]["repair"]["providers"] if p["offered_over_http"]] == ["claude-cli"]


def test_every_other_caller_reads_the_offer_unchanged_and_the_reason_names_the_property(
        offline_ollama, tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    server, plain = EO.execution_capabilities(), EO.execution_capabilities(_client(False))
    assert server == plain and plain["host_tools"] is False
    assert plain["roles"]["planner"]["selectable_over_http"] is False
    for role in ("builder", "reviewer", "repair", "planner"):
        [cli] = [p for p in plain["roles"][role]["providers"] if p["id"] == "claude-cli"]
        assert cli["offered_over_http"] is False and "host_tools" in cli["not_offered_reason"]


def test_the_refusal_follows_the_client(monkeypatch):
    import shutil

    monkeypatch.setattr(shutil, "which", lambda name: f"/usr/bin/{name}")
    for body in ({"builder_provider": "claude-cli"}, {"reviewer_provider": "claude-cli"},
                 {"planner_provider": "ollama"}, {"planner_provider": "claude-cli"}):
        assert EO.remote_provider_refusal(body, _client(True)) == ""
        assert "host_tools" in EO.remote_provider_refusal(body, _client(False))
        assert EO.remote_provider_refusal(body) == EO.remote_provider_refusal(body, _client(False))
    assert "not a provider of this role" in EO.remote_provider_refusal({"planner_provider": "pi"}, _client(True))


def test_a_claude_code_cli_that_is_not_installed_is_refused_as_not_available(monkeypatch):
    import shutil

    monkeypatch.setattr(shutil, "which", lambda name: None)
    assert "not available on this server" in EO.remote_provider_refusal(
        {"builder_provider": "claude-cli"}, _client(True))


def test_the_route_answers_the_calling_clients_offer(offline_ollama, tmp_path, monkeypatch):
    from packages.orchestration.public_api import answer_public_api_get

    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    status, body, _headers = answer_public_api_get("/api/v1/execution", "", _client(True))
    assert status == 200 and body["host_tools"] is True
    status, body, _headers = answer_public_api_get("/api/v1/execution", "", _client(False))
    assert status == 200 and body["host_tools"] is False
