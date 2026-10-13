"""F306 T007, R-1235's second step — the execution configuration and its two serializers, split
out of ``pingpong_job``. This module holds the durable ``ExecutionConfig`` dataclass and its
export/import pair, ``_export_execution_config`` and ``_import_execution_config``;
``pingpong_job.py`` re-exports all three by name, so every ``pingpong_job.<name>`` caller keeps
working unchanged.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ExecutionConfig:
    """Durable execution config for job continuation."""
    builder: str = "fake"
    builder_source: str = "default"
    reviewer: str = "fake"
    reviewer_source: str = "default"
    builder_model: str = ""
    builder_model_source: str = "default"
    builder_effort: str = ""
    builder_effort_source: str = "default"
    reviewer_model: str = ""
    reviewer_model_source: str = "default"
    reviewer_effort: str = ""
    reviewer_effort_source: str = "default"
    repair_provider: str = ""
    repair_provider_source: str = "default"
    repair_model: str = ""
    repair_model_source: str = "default"
    repair_effort: str = ""
    repair_effort_source: str = "default"
    max_rounds: int = 3
    max_rounds_source: str = "default"
    repair_rounds_allowed: int = 2
    repair_rounds_source: str = "default"
    test_command: str = ""
    test_command_source: str = "default"
    claude_cli_write_mode: str = "none"
    claude_cli_write_mode_source: str = "default"
    context_strategy: str = "task_bounded_sequential_job"
    # F012 round 4 (F2): invocation-level controls that alter execution/evidence. Material
    # inputs, persisted with their source so `explicit > persisted > default` is auditable.
    timeout_sec: int = 120
    timeout_sec_source: str = "default"
    timeout_profile: str = ""
    timeout_profile_source: str = "default"
    max_output_chars: int = 50000
    max_output_chars_source: str = "default"
    stream_evidence: bool = False
    stream_evidence_source: str = "default"
    max_tasks: int = 0
    max_tasks_source: str = "default"


def _export_execution_config(c: ExecutionConfig | None) -> dict[str, Any] | None:
    if c is None:
        return None
    return {
        "builder": c.builder,
        "builder_source": c.builder_source,
        "reviewer": c.reviewer,
        "reviewer_source": c.reviewer_source,
        "builder_model": c.builder_model,
        "builder_model_source": c.builder_model_source,
        "builder_effort": c.builder_effort,
        "builder_effort_source": c.builder_effort_source,
        "reviewer_model": c.reviewer_model,
        "reviewer_model_source": c.reviewer_model_source,
        "reviewer_effort": c.reviewer_effort,
        "reviewer_effort_source": c.reviewer_effort_source,
        "repair_provider": c.repair_provider,
        "repair_provider_source": c.repair_provider_source,
        "repair_model": c.repair_model,
        "repair_model_source": c.repair_model_source,
        "repair_effort": c.repair_effort,
        "repair_effort_source": c.repair_effort_source,
        "max_rounds": c.max_rounds,
        "max_rounds_source": c.max_rounds_source,
        "repair_rounds_allowed": c.repair_rounds_allowed,
        "repair_rounds_source": c.repair_rounds_source,
        "test_command": c.test_command,
        "test_command_present": bool(c.test_command),
        "test_command_source": c.test_command_source,
        "claude_cli_write_mode": c.claude_cli_write_mode,
        "claude_cli_write_mode_source": c.claude_cli_write_mode_source,
        "context_strategy": c.context_strategy,
        "timeout_sec": c.timeout_sec,
        "timeout_sec_source": c.timeout_sec_source,
        "timeout_profile": c.timeout_profile,
        "timeout_profile_source": c.timeout_profile_source,
        "max_output_chars": c.max_output_chars,
        "max_output_chars_source": c.max_output_chars_source,
        "stream_evidence": c.stream_evidence,
        "stream_evidence_source": c.stream_evidence_source,
        "max_tasks": c.max_tasks,
        "max_tasks_source": c.max_tasks_source,
    }


def _import_execution_config(d: dict[str, Any] | None) -> ExecutionConfig | None:
    if d is None:
        return None
    return ExecutionConfig(
        builder=d.get("builder", "fake"),
        builder_source=d.get("builder_source", "default"),
        reviewer=d.get("reviewer", "fake"),
        reviewer_source=d.get("reviewer_source", "default"),
        builder_model=d.get("builder_model", ""),
        builder_model_source=d.get("builder_model_source", "default"),
        builder_effort=d.get("builder_effort", ""),
        builder_effort_source=d.get("builder_effort_source", "default"),
        reviewer_model=d.get("reviewer_model", ""),
        reviewer_model_source=d.get("reviewer_model_source", "default"),
        reviewer_effort=d.get("reviewer_effort", ""),
        reviewer_effort_source=d.get("reviewer_effort_source", "default"),
        repair_provider=d.get("repair_provider", ""),
        repair_provider_source=d.get("repair_provider_source", "default"),
        repair_model=d.get("repair_model", ""),
        repair_model_source=d.get("repair_model_source", "default"),
        repair_effort=d.get("repair_effort", ""),
        repair_effort_source=d.get("repair_effort_source", "default"),
        max_rounds=d.get("max_rounds", 3),
        max_rounds_source=d.get("max_rounds_source", "default"),
        repair_rounds_allowed=d.get("repair_rounds_allowed", 2),
        repair_rounds_source=d.get("repair_rounds_source", "default"),
        test_command=d.get("test_command", ""),
        test_command_source=d.get("test_command_source", "default"),
        claude_cli_write_mode=d.get("claude_cli_write_mode", "none"),
        claude_cli_write_mode_source=d.get("claude_cli_write_mode_source", "default"),
        context_strategy=d.get("context_strategy", "task_bounded_sequential_job"),
        timeout_sec=int(d.get("timeout_sec", 120) or 120),
        timeout_sec_source=d.get("timeout_sec_source", "default"),
        timeout_profile=d.get("timeout_profile", ""),
        timeout_profile_source=d.get("timeout_profile_source", "default"),
        max_output_chars=int(d.get("max_output_chars", 50000) or 50000),
        max_output_chars_source=d.get("max_output_chars_source", "default"),
        stream_evidence=bool(d.get("stream_evidence", False)),
        stream_evidence_source=d.get("stream_evidence_source", "default"),
        max_tasks=int(d.get("max_tasks", 0) or 0),
        max_tasks_source=d.get("max_tasks_source", "default"),
    )
