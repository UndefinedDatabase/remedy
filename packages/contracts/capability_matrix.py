"""The capability matrix: a declarative register of what each capability-consuming feature needs
from an adapter and what it does when that capability is absent (DECISION F157 D2).

A consumer asks this register, never an adapter's ``capabilities()`` directly; ``require_or_degrade``
and ``capability_matrix_for`` take the resolved ``(adapter, model)`` pair and call
``capabilities(model)`` themselves, so a mid-job failover that changes the pair changes what the
next read sees.
"""
from __future__ import annotations

import types
from dataclasses import dataclass, fields

from packages.contracts.adapter_contract import AdapterCapabilities, WorkerAdapter

#: The field names `AdapterCapabilities` declares, read once rather than per call.
_CAPABILITY_FIELD_NAMES = frozenset(f.name for f in fields(AdapterCapabilities))

# WHY: the three outcomes a consumer's capability read resolves to (DECISION F157 D2 (3)).
CAPABILITY_MODE_NATIVE = "native"
CAPABILITY_MODE_DEGRADED = "degraded"
CAPABILITY_MODE_UNAVAILABLE = "unavailable"


# WHY: raised before any capability is read, so an unregistered feature key never silently degrades.
class CapabilityConsumerUnregistered(LookupError):
    """Raised by `require_or_degrade` when `feature_key` is not a `CAPABILITY_REQUIREMENTS` key."""


# WHY: one register entry — what a feature needs and what it does without it (DECISION F157 D2 (4)).
@dataclass(frozen=True)
class CapabilityRequirement:
    requires: tuple[str, ...]
    degradation: str | None
    notes: str


# WHY: one consumer's answer for one (adapter, model) pair (DECISION F157 D2 (3)).
@dataclass(frozen=True)
class CapabilityDecision:
    feature_key: str
    mode: str
    strategy: str | None
    missing: tuple[str, ...]


# WHY: the register DECISION F157 D2 (4) froze, in the reviewed inventory's order.
CAPABILITY_REQUIREMENTS: types.MappingProxyType[str, CapabilityRequirement] = types.MappingProxyType({
    "reviewer_schema_gate": CapabilityRequirement(
        requires=("json_schema",),
        degradation="schema_in_prompt",
        notes="The reviewer states the schema in the prompt and parses the free-text answer.",
    ),
    "planner_schema_gate": CapabilityRequirement(
        requires=("json_schema",),
        degradation="schema_in_prompt",
        notes="The planner states the schema in the prompt and parses the free-text answer.",
    ),
    "parked_session_resume": CapabilityRequirement(
        requires=("session_resume",),
        degradation="full_context_resend",
        notes="A parked session is dropped and the full context is resent from scratch.",
    ),
    "stream_evidence_capture": CapabilityRequirement(
        requires=("streaming",),
        degradation="buffered_output",
        notes="The call runs unstreamed and its evidence is captured from the buffered output.",
    ),
})

# WHY: the three declared capabilities no feature reads yet (DECISION F157 D2 (5)).
CAPABILITY_NO_CONSUMER_NOTES: types.MappingProxyType[str, str] = types.MappingProxyType({
    "vision": "No feature attaches or describes an image today; nothing consumes this flag.",
    "tool_use": "Every call's tool list is fixed by write mode, never chosen by this flag.",
    "max_context_tokens": "Declared but always 0 today; nothing truncates or resends on it.",
})


# WHY: whether one declared capability is usable, the one place "present" is defined (DECISION F157 D2 (3)).
def capability_present(capabilities: AdapterCapabilities, name: str) -> bool:
    if name not in _CAPABILITY_FIELD_NAMES:
        raise ValueError(f"not a capability field: {name!r}")
    value = getattr(capabilities, name)
    if name == "max_context_tokens":
        return value > 0
    return bool(value)


def _decide(
    feature_key: str,
    requirement: CapabilityRequirement,
    capabilities: AdapterCapabilities,
) -> CapabilityDecision:
    """The one decision rule both `require_or_degrade` and `capability_matrix_for` apply."""
    missing = tuple(
        name for name in requirement.requires if not capability_present(capabilities, name)
    )
    if not missing:
        return CapabilityDecision(
            feature_key=feature_key, mode=CAPABILITY_MODE_NATIVE, strategy=None, missing=(),
        )
    if requirement.degradation is None:
        return CapabilityDecision(
            feature_key=feature_key, mode=CAPABILITY_MODE_UNAVAILABLE, strategy=None, missing=missing,
        )
    return CapabilityDecision(
        feature_key=feature_key,
        mode=CAPABILITY_MODE_DEGRADED,
        strategy=requirement.degradation,
        missing=missing,
    )


# WHY: the one call every consumer makes — the register lookup first, the capability read second
# (DECISION F157 D2 (3)).
def require_or_degrade(
    feature_key: str,
    adapter: WorkerAdapter,
    model: str,
    *,
    requirements: types.MappingProxyType[str, CapabilityRequirement] = CAPABILITY_REQUIREMENTS,
) -> CapabilityDecision:
    if feature_key not in requirements:
        raise CapabilityConsumerUnregistered(f"unregistered capability consumer: {feature_key!r}")
    capabilities = adapter.capabilities(model)
    return _decide(feature_key, requirements[feature_key], capabilities)


# WHY: every registered entry's decision for one (adapter, model) pair, from a single capabilities() call.
def capability_matrix_for(
    adapter: WorkerAdapter,
    model: str,
    *,
    requirements: types.MappingProxyType[str, CapabilityRequirement] = CAPABILITY_REQUIREMENTS,
) -> tuple[CapabilityDecision, ...]:
    capabilities = adapter.capabilities(model)
    return tuple(
        _decide(feature_key, requirement, capabilities)
        for feature_key, requirement in requirements.items()
    )


# WHY: a decision's JSON-ready form, the shape the run record and `remedy worker show` both serialize.
def capability_decision_record(decision: CapabilityDecision) -> dict:
    return {
        "feature_key": decision.feature_key,
        "mode": decision.mode,
        "strategy": decision.strategy,
        "missing": list(decision.missing),
    }


# WHY: the run record's `capability_degradations` evidence — one entry per distinct non-native decision.
def capability_degradation_entries(
    decisions: tuple[CapabilityDecision, ...] | list[CapabilityDecision],
) -> list[dict]:
    entries: list[dict] = []
    seen: set[tuple] = set()
    for decision in decisions:
        if decision.mode == CAPABILITY_MODE_NATIVE:
            continue
        record = capability_decision_record(decision)
        key = (record["feature_key"], record["mode"], record["strategy"], tuple(record["missing"]))
        if key in seen:
            continue
        seen.add(key)
        entries.append(record)
    return entries


# WHY: the run-record key this evidence lives under; never the generic `degraded` other sites use.
CAPABILITY_DEGRADATIONS_FIELD = "capability_degradations"
