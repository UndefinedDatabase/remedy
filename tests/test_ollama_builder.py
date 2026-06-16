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
# Structured patch prompt and memory context (Step 307)
# ---------------------------------------------------------------------------

def test_system_prompt_mentions_structured_patch():
    from packages.providers.ollama_builder.provider import _SYSTEM_PROMPT
    assert "structured_patch_text" in _SYSTEM_PROMPT
    assert "file_ops" in _SYSTEM_PROMPT
    assert "structured_patch_format" in _SYSTEM_PROMPT


def test_user_message_includes_memory_context():
    from uuid import uuid4

    from packages.orchestration.builder_models import TaskExecutionContext
    from packages.providers.ollama_builder.provider import _build_user_message
    ctx = TaskExecutionContext(
        job_id=uuid4(),
        task_id=uuid4(),
        job_prompt="Fix calc",
        task_type="code_change",
        task_description="Fix addition",
        memory_context="## Project Memory\n- Use pytest for tests",
    )
    msg = _build_user_message(ctx)
    assert "Project Memory" in msg
    assert "Use pytest for tests" in msg


def test_user_message_omits_memory_when_none():
    from uuid import uuid4

    from packages.orchestration.builder_models import TaskExecutionContext
    from packages.providers.ollama_builder.provider import _build_user_message
    ctx = TaskExecutionContext(
        job_id=uuid4(),
        task_id=uuid4(),
        job_prompt="Fix calc",
        task_type="code_change",
        task_description="Fix addition",
    )
    msg = _build_user_message(ctx)
    assert "Project Memory" not in msg
