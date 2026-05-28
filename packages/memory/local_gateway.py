"""Local JSONL-based memory gateway for Remedy.

Storage layout::

    <DATA_DIR>/memory/<project_id>/memory.jsonl   — project-scoped
    <DATA_DIR>/memory/unscoped/<job_id>.jsonl      — unscoped (job-only)

Conforms to the MemoryGateway protocol from packages.contracts.interfaces.
Recall is keyword/recency-based (no embeddings, no LLM).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from packages.memory.models import MemoryEntry
from packages.orchestration.data_paths import resolve_data_root


def _memory_dir() -> Path:
    """Return the root memory directory."""
    return resolve_data_root() / "memory"


def _jsonl_path(project_id: str | None, job_id: str | None) -> Path:
    """Resolve the JSONL file path for a given scope."""
    root = _memory_dir()
    if project_id:
        p = root / project_id / "memory.jsonl"
    elif job_id:
        p = root / "unscoped" / f"{job_id}.jsonl"
    else:
        p = root / "unscoped" / "global.jsonl"
    return p


def _load_entries(path: Path) -> list[MemoryEntry]:
    """Load all entries from a JSONL file."""
    if not path.exists():
        return []
    entries: list[MemoryEntry] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
            entries.append(MemoryEntry.from_dict(d))
        except (json.JSONDecodeError, KeyError, ValueError):
            continue
    return entries


def _append_entry(path: Path, entry: MemoryEntry) -> None:
    """Append one entry to the JSONL file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(entry.to_json_line() + "\n")


def _rewrite_entries(path: Path, entries: list[MemoryEntry]) -> None:
    """Rewrite all entries to the JSONL file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for entry in entries:
            f.write(entry.to_json_line() + "\n")


# ---------------------------------------------------------------------------
# Public API — sync (CLI-friendly)
# ---------------------------------------------------------------------------


def store_memory(
    key: str,
    value: str,
    *,
    project_id: str | None = None,
    job_id: str | None = None,
    tags: list[str] | None = None,
    source_type: str = "human",
    approved: bool = False,
) -> MemoryEntry:
    """Store a new memory entry. Returns the created entry."""
    entry = MemoryEntry(
        project_id=project_id,
        job_id=job_id,
        key=key,
        value=value,
        tags=tags or [],
        source_type=source_type,  # type: ignore[arg-type]
        approved=approved,
    )
    path = _jsonl_path(project_id, job_id)
    _append_entry(path, entry)
    return entry


def recall_memory(
    *,
    project_id: str | None = None,
    job_id: str | None = None,
    keyword: str | None = None,
    max_results: int = 5,
) -> list[MemoryEntry]:
    """Recall memory entries by keyword/recency. No embeddings, no LLM.

    Returns up to max_results entries, newest first.
    If keyword is given, filters entries where keyword appears in key, value, or tags.
    """
    path = _jsonl_path(project_id, job_id)
    entries = _load_entries(path)

    if keyword:
        kw = keyword.lower()
        entries = [
            e for e in entries
            if kw in e.key.lower()
            or kw in e.value.lower()
            or any(kw in t.lower() for t in e.tags)
        ]

    # Sort by created_at descending (newest first)
    entries.sort(key=lambda e: e.created_at, reverse=True)
    return entries[:max_results]


def list_memory(
    *,
    project_id: str | None = None,
    job_id: str | None = None,
) -> list[MemoryEntry]:
    """List all memory entries for a scope."""
    path = _jsonl_path(project_id, job_id)
    entries = _load_entries(path)
    entries.sort(key=lambda e: e.created_at, reverse=True)
    return entries


def delete_memory(
    entry_id: str,
    *,
    project_id: str | None = None,
    job_id: str | None = None,
) -> bool:
    """Delete a memory entry by ID. Returns True if found and deleted."""
    path = _jsonl_path(project_id, job_id)
    entries = _load_entries(path)
    before = len(entries)
    entries = [e for e in entries if str(e.id) != entry_id]
    if len(entries) == before:
        return False
    _rewrite_entries(path, entries)
    return True


def has_approved_memory(
    *,
    project_id: str | None = None,
    job_id: str | None = None,
) -> bool:
    """Check if any approved memory entries exist for a scope."""
    path = _jsonl_path(project_id, job_id)
    entries = _load_entries(path)
    return any(e.approved for e in entries)


# ---------------------------------------------------------------------------
# Async MemoryGateway protocol implementation
# ---------------------------------------------------------------------------


class LocalMemoryGateway:
    """Local JSONL-backed memory gateway conforming to MemoryGateway protocol.

    The async methods wrap the sync implementations above.
    """

    def __init__(
        self,
        project_id: str | None = None,
        job_id: str | None = None,
    ) -> None:
        self._project_id = project_id
        self._job_id = job_id

    async def read(self, key: str) -> object:
        """Retrieve the most recent value for a key. Returns None if not found."""
        entries = recall_memory(
            project_id=self._project_id,
            job_id=self._job_id,
            keyword=key,
            max_results=1,
        )
        # Find exact key match
        for e in entries:
            if e.key == key:
                return e.value
        return None

    async def write(self, key: str, value: object) -> None:
        """Persist a value under the given key."""
        store_memory(
            key=key,
            value=str(value),
            project_id=self._project_id,
            job_id=self._job_id,
        )

    async def delete(self, key: str) -> None:
        """Remove entries matching a key."""
        path = _jsonl_path(self._project_id, self._job_id)
        entries = _load_entries(path)
        entries = [e for e in entries if e.key != key]
        _rewrite_entries(path, entries)
