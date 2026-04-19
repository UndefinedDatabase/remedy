"""
Tests for OllamaPlanner configuration and env var precedence.

No live Ollama server required — only __init__ and configuration are tested.
"""

from __future__ import annotations

import pytest


# ---------------------------------------------------------------------------
# Model resolution precedence (_resolve_model)
# ---------------------------------------------------------------------------

def test_constructor_arg_takes_priority(monkeypatch):
    monkeypatch.setenv("REMEDY_OLLAMA_PLANNER_MODEL", "env-planner-model")
    monkeypatch.setenv("REMEDY_OLLAMA_MODEL", "env-generic-model")
    from packages.providers.ollama_planner.provider import OllamaPlanner
    planner = OllamaPlanner(model="explicit-model")
    assert planner.model == "explicit-model"


def test_planner_env_var_takes_priority_over_generic(monkeypatch):
    monkeypatch.setenv("REMEDY_OLLAMA_PLANNER_MODEL", "planner-specific")
    monkeypatch.setenv("REMEDY_OLLAMA_MODEL", "generic-model")
    from packages.providers.ollama_planner.provider import OllamaPlanner
    planner = OllamaPlanner()
    assert planner.model == "planner-specific"


def test_fallback_to_generic_env_var(monkeypatch):
    monkeypatch.delenv("REMEDY_OLLAMA_PLANNER_MODEL", raising=False)
    monkeypatch.setenv("REMEDY_OLLAMA_MODEL", "generic-fallback")
    from packages.providers.ollama_planner.provider import OllamaPlanner
    planner = OllamaPlanner()
    assert planner.model == "generic-fallback"


def test_fallback_to_default_when_no_env_vars(monkeypatch):
    monkeypatch.delenv("REMEDY_OLLAMA_PLANNER_MODEL", raising=False)
    monkeypatch.delenv("REMEDY_OLLAMA_MODEL", raising=False)
    from packages.providers.ollama_planner.provider import OllamaPlanner
    planner = OllamaPlanner()
    assert planner.model == "qwen3-coder-next"


# ---------------------------------------------------------------------------
# Host resolution
# ---------------------------------------------------------------------------

def test_default_host(monkeypatch):
    monkeypatch.delenv("REMEDY_OLLAMA_HOST", raising=False)
    from packages.providers.ollama_planner.provider import OllamaPlanner
    planner = OllamaPlanner()
    assert planner.host == "http://localhost:11434"


def test_host_from_env_var(monkeypatch):
    monkeypatch.setenv("REMEDY_OLLAMA_HOST", "http://remote:11434")
    from packages.providers.ollama_planner.provider import OllamaPlanner
    planner = OllamaPlanner()
    assert planner.host == "http://remote:11434"


def test_constructor_host_overrides_env(monkeypatch):
    monkeypatch.setenv("REMEDY_OLLAMA_HOST", "http://env-host:11434")
    from packages.providers.ollama_planner.provider import OllamaPlanner
    planner = OllamaPlanner(host="http://explicit:11434")
    assert planner.host == "http://explicit:11434"


# ---------------------------------------------------------------------------
# Optional generation parameters
# ---------------------------------------------------------------------------

def test_temperature_from_env_var(monkeypatch):
    monkeypatch.setenv("REMEDY_OLLAMA_PLANNER_TEMPERATURE", "0.3")
    from packages.providers.ollama_planner.provider import OllamaPlanner
    planner = OllamaPlanner()
    assert planner.temperature == pytest.approx(0.3)


def test_num_predict_from_env_var(monkeypatch):
    monkeypatch.setenv("REMEDY_OLLAMA_PLANNER_NUM_PREDICT", "512")
    from packages.providers.ollama_planner.provider import OllamaPlanner
    planner = OllamaPlanner()
    assert planner.num_predict == 512


def test_temperature_unset_by_default(monkeypatch):
    monkeypatch.delenv("REMEDY_OLLAMA_PLANNER_TEMPERATURE", raising=False)
    from packages.providers.ollama_planner.provider import OllamaPlanner
    planner = OllamaPlanner()
    assert planner.temperature is None


def test_num_predict_unset_by_default(monkeypatch):
    monkeypatch.delenv("REMEDY_OLLAMA_PLANNER_NUM_PREDICT", raising=False)
    from packages.providers.ollama_planner.provider import OllamaPlanner
    planner = OllamaPlanner()
    assert planner.num_predict is None


def test_constructor_temperature_overrides_env(monkeypatch):
    monkeypatch.setenv("REMEDY_OLLAMA_PLANNER_TEMPERATURE", "0.9")
    from packages.providers.ollama_planner.provider import OllamaPlanner
    planner = OllamaPlanner(temperature=0.1)
    assert planner.temperature == pytest.approx(0.1)
