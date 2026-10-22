"""Tests for packages.orchestration.side_role_routing — F113 T002: the `local_routing.side_roles`
table, the hard rule that keeps every core role off a local endpoint, the fallback to the role's own
provider, and the summary role served locally on a fixture endpoint (DECISION F113 D1)."""

from __future__ import annotations

import json
import sys
import types
import warnings

import pytest

from packages.orchestration import artifact_summary, chat_answer, result_tour
from packages.orchestration.artifact_summary import generate_artifact_summary, summary_call_fn
from packages.orchestration.config import get_key_spec
from packages.orchestration.config_keys_model_routing import SIDE_ROLES_CONFIG_KEY
from packages.orchestration.failure_postmortem import is_provider_unavailable_error
from packages.orchestration.local_endpoints import LocalEndpoint, LocalEndpointProbes
from packages.orchestration.model_failover import FAILOVER_LOCAL_ROLES, RULE_CORE_ROLE_ON_LOCAL_PROVIDER
from packages.orchestration.model_routing import ROLE_TASK_CLASSES, TASK_CLASS_TIERS
from packages.orchestration.role_config import KNOWN_ROLES
from packages.orchestration.schemas import JobIntake
from packages.orchestration.side_role_routing import (
    COST_BASIS_LOCAL_ZERO,
    ROUTE_FALLBACK,
    ROUTE_LOCAL,
    SideRoleRoute,
    SideRoleRouteRefused,
    SideRoleRoutingError,
    parse_side_role_routes,
    resolve_side_role_routes,
    route_side_role,
    side_role_call_fn,
)
from tests.orchestration.test_local_endpoints import configure_toml

BOX = LocalEndpoint(name="box", base_url="http://127.0.0.1:9", model="muse-glimmer")
ENDPOINTS = {"box": BOX}
CORE_ROLES = sorted(set(KNOWN_ROLES) - FAILOVER_LOCAL_ROLES)
TABLES = ('[remedy.local_routing.endpoints.box]\nbase_url = "http://127.0.0.1:9"\nmodel = "muse-glimmer"\n'
          '[remedy.local_routing.side_roles]\n')
SECTIONS = [{"section": "foo.py", "span_ref": "file:foo.py", "text": "+a line"}]
REPLY = json.dumps({"l1": "a local summary", "l2": [{"section": "foo.py", "span_ref": "file:foo.py",
                                                     "summary": "foo changed"}]})


def probes(up: bool) -> LocalEndpointProbes:
    return LocalEndpointProbes(list_models=lambda url: ["muse-glimmer:latest"] if up else [])


def fake_ollama(monkeypatch, reply: str) -> dict[str, object]:
    """An `ollama` module whose client answers every chat with `reply` and records what it was asked."""
    seen: dict[str, object] = {}

    class FakeClient:
        def __init__(self, host=None, timeout=None):
            seen["host"] = host

        def chat(self, **request):
            seen["model"] = request["model"]
            return types.SimpleNamespace(message=types.SimpleNamespace(content=reply))

    module = types.ModuleType("ollama")
    module.Client = FakeClient
    monkeypatch.setitem(sys.modules, "ollama", module)
    return seen


class TestTheSideRoleTable:
    def test_the_key_maps_a_role_to_an_endpoint_name_with_no_default(self):
        spec = get_key_spec(SIDE_ROLES_CONFIG_KEY)
        assert (spec.key, spec.value_type, spec.entry_type, spec.default) == (
            "local_routing.side_roles", dict, str, None)

    def test_the_side_roles_are_exactly_the_cheap_tier_roles(self):
        cheap = {role for role, task_class in ROLE_TASK_CLASSES.items() if TASK_CLASS_TIERS[task_class] == "cheap"}
        assert FAILOVER_LOCAL_ROLES == cheap == {"summary", "teacher", "study"}

    @pytest.mark.parametrize("role", sorted(FAILOVER_LOCAL_ROLES))
    def test_every_side_role_may_run_on_a_local_endpoint(self, role):
        assert parse_side_role_routes({role: "box"}, ENDPOINTS) == {role: BOX}

    @pytest.mark.parametrize("role", CORE_ROLES)
    def test_every_core_role_is_refused_with_the_rule_named(self, role):
        with pytest.raises(SideRoleRouteRefused) as caught:
            parse_side_role_routes({role: "box"}, ENDPOINTS)
        assert caught.value.roles == (role,)
        assert str(caught.value) == f"local_routing.side_roles: refused — {role}: {RULE_CORE_ROLE_ON_LOCAL_PROVIDER}"

    def test_the_core_roles_cover_build_review_and_orchestration(self):
        assert {"builder", "reviewer", "repair", "orchestrator", "planner", "final_verifier"} <= set(CORE_ROLES)

    def test_every_refused_role_is_named_at_once_and_a_side_role_beside_them_does_not_save_the_table(self):
        with pytest.raises(SideRoleRouteRefused) as caught:
            parse_side_role_routes({"builder": "box", "summary": "box", "reviewer": "box"}, ENDPOINTS)
        assert caught.value.roles == ("builder", "reviewer")

    def test_an_unknown_role_is_refused(self):
        with pytest.raises(SideRoleRoutingError, match="'scribe' is not a known role"):
            parse_side_role_routes({"scribe": "box"}, ENDPOINTS)

    def test_an_endpoint_the_endpoint_table_does_not_name_is_refused(self):
        with pytest.raises(SideRoleRoutingError, match="names endpoint 'nas', which local_routing.endpoints"):
            parse_side_role_routes({"summary": "nas"}, ENDPOINTS)

    def test_the_configured_table_resolves_from_toml(self, monkeypatch, tmp_path):
        configure_toml(monkeypatch, tmp_path, TABLES + 'summary = "box"\n')
        assert resolve_side_role_routes() == {"summary": BOX}

    def test_a_table_routing_the_builder_to_local_is_refused_with_the_rule_named(self, monkeypatch, tmp_path):
        configure_toml(monkeypatch, tmp_path, TABLES + 'summary = "box"\nbuilder = "box"\n')
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            assert resolve_side_role_routes() == {}
        assert [str(w.message) for w in caught] == [
            "local_routing.side_roles: refused — builder: core_role_on_local_provider; no side role runs locally"]


class TestTheRoute:
    def test_a_mapped_role_whose_endpoint_serves_runs_there_at_zero_cost(self):
        route = route_side_role("summary", BOX, probes(up=True))
        assert route == SideRoleRoute("summary", ROUTE_LOCAL, "box", "muse-glimmer", "")
        assert route.cost_basis == COST_BASIS_LOCAL_ZERO == "local_zero"

    def test_a_mapped_role_whose_endpoint_is_down_falls_back_with_the_reason_classified(self):
        route = route_side_role("summary", BOX, probes(up=False))
        assert (route.route, route.endpoint, route.routed_model) == (ROUTE_FALLBACK, "box", "")
        assert is_provider_unavailable_error(route.reason)
        assert route.cost_basis == "unknown"

    def test_the_evidence_names_every_field(self):
        assert route_side_role("summary", BOX, probes(up=True)).evidence() == {
            "role": "summary", "route": "local", "endpoint": "box", "routed_model": "muse-glimmer",
            "reason": "", "cost_basis": "local_zero"}


class TestTheCallFn:
    def test_an_unmapped_role_gets_its_own_path_untouched(self):
        own = lambda prompt, attempt: "own"  # noqa: E731
        call_fn = side_role_call_fn("summary", JobIntake, lambda: own, routes={}, probes=probes(up=True))
        assert call_fn is own
        assert not hasattr(call_fn, "side_role_route")

    def test_a_mapped_role_runs_on_its_endpoint_and_never_asks_its_own_path(self, monkeypatch):
        seen = fake_ollama(monkeypatch, "{}")
        asked: list[int] = []
        call_fn = side_role_call_fn("summary", JobIntake, lambda: asked.append(1),
                                    routes={"summary": BOX}, probes=probes(up=True))
        call_fn("p", 0)
        assert (seen["host"], seen["model"], asked) == ("http://127.0.0.1:9", "muse-glimmer", [])
        assert call_fn.side_role_route.route == ROUTE_LOCAL

    def test_a_mapped_role_whose_endpoint_is_down_runs_on_its_own_path_with_the_route(self):
        def own(prompt: str, attempt: int) -> str:
            return "own"

        call_fn = side_role_call_fn("summary", JobIntake, lambda: own, routes={"summary": BOX}, probes=probes(up=False))
        assert call_fn is own
        assert call_fn.side_role_route.route == ROUTE_FALLBACK

    def test_a_fallback_with_nothing_to_serve_answers_none(self):
        assert side_role_call_fn("summary", JobIntake, lambda: None, routes={"summary": BOX},
                                 probes=probes(up=False)) is None


class TestTheSummaryRoleOnAFixtureEndpoint:
    def test_the_summary_is_served_locally_with_its_route_and_basis_recorded(self, monkeypatch, tmp_path):
        configure_toml(monkeypatch, tmp_path, TABLES + 'summary = "box"\n')
        monkeypatch.setattr("packages.orchestration.side_role_routing.LOCAL_ENDPOINT_PROBES", probes(up=True))
        seen = fake_ollama(monkeypatch, REPLY)
        summary = generate_artifact_summary(SECTIONS, "workspace.diff", "abc", summary_call_fn())
        assert (summary.l1, summary.generator) == ("a local summary", "summary-role")
        assert (seen["host"], seen["model"]) == ("http://127.0.0.1:9", "muse-glimmer")
        assert summary.route == {"role": "summary", "route": "local", "endpoint": "box",
                                 "routed_model": "muse-glimmer", "reason": "", "cost_basis": "local_zero"}

    def test_an_endpoint_that_is_down_falls_back_cleanly_to_the_roles_own_model(self, monkeypatch, tmp_path):
        configure_toml(monkeypatch, tmp_path, TABLES + 'summary = "box"\n')
        monkeypatch.setattr("packages.orchestration.side_role_routing.LOCAL_ENDPOINT_PROBES", probes(up=False))
        built: list[object] = []

        def own_path(model_cls, *, model=None, provider=None):
            built.append(model_cls)
            return lambda prompt, attempt: REPLY

        monkeypatch.setattr(artifact_summary, "make_structured_call_fn", own_path)
        summary = generate_artifact_summary(SECTIONS, "workspace.diff", "abc", summary_call_fn())
        assert summary.l1 == "a local summary"
        assert built == [artifact_summary.GeneratedSummaryContent]
        assert summary.route["route"] == "fallback"
        assert summary.route["reason"] == (
            "provider_unavailable: local endpoint box at http://127.0.0.1:9 does not serve model muse-glimmer")

    def test_an_unmapped_summary_records_no_route(self):
        summary = generate_artifact_summary(SECTIONS, "workspace.diff", "abc", lambda prompt, attempt: REPLY)
        assert summary.route is None
        assert "route" not in json.loads(summary.model_dump_json(exclude_none=True))

    def test_a_summary_that_failed_on_its_endpoint_keeps_the_route_beside_the_fallback(self, monkeypatch, tmp_path):
        configure_toml(monkeypatch, tmp_path, TABLES + 'summary = "box"\n')
        monkeypatch.setattr("packages.orchestration.side_role_routing.LOCAL_ENDPOINT_PROBES", probes(up=True))
        fake_ollama(monkeypatch, "not json")
        summary = generate_artifact_summary(SECTIONS, "workspace.diff", "abc", summary_call_fn())
        assert summary.generator.startswith("fallback:")
        assert summary.route["route"] == "local"

    @pytest.mark.parametrize("factory", [result_tour.tour_call_fn, chat_answer.chat_call_fn])
    def test_the_tour_and_the_chat_answer_follow_the_same_route(self, monkeypatch, tmp_path, factory):
        configure_toml(monkeypatch, tmp_path, TABLES + 'summary = "box"\n')
        monkeypatch.setattr("packages.orchestration.side_role_routing.LOCAL_ENDPOINT_PROBES", probes(up=True))
        seen = fake_ollama(monkeypatch, "{}")
        call_fn = factory()
        call_fn("p", 0)
        assert seen["host"] == "http://127.0.0.1:9"
        assert call_fn.side_role_route.route == ROUTE_LOCAL
