"""
Builder bridge: BuilderOutput → parse → intent → approval → source_apply → test.

Connects the builder provider output to the structured patch pipeline.
Each step is gated: parse must succeed, intent must be approved, apply must
succeed before testing. Returns a BridgeResult with stage tracking.

Public API::

    run_builder_bridge(output, repo_path, *, job, data_dir, autonomy_level) -> BridgeResult
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

from packages.orchestration.builder_models import (
    BuilderOutput,
    BuilderPatchResult,
    parse_builder_patch,
)


STOP_REASONS = frozenset({
    "structured_patch_parse_failed",
    "provider_output_prose_only",
    "provider_output_malformed",
    "multiple_patch_blocks",
    "unsafe_path",
    "path_traversal",
    "missing_target_path",
    "malformed_diff",
    "stale_diff_context",
    "approval_required",
    "permission_denied",
    "source_apply_failed",
    "test_failed_after_apply",
    "repair_budget_exhausted",
    "repeated_patch_detected",
    "no_actionable_change",
    "provider_unavailable",
    "real_ollama_skipped",
    "unsafe_shell_command",
    "no_structured_patch_text",
    "validation_failed",
    "test_timeout",
    "parse_exception",
})


def _map_error_kind_to_stop_reason(error_kind: str) -> str:
    """Map parser error_kind to a canonical stop reason."""
    if error_kind in STOP_REASONS:
        return error_kind
    _MAP = {
        "prose_only": "provider_output_prose_only",
        "parse_exception": "provider_output_malformed",
    }
    return _MAP.get(error_kind, "structured_patch_parse_failed")


@dataclass
class BridgeResult:
    """Result of running the builder bridge pipeline."""
    stage: str = "init"
    stop_reason: str = ""
    parse_result: BuilderPatchResult | None = None
    intent_id: str = ""
    apply_success: bool = False
    test_passed: bool | None = None
    error: str = ""
    events: list[dict[str, Any]] = field(default_factory=list)


def run_builder_bridge(
    output: BuilderOutput,
    repo_path: Path,
    *,
    job: Any,
    data_dir: str | Path,
    autonomy_level: int = 2,
) -> BridgeResult:
    """Run the full builder bridge pipeline.

    Stages:
      1. Parse structured patch from BuilderOutput
      2. Create patch intent + auto-approve (fixture mode)
      3. Apply patch via source_apply
      4. Run tests (if autonomy >= 4)

    Returns BridgeResult with stage tracking and events.
    """
    from packages.orchestration.source_apply import apply_structured_patch
    from packages.orchestration.timeline import append_run_event

    result = BridgeResult()

    # Stage 1: Parse
    parse_result = parse_builder_patch(output)
    result.parse_result = parse_result

    stop_reason_for_parse = _map_error_kind_to_stop_reason(parse_result.error_kind) if not parse_result.parse_success else ""

    _emit(data_dir, job.id, "builder_patch_parsed", {
        "parse_success": parse_result.parse_success,
        "error_kind": parse_result.error_kind,
        "stop_reason": stop_reason_for_parse,
        "output_hash": parse_result.output_hash,
        "output_length": parse_result.output_length,
        "target_path_count": len(parse_result.target_paths),
    })

    if not parse_result.parse_success:
        result.stage = "parse_failed"
        result.stop_reason = stop_reason_for_parse
        result.error = parse_result.error_kind
        return result

    result.stage = "parsed"
    patch = parse_result.patch

    # Stage 2: Create intent + approval gate
    if autonomy_level < 3:
        result.stage = "approval_pending"
        result.stop_reason = "approval_required"
        return result

    intent_id = _create_and_approve_intent(job, parse_result)
    result.intent_id = intent_id
    result.stage = "approved"

    _emit(data_dir, job.id, "builder_bridge_intent_approved", {
        "intent_id": intent_id,
        "target_paths": parse_result.target_paths,
        "risk": parse_result.risk,
    })

    # Stage 3: Apply
    from packages.orchestration.permissions import Capability, set_permission
    set_permission(job, Capability.repo_generated_write, allow=True)

    apply_result = apply_structured_patch(
        patch, repo_path,
        data_dir=str(data_dir), job_id=job.id, job=job,
        intent_id=intent_id,
    )
    result.apply_success = apply_result.success

    if not apply_result.success:
        result.stage = "apply_failed"
        result.stop_reason = "source_apply_failed"
        result.error = "; ".join(apply_result.errors[:3])
        return result

    result.stage = "applied"

    # Stage 4: Test (if autonomy >= 4)
    if autonomy_level >= 4:
        import subprocess
        import sys

        test_cmd = _find_test_command(repo_path)
        if test_cmd:
            try:
                env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
                proc = subprocess.run(
                    test_cmd,
                    capture_output=True, text=True, timeout=60,
                    cwd=str(repo_path),
                    env=env,
                )
                passed = proc.returncode == 0
                result.test_passed = passed
                result.stage = "tested"

                _emit(data_dir, job.id, "builder_bridge_test_completed", {
                    "exit_code": proc.returncode,
                    "passed": passed,
                })

                if passed:
                    import hashlib
                    proof_hash = hashlib.sha256(
                        (output.structured_patch_text or "").encode()
                    ).hexdigest()[:16]
                    _emit(data_dir, job.id, "proof_collected", {
                        "content_hash": proof_hash,
                        "source": "builder_bridge",
                        "test_passed": True,
                    })
                    result.stage = "proof_collected"
                else:
                    result.stop_reason = "test_failed_after_apply"
            except (subprocess.TimeoutExpired, OSError):
                result.test_passed = False
                result.stage = "test_timeout"
                result.stop_reason = "test_timeout"

    return result


def _create_and_approve_intent(job: Any, parse_result: BuilderPatchResult) -> str:
    """Create a patch intent from parse result and approve it."""
    from packages.core.models import Artifact
    from packages.orchestration.approval_queue import (
        APPROVAL_APPROVED,
        make_intent_id,
        set_approval_state,
    )

    explanations = []
    for path in parse_result.target_paths:
        explanations.append({
            "file": path,
            "action": "modify",
            "risk": parse_result.risk,
            "reason": "builder bridge auto-approve",
            "summary": f"Structured patch for {path}",
        })

    artifact = Artifact(
        task_id=uuid4(),
        name="builder-bridge-intent",
        content="",
    )
    artifact.metadata = {
        "patch_intent_explanations": explanations,
        "output_hash": parse_result.output_hash,
    }
    job.artifacts.append(artifact)

    intent_id = make_intent_id(artifact.id, 0)
    set_approval_state(
        job, intent_id, APPROVAL_APPROVED,
        reason="builder bridge auto-approve",
        decided_by="builder_bridge",
    )
    return intent_id


def _find_test_command(repo_path: Path) -> list[str] | None:
    """Find test command for the repo."""
    import sys

    if (repo_path / "Makefile").is_file():
        return ["make", "test"]
    if (repo_path / "pyproject.toml").is_file() or (repo_path / "tests").is_dir():
        return [sys.executable, "-m", "pytest", "-x", "-q", "--tb=short", "--no-header"]
    return None


@dataclass
class LoopResult:
    """Result of running the bounded repair loop."""
    cycles_run: int = 0
    max_cycles: int = 3
    final_result: BridgeResult | None = None
    repair_contexts: list[dict[str, Any]] = field(default_factory=list)
    success: bool = False
    stop_reason: str = ""


def run_builder_bridge_loop(
    build_fn: Any,
    repo_path: Path,
    *,
    job: Any,
    data_dir: str | Path,
    autonomy_level: int = 4,
    max_cycles: int = 3,
) -> LoopResult:
    """Run bounded repair loop: build → bridge → test → repair → rebuild.

    build_fn: callable(repair_context: dict | None) -> BuilderOutput
        Called each cycle. First call gets None, subsequent calls get repair context.

    Stops when:
      - Tests pass (success)
      - max_cycles reached
      - Parse or apply fails (no point retrying same output)
    """
    import hashlib

    from packages.orchestration.repair_context import build_repair_context
    from packages.orchestration.timeline import load_run_events

    loop_result = LoopResult(max_cycles=max_cycles)
    repair_ctx: dict[str, Any] | None = None
    seen_patch_hashes: set[str] = set()

    for cycle in range(1, max_cycles + 1):
        loop_result.cycles_run = cycle

        # Build
        output = build_fn(repair_ctx)

        # Detect repeated patch
        patch_text = output.structured_patch_text or ""
        patch_hash = hashlib.sha256(patch_text.encode()).hexdigest()[:16]
        if patch_hash in seen_patch_hashes and patch_text:
            loop_result.stop_reason = "repeated_patch_detected"
            _emit(data_dir, job.id, "repair_loop_stopped", {
                "cycle": cycle,
                "reason": "repeated_patch_detected",
                "patch_hash": patch_hash,
            })
            break
        if patch_text:
            seen_patch_hashes.add(patch_hash)

        _emit(data_dir, job.id, "repair_loop_cycle_started", {
            "cycle": cycle,
            "max_cycles": max_cycles,
            "has_repair_context": repair_ctx is not None,
            "patch_hash": patch_hash,
        })

        # Run bridge
        bridge_result = run_builder_bridge(
            output, repo_path,
            job=job, data_dir=data_dir,
            autonomy_level=autonomy_level,
        )
        loop_result.final_result = bridge_result

        # Check outcomes
        if bridge_result.stage in ("parse_failed", "apply_failed"):
            loop_result.stop_reason = bridge_result.stop_reason or bridge_result.stage
            _emit(data_dir, job.id, "repair_loop_stopped", {
                "cycle": cycle,
                "reason": bridge_result.stop_reason or bridge_result.stage,
                "error": bridge_result.error,
            })
            break

        if bridge_result.test_passed is True:
            loop_result.success = True
            _emit(data_dir, job.id, "repair_loop_succeeded", {
                "cycle": cycle,
            })
            break

        if bridge_result.test_passed is False and cycle < max_cycles:
            # Build repair context for next cycle
            events = load_run_events(data_dir, job.id)
            test_event = {"metadata": {"exit_code": 1, "passed": False, "cycle": cycle}}
            repair_ctx = build_repair_context(job.id, test_event, events)
            loop_result.repair_contexts.append(repair_ctx)

            _emit(data_dir, job.id, "repair_context_created", {
                "cycle": cycle,
                "failure_kind": repair_ctx.get("failure_kind", "unknown"),
            })

    # Budget exhaustion
    if not loop_result.success and not loop_result.stop_reason:
        loop_result.stop_reason = "repair_budget_exhausted"

    return loop_result


def _emit(data_dir: str | Path, job_id: UUID, event: str, metadata: dict[str, Any]) -> None:
    from packages.orchestration.timeline import append_run_event
    append_run_event(data_dir, job_id, event=event, metadata=metadata)
