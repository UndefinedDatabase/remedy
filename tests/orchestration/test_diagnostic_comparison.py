"""Round 39 F2 — diagnostic comparison producer/validator contract tests.

Every producer output validates. Every tampered field is detected. The validator
recomputes SHA-256, sortedness, set equality, and set differences independently.
"""
from __future__ import annotations

import pytest

from packages.orchestration.diagnostic_comparison import (
    DIAGNOSTIC_COMPARISON_SCHEMA_VERSION,
    DiagnosticComparisonError,
    produce_diagnostic_comparison,
    validate_diagnostic_comparison,
)

_BASE = "afe8394abc"
_HEAD = "f3ed24fdef"
_CMD = "python3 -m pytest tests/orchestration/ --tb=no -q"


def _make(**overrides):
    defaults = dict(
        base_commit=_BASE, head_commit=_HEAD, command=_CMD,
        base_failure_node_ids=["tests/a.py::test_x", "tests/b.py::test_y"],
        head_failure_node_ids=["tests/a.py::test_x", "tests/b.py::test_y"],
        base_passed=100, base_failed=2, base_skipped=1,
        head_passed=100, head_failed=2, head_skipped=1,
    )
    defaults.update(overrides)
    return produce_diagnostic_comparison(**defaults)


class TestProducerOutputValidates:
    def test_identical_failures(self):
        c = _make()
        assert c["failure_sets_equal"] is True
        assert c["only_in_base"] == []
        assert c["only_in_head"] == []
        assert validate_diagnostic_comparison(c, _HEAD) == []

    def test_different_failures(self):
        c = _make(
            head_failure_node_ids=["tests/c.py::test_z"],
            head_failed=1,
        )
        assert c["failure_sets_equal"] is False
        assert "tests/a.py::test_x" in c["only_in_base"]
        assert "tests/c.py::test_z" in c["only_in_head"]
        assert validate_diagnostic_comparison(c, _HEAD) == []

    def test_empty_failure_sets(self):
        c = _make(
            base_failure_node_ids=[], head_failure_node_ids=[],
            base_failed=0, head_failed=0,
        )
        assert c["failure_sets_equal"] is True
        assert validate_diagnostic_comparison(c, _HEAD) == []

    def test_base_only_failures(self):
        c = _make(
            head_failure_node_ids=[], head_failed=0,
        )
        assert c["failure_sets_equal"] is False
        assert len(c["only_in_base"]) == 2
        assert c["only_in_head"] == []
        assert validate_diagnostic_comparison(c, _HEAD) == []

    def test_node_ids_are_sorted_and_deduped(self):
        c = _make(
            base_failure_node_ids=["z::test", "a::test", "a::test"],
            base_failed=2,
        )
        assert c["base"]["failure_node_ids"] == ["a::test", "z::test"]
        assert validate_diagnostic_comparison(c, _HEAD) == []


class TestProducerRejectsInvalid:
    def test_missing_base_commit(self):
        with pytest.raises(DiagnosticComparisonError, match="base_commit"):
            _make(base_commit="")

    def test_missing_head_commit(self):
        with pytest.raises(DiagnosticComparisonError, match="head_commit"):
            _make(head_commit="")

    def test_missing_command(self):
        with pytest.raises(DiagnosticComparisonError, match="command"):
            _make(command="")


class TestValidatorDetectsTampering:
    def test_wrong_schema_version(self):
        c = _make()
        c["schema_version"] = "999.0.0"
        problems = validate_diagnostic_comparison(c, _HEAD)
        assert any("schema_version" in p for p in problems)

    def test_wrong_head_commit(self):
        c = _make()
        problems = validate_diagnostic_comparison(c, "wrong_commit")
        assert any("head_commit" in p for p in problems)

    def test_tampered_failure_set_sha256(self):
        c = _make()
        c["base"]["failure_set_sha256"] = "0" * 64
        problems = validate_diagnostic_comparison(c, _HEAD)
        assert any("failure_set_sha256 mismatch" in p for p in problems)

    def test_tampered_failure_sets_equal(self):
        c = _make()
        c["failure_sets_equal"] = False
        problems = validate_diagnostic_comparison(c, _HEAD)
        assert any("failure_sets_equal" in p for p in problems)

    def test_unsorted_node_ids(self):
        c = _make()
        c["head"]["failure_node_ids"] = ["z::test", "a::test"]
        problems = validate_diagnostic_comparison(c, _HEAD)
        assert any("not sorted" in p for p in problems)

    def test_duplicate_node_ids(self):
        c = _make()
        c["head"]["failure_node_ids"] = ["a::test", "a::test"]
        problems = validate_diagnostic_comparison(c, _HEAD)
        assert any("duplicates" in p for p in problems)

    def test_failed_count_mismatch(self):
        c = _make()
        c["base"]["failed"] = 999
        problems = validate_diagnostic_comparison(c, _HEAD)
        assert any("failed" in p and "999" in p for p in problems)

    def test_tampered_only_in_base(self):
        c = _make(
            head_failure_node_ids=["tests/c.py::test_z"], head_failed=1,
        )
        c["only_in_base"] = []
        problems = validate_diagnostic_comparison(c, _HEAD)
        assert any("only_in_base" in p for p in problems)

    def test_tampered_only_in_head(self):
        c = _make(
            head_failure_node_ids=["tests/c.py::test_z"], head_failed=1,
        )
        c["only_in_head"] = []
        problems = validate_diagnostic_comparison(c, _HEAD)
        assert any("only_in_head" in p for p in problems)

    def test_missing_required_key(self):
        c = _make()
        del c["failure_sets_equal"]
        problems = validate_diagnostic_comparison(c, _HEAD)
        assert any("missing required keys" in p for p in problems)

    def test_missing_side_key(self):
        c = _make()
        del c["base"]["failure_set_sha256"]
        problems = validate_diagnostic_comparison(c, _HEAD)
        assert any("missing keys" in p for p in problems)

    def test_not_a_dict(self):
        problems = validate_diagnostic_comparison("not a dict", _HEAD)
        assert any("not a dict" in p for p in problems)

    def test_side_not_a_dict(self):
        c = _make()
        c["base"] = "not a dict"
        problems = validate_diagnostic_comparison(c, _HEAD)
        assert any("not a dict" in p for p in problems)


class TestSchemaVersion:
    def test_version_is_2_0_0(self):
        assert DIAGNOSTIC_COMPARISON_SCHEMA_VERSION == "2.0.0"

    def test_producer_emits_version(self):
        c = _make()
        assert c["schema_version"] == "2.0.0"
