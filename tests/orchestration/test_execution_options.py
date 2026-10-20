"""`execution_options`: what a client may choose for an execution, decided and answered by the server (exec-1017 D6)."""
from __future__ import annotations

import json
import os

import pytest

from apps.cli.client_interface_execution import CLIENT_EXECUTION_ANSWER_KEYS
from packages.orchestration import execution_options as EO


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
