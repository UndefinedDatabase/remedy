"""Sandbox profile schema: what a worker process may touch, as a named, testable, tighten-only policy.

A SandboxProfile fixes five dimensions a worker's sandbox decides: the filesystem scope it may
touch, its network reach (deny or a host allowlist), its resource ulimits, which binaries it may
run, and its tmp quota. Three built-ins ship as TOML files beside this module (DECISION F162 D2).

T001 is the policy math only: parsing, the built-ins, and the tighten-only comparator that refuses
a looser profile and names the minimum it would loosen. T002 compiles a profile onto the exec
guard and the tool sandbox and records, per dimension and platform, whether each is enforced. No
worker spawn path reads a profile yet — no adapter, no config key — so
`tests/test_no_orphan_modules.py` still carries this module as deliberately unwired, its reason now
naming T003.

The comparator (`profile_within`, `profile_loosenings`) orders profiles with a PREORDER, not a
total order: reflexive and transitive, but not antisymmetric — two differently named profiles
holding equal values are within each other both ways. `tighten_sandbox_profile` is the one-sided
use of that order a caller needs: a project may ask for anything at or below its adapter's minimum,
never above it.
"""
from __future__ import annotations

import dataclasses
import json
import signal
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, NoReturn

from packages.orchestration.exec_guard import ExecGuardPolicy, ExecGuardResult, run_guarded
from packages.orchestration.tool_sandbox import SandboxSpec, SandboxUnavailable, require_sandbox

if sys.version_info >= (3, 11):
    import tomllib
else:  # pragma: no cover - the 3.10 floor reads profile TOML through the backport
    import tomli as tomllib

#: The five policy dimensions, in the order every comparator and refusal reports them.
SANDBOX_DIMENSIONS = ("fs_scope", "net", "ulimits", "allowed_binaries", "tmp_quota_mb")

#: The three required `[ulimits]` keys, in report order.
SANDBOX_ULIMIT_KEYS = ("cpu_s", "mem_mb", "nofile")

#: The shipped profiles, in load and comparison order.
BUILTIN_SANDBOX_PROFILE_NAMES = ("strict", "standard", "net-local")

#: Exactly the top-level keys a profile's TOML may hold; none optional, none extra.
_REQUIRED_TOP_KEYS = frozenset({"fs_scope", "net", "allowed_binaries", "tmp_quota_mb", "ulimits"})

#: The built-in TOML files live beside this module, not inside it (DECISION F162 D2 (1)).
_PROFILE_FILES_DIR = Path(__file__).resolve().parent / "sandbox_profile_files"


class SandboxProfileError(ValueError):
    """A profile's TOML broke DECISION F162 D2's shape, or named an unknown profile."""


@dataclass(frozen=True)
class SandboxNet:
    """A profile's network reach: deny (`hosts` empty) or an allowlist (`hosts` non-empty)."""

    mode: str
    hosts: tuple[str, ...]


@dataclass(frozen=True)
class SandboxUlimits:
    """One positive int or None (unlimited) per SANDBOX_ULIMIT_KEYS entry."""

    cpu_s: int | None
    mem_mb: int | None
    nofile: int | None


@dataclass(frozen=True)
class SandboxProfile:
    """A named, fully-spelled point in all five SANDBOX_DIMENSIONS; no value is implied by absence."""

    name: str
    fs_scope: tuple[str, ...]
    net: SandboxNet
    ulimits: SandboxUlimits
    allowed_binaries: tuple[str, ...] | None
    tmp_quota_mb: int | None


@dataclass(frozen=True)
class SandboxLoosening:
    """One dimension where a candidate profile is looser than a minimum, spelled for the refusal."""

    dimension: str
    minimum_value: str
    candidate_value: str


class SandboxProfileLoosened(SandboxProfileError):
    """tighten_sandbox_profile's refusal: str() names the minimum and every loosening, in order."""

    def __init__(self, minimum_name: str, loosenings: tuple[SandboxLoosening, ...],
                 requested_name: str) -> None:
        clauses = "; ".join(f"{loosening.dimension} {loosening.minimum_value} -> "
                             f"{loosening.candidate_value}" for loosening in loosenings)
        super().__init__(f"sandbox profile '{requested_name}' loosens the minimum "
                          f"'{minimum_name}': {clauses}")
        self.minimum_name = minimum_name
        self.loosenings = loosenings


def _refuse(name: str, key: str, problem: str) -> NoReturn:
    """Every refusal names the profile and the key (DECISION F162 D2 (3))."""
    raise SandboxProfileError(f"sandbox profile '{name}' key '{key}': {problem}")


def _parse_int_or_unlimited(name: str, key: str, value: object) -> int | None:
    """A positive int, or the string 'unlimited' for None; bool is never an integer here."""
    if isinstance(value, str):
        if value == "unlimited":
            return None
        _refuse(name, key, f"{value!r} is not an integer or 'unlimited'")
    if isinstance(value, bool) or not isinstance(value, int):
        _refuse(name, key, f"{value!r} is not an integer or 'unlimited'")
    if value <= 0:
        _refuse(name, key, f"{value} is not a positive integer")
    return value


def _normalize_fs_scope_entry(name: str, entry: object) -> str:
    """{workspace}, a path below it, or an absolute POSIX path; '.', '..' and empty parts refused."""
    if not isinstance(entry, str) or entry == "":
        _refuse(name, "fs_scope", f"{entry!r} is not a path")
    if entry == "{workspace}":
        return entry
    if entry.startswith("{workspace}/"):
        prefix, raw_tail = "{workspace}/", entry[len("{workspace}/"):]
    elif entry.startswith("/"):
        prefix, raw_tail = "/", entry[1:]
    else:
        _refuse(name, "fs_scope", f"{entry!r} is neither '{{workspace}}', below it, nor absolute")
    parts = [part for part in raw_tail.split("/") if part != "."]
    if not parts or any(part in ("", "..") for part in parts):
        _refuse(name, "fs_scope", f"{entry!r} holds an empty or '..' path part")
    return prefix + "/".join(parts)


def _normalize_host(name: str, host: object) -> str:
    """A non-empty string without whitespace or '/'; hosts are lower-cased before comparison."""
    if (not isinstance(host, str) or host == "" or "/" in host
            or any(char.isspace() for char in host)):
        _refuse(name, "net", f"{host!r} is not a bare host name")
    return host.lower()


def _normalize_binary(name: str, binary: object) -> str:
    """A bare binary name: no path separator."""
    if not isinstance(binary, str) or binary == "" or "/" in binary:
        _refuse(name, "allowed_binaries", f"{binary!r} is not a bare binary name")
    return binary


def _parse_net(name: str, raw: object) -> SandboxNet:
    """The string 'deny', or a one-key table {allow = [...]} with at least one host."""
    if raw == "deny":
        return SandboxNet(mode="deny", hosts=())
    if isinstance(raw, dict) and set(raw) == {"allow"}:
        allow = raw["allow"]
        if isinstance(allow, list) and allow:
            hosts = tuple(sorted({_normalize_host(name, host) for host in allow}))
            return SandboxNet(mode="allowlist", hosts=hosts)
    _refuse(name, "net", f"{raw!r} is neither 'deny' nor a non-empty {{ allow = [...] }} table")


def _parse_allowed_binaries(name: str, raw: object) -> tuple[str, ...] | None:
    """A list of bare binary names, or the string 'any' for None."""
    if raw == "any":
        return None
    if isinstance(raw, list):
        return tuple(sorted({_normalize_binary(name, binary) for binary in raw}))
    _refuse(name, "allowed_binaries", f"{raw!r} is neither a list of binaries nor 'any'")


def _parse_fs_scope(name: str, raw: object) -> tuple[str, ...]:
    """A non-empty array of normalized paths; duplicates collapse."""
    if not isinstance(raw, list) or not raw:
        _refuse(name, "fs_scope", f"{raw!r} is not a non-empty array")
    return tuple(sorted({_normalize_fs_scope_entry(name, entry) for entry in raw}))


def _parse_ulimits(name: str, raw: object) -> SandboxUlimits:
    """Exactly cpu_s, mem_mb and nofile; each a positive int or 'unlimited'."""
    if not isinstance(raw, dict):
        _refuse(name, "ulimits", f"{raw!r} is not a table")
    missing = [key for key in SANDBOX_ULIMIT_KEYS if key not in raw]
    if missing:
        _refuse(name, f"ulimits.{missing[0]}", "missing from [ulimits]")
    extra = [key for key in raw if key not in SANDBOX_ULIMIT_KEYS]
    if extra:
        _refuse(name, f"ulimits.{extra[0]}", "is not one of cpu_s, mem_mb, nofile")
    return SandboxUlimits(**{key: _parse_int_or_unlimited(name, f"ulimits.{key}", raw[key])
                              for key in SANDBOX_ULIMIT_KEYS})


def parse_sandbox_profile(name: str, text: str) -> SandboxProfile:
    """Parse one profile's TOML; every refusal raises SandboxProfileError naming name and the key."""
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        _refuse(name, "<toml>", f"text is not valid TOML: {exc}")
    missing = sorted(_REQUIRED_TOP_KEYS - set(data))
    if missing:
        _refuse(name, missing[0], "missing from the profile")
    extra = sorted(set(data) - _REQUIRED_TOP_KEYS)
    if extra:
        _refuse(name, extra[0], "is not a recognised top-level key")
    return SandboxProfile(
        name=name,
        fs_scope=_parse_fs_scope(name, data["fs_scope"]),
        net=_parse_net(name, data["net"]),
        ulimits=_parse_ulimits(name, data["ulimits"]),
        allowed_binaries=_parse_allowed_binaries(name, data["allowed_binaries"]),
        tmp_quota_mb=_parse_int_or_unlimited(name, "tmp_quota_mb", data["tmp_quota_mb"]),
    )


def load_builtin_sandbox_profiles(directory: Path | None = None) -> dict[str, SandboxProfile]:
    """Read strict.toml, standard.toml and net-local.toml; refuse a missing or a stray *.toml file."""
    folder = directory if directory is not None else _PROFILE_FILES_DIR
    present = {path.stem: path for path in folder.glob("*.toml")}
    missing = [n for n in BUILTIN_SANDBOX_PROFILE_NAMES if n not in present]
    if missing:
        raise SandboxProfileError(f"sandbox profile folder {folder}: missing built-in "
                                   f"{missing[0]}.toml")
    stray = sorted(set(present) - set(BUILTIN_SANDBOX_PROFILE_NAMES))
    if stray:
        raise SandboxProfileError(f"sandbox profile folder {folder}: unexpected file "
                                   f"{stray[0]}.toml")
    return {n: parse_sandbox_profile(n, present[n].read_text(encoding="utf-8"))
            for n in BUILTIN_SANDBOX_PROFILE_NAMES}


def get_sandbox_profile(name: str) -> SandboxProfile:
    """One of the three built-ins; any other name is refused, naming all three."""
    profiles = load_builtin_sandbox_profiles()
    if name not in profiles:
        raise SandboxProfileError(f"unknown sandbox profile {name!r}; known: "
                                   f"{', '.join(BUILTIN_SANDBOX_PROFILE_NAMES)}")
    return profiles[name]


def _fs_scope_within(candidate: tuple[str, ...], minimum: tuple[str, ...]) -> bool:
    """Every candidate entry equals or lies below some minimum entry, by path parts."""
    minimum_parts = [tuple(entry.split("/")) for entry in minimum]
    for entry in candidate:
        parts = tuple(entry.split("/"))
        if not any(parts[:len(one_minimum)] == one_minimum for one_minimum in minimum_parts):
            return False
    return True


def _net_within(candidate: SandboxNet, minimum: SandboxNet) -> bool:
    """deny is within everything; an allowlist is within an allowlist holding all its hosts."""
    if candidate.mode == "deny":
        return True
    if minimum.mode == "deny":
        return False
    return set(candidate.hosts) <= set(minimum.hosts)


def _int_within(candidate: int | None, minimum: int | None) -> bool:
    """An int is within any int at least as large and within None; None is within None only."""
    if minimum is None:
        return True
    if candidate is None:
        return False
    return candidate <= minimum


def _binaries_within(candidate: tuple[str, ...] | None, minimum: tuple[str, ...] | None) -> bool:
    """A tuple is within None and within any tuple holding all its names; None is within None only."""
    if minimum is None:
        return True
    if candidate is None:
        return False
    return set(candidate) <= set(minimum)


def _spell_value(dimension: str, value: object) -> str:
    """The TOML spelling a loosening and a refusal message print for one dimension's value."""
    if dimension == "net":
        if value.mode == "deny":
            return "deny"
        return f"{{ allow = {json.dumps(list(value.hosts))} }}"
    if value is None:
        return "any" if dimension == "allowed_binaries" else "unlimited"
    if isinstance(value, tuple):
        return json.dumps(list(value))
    return str(value)


def profile_loosenings(candidate: SandboxProfile, minimum: SandboxProfile) -> tuple[SandboxLoosening, ...]:
    """The tighten-only comparator's diagnostic: where candidate is looser than minimum, in order."""
    loosenings: list[SandboxLoosening] = []
    if not _fs_scope_within(candidate.fs_scope, minimum.fs_scope):
        loosenings.append(SandboxLoosening("fs_scope", _spell_value("fs_scope", minimum.fs_scope),
                                            _spell_value("fs_scope", candidate.fs_scope)))
    if not _net_within(candidate.net, minimum.net):
        loosenings.append(SandboxLoosening("net", _spell_value("net", minimum.net),
                                            _spell_value("net", candidate.net)))
    for key in SANDBOX_ULIMIT_KEYS:
        dimension = f"ulimits.{key}"
        candidate_value = getattr(candidate.ulimits, key)
        minimum_value = getattr(minimum.ulimits, key)
        if not _int_within(candidate_value, minimum_value):
            loosenings.append(SandboxLoosening(dimension, _spell_value(dimension, minimum_value),
                                                _spell_value(dimension, candidate_value)))
    if not _binaries_within(candidate.allowed_binaries, minimum.allowed_binaries):
        loosenings.append(SandboxLoosening(
            "allowed_binaries", _spell_value("allowed_binaries", minimum.allowed_binaries),
            _spell_value("allowed_binaries", candidate.allowed_binaries)))
    if not _int_within(candidate.tmp_quota_mb, minimum.tmp_quota_mb):
        loosenings.append(SandboxLoosening(
            "tmp_quota_mb", _spell_value("tmp_quota_mb", minimum.tmp_quota_mb),
            _spell_value("tmp_quota_mb", candidate.tmp_quota_mb)))
    return tuple(loosenings)


def profile_within(candidate: SandboxProfile, minimum: SandboxProfile) -> bool:
    """True exactly when candidate loosens nothing against minimum; the preorder's test."""
    return not profile_loosenings(candidate, minimum)


def tighten_sandbox_profile(minimum: SandboxProfile, requested: SandboxProfile) -> SandboxProfile:
    """Return requested unchanged when it tightens or matches minimum; else refuse by name."""
    loosenings = profile_loosenings(requested, minimum)
    if loosenings:
        raise SandboxProfileLoosened(minimum.name, loosenings, requested.name)
    return requested


# ---------------------------------------------------------------------------
# T002: enforcement onto the exec guard and the tool sandbox (DECISION F162 D3)
# ---------------------------------------------------------------------------


def _tighter_optional_int(base_value: int | None, profile_value: int | None) -> int | None:
    """The smaller of two optional limits; None is unlimited and always loses to a real int."""
    if base_value is None:
        return profile_value
    if profile_value is None:
        return base_value
    return min(base_value, profile_value)


# WHY: a profile never loosens what the base already set (D3 (2)) — every field below is the
# TIGHTER of the base's own value and the profile's, never a plain override; `tool_sandbox` False
# (DECISION F162 D5 (1)) leaves *base*'s own sandbox untouched, for a process that cannot run
# inside the tool sandbox at all, while every other field still compiles as D3 (2) states.
def sandbox_profile_guard_policy(
    profile: SandboxProfile, *, workspace: str, base: ExecGuardPolicy = ExecGuardPolicy(),
    tool_sandbox: bool = True,
) -> ExecGuardPolicy:
    """Compile *profile* onto *base* for a run at *workspace*.

    `fs_scope`, `allowed_binaries` and `tmp_quota_mb` compile to nothing beyond the sandbox
    itself — exactly what `sandbox_profile_enforcement` reports for those three dimensions.
    """
    mem_bytes = None if profile.ulimits.mem_mb is None else profile.ulimits.mem_mb * 1048576
    allowlist = profile.net.mode == "allowlist"
    if not tool_sandbox:
        sandbox = base.sandbox
    elif base.sandbox is None:
        sandbox = SandboxSpec(workspace=workspace, share_network=allowlist)
    else:
        sandbox = dataclasses.replace(
            base.sandbox, share_network=base.sandbox.share_network and allowlist)
    return dataclasses.replace(
        base,
        cpu_seconds=_tighter_optional_int(base.cpu_seconds, profile.ulimits.cpu_s),
        address_space_bytes=_tighter_optional_int(base.address_space_bytes, mem_bytes),
        open_files=_tighter_optional_int(base.open_files, profile.ulimits.nofile),
        deny_network=base.deny_network or profile.net.mode == "deny",
        sandbox=sandbox,
    )


# WHY: run_guarded can never classify a sandboxed CPU death as resource_limit/cpu_seconds, because
# the sandbox's own init reaps the signal and exits a plain 128+SIGXCPU — this is the one caller
# that both sandboxes a process and limits its CPU, so the attribution lives here (D3 (3)).
def run_guarded_with_sandbox_profile(
    argv: Sequence[str], profile: SandboxProfile, *, workspace: str,
    base: ExecGuardPolicy = ExecGuardPolicy(),
) -> ExecGuardResult:
    """Run *argv* under *profile* compiled onto *base*, attributing a sandboxed CPU trip."""
    policy = sandbox_profile_guard_policy(profile, workspace=workspace, base=base)
    result = run_guarded(argv, policy)
    if (policy.sandbox is not None and policy.cpu_seconds is not None
            and result.tripped_limit is None and result.returncode == 128 + signal.SIGXCPU):
        return dataclasses.replace(result, classification="resource_limit",
                                    tripped_limit="cpu_seconds")
    return result


#: The enforcement record's keys, in report order — the per-dimension, per-platform honesty
#: table DECISION F162 D3 (4) asks for, so a reader never has to infer the order.
SANDBOX_ENFORCEMENT_KEYS = (
    "fs_scope", "net", "ulimits.cpu_s", "ulimits.mem_mb", "ulimits.nofile",
    "allowed_binaries", "tmp_quota_mb",
)


@dataclass(frozen=True)
class SandboxDimensionEnforcement:
    """One dimension's honesty record: never claim enforced where nothing here can check it."""

    key: str
    state: str
    reason: str


def _enforcement_for_fs_scope(profile: SandboxProfile, platform: str,
                               sandbox_available: bool) -> SandboxDimensionEnforcement:
    """fs_scope is enforced only by the sandbox pinning {workspace} as the one writable tree."""
    if not platform.startswith("linux"):
        return SandboxDimensionEnforcement("fs_scope", "unenforced", f"not verified on {platform}")
    if not sandbox_available:
        return SandboxDimensionEnforcement(
            "fs_scope", "unenforced", "no tool sandbox: only the working directory is pinned")
    if "{workspace}" in profile.fs_scope:
        return SandboxDimensionEnforcement(
            "fs_scope", "enforced", "the tool sandbox makes the workspace the one writable tree")
    return SandboxDimensionEnforcement(
        "fs_scope", "unenforced",
        "the tool sandbox keeps the whole workspace writable, wider than the declared scope")


def _enforcement_for_net(profile: SandboxProfile, platform: str,
                          sandbox_available: bool) -> SandboxDimensionEnforcement:
    """deny is enforced by the sandbox's private namespace; an allowlist never filters hosts."""
    if not platform.startswith("linux"):
        return SandboxDimensionEnforcement("net", "unenforced", f"not verified on {platform}")
    if profile.net.mode == "allowlist":
        return SandboxDimensionEnforcement(
            "net", "unenforced", "the host network is shared and hosts are not filtered")
    if sandbox_available:
        return SandboxDimensionEnforcement(
            "net", "enforced", "a private network namespace with its own loopback only")
    return SandboxDimensionEnforcement(
        "net", "unenforced", "no tool sandbox: only proxy variables point at a closed port")


def _enforcement_for_ulimit(key: str, value: int | None, platform: str,
                             reason: str) -> SandboxDimensionEnforcement:
    """A ulimits key is enforced by the exec guard's own rlimit, independent of the sandbox."""
    dimension = f"ulimits.{key}"
    if value is None:
        return SandboxDimensionEnforcement(dimension, "enforced", "nothing to limit")
    if not platform.startswith("linux"):
        return SandboxDimensionEnforcement(dimension, "unenforced", f"not verified on {platform}")
    return SandboxDimensionEnforcement(dimension, "enforced", reason)


def _enforcement_for_allowed_binaries(value: tuple[str, ...] | None,
                                       platform: str) -> SandboxDimensionEnforcement:
    """No mechanism filters binaries by name; the read-only system dirs expose every one."""
    if value is None:
        return SandboxDimensionEnforcement("allowed_binaries", "enforced", "nothing to limit")
    if not platform.startswith("linux"):
        return SandboxDimensionEnforcement(
            "allowed_binaries", "unenforced", f"not verified on {platform}")
    return SandboxDimensionEnforcement(
        "allowed_binaries", "unenforced", "binaries are not filtered by name")


def _enforcement_for_tmp_quota(value: int | None, platform: str,
                                sandbox_available: bool) -> SandboxDimensionEnforcement:
    """Neither the sandbox nor the host sizes /tmp; a quota is never more than unenforced."""
    if value is None:
        return SandboxDimensionEnforcement("tmp_quota_mb", "enforced", "nothing to limit")
    if not platform.startswith("linux"):
        return SandboxDimensionEnforcement("tmp_quota_mb", "unenforced", f"not verified on {platform}")
    if sandbox_available:
        return SandboxDimensionEnforcement(
            "tmp_quota_mb", "unenforced", "the private /tmp has no size limit")
    return SandboxDimensionEnforcement(
        "tmp_quota_mb", "unenforced", "no tool sandbox: /tmp is the host's")


def sandbox_profile_enforcement(
    profile: SandboxProfile, *, platform: str, sandbox_available: bool,
) -> tuple[SandboxDimensionEnforcement, ...]:
    """The per-dimension, per-platform honesty record for *profile* (DECISION F162 D3 (4))."""
    return (
        _enforcement_for_fs_scope(profile, platform, sandbox_available),
        _enforcement_for_net(profile, platform, sandbox_available),
        _enforcement_for_ulimit("cpu_s", profile.ulimits.cpu_s, platform,
                                 "RLIMIT_CPU on the process tree"),
        _enforcement_for_ulimit("mem_mb", profile.ulimits.mem_mb, platform,
                                 "RLIMIT_AS on the process tree"),
        _enforcement_for_ulimit("nofile", profile.ulimits.nofile, platform,
                                 "RLIMIT_NOFILE on the process tree"),
        _enforcement_for_allowed_binaries(profile.allowed_binaries, platform),
        _enforcement_for_tmp_quota(profile.tmp_quota_mb, platform, sandbox_available),
    )


# WHY: callers that only need to know whether to describe a dimension as enforced never start a
# real sandboxed process to find out; only SandboxUnavailable means no (D3 (4)).
def sandbox_runner_available() -> bool:
    """Whether the real sandbox can run here, without starting any sandboxed process."""
    try:
        require_sandbox()
    except SandboxUnavailable:
        return False
    return True


# ---------------------------------------------------------------------------
# T003: the sandbox evidence, beside worker_isolation.jsonl (DECISION F162 D5 (4))
# ---------------------------------------------------------------------------

#: The one file name every claude-cli build's sandbox line is written to, beside
#: worker_isolation.jsonl (DECISION F162 D5 (4)).
WORKER_SANDBOX_FILENAME = "worker_sandbox.jsonl"


# WHY: the one typed shape record_worker_sandbox writes, built once so a test and the factory
# read the same fields back, mirroring worker_isolation_record (DECISION F162 D5 (4)).
def worker_sandbox_record(
    profile: SandboxProfile, *, tool_sandbox: bool, platform: str, sandbox_available: bool,
) -> dict[str, Any]:
    """D5 (4)'s evidence fields, except `role`, `provider` and `model`, which
    `record_worker_sandbox` adds."""
    enforcement = sandbox_profile_enforcement(
        profile, platform=platform, sandbox_available=sandbox_available)
    return {
        "profile": profile.name,
        "runner": "process",
        "tool_sandbox": tool_sandbox,
        "dimensions": {item.key: item.state for item in enforcement},
        "reasons": {item.key: item.reason for item in enforcement},
    }


# WHY: the run's sandbox evidence lives beside its isolation evidence, one line per claude-cli
# provider build, mirroring record_worker_isolation exactly (DECISION F162 D5 (4)).
def record_worker_sandbox(
    evidence_dir: str | None, *, role: str, provider: str, model: str, record: dict[str, Any],
) -> None:
    """Append one `worker_sandbox.jsonl` line; nothing written for a falsy EVIDENCE_DIR."""
    if not evidence_dir:
        return
    directory = Path(evidence_dir)
    directory.mkdir(parents=True, exist_ok=True)
    line = json.dumps(
        {"role": role, "provider": provider, "model": model, **record}, sort_keys=True)
    with open(directory / WORKER_SANDBOX_FILENAME, "a", encoding="utf-8") as handle:
        handle.write(line + "\n")
