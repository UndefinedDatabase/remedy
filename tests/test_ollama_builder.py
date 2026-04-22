"""
Tests for OllamaBuilder configuration and env var precedence.

No live Ollama server required — only __init__ and configuration are tested.
"""

from __future__ import annotations

import pytest


# ---------------------------------------------------------------------------
# Model resolution precedence
# ---------------------------------------------------------------------------

def test_default_model(monkeypatch):
    monkeypatch.delenv("REMEDY_OLLAMA_BUILDER_MODEL", raising=False)
    monkeypatch.delenv("REMEDY_OLLAMA_MODEL", raising=False)
    from packages.providers.ollama_builder.provider import OllamaBuilder
    builder = OllamaBuilder()
    assert builder.model == "qwen3-coder-next"


def test_builder_env_var(monkeypatch):
    monkeypatch.setenv("REMEDY_OLLAMA_BUILDER_MODEL", "builder-model")
    monkeypatch.delenv("REMEDY_OLLAMA_MODEL", raising=False)
    from packages.providers.ollama_builder.provider import OllamaBuilder
    builder = OllamaBuilder()
    assert builder.model == "builder-model"


def test_generic_env_var_fallback(monkeypatch):
    monkeypatch.delenv("REMEDY_OLLAMA_BUILDER_MODEL", raising=False)
    monkeypatch.setenv("REMEDY_OLLAMA_MODEL", "generic-fallback")
    from packages.providers.ollama_builder.provider import OllamaBuilder
    builder = OllamaBuilder()
    assert builder.model == "generic-fallback"


def test_builder_env_var_takes_priority_over_generic(monkeypatch):
    monkeypatch.setenv("REMEDY_OLLAMA_BUILDER_MODEL", "builder-specific")
    monkeypatch.setenv("REMEDY_OLLAMA_MODEL", "generic-model")
    from packages.providers.ollama_builder.provider import OllamaBuilder
    builder = OllamaBuilder()
    assert builder.model == "builder-specific"


def test_constructor_arg_takes_priority(monkeypatch):
    monkeypatch.setenv("REMEDY_OLLAMA_BUILDER_MODEL", "builder-specific")
    monkeypatch.setenv("REMEDY_OLLAMA_MODEL", "generic-model")
    from packages.providers.ollama_builder.provider import OllamaBuilder
    builder = OllamaBuilder(model="explicit-model")
    assert builder.model == "explicit-model"


# ---------------------------------------------------------------------------
# Host resolution
# ---------------------------------------------------------------------------

def test_default_host(monkeypatch):
    monkeypatch.delenv("REMEDY_OLLAMA_HOST", raising=False)
    from packages.providers.ollama_builder.provider import OllamaBuilder
    builder = OllamaBuilder()
    assert builder.host == "http://localhost:11434"


def test_host_from_env(monkeypatch):
    monkeypatch.setenv("REMEDY_OLLAMA_HOST", "http://remote:11434")
    from packages.providers.ollama_builder.provider import OllamaBuilder
    builder = OllamaBuilder()
    assert builder.host == "http://remote:11434"


def test_constructor_host_overrides_env(monkeypatch):
    monkeypatch.setenv("REMEDY_OLLAMA_HOST", "http://env-host:11434")
    from packages.providers.ollama_builder.provider import OllamaBuilder
    builder = OllamaBuilder(host="http://explicit:11434")
    assert builder.host == "http://explicit:11434"


# ---------------------------------------------------------------------------
# Optional generation parameters
# ---------------------------------------------------------------------------

def test_temperature_from_env(monkeypatch):
    monkeypatch.setenv("REMEDY_OLLAMA_BUILDER_TEMPERATURE", "0.5")
    from packages.providers.ollama_builder.provider import OllamaBuilder
    builder = OllamaBuilder()
    assert builder.temperature == pytest.approx(0.5)


def test_num_predict_from_env(monkeypatch):
    monkeypatch.setenv("REMEDY_OLLAMA_BUILDER_NUM_PREDICT", "200")
    from packages.providers.ollama_builder.provider import OllamaBuilder
    builder = OllamaBuilder()
    assert builder.num_predict == 200


def test_temperature_unset_by_default(monkeypatch):
    monkeypatch.delenv("REMEDY_OLLAMA_BUILDER_TEMPERATURE", raising=False)
    from packages.providers.ollama_builder.provider import OllamaBuilder
    builder = OllamaBuilder()
    assert builder.temperature is None


def test_num_predict_unset_by_default(monkeypatch):
    monkeypatch.delenv("REMEDY_OLLAMA_BUILDER_NUM_PREDICT", raising=False)
    from packages.providers.ollama_builder.provider import OllamaBuilder
    builder = OllamaBuilder()
    assert builder.num_predict is None


def test_constructor_temperature_overrides_env(monkeypatch):
    monkeypatch.setenv("REMEDY_OLLAMA_BUILDER_TEMPERATURE", "0.9")
    from packages.providers.ollama_builder.provider import OllamaBuilder
    builder = OllamaBuilder(temperature=0.1)
    assert builder.temperature == pytest.approx(0.1)


# ---------------------------------------------------------------------------
# Env var validation errors
# ---------------------------------------------------------------------------

def test_invalid_temperature_raises_with_var_name(monkeypatch):
    monkeypatch.setenv("REMEDY_OLLAMA_BUILDER_TEMPERATURE", "not-a-float")
    from packages.providers.ollama_builder.provider import OllamaBuilder
    with pytest.raises(ValueError, match="REMEDY_OLLAMA_BUILDER_TEMPERATURE"):
        OllamaBuilder()


def test_invalid_num_predict_raises_with_var_name(monkeypatch):
    monkeypatch.setenv("REMEDY_OLLAMA_BUILDER_NUM_PREDICT", "not-an-int")
    from packages.providers.ollama_builder.provider import OllamaBuilder
    with pytest.raises(ValueError, match="REMEDY_OLLAMA_BUILDER_NUM_PREDICT"):
        OllamaBuilder()


# ---------------------------------------------------------------------------
# BuilderOutput schema: proposed_changes min_length=1
# ---------------------------------------------------------------------------

def test_builder_output_rejects_empty_proposed_changes():
    """BuilderOutput must require at least 1 proposed change."""
    from pydantic import ValidationError
    from packages.orchestration.builder_models import BuilderOutput
    with pytest.raises(ValidationError):
        BuilderOutput(summary="ok", proposed_changes=[])


def test_builder_output_accepts_single_proposed_change():
    from packages.orchestration.builder_models import BuilderOutput
    output = BuilderOutput(summary="ok", proposed_changes=["add function foo"])
    assert len(output.proposed_changes) == 1


def test_builder_output_rejects_missing_proposed_changes():
    """proposed_changes is required and cannot be omitted."""
    from pydantic import ValidationError
    from packages.orchestration.builder_models import BuilderOutput
    with pytest.raises(ValidationError):
        BuilderOutput(summary="ok")  # type: ignore[call-arg]


# ---------------------------------------------------------------------------
# CLI path: bad env var is caught as configuration error
# ---------------------------------------------------------------------------

def test_bad_temperature_env_var_raises_value_error_on_construction(monkeypatch):
    """OllamaBuilder() raises ValueError from __init__ — confirms CLI must wrap it."""
    monkeypatch.setenv("REMEDY_OLLAMA_BUILDER_TEMPERATURE", "definitely-not-a-float")
    from packages.providers.ollama_builder.provider import OllamaBuilder
    with pytest.raises(ValueError, match="REMEDY_OLLAMA_BUILDER_TEMPERATURE"):
        OllamaBuilder()  # ValueError must come from construction, not from .build()
