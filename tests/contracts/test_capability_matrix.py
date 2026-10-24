"""F157 T002: the capability matrix, its unit tests and its two guards (DECISION F157 D2).

The read guard (`capability_read_violations`) and the consumer guard
(`unregistered_consumer_violations`) live here, in the manner of
`tests/contracts/test_adapter_import_guard.py`: each parses source text directly, so a violation
fixture needs no file on disk, and each sweeps `packages/` and `apps/` to prove the live tree red
if it were wrong.
"""
from __future__ import annotations

import ast
import re
import types
from dataclasses import fields
from pathlib import Path

import pytest

from packages.contracts.adapter_contract import AdapterCapabilities
from packages.contracts.capability_matrix import (
    CAPABILITY_DEGRADATIONS_FIELD,
    CAPABILITY_MODE_DEGRADED,
    CAPABILITY_MODE_NATIVE,
    CAPABILITY_MODE_UNAVAILABLE,
    CAPABILITY_NO_CONSUMER_NOTES,
    CAPABILITY_REQUIREMENTS,
    CapabilityConsumerUnregistered,
    CapabilityDecision,
    CapabilityRequirement,
    capability_decision_record,
    capability_degradation_entries,
    capability_matrix_for,
    capability_present,
    format_capability_degradations,
    require_or_degrade,
)

REPO_ROOT = Path(__file__).resolve().parents[2]

# WHY: the three paths D2 (7) allows a `.capabilities(` call in; every other site asks the matrix.
CAPABILITY_READ_SITES = (
    "packages/contracts/capability_matrix.py",
    "packages/contracts/adapter_conformance_kit.py",
    "apps/cli/commands/worker.py",
)


class _ToyAdapter:
    """A toy `WorkerAdapter` whose `capabilities()` returns a fixed answer and counts its calls."""

    adapter_id = "toy"

    def __init__(self, capabilities: AdapterCapabilities) -> None:
        self._capabilities = capabilities
        self.calls = 0

    def capabilities(self, model: str) -> AdapterCapabilities:
        self.calls += 1
        return self._capabilities


def _full_capabilities(**overrides) -> AdapterCapabilities:
    base = dict(
        vision=True, json_schema=True, session_resume=True, streaming=True, tool_use=True,
        max_context_tokens=1,
    )
    base.update(overrides)
    return AdapterCapabilities(**base)


def _empty_capabilities(**overrides) -> AdapterCapabilities:
    base = dict(
        vision=False, json_schema=False, session_resume=False, streaming=False, tool_use=False,
        max_context_tokens=0,
    )
    base.update(overrides)
    return AdapterCapabilities(**base)


# -- Per register entry -------------------------------------------------------------------------

@pytest.mark.parametrize("feature_key,requirement", list(CAPABILITY_REQUIREMENTS.items()))
def test_native_when_every_required_capability_is_present(feature_key, requirement):
    adapter = _ToyAdapter(_full_capabilities())
    decision = require_or_degrade(feature_key, adapter, "model-x")
    assert decision == CapabilityDecision(
        feature_key=feature_key, mode=CAPABILITY_MODE_NATIVE, strategy=None, missing=(),
    )
    assert adapter.calls == 1


@pytest.mark.parametrize("feature_key,requirement", list(CAPABILITY_REQUIREMENTS.items()))
def test_degraded_with_the_entrys_token_and_missing_names_it_when_absent(feature_key, requirement):
    absent = {name: (False if name != "max_context_tokens" else 0) for name in requirement.requires}
    adapter = _ToyAdapter(_full_capabilities(**absent))
    decision = require_or_degrade(feature_key, adapter, "model-x")
    assert decision.mode == CAPABILITY_MODE_DEGRADED
    assert decision.strategy == requirement.degradation
    assert decision.missing == requirement.requires


def test_unavailable_through_a_test_local_requirement_with_no_degradation():
    local_requirements = types.MappingProxyType({
        "refusal_only_feature": CapabilityRequirement(
            requires=("vision",), degradation=None, notes="This feature may refuse outright.",
        ),
    })
    adapter = _ToyAdapter(_empty_capabilities())
    decision = require_or_degrade(
        "refusal_only_feature", adapter, "model-x", requirements=local_requirements,
    )
    assert decision.mode == CAPABILITY_MODE_UNAVAILABLE
    assert decision.strategy is None
    assert decision.missing == ("vision",)


def test_an_unregistered_key_raises_before_any_capability_is_read():
    adapter = _ToyAdapter(_full_capabilities())
    with pytest.raises(CapabilityConsumerUnregistered, match="no_such_feature"):
        require_or_degrade("no_such_feature", adapter, "model-x")
    assert adapter.calls == 0


# -- capability_present --------------------------------------------------------------------------

def test_max_context_tokens_at_zero_is_absent():
    assert capability_present(_full_capabilities(max_context_tokens=0), "max_context_tokens") is False


def test_max_context_tokens_at_one_is_present():
    assert capability_present(_full_capabilities(max_context_tokens=1), "max_context_tokens") is True


@pytest.mark.parametrize("flag", ["vision", "json_schema", "session_resume", "streaming", "tool_use"])
def test_a_bool_flag_is_present_or_absent_both_ways(flag):
    assert capability_present(_full_capabilities(**{flag: True}), flag) is True
    assert capability_present(_full_capabilities(**{flag: False}), flag) is False


def test_an_unknown_name_raises_value_error():
    with pytest.raises(ValueError, match="bogus"):
        capability_present(_full_capabilities(), "bogus")


# -- missing order --------------------------------------------------------------------------------

def test_missing_lists_two_absent_names_in_the_requirement_order():
    local_requirements = types.MappingProxyType({
        "two_capability_feature": CapabilityRequirement(
            requires=("json_schema", "streaming"), degradation="fallback_mode", notes="Needs two.",
        ),
    })
    adapter = _ToyAdapter(_empty_capabilities())
    decision = require_or_degrade(
        "two_capability_feature", adapter, "model-x", requirements=local_requirements,
    )
    assert decision.missing == ("json_schema", "streaming")


# -- capability_matrix_for ------------------------------------------------------------------------

def test_capability_matrix_for_answers_one_decision_per_entry_with_exactly_one_call():
    adapter = _ToyAdapter(_full_capabilities())
    decisions = capability_matrix_for(adapter, "model-x")
    assert [d.feature_key for d in decisions] == list(CAPABILITY_REQUIREMENTS.keys())
    assert adapter.calls == 1


# -- capability_decision_record / capability_degradation_entries ---------------------------------

def test_capability_decision_record_carries_its_keys_and_a_list_typed_missing():
    decision = CapabilityDecision(
        feature_key="x", mode=CAPABILITY_MODE_DEGRADED, strategy="y", missing=("a", "b"),
    )
    record = capability_decision_record(decision)
    assert set(record.keys()) == {"feature_key", "mode", "strategy", "missing"}
    assert record["missing"] == ["a", "b"]
    assert isinstance(record["missing"], list)


def test_capability_degradation_entries_drops_native_and_dedupes_in_first_seen_order():
    native = CapabilityDecision(feature_key="native_one", mode=CAPABILITY_MODE_NATIVE, strategy=None, missing=())
    degraded_a = CapabilityDecision(
        feature_key="a", mode=CAPABILITY_MODE_DEGRADED, strategy="s", missing=("json_schema",),
    )
    degraded_a_repeat = CapabilityDecision(
        feature_key="a", mode=CAPABILITY_MODE_DEGRADED, strategy="s", missing=("json_schema",),
    )
    degraded_b = CapabilityDecision(
        feature_key="b", mode=CAPABILITY_MODE_UNAVAILABLE, strategy=None, missing=("vision",),
    )
    entries = capability_degradation_entries([native, degraded_a, degraded_a_repeat, degraded_b])
    assert entries == [
        capability_decision_record(degraded_a),
        capability_decision_record(degraded_b),
    ]


# -- format_capability_degradations ---------------------------------------------------------------

def test_format_capability_degradations_of_an_empty_list_is_none():
    assert format_capability_degradations([]) == "none"


def test_format_capability_degradations_of_a_degraded_entry():
    entry = capability_decision_record(CapabilityDecision(
        feature_key="a", mode=CAPABILITY_MODE_DEGRADED, strategy="s", missing=("json_schema",),
    ))
    assert format_capability_degradations([entry]) == "a as s"


def test_format_capability_degradations_of_an_unavailable_entry():
    entry = capability_decision_record(CapabilityDecision(
        feature_key="b", mode=CAPABILITY_MODE_UNAVAILABLE, strategy=None, missing=("vision",),
    ))
    assert format_capability_degradations([entry]) == "b unavailable"


def test_format_capability_degradations_of_two_entries_joined():
    degraded = capability_decision_record(CapabilityDecision(
        feature_key="a", mode=CAPABILITY_MODE_DEGRADED, strategy="s", missing=("json_schema",),
    ))
    unavailable = capability_decision_record(CapabilityDecision(
        feature_key="b", mode=CAPABILITY_MODE_UNAVAILABLE, strategy=None, missing=("vision",),
    ))
    assert format_capability_degradations([degraded, unavailable]) == "a as s, b unavailable"


# -- completeness ----------------------------------------------------------------------------------

def test_required_names_and_no_consumer_names_partition_the_contract_fields():
    required_names = {name for req in CAPABILITY_REQUIREMENTS.values() for name in req.requires}
    no_consumer_names = set(CAPABILITY_NO_CONSUMER_NOTES.keys())
    assert required_names.isdisjoint(no_consumer_names)
    all_field_names = {f.name for f in fields(AdapterCapabilities)}
    assert required_names | no_consumer_names == all_field_names


def test_every_notes_and_every_note_is_non_empty():
    for requirement in CAPABILITY_REQUIREMENTS.values():
        assert requirement.notes.strip()
    for note in CAPABILITY_NO_CONSUMER_NOTES.values():
        assert note.strip()


def test_every_degradation_token_matches_the_naming_convention():
    pattern = re.compile(r"^[a-z][a-z0-9_]*$")
    for requirement in CAPABILITY_REQUIREMENTS.values():
        if requirement.degradation is not None:
            assert pattern.fullmatch(requirement.degradation)


def test_the_run_record_field_is_not_the_generic_degraded_word():
    assert CAPABILITY_DEGRADATIONS_FIELD == "capability_degradations"


# -- the frozen register ---------------------------------------------------------------------------

def test_assigning_a_key_to_the_register_raises_type_error():
    with pytest.raises(TypeError):
        CAPABILITY_REQUIREMENTS["new_key"] = CapabilityRequirement(  # type: ignore[index]
            requires=(), degradation=None, notes="x",
        )


# -- the read guard: `.capabilities(` only at a CAPABILITY_READ_SITES path -------------------------

def capability_read_violations(source: str, rel_path: str) -> list[str]:
    """`path:line` of every `.capabilities(` call in `source`, unless `rel_path` is a read site."""
    if rel_path in CAPABILITY_READ_SITES:
        return []
    tree = ast.parse(source)
    violations = []
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr == "capabilities"):
            violations.append(f"{rel_path}:{node.lineno}")
    return violations


def _walk_py(*trees: str) -> list[Path]:
    paths = []
    for tree_rel in trees:
        for path in sorted((REPO_ROOT / tree_rel).rglob("*.py")):
            if "__pycache__" in path.parts:
                continue
            paths.append(path)
    return paths


def _has_capabilities_call(source: str) -> bool:
    tree = ast.parse(source)
    return any(
        isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
        and node.func.attr == "capabilities"
        for node in ast.walk(tree)
    )


def test_no_file_under_packages_or_apps_reads_capabilities_outside_the_read_sites():
    violations = []
    for path in _walk_py("packages", "apps"):
        rel = path.relative_to(REPO_ROOT).as_posix()
        violations.extend(capability_read_violations(path.read_text(encoding="utf-8"), rel))
    assert violations == []


def test_every_capability_read_site_exists_and_reads_capabilities_at_least_once():
    for rel in CAPABILITY_READ_SITES:
        path = REPO_ROOT / rel
        assert path.is_file(), rel
        assert _has_capabilities_call(path.read_text(encoding="utf-8")), rel


def test_the_read_guard_reports_a_violation_fixture():
    violation_fixture = (
        "def call_it(adapter):\n"
        '    return adapter.capabilities("m")\n'
    )
    violations = capability_read_violations(violation_fixture, "packages/orchestration/fixture.py")
    assert len(violations) == 1


# -- the consumer guard: every `require_or_degrade(` first argument is a registered literal key ---

def unregistered_consumer_violations(source: str, rel_path: str) -> list[str]:
    """`path:line` of every `require_or_degrade(` call whose first argument is not a string
    constant naming a `CAPABILITY_REQUIREMENTS` key."""
    tree = ast.parse(source)
    violations = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", None)
        if name != "require_or_degrade":
            continue
        first = node.args[0] if node.args else None
        if (isinstance(first, ast.Constant) and isinstance(first.value, str)
                and first.value in CAPABILITY_REQUIREMENTS):
            continue
        violations.append(f"{rel_path}:{node.lineno}")
    return violations


def test_no_call_to_require_or_degrade_under_packages_or_apps_names_an_unregistered_key():
    violations = []
    for path in _walk_py("packages", "apps"):
        rel = path.relative_to(REPO_ROOT).as_posix()
        violations.extend(unregistered_consumer_violations(path.read_text(encoding="utf-8"), rel))
    assert violations == []


def test_the_consumer_guard_reports_an_unknown_literal_key():
    violation_fixture = (
        "from packages.contracts.capability_matrix import require_or_degrade\n"
        "def call_it(adapter):\n"
        '    return require_or_degrade("no_such_feature", adapter, "m")\n'
    )
    violations = unregistered_consumer_violations(violation_fixture, "packages/orchestration/fixture.py")
    assert len(violations) == 1


def test_the_consumer_guard_reports_a_variable_key():
    violation_fixture = (
        "from packages.contracts.capability_matrix import require_or_degrade\n"
        "def call_it(adapter, key):\n"
        "    return require_or_degrade(key, adapter, \"m\")\n"
    )
    violations = unregistered_consumer_violations(violation_fixture, "packages/orchestration/fixture.py")
    assert len(violations) == 1


def test_the_consumer_guard_reports_no_violation_for_a_registered_literal_key():
    clean_fixture = (
        "from packages.contracts.capability_matrix import require_or_degrade\n"
        "def call_it(adapter):\n"
        '    return require_or_degrade("reviewer_schema_gate", adapter, "m")\n'
    )
    assert unregistered_consumer_violations(clean_fixture, "packages/orchestration/fixture.py") == []
