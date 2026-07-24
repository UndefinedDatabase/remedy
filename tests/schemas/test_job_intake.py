"""F013 T001 — JobIntake schema: round-trip, rejection, registry."""
from __future__ import annotations

import json

import pytest

from packages.orchestration.schemas import (
    JOB_INTAKE_SCHEMA_V,
    PARSE_ERROR_CLASS,
    SCHEMA_REGISTRY,
    JobIntake,
    schema_v_of,
    to_json_schema,
    to_json_schema_str,
    validate_response,
)

_VALID = {
    "schema_v": "ji1",
    "goal": "Add pagination to the user list endpoint.",
    "context_refs": ["src/api/users.py", "docs/pagination.md"],
    "constraints": ["No breaking API changes"],
    "acceptance_hints": ["GET /users?page=2 returns page 2"],
    "truncated_input": False,
    "clarifications": [
        {
            "question": "Should we support cursor-based pagination?",
            "default_answer": "No, offset-based is sufficient.",
            "impact": "Changes the query parameter contract.",
        },
    ],
}

_VALID_MINIMAL = {
    "schema_v": "ji1",
    "goal": "Fix the login bug.",
}


class TestJobIntakeVersioning:
    def test_schema_v_constant(self):
        assert JOB_INTAKE_SCHEMA_V == "ji1"
        assert schema_v_of(JobIntake) == "ji1"

    def test_registered_in_schema_registry(self):
        assert SCHEMA_REGISTRY[JOB_INTAKE_SCHEMA_V] is JobIntake

    def test_schema_v_is_required(self):
        assert "schema_v" in JobIntake.model_fields
        assert JobIntake.model_fields["schema_v"].is_required()
        assert "schema_v" in to_json_schema(JobIntake).get("required", [])

    def test_tag_is_compact(self):
        assert 2 <= len(JOB_INTAKE_SCHEMA_V) <= 6


class TestJobIntakeRoundTrip:
    def test_valid_full_payload(self):
        res = validate_response(JobIntake, json.dumps(_VALID))
        assert res.ok, res.hint
        assert isinstance(res.value, JobIntake)
        assert res.value.goal == _VALID["goal"]
        assert res.value.context_refs == _VALID["context_refs"]
        assert len(res.value.clarifications) == 1
        assert res.value.clarifications[0].question == _VALID["clarifications"][0]["question"]

    def test_valid_minimal_payload(self):
        res = validate_response(JobIntake, json.dumps(_VALID_MINIMAL))
        assert res.ok, res.hint
        assert res.value.goal == "Fix the login bug."
        assert res.value.context_refs == []
        assert res.value.constraints == []
        assert res.value.acceptance_hints == []
        assert res.value.truncated_input is False
        assert res.value.clarifications == []

    def test_round_trip_is_stable(self):
        first = validate_response(JobIntake, json.dumps(_VALID)).value
        again = validate_response(JobIntake, first.model_dump_json()).value
        assert first == again
        assert first.model_dump_json() == again.model_dump_json()

    def test_dict_input_accepted(self):
        assert validate_response(JobIntake, _VALID).ok

    def test_fenced_json_accepted(self):
        raw = "```json\n" + json.dumps(_VALID) + "\n```"
        assert validate_response(JobIntake, raw).ok


class TestJobIntakeRejection:
    def test_missing_schema_v(self):
        bad = dict(_VALID)
        del bad["schema_v"]
        res = validate_response(JobIntake, json.dumps(bad))
        assert not res.ok and res.error_class == PARSE_ERROR_CLASS
        assert "schema_v" in res.hint

    def test_wrong_schema_v(self):
        res = validate_response(JobIntake, json.dumps({**_VALID, "schema_v": "zz9"}))
        assert not res.ok and res.error_class == PARSE_ERROR_CLASS

    def test_missing_goal(self):
        bad = {"schema_v": "ji1"}
        res = validate_response(JobIntake, json.dumps(bad))
        assert not res.ok and res.error_class == PARSE_ERROR_CLASS
        assert "goal" in res.hint

    def test_wrong_type_goal(self):
        res = validate_response(JobIntake, json.dumps({**_VALID, "goal": 42}))
        assert not res.ok and res.error_class == PARSE_ERROR_CLASS
        assert "goal" in res.hint

    def test_extra_field_forbidden(self):
        res = validate_response(JobIntake, json.dumps({**_VALID, "surprise": 1}))
        assert not res.ok and res.error_class == PARSE_ERROR_CLASS
        assert "surprise" in res.hint

    def test_extra_field_in_clarification_forbidden(self):
        bad = {**_VALID, "clarifications": [{
            "question": "q", "default_answer": "a", "impact": "i", "extra": True,
        }]}
        res = validate_response(JobIntake, json.dumps(bad))
        assert not res.ok and res.error_class == PARSE_ERROR_CLASS
        assert "extra" in res.hint

    def test_wrong_type_truncated_input(self):
        res = validate_response(JobIntake, json.dumps({**_VALID, "truncated_input": [1, 2]}))
        assert not res.ok and res.error_class == PARSE_ERROR_CLASS

    def test_clarifications_over_max_rejected(self):
        clarifications = [
            {"question": f"q{i}", "default_answer": f"a{i}", "impact": f"i{i}"}
            for i in range(6)
        ]
        res = validate_response(JobIntake, json.dumps({**_VALID, "clarifications": clarifications}))
        assert not res.ok and res.error_class == PARSE_ERROR_CLASS

    def test_not_json_is_parse_failure(self):
        res = validate_response(JobIntake, "just a plain text mission")
        assert not res.ok and res.error_class == PARSE_ERROR_CLASS
        assert res.json_error is True


class TestJobIntakeSchemaSize:
    def test_schema_stays_under_ceiling(self):
        assert len(to_json_schema_str(JobIntake)) <= 1500

    @pytest.mark.parametrize("field", [
        "goal", "context_refs", "constraints", "acceptance_hints",
        "truncated_input", "clarifications",
    ])
    def test_expected_fields_in_schema(self, field):
        props = to_json_schema(JobIntake)["properties"]
        assert field in props
