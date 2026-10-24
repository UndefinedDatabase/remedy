"""F151 T002: the adapter contract's own promises, one test per promise (DECISION F151 D2)."""
from __future__ import annotations

import dataclasses
import re

import pytest

from packages.contracts.adapter_contract import (
    ADAPTER_ERROR_CLASSES,
    ADAPTER_ROLES,
    ISOLATION_METHODS,
    STREAM_EVENT_TYPES,
    AdapterCapabilities,
    AdapterUsage,
    CliInvocation,
    HttpInvocation,
    InvocationOptions,
    WorkerAdapter,
    WorkerIsolation,
    WorkerSandboxDefault,
)
from packages.orchestration import stream_evidence
from packages.orchestration.failure_postmortem import FailureClass
from packages.orchestration.token_actuals import UsageActuals

_VALID_ADR_REF = "docs/adr/0002-claude-cli-worker-isolation.md"

#: A valid profile's TOML text, shared by every WorkerSandboxDefault this file builds; parsing it
#: is not this file's job (DECISION F162 D4 (1): the contract itself never imports sandbox_profiles).
_VALID_SANDBOX_PROFILE_TOML = (
    'fs_scope = ["{workspace}"]\n'
    'net = "deny"\n'
    'allowed_binaries = "any"\n'
    'tmp_quota_mb = "unlimited"\n'
    "[ulimits]\n"
    'cpu_s = "unlimited"\n'
    'mem_mb = "unlimited"\n'
    'nofile = "unlimited"\n'
)

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
    "WorkerIsolation": WorkerIsolation(
        method="tool_flag", adr_ref=_VALID_ADR_REF, tool_args=("--flag",)),
    "WorkerSandboxDefault": WorkerSandboxDefault(
        profile_toml=_VALID_SANDBOX_PROFILE_TOML, tool_sandbox=True),
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


def test_isolation_methods_is_exactly_the_three_f152_d3_1_names():
    assert ISOLATION_METHODS == ("tool_flag", "clean_env", "sandbox_reinforced")


#: One case per DECISION F152 D3 (1) refusal rule: kwargs that construct a WorkerIsolation
#: starting from a valid base, each overriding exactly the field(s) its own rule refuses.
_ISOLATION_REFUSAL_CASES = (
    ({"method": "bogus", "adr_ref": _VALID_ADR_REF, "tool_args": ("--x",)},
     "unknown isolation method"),
    ({"method": "tool_flag", "adr_ref": "adr/0002-x.md", "tool_args": ("--x",)},
     "adr_ref must match"),
    ({"method": "tool_flag", "adr_ref": "docs/adr/002-x.md", "tool_args": ("--x",)},
     "adr_ref must match"),
    ({"method": "tool_flag", "adr_ref": "docs/adr/0002-X.md", "tool_args": ("--x",)},
     "adr_ref must match"),
    ({"method": "tool_flag", "adr_ref": "docs/adr/0002-x", "tool_args": ("--x",)},
     "adr_ref must match"),
    ({"method": "tool_flag", "adr_ref": _VALID_ADR_REF, "tool_args": "--x"},
     "tool_args must be a tuple of non-empty strings"),
    ({"method": "tool_flag", "adr_ref": _VALID_ADR_REF, "tool_args": ("",)},
     "tool_args must be a tuple of non-empty strings"),
    ({"method": "clean_env", "adr_ref": _VALID_ADR_REF, "env_allowlist": "HOME"},
     "env_allowlist must be a tuple of non-empty strings"),
    ({"method": "clean_env", "adr_ref": _VALID_ADR_REF, "env_allowlist": ("",)},
     "env_allowlist must be a tuple of non-empty strings"),
    ({"method": "tool_flag", "adr_ref": _VALID_ADR_REF},
     "tool_flag requires tool_args"),
    ({"method": "clean_env", "adr_ref": _VALID_ADR_REF},
     "clean_env requires env_allowlist"),
    ({"method": "sandbox_reinforced", "adr_ref": _VALID_ADR_REF},
     "sandbox_reinforced requires env_allowlist"),
    ({"method": "tool_flag", "adr_ref": _VALID_ADR_REF, "tool_args": ("--x",),
      "throwaway_home": True},
     "throwaway_home is not allowed with tool_flag"),
)


@pytest.mark.parametrize(
    ("kwargs", "fragment"), _ISOLATION_REFUSAL_CASES,
    ids=[f"{i}-{frag.split()[0]}" for i, (_k, frag) in enumerate(_ISOLATION_REFUSAL_CASES)])
def test_worker_isolation_refuses_each_d3_1_violation(kwargs, fragment):
    with pytest.raises(ValueError, match=re.escape(fragment)):
        WorkerIsolation(**kwargs)


#: One case per DECISION F162 D4 (1) refusal rule: kwargs that construct a WorkerSandboxDefault
#: starting from a valid base, each overriding exactly the field(s) its own rule refuses.
_SANDBOX_DEFAULT_REFUSAL_CASES = (
    ({"profile_toml": "", "tool_sandbox": True}, "profile_toml must be a non-empty string"),
    ({"profile_toml": 1, "tool_sandbox": True}, "profile_toml must be a non-empty string"),
    ({"profile_toml": _VALID_SANDBOX_PROFILE_TOML, "tool_sandbox": "yes"},
     "tool_sandbox must be a bool"),
    ({"profile_toml": _VALID_SANDBOX_PROFILE_TOML, "tool_sandbox": True, "reason": 1},
     "reason must be a string"),
    ({"profile_toml": _VALID_SANDBOX_PROFILE_TOML, "tool_sandbox": False},
     "tool_sandbox False requires a non-empty reason"),
    ({"profile_toml": _VALID_SANDBOX_PROFILE_TOML, "tool_sandbox": False, "reason": ""},
     "tool_sandbox False requires a non-empty reason"),
)


@pytest.mark.parametrize(
    ("kwargs", "fragment"), _SANDBOX_DEFAULT_REFUSAL_CASES,
    ids=[f"{i}-{frag.split()[0]}" for i, (_k, frag) in enumerate(_SANDBOX_DEFAULT_REFUSAL_CASES)])
def test_worker_sandbox_default_refuses_each_d4_1_violation(kwargs, fragment):
    with pytest.raises(ValueError, match=re.escape(fragment)):
        WorkerSandboxDefault(**kwargs)


class _ConformingToy:
    """A minimal class with all eight WorkerAdapter members."""

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

    def sandbox_default(self):
        return WorkerSandboxDefault(profile_toml=_VALID_SANDBOX_PROFILE_TOML, tool_sandbox=True)


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

    def sandbox_default(self):
        return WorkerSandboxDefault(profile_toml=_VALID_SANDBOX_PROFILE_TOML, tool_sandbox=True)


def test_class_with_all_eight_members_is_a_worker_adapter():
    assert isinstance(_ConformingToy(), WorkerAdapter)


def test_class_missing_map_usage_is_not_a_worker_adapter():
    assert not isinstance(_MissingMapUsage(), WorkerAdapter)
