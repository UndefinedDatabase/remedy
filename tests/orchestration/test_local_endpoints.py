"""Tests for packages.orchestration.local_endpoints — F113 T001: the `local_routing.endpoints` table,
the health probe at first use and its classification, and the call bound to an endpoint's host and
model (DECISION F113 D1)."""

from __future__ import annotations

import json
import pathlib
import sys
import types
import warnings

import pytest

from packages.orchestration.config import get_key_spec
from packages.orchestration.config_keys_model_routing import LOCAL_ENDPOINTS_CONFIG_KEY
from packages.orchestration.failure_postmortem import (
    FailureClass,
    FailureSignals,
    classify,
    is_provider_unavailable_error,
)
from packages.orchestration.local_endpoints import (
    LOCAL_ENDPOINT_KEYS,
    LOCAL_UNAVAILABLE_PREFIX,
    LocalEndpoint,
    LocalEndpointError,
    LocalEndpointProbes,
    make_local_call_fn,
    parse_local_endpoints,
    probe_local_endpoint,
    resolve_local_endpoints,
)
from packages.orchestration.schemas import JobIntake

BOX = LocalEndpoint(name="box", base_url="http://127.0.0.1:9", model="muse-glimmer")


def configure_toml(monkeypatch, tmp_path, body: str) -> None:
    """Resolve the configuration from real TOML in `tmp_path`, as test_model_failover.py does."""
    from packages.orchestration.config import load_config

    toml_file = tmp_path / "remedy.toml"
    toml_file.write_text(body, encoding="utf-8")
    loaded = load_config(project_path=toml_file, user_path=pathlib.Path("/nonexistent/user.toml"))
    monkeypatch.setattr("packages.orchestration.config.get_config", lambda: loaded)


class TestTheEndpointTable:
    def test_the_key_is_a_table_of_tables_with_no_default(self):
        spec = get_key_spec(LOCAL_ENDPOINTS_CONFIG_KEY)
        assert (spec.key, spec.value_type, spec.entry_type, spec.default) == (
            "local_routing.endpoints", dict, dict, None)

    def test_two_named_endpoints_round_trip_in_order(self):
        found = parse_local_endpoints({
            "box": {"base_url": "http://127.0.0.1:9/", "model": "muse-glimmer"},
            "nas": {"base_url": "https://nas.local:11434", "model": "small:3b"},
        })
        assert list(found) == ["box", "nas"]
        assert found["box"] == BOX
        assert found["nas"] == LocalEndpoint("nas", "https://nas.local:11434", "small:3b")

    @pytest.mark.parametrize(("entry", "fault"), [
        ("http://x", "must be a table"),
        ({"base_url": "http://x", "model": "m", "gpu": 1}, "unknown key 'gpu'"),
        ({"model": "m"}, "must set base_url"),
        ({"base_url": "ftp://x", "model": "m"}, "must set base_url"),
        ({"base_url": "http://x"}, "must set model"),
        ({"base_url": "http://x", "model": ""}, "must set model"),
    ])
    def test_a_malformed_endpoint_is_refused_with_its_fault_named(self, entry, fault):
        with pytest.raises(LocalEndpointError) as caught:
            parse_local_endpoints({"box": entry})
        assert str(caught.value).startswith("local_routing.endpoints: 'box'")
        assert fault in str(caught.value)

    def test_an_endpoint_holds_exactly_a_base_url_and_a_model(self):
        assert LOCAL_ENDPOINT_KEYS == ("base_url", "model")

    def test_a_local_endpoint_never_resumes_a_session(self):
        assert BOX.supports_resume is False

    def test_the_configured_table_resolves_from_toml(self, monkeypatch, tmp_path):
        configure_toml(monkeypatch, tmp_path,
                       '[remedy.local_routing.endpoints.box]\nbase_url = "http://127.0.0.1:9"\n'
                       'model = "muse-glimmer"\n')
        assert resolve_local_endpoints() == {"box": BOX}

    def test_an_unset_table_resolves_to_no_endpoint(self, monkeypatch, tmp_path):
        configure_toml(monkeypatch, tmp_path, "")
        assert resolve_local_endpoints() == {}

    def test_an_unreadable_table_warns_once_and_names_no_endpoint(self, monkeypatch, tmp_path):
        configure_toml(monkeypatch, tmp_path,
                       '[remedy.local_routing.endpoints.box]\nbase_url = "http://127.0.0.1:9"\n')
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            assert resolve_local_endpoints() == {}
        assert [str(w.message) for w in caught] == [
            "local_routing.endpoints: 'box' must set model to a non-empty string; no side role runs locally"]


class TestTheProbe:
    def test_an_endpoint_whose_server_lists_its_model_is_available(self):
        health = probe_local_endpoint(BOX, list_models=lambda url: ["other:1b", "muse-glimmer:latest"])
        assert (health.endpoint, health.available, health.reason) == ("box", True, "")

    def test_a_tagged_model_must_be_listed_with_its_own_tag(self):
        tagged = LocalEndpoint("box", "http://127.0.0.1:9", "small:3b")
        assert probe_local_endpoint(tagged, list_models=lambda url: ["small:3b"]).available
        assert not probe_local_endpoint(tagged, list_models=lambda url: ["small:latest"]).available

    def test_a_server_without_the_model_is_unavailable_and_says_so(self):
        health = probe_local_endpoint(BOX, list_models=lambda url: ["other:1b"])
        assert not health.available
        assert health.reason == (
            "provider_unavailable: local endpoint box at http://127.0.0.1:9 does not serve model muse-glimmer")

    @pytest.mark.parametrize("error", [ConnectionError("Failed to connect to Ollama"), OSError("refused"),
                                       ImportError("ollama package not installed")])
    def test_a_server_that_does_not_answer_is_unavailable_and_never_raises(self, error):
        def lister(url: str) -> list[str]:
            raise error

        health = probe_local_endpoint(BOX, list_models=lister)
        assert not health.available
        assert health.reason.startswith(f"{LOCAL_UNAVAILABLE_PREFIX} box at http://127.0.0.1:9 did not answer: "
                                        f"{type(error).__name__}")

    def test_the_probe_asks_the_endpoints_own_base_url(self):
        asked: list[str] = []
        probe_local_endpoint(BOX, list_models=lambda url: asked.append(url) or [])
        assert asked == ["http://127.0.0.1:9"]

    def test_an_unavailable_reason_is_classified_provider_unavailable(self):
        reason = probe_local_endpoint(BOX, list_models=lambda url: []).reason
        assert is_provider_unavailable_error(reason)
        assert classify(FailureSignals(error_text=reason)).failure_class is FailureClass.PROVIDER_UNAVAILABLE

    def test_the_default_lister_reads_the_ollama_clients_model_list(self, monkeypatch):
        seen: dict[str, object] = {}

        class FakeClient:
            def __init__(self, host=None, timeout=None):
                seen.update(host=host, timeout=timeout)

            def list(self):
                return types.SimpleNamespace(models=[types.SimpleNamespace(model="muse-glimmer:latest")])

        fake = types.ModuleType("ollama")
        fake.Client = FakeClient
        monkeypatch.setitem(sys.modules, "ollama", fake)
        assert probe_local_endpoint(BOX).available
        assert seen["host"] == "http://127.0.0.1:9"


class TestTheProbeAtFirstUse:
    def test_later_uses_read_the_first_answer_until_it_is_too_old(self):
        now = [100.0]
        asked: list[str] = []
        probes = LocalEndpointProbes(list_models=lambda url: asked.append(url) or ["muse-glimmer"],
                                     clock=lambda: now[0], max_age_s=300.0)
        assert probes.health(BOX).available
        now[0] = 399.0
        assert probes.health(BOX).available
        assert len(asked) == 1
        now[0] = 400.0
        probes.health(BOX)
        assert len(asked) == 2

    def test_each_endpoint_is_probed_on_its_own(self):
        asked: list[str] = []
        probes = LocalEndpointProbes(list_models=lambda url: asked.append(url) or [])
        probes.health(BOX)
        probes.health(LocalEndpoint("nas", "http://nas:1", "muse-glimmer"))
        assert asked == ["http://127.0.0.1:9", "http://nas:1"]

    def test_an_endpoint_that_came_back_is_used_again_after_the_answer_ages(self):
        now = [0.0]
        up = [False]
        probes = LocalEndpointProbes(list_models=lambda url: ["muse-glimmer"] if up[0] else [],
                                     clock=lambda: now[0], max_age_s=10.0)
        assert not probes.health(BOX).available
        up[0] = True
        assert not probes.health(BOX).available
        now[0] = 10.0
        assert probes.health(BOX).available


class TestTheCall:
    def test_the_call_runs_on_the_endpoints_host_and_model(self, monkeypatch):
        seen: dict[str, object] = {}

        class FakeClient:
            def __init__(self, host=None, timeout=None):
                seen["host"] = host

            def chat(self, **request):
                seen["model"] = request["model"]
                seen["format"] = request["format"]
                content = json.dumps({"intent": "x"})
                return types.SimpleNamespace(message=types.SimpleNamespace(content=content))

        fake = types.ModuleType("ollama")
        fake.Client = FakeClient
        monkeypatch.setitem(sys.modules, "ollama", fake)
        call_fn = make_local_call_fn(BOX, JobIntake)
        assert call_fn("a prompt", 0) == json.dumps({"intent": "x"})
        assert (seen["host"], seen["model"]) == ("http://127.0.0.1:9", "muse-glimmer")
        assert isinstance(seen["format"], dict)
        assert call_fn.resolved_model == "muse-glimmer"
