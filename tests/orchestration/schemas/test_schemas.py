"""F005 T001 — schemas package: goldens, round-trip, validation, size snapshots."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.orchestration.dod_schema import (
    DOD_DRAFT_SCHEMA_V,
    DOD_SCHEMA_V,
    DoD,
)
from packages.orchestration.schemas import (
    DESIGN_SPEC_SCHEMA_V,
    PARSE_ERROR_CLASS,
    PLANNER_PLAN_SCHEMA_V,
    REVIEW_VERDICT_SCHEMA_V,
    SCHEMA_REGISTRY,
    DesignSpec,
    PlannerPlan,
    ReviewVerdict,
    schema_v_of,
    to_json_schema,
    to_json_schema_str,
    validate_response,
)

GOLDENS = Path(__file__).parent / "goldens"


def _golden(name: str) -> str:
    return (GOLDENS / name).read_text()


# ---------------------------------------------------------------------------
# schema_v presence and registry
# ---------------------------------------------------------------------------

class TestSchemaVersioning:
    @pytest.mark.parametrize("model,tag", [
        (ReviewVerdict, REVIEW_VERDICT_SCHEMA_V),
        (PlannerPlan, PLANNER_PLAN_SCHEMA_V),
        (DesignSpec, DESIGN_SPEC_SCHEMA_V),
        (DoD, DOD_SCHEMA_V),
    ])
    def test_every_model_declares_schema_v(self, model, tag):
        assert schema_v_of(model) == tag
        assert "schema_v" in model.model_fields
        # The tag is a required, pinned field — it appears in the JSON schema.
        assert "schema_v" in to_json_schema(model)["properties"]

    def test_registry_maps_each_tag_to_its_model(self):
        assert SCHEMA_REGISTRY[REVIEW_VERDICT_SCHEMA_V] is ReviewVerdict
        assert SCHEMA_REGISTRY[PLANNER_PLAN_SCHEMA_V] is PlannerPlan
        assert SCHEMA_REGISTRY[DESIGN_SPEC_SCHEMA_V] is DesignSpec
        assert SCHEMA_REGISTRY[DOD_SCHEMA_V] is DoD

    def test_the_provider_facing_dod_draft_is_not_registered(self):
        """Only contracts a reader must resolve from a tag belong in the registry.

        A ``dod_v1`` payload is persisted in a job's evidence area, so its tag
        has to resolve. ``dod_draft_v1`` never leaves the compiler's own call —
        registering it would put a tag nobody resolves in the one place that
        claims to be the source of truth for what a tag means.
        """
        assert DOD_DRAFT_SCHEMA_V not in SCHEMA_REGISTRY

    def test_tags_are_compact(self):
        # flight_plan_v1 (14) and mission_plan_v1 (15) deliberately use
        # descriptive tags — both name a PLAN a human reads in evidence, where
        # "fp1"/"mp1" would be a riddle. The exemption is a named list, not a
        # raised limit: every other tag must stay <= 6 chars (compact guard).
        _LONG_TAG_EXEMPTIONS = {"flight_plan_v1", "mission_plan_v1"}
        for tag in SCHEMA_REGISTRY:
            if tag in _LONG_TAG_EXEMPTIONS:
                assert len(tag) <= 15, f"exempted tag {tag!r} exceeds 15"
            else:
                assert 2 <= len(tag) <= 6, f"schema_v {tag!r} is not compact"


class TestSchemaVMandatory:
    """F005 Finding 1: schema_v is REQUIRED in every top-level response."""

    _BASE = {
        ReviewVerdict: {"verdict": "pass", "findings": [], "confidence": "high", "summary": "ok"},
        PlannerPlan: {"summary": "s", "proposed_tasks": [{"task_type": "t", "description": "d"}]},
        DesignSpec: {"summary": "s"},
    }
    _TAG = {ReviewVerdict: "rv1", PlannerPlan: "pp1", DesignSpec: "ds1"}

    @pytest.mark.parametrize("model", [ReviewVerdict, PlannerPlan, DesignSpec])
    def test_missing_schema_v_is_rejected(self, model):
        res = validate_response(model, json.dumps(self._BASE[model]))
        assert not res.ok and res.error_class == PARSE_ERROR_CLASS
        assert "schema_v" in res.hint

    @pytest.mark.parametrize("model", [ReviewVerdict, PlannerPlan, DesignSpec])
    def test_correct_schema_v_is_accepted(self, model):
        payload = dict(self._BASE[model], schema_v=self._TAG[model])
        assert validate_response(model, json.dumps(payload)).ok

    @pytest.mark.parametrize("model", [ReviewVerdict, PlannerPlan, DesignSpec])
    def test_wrong_schema_v_is_rejected(self, model):
        payload = dict(self._BASE[model], schema_v="zz9")
        res = validate_response(model, json.dumps(payload))
        assert not res.ok and res.error_class == PARSE_ERROR_CLASS

    @pytest.mark.parametrize("model", [ReviewVerdict, PlannerPlan, DesignSpec])
    def test_generated_schema_marks_schema_v_required(self, model):
        assert "schema_v" in to_json_schema(model).get("required", [])

    def test_schema_v_of_reads_classvar_not_field_default(self, model=ReviewVerdict):
        # The field has no default now; schema_v_of must still work.
        assert model.model_fields["schema_v"].is_required()
        assert schema_v_of(model) == "rv1"


# ---------------------------------------------------------------------------
# golden valid examples + round-trip
# ---------------------------------------------------------------------------

class TestGoldensAndRoundTrip:
    @pytest.mark.parametrize("model,golden", [
        (ReviewVerdict, "valid_review_verdict.json"),
        (PlannerPlan, "valid_planner_plan.json"),
        (DesignSpec, "valid_design_spec.json"),
    ])
    def test_golden_validates(self, model, golden):
        res = validate_response(model, _golden(golden))
        assert res.ok, res.hint
        assert isinstance(res.value, model)

    @pytest.mark.parametrize("model,golden", [
        (ReviewVerdict, "valid_review_verdict.json"),
        (PlannerPlan, "valid_planner_plan.json"),
        (DesignSpec, "valid_design_spec.json"),
    ])
    def test_round_trip_is_stable(self, model, golden):
        first = validate_response(model, _golden(golden)).value
        again = validate_response(model, first.model_dump_json()).value
        assert first == again
        # A second serialization is byte-identical — genuinely stable.
        assert first.model_dump_json() == again.model_dump_json()

    def test_review_findings_survive_round_trip(self):
        v = validate_response(ReviewVerdict, _golden("valid_review_verdict.json")).value
        assert [f.id for f in v.findings] == ["F1", "F2"]
        assert v.findings[0].severity == "high"


# ---------------------------------------------------------------------------
# invalid examples -> classified parse failures with a hint
# ---------------------------------------------------------------------------

_VALID_REVIEW = {
    "schema_v": "rv1", "verdict": "pass", "findings": [],
    "confidence": "high", "summary": "ok",
}
_VALID_PLAN = {
    "schema_v": "pp1", "summary": "s",
    "proposed_tasks": [{"task_type": "implement", "description": "d"}],
}


def _mutate(base: dict, **changes) -> dict:
    out = dict(base)
    out.update(changes)
    return out


class TestInvalidResponses:
    def test_missing_required_field(self):
        bad = dict(_VALID_REVIEW)
        del bad["verdict"]
        res = validate_response(ReviewVerdict, json.dumps(bad))
        assert not res.ok and res.error_class == PARSE_ERROR_CLASS
        assert "verdict" in res.hint

    def test_wrong_enum_value(self):
        res = validate_response(ReviewVerdict, json.dumps(_mutate(_VALID_REVIEW, verdict="maybe")))
        assert not res.ok and res.error_class == PARSE_ERROR_CLASS
        assert "verdict" in res.hint

    def test_wrong_field_type(self):
        res = validate_response(ReviewVerdict, json.dumps(_mutate(_VALID_REVIEW, summary=123)))
        assert not res.ok and res.error_class == PARSE_ERROR_CLASS
        assert "summary" in res.hint

    def test_unsupported_schema_v(self):
        res = validate_response(ReviewVerdict, json.dumps(_mutate(_VALID_REVIEW, schema_v="rv9")))
        assert not res.ok and res.error_class == PARSE_ERROR_CLASS
        assert "schema_v" in res.hint

    def test_additional_unexpected_field_forbidden(self):
        res = validate_response(ReviewVerdict, json.dumps(_mutate(_VALID_REVIEW, surprise=1)))
        assert not res.ok and res.error_class == PARSE_ERROR_CLASS
        assert "surprise" in res.hint

    def test_unexpected_field_in_nested_finding_forbidden(self):
        bad = _mutate(_VALID_REVIEW, findings=[{
            "id": "F1", "severity": "low", "file": "a", "summary": "s", "extra": 1,
        }])
        res = validate_response(ReviewVerdict, json.dumps(bad))
        assert not res.ok and res.error_class == PARSE_ERROR_CLASS
        assert "extra" in res.hint

    def test_planner_requires_at_least_one_task(self):
        res = validate_response(PlannerPlan, json.dumps(_mutate(_VALID_PLAN, proposed_tasks=[])))
        assert not res.ok and res.error_class == PARSE_ERROR_CLASS
        assert "proposed_tasks" in res.hint

    def test_not_json_is_a_parse_failure(self):
        res = validate_response(ReviewVerdict, "sorry, here is my review: looks good!")
        assert not res.ok and res.error_class == PARSE_ERROR_CLASS
        assert res.json_error is True

    def test_malformed_json_is_a_parse_failure(self):
        res = validate_response(ReviewVerdict, '{"schema_v":"rv1","verdict":"pass",')
        assert not res.ok and res.error_class == PARSE_ERROR_CLASS
        assert res.json_error is True

    def test_hint_is_concise(self):
        # Many simultaneous errors must not produce a giant hint.
        res = validate_response(ReviewVerdict, json.dumps({"schema_v": "rv9"}))
        assert not res.ok
        assert len(res.hint) <= 240


class TestLenientExtraction:
    def test_fenced_json_accepted(self):
        raw = "```json\n" + json.dumps(_VALID_REVIEW) + "\n```"
        assert validate_response(ReviewVerdict, raw).ok

    def test_prose_wrapped_object_accepted(self):
        raw = "Here you go: " + json.dumps(_VALID_REVIEW) + " — thanks!"
        assert validate_response(ReviewVerdict, raw).ok

    def test_already_parsed_dict_accepted(self):
        assert validate_response(ReviewVerdict, _VALID_REVIEW).ok


# ---------------------------------------------------------------------------
# schema-size snapshots — guard against accidental schema bloat
# ---------------------------------------------------------------------------

class TestSchemaSize:
    #: Snapshot of the compact JSON-schema length. A change here means the schema
    #: grew or shrank — update deliberately, never to paper over bloat.
    SNAPSHOT = {
        ReviewVerdict: 1099,
        PlannerPlan: 909,
        DesignSpec: 525,
    }
    #: Hard ceilings so no model can ever balloon (tokens).
    CEILING = {
        ReviewVerdict: 1400,
        PlannerPlan: 1200,
        DesignSpec: 800,
    }

    @pytest.mark.parametrize("model", [ReviewVerdict, PlannerPlan, DesignSpec])
    def test_schema_size_matches_snapshot(self, model):
        size = len(to_json_schema_str(model))
        assert size == self.SNAPSHOT[model], (
            f"{model.__name__} schema size changed to {size} "
            f"(was {self.SNAPSHOT[model]}); update the snapshot intentionally"
        )

    @pytest.mark.parametrize("model", [ReviewVerdict, PlannerPlan, DesignSpec])
    def test_schema_stays_under_ceiling(self, model):
        assert len(to_json_schema_str(model)) <= self.CEILING[model]
