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


# ---------------------------------------------------------------------------
# raw_call delegation + option passthrough
# ---------------------------------------------------------------------------

class TestRawCall:
    def _make_planner_with_fake(self, monkeypatch, **kwargs):
        import sys
        import types

        fake_ollama = types.ModuleType("ollama")
        captured = {}

        class FakeClient:
            def __init__(self, host=None):
                captured["host"] = host

            def chat(self, **kw):
                captured["chat_kwargs"] = kw
                msg = types.SimpleNamespace(content='{"result":"ok"}')
                return types.SimpleNamespace(message=msg)

        fake_ollama.Client = FakeClient
        monkeypatch.setitem(sys.modules, "ollama", fake_ollama)
        from packages.providers.ollama_planner.provider import OllamaPlanner
        return OllamaPlanner(**kwargs), captured

    def test_raw_call_passes_schema_and_prompt(self, monkeypatch):
        planner, cap = self._make_planner_with_fake(monkeypatch)
        result = planner.raw_call("hello", schema={"type": "object"})
        assert result == '{"result":"ok"}'
        assert cap["chat_kwargs"]["format"] == {"type": "object"}
        msgs = cap["chat_kwargs"]["messages"]
        assert len(msgs) == 1
        assert msgs[0]["role"] == "user"
        assert msgs[0]["content"] == "hello"

    def test_raw_call_includes_system_when_given(self, monkeypatch):
        planner, cap = self._make_planner_with_fake(monkeypatch)
        planner.raw_call("hello", schema={}, system="be brief")
        msgs = cap["chat_kwargs"]["messages"]
        assert len(msgs) == 2
        assert msgs[0] == {"role": "system", "content": "be brief"}
        assert msgs[1] == {"role": "user", "content": "hello"}

    def test_raw_call_no_system_omits_system_message(self, monkeypatch):
        planner, cap = self._make_planner_with_fake(monkeypatch)
        planner.raw_call("hello", schema={})
        msgs = cap["chat_kwargs"]["messages"]
        assert all(m["role"] != "system" for m in msgs)

    def test_raw_call_passes_temperature_and_num_predict(self, monkeypatch):
        planner, cap = self._make_planner_with_fake(
            monkeypatch, temperature=0.5, num_predict=256,
        )
        planner.raw_call("hello", schema={})
        opts = cap["chat_kwargs"].get("options", {})
        assert opts["temperature"] == pytest.approx(0.5)
        assert opts["num_predict"] == 256

    def test_raw_call_omits_options_when_none(self, monkeypatch):
        planner, cap = self._make_planner_with_fake(monkeypatch)
        planner.raw_call("hello", schema={})
        assert "options" not in cap["chat_kwargs"]

    def test_plan_raw_delegates_to_raw_call(self, monkeypatch):
        planner, cap = self._make_planner_with_fake(monkeypatch)
        planner.plan_raw("build a CLI", schema={"type": "object"})
        msgs = cap["chat_kwargs"]["messages"]
        assert msgs[0]["role"] == "system"
        assert msgs[1]["content"] == "Plan this job:\n\nbuild a CLI"

    def test_raw_call_uses_env_model(self, monkeypatch):
        monkeypatch.setenv("REMEDY_OLLAMA_PLANNER_MODEL", "test-model-77")
        planner, cap = self._make_planner_with_fake(monkeypatch)
        planner.raw_call("hello", schema={})
        assert cap["chat_kwargs"]["model"] == "test-model-77"
