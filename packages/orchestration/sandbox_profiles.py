"""Sandbox profile schema: what a worker process may touch, as a named, testable, tighten-only policy.

A SandboxProfile fixes five dimensions a worker's sandbox decides: the filesystem scope it may
touch, its network reach (deny or a host allowlist), its resource ulimits, which binaries it may
run, and its tmp quota. Three built-ins ship as TOML files beside this module (DECISION F162 D2).

T001 is the policy math only: parsing, the built-ins, and the tighten-only comparator that refuses
a looser profile and names the minimum it would loosen. Nothing in this module is read by a spawn
path yet — no adapter, no config key, no exec guard call, no tool sandbox call. T002 wires it into
those seams; until then `tests/test_no_orphan_modules.py` carries this module as deliberately
unwired.

The comparator (`profile_within`, `profile_loosenings`) orders profiles with a PREORDER, not a
total order: reflexive and transitive, but not antisymmetric — two differently named profiles
holding equal values are within each other both ways. `tighten_sandbox_profile` is the one-sided
use of that order a caller needs: a project may ask for anything at or below its adapter's minimum,
never above it.
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import NoReturn

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
