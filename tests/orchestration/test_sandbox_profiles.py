"""Pins DECISION F162 D2: the sandbox profile schema, its three built-ins, and the tighten-only
order's refusal. `packages/orchestration/sandbox_profiles.py`'s own module docstring states what
T001 does NOT yet do — nothing here proves a profile is read by any spawn path.

This half (F162 round 2 C2) pins parsing: the TOML form's refusal rules, one per rule of DECISION
F162 D2 (3), the built-ins' exact values, and normalization. F162 round 2 C3 adds the tighten-only
order's table tests, the preorder properties and the refusal message.
"""
from __future__ import annotations

import dataclasses
import itertools

import pytest

from packages.orchestration.sandbox_profiles import (
    BUILTIN_SANDBOX_PROFILE_NAMES,
    SandboxLoosening,
    SandboxNet,
    SandboxProfile,
    SandboxProfileError,
    SandboxProfileLoosened,
    SandboxUlimits,
    get_sandbox_profile,
    load_builtin_sandbox_profiles,
    parse_sandbox_profile,
    profile_loosenings,
    profile_within,
    tighten_sandbox_profile,
)

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
