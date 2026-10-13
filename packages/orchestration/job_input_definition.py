"""F306 T006, R-1235's first step — the job-input definition, its builder and its field sets,
split out of ``run_manifest``.

This module holds: the Redaction-section helpers the builder needs (``is_secret_key``,
``_safe_scalar`` and their ``_SECRET_TERMS`` vocabulary), the identity hasher ``_h`` and
``_redacted_command_identity``, the builder itself (``build_job_input_definition``) and its
byte/hash helpers (``job_input_definition_bytes``, ``job_input_definition_sha256``,
``job_input_sha256``), and the EXACT JobInputDefinitionV1 field-set constants
(``JOB_INPUT_TOP_FIELDS``, ``JOB_INPUT_TASK_FIELDS``, ``JOB_INPUT_EXECUTION_STR_FIELDS``,
``JOB_INPUT_EXECUTION_INT_FIELDS``, ``JOB_INPUT_EXECUTION_BOOL_FIELDS``, ``_JOB_INPUT_SOURCE_OF``,
``_source_field``, ``JOB_INPUT_EXECUTION_FIELDS``). ``run_manifest.py`` re-exports every one of
these by name, so every ``run_manifest.<name>`` caller keeps working unchanged. This is the first
step toward the repair R-1235's own finding text names; ``validate_job_input_definition`` and
``decode_job_input_definition_v1`` stay on ``run_manifest``, because the validator calls
``_is_hex64``, ``_safe_component``, ``VALID_ISOLATION_MODES``, ``_contains_secret`` and
``_contains_local_path`` — shared helpers every other validator on that module uses too, and
which tests replace directly on ``run_manifest`` — which this module must never import.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any

_SECRET_TERMS = ("token", "key", "secret", "password", "credential")


def is_secret_key(key: str) -> bool:
    low = str(key or "").lower()
    return any(term in low for term in _SECRET_TERMS)


def _safe_scalar(value: Any) -> Any:
    from packages.orchestration.failure_postmortem import safe_text

    return safe_text(value) if isinstance(value, str) else value


def _h(text: str) -> str:
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()


def _redacted_command_identity(command: str) -> dict[str, Any]:
    """A test/CLI command can carry a secret (a token in an env-style arg). Keep a
    deterministic identity that still moves when the command changes, without serializing
    the secret: the redacted text plus a hash of the RAW command."""
    return {"redacted": _safe_scalar(command or ""), "sha256": _h(command or "")}


def build_job_input_definition(job: Any) -> dict[str, Any]:
    """The COMPLETE typed job-input definition (F1): every persisted input that can change
    which work runs, how many calls run, what prompts are assembled, what tests run, or what
    provider options are used. A single opaque job-file hash is NOT enough."""
    ec = getattr(job, "execution_config", None)

    def _g(name: str, default: Any = "") -> Any:
        if ec is not None:
            return getattr(ec, name, default)
        # A job that has not run yet carries no resolved execution config: every value IS the
        # product default, so every SOURCE is "default". Recording an empty source instead would
        # make a planning-only job's own definition invalid — and the contract says a
        # planning-only job (zero calls) has a valid manifest (T0_F012).
        if name.endswith("_source"):
            return "default"
        return default

    tasks = []
    for idx, t in enumerate(getattr(job, "tasks", [])):
        tasks.append({
            "order": idx,
            "task_id": t.task_id,
            "source_heading_number": getattr(t, "source_heading_number", 0),
            "title_sha256": _h(getattr(t, "title", "") or ""),
            "body_sha256": _h(getattr(t, "body", "") or ""),
            "acceptance_sha256": _h(getattr(t, "acceptance", "") or ""),
        })

    execution = {
        "builder": _g("builder"), "builder_source": _g("builder_source"),
        "builder_model": _g("builder_model"), "builder_model_source": _g("builder_model_source"),
        "builder_effort": _g("builder_effort"), "builder_effort_source": _g("builder_effort_source"),
        "reviewer": _g("reviewer"), "reviewer_source": _g("reviewer_source"),
        "reviewer_model": _g("reviewer_model"), "reviewer_model_source": _g("reviewer_model_source"),
        "reviewer_effort": _g("reviewer_effort"), "reviewer_effort_source": _g("reviewer_effort_source"),
        "repair_provider": _g("repair_provider"), "repair_provider_source": _g("repair_provider_source"),
        "repair_model": _g("repair_model"), "repair_model_source": _g("repair_model_source"),
        "repair_effort": _g("repair_effort"), "repair_effort_source": _g("repair_effort_source"),
        "max_rounds": _g("max_rounds", 0), "max_rounds_source": _g("max_rounds_source"),
        "repair_rounds_allowed": _g("repair_rounds_allowed", 0),
        "repair_rounds_source": _g("repair_rounds_source"),
        "test_command": _redacted_command_identity(_g("test_command")),
        "test_command_source": _g("test_command_source"),
        "claude_cli_write_mode": _g("claude_cli_write_mode"),
        "claude_cli_write_mode_source": _g("claude_cli_write_mode_source"),
        "context_strategy": _g("context_strategy"),
        # F2 invocation controls — material inputs, hashed with their source.
        "timeout_sec": _g("timeout_sec", 0), "timeout_sec_source": _g("timeout_sec_source"),
        "timeout_profile": _g("timeout_profile"),
        "timeout_profile_source": _g("timeout_profile_source"),
        "max_output_chars": _g("max_output_chars", 0),
        "max_output_chars_source": _g("max_output_chars_source"),
        "stream_evidence": bool(_g("stream_evidence", False)),
        "stream_evidence_source": _g("stream_evidence_source"),
        "max_tasks": _g("max_tasks", 0), "max_tasks_source": _g("max_tasks_source"),
    }
    return {
        "job_input_v": 1,
        "job_title_sha256": _h(getattr(job, "job_title", "") or ""),
        "job_file_sha256": str(getattr(job, "job_file_sha256", "") or ""),
        "isolation_mode": str(getattr(job, "isolation_mode", "") or ""),
        "tasks": tasks,
        "execution": execution,
    }


def job_input_definition_bytes(definition: dict[str, Any]) -> bytes:
    """F6: THE canonical byte encoding of a JobInputDefinition. Every producer and every
    verifier hashes exactly these bytes — capture, manifest construction, validation, the
    current candidate, the diff, recovery and export."""
    return json.dumps(definition, sort_keys=True, ensure_ascii=False).encode("utf-8")


def job_input_definition_sha256(definition: dict[str, Any]) -> str:
    """F6: the ONE canonical hash helper. ``manifest.job_input_sha256`` MUST equal this over the
    manifest's own EMBEDDED ``snapshot.job_input`` — so the recorded hash cannot drift from the
    definition it claims to identify."""
    return hashlib.sha256(job_input_definition_bytes(definition)).hexdigest()


def job_input_sha256(job: Any, models: dict[str, str] | None = None) -> str:
    """The identity of the COMPLETE job-input definition. ``models`` is accepted for
    backward compatibility but is now derived from the definition itself."""
    return job_input_definition_sha256(build_job_input_definition(job))


#: F7: the EXACT JobInputDefinitionV1 schema.
JOB_INPUT_TOP_FIELDS = frozenset({"job_input_v", "job_title_sha256", "job_file_sha256",
                                  "isolation_mode", "tasks", "execution"})
JOB_INPUT_TASK_FIELDS = frozenset({"order", "task_id", "source_heading_number",
                                   "title_sha256", "body_sha256", "acceptance_sha256"})
#: The EXACT material execution field set. Every value has a paired ``_source``. This list and
#: ``ExecutionConfig``'s dataclass fields are kept in lockstep by a guard test, so a future
#: material field cannot be added without updating F012's hashed definition.
JOB_INPUT_EXECUTION_STR_FIELDS = (
    "builder", "builder_model", "builder_effort",
    "reviewer", "reviewer_model", "reviewer_effort",
    "repair_provider", "repair_model", "repair_effort",
    "claude_cli_write_mode", "timeout_profile",
)
JOB_INPUT_EXECUTION_INT_FIELDS = ("max_rounds", "repair_rounds_allowed", "timeout_sec",
                                  "max_output_chars", "max_tasks")
JOB_INPUT_EXECUTION_BOOL_FIELDS = ("stream_evidence",)
#: ``repair_rounds_allowed`` pairs with ``repair_rounds_source`` — not ``*_allowed_source``.
_JOB_INPUT_SOURCE_OF = {"repair_rounds_allowed": "repair_rounds_source"}


def _source_field(name: str) -> str:
    return _JOB_INPUT_SOURCE_OF.get(name, f"{name}_source")


JOB_INPUT_EXECUTION_FIELDS = frozenset(
    list(JOB_INPUT_EXECUTION_STR_FIELDS) + list(JOB_INPUT_EXECUTION_INT_FIELDS)
    + list(JOB_INPUT_EXECUTION_BOOL_FIELDS)
    + [_source_field(f) for f in JOB_INPUT_EXECUTION_STR_FIELDS]
    + [_source_field(f) for f in JOB_INPUT_EXECUTION_INT_FIELDS]
    + [_source_field(f) for f in JOB_INPUT_EXECUTION_BOOL_FIELDS]
    + ["test_command", "test_command_source", "context_strategy"])
