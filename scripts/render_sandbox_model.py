"""Generates `docs/system/sandbox-model.md`, the sandbox honesty document (DECISION F162 D8).

Run `python3 scripts/render_sandbox_model.py` from the repository root to regenerate the document
after a profile, an enforcement reason or a proof test changes. `tests/docs/test_sandbox_model_doc.py`
fails whenever the committed file and `render_sandbox_model()` differ. This module imports the two
enforcement records, the three built-in profiles and the claude-cli adapter; nothing under
`packages/` or `apps/` reads it, so `tests/test_no_orphan_modules.py` carries it as deliberately
unwired, run by hand like its precedent `write_environment_guide` in
`packages/orchestration/config.py`.
"""
from __future__ import annotations

from pathlib import Path

from packages.orchestration.sandbox_container import container_sandbox_enforcement
from packages.orchestration.sandbox_profiles import (
    BUILTIN_SANDBOX_PROFILE_NAMES,
    SANDBOX_ENFORCEMENT_KEYS,
    SandboxProfile,
    _spell_value,
    get_sandbox_profile,
    parse_sandbox_profile,
    sandbox_profile_enforcement,
)
from packages.providers.adapters.claude_cli_reference import ClaudeCliReferenceAdapter

#: Where the rendered document lives, repository-relative (DECISION F162 D8 (2)).
SANDBOX_MODEL_DOC_PATH = "docs/system/sandbox-model.md"

#: One node id per dimension key, for the PROCESS runner: the fixture process of DECISION F162
#: D3 (5) where one proves the dimension for real, else the record test that pins the dimension's
#: state and reason word for word (DECISION F162 D8 (3)). Each id is copied from
#: `pytest --collect-only -q` over the two runner test files, not typed.
_PROCESS_PROOF: dict[str, str] = {
    "fs_scope": (
        "tests/orchestration/test_sandbox_profiles.py"
        "::test_strict_pins_the_workspace_as_the_one_writable_tree"),
    "net": (
        "tests/orchestration/test_sandbox_profiles.py"
        "::test_a_deny_profile_cannot_reach_the_host_loopback_and_net_local_can"),
    "ulimits.cpu_s": (
        "tests/orchestration/test_sandbox_profiles.py"
        "::test_a_one_second_cpu_limit_ends_a_busy_loop_classified_resource_limit_cpu_seconds"),
    "ulimits.mem_mb": (
        "tests/orchestration/test_sandbox_profiles.py"
        "::test_a_mem_limit_of_256_mib_refuses_1gib_and_allows_64mib"),
    "ulimits.nofile": (
        "tests/orchestration/test_sandbox_profiles.py"
        "::test_a_nofile_limit_of_16_refuses_the_64th_open_of_dev_null_with_errno_24"),
    "allowed_binaries": (
        "tests/orchestration/test_sandbox_profiles.py"
        "::test_sandbox_profile_enforcement_full_tuple_for_strict_sandboxed_linux"),
    "tmp_quota_mb": (
        "tests/orchestration/test_sandbox_profiles.py"
        "::test_sandbox_profile_enforcement_full_tuple_for_strict_sandboxed_linux"),
}

#: DECISION F162 D9: a row's PROCESS proof when its reason is `nothing to limit` — the existing
#: test that pins the claude-cli default's `adapter_sandbox_record` dict, which holds that reason
#: for `ulimits.cpu_s`, `ulimits.mem_mb`, `allowed_binaries` and `tmp_quota_mb`.
_NOTHING_TO_LIMIT_PROCESS_PROOF = (
    "tests/orchestration/test_worker_adapter_slot.py"
    "::test_adapter_sandbox_record_claude_cli_on_linux_matches_the_dict_literal")

#: The same, for the CONTAINER runner: the test pinning `container_sandbox_enforcement`'s full
#: value tuple for the claude-cli default with a runtime, which holds the same reason for the
#: same four keys.
_NOTHING_TO_LIMIT_CONTAINER_PROOF = (
    "tests/orchestration/test_sandbox_container.py"
    "::test_container_sandbox_enforcement_full_tuple_for_claude_cli_default_with_a_runtime")

#: The same, for the CONTAINER runner (DECISION F162 D7 (5) for the fixtures it has of its own).
_CONTAINER_PROOF: dict[str, str] = {
    "fs_scope": (
        "tests/orchestration/test_sandbox_container.py"
        "::test_container_strict_pins_the_workspace_as_the_one_writable_tree"),
    "net": (
        "tests/orchestration/test_sandbox_container.py"
        "::test_container_a_deny_profile_cannot_reach_the_host_loopback_and_net_local_can"),
    "ulimits.cpu_s": (
        "tests/orchestration/test_sandbox_container.py"
        "::test_container_a_one_second_cpu_limit_ends_a_busy_loop_classified_resource_limit_cpu_seconds"),
    "ulimits.mem_mb": (
        "tests/orchestration/test_sandbox_container.py"
        "::test_container_a_mem_limit_of_256_mib_refuses_1gib_and_allows_64mib"),
    "ulimits.nofile": (
        "tests/orchestration/test_sandbox_container.py"
        "::test_container_a_nofile_limit_of_16_refuses_the_64th_open_of_dev_null_with_errno_24"),
    "allowed_binaries": (
        "tests/orchestration/test_sandbox_container.py"
        "::test_container_sandbox_enforcement_full_tuple_for_strict_with_a_runtime"),
    "tmp_quota_mb": (
        "tests/orchestration/test_sandbox_container.py"
        "::test_container_tmp_quota_of_64_mib_refuses_a_100_mib_write_with_errno_28"),
}


def _declared(profile: SandboxProfile, key: str) -> str:
    """The Declared cell: the value, in the spelling `SandboxLoosening` uses (DECISION F162 D2)."""
    if key == "fs_scope":
        return _spell_value("fs_scope", profile.fs_scope)
    if key == "net":
        return _spell_value("net", profile.net)
    if key == "allowed_binaries":
        return _spell_value("allowed_binaries", profile.allowed_binaries)
    if key == "tmp_quota_mb":
        return _spell_value("tmp_quota_mb", profile.tmp_quota_mb)
    ulimit_key = key.split(".", 1)[1]
    return _spell_value(key, getattr(profile.ulimits, ulimit_key))


def _runner_cell(state: str, reason: str) -> str:
    """`prevents` for an enforced state, `does not prevent` for an unenforced one, and `no limit
    declared` for the reason `nothing to limit` — a run cannot go beyond a value the profile never
    declares, so it is never honest to say the runner "prevents" anything there (DECISION F162
    D8 (2), D9)."""
    if reason == "nothing to limit":
        return "no limit declared"
    verb = "prevents" if state == "enforced" else "does not prevent"
    return f"{verb} — {reason}"


def _profile_table(name: str, profile: SandboxProfile, *, process_sandboxed: bool) -> list[str]:
    """One profile's table: Dimension, Declared, Process runner, Container runner, Proof."""
    process_by_key = {
        item.key: item for item in sandbox_profile_enforcement(
            profile, platform="linux", sandbox_available=process_sandboxed)}
    container_by_key = {
        item.key: item for item in container_sandbox_enforcement(
            profile, runtime_available=True)}
    lines = [
        f"### {name}",
        "",
        "| Dimension | Declared | Process runner | Container runner | Proof |",
        "|---|---|---|---|---|",
    ]
    for key in SANDBOX_ENFORCEMENT_KEYS:
        process_item = process_by_key[key]
        container_item = container_by_key[key]
        declared = _declared(profile, key)
        process_cell = _runner_cell(process_item.state, process_item.reason)
        container_cell = _runner_cell(container_item.state, container_item.reason)
        process_proof = (
            _NOTHING_TO_LIMIT_PROCESS_PROOF if process_item.reason == "nothing to limit"
            else _PROCESS_PROOF[key])
        container_proof = (
            _NOTHING_TO_LIMIT_CONTAINER_PROOF if container_item.reason == "nothing to limit"
            else _CONTAINER_PROOF[key])
        proof = f"process: {process_proof}; container: {container_proof}"
        lines.append(f"| `{key}` | `{declared}` | {process_cell} | {container_cell} | {proof} |")
    lines.append("")
    return lines


def _claude_cli_default_profile() -> SandboxProfile:
    """The claude-cli adapter's own declared default, parsed the way `effective_sandbox_profile`
    parses it."""
    adapter = ClaudeCliReferenceAdapter()
    declaration = adapter.sandbox_default()
    return parse_sandbox_profile(adapter.adapter_id, declaration.profile_toml)


def render_sandbox_model() -> str:
    """`docs/system/sandbox-model.md`, rendered from the profile and enforcement records."""
    lines = [
        "# Sandbox Model",
        "",
        "> GENERATED from the sandbox profile and enforcement records in",
        "> `packages/orchestration/sandbox_profiles.py` and",
        "> `packages/orchestration/sandbox_container.py`, by `render_sandbox_model()`. Do not",
        "> edit it by hand: `tests/docs/test_sandbox_model_doc.py` fails whenever this file and",
        "> the rendering differ. Regenerate it from the repository root with",
        "> `python3 scripts/render_sandbox_model.py`.",
        "",
        "A sandbox profile fixes five dimensions a worker's sandbox decides: the filesystem",
        "scope it may touch, its network reach, its resource ulimits, which binaries it may",
        "run, and its tmp quota; the three `ulimits` keys each get their own row below, for",
        "seven rows per profile. A dimension is marked enforced when a real mechanism stops the",
        "run going past the declared value, never merely because the profile declares one",
        "(DECISION F162 D3 (4)). Off Linux, every dimension that declares an actual limit reports",
        "unenforced for both runners, because neither has a verified mechanism there; a",
        "dimension with nothing to limit still reports enforced, trivially.",
        "",
    ]
    for builtin_name in BUILTIN_SANDBOX_PROFILE_NAMES:
        lines += _profile_table(
            builtin_name, get_sandbox_profile(builtin_name), process_sandboxed=True)
    lines += _profile_table(
        "claude-cli (adapter default)", _claude_cli_default_profile(), process_sandboxed=False)
    return "\n".join(lines).rstrip("\n") + "\n"


def write_sandbox_model(root: Path | None = None) -> Path:
    """Write the rendered document under `root` (the repository root by default) and return its
    path."""
    base = root if root is not None else Path(__file__).resolve().parents[1]
    path = base / SANDBOX_MODEL_DOC_PATH
    path.write_text(render_sandbox_model(), encoding="utf-8")
    return path


if __name__ == "__main__":
    write_sandbox_model()
