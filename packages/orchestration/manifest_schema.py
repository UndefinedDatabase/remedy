"""F012 — the STRICT external schema layer for untrusted manifest JSON (round 7).

Everything Remedy reads back from disk is untrusted input. The dataclass ``from_json`` helpers
used to coerce (``bool("false") is True``, ``int("1") == 1``), so a tampered record could flip a
Boolean or smuggle a string where an integer belongs and still parse. This module is the ONE
place that decides whether raw JSON is acceptable:

* a Boolean must be an actual JSON Boolean (``True``/``False``) — never ``"false"``/``0``;
* an integer must be an actual non-Boolean JSON integer — never ``"1"`` and never ``True``
  (Python's ``bool`` is an ``int`` subclass, which is exactly how ``True`` sneaks in);
* strings, lists and maps must already be that type;
* required fields have NO silent default;
* nothing is silently normalized;
* every string/list/map is BOUNDED before a large nested structure is allocated.

It is deliberately dependency-light (no ``run_manifest`` import) so the manifest module, the
recovery path, the export and the CLI can all share it without a cycle. It validates raw shapes
and returns the checked mapping; the typed dataclasses are constructed by the caller.

The LIMITS below are the single contract shared by the writer, the canonical reader, recovery and
the export (F11) — a writer must never be able to create a record the exporter would later refuse
for size alone.
"""
from __future__ import annotations

from typing import Any

# --------------------------------------------------------------------------- limits (F11)

#: One uniform size contract. Every layer (raw read → decode → typed validation → write →
#: recovery → canonical load → export) applies exactly these numbers.
MAX_INDEX_BYTES = 4 * 1024 * 1024
MAX_EPISODE_MANIFEST_BYTES = 8 * 1024 * 1024
MAX_ROOT_MIRROR_BYTES = MAX_EPISODE_MANIFEST_BYTES
MAX_CALL_ARTIFACT_BYTES = 2 * 1024 * 1024
MAX_PREPARED_INPUT_BYTES = 256 * 1024
MAX_INPUT_SNAPSHOT_BYTES = 2 * 1024 * 1024
MAX_JOB_INPUT_BYTES = 1024 * 1024
MAX_TREE_BYTES = 64 * 1024 * 1024

MAX_EPISODES = 512
MAX_CALLS_PER_EPISODE = 2048
MAX_CONFIG_ENTRIES = 512
MAX_ENV_ENTRIES = 256
MAX_PROBLEMS = 128
MAX_TASKS = 512

MAX_ID_LEN = 128
MAX_SHORT_TEXT = 512
MAX_PROBLEM_LEN = 500
MAX_VALUE_LEN = 4096


class SchemaError(ValueError):
    """Raw JSON did not satisfy the strict external schema. Never normalized away."""


# --------------------------------------------------------------------------- primitives


def req_map(d: Any, where: str) -> dict[str, Any]:
    if not isinstance(d, dict):
        raise SchemaError(f"{where}: expected a JSON object, got {type(d).__name__}")
    return d


def req_key(d: dict[str, Any], key: str, where: str) -> Any:
    if key not in d:
        raise SchemaError(f"{where}: missing required field {key!r}")
    return d[key]


def req_str(d: dict[str, Any], key: str, where: str, *, max_len: int = MAX_SHORT_TEXT,
            allow_empty: bool = False) -> str:
    v = req_key(d, key, where)
    if not isinstance(v, str):
        raise SchemaError(f"{where}.{key}: expected a JSON string, got {type(v).__name__}")
    if not allow_empty and v == "":
        raise SchemaError(f"{where}.{key}: must not be empty")
    if len(v) > max_len:
        raise SchemaError(f"{where}.{key}: exceeds {max_len} characters")
    return v


def req_bool(d: dict[str, Any], key: str, where: str) -> bool:
    v = req_key(d, key, where)
    if not isinstance(v, bool):
        raise SchemaError(
            f"{where}.{key}: expected a JSON boolean, got {type(v).__name__} ({v!r})")
    return v


def opt_bool_or_null(d: dict[str, Any], key: str, where: str) -> bool | None:
    v = req_key(d, key, where)
    if v is None:
        return None
    if not isinstance(v, bool):
        raise SchemaError(
            f"{where}.{key}: expected a JSON boolean or null, got {type(v).__name__} ({v!r})")
    return v


def req_int(d: dict[str, Any], key: str, where: str, *, minimum: int | None = None,
            maximum: int | None = None) -> int:
    v = req_key(d, key, where)
    # bool is an int subclass in Python — reject it explicitly, or True becomes 1.
    if isinstance(v, bool) or not isinstance(v, int):
        raise SchemaError(
            f"{where}.{key}: expected a JSON integer, got {type(v).__name__} ({v!r})")
    if minimum is not None and v < minimum:
        raise SchemaError(f"{where}.{key}: {v} is below the minimum {minimum}")
    if maximum is not None and v > maximum:
        raise SchemaError(f"{where}.{key}: {v} exceeds the maximum {maximum}")
    return v


def req_list(d: dict[str, Any], key: str, where: str, *, max_len: int) -> list[Any]:
    v = req_key(d, key, where)
    if not isinstance(v, list):
        raise SchemaError(f"{where}.{key}: expected a JSON array, got {type(v).__name__}")
    if len(v) > max_len:
        raise SchemaError(f"{where}.{key}: has {len(v)} entries, exceeding {max_len}")
    return v


def req_str_list(d: dict[str, Any], key: str, where: str, *, max_len: int,
                 max_item_len: int = MAX_PROBLEM_LEN) -> tuple[str, ...]:
    items = req_list(d, key, where, max_len=max_len)
    out: list[str] = []
    for i, it in enumerate(items):
        if not isinstance(it, str):
            raise SchemaError(f"{where}.{key}[{i}]: expected a JSON string")
        if len(it) > max_item_len:
            raise SchemaError(f"{where}.{key}[{i}]: exceeds {max_item_len} characters")
        out.append(it)
    return tuple(out)


def no_unknown_keys(d: dict[str, Any], allowed: set[str], where: str) -> None:
    extra = sorted(set(d) - allowed)
    if extra:
        raise SchemaError(f"{where}: unknown field(s) {extra}")


def bounded_bytes(raw: bytes, limit: int, where: str) -> bytes:
    if len(raw) > limit:
        raise SchemaError(f"{where}: {len(raw)} bytes exceeds the {limit}-byte limit")
    return raw


# --------------------------------------------------------------------------- shared formats


def is_hex64(value: Any) -> bool:
    return (isinstance(value, str) and len(value) == 64
            and all(c in "0123456789abcdef" for c in value))


def has_control_chars(value: str) -> bool:
    return any(ord(c) < 0x20 or ord(c) == 0x7F for c in value)
