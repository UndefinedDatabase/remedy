"""
Builder bridge: BuilderOutput → parse → intent → approval → source_apply → test.

Connects the builder provider output to the structured patch pipeline.
Each step is gated: parse must succeed, intent must be approved, apply must
succeed before testing. Returns a BridgeResult with stage tracking.

Public API::

    run_builder_bridge(output, repo_path, *, job, data_dir, autonomy_level) -> BridgeResult
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

from packages.orchestration.builder_models import (
    BuilderOutput,
    BuilderPatchResult,
    parse_builder_patch,
)
from packages.orchestration.diff_repair import (
    changed_line_ranges_from_patch,
    select_repair_hunks,
)
from packages.orchestration.diff_repair_apply import apply_diff_repair
from packages.orchestration.diff_repair_response import (
    diff_repair_response_to_patch,
    parse_diff_repair_response,
)
from packages.orchestration.exec_guard import run_guarded_test_command

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
    "diff_repair_fell_back",
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
    # Which applicator ran: `diff` or `full_fallback` from `apply_diff_repair`.
    diff_repair_mode: str = ""        # "" when the round used no diff channel
    # The NAMED reason a diff attempt was discarded whole — empty when none was.
    diff_fallback_reason: str = ""


def run_builder_bridge(
    output: BuilderOutput,
    repo_path: Path,
    *,
    job: Any,
    data_dir: str | Path,
    autonomy_level: int = 2,
    diff_response: Any = None,
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

    result = BridgeResult()

    # Stage 1: Parse
    if diff_response is None:
        parse_result = parse_builder_patch(output)
    else:
        # `risk` and `requires_approval` keep their model defaults on purpose:
        # risk classification lives in the structured-patch parser, and Remedy
        # deliberately does not compute a second risk level on the diff channel
        # in v1.
        import hashlib

        raw = output.structured_patch_text or ""
        parse_result = BuilderPatchResult(
            parse_success=True,
            patch=diff_repair_response_to_patch(diff_response),
            target_paths=list(diff_response.files),
            output_hash=hashlib.sha256(raw.encode()).hexdigest()[:16],
            output_length=len(raw),
        )
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

    if diff_response is None:
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
    else:
        diff_result = apply_diff_repair(
            diff_response, repo_path,
            job=job, intent_id=intent_id, data_dir=data_dir,
        )
        result.diff_repair_mode = diff_result.mode
        result.diff_fallback_reason = diff_result.fallback_reason
        _emit(data_dir, job.id, "diff_repair_applied", {
            "mode": diff_result.mode,
            "applied": diff_result.applied,
            "fallback_reason": diff_result.fallback_reason,
            "files_modified": diff_result.files_modified,
            "rollback_incomplete": diff_result.rollback_incomplete,
            "error_count": len(diff_result.errors),
        })
        if not diff_result.applied:
            result.stage = "diff_fallback"
            result.stop_reason = "diff_repair_fell_back"
            return result
        result.apply_success = True
        result.stage = "applied"

    # Stage 4: Test (if autonomy >= 4)
    if autonomy_level >= 4:
        import subprocess

        test_cmd = _find_test_command(repo_path)
        if test_cmd:
            try:
                # Stage-1 guard, per DECISION F085 D3. `extra_env` SETS the one
                # variable this site used to overlay onto a copy of `os.environ`,
                # which the guard's allowlist scrub would otherwise drop. The 60 s
                # was already this call's wall and stays its wall: the guard's own
                # deadline replaces `subprocess.run`'s and still surfaces as
                # `TimeoutExpired`, so the handler below is unchanged. Streams come
                # back as BYTES rather than text, and only `returncode` is read here.
                proc = run_guarded_test_command(
                    test_cmd,
                    timeout_sec=60,
                    cwd=str(repo_path),
                    extra_env={"PYTHONDONTWRITEBYTECODE": "1"},
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


# The full-file DENOMINATOR for one repair round: what the old path would send.
def _repair_payload_chars(repo_root: Path, paths: list[str]) -> int:
    """Characters the FULL-FILE path would have sent for these paths.

    Unreadable and missing paths contribute nothing rather than raising:
    this number exists to be compared, and a measurement that can crash
    the repair loop is worse than one that undercounts a file it cannot
    read.
    """
    total = 0
    for rel in paths:
        try:
            total += len((repo_root / rel).read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError):
            continue
    return total


# The PROMPT-side hunk choice for one repair round: what the next prompt carries.
def _attach_diff_repair_hunks(
    repair_ctx: dict[str, Any],
    bridge_result: BridgeResult,
    repo_path: Path,
    *,
    margin_lines: int,
) -> dict[str, Any]:
    """Select margin-expanded hunks for the applied patch and carry them.

    Returns the round's evidence metadata and mutates ``repair_ctx`` only on
    the diff path: every full-file answer names the reason it took that path.
    """
    # Remedy deliberately does not report `full_fallback` here: `mode` is `diff`
    # or `full_file`, the PROMPT-side choice, while `full_fallback` is the
    # APPLY-side outcome `diff_repair_apply` names and the apply half wires.
    parse_result = bridge_result.parse_result
    patch = getattr(parse_result, "patch", None)
    if parse_result is None or not patch:
        return {"mode": "full_file", "reason": "no_patch"}

    ranges = changed_line_ranges_from_patch(patch)
    if not ranges:
        return {"mode": "full_file", "reason": "no_ranges"}

    selection = select_repair_hunks(repo_path, ranges, margin_lines=margin_lines)
    if not selection.hunks:
        return {
            "mode": "full_file",
            "reason": "no_hunks_selected",
            "omitted": [list(entry) for entry in selection.omitted],
        }

    repair_ctx["diff_hunks"] = [
        {
            "path": hunk.path,
            "start_line": hunk.start_line,
            "end_line": hunk.end_line,
            "text": hunk.text,
        }
        for hunk in selection.hunks
    ]
    repair_ctx["diff_hunks_omitted"] = [list(entry) for entry in selection.omitted]
    # Remedy deliberately does not put hunk TEXT in this metadata — counts only
    # (`hunk_count`, `total_chars`, `full_file_chars`, `omitted`) — because
    # `build_repair_context`'s contract is that its dict is safe to log; source
    # text belongs in the prompt.
    # The pair the saving is read from: `total_chars` is what the diff path SENT,
    # `full_file_chars` is what the full-file path WOULD have sent for the same
    # paths. Remedy deliberately does not record a derived `chars_saved` field —
    # a derived number can disagree with its own inputs, and the reader subtracts.
    # Per DECISION F111 D9 both are CHARACTERS, never tokens.
    return {
        "mode": "diff",
        "hunk_count": len(selection.hunks),
        "total_chars": selection.total_chars,
        "full_file_chars": _repair_payload_chars(repo_path, sorted(ranges)),
        "omitted": [list(entry) for entry in selection.omitted],
    }


def run_builder_bridge_loop(
    build_fn: Any,
    repo_path: Path,
    *,
    job: Any,
    data_dir: str | Path,
    autonomy_level: int = 4,
    max_cycles: int = 3,
    diff_mode: bool = True,
    diff_margin_lines: int = 3,
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

        diff_response = None
        if diff_mode and repair_ctx is not None and repair_ctx.get("repair_mode") == "diff":
            diff_response, decode_reason = parse_diff_repair_response(
                output.structured_patch_text or ""
            )
            if diff_response is None:
                _emit(data_dir, job.id, "diff_repair_not_used", {
                    "cycle": cycle, "reason": decode_reason,
                })

        # Run bridge
        bridge_result = run_builder_bridge(
            output, repo_path,
            job=job, data_dir=data_dir,
            autonomy_level=autonomy_level,
            diff_response=diff_response,
        )
        loop_result.final_result = bridge_result

        # A discarded diff attempt is not a dead end and not an applied patch, so
        # the round continues on the full-file path with the reason recorded, and
        # Remedy deliberately does not retry the SAME answer in full-file mode —
        # the answer was diff-shaped, so the next prompt has to ask for a full file.
        if bridge_result.stage == "diff_fallback":
            _emit(data_dir, job.id, "repair_round_fell_back_to_full_file", {
                "cycle": cycle,
                "reason": bridge_result.diff_fallback_reason,
            })
            if cycle < max_cycles:
                repair_ctx = build_repair_context(
                    job.id,
                    {"metadata": {"exit_code": 1, "passed": False, "cycle": cycle}},
                    load_run_events(data_dir, job.id),
                )
                repair_ctx["repair_mode"] = "full_file"
                repair_ctx["full_file_reason"] = bridge_result.diff_fallback_reason
                loop_result.repair_contexts.append(repair_ctx)
            continue

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

            if diff_mode:
                mode_meta = _attach_diff_repair_hunks(
                    repair_ctx, bridge_result, repo_path,
                    margin_lines=diff_margin_lines,
                )
            else:
                mode_meta = {"mode": "full_file", "reason": "diff_mode_off"}
            repair_ctx["repair_mode"] = mode_meta["mode"]
            _emit(data_dir, job.id, "repair_mode_selected", {"cycle": cycle, **mode_meta})

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
