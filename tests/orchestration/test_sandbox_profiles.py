"""Pins DECISION F162 D2: the sandbox profile schema, its three built-ins, and the tighten-only
order's refusal. `packages/orchestration/sandbox_profiles.py`'s own module docstring states what
T001 does NOT yet do — nothing here proves a profile is read by any spawn path.

This half (F162 round 2 C2) pins parsing: the TOML form's refusal rules, one per rule of DECISION
F162 D2 (3), the built-ins' exact values, and normalization. F162 round 2 C3 adds the tighten-only
order's table tests, the preorder properties and the refusal message.
"""
from __future__ import annotations

import pytest

from packages.orchestration.sandbox_profiles import (
    BUILTIN_SANDBOX_PROFILE_NAMES,
    SandboxNet,
    SandboxProfile,
    SandboxProfileError,
    SandboxUlimits,
    get_sandbox_profile,
    load_builtin_sandbox_profiles,
    parse_sandbox_profile,
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
