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
    fixture_builder: bool = False,
    json_output: bool = False,
) -> AutorunResult:
    """Run the autorun loop. Creates job, injects context, runs builder, etc."""
    import sys

    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.storage import save_job
    from packages.orchestration.timeline import append_run_event

    data_dir = resolve_data_root()
    result = AutorunResult(job_id="", cycles_run=0, stage="init")

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
            pass  # Module not yet created — will be in Step 97

    # Phase 4: Run builder (if autonomy >= 2)
    if autonomy_level >= 2:
        if fixture_builder:
            fx_result = _run_fixture_builder(job, goal, repo, data_dir, autonomy_level)
            result.stage = fx_result.get("stage", "builder_complete")
            # Merge fixture result into autorun result events
            for key in ("source_context_injected", "structured_patch_created",
                        "approval_required", "source_patch_applied", "tests_passed"):
                if key in fx_result:
                    result.events.append({"event": key, "value": str(fx_result[key])})
        else:
            # Real builder would go here — requires worker adapter
            result.stage = "builder_skipped_no_worker"

    # Phase 5: Approval gate (if autonomy >= 3)
    if autonomy_level >= 3 and result.stage == "builder_complete":
        # Check for pending approvals
        result.stage = "approval_pending"

    # Phase 6: Start UI if requested
    if enable_ui:
        import secrets
        token = secrets.token_urlsafe(24)
        result.ui_url = f"http://127.0.0.1:8787/?job={result.job_id}&token={token}"
        print(f"\nRemedy UI: {result.ui_url}\n", file=sys.stderr)

    result.cycles_run = 1
    return result


def _run_fixture_builder(
    job: Any, goal: str, repo: Path, data_dir: str | Path, autonomy_level: int,
) -> dict[str, Any]:
    """Fixture builder — deterministic E2E autocoder slice, no LLM.

    Creates a failing test, builds structured patch to fix it,
    applies, runs test, records proof. Step 116.
    """
    from packages.orchestration.source_apply import apply_structured_patch
    from packages.orchestration.structured_patch import FileOp, StructuredPatch
    from packages.orchestration.timeline import append_run_event

    fx: dict[str, Any] = {"stage": "builder_complete"}

    # 1. Create a tiny failing test in repo — calc.py fixture
    (repo / "tests").mkdir(parents=True, exist_ok=True)
    test_path = repo / "tests" / "test_calc.py"
    src_path = repo / "calc.py"
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
            action="create",
            language="python",
            content=fix_content,
            risk="low",
            summary="Create calc functions (add, mul)",
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

    # 4. Apply patch (fixture auto-approves)
    if autonomy_level >= 3:
        apply_result = apply_structured_patch(
            patch, repo, data_dir=str(data_dir), job_id=job.id,
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

    return fx


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
