"""
Builder models: execution context and output.

These models live in orchestration/ (not in providers/) because orchestration
imports and transforms them — providers depend on these, not the other way around.
"""

from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class TaskExecutionContext(BaseModel):
    """Context provided to a builder provider for a single task execution.

    Contains all information the builder needs to produce meaningful output.
    Built by run_next_task() from the current job and task state — the provider
    receives this object and must not mutate the Job directly.

    job_id:               UUID of the job containing the task.
    job_prompt:           User prompt from the job (may be None).
    task_id:              UUID of the task to execute.
    task_type:            snake_case type identifier for the task.
    task_description:     Human-readable description of what the task should accomplish.
    planning_summary:     Summary from the planning artifact, if available.
    prior_task_summaries: Summaries from already-completed task artifacts, in order.
    memory_context:       Optional compact text from approved project memory (no raw content).
    memory_metadata:      Safe metadata about memory injection (counts, hash, no raw text).
    """

    job_id: UUID
    job_prompt: str | None
    task_id: UUID
    task_type: str
    task_description: str
    planning_summary: str | None = None
    prior_task_summaries: list[str] = []
    memory_context: str | None = None
    memory_metadata: dict = Field(default_factory=dict)


class BuilderOutput(BaseModel):
    """Structured execution result returned by a builder provider.

    summary:          short overview of what was done or planned for this task.
    proposed_changes: list of concrete changes or actions taken/proposed.
    notes:            optional assumptions, observations, or clarifications.
    risks:            optional list of potential issues or concerns.
    structured_patch_text: raw structured patch output from provider (JSON or diff).
    structured_patch_format: format hint ("json", "unified_diff", "none").
    """

    summary: str
    proposed_changes: list[str] = Field(min_length=1)
    notes: list[str] = []
    risks: list[str] = []
    structured_patch_text: str | None = None
    structured_patch_format: str = "none"


class BuilderPatchResult(BaseModel):
    """Result of parsing a BuilderOutput's structured patch text.

    parse_success:      whether the text was parsed into a valid StructuredPatch.
    patch:              the parsed StructuredPatch (None if parse failed).
    error_kind:         short error category if parse failed.
    target_paths:       paths affected by the patch.
    risk:               risk level from parsed patch.
    requires_approval:  whether approval is needed.
    output_hash:        hash of structured_patch_text (safe metadata).
    output_length:      length of structured_patch_text.
    diagnostics:        short diagnostic messages (no raw provider output).
    """

    parse_success: bool
    patch: Any = None  # StructuredPatch when parse_success is True
    error_kind: str = ""
    target_paths: list[str] = []
    risk: str = "low"
    requires_approval: bool = True
    output_hash: str = ""
    output_length: int = 0
    diagnostics: list[str] = []


def parse_builder_patch(output: BuilderOutput) -> BuilderPatchResult:
    """Parse structured patch from BuilderOutput.

    Returns safe result with no raw provider output in diagnostics.
    """
    import hashlib

    from packages.orchestration.structured_patch import (
        parse_structured_patch,
        validate_structured_patch,
    )

    text = output.structured_patch_text
    if not text:
        return BuilderPatchResult(
            parse_success=False,
            error_kind="no_structured_patch_text",
        )

    output_hash = hashlib.sha256(text.encode()).hexdigest()[:16]
    output_length = len(text)

    # Reject raw shell commands pretending to be patch
    _SHELL_PATTERNS = ("rm -rf", "sudo ", "curl | sh", "wget ", "chmod 777")
    text_lower = text.lower()
    for pat in _SHELL_PATTERNS:
        if pat in text_lower:
            return BuilderPatchResult(
                parse_success=False,
                error_kind="unsafe_shell_command",
                output_hash=output_hash,
                output_length=output_length,
                diagnostics=[f"Rejected: contains shell pattern '{pat}'"],
            )

    try:
        patch = parse_structured_patch(text)
    except Exception:
        return BuilderPatchResult(
            parse_success=False,
            error_kind="parse_exception",
            output_hash=output_hash,
            output_length=output_length,
            diagnostics=["Exception during parse (details redacted)"],
        )

    # Check if it's just prose (markdown fallback)
    if patch.intent_kind == "markdown":
        return BuilderPatchResult(
            parse_success=False,
            error_kind="prose_only",
            output_hash=output_hash,
            output_length=output_length,
            diagnostics=["Output is narrative only, not a structured patch"],
        )

    # Validate the parsed patch
    issues = validate_structured_patch(patch)
    if issues:
        return BuilderPatchResult(
            parse_success=False,
            error_kind="validation_failed",
            output_hash=output_hash,
            output_length=output_length,
            target_paths=list(patch.target_paths),
            diagnostics=issues[:5],  # Bounded
        )

    return BuilderPatchResult(
        parse_success=True,
        patch=patch,
        target_paths=list(patch.target_paths),
        risk=patch.risk,
        requires_approval=patch.requires_approval,
        output_hash=output_hash,
        output_length=output_length,
    )
