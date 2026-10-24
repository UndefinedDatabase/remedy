"""Pins DECISION F162 D2: the sandbox profile schema, its three built-ins, and the tighten-only
order's refusal. `packages/orchestration/sandbox_profiles.py`'s own module docstring states what
T001 does NOT yet do — nothing here proves a profile is read by any spawn path.

This half (F162 round 2 C2) pins parsing: the TOML form's refusal rules, one per rule of DECISION
F162 D2 (3), the built-ins' exact values, and normalization. F162 round 2 C3 adds the tighten-only
order's table tests, the preorder properties and the refusal message.
"""
from __future__ import annotations

import dataclasses
import errno
import itertools
import json
import os
import signal
import socket
import sys
import threading

import pytest

import packages.orchestration.sandbox_profiles as SP
from packages.contracts.adapter_contract import WorkerSandboxDefault
from packages.orchestration.exec_guard import ExecGuardPolicy, ExecGuardResult
from packages.orchestration.sandbox_profiles import (
    BUILTIN_SANDBOX_PROFILE_NAMES,
    SANDBOX_ENFORCEMENT_KEYS,
    WORKER_SANDBOX_FILENAME,
    SandboxDimensionEnforcement,
    SandboxLoosening,
    SandboxNet,
    SandboxProfile,
    SandboxProfileError,
    SandboxProfileLoosened,
    SandboxUlimits,
    effective_sandbox_profile,
    get_sandbox_profile,
    load_builtin_sandbox_profiles,
    parse_sandbox_profile,
    profile_loosenings,
    profile_within,
    record_worker_sandbox,
    run_guarded_with_sandbox_profile,
    sandbox_doctor_checks,
    sandbox_profile_config_key,
    sandbox_profile_enforcement,
    sandbox_profile_guard_policy,
    sandbox_runner_available,
    tighten_sandbox_profile,
    worker_sandbox_record,
)
from packages.orchestration.tool_sandbox import SandboxSpec, SandboxUnavailable, require_sandbox
from packages.providers.adapters.claude_cli_reference import ClaudeCliReferenceAdapter

#: A profile that satisfies every rule of DECISION F162 D2 (3); every refusal case below is one
#: line of this text dropped, replaced or added.
_VALID = """\
fs_scope = ["{workspace}"]
net = "deny"
allowed_binaries = "any"
tmp_quota_mb = 10
[ulimits]
cpu_s = 10
mem_mb = 10
nofile = 10
"""


def _drop_line(text: str, prefix: str) -> str:
    """_VALID with the one line starting with prefix removed."""
    return "\n".join(line for line in text.splitlines() if not line.startswith(prefix)) + "\n"


def _replace_line(text: str, prefix: str, new_line: str) -> str:
    """_VALID with the one line starting with prefix replaced verbatim."""
    return "\n".join(new_line if line.startswith(prefix) else line for line in text.splitlines()) + "\n"


def _insert_before(text: str, prefix: str, new_line: str) -> str:
    """_VALID with new_line inserted just before the one line starting with prefix."""
    lines = text.splitlines()
    index = next(i for i, line in enumerate(lines) if line.startswith(prefix))
    lines.insert(index, new_line)
    return "\n".join(lines) + "\n"


def _append_line(text: str, new_line: str) -> str:
    """_VALID with new_line appended as the file's last line, inside the open [ulimits] table."""
    return text.rstrip("\n") + "\n" + new_line + "\n"


_MISSING_ULIMITS = _drop_line(_drop_line(_drop_line(_drop_line(_VALID, "[ulimits]"), "cpu_s"),
                                          "mem_mb"), "nofile")

#: One case per rule of DECISION F162 D2 (3): (id, this profile's TOML text, the key the refusal names).
_REFUSAL_CASES = (
    ("missing_fs_scope", _drop_line(_VALID, "fs_scope"), "fs_scope"),
    ("missing_net", _drop_line(_VALID, "net"), "net"),
    ("missing_allowed_binaries", _drop_line(_VALID, "allowed_binaries"), "allowed_binaries"),
    ("missing_tmp_quota_mb", _drop_line(_VALID, "tmp_quota_mb"), "tmp_quota_mb"),
    ("missing_ulimits", _MISSING_ULIMITS, "ulimits"),
    ("unknown_top_key", _insert_before(_VALID, "[ulimits]", "extra = 1"), "extra"),
    ("ulimits_missing_key", _drop_line(_VALID, "nofile"), "ulimits.nofile"),
    ("ulimits_extra_key", _append_line(_VALID, "other = 1"), "ulimits.other"),
    ("tmp_quota_mb_zero", _replace_line(_VALID, "tmp_quota_mb", "tmp_quota_mb = 0"), "tmp_quota_mb"),
    ("tmp_quota_mb_negative", _replace_line(_VALID, "tmp_quota_mb", "tmp_quota_mb = -1"), "tmp_quota_mb"),
    ("tmp_quota_mb_bool", _replace_line(_VALID, "tmp_quota_mb", "tmp_quota_mb = true"), "tmp_quota_mb"),
    ("tmp_quota_mb_string", _replace_line(_VALID, "tmp_quota_mb", 'tmp_quota_mb = "lots"'), "tmp_quota_mb"),
    ("empty_fs_scope", _replace_line(_VALID, "fs_scope", "fs_scope = []"), "fs_scope"),
    ("fs_scope_dotdot", _replace_line(_VALID, "fs_scope", 'fs_scope = ["{workspace}/../x"]'), "fs_scope"),
    ("fs_scope_relative", _replace_line(_VALID, "fs_scope", 'fs_scope = ["relative/x"]'), "fs_scope"),
    ("fs_scope_workspace_glued", _replace_line(_VALID, "fs_scope", 'fs_scope = ["{workspace}x"]'), "fs_scope"),
    ("fs_scope_double_slash", _replace_line(_VALID, "fs_scope", 'fs_scope = ["/a//b"]'), "fs_scope"),
    ("net_open_string", _replace_line(_VALID, "net", 'net = "open"'), "net"),
    ("net_empty_allow", _replace_line(_VALID, "net", "net = { allow = [] }"), "net"),
    ("net_second_key", _replace_line(_VALID, "net", 'net = { allow = ["a"], extra = 1 }'), "net"),
    ("net_host_with_space", _replace_line(_VALID, "net", 'net = { allow = ["a b"] }'), "net"),
    ("net_host_with_slash", _replace_line(_VALID, "net", 'net = { allow = ["a/b"] }'), "net"),
    ("binary_with_slash", _replace_line(_VALID, "allowed_binaries", 'allowed_binaries = ["bin/sh"]'),
     "allowed_binaries"),
    ("allowed_binaries_all", _replace_line(_VALID, "allowed_binaries", 'allowed_binaries = "all"'),
     "allowed_binaries"),
    ("not_toml", "this is not { valid toml", "<toml>"),
)


@pytest.mark.parametrize("case_id,text,key", _REFUSAL_CASES, ids=[c[0] for c in _REFUSAL_CASES])
def test_each_d2_rule_3_violation_is_refused_naming_the_profile_and_the_key(case_id, text, key):
    with pytest.raises(SandboxProfileError) as excinfo:
        parse_sandbox_profile("x", text)
    message = str(excinfo.value)
    assert "'x'" in message, (case_id, message)
    assert f"'{key}'" in message, (case_id, message)


def test_builtins_load_in_order_and_equal_the_decision_f162_d2_4_literals():
    profiles = load_builtin_sandbox_profiles()
    assert list(profiles) == list(BUILTIN_SANDBOX_PROFILE_NAMES)
    assert profiles["strict"] == SandboxProfile(
        name="strict", fs_scope=("{workspace}",), net=SandboxNet("deny", ()),
        ulimits=SandboxUlimits(cpu_s=600, mem_mb=2048, nofile=256),
        allowed_binaries=("git", "python3", "sh"), tmp_quota_mb=64)
    assert profiles["standard"] == SandboxProfile(
        name="standard", fs_scope=("{workspace}",), net=SandboxNet("deny", ()),
        ulimits=SandboxUlimits(cpu_s=1800, mem_mb=None, nofile=1024),
        allowed_binaries=None, tmp_quota_mb=512)
    assert profiles["net-local"] == SandboxProfile(
        name="net-local", fs_scope=("{workspace}",),
        net=SandboxNet("allowlist", ("127.0.0.1", "::1", "localhost")),
        ulimits=SandboxUlimits(cpu_s=1800, mem_mb=None, nofile=1024),
        allowed_binaries=None, tmp_quota_mb=512)


def test_get_sandbox_profile_returns_each_builtin_and_refuses_an_unknown_name():
    for name in BUILTIN_SANDBOX_PROFILE_NAMES:
        assert get_sandbox_profile(name).name == name
    with pytest.raises(SandboxProfileError) as excinfo:
        get_sandbox_profile("bogus")
    message = str(excinfo.value)
    for name in BUILTIN_SANDBOX_PROFILE_NAMES:
        assert name in message, message


def test_normalization_collapses_duplicates_sorts_and_lowercases_and_squashes_dot_segments():
    text = _replace_line(_VALID, "fs_scope",
                          'fs_scope = ["{workspace}/b", "{workspace}/a/./b", "{workspace}/a/b"]')
    text = _replace_line(text, "net", 'net = { allow = ["B", "a", "A"] }')
    text = _replace_line(text, "allowed_binaries", 'allowed_binaries = ["sh", "git", "git"]')
    profile = parse_sandbox_profile("norm", text)
    assert profile.fs_scope == ("{workspace}/a/b", "{workspace}/b")
    assert profile.net.hosts == ("a", "b")
    assert profile.allowed_binaries == ("git", "sh")


def test_loader_refuses_a_folder_missing_a_builtin_file(tmp_path):
    (tmp_path / "strict.toml").write_text(_VALID, encoding="utf-8")
    (tmp_path / "standard.toml").write_text(_VALID, encoding="utf-8")
    with pytest.raises(SandboxProfileError) as excinfo:
        load_builtin_sandbox_profiles(tmp_path)
    assert "net-local" in str(excinfo.value)


def test_loader_refuses_a_folder_holding_an_extra_toml_file(tmp_path):
    for name in BUILTIN_SANDBOX_PROFILE_NAMES:
        (tmp_path / f"{name}.toml").write_text(_VALID, encoding="utf-8")
    (tmp_path / "stray.toml").write_text(_VALID, encoding="utf-8")
    with pytest.raises(SandboxProfileError) as excinfo:
        load_builtin_sandbox_profiles(tmp_path)
    assert "stray" in str(excinfo.value)


# ---------------------------------------------------------------------------
# F162 round 2 C3: the tighten-only order's table tests and its refusal.
# ---------------------------------------------------------------------------

#: A neutral fixture profile; each dimension table below varies exactly one field off this base.
_BASE = SandboxProfile(
    name="base", fs_scope=("{workspace}",), net=SandboxNet("deny", ()),
    ulimits=SandboxUlimits(cpu_s=10, mem_mb=10, nofile=10),
    allowed_binaries=("git",), tmp_quota_mb=10,
)

_BUILTINS = load_builtin_sandbox_profiles()

#: Reflexivity and transitivity are checked over this set: every built-in plus two fixtures whose
#: fs_scope relationship is not already covered between the built-ins alone.
_PREORDER_FIXTURES = (
    *_BUILTINS.values(), _BASE,
    dataclasses.replace(_BASE, name="base-sub", fs_scope=("{workspace}/sub",)),
)

_FS_SCOPE_CASES = (
    ("equal", ("{workspace}",), ("{workspace}",), True),
    ("below", ("{workspace}",), ("{workspace}/sub",), True),
    ("sibling", ("{workspace}/a",), ("{workspace}/b",), False),
    ("workspace_vs_absolute", ("{workspace}",), ("/abs",), False),
    ("absolute_vs_workspace", ("/abs",), ("{workspace}",), False),
    ("one_entry_outside", ("{workspace}",), ("{workspace}/sub", "/outside"), False),
)


@pytest.mark.parametrize("case_id,minimum_scope,candidate_scope,within", _FS_SCOPE_CASES,
                         ids=[c[0] for c in _FS_SCOPE_CASES])
def test_fs_scope_order_matches_decision_f162_d2_5(case_id, minimum_scope, candidate_scope, within):
    minimum = dataclasses.replace(_BASE, fs_scope=minimum_scope)
    candidate = dataclasses.replace(_BASE, fs_scope=candidate_scope)
    assert profile_within(candidate, minimum) is within, case_id


_NET_CASES = (
    ("deny_within_deny", SandboxNet("deny", ()), SandboxNet("deny", ()), True),
    ("deny_within_allowlist", SandboxNet("allowlist", ("a",)), SandboxNet("deny", ()), True),
    ("allowlist_not_within_deny", SandboxNet("deny", ()), SandboxNet("allowlist", ("a",)), False),
    ("subset", SandboxNet("allowlist", ("a", "b")), SandboxNet("allowlist", ("a",)), True),
    ("superset", SandboxNet("allowlist", ("a",)), SandboxNet("allowlist", ("a", "b")), False),
)


@pytest.mark.parametrize("case_id,minimum_net,candidate_net,within", _NET_CASES,
                         ids=[c[0] for c in _NET_CASES])
def test_net_order_matches_decision_f162_d2_5(case_id, minimum_net, candidate_net, within):
    minimum = dataclasses.replace(_BASE, net=minimum_net)
    candidate = dataclasses.replace(_BASE, net=candidate_net)
    assert profile_within(candidate, minimum) is within, case_id


#: Shared by a ulimits key and tmp_quota_mb: both compare under the same int-or-None rule.
_INT_CASES = (
    ("smaller", 10, 5, True),
    ("equal", 10, 10, True),
    ("larger", 10, 20, False),
    ("integer_within_unlimited", None, 10, True),
    ("unlimited_not_within_integer", 10, None, False),
)


@pytest.mark.parametrize("case_id,minimum_value,candidate_value,within", _INT_CASES,
                         ids=[c[0] for c in _INT_CASES])
def test_a_ulimits_key_order_matches_decision_f162_d2_5(case_id, minimum_value, candidate_value, within):
    minimum = dataclasses.replace(_BASE, ulimits=dataclasses.replace(_BASE.ulimits, cpu_s=minimum_value))
    candidate = dataclasses.replace(_BASE, ulimits=dataclasses.replace(_BASE.ulimits, cpu_s=candidate_value))
    assert profile_within(candidate, minimum) is within, case_id


@pytest.mark.parametrize("case_id,minimum_value,candidate_value,within", _INT_CASES,
                         ids=[c[0] for c in _INT_CASES])
def test_tmp_quota_mb_order_matches_decision_f162_d2_5(case_id, minimum_value, candidate_value, within):
    minimum = dataclasses.replace(_BASE, tmp_quota_mb=minimum_value)
    candidate = dataclasses.replace(_BASE, tmp_quota_mb=candidate_value)
    assert profile_within(candidate, minimum) is within, case_id


_BINARIES_CASES = (
    ("subset", ("a", "b"), ("a",), True),
    ("superset", ("a",), ("a", "b"), False),
    ("tuple_within_any", None, ("a",), True),
    ("any_not_within_tuple", ("a",), None, False),
)


@pytest.mark.parametrize("case_id,minimum_binaries,candidate_binaries,within", _BINARIES_CASES,
                         ids=[c[0] for c in _BINARIES_CASES])
def test_allowed_binaries_order_matches_decision_f162_d2_5(case_id, minimum_binaries, candidate_binaries,
                                                           within):
    minimum = dataclasses.replace(_BASE, allowed_binaries=minimum_binaries)
    candidate = dataclasses.replace(_BASE, allowed_binaries=candidate_binaries)
    assert profile_within(candidate, minimum) is within, case_id


def test_profile_loosenings_standard_against_strict_is_exactly_five_in_order():
    loosenings = profile_loosenings(_BUILTINS["standard"], _BUILTINS["strict"])
    assert loosenings == (
        SandboxLoosening("ulimits.cpu_s", "600", "1800"),
        SandboxLoosening("ulimits.mem_mb", "2048", "unlimited"),
        SandboxLoosening("ulimits.nofile", "256", "1024"),
        SandboxLoosening("allowed_binaries", '["git", "python3", "sh"]', "any"),
        SandboxLoosening("tmp_quota_mb", "64", "512"),
    )


def test_profile_loosenings_net_local_against_standard_is_exactly_one_net_loosening():
    loosenings = profile_loosenings(_BUILTINS["net-local"], _BUILTINS["standard"])
    assert loosenings == (
        SandboxLoosening("net", "deny", '{ allow = ["127.0.0.1", "::1", "localhost"] }'),
    )


def test_strict_is_within_standard_and_net_local_and_standard_is_within_net_local():
    assert profile_within(_BUILTINS["strict"], _BUILTINS["standard"])
    assert profile_within(_BUILTINS["strict"], _BUILTINS["net-local"])
    assert profile_within(_BUILTINS["standard"], _BUILTINS["net-local"])


def test_the_order_is_reflexive_over_every_builtin_and_fixture_profile():
    for profile in _PREORDER_FIXTURES:
        assert profile_within(profile, profile), profile.name


def test_the_order_is_transitive_over_every_triple_of_builtin_and_fixture_profiles():
    for a, b, c in itertools.product(_PREORDER_FIXTURES, repeat=3):
        if profile_within(a, b) and profile_within(b, c):
            assert profile_within(a, c), (a.name, b.name, c.name)


def test_two_differently_named_equal_valued_profiles_are_within_each_other_both_ways():
    standard = _BUILTINS["standard"]
    twin = dataclasses.replace(standard, name="standard-twin")
    assert profile_within(standard, twin)
    assert profile_within(twin, standard)


def test_tighten_sandbox_profile_returns_the_requested_object_when_within():
    minimum = _BUILTINS["standard"]
    requested = _BUILTINS["strict"]
    assert tighten_sandbox_profile(minimum, requested) is requested


def test_tighten_sandbox_profile_refuses_a_loosening_naming_the_minimum_and_every_loosening():
    minimum = _BUILTINS["strict"]
    requested = _BUILTINS["standard"]
    with pytest.raises(SandboxProfileLoosened) as excinfo:
        tighten_sandbox_profile(minimum, requested)
    error = excinfo.value
    assert str(error) == (
        "sandbox profile 'standard' loosens the minimum 'strict': "
        "ulimits.cpu_s 600 -> 1800; ulimits.mem_mb 2048 -> unlimited; "
        "ulimits.nofile 256 -> 1024; "
        'allowed_binaries ["git", "python3", "sh"] -> any; '
        "tmp_quota_mb 64 -> 512"
    )
    assert error.minimum_name == "strict"
    assert error.loosenings == (
        SandboxLoosening("ulimits.cpu_s", "600", "1800"),
        SandboxLoosening("ulimits.mem_mb", "2048", "unlimited"),
        SandboxLoosening("ulimits.nofile", "256", "1024"),
        SandboxLoosening("allowed_binaries", '["git", "python3", "sh"]', "any"),
        SandboxLoosening("tmp_quota_mb", "64", "512"),
    )


# ---------------------------------------------------------------------------
# F162 round 3 C3: the compiler, the runner, the per-platform enforcement record.
# ---------------------------------------------------------------------------

def test_compiler_strict_on_a_default_base_gives_the_tight_limits_and_no_shared_network(tmp_path):
    policy = sandbox_profile_guard_policy(get_sandbox_profile("strict"), workspace=str(tmp_path))
    assert policy.cpu_seconds == 600
    assert policy.address_space_bytes == 2048 * 1048576
    assert policy.open_files == 256
    assert policy.deny_network is True
    assert policy.sandbox.workspace == str(tmp_path)
    assert policy.sandbox.share_network is False


def test_compiler_net_local_shares_the_network_and_does_not_deny_it(tmp_path):
    policy = sandbox_profile_guard_policy(get_sandbox_profile("net-local"), workspace=str(tmp_path))
    assert policy.sandbox.share_network is True
    assert policy.deny_network is False


def test_compiler_never_loosens_a_base_cpu_seconds_tighter_than_the_profile(tmp_path):
    base = ExecGuardPolicy(cpu_seconds=5)
    policy = sandbox_profile_guard_policy(get_sandbox_profile("strict"), workspace=str(tmp_path),
                                           base=base)
    assert policy.cpu_seconds == 5


def test_compiler_never_loosens_a_base_that_already_denies_the_network(tmp_path):
    base = ExecGuardPolicy(deny_network=True)
    policy = sandbox_profile_guard_policy(get_sandbox_profile("net-local"), workspace=str(tmp_path),
                                           base=base)
    assert policy.deny_network is True


def test_compiler_keeps_a_bases_mount_and_leaves_share_network_false_under_net_local(tmp_path):
    mount = (str(tmp_path / "extra"), "/run/remedy/extra", False)
    base = ExecGuardPolicy(sandbox=SandboxSpec(workspace=str(tmp_path), mounts=(mount,)))
    policy = sandbox_profile_guard_policy(get_sandbox_profile("net-local"), workspace=str(tmp_path),
                                           base=base)
    assert policy.sandbox.mounts == (mount,)
    assert policy.sandbox.share_network is False


def test_compiler_standard_leaves_address_space_bytes_none(tmp_path):
    policy = sandbox_profile_guard_policy(get_sandbox_profile("standard"), workspace=str(tmp_path))
    assert policy.address_space_bytes is None


# ---------------------------------------------------------------------------
# F162 round 5 C3: the compiler's tool_sandbox keyword (DECISION F162 D5 (1)).
# ---------------------------------------------------------------------------

def test_compiler_tool_sandbox_false_keeps_a_base_without_a_sandbox_without_one(tmp_path):
    policy = sandbox_profile_guard_policy(
        get_sandbox_profile("strict"), workspace=str(tmp_path), tool_sandbox=False)
    assert policy.sandbox is None


def test_compiler_tool_sandbox_false_keeps_a_bases_own_sandbox_unchanged(tmp_path):
    spec = SandboxSpec(workspace=str(tmp_path), share_network=True)
    base = ExecGuardPolicy(sandbox=spec)
    policy = sandbox_profile_guard_policy(
        get_sandbox_profile("strict"), workspace=str(tmp_path), base=base, tool_sandbox=False)
    assert policy.sandbox is spec


def test_compiler_tool_sandbox_false_still_sets_deny_network_for_a_deny_profile(tmp_path):
    policy = sandbox_profile_guard_policy(
        get_sandbox_profile("strict"), workspace=str(tmp_path), tool_sandbox=False)
    assert policy.deny_network is True


def _stub_exec_guard_result(returncode: int, tripped_limit: str | None = None,
                             classification: str = "failed") -> ExecGuardResult:
    return ExecGuardResult(
        returncode=returncode, term_signal=None, stdout=b"", stderr=b"", stdout_truncated=False,
        stderr_truncated=False, stdout_bytes_seen=0, stderr_bytes_seen=0, streams_complete=True,
        wall_seconds=0.0, cpu_seconds_used=0.0, classification=classification,
        tripped_limit=tripped_limit, limits_enforced=(), limits_unsupported=())


def test_the_runner_attributes_a_sandboxed_cpu_trip_with_no_tripped_limit_and_152(tmp_path, monkeypatch):
    profile = get_sandbox_profile("strict")
    cpu_result = _stub_exec_guard_result(128 + signal.SIGXCPU)
    monkeypatch.setattr(SP, "run_guarded", lambda argv, policy: cpu_result)
    attributed = run_guarded_with_sandbox_profile(["x"], profile, workspace=str(tmp_path))
    assert attributed is not cpu_result
    assert attributed.classification == "resource_limit"
    assert attributed.tripped_limit == "cpu_seconds"


def test_the_runner_leaves_a_result_unchanged_without_a_cpu_limit(tmp_path, monkeypatch):
    no_cpu_profile = dataclasses.replace(
        get_sandbox_profile("strict"), ulimits=dataclasses.replace(
            get_sandbox_profile("strict").ulimits, cpu_s=None))
    cpu_result = _stub_exec_guard_result(128 + signal.SIGXCPU)
    monkeypatch.setattr(SP, "run_guarded", lambda argv, policy: cpu_result)
    unchanged = run_guarded_with_sandbox_profile(["x"], no_cpu_profile, workspace=str(tmp_path))
    assert unchanged is cpu_result


def test_the_runner_leaves_a_result_unchanged_with_a_plain_returncode_1(tmp_path, monkeypatch):
    profile = get_sandbox_profile("strict")
    failed_result = _stub_exec_guard_result(1)
    monkeypatch.setattr(SP, "run_guarded", lambda argv, policy: failed_result)
    unchanged = run_guarded_with_sandbox_profile(["x"], profile, workspace=str(tmp_path))
    assert unchanged is failed_result


def test_the_runner_leaves_a_result_unchanged_when_a_tripped_limit_is_already_set(tmp_path, monkeypatch):
    profile = get_sandbox_profile("strict")
    already_tripped = _stub_exec_guard_result(128 + signal.SIGXCPU, tripped_limit="wall_timeout")
    monkeypatch.setattr(SP, "run_guarded", lambda argv, policy: already_tripped)
    unchanged = run_guarded_with_sandbox_profile(["x"], profile, workspace=str(tmp_path))
    assert unchanged is already_tripped


def test_sandbox_runner_available_answers_false_on_unavailable_and_true_on_a_path(monkeypatch):
    def _raise() -> str:
        raise SandboxUnavailable("missing_prerequisite", "no bwrap", "install it")

    monkeypatch.setattr(SP, "require_sandbox", _raise)
    assert sandbox_runner_available() is False
    monkeypatch.setattr(SP, "require_sandbox", lambda: "/usr/bin/bwrap")
    assert sandbox_runner_available() is True


#: One (key, state) row per built-in and platform combination of DECISION F162 D3 (4).
_ENFORCEMENT_TABLE_CASES = (
    ("strict", "linux", True, (
        ("fs_scope", "enforced"), ("net", "enforced"), ("ulimits.cpu_s", "enforced"),
        ("ulimits.mem_mb", "enforced"), ("ulimits.nofile", "enforced"),
        ("allowed_binaries", "unenforced"), ("tmp_quota_mb", "unenforced"),
    )),
    ("strict", "linux", False, (
        ("fs_scope", "unenforced"), ("net", "unenforced"), ("ulimits.cpu_s", "enforced"),
        ("ulimits.mem_mb", "enforced"), ("ulimits.nofile", "enforced"),
        ("allowed_binaries", "unenforced"), ("tmp_quota_mb", "unenforced"),
    )),
    ("strict", "darwin", False, (
        ("fs_scope", "unenforced"), ("net", "unenforced"), ("ulimits.cpu_s", "unenforced"),
        ("ulimits.mem_mb", "unenforced"), ("ulimits.nofile", "unenforced"),
        ("allowed_binaries", "unenforced"), ("tmp_quota_mb", "unenforced"),
    )),
    ("strict", "win32", False, (
        ("fs_scope", "unenforced"), ("net", "unenforced"), ("ulimits.cpu_s", "unenforced"),
        ("ulimits.mem_mb", "unenforced"), ("ulimits.nofile", "unenforced"),
        ("allowed_binaries", "unenforced"), ("tmp_quota_mb", "unenforced"),
    )),
    ("standard", "linux", True, (
        ("fs_scope", "enforced"), ("net", "enforced"), ("ulimits.cpu_s", "enforced"),
        ("ulimits.mem_mb", "enforced"), ("ulimits.nofile", "enforced"),
        ("allowed_binaries", "enforced"), ("tmp_quota_mb", "unenforced"),
    )),
    ("standard", "linux", False, (
        ("fs_scope", "unenforced"), ("net", "unenforced"), ("ulimits.cpu_s", "enforced"),
        ("ulimits.mem_mb", "enforced"), ("ulimits.nofile", "enforced"),
        ("allowed_binaries", "enforced"), ("tmp_quota_mb", "unenforced"),
    )),
    ("standard", "darwin", False, (
        ("fs_scope", "unenforced"), ("net", "unenforced"), ("ulimits.cpu_s", "unenforced"),
        ("ulimits.mem_mb", "enforced"), ("ulimits.nofile", "unenforced"),
        ("allowed_binaries", "enforced"), ("tmp_quota_mb", "unenforced"),
    )),
    ("net-local", "linux", True, (
        ("fs_scope", "enforced"), ("net", "unenforced"), ("ulimits.cpu_s", "enforced"),
        ("ulimits.mem_mb", "enforced"), ("ulimits.nofile", "enforced"),
        ("allowed_binaries", "enforced"), ("tmp_quota_mb", "unenforced"),
    )),
    ("net-local", "linux", False, (
        ("fs_scope", "unenforced"), ("net", "unenforced"), ("ulimits.cpu_s", "enforced"),
        ("ulimits.mem_mb", "enforced"), ("ulimits.nofile", "enforced"),
        ("allowed_binaries", "enforced"), ("tmp_quota_mb", "unenforced"),
    )),
    ("net-local", "darwin", False, (
        ("fs_scope", "unenforced"), ("net", "unenforced"), ("ulimits.cpu_s", "unenforced"),
        ("ulimits.mem_mb", "enforced"), ("ulimits.nofile", "unenforced"),
        ("allowed_binaries", "enforced"), ("tmp_quota_mb", "unenforced"),
    )),
)


@pytest.mark.parametrize(
    "profile_name,platform,sandbox_available,expected", _ENFORCEMENT_TABLE_CASES,
    ids=[f"{c[0]}-{c[1]}-{c[2]}" for c in _ENFORCEMENT_TABLE_CASES])
def test_sandbox_profile_enforcement_key_state_table(profile_name, platform, sandbox_available,
                                                       expected):
    profile = get_sandbox_profile(profile_name)
    record = sandbox_profile_enforcement(profile, platform=platform,
                                          sandbox_available=sandbox_available)
    assert tuple(e.key for e in record) == SANDBOX_ENFORCEMENT_KEYS
    assert tuple((e.key, e.state) for e in record) == expected


def test_sandbox_profile_enforcement_full_tuple_for_strict_sandboxed_linux():
    record = sandbox_profile_enforcement(get_sandbox_profile("strict"), platform="linux",
                                          sandbox_available=True)
    assert record == (
        SandboxDimensionEnforcement(
            "fs_scope", "enforced", "the tool sandbox makes the workspace the one writable tree"),
        SandboxDimensionEnforcement(
            "net", "enforced", "a private network namespace with its own loopback only"),
        SandboxDimensionEnforcement("ulimits.cpu_s", "enforced", "RLIMIT_CPU on the process tree"),
        SandboxDimensionEnforcement("ulimits.mem_mb", "enforced", "RLIMIT_AS on the process tree"),
        SandboxDimensionEnforcement("ulimits.nofile", "enforced", "RLIMIT_NOFILE on the process tree"),
        SandboxDimensionEnforcement(
            "allowed_binaries", "unenforced", "binaries are not filtered by name"),
        SandboxDimensionEnforcement(
            "tmp_quota_mb", "unenforced", "the private /tmp has no size limit"),
    )


def test_sandbox_profile_enforcement_full_tuple_for_net_local_unsandboxed_linux():
    record = sandbox_profile_enforcement(get_sandbox_profile("net-local"), platform="linux",
                                          sandbox_available=False)
    assert record == (
        SandboxDimensionEnforcement(
            "fs_scope", "unenforced", "no tool sandbox: only the working directory is pinned"),
        SandboxDimensionEnforcement(
            "net", "unenforced", "the host network is shared and hosts are not filtered"),
        SandboxDimensionEnforcement("ulimits.cpu_s", "enforced", "RLIMIT_CPU on the process tree"),
        SandboxDimensionEnforcement("ulimits.mem_mb", "enforced", "nothing to limit"),
        SandboxDimensionEnforcement("ulimits.nofile", "enforced", "RLIMIT_NOFILE on the process tree"),
        SandboxDimensionEnforcement("allowed_binaries", "enforced", "nothing to limit"),
        SandboxDimensionEnforcement(
            "tmp_quota_mb", "unenforced", "no tool sandbox: /tmp is the host's"),
    )


def test_sandbox_profile_enforcement_names_wider_than_declared_scope_for_a_sub_scope():
    profile = dataclasses.replace(get_sandbox_profile("strict"), fs_scope=("{workspace}/sub",))
    record = sandbox_profile_enforcement(profile, platform="linux", sandbox_available=True)
    assert record[0] == SandboxDimensionEnforcement(
        "fs_scope", "unenforced",
        "the tool sandbox keeps the whole workspace writable, wider than the declared scope")


# ---------------------------------------------------------------------------
# F162 round 3 C4: fixture processes prove each limit under the real sandbox.
# F162 round 7 C3: these scripts and markers are the ones test_sandbox_container.py shares.
# ---------------------------------------------------------------------------

#: The net fixture's script (one `{port}` placeholder) and its two markers.
NET_FIXTURE_SCRIPT = (
    "import socket\n"
    "try:\n"
    "    socket.create_connection(('127.0.0.1', {port}), timeout=5).close()\n"
    "    print('NET_REACHED')\n"
    "except OSError:\n"
    "    print('NET_REFUSED')\n"
)
NET_REACHED_MARKER = b"NET_REACHED"
NET_REFUSED_MARKER = b"NET_REFUSED"

#: The fs-scope fixture's script (one `{outside}` placeholder) and its marker.
FS_SCOPE_FIXTURE_SCRIPT = (
    "with open('inside.txt', 'w') as f:\n"
    "    f.write('x')\n"
    "print('FS_INSIDE_DONE')\n"
    "try:\n"
    "    open({outside!r}, 'w').write('x')\n"
    "    print('FS_OUTSIDE_DONE')\n"
    "except OSError:\n"
    "    print('FS_OUTSIDE_REFUSED')\n"
)
FS_INSIDE_DONE_MARKER = b"FS_INSIDE_DONE"

#: The CPU fixture's script (no placeholder) and its markers.
CPU_FIXTURE_SCRIPT = (
    "print('CPU_STARTED', flush=True)\n"
    "x = 0\n"
    "while True:\n"
    "    x += 1\n"
    "print('CPU_LOOP_DONE')\n"
)
CPU_STARTED_MARKER = b"CPU_STARTED"
CPU_LOOP_DONE_MARKER = b"CPU_LOOP_DONE"

#: The nofile fixture's script (no placeholder) and its marker's text prefix.
NOFILE_FIXTURE_SCRIPT = (
    "handles = []\n"
    "err = None\n"
    "try:\n"
    "    for _ in range(64):\n"
    "        handles.append(open('/dev/null'))\n"
    "except OSError as exc:\n"
    "    err = exc.errno\n"
    "print('NOFILE_ERRNO', err)\n"
)
NOFILE_ERRNO_PREFIX = "NOFILE_ERRNO"

#: The memory fixture's process-runner script (no placeholder) and its markers; the container
#: runner's own memory fixture uses a DIFFERENT script (DECISION F162 D7 (5)), defined beside it.
MEM_FIXTURE_SCRIPT = (
    "try:\n"
    "    bytearray(1 << 30)\n"
    "    print('MEM_BIG_ALLOCATED')\n"
    "except MemoryError:\n"
    "    print('MEM_BIG_REFUSED')\n"
    "small = bytearray(1 << 26)\n"
    "print('MEM_SMALL_ALLOCATED', len(small))\n"
)
MEM_BIG_REFUSED_MARKER = b"MEM_BIG_REFUSED"
MEM_SMALL_ALLOCATED_MARKER = b"MEM_SMALL_ALLOCATED"


@pytest.fixture
def sandbox_ready():
    try:
        require_sandbox()
    except SandboxUnavailable as exc:
        pytest.skip(f"NOT VERIFIED: the tool sandbox cannot run here ({exc.state}: {exc.message}); "
                    "a skipped isolation test is not a passed one")


def _fixture_base(workspace: str) -> ExecGuardPolicy:
    """The policy every fixture process runs under: a real interpreter, a bounded wall clock."""
    path_dir = os.path.dirname(sys.executable)
    return ExecGuardPolicy(wall_timeout_seconds=60, cwd=workspace,
                            env={"PATH": f"{path_dir}:/usr/bin:/bin", "LANG": "C.UTF-8"})


def _run_fixture_script(profile: SandboxProfile, script: str, workspace: str) -> ExecGuardResult:
    """One real process, under *profile*, through the production runner."""
    return run_guarded_with_sandbox_profile(
        [sys.executable, "-I", "-c", script], profile, workspace=workspace,
        base=_fixture_base(workspace))


def test_a_deny_profile_cannot_reach_the_host_loopback_and_net_local_can(tmp_path, sandbox_ready):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(("127.0.0.1", 0))
    listener.listen(1)
    port = listener.getsockname()[1]

    def _accept_forever() -> None:
        while True:
            try:
                conn, _addr = listener.accept()
            except OSError:
                return
            conn.close()

    threading.Thread(target=_accept_forever, daemon=True).start()
    try:
        script = NET_FIXTURE_SCRIPT.format(port=port)
        deny_ws = tmp_path / "deny-ws"
        deny_ws.mkdir()
        deny_result = _run_fixture_script(get_sandbox_profile("strict"), script, str(deny_ws))
        assert NET_REFUSED_MARKER in deny_result.stdout

        allow_ws = tmp_path / "allow-ws"
        allow_ws.mkdir()
        allow_result = _run_fixture_script(get_sandbox_profile("net-local"), script, str(allow_ws))
        assert NET_REACHED_MARKER in allow_result.stdout
    finally:
        listener.close()


def test_strict_pins_the_workspace_as_the_one_writable_tree(tmp_path, sandbox_ready):
    ws = tmp_path / "ws"
    ws.mkdir()
    outside = tmp_path / "outside.txt"
    script = FS_SCOPE_FIXTURE_SCRIPT.format(outside=str(outside))
    result = _run_fixture_script(get_sandbox_profile("strict"), script, str(ws))
    assert FS_INSIDE_DONE_MARKER in result.stdout
    assert (ws / "inside.txt").exists()
    assert not outside.exists()


def test_a_one_second_cpu_limit_ends_a_busy_loop_classified_resource_limit_cpu_seconds(
        tmp_path, sandbox_ready):
    ws = tmp_path / "ws"
    ws.mkdir()
    strict = get_sandbox_profile("strict")
    profile = dataclasses.replace(strict, ulimits=dataclasses.replace(strict.ulimits, cpu_s=1))
    result = _run_fixture_script(profile, CPU_FIXTURE_SCRIPT, str(ws))
    assert CPU_STARTED_MARKER in result.stdout
    assert CPU_LOOP_DONE_MARKER not in result.stdout
    assert result.classification == "resource_limit"
    assert result.tripped_limit == "cpu_seconds"


def test_a_nofile_limit_of_16_refuses_the_64th_open_of_dev_null_with_errno_24(tmp_path, sandbox_ready):
    ws = tmp_path / "ws"
    ws.mkdir()
    strict = get_sandbox_profile("strict")
    profile = dataclasses.replace(strict, ulimits=dataclasses.replace(strict.ulimits, nofile=16))
    result = _run_fixture_script(profile, NOFILE_FIXTURE_SCRIPT, str(ws))
    assert f"{NOFILE_ERRNO_PREFIX} {errno.EMFILE}".encode() in result.stdout


def test_a_mem_limit_of_256_mib_refuses_1gib_and_allows_64mib(tmp_path, sandbox_ready):
    ws = tmp_path / "ws"
    ws.mkdir()
    strict = get_sandbox_profile("strict")
    profile = dataclasses.replace(strict, ulimits=dataclasses.replace(strict.ulimits, mem_mb=256))
    result = _run_fixture_script(profile, MEM_FIXTURE_SCRIPT, str(ws))
    assert MEM_BIG_REFUSED_MARKER in result.stdout
    assert MEM_SMALL_ALLOCATED_MARKER in result.stdout


# ---------------------------------------------------------------------------
# F162 round 5 C3: the sandbox evidence, beside worker_isolation.jsonl (DECISION F162 D5 (4)).
# ---------------------------------------------------------------------------

def test_worker_sandbox_record_net_local_sandboxed_linux_matches_the_dict_literal():
    record = worker_sandbox_record(
        get_sandbox_profile("net-local"), tool_sandbox=True, platform="linux",
        sandbox_available=True)
    assert record == {
        "profile": "net-local",
        "runner": "process",
        "tool_sandbox": True,
        "dimensions": {
            "fs_scope": "enforced", "net": "unenforced", "ulimits.cpu_s": "enforced",
            "ulimits.mem_mb": "enforced", "ulimits.nofile": "enforced",
            "allowed_binaries": "enforced", "tmp_quota_mb": "unenforced",
        },
        "reasons": {
            "fs_scope": "the tool sandbox makes the workspace the one writable tree",
            "net": "the host network is shared and hosts are not filtered",
            "ulimits.cpu_s": "RLIMIT_CPU on the process tree",
            "ulimits.mem_mb": "nothing to limit",
            "ulimits.nofile": "RLIMIT_NOFILE on the process tree",
            "allowed_binaries": "nothing to limit",
            "tmp_quota_mb": "the private /tmp has no size limit",
        },
    }


class TestRecordWorkerSandbox:
    def test_writes_nothing_for_a_falsy_directory(self, tmp_path, monkeypatch):
        # R-1466: a stray write for a falsy directory would land relative to the working
        # directory, so the working directory is set to tmp_path before either call.
        monkeypatch.chdir(tmp_path)
        record = worker_sandbox_record(
            get_sandbox_profile("net-local"), tool_sandbox=True, platform="linux",
            sandbox_available=True)
        record_worker_sandbox(None, role="builder", provider="claude-cli", model="m", record=record)
        record_worker_sandbox("", role="builder", provider="claude-cli", model="m", record=record)
        assert list(tmp_path.iterdir()) == []

    def test_appends_one_sorted_key_line_per_call(self, tmp_path):
        record = worker_sandbox_record(
            get_sandbox_profile("net-local"), tool_sandbox=True, platform="linux",
            sandbox_available=True)
        record_worker_sandbox(
            str(tmp_path), role="builder", provider="claude-cli", model="m", record=record)
        record_worker_sandbox(
            str(tmp_path), role="reviewer", provider="claude-cli", model="m", record=record)
        lines = (tmp_path / WORKER_SANDBOX_FILENAME).read_text(encoding="utf-8").splitlines()
        assert len(lines) == 2
        assert all(line == json.dumps(json.loads(line), sort_keys=True) for line in lines)
        parsed = [json.loads(line) for line in lines]
        assert [p["role"] for p in parsed] == ["builder", "reviewer"]
        assert all(p["provider"] == "claude-cli" and p["model"] == "m" for p in parsed)


# ---------------------------------------------------------------------------
# F162 round 6 C3: a project's chosen profile, tightened against the adapter's own default
# (DECISION F162 D6)
# ---------------------------------------------------------------------------


class _Config(dict):
    """A stand-in for `RemedyConfig`: `get` answers the value a key was given, else None."""


def test_sandbox_profile_config_key_turns_the_dash_into_an_underscore():
    assert sandbox_profile_config_key("claude-cli") == "claude_cli.sandbox_profile"


class TestEffectiveSandboxProfile:
    """DECISION F162 D6 (2): the resolver never reaches a call looser than the adapter's own
    default, which is the policy minimum."""

    def _adapter(self) -> ClaudeCliReferenceAdapter:
        return ClaudeCliReferenceAdapter()

    @pytest.mark.parametrize("value", [None, "", "   "])
    def test_an_unset_or_blank_value_answers_the_adapters_own_default(self, value):
        profile = effective_sandbox_profile(
            self._adapter(), config=_Config({"claude_cli.sandbox_profile": value}))
        assert profile.name == "claude-cli"
        assert profile.net == SandboxNet(mode="allowlist", hosts=("api.anthropic.com",))

    def test_a_stricter_builtin_tightens_the_default_and_is_returned_by_its_own_name(self):
        profile = effective_sandbox_profile(
            self._adapter(), config=_Config({"claude_cli.sandbox_profile": "strict"}))
        assert profile == get_sandbox_profile("strict")

    def test_net_local_loosens_net_and_is_refused_naming_the_default(self):
        with pytest.raises(SandboxProfileLoosened) as exc_info:
            effective_sandbox_profile(
                self._adapter(), config=_Config({"claude_cli.sandbox_profile": "net-local"}))
        assert exc_info.value.minimum_name == "claude-cli"
        assert "'claude-cli'" in str(exc_info.value)

    def test_an_unknown_name_is_refused_naming_the_three_builtins(self):
        with pytest.raises(SandboxProfileError, match="strict, standard, net-local"):
            effective_sandbox_profile(
                self._adapter(), config=_Config({"claude_cli.sandbox_profile": "bogus"}))

    def test_with_no_config_it_reads_the_process_config(self, monkeypatch):
        import packages.orchestration.config as config_module

        monkeypatch.setattr(
            config_module, "get_config",
            lambda: _Config({"claude_cli.sandbox_profile": "strict"}))
        assert effective_sandbox_profile(self._adapter()) == get_sandbox_profile("strict")


# ---------------------------------------------------------------------------
# F162 round 6 C4: worker doctor names each worker's sandbox profile and its
# unenforced dimensions (DECISION F162 D6 (4))
# ---------------------------------------------------------------------------


class _EveryDimensionEnforcedDouble(ClaudeCliReferenceAdapter):
    """`standard`'s own values, `tmp_quota_mb` changed to unlimited, `tool_sandbox` True: with
    `sandbox_runner_available` also answering True, nothing here is left unenforced."""

    def sandbox_default(self) -> WorkerSandboxDefault:
        return WorkerSandboxDefault(
            profile_toml=(
                'fs_scope = ["{workspace}"]\n'
                'net = "deny"\n'
                'allowed_binaries = "any"\n'
                'tmp_quota_mb = "unlimited"\n'
                "[ulimits]\n"
                "cpu_s = 1800\n"
                'mem_mb = "unlimited"\n'
                "nofile = 1024\n"
            ),
            tool_sandbox=True,
        )


class TestSandboxDoctorChecks:
    @pytest.mark.skipif(not sys.platform.startswith("linux"),
                         reason="the claude-cli default's enforcement text is pinned to linux")
    def test_the_claude_cli_default_warns_on_fs_scope_and_net(self):
        checks = sandbox_doctor_checks(
            ClaudeCliReferenceAdapter(), provider_id="claude_code", config=_Config())
        assert checks == (
            ("sandbox_claude_code", True,
             "profile claude-cli; warning, unenforced: "
             "fs_scope (no tool sandbox: only the working directory is pinned); "
             "net (the host network is shared and hosts are not filtered)"),
        )

    @pytest.mark.skipif(not sys.platform.startswith("linux"),
                         reason="strict's enforcement text outside the tool sandbox is pinned to linux")
    def test_strict_chosen_warns_on_every_dimension_outside_the_tool_sandbox(self):
        checks = sandbox_doctor_checks(
            ClaudeCliReferenceAdapter(), provider_id="claude_code",
            config=_Config({"claude_cli.sandbox_profile": "strict"}))
        assert checks == (
            ("sandbox_claude_code", True,
             "profile strict; warning, unenforced: "
             "fs_scope (no tool sandbox: only the working directory is pinned); "
             "net (no tool sandbox: only proxy variables point at a closed port); "
             "allowed_binaries (binaries are not filtered by name); "
             "tmp_quota_mb (no tool sandbox: /tmp is the host's)"),
        )

    def test_net_local_chosen_fails_naming_the_refusal(self):
        checks = sandbox_doctor_checks(
            ClaudeCliReferenceAdapter(), provider_id="claude_code",
            config=_Config({"claude_cli.sandbox_profile": "net-local"}))
        assert len(checks) == 1
        name, ok, detail = checks[0]
        assert (name, ok) == ("sandbox_claude_code", False)
        assert "loosens the minimum 'claude-cli'" in detail

    @pytest.mark.skipif(not sys.platform.startswith("linux"),
                         reason="the enforced/unenforced split is pinned to linux")
    def test_every_dimension_enforced_inside_an_available_tool_sandbox(self, monkeypatch):
        monkeypatch.setattr(SP, "sandbox_runner_available", lambda: True)
        checks = sandbox_doctor_checks(
            _EveryDimensionEnforcedDouble(), provider_id="claude_code", config=_Config())
        assert checks == (
            ("sandbox_claude_code", True, "profile claude-cli; every dimension enforced"),)
