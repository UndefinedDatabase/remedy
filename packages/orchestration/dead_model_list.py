"""F254 — the known-dead model list: shipped data, plus the operator's additions.

A model id that a provider has retired keeps working as a config default right
up until a job fails on it, and the failure names the provider, not the stale
string.  This module is where Remedy answers "is this id known to be dead?" — by
reading a shipped, operator-editable data file (``scripts/dead_models.json``)
and merging it with whatever the operator added under ``doctor.dead_models``.

The file lives in ``scripts/`` beside the other shipped campaign data, resolved
the same way :func:`packages.orchestration.gauntlet_orders.default_orders_dir`
resolves its directory: it is shipped INPUT an operator is meant to edit, not
test data.

Public API::

    DEAD_MODEL_SCHEMA_VERSION: the schema_version this loader accepts
    DeadModelEntry: one dead id, why it is dead, and what replaced it
    DeadModelListError: the list is missing or malformed
    default_dead_list_path() -> Path
    load_dead_models(path=None) -> tuple[DeadModelEntry, ...]
    dead_model_ids(path=None) -> frozenset[str]

Deliberate absences:
  * Remedy deliberately does not probe a provider or call the network to decide
    whether a model is dead.  Live provider probing is a Non-goal of F254
    (docs/roadmap/features/T2_F254.md), so this list is operator-maintained
    DATA: the check is exactly as fresh as its file, and any output built on it
    must say so rather than implying live knowledge of a provider's catalogue.
  * Remedy deliberately does not let config REPLACE the shipped list.  Config
    only extends, the same way ``smoke.error_patterns`` extends
    ``product_smoke.CONSOLE_ERROR_PATTERNS`` — a shipped entry cannot be
    configured away, because "we already know this id is dead" is a guarantee,
    not a preference.
  * Remedy deliberately does not fall back to an empty list when the file
    cannot be read.  "No dead models" and "I could not read the list" are
    opposite answers and must never look alike, so an unreadable file raises.
  * Remedy deliberately does not name a replacement id it cannot source from
    this repository.  ``superseded_by`` is empty rather than guessed; choosing
    successors is F232's job (the model upgrade playbook).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

#: The one schema version this loader accepts.  A file from the future is
#: refused rather than half-read: a field this code does not understand is
#: exactly the field that would have said "actually, not dead".
DEAD_MODEL_SCHEMA_VERSION = 1

#: The config key whose value EXTENDS the shipped list.  Named once here so the
#: loader and the key registry cannot drift apart.
DEAD_MODEL_CONFIG_KEY = "doctor.dead_models"

#: The file name shipped under ``scripts/``.  One spelling, so nothing loads a
#: copy of the list.
DEAD_MODEL_LIST_FILENAME = "dead_models.json"


class DeadModelListError(RuntimeError):
    """The shipped dead-model list is missing, unreadable, or malformed.

    Raised rather than degraded to an empty list: a doctor check that silently
    reports "nothing dead" because it could not open its data file is worse
    than no check at all — it manufactures confidence out of an I/O failure.
    """


@dataclass(frozen=True)
class DeadModelEntry:
    """One retired model id, as written in the shipped file."""

    id: str
    reason: str
    superseded_by: str


def default_dead_list_path(repo_root: Path | None = None) -> Path:
    """Where the shipped list lives — resolved like the gauntlet order set."""
    root = repo_root or Path(__file__).resolve().parents[2]
    return root / "scripts" / DEAD_MODEL_LIST_FILENAME


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise DeadModelListError(message)


def load_dead_models(path: Path | None = None) -> tuple[DeadModelEntry, ...]:
    """Read and validate the dead-model list. Never half-loads, never guesses.

    Every failure message names the path, because the first question a reader
    has when this raises is "which file did it try to read?" — and the answer
    is not obvious once an operator has pointed the loader elsewhere.

    Raises:
        DeadModelListError: the file is missing or unreadable, is not a JSON
            object, carries an unsupported ``schema_version``, or holds an
            entry without a non-empty ``id`` and ``reason``.
    """
    list_path = path or default_dead_list_path()
    try:
        body = json.loads(list_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise DeadModelListError(f"{list_path}: unreadable ({exc})") from exc

    _require(isinstance(body, dict), f"{list_path}: not a JSON object")

    version = body.get("schema_version")
    _require(version == DEAD_MODEL_SCHEMA_VERSION,
             f"{list_path}: unsupported schema_version {version!r} "
             f"(this Remedy reads {DEAD_MODEL_SCHEMA_VERSION})")

    raw_entries = body.get("dead_models")
    _require(isinstance(raw_entries, list),
             f"{list_path}: dead_models must be a list")

    entries: list[DeadModelEntry] = []
    for position, raw in enumerate(raw_entries, 1):
        _require(isinstance(raw, dict),
                 f"{list_path}: dead_models[{position}] is not an object")
        for field_name in ("id", "reason"):
            value = raw.get(field_name)
            _require(isinstance(value, str) and value.strip(),
                     f"{list_path}: dead_models[{position}] has a missing or "
                     f"blank {field_name}")
        superseded = raw.get("superseded_by", "")
        _require(isinstance(superseded, str),
                 f"{list_path}: dead_models[{position}].superseded_by must be "
                 f"a string (empty when no replacement is known)")
        entries.append(DeadModelEntry(id=raw["id"], reason=raw["reason"],
                                      superseded_by=superseded))

    ids = [entry.id for entry in entries]
    _require(len(set(ids)) == len(ids),
             f"{list_path}: duplicate dead model ids: {sorted(ids)}")
    return tuple(entries)


def _configured_dead_model_ids() -> tuple[str, ...]:
    """The operator's ADDITIONS, read through the normal config accessor.

    A config that will not load yields no additions rather than an exception:
    the shipped list is the guarantee, and losing the extension must not take
    the guarantee down with it.  The shipped list's own failures still raise —
    see :func:`load_dead_models`.
    """
    try:
        from packages.orchestration.config import get_config
        value = get_config().get(DEAD_MODEL_CONFIG_KEY)
    except Exception:  # noqa: BLE001 — config unavailable = no extension
        return ()
    if not value:
        return ()
    return tuple(str(item).strip() for item in value if str(item).strip())


def dead_model_ids(path: Path | None = None) -> frozenset[str]:
    """The shipped ids PLUS the operator's ``doctor.dead_models`` additions.

    Config EXTENDS and never replaces, exactly as ``smoke.error_patterns``
    extends the documented console-error base list: an operator can teach
    Remedy about a model their own provider retired, but cannot configure away
    an id Remedy already ships as dead.
    """
    shipped = frozenset(entry.id for entry in load_dead_models(path))
    return shipped | frozenset(_configured_dead_model_ids())
