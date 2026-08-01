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

    # R-0164: a leading dash in a position that names a THING, not an option.
    # Left alone, "-x" lands in the argv where a selector or a program belongs
    # and silently changes what runs.

    def test_flag_shaped_pytest_selector_is_refused(self):
        with pytest.raises(Exception) as exc:
            DraftCheck(id="c1", kind="pytest", spec={"selector": "-x"})
        message = str(exc.value)
        assert "'selector'" in message
        assert "'-x'" in message

    @pytest.mark.parametrize("kind", ["lint", "build"])
    def test_flag_shaped_tool_is_refused(self, kind):
        with pytest.raises(Exception) as exc:
            DraftCheck(id="c1", kind=kind, spec={"tool": "--version"})
        message = str(exc.value)
        assert "'tool'" in message
        assert "'--version'" in message

    def test_flag_shaped_custom_cmd_program_is_refused(self):
        with pytest.raises(Exception) as exc:
            DraftCheck(id="c1", kind="custom_cmd",
                       spec={"argv": ["--help", "please"]})
        message = str(exc.value)
        assert "'argv[0]'" in message
        assert "'--help'" in message

    def test_leading_whitespace_does_not_smuggle_a_flag_through(self):
        with pytest.raises(Exception) as exc:
            DraftCheck(id="c1", kind="pytest", spec={"selector": "  -x"})
        assert "'selector'" in str(exc.value)

    def test_a_dash_after_the_first_character_is_still_fine(self):
        """Only the FIRST token position is constrained — real names have dashes."""
        assert DraftCheck(
            id="c1", kind="custom_cmd",
            spec={"argv": ["npm-run", "--silent", "test"]}).spec["argv"][1] == "--silent"
        assert DraftCheck(
            id="c2", kind="pytest",
            spec={"selector": "tests/test_a-b.py", "args": ["-x"]}).spec["args"] == ["-x"]

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


# ---------------------------------------------------------------------------
# The traceability rule
# ---------------------------------------------------------------------------

class TestTraceability:
    def test_rule_text_is_verbatim_from_the_feature_file(self):
        """The constant is the feature file's own sentence, not a paraphrase.

        The feature file hard-wraps its prose, so the comparison unwraps the
        document — whitespace only. Every other character must match.
        """
        document = " ".join(FEATURE_FILE.read_text(encoding="utf-8").split())
        assert TRACEABILITY_RULE in document

    def test_acceptance_lines_are_keyed_by_task_and_index(self):
        plan = plan_of(load_fixture("docs_site"))
        lines = plan_acceptance_lines(plan)
        assert [line.key for line in lines] == [
            "T001:0", "T001:1", "T002:0", "T003:0"]
        assert lines[0] == AcceptanceLine(
            key=acceptance_line_key("T001", 0), task_id="T001", index=0,
            text="tests/docs/test_links.py passes for every internal link")

    @pytest.mark.parametrize("name", FIXTURE_NAMES)
    def test_positive_every_acceptance_line_maps_to_a_check_id(self, name):
        fixture = load_fixture(name)
        plan = plan_of(fixture)
        result = compile_dod(
            fixture["intake"], plan, replaying(fixture["provider_draft"]))

        report = assert_acceptance_traceable(result.dod, plan)
        assert report.ok
        assert report.uncovered == ()
        assert set(report.covered) == {
            line.key for line in plan_acceptance_lines(plan)}
        for key, check_ids in report.covered.items():
            assert check_ids, key

    def test_violation_is_reported_and_raised(self):
        plan = simple_plan("first line", "second line")
        dod = DoD(
            schema_v=DOD_SCHEMA_V, compiled=False, origin="deterministic",
            checks=[DoDCheck(
                id="only", kind="pytest", spec={"selector": "tests"},
                acceptance_refs=["T001:0"], source="plan_acceptance")],
        )

        report = trace_acceptance(dod, plan)
        assert report.ok is False
        assert report.uncovered == ("T001:1",)
        assert report.covered["T001:0"] == ("only",)

        with pytest.raises(DoDTraceabilityError) as exc:
            assert_acceptance_traceable(dod, plan)
        assert TRACEABILITY_RULE in str(exc.value)
        assert "T001:1" in str(exc.value)

    def test_a_ref_to_a_line_that_does_not_exist_is_dangling_not_coverage(self):
        plan = simple_plan("first line")
        dod = DoD(
            schema_v=DOD_SCHEMA_V, compiled=False, origin="deterministic",
            checks=[DoDCheck(
                id="only", kind="pytest", spec={"selector": "tests"},
                acceptance_refs=["T009:7"], source="plan_acceptance")],
        )
        report = trace_acceptance(dod, plan)
        assert report.dangling_refs == ("T009:7",)
        assert report.uncovered == ("T001:0",)


# ---------------------------------------------------------------------------
# Golden fixtures
# ---------------------------------------------------------------------------

class TestGoldenFixtures:
    @pytest.mark.parametrize("name", FIXTURE_NAMES)
    def test_provider_path_matches_the_golden_dod(self, name):
        fixture = load_fixture(name)
        result = compile_dod(
            fixture["intake"], plan_of(fixture),
            replaying(fixture["provider_draft"]))

        assert result.dod.model_dump() == fixture["golden_dod"]
        assert result.source == "llm"
        assert result.calls == 1
        assert result.error_hint == ""

    @pytest.mark.parametrize("name", FIXTURE_NAMES)
    def test_no_provider_matches_the_golden_fallback_dod(self, name):
        fixture = load_fixture(name)
        result = compile_dod(fixture["intake"], plan_of(fixture), None)

        assert result.dod.model_dump() == fixture["golden_fallback_dod"]
        assert result.source == "deterministic"

    def test_fully_covered_fixture_needs_no_generated_check(self):
        """api_service: the provider covered every line, so nothing is added."""
        fixture = load_fixture("api_service")
        result = compile_dod(
            fixture["intake"], plan_of(fixture),
            replaying(fixture["provider_draft"]))
        assert {c.source for c in result.dod.checks} == {"compiled"}

    def test_uncovered_lines_sharing_a_selector_share_one_check(self):
        """cli_tool: two prose lines collapse into one generated check."""
        fixture = load_fixture("cli_tool")
        result = compile_dod(
            fixture["intake"], plan_of(fixture),
            replaying(fixture["provider_draft"]))
        generated = [c for c in result.dod.checks if c.source == "plan_acceptance"]
        assert len(generated) == 1
        assert generated[0].acceptance_refs == ["T001:1", "T002:0"]
        assert generated[0].spec == {"selector": DEFAULT_TEST_SELECTOR}

    def test_runtime_flow_is_schema_valid_in_the_compiled_dod(self):
        """The kind exists from R1 on; only its RUNNER lands in T003."""
        fixture = load_fixture("api_service")
        result = compile_dod(
            fixture["intake"], plan_of(fixture),
            replaying(fixture["provider_draft"]))
        flows = [c for c in result.dod.checks if c.kind == "runtime_flow"]
        assert [c.id for c in flows] == ["api-smoke"]


# ---------------------------------------------------------------------------
# Fallback labeling
# ---------------------------------------------------------------------------

class TestFallbackLabeling:
    def _plan(self) -> FlightPlan:
        return simple_plan("tests/x/test_a.py passes", "the CLI prints a table")

    def test_no_provider_is_labeled_deterministic(self):
        result = compile_dod({"goal": "g"}, self._plan(), None)
        assert result.dod.compiled is False
        assert result.dod.origin == "deterministic"
        assert result.source == "deterministic"
        assert result.error_hint == "no provider"
        assert result.calls == 0

    def test_provider_exception_falls_back_labeled(self):
        def boom(prompt: str, attempt: int) -> str:
            raise RuntimeError("connection refused")

        result = compile_dod({"goal": "g"}, self._plan(), boom)
        assert result.dod.compiled is False
        assert result.dod.origin == "deterministic"
        assert "connection refused" in result.error_hint

    def test_unparseable_answer_falls_back_after_one_retry(self):
        calls: list[int] = []

        def garbage(prompt: str, attempt: int) -> str:
            calls.append(attempt)
            return "I would rather write prose."

        result = compile_dod({"goal": "g"}, self._plan(), garbage)
        assert calls == [0, 1], "exactly one parse retry, never more"
        assert result.dod.compiled is False
        assert result.dod.origin == "deterministic"
        assert result.calls == 2
        assert result.error_hint

    def test_fallback_dod_is_still_runnable_and_traceable(self):
        plan = self._plan()
        result = compile_dod({"goal": "g"}, plan, None)
        assert result.traceability is not None and result.traceability.ok
        assert [c.spec["selector"] for c in result.dod.checks] == [
            "tests/x/test_a.py", DEFAULT_TEST_SELECTOR]
        assert {c.source for c in result.dod.checks} == {"plan_acceptance"}

    def test_deterministic_dod_is_reproducible(self):
        plan = self._plan()
        assert (deterministic_dod(plan).model_dump()
                == deterministic_dod(plan).model_dump())

    def test_a_draft_missing_schema_v_never_becomes_a_compiled_dod(self):
        """A near-miss answer is a parse failure, not a silent acceptance."""
        result = compile_dod(
            {"goal": "g"}, self._plan(),
            replaying({"checks": [
                {"id": "c1", "kind": "pytest", "spec": {"selector": "tests"}}]}),
        )
        assert result.dod.compiled is False
        assert "schema_v" in result.error_hint


# ---------------------------------------------------------------------------
# The prompt and the provider contract
# ---------------------------------------------------------------------------

class TestProviderContract:
    def test_prompt_carries_the_acceptance_keys_and_the_draft_schema(self):
        seen: list[str] = []
        fixture = load_fixture("docs_site")

        def record(prompt: str, attempt: int) -> str:
            seen.append(prompt)
            return json.dumps(fixture["provider_draft"])

        compile_dod(fixture["intake"], plan_of(fixture), record)
        prompt = seen[0]
        for key in ("T001:0", "T001:1", "T002:0", "T003:0"):
            assert key in prompt
        assert DOD_DRAFT_SCHEMA_V in prompt

    def test_provider_ids_that_collide_are_made_unique_not_dropped(self):
        plan = simple_plan("first", "second")
        draft = {
            "schema_v": DOD_DRAFT_SCHEMA_V,
            "checks": [
                {"id": "acc-001", "kind": "pytest",
                 "spec": {"selector": "tests/a.py"}, "acceptance_refs": ["T001:0"]},
            ],
        }
        result = compile_dod({"goal": "g"}, plan, replaying(draft))
        ids = [c.id for c in result.dod.checks]
        assert ids == ["acc-001", "acc-001-2"]
        assert len(set(ids)) == len(ids)

    def test_draft_model_rejects_duplicate_ids_from_the_provider(self):
        check = {"id": "dup", "kind": "pytest", "spec": {"selector": "tests"}}
        with pytest.raises(Exception) as exc:
            DoDDraft.model_validate({
                "schema_v": DOD_DRAFT_SCHEMA_V, "checks": [check, dict(check)]})
        assert "duplicate check id" in str(exc.value)


# ---------------------------------------------------------------------------
# The standard-check registry seam
# ---------------------------------------------------------------------------

class TestStandardCheckRegistry:
    @pytest.fixture(autouse=True)
    def _clean_registry(self):
        before = registered_standard_check_providers()
        yield
        for name in registered_standard_check_providers():
            if name not in before:
                unregister_standard_check_provider(name)

    def test_registered_checks_are_merged_and_labeled_standard(self):
        seen: list[StandardCheckContext] = []

        def smoke(ctx: StandardCheckContext) -> list[DraftCheck]:
            seen.append(ctx)
            return [DraftCheck(
                id="smoke", kind="custom_cmd",
                spec={"argv": ["remedy", "smoke"]}, blocking=True)]

        register_standard_check_provider("smoke", smoke)
        plan = simple_plan("tests/x/test_a.py passes")
        result = compile_dod({"goal": "g"}, plan, None)

        standard = [c for c in result.dod.checks if c.source == "standard"]
        assert [c.id for c in standard] == ["std-smoke"]
        assert standard[0].spec == {"argv": ["remedy", "smoke"]}
        assert seen and seen[0].plan is plan and seen[0].intake == {"goal": "g"}

    def test_standard_checks_also_reach_the_provider_path(self):
        register_standard_check_provider(
            "smoke", lambda ctx: [DraftCheck(
                id="smoke", kind="custom_cmd", spec={"argv": ["true"]})])
        fixture = load_fixture("docs_site")
        result = compile_dod(
            fixture["intake"], plan_of(fixture),
            replaying(fixture["provider_draft"]))
        assert [c.id for c in result.dod.checks if c.source == "standard"] == [
            "std-smoke"]

    def test_a_duplicate_registration_is_an_error_not_a_silent_overwrite(self):
        register_standard_check_provider("smoke", lambda ctx: [])
        with pytest.raises(ValueError) as exc:
            register_standard_check_provider("smoke", lambda ctx: [])
        assert "already registered" in str(exc.value)

    def test_an_empty_registry_changes_nothing(self):
        plan = simple_plan("tests/x/test_a.py passes")
        assert registered_standard_check_providers() == ()
        assert all(c.source == "plan_acceptance"
                   for c in compile_dod({"goal": "g"}, plan, None).dod.checks)
