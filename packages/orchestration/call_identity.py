"""F012 — the exact provider-transport input fingerprint, and stable call identity.

Two things live here, kept in a tiny dependency-light module so the providers, the ping-pong
loop and the run-manifest builder can all share them without an import cycle.

1. ``PreparedCallInput`` — the fingerprint of the EXACT request a provider transport received.
   The reviewed build hashed ``reviewer_effective`` in the loop, BEFORE the provider appended
   its schema / rewrote the prompt, so the recorded hash did not match what was actually sent.
   Now each provider computes this at the moment it constructs the real request (the prompt
   bytes it will transmit, the out-of-band native schema, the model, the mode and the material
   options), so the recorded fingerprint IS the sent request by construction.

2. ``CallIdentity`` — the stable, collision-free identity of one finalized logical call:
   ``(job_id, task_id, run_id, sequence, role, round, kind, call_id)``. The reviewed
   ``FinalizedCall`` keyed only on ``(round, role, kind)``, so a two-task job produced
   duplicate keys and the diff collapsed them. Every field needed to keep two same-role,
   same-round calls distinct is here.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_text(text: str) -> str:
    return _sha((text or "").encode("utf-8"))


@dataclass(frozen=True)
class PreparedCallInput:
    """The fingerprint of the exact request handed to a provider transport.

    ``fingerprint`` is the single identity used by the manifest; it is a hash over every
    material component, so two requests that differ in prompt bytes, schema, model, mode OR
    a material option have different fingerprints.
    """

    prompt_sha256: str
    prompt_len_bytes: int       # F9: the EXACT UTF-8 byte count that prompt_sha256 hashes
    schema_sha256: str          # native out-of-band schema hash, or "" when none
    model: str
    mode: str                   # api-structured | api-legacy | cli-native | cli-legacy | fake
    options_sha256: str         # hash of material options (max_tokens, write_mode, …)
    fingerprint: str

    def to_json(self) -> dict[str, Any]:
        return {
            "prompt_sha256": self.prompt_sha256,
            "prompt_len_bytes": self.prompt_len_bytes,
            "schema_sha256": self.schema_sha256,
            "model": self.model,
            "mode": self.mode,
            "options_sha256": self.options_sha256,
            "fingerprint": self.fingerprint,
        }

    @classmethod
    def from_trusted_json(cls, d: dict[str, Any]) -> "PreparedCallInput":
        """F14: TRUSTED, in-memory canonical data ONLY. Never call this on bytes read back from
        disk — untrusted records go through ``run_manifest.decode_prepared_call_input_v1``."""
        return cls(
            prompt_sha256=str(d.get("prompt_sha256", "")),
            prompt_len_bytes=int(d.get("prompt_len_bytes", 0) or 0),
            schema_sha256=str(d.get("schema_sha256", "")),
            model=str(d.get("model", "")),
            mode=str(d.get("mode", "")),
            options_sha256=str(d.get("options_sha256", "")),
            fingerprint=str(d.get("fingerprint", "")),
        )


def prepare_call_input(*, prompt: str, model: str, mode: str, schema: str = "",
                       options: dict[str, Any] | None = None) -> PreparedCallInput:
    """Build a ``PreparedCallInput`` from the EXACT transport request components.

    Call this where the real request is assembled — the ``prompt`` must be the exact bytes
    sent, and ``schema`` the exact out-of-band schema string (empty when the schema is already
    inside ``prompt`` or unused). ``options`` are the material knobs that change the request.
    """
    prompt_bytes = (prompt or "").encode("utf-8")
    prompt_sha = _sha(prompt_bytes)
    # F9: the recorded length is the EXACT UTF-8 byte count of the bytes prompt_sha256 hashes —
    # not a Python character count — and it is BOUND INTO the fingerprint, so tampering with it
    # invalidates the fingerprint instead of sitting there authoritative but unbound.
    prompt_len_bytes = len(prompt_bytes)
    schema_sha = sha_text(schema) if schema else ""
    opts = options or {}
    options_sha = _sha(json.dumps(opts, sort_keys=True, ensure_ascii=False).encode("utf-8"))
    fingerprint = _sha(
        json.dumps({
            "prompt_sha256": prompt_sha,
            "prompt_len_bytes": prompt_len_bytes,
            "schema_sha256": schema_sha,
            "model": model,
            "mode": mode,
            "options_sha256": options_sha,
        }, sort_keys=True, ensure_ascii=False).encode("utf-8"))
    return PreparedCallInput(
        prompt_sha256=prompt_sha,
        prompt_len_bytes=prompt_len_bytes,
        schema_sha256=schema_sha,
        model=model,
        mode=mode,
        options_sha256=options_sha,
        fingerprint=fingerprint,
    )


@dataclass(frozen=True)
class CallIdentity:
    """The collision-free identity of one finalized logical provider call."""

    job_id: str
    task_id: str
    run_id: str
    sequence: int              # job-wide monotonic order of finalized calls
    role: str                  # builder | reviewer
    round: int
    kind: str                  # attempt | parse-retry
    call_id: str               # provider/run call id (stream_call_id when streaming)
    episode_id: str = ""       # F4: the execution episode that OWNS this call

    def key(self) -> tuple:
        """The PROVENANCE key: guaranteed unique per recorded call, including the execution
        identifiers. Used for record uniqueness and Evidence provenance — NEVER as the
        input-comparison key (two identical runs legitimately differ here)."""
        return (self.episode_id, self.task_id, self.run_id, self.sequence, self.role,
                self.round, self.kind, self.call_id)

    def logical_key(self) -> tuple:
        """F1: the STABLE LOGICAL key — what makes two calls "the same call" across two
        separate executions of the same inputs. It deliberately excludes every random /
        execution-scoped identifier (job id, episode id, run id, provider-generated call id):
        those are provenance, not input. Two runs given the same inputs produce the same
        logical keys in the same order."""
        return (self.task_id, self.sequence, self.role, self.round, self.kind)

    def to_json(self) -> dict[str, Any]:
        return {
            "job_id": self.job_id,
            "task_id": self.task_id,
            "run_id": self.run_id,
            "sequence": self.sequence,
            "role": self.role,
            "round": self.round,
            "kind": self.kind,
            "call_id": self.call_id,
            "episode_id": self.episode_id,
        }

    @classmethod
    def from_trusted_json(cls, d: dict[str, Any]) -> "CallIdentity":
        """F14: TRUSTED in-memory data ONLY — untrusted records use
        ``run_manifest.decode_call_identity_v1``."""
        return cls(
            job_id=str(d.get("job_id", "")),
            task_id=str(d.get("task_id", "")),
            run_id=str(d.get("run_id", "")),
            sequence=int(d.get("sequence", 0) or 0),
            role=str(d.get("role", "")),
            round=int(d.get("round", 0) or 0),
            kind=str(d.get("kind", "")),
            call_id=str(d.get("call_id", "")),
            episode_id=str(d.get("episode_id", "")),
        )
