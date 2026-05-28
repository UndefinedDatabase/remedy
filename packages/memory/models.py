"""Memory entry model for Remedy's local memory gateway."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal
from uuid import UUID, uuid4


@dataclass
class MemoryEntry:
    """A single memory entry stored in the local gateway.

    Fields follow the spec: version, id, project_id, job_id, key, value,
    tags, source_type, source_id, created_at, expires_at, approved,
    confidence_source, redaction_policy.

    No raw artifact/stdout/diff/secret content is stored.
    """

    version: int = 1
    id: UUID = field(default_factory=uuid4)
    project_id: str | None = None
    job_id: str | None = None
    key: str = ""
    value: str = ""
    tags: list[str] = field(default_factory=list)
    source_type: Literal["human", "agent", "system"] = "human"
    source_id: str | None = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    expires_at: str | None = None
    approved: bool = False
    confidence_source: Literal["human_explicit", "human_implicit", "agent_derived", "system"] = "human_explicit"
    redaction_policy: Literal["none", "redact_secrets", "redact_all"] = "redact_secrets"

    def to_json_line(self) -> str:
        """Serialize to compact JSON line."""
        d = {
            "version": self.version,
            "id": str(self.id),
            "project_id": self.project_id,
            "job_id": self.job_id,
            "key": self.key,
            "value": self.value,
            "tags": self.tags,
            "source_type": self.source_type,
            "source_id": self.source_id,
            "created_at": self.created_at,
            "expires_at": self.expires_at,
            "approved": self.approved,
            "confidence_source": self.confidence_source,
            "redaction_policy": self.redaction_policy,
        }
        return json.dumps(d, separators=(",", ":"))

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> MemoryEntry:
        """Deserialize from a dict (parsed JSON line)."""
        return cls(
            version=d.get("version", 1),
            id=UUID(d["id"]),
            project_id=d.get("project_id"),
            job_id=d.get("job_id"),
            key=d.get("key", ""),
            value=d.get("value", ""),
            tags=d.get("tags", []),
            source_type=d.get("source_type", "human"),
            source_id=d.get("source_id"),
            created_at=d.get("created_at", ""),
            expires_at=d.get("expires_at"),
            approved=d.get("approved", False),
            confidence_source=d.get("confidence_source", "human_explicit"),
            redaction_policy=d.get("redaction_policy", "redact_secrets"),
        )
