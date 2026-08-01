"""F061 T001 — the DoD schema and the compiler that fills it.

What the order requires proof of:

  * the schema round-trips through JSON unchanged, and refuses a DoD that
    claims to be compiled when it was not;
  * three long-goal fixture missions compile to their golden DoDs — on the
    provider path AND on the no-provider path;
  * the traceability rule holds by construction, and a DoD that violates it
    is caught rather than shrugged at (positive AND violation);
  * a fallback DoD is labeled ``compiled=false`` / ``origin="deterministic"``
    on every route into it — no provider, provider error, unparseable answer;
  * detectably unrunnable specs are refused at COMPILE time, not discovered
    by a runner hours later.

No provider is contacted: every "LLM" here is a local callable returning
recorded text.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.orchestration.dod_compiler import (
    DEFAULT_TEST_SELECTOR,
    AcceptanceLine,
    DoDTraceabilityError,
    StandardCheckContext,
    acceptance_line_key,
    assert_acceptance_traceable,
    compile_dod,
    deterministic_dod,
    plan_acceptance_lines,
    register_standard_check_provider,
    registered_standard_check_providers,
    trace_acceptance,
    unregister_standard_check_provider,
)
from packages.orchestration.dod_schema import (
    DOD_DRAFT_SCHEMA_V,
    DOD_SCHEMA_V,
    TRACEABILITY_RULE,
    DoD,
    DoDCheck,
    DoDDraft,
    DoDSpecError,
    DraftCheck,
)
from packages.orchestration.schemas.models import FlightPlan

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "dod"
FIXTURE_NAMES = ("docs_site", "api_service", "cli_tool")
FEATURE_FILE = (
    Path(__file__).resolve().parents[2]
    / "docs" / "roadmap" / "features" / "T1_F061.md"
)


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURE_DIR / f"{name}.json").read_text(encoding="utf-8"))


def plan_of(fixture: dict) -> FlightPlan:
    return FlightPlan.model_validate(fixture["plan"])


def replaying(payload: dict):
    """A call_fn that hands back one recorded provider answer."""
    text = json.dumps(payload)

    def _call(prompt: str, attempt: int) -> str:
        return text

    return _call


def simple_plan(*acceptance: str) -> FlightPlan:
    return FlightPlan.model_validate({
        "schema_v": "flight_plan_v1",
        "tasks": [{
            "id": "T001",
            "title": "t",
            "goal": "g",
            "acceptance": list(acceptance),
            "est_tokens_band": "S",
        }],
    })


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

class TestSchema:
    def test_round_trip_through_json_is_unchanged(self):
        dod = DoD(
            schema_v=DOD_SCHEMA_V,
            compiled=True,
            origin="provider",
            checks=[DoDCheck(
                id="c1",
                kind="pytest",
                spec={"selector": "tests/x.py::test_y"},
                blocking=True,
                acceptance_refs=["T001:0"],
                description="d",
                source="compiled",
            )],
        )
        again = DoD.model_validate(json.loads(json.dumps(dod.model_dump())))
        assert again == dod
        assert again.model_dump() == dod.model_dump()

    def test_schema_v_is_required_not_defaulted(self):
        with pytest.raises(Exception) as exc:
            DoD.model_validate({
                "compiled": False,
                "origin": "deterministic",
                "checks": [{
                    "id": "c1", "kind": "pytest",
                    "spec": {"selector": "tests"}, "source": "plan_acceptance",
                }],
            })
        assert "schema_v" in str(exc.value)

    def test_unknown_field_is_refused(self):
        with pytest.raises(Exception):
            DoDCheck.model_validate({
                "id": "c1", "kind": "pytest", "spec": {"selector": "tests"},
                "source": "compiled", "surprise": 1,
            })

    @pytest.mark.parametrize("compiled,origin", [
        (True, "deterministic"),
        (False, "provider"),
    ])
    def test_compiled_flag_and_origin_must_agree(self, compiled, origin):
        """A deterministic DoD cannot be dressed up as a compiled one."""
        with pytest.raises(Exception) as exc:
            DoD(
                schema_v=DOD_SCHEMA_V, compiled=compiled, origin=origin,
                checks=[DoDCheck(
                    id="c1", kind="pytest", spec={"selector": "tests"},
                    source="plan_acceptance")],
            )
        assert "compiled" in str(exc.value)

    def test_duplicate_check_ids_are_refused(self):
        check = {"id": "same", "kind": "pytest", "spec": {"selector": "tests"},
                 "source": "compiled"}
        with pytest.raises(Exception) as exc:
            DoD.model_validate({
                "schema_v": DOD_SCHEMA_V, "compiled": True, "origin": "provider",
                "checks": [check, dict(check)],
            })
        assert "duplicate check id" in str(exc.value)

    def test_draft_cannot_declare_a_source(self):
        """Provenance is the compiler's to assign, not the provider's."""
        with pytest.raises(Exception):
            DraftCheck.model_validate({
                "id": "c1", "kind": "pytest", "spec": {"selector": "tests"},
                "source": "standard",
            })

    def test_blocking_checks_property_selects_the_gating_ones(self):
        dod = DoD(
            schema_v=DOD_SCHEMA_V, compiled=False, origin="deterministic",
            checks=[
                DoDCheck(id="a", kind="pytest", spec={"selector": "tests"},
                         blocking=True, source="plan_acceptance"),
                DoDCheck(id="b", kind="pytest", spec={"selector": "tests"},
                         blocking=False, source="plan_acceptance"),
            ],
        )
        assert [c.id for c in dod.blocking_checks] == ["a"]


# ---------------------------------------------------------------------------
# Compile-time rejection of nonsense specs
# ---------------------------------------------------------------------------

class TestNonsenseSpecRejection:
    @pytest.mark.parametrize("kind,spec,needle", [
        ("pytest", {"selector": ""}, "non-empty 'selector'"),
        ("pytest", {}, "non-empty 'selector'"),
        ("pytest", {"selector": "tests", "args": "-q"}, "must be a list"),
        ("lint", {"tool": ""}, "non-empty 'tool'"),
        ("build", {}, "non-empty 'tool'"),
        ("custom_cmd", {"argv": []}, "non-empty 'argv'"),
        ("custom_cmd", {"argv": ["", "x"]}, "argv[0] must be a non-empty"),
        ("runtime_flow", {"steps": []}, "non-empty 'steps'"),
        ("runtime_flow", {"steps": [{"expect": "200"}]}, "non-empty 'action'"),
        ("pytest", {"selector": "tests", "typo": 1}, "unknown key"),
    ])
    def test_unrunnable_spec_is_refused_at_compile_time(self, kind, spec, needle):
        with pytest.raises(Exception) as exc:
            DraftCheck(id="c1", kind=kind, spec=spec)
        assert needle in str(exc.value)

    def test_unknown_kind_is_refused(self):
        with pytest.raises(Exception) as exc:
            DraftCheck.model_validate({
                "id": "c1", "kind": "telepathy", "spec": {}})
        assert "kind" in str(exc.value)

    @pytest.mark.parametrize("cwd", ["/etc", "../outside", "a/../../b"])
    def test_cwd_may_not_escape_the_worktree(self, cwd):
        with pytest.raises(Exception) as exc:
            DraftCheck(id="c1", kind="pytest",
                       spec={"selector": "tests", "cwd": cwd})
        assert "cwd" in str(exc.value)

    def test_relative_cwd_is_accepted(self):
        check = DraftCheck(id="c1", kind="pytest",
                           spec={"selector": "tests", "cwd": "apps/ui"})
        assert check.spec["cwd"] == "apps/ui"

    @pytest.mark.parametrize("ident", ["", "   ", "has space", "semi;colon", "x" * 65])
    def test_illegal_check_ids_are_refused(self, ident):
        with pytest.raises(Exception):
            DraftCheck(id=ident, kind="pytest", spec={"selector": "tests"})

    def test_spec_error_is_a_value_error(self):
        """So pydantic reports it as a validation failure, not a crash."""
        assert issubclass(DoDSpecError, ValueError)


