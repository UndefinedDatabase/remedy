"""F151 T002: the adapter contract's own promises, one test per promise (DECISION F151 D2)."""
from __future__ import annotations

import dataclasses

import pytest

from packages.contracts.adapter_contract import (
    ADAPTER_ERROR_CLASSES,
    ADAPTER_ROLES,
    STREAM_EVENT_TYPES,
    AdapterCapabilities,
    AdapterUsage,
    CliInvocation,
    HttpInvocation,
    InvocationOptions,
    WorkerAdapter,
)
from packages.orchestration import stream_evidence
from packages.orchestration.failure_postmortem import FailureClass
from packages.orchestration.token_actuals import UsageActuals

_USAGE_ACTUALS = UsageActuals(
    input_tokens=1, output_tokens=1, cache_read=0, cache_creation=0,
    total_cost_usd=None, num_turns=1, duration_ms=1, session_id="s",
)

_FROZEN_INSTANCES = {
    "AdapterCapabilities": AdapterCapabilities(
        vision=False, json_schema=False, session_resume=False,
        streaming=False, tool_use=False, max_context_tokens=0),
    "InvocationOptions": InvocationOptions(model="m"),
    "CliInvocation": CliInvocation(argv=("x",)),
    "HttpInvocation": HttpInvocation(method="GET", url="http://x", body={}),
    "AdapterUsage": AdapterUsage(actuals=_USAGE_ACTUALS, raw_counters={}),
}


@pytest.mark.parametrize("name", sorted(_FROZEN_INSTANCES))
def test_dataclass_is_frozen(name):
    instance = _FROZEN_INSTANCES[name]
    field_name = dataclasses.fields(instance)[0].name
    with pytest.raises(dataclasses.FrozenInstanceError):
        setattr(instance, field_name, getattr(instance, field_name))


def test_invocation_options_carries_no_timeout_field():
    names = [f.name for f in dataclasses.fields(InvocationOptions)]
    assert not any("timeout" in n for n in names), names


def test_stream_event_types_equals_every_event_constant_in_stream_evidence():
    # vars(), not a hand-copied list: a tenth EVENT_* constant must red this test.
    expected = {v for k, v in vars(stream_evidence).items() if k.startswith("EVENT_")}
    assert STREAM_EVENT_TYPES == expected


def test_adapter_error_classes_is_exactly_five_members():
    assert ADAPTER_ERROR_CLASSES == {
        FailureClass.PROVIDER_UNAVAILABLE, FailureClass.PROVIDER_TIMEOUT,
        FailureClass.PROVIDER_NONZERO_EXIT, FailureClass.PARSE, FailureClass.UNKNOWN,
    }


def test_adapter_roles_is_exactly_builder_and_reviewer():
    assert ADAPTER_ROLES == ("builder", "reviewer")


class _ConformingToy:
    """A minimal class with all seven WorkerAdapter members."""

    @property
    def adapter_id(self) -> str:
        return "conforming-toy"

    def capabilities(self, model: str) -> AdapterCapabilities:
        return AdapterCapabilities(
            vision=False, json_schema=False, session_resume=False,
            streaming=False, tool_use=False, max_context_tokens=0)

    def build_invocation(self, role, prompt_parts, options):
        if role not in ADAPTER_ROLES:
            raise ValueError(role)
        return CliInvocation(argv=tuple(prompt_parts))

    def map_stream(self, raw_lines):
        return ()

    def map_usage(self, raw):
        return None

    def classify_error(self, error_text, exit_code):
        return FailureClass.UNKNOWN

    def isolation(self):
        return None


class _MissingMapUsage:
    """Every member of _ConformingToy except map_usage."""

    @property
    def adapter_id(self) -> str:
        return "incomplete-toy"

    def capabilities(self, model: str) -> AdapterCapabilities:
        return AdapterCapabilities(
            vision=False, json_schema=False, session_resume=False,
            streaming=False, tool_use=False, max_context_tokens=0)

    def build_invocation(self, role, prompt_parts, options):
        if role not in ADAPTER_ROLES:
            raise ValueError(role)
        return CliInvocation(argv=tuple(prompt_parts))

    def map_stream(self, raw_lines):
        return ()

    def classify_error(self, error_text, exit_code):
        return FailureClass.UNKNOWN

    def isolation(self):
        return None


def test_class_with_all_seven_members_is_a_worker_adapter():
    assert isinstance(_ConformingToy(), WorkerAdapter)


def test_class_missing_map_usage_is_not_a_worker_adapter():
    assert not isinstance(_MissingMapUsage(), WorkerAdapter)
