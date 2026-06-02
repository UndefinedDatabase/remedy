"""
Autorun v1 — controlled execution loop for ``remedy do``.

Runs a goal-driven loop: create job, inject source context,
run builder, create patch intent, gate approval, apply, test.

Autonomy levels:
  0 — observe:   dry-run, show plan only
  1 — propose:   create job + task, no execution
  2 — generate:  run builder, create patch intent (needs approval)
  3 — apply:     apply approved patches only
  4 — test:      run tests after apply if permission exists
  5 — revert:    revert failed applies
  6 — loop:      limited repair loop (re-propose after failure)
  7 — blocked:   future / not implemented

Public API::

    run_autorun(goal, repo_path, ...) -> AutorunResult
    dry_run_autorun(goal, repo_path, ...) -> dict
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4


@dataclass
class AutorunResult:
    """Result of an autorun execution."""
    job_id: str
    cycles_run: int
    stage: str
    events: list[dict[str, str]] = field(default_factory=list)
    ui_url: str = ""
    error: str = ""
    stop_reason: str = ""
    provider: str = ""


def dry_run_autorun(
    goal: str,
    repo_path: str,
    *,
    project_id: str | None = None,
    autonomy_level: int = 2,
    max_cycles: int = 3,
    enable_ui: bool = False,
) -> dict[str, Any]:
    """Dry run — no LLM, no repo mutation. Shows what would happen."""
    from packages.orchestration.data_paths import resolve_data_root

    repo = Path(repo_path).resolve()
    repo_exists = repo.is_dir()

    # Check for manifests
    manifests = []
    if repo_exists:
        for name in ("package.json", "pyproject.toml", "Cargo.toml", "go.mod", "Makefile"):
            if (repo / name).is_file():
                manifests.append(name)

    # Token budget estimate
    token_budget = 2000
    if autonomy_level >= 2:
        token_budget = 4000

    plan = {
        "version": 1,
        "dry_run": True,
        "goal": goal,
        "repo_path": str(repo),
        "repo_exists": repo_exists,
        "project_id": project_id,
        "autonomy_level": autonomy_level,
        "autonomy_label": _autonomy_label(autonomy_level),
        "max_cycles": max_cycles,
        "manifests_found": manifests,
        "phases": [],
        "token_budget": token_budget,
        "ui_plan": {
            "enabled": enable_ui,
            "url_template": "http://127.0.0.1:8787/?job=<job_id>&token=<token>",
        },
        "gates": [],
    }

    # Phases based on autonomy
    phases = ["create_project", "create_job", "attach_repo"]
    if autonomy_level >= 1:
        phases.append("source_context_injection")
    if autonomy_level >= 2:
        phases.extend(["run_builder", "create_patch_intent"])
    if autonomy_level >= 3:
        phases.extend(["approval_gate", "apply_patch"])
    if autonomy_level >= 4:
        phases.append("run_tests")
    if autonomy_level >= 5:
        phases.append("revert_on_failure")
    if autonomy_level >= 6:
        phases.append("repair_loop")
    plan["phases"] = phases

    # Gates
    if autonomy_level >= 2:
        plan["gates"].append({"gate": "approval", "description": "Human must approve patch before apply"})
    if autonomy_level >= 4:
        plan["gates"].append({"gate": "test_permission", "description": "test_execution permission required"})

    return plan


def run_autorun(
    goal: str,
    repo_path: str,
    *,
    project_id: str | None = None,
    autonomy_level: int = 2,
    max_cycles: int = 3,
    enable_ui: bool = False,
    fixture_builder: bool | str = False,
    builder_provider: str = "none",
    json_output: bool = False,
) -> AutorunResult:
    """Run the autorun loop. Creates job, injects context, runs builder, etc.

    ``fixture_builder`` can be True (standard fixture) or "repair-loop"
    (two-cycle repair loop fixture).
    ``builder_provider`` selects the builder: "none", "fixture", "ollama".
    When "fixture", behaves like fixture_builder=True.
    When "ollama", calls OllamaBuilder through the bridge pipeline.
    """
    import sys

    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.storage import save_job
    from packages.orchestration.timeline import append_run_event

    data_dir = resolve_data_root()
    result = AutorunResult(job_id="", cycles_run=0, stage="init")

    # Resolve provider: --builder-provider takes precedence over --fixture-builder
    if builder_provider == "fixture":
        fixture_builder = fixture_builder or True
    elif builder_provider == "ollama":
        fixture_builder = False
        result.provider = "ollama"

    # Phase 1: Create job
    from packages.core.models import Job
    job = Job(name=goal[:80])
    save_job(job)
    result.job_id = str(job.id)

    _emit(data_dir, job.id, "autorun_started", {
        "goal": goal[:200],
        "autonomy_level": autonomy_level,
        "max_cycles": max_cycles,
        "repo_path": str(Path(repo_path).resolve()),
    })

    # Phase 2: Attach repo
    repo = Path(repo_path).resolve()
    if repo.is_dir():
        job.metadata = job.metadata or {}
        job.metadata["repo_path"] = str(repo)
        save_job(job)

    result.stage = "job_created"

    # Phase 3: Source context injection (Step 97)
    if autonomy_level >= 1:
        try:
            from packages.orchestration.source_context import inject_source_context
            inject_source_context(job, repo, data_dir=str(data_dir))
            result.stage = "context_injected"
        except ImportError:
            pass

    # Phase 4: Run builder (if autonomy >= 2)
    if autonomy_level >= 2:
        if fixture_builder == "repair-loop":
            fx_result = _run_repair_loop_fixture(
                job, goal, repo, data_dir, autonomy_level, max_cycles,
            )
            result.stage = fx_result.get("stage", "builder_complete")
            result.cycles_run = fx_result.get("cycles_run", 1)
            for key in ("source_context_injected", "structured_patch_created",
                        "approval_required", "source_patch_applied", "tests_passed",
                        "repair_context_created", "repair_loop_used"):
                if key in fx_result:
                    result.events.append({"event": key, "value": str(fx_result[key])})
        elif fixture_builder:
            fx_result = _run_fixture_builder(job, goal, repo, data_dir, autonomy_level)
            result.stage = fx_result.get("stage", "builder_complete")
            for key in ("source_context_injected", "structured_patch_created",
                        "approval_required", "source_patch_applied", "tests_passed"):
                if key in fx_result:
                    result.events.append({"event": key, "value": str(fx_result[key])})
        elif builder_provider == "ollama":
            ollama_result = _run_ollama_builder(
                job, goal, repo, data_dir, autonomy_level, max_cycles,
            )
            result.stage = ollama_result.get("stage", "builder_complete")
            result.cycles_run = ollama_result.get("cycles_run", 1)
            result.stop_reason = ollama_result.get("stop_reason", "")
            result.provider = "ollama"
            for key in ("structured_patch_attempted", "parse_success",
                        "source_context_injected", "structured_patch_created",
                        "approval_required", "source_patch_applied", "tests_passed",
                        "stop_reason"):
                if key in ollama_result:
                    result.events.append({"event": key, "value": str(ollama_result[key])})
        else:
            result.stage = "builder_skipped_no_worker"

    # Phase 5: Approval gate (if autonomy >= 3)
    if autonomy_level >= 3 and result.stage == "builder_complete":
        result.stage = "approval_pending"

    # Phase 6: Start UI if requested
    if enable_ui:
        import secrets
        token = secrets.token_urlsafe(24)
        result.ui_url = f"http://127.0.0.1:8787/?job={result.job_id}&token={token}"
        print(f"\nRemedy UI: {result.ui_url}\n", file=sys.stderr)

    if not result.cycles_run:
        result.cycles_run = 1
    return result


def _create_and_approve_fixture_intent(job: Any, patch_summary: str) -> str:
    """Create a real patch intent record on job and approve it. Returns intent_id.

    Used by fixture builders to satisfy the source_apply approval gate.
    Creates a minimal artifact with patch_intent_explanations and records
    approval through approval_queue helpers.
    """
    from packages.core.models import Artifact
    from packages.orchestration.approval_queue import (
        make_intent_id, set_approval_state, APPROVAL_APPROVED,
    )

    artifact = Artifact(
        task_id=uuid4(),
        name="fixture-intent",
        content="",
    )
    artifact.metadata = {
        "patch_intent_explanations": [
            {"file": "fixture", "action": "modify", "risk": "low",
             "reason": "fixture auto-approve", "summary": patch_summary}
        ],
    }
    job.artifacts.append(artifact)

    intent_id = make_intent_id(artifact.id, 0)
    set_approval_state(job, intent_id, APPROVAL_APPROVED,
                       reason="fixture auto-approve", decided_by="fixture")
    return intent_id


def _run_fixture_builder(
    job: Any, goal: str, repo: Path, data_dir: str | Path, autonomy_level: int,
) -> dict[str, Any]:
    """Fixture builder — deterministic E2E autocoder slice, no LLM.

    Creates a failing test, builds structured patch to fix it,
    applies, runs test, records proof. Step 116.
    """
    from packages.orchestration.permissions import Capability, set_permission
    from packages.orchestration.source_apply import apply_structured_patch
    from packages.orchestration.structured_patch import FileOp, StructuredPatch
    from packages.orchestration.timeline import append_run_event

    # Grant write permission for fixture
    set_permission(job, Capability.repo_generated_write, allow=True)

    fx: dict[str, Any] = {"stage": "builder_complete"}

    # 1. Create a wrong calc.py + failing test in repo — calc.py fixture
    (repo / "tests").mkdir(parents=True, exist_ok=True)
    test_path = repo / "tests" / "test_calc.py"
    src_path = repo / "calc.py"
    # Wrong implementation — add subtracts, mul adds
    wrong_content = (
        "def add(a: int, b: int) -> int:\n"
        "    return a - b  # BUG: should be a + b\n"
        "\n"
        "\n"
        "def mul(a: int, b: int) -> int:\n"
        "    return a + b  # BUG: should be a * b\n"
    )
    src_path.write_text(wrong_content, encoding="utf-8")
    test_content = (
        "from calc import add, mul\n"
        "\n"
        "def test_add():\n"
        "    assert add(2, 3) == 5\n"
        "\n"
        "def test_mul():\n"
        "    assert mul(4, 5) == 20\n"
    )
    test_path.write_text(test_content, encoding="utf-8")
    # Makefile for build/test contract
    makefile_path = repo / "Makefile"
    makefile_path.write_text(
        "test:\n"
        "\tpython -m pytest tests/ -x -q\n",
        encoding="utf-8",
    )

    # 2. Source context injection
    try:
        from packages.orchestration.source_context import inject_source_context
        ctx = inject_source_context(job, repo, data_dir=str(data_dir))
        fx["source_context_injected"] = True
        _emit(data_dir, job.id, "source_context_injected", {
            "file_count": ctx.file_count,
            "manifest_count": ctx.manifest_count,
            "test_file_count": ctx.test_file_count,
            "estimated_tokens": ctx.estimated_tokens,
            "mode": ctx.mode,
            "truncated": ctx.truncated,
            "selection_hash": ctx.selection_hash,
        })
    except Exception:
        fx["source_context_injected"] = False

    # 3. Create structured patch (the "fix")
    fix_content = (
        "def add(a: int, b: int) -> int:\n"
        "    return a + b\n"
        "\n"
        "\n"
        "def mul(a: int, b: int) -> int:\n"
        "    return a * b\n"
    )
    patch = StructuredPatch(
        intent_kind="file_ops",
        file_ops=(FileOp(
            path="calc.py",
            action="modify",
            language="python",
            content=fix_content,
            risk="low",
            summary="Fix calc functions (add, mul)",
        ),),
        target_paths=("calc.py",),
        risk="low",
        applicability="applicable",
        requires_approval=True,
    )
    _emit(data_dir, job.id, "structured_patch_intent_created", {
        "intent_kind": patch.intent_kind,
        "target_path_count": len(patch.target_paths),
        "risk": patch.risk,
        "applicability": patch.applicability,
        "requires_approval": patch.requires_approval,
    })
    fx["structured_patch_created"] = True
    fx["approval_required"] = patch.requires_approval

    # 4. Apply patch (fixture auto-approves via real intent)
    if autonomy_level >= 3:
        intent_id = _create_and_approve_fixture_intent(job, "Fix calc functions")
        apply_result = apply_structured_patch(
            patch, repo, data_dir=str(data_dir), job_id=job.id, job=job,
            intent_id=intent_id,
        )
        fx["source_patch_applied"] = apply_result.success
    else:
        fx["source_patch_applied"] = False

    # 5. Run test (if autonomy >= 4)
    if autonomy_level >= 4 and fx.get("source_patch_applied"):
        import subprocess
        import sys as _sys
        try:
            proc = subprocess.run(
                [_sys.executable, "-m", "pytest", str(test_path), "-x", "-q", "--tb=short", "--no-header"],
                capture_output=True, text=True, timeout=30,
                cwd=str(repo),
            )
            passed = proc.returncode == 0
            fx["tests_passed"] = passed
            _emit(data_dir, job.id, "test_run_completed", {
                "exit_code": proc.returncode,
                "passed": passed,
                "fixture": True,
            })
            # Record proof
            if passed:
                import hashlib
                proof_hash = hashlib.sha256(
                    (fix_content + test_content).encode()
                ).hexdigest()[:16]
                _emit(data_dir, job.id, "proof_collected", {
                    "content_hash": proof_hash,
                    "source": "fixture_test",
                    "test_passed": True,
                })
                fx["stage"] = "proof_collected"
        except (subprocess.TimeoutExpired, OSError):
            fx["tests_passed"] = False
    else:
        fx["tests_passed"] = False

    # Create memory candidate if tests passed (standard fixture)
    if fx.get("tests_passed"):
        try:
            from packages.orchestration.memory_candidates import create_candidate
            create_candidate(
                job, "test_command",
                "Test command pytest passes for calc fixture",
                confidence="high",
            )
        except Exception:
            pass

    # Persist final state
    from packages.orchestration.storage import save_job as _save
    _save(job)

    return fx


def _run_repair_loop_fixture(
    job: Any, goal: str, repo: Path, data_dir: str | Path,
    autonomy_level: int, max_cycles: int,
) -> dict[str, Any]:
    """Repair-loop fixture — two-cycle deterministic E2E.

    Cycle 1: Apply wrong-ish fix → tests fail → repair_context_created.
    Cycle 2: Apply correct fix → tests pass → proof_collected.
    """
    from packages.orchestration.permissions import Capability, set_permission
    from packages.orchestration.source_apply import apply_structured_patch
    from packages.orchestration.structured_patch import FileOp, StructuredPatch
    from packages.orchestration.repair_context import build_repair_context
    import subprocess, sys as _sys

    # Grant write permission for fixture
    set_permission(job, Capability.repo_generated_write, allow=True)

    fx: dict[str, Any] = {"stage": "builder_complete", "cycles_run": 0}

    # Setup: wrong calc.py + test
    (repo / "tests").mkdir(parents=True, exist_ok=True)
    test_path = repo / "tests" / "test_calc.py"
    src_path = repo / "calc.py"
    wrong_content = (
        "def add(a: int, b: int) -> int:\n"
        "    return a - b  # BUG\n"
        "\n\ndef mul(a: int, b: int) -> int:\n"
        "    return a + b  # BUG\n"
    )
    src_path.write_text(wrong_content, encoding="utf-8")
    test_content = (
        "from calc import add, mul\n\n"
        "def test_add():\n    assert add(2, 3) == 5\n\n"
        "def test_mul():\n    assert mul(4, 5) == 20\n"
    )
    test_path.write_text(test_content, encoding="utf-8")

    # Source context
    try:
        from packages.orchestration.source_context import inject_source_context
        inject_source_context(job, repo, data_dir=str(data_dir))
        fx["source_context_injected"] = True
    except Exception:
        fx["source_context_injected"] = False

    # Cycle 1: partially wrong fix (add correct, mul still wrong)
    cycle1_content = (
        "def add(a: int, b: int) -> int:\n"
        "    return a + b\n"
        "\n\ndef mul(a: int, b: int) -> int:\n"
        "    return a + b  # still wrong\n"
    )
    patch1 = StructuredPatch(
        intent_kind="file_ops",
        file_ops=(FileOp(
            path="calc.py", action="modify", language="python",
            content=cycle1_content, risk="low",
            summary="Partial fix: add correct, mul still wrong",
        ),),
        target_paths=("calc.py",), risk="low",
        applicability="applicable", requires_approval=True,
    )
    _emit(data_dir, job.id, "structured_patch_intent_created", {
        "intent_kind": "file_ops", "target_path_count": 1,
        "risk": "low", "cycle": 1,
    })
    fx["structured_patch_created"] = True
    fx["approval_required"] = True

    if autonomy_level >= 3:
        intent_id1 = _create_and_approve_fixture_intent(job, "Partial fix cycle 1")
        apply_structured_patch(patch1, repo, data_dir=str(data_dir), job_id=job.id, job=job,
                               intent_id=intent_id1)
        fx["source_patch_applied"] = True

    if autonomy_level >= 4 and max_cycles >= 1:
        fx["cycles_run"] = 1
        proc = subprocess.run(
            [_sys.executable, "-m", "pytest", str(test_path), "-x", "-q",
             "--tb=short", "--no-header"],
            capture_output=True, text=True, timeout=30, cwd=str(repo),
        )
        passed = proc.returncode == 0
        test_event = {"event": "test_run_completed", "metadata": {
            "exit_code": proc.returncode, "passed": passed, "fixture": True, "cycle": 1,
        }}
        _emit(data_dir, job.id, "test_run_completed", test_event["metadata"])
        fx["tests_passed"] = passed

        if not passed and autonomy_level >= 6 and max_cycles >= 2:
            # Repair context
            from packages.orchestration.timeline import load_run_events
            events = load_run_events(data_dir, job.id)
            rc = build_repair_context(job.id, test_event, events)
            _emit(data_dir, job.id, "repair_context_created", {
                "test_run_id": rc["test_run_id"],
                "related_apply_id": rc["related_apply_id"],
                "failure_kind": rc["failure_kind"],
                "affected_file_count": len(rc["affected_files"]),
                "estimated_tokens": rc["estimated_tokens"],
                "truncated": rc["truncated"],
            })
            fx["repair_context_created"] = True
            fx["repair_loop_used"] = True

            # Cycle 2: correct fix
            fix_content = (
                "def add(a: int, b: int) -> int:\n"
                "    return a + b\n"
                "\n\ndef mul(a: int, b: int) -> int:\n"
                "    return a * b\n"
            )
            patch2 = StructuredPatch(
                intent_kind="file_ops",
                file_ops=(FileOp(
                    path="calc.py", action="modify", language="python",
                    content=fix_content, risk="low",
                    summary="Repair fix: correct mul",
                ),),
                target_paths=("calc.py",), risk="low",
                applicability="applicable", requires_approval=True,
            )
            _emit(data_dir, job.id, "structured_patch_intent_created", {
                "intent_kind": "file_ops", "target_path_count": 1,
                "risk": "low", "cycle": 2,
            })
            intent_id2 = _create_and_approve_fixture_intent(job, "Repair fix cycle 2")
            apply_structured_patch(patch2, repo, data_dir=str(data_dir), job_id=job.id, job=job,
                                   intent_id=intent_id2)

            proc2 = subprocess.run(
                [_sys.executable, "-m", "pytest", str(test_path), "-x", "-q",
                 "--tb=short", "--no-header"],
                capture_output=True, text=True, timeout=30, cwd=str(repo),
            )
            passed2 = proc2.returncode == 0
            _emit(data_dir, job.id, "test_run_completed", {
                "exit_code": proc2.returncode, "passed": passed2,
                "fixture": True, "cycle": 2,
            })
            fx["tests_passed"] = passed2
            fx["cycles_run"] = 2

            if passed2:
                import hashlib
                proof_hash = hashlib.sha256(
                    (fix_content + test_content).encode()
                ).hexdigest()[:16]
                _emit(data_dir, job.id, "proof_collected", {
                    "content_hash": proof_hash,
                    "source": "repair_loop_fixture",
                    "test_passed": True,
                })
                fx["stage"] = "completed"

                # Memory candidate from repair success
                try:
                    from packages.orchestration.memory_candidates import create_candidate
                    from packages.orchestration.storage import save_job
                    create_candidate(
                        job, "repair_pattern",
                        "Repair loop fixed mul function after partial fix",
                        confidence="medium",
                    )
                    save_job(job)
                except Exception:
                    pass

    # Persist final state (ensures candidates/metadata survive)
    from packages.orchestration.storage import save_job as _save
    _save(job)

    return fx


def _run_ollama_builder(
    job: Any, goal: str, repo: Path, data_dir: str | Path,
    autonomy_level: int, max_cycles: int,
) -> dict[str, Any]:
    """Real Ollama builder path — calls OllamaBuilder through bridge pipeline.

    Returns dict with safe metadata, stop_reason, stage.
    No raw provider output leaks.
    """
    from packages.orchestration.storage import save_job

    result: dict[str, Any] = {"stage": "builder_complete", "cycles_run": 0}
    result["structured_patch_attempted"] = True

    # Source context injection
    try:
        from packages.orchestration.source_context import inject_source_context
        ctx = inject_source_context(job, repo, data_dir=str(data_dir))
        result["source_context_injected"] = True
        _emit(data_dir, job.id, "source_context_injected", {
            "file_count": ctx.file_count,
            "estimated_tokens": ctx.estimated_tokens,
            "selection_hash": ctx.selection_hash,
        })
    except Exception:
        result["source_context_injected"] = False

    # Build TaskExecutionContext
    from packages.orchestration.builder_models import TaskExecutionContext
    context = TaskExecutionContext(
        job_id=job.id,
        task_id=uuid4(),
        job_prompt=goal,
        task_type="code_change",
        task_description=goal,
    )

    # Try to get memory context
    try:
        from packages.memory.format_memory import format_memory_section
        context.memory_context = format_memory_section()
    except Exception:
        pass

    # Call OllamaBuilder
    try:
        from packages.providers.ollama_builder.provider import OllamaBuilder
        builder = OllamaBuilder()
        output = builder.build(context)
    except ImportError:
        result["stage"] = "provider_error"
        result["stop_reason"] = "provider_unavailable"
        _emit(data_dir, job.id, "autorun_provider_error", {
            "provider": "ollama",
            "error_kind": "import_error",
            "stop_reason": "provider_unavailable",
        })
        save_job(job)
        return result
    except Exception:
        result["stage"] = "provider_error"
        result["stop_reason"] = "provider_unavailable"
        _emit(data_dir, job.id, "autorun_provider_error", {
            "provider": "ollama",
            "error_kind": "provider_error",
            "stop_reason": "provider_unavailable",
        })
        save_job(job)
        return result

    _emit(data_dir, job.id, "autorun_builder_completed", {
        "provider": "ollama",
        "has_structured_patch": bool(output.structured_patch_text),
    })

    # Run through bridge pipeline
    from packages.orchestration.builder_bridge import run_builder_bridge

    bridge_result = run_builder_bridge(
        output, repo,
        job=job, data_dir=data_dir,
        autonomy_level=autonomy_level,
    )

    result["cycles_run"] = 1
    result["stage"] = bridge_result.stage
    result["stop_reason"] = bridge_result.stop_reason
    result["parse_success"] = bridge_result.parse_result.parse_success if bridge_result.parse_result else False
    result["structured_patch_created"] = bridge_result.parse_result.parse_success if bridge_result.parse_result else False
    result["approval_required"] = bridge_result.stage == "approval_pending"
    result["source_patch_applied"] = bridge_result.apply_success
    result["tests_passed"] = bridge_result.test_passed is True

    save_job(job)
    return result


def _autonomy_label(level: int) -> str:
    labels = {
        0: "observe", 1: "propose", 2: "generate",
        3: "apply", 4: "test", 5: "revert",
        6: "loop", 7: "blocked",
    }
    return labels.get(level, "unknown")


def _emit(data_dir: str | Path, job_id: UUID, event: str, metadata: dict[str, Any]) -> None:
    from packages.orchestration.timeline import append_run_event
    append_run_event(data_dir, job_id, event=event, metadata=metadata)
