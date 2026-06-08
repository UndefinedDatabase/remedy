"""
File Provenance v0 — trace why a file was changed in a Remedy job.

Given a job and a file path, walks the causal chain:
  patch_intent → approval → patch_apply → proof → test_run

Returns a structured provenance record suitable for CLI display or JSON export.

Public API::

    build_file_provenance(job, events, path) -> FileProvenance
    summarize_file_provenance(provenance) -> str
    export_file_provenance_json(provenance) -> dict[str, Any]
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from packages.core.models import Job
from packages.orchestration.approval_queue import list_patch_intents


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ProvenanceLink:
    """One step in the causal chain."""

    step: str
    node_type: str
    node_id: str
    status: str
    detail: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class FileProvenance:
    """Provenance record for a single file in a single job."""

    job_id: str
    path: str
    found: bool
    chain: tuple[ProvenanceLink, ...]
    proof_status: str = ""  # verified | failed | incomplete | unverified | ""


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def build_file_provenance(
    job: Job,
    events: list[dict[str, Any]],
    path: str,
) -> FileProvenance:
    """Build provenance chain for *path* within *job*.

    Deterministic, read-only, no repo access.
    """
    job_id_str = str(job.id)
    chain: list[ProvenanceLink] = []

    # 1. Find patch intents targeting this path
    intents = list_patch_intents(job)
    matching_intents = [i for i in intents if i["target_path"] == path]

    if not matching_intents:
        return FileProvenance(
            job_id=job_id_str, path=path, found=False, chain=()
        )

    for intent in matching_intents:
        iid = intent["intent_id"]

        # patch_intent
        chain.append(ProvenanceLink(
            step="patch_intent",
            node_type="patch_intent",
            node_id=f"pi:{iid}",
            status=intent["state"],
            detail={
                "intent_id": iid,
                "action": intent["action"],
                "risk": intent["risk"],
                "target_path": intent["target_path"],
            },
        ))

        # approval_decision
        if intent["state"] != "pending":
            chain.append(ProvenanceLink(
                step="approval_decision",
                node_type="approval_decision",
                node_id=f"approval:{iid}",
                status=intent["state"],
                detail={
                    "decided_at": intent.get("decided_at", ""),
                    "decided_by": intent.get("decided_by", ""),
                },
            ))

        # patch_apply (from artifact metadata)
        for artifact in job.artifacts:
            records = artifact.metadata.get("patch_intent_apply_records", {})
            if iid in records:
                rec = records[iid]
                chain.append(ProvenanceLink(
                    step="patch_apply",
                    node_type="patch_apply",
                    node_id=f"apply:{iid}",
                    status=rec.get("state", "unknown"),
                    detail={
                        "bytes_written": rec.get("bytes_written", 0),
                        "line_count": rec.get("line_count", 0),
                    },
                ))

        # patch_apply_proof (from events)
        proof_events = [
            e for e in events
            if e.get("event") == "patch_apply_proof_recorded"
            and e.get("metadata", {}).get("intent_id") == iid
        ]
        for pe in proof_events:
            pm = pe.get("metadata", {})
            chain.append(ProvenanceLink(
                step="patch_apply_proof",
                node_type="patch_apply_proof",
                node_id=f"proof:{iid}",
                status=str(pm.get("outcome", "recorded")),
                detail={
                    "before_sha256": str(pm.get("before_sha256", ""))[:16] + "…",
                    "after_sha256": str(pm.get("after_sha256", ""))[:16] + "…",
                    "bytes_delta": int(pm.get("bytes_delta", 0)),
                    "line_delta": int(pm.get("line_delta", 0)),
                    "applied_at": str(pm.get("applied_at", "")),
                },
            ))

    # test_run (any test_run_completed after apply)
    test_events = [
        e for e in events
        if e.get("event") == "test_run_completed"
    ]
    for idx, te in enumerate(test_events):
        tm = te.get("metadata", {})
        chain.append(ProvenanceLink(
            step="test_run",
            node_type="test_run",
            node_id=f"test_run:{idx}",
            status=str(tm.get("status", "unknown")),
            detail={
                "command": str(tm.get("command", "")),
                "exit_code": tm.get("exit_code"),
            },
        ))

    # Derive proof status from proof chain
    proof_status = ""
    try:
        from packages.orchestration.proof_chain import build_proof_chain
        pc = build_proof_chain(job, events, path=path)
        if pc.changes:
            proof_status = pc.changes[0].proof_status
    except Exception:
        pass

    return FileProvenance(
        job_id=job_id_str,
        path=path,
        found=True,
        chain=tuple(chain),
        proof_status=proof_status,
    )


def summarize_file_provenance(prov: FileProvenance) -> str:
    """Human-readable provenance summary."""
    parts: list[str] = []
    parts.append(f"File Provenance: {prov.path}")
    parts.append(f"Job: {prov.job_id[:8]}")

    if prov.proof_status:
        parts.append(f"Proof: {prov.proof_status}")

    if not prov.found:
        parts.append("  No patch intents found for this file.")
        return "\n".join(parts)

    parts.append(f"Chain ({len(prov.chain)} steps):")
    for link in prov.chain:
        parts.append(
            f"  [{link.step}] {link.node_id}  status={link.status}"
        )
        for k, v in link.detail.items():
            parts.append(f"    {k}: {v}")

    return "\n".join(parts)


def export_file_provenance_json(prov: FileProvenance) -> dict[str, Any]:
    """JSON-serialisable export."""
    return {
        "version": 1,
        "job_id": prov.job_id,
        "path": prov.path,
        "found": prov.found,
        "proof_status": prov.proof_status,
        "chain": [
            {
                "step": link.step,
                "node_type": link.node_type,
                "node_id": link.node_id,
                "status": link.status,
                "detail": link.detail,
            }
            for link in prov.chain
        ],
    }
