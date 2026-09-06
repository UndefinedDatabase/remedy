"""
Run Log v1 — append-only JSONL event trail for Remedy operations.

Events are written to:
  <REMEDY_DATA_DIR>/runs/<job_id>/<run_id>.jsonl

One event per line; each line is a compact JSON object. Files are
append-only — no event is ever modified or deleted once written.

Redaction policy (v1):
  Logged:     IDs, event names, provider/model/role, task_type, artifact
              kind, file paths already visible in CLI output, counts,
              booleans, outcomes, elapsed_ms, risk levels, verifier profile
              name, verification failure check names and messages.
  NOT logged: full artifact content, full prompts, full workspace file
              contents, full diff previews.

Storage location follows the same REMEDY_DATA_DIR resolution order as
storage.py and workspace.py:
  1. REMEDY_DATA_DIR environment variable, if set.
  2. Repository-local default: <repo_root>/.data/runs/
"""

from __future__ import annotations

import dataclasses
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

from packages.orchestration.data_paths import run_log_dir

# ---------------------------------------------------------------------------
# Run ID
# ---------------------------------------------------------------------------


def new_run_id() -> str:
    """Generate a unique run ID for one CLI invocation.

    Returns a 32-character hex string (UUID4 without hyphens).
    Each CLI invocation should create at most one RunLogWriter with a
    fresh run_id, so all events from one session share the same run_id.
    """
    return uuid4().hex


# ---------------------------------------------------------------------------
# Event model
# ---------------------------------------------------------------------------


@dataclass
class RunEvent:
    """A single event in the append-only run log.

    Serialized as one compact JSON line in the JSONL file.

    Redaction: top-level None fields are omitted from the serialized line.
    The metadata dict is always included (may be empty).
    """

    event: str
    job_id: str
    run_id: str
    timestamp: str
    task_id: str | None = None
    artifact_id: str | None = None
    provider: str | None = None
    role: str | None = None
    model: str | None = None
    outcome: str | None = None
    message: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_json_line(self) -> str:
        """Serialize to a compact JSON string (no trailing newline).

        None-valued fields are dropped; metadata is always included.
        """
        d = dataclasses.asdict(self)
        filtered = {k: v for k, v in d.items() if v is not None or k == "metadata"}
        return json.dumps(filtered, separators=(",", ":"))


# ---------------------------------------------------------------------------
# Writer
# ---------------------------------------------------------------------------


class RunLogWriter:
    """Append-only writer for a single run's JSONL event log.

    Creates <data_root>/runs/<job_id>/<run_id>.jsonl on first write (directory
    is created eagerly on construction).

    One instance should be used per CLI invocation. All events from a
    single invocation share the same run_id, forming a chronological
    session trail.
    """

    # The job-keyed join lives in data_paths.run_log_dir, so DECISION F260 D1's re-key changes one function body.
    def __init__(
        self,
        job_id: UUID,
        run_id: str | None = None,
        *,
        data_root: Path | None = None,
    ) -> None:
        self._job_id = str(job_id)
        self._run_id = run_id if run_id is not None else new_run_id()
        job_dir = run_log_dir(self._job_id, data_root)
        job_dir.mkdir(parents=True, exist_ok=True)
        self._path = job_dir / f"{self._run_id}.jsonl"

    @property
    def path(self) -> Path:
        """Absolute path of the JSONL file for this run."""
        return self._path

    @property
    def run_id(self) -> str:
        """The run ID shared by all events in this session."""
        return self._run_id

    def append(self, event: RunEvent) -> None:
        """Append one RunEvent to the JSONL file."""
        with self._path.open("a", encoding="utf-8") as f:
            f.write(event.to_json_line() + "\n")

    def log(
        self,
        event: str,
        *,
        task_id: str | None = None,
        artifact_id: str | None = None,
        provider: str | None = None,
        role: str | None = None,
        model: str | None = None,
        outcome: str | None = None,
        message: str | None = None,
        **metadata: Any,
    ) -> None:
        """Build and append a RunEvent from keyword arguments.

        Extra keyword arguments beyond the named fields become entries
        in the event's metadata dict.

        Example::

            log.log(
                "builder_completed",
                task_id="...",
                outcome="changed",
                elapsed_ms=1234,
                task_type="write_readme",
            )
        """
        evt = RunEvent(
            event=event,
            job_id=self._job_id,
            run_id=self._run_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            task_id=task_id,
            artifact_id=artifact_id,
            provider=provider,
            role=role,
            model=model,
            outcome=outcome,
            message=message,
            metadata=dict(metadata),
        )
        self.append(evt)


# ---------------------------------------------------------------------------
# Read helper (for tests and diagnostics only)
# ---------------------------------------------------------------------------


def read_run_events(path: Path) -> list[dict[str, Any]]:
    """Read all events from a JSONL run log file.

    Returns a list of dicts (one per line). Intended for tests and
    diagnostics — not for production code paths.

    Returns an empty list if the file does not exist.
    """
    if not path.exists():
        return []
    events: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            events.append(json.loads(line))
    return events
