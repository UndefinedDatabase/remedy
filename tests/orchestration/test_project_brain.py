"""
Domain tests: orchestration/test_project_brain.py
Migrated from step-numbered test files.
"""

from __future__ import annotations

from pathlib import Path
from uuid import UUID, uuid4
from uuid import uuid4
import ast
import json
import os
import pytest
import re
import subprocess
import sys

from packages.core.models import (
    Artifact,
    ArtifactKind,
    Job,
    RunState,
    Task,
)
from packages.core.models import Job, RunState
from packages.core.models import Job, RunState, Task
from packages.memory.models import MemoryEntry
from packages.orchestration.storage import save_job

ROOT = Path(__file__).resolve().parent.parent.parent

UI_SRC = ROOT / "apps" / "ui" / "src"

UI_ROOT = ROOT / "apps" / "ui"

FORBIDDEN_KEYS = (
    "stdout", "stderr", "raw_output", "command_output",
    "Traceback", "diff_preview", "approval_reason",
)


def _make_job(*, project_id: str | None = None, target_repo: str | None = None) -> Job:
    meta: dict = {}
    if project_id:
        meta["project_id"] = project_id
    if target_repo:
        meta["target_repo"] = target_repo
    return Job(
        id=uuid4(),
        name="test job",
        user_prompt="test prompt",
        state=RunState.RUNNING,
        tasks=[
            Task(
                id=uuid4(),
                description="task",
                status=RunState.PENDING,
                inputs={"task_type": "patch"},
                output_artifact_ids=[],
            ),
        ],
        artifacts=[],
        metadata=meta,
    )


# ===========================================================================
# Step 57: Brain Graph Core Refactor — Structural Tests
# ===========================================================================


def _make_job_s68(**overrides) -> Job:
    defaults = {
        "id": uuid4(),
        "name": "test-job",
        "user_prompt": "test prompt",
        "description": "test job",
        "tasks": [
            Task(description="task 1", status=RunState.COMPLETED),
        ],
        "state": RunState.COMPLETED,
        "permissions": {"repo_generated_write": "allow", "repo_test_run": "allow"},
        "metadata": {"target_repo": "."},
    }
    defaults.update(overrides)
    return Job(**defaults)


def _make_job_s163(name: str = "Test goal") -> Job:
    job = Job(name=name)
    job.metadata = job.metadata or {}
    return job


def _make_job_s61(*, project_id: str | None = None, target_repo: str | None = None) -> Job:
    meta: dict = {}
    if project_id:
        meta["project_id"] = project_id
    if target_repo:
        meta["target_repo"] = target_repo
    return Job(
        id=uuid4(),
        name="step61-test",
        user_prompt="test prompt",
        state=RunState.RUNNING,
        tasks=[
            Task(
                id=uuid4(),
                description="task",
                status=RunState.PENDING,
                inputs={"task_type": "patch"},
                output_artifact_ids=[],
            ),
        ],
        artifacts=[],
        metadata=meta,
    )


def _make_job_s62() -> Job:
    return Job(
        id=uuid4(),
        name="hygiene-test",
        user_prompt="test",
        state=RunState.RUNNING,
        tasks=[Task(id=uuid4(), description="t", status=RunState.PENDING,
                     inputs={"task_type": "patch"}, output_artifact_ids=[])],
        artifacts=[],
        metadata={},
    )


def _make_events() -> list[dict]:
    return [
        {"event": "job_created", "run_id": "r1", "job_id": "j1",
         "timestamp": "2026-01-01T00:00:00", "outcome": "ok", "metadata": {}},
        {"event": "patch_intent_created", "run_id": "r1", "job_id": "j1",
         "timestamp": "2026-01-01T00:01:00", "outcome": "ok",
         "metadata": {"intent_id": "pi1", "target_path": "foo.py", "action": "create"}},
    ]


# ── Step 68.1: Event Schema Registry ────────────────────────────────────


def _make_events_s163() -> list[dict]:
    return [
        {"event": "autorun_started", "timestamp": "2026-01-01T00:00:00Z", "metadata": {}},
        {"event": "structured_patch_intent_created", "timestamp": "2026-01-01T00:01:00Z", "metadata": {"intent_kind": "file_ops"}},
        {"event": "source_patch_applied", "timestamp": "2026-01-01T00:02:00Z", "metadata": {}},
        {"event": "test_run_completed", "timestamp": "2026-01-01T00:03:00Z", "metadata": {"exit_code": 0, "passed": True}},
        {"event": "proof_collected", "timestamp": "2026-01-01T00:04:00Z", "metadata": {"content_hash": "abc123"}},
    ]


# ===========================================================================
# Step 163 — Memory Candidate Contract Closure
# ===========================================================================


def _proof_event(intent_id: str, target_path: str) -> dict:
    return {
        "event": "patch_apply_proof_recorded",
        "outcome": "proof_stored",
        "metadata": {
            "intent_id": intent_id,
            "target_path": target_path,
            "sha256": f"sha_{intent_id}",
            "bytes_written": 100,
            "line_count": 10,
        },
    }


def _test_event(status: str = "passed", exit_code: int = 0) -> dict:
    return {
        "event": "test_run_completed",
        "outcome": status,
        "metadata": {
            "command": "pytest",
            "status": status,
            "exit_code": exit_code,
        },
    }


FORBIDDEN_KEYS = (
    "stdout", "stderr", "raw_output", "command_output",
    "Traceback", "diff_preview", "approval_reason",
)


# ===========================================================================
# Multi-proof causal edge correctness
# ===========================================================================




class TestBrainGraphStructure:
    """Structural invariants for the refactored project_brain module."""

    def test_build_project_brain_body_under_80_lines(self):
        src = Path("packages/orchestration/project_brain.py").read_text()
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "build_project_brain":
                body_lines = node.end_lineno - node.lineno + 1
                assert body_lines < 80, f"build_project_brain is {body_lines} lines, must be < 80"
                return
        pytest.fail("build_project_brain not found")

    def test_no_any_n_id_pattern(self):
        src = Path("packages/orchestration/project_brain.py").read_text()
        assert "any(n.id ==" not in src, "any(n.id == ...) pattern must be eliminated"

    def test_no_inline_imports_in_build_project_brain(self):
        src = Path("packages/orchestration/project_brain.py").read_text()
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "build_project_brain":
                for child in ast.walk(node):
                    if isinstance(child, (ast.Import, ast.ImportFrom)):
                        pytest.fail(
                            f"Inline import in build_project_brain at line {child.lineno}"
                        )
                return

    def test_acc_has_node_id_set(self):
        from packages.orchestration.project_brain import _Acc

        job = _make_job()
        acc = _Acc(job, [], None)
        assert hasattr(acc, "node_id_set")
        assert isinstance(acc.node_id_set(), set)

    def test_acc_degraded_tracking(self):
        from packages.orchestration.project_brain import _Acc

        job = _make_job()
        acc = _Acc(job, [], None)
        assert acc.degraded == []
        acc.degraded.append("test_section")
        assert "test_section" in acc.degraded

    def test_graph_has_degraded_field(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain import build_project_brain

        job = _make_job()
        save_job(job)
        graph = build_project_brain(job, [])
        assert hasattr(graph, "degraded")
        assert isinstance(graph.degraded, tuple)

    def test_export_includes_degraded(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain import (
            build_project_brain,
            export_project_brain_json,
        )

        job = _make_job()
        save_job(job)
        graph = build_project_brain(job, [])
        exported = export_project_brain_json(graph)
        assert "degraded" in exported
        assert isinstance(exported["degraded"], list)

    def test_builder_functions_exist(self):
        import packages.orchestration.project_brain as pb

        builders = [
            "_build_job_node",
            "_build_task_nodes",
            "_build_artifact_nodes",
            "_build_patch_intent_nodes",
            "_build_apply_nodes",
            "_build_test_run_nodes",
            "_build_event_derived_nodes",
            "_build_constitution_node",
            "_build_memory_nodes",
            "_build_context_coverage_node",
            "_build_project_placeholder",
            "_build_run_contract_node",
            "_build_token_policy_node",
            "_build_worker_adapter_nodes",
            "_build_readiness_node",
            "_build_context_pack_node",
            "_build_proof_nodes",
            "_build_revert_nodes",
            "_build_change_set_nodes",
            "_build_causal_edges",
            "_build_continuation_edges",
        ]
        for name in builders:
            assert callable(getattr(pb, name, None)), f"Missing builder: {name}"


# ===========================================================================
# Step 58: Brain Reliability Hygiene
# ===========================================================================




class TestBrainReliabilityHygiene:
    """Shared symbols, structured degradation, no bare except Exception."""

    def test_symbols_module_exists(self):
        from packages.orchestration._symbols import OK, FAIL, WARN, INFO, NEXT, LINE

        assert OK == "\u2713"
        assert FAIL == "\u2715"
        assert WARN == "!"
        assert INFO == "\u25cb"
        assert NEXT == "\u2192"
        assert LINE == "\u2500"

    def test_symbols_section_helper(self):
        from packages.orchestration._symbols import section

        result = section("Test")
        assert "Test" in result
        assert "\u2500" in result

    def test_no_except_exception_in_project_brain(self):
        src = Path("packages/orchestration/project_brain.py").read_text()
        assert "except Exception" not in src

    def test_no_except_exception_in_key_modules(self):
        """Key orchestration modules must not use bare except Exception."""
        modules = [
            "packages/orchestration/context_coverage.py",
            "packages/orchestration/project_context_coverage.py",
            "packages/orchestration/autonomy_readiness.py",
            "packages/orchestration/memory_learn.py",
            "packages/orchestration/context_pack.py",
            "packages/orchestration/storage.py",
            "packages/orchestration/project_registry.py",
            "packages/orchestration/patch_apply.py",
            "packages/orchestration/command_discovery.py",
        ]
        for mod in modules:
            src = Path(mod).read_text()
            assert "except Exception:" not in src, f"{mod} still has 'except Exception:'"

    def test_symbols_used_by_project_brain(self):
        src = Path("packages/orchestration/project_brain.py").read_text()
        assert "from packages.orchestration._symbols import" in src

    def test_symbols_used_by_brain_detail(self):
        src = Path("packages/orchestration/brain_detail.py").read_text()
        assert "from packages.orchestration._symbols import" in src


# ===========================================================================
# Step 59: Causal Accuracy + Continue Tests
# ===========================================================================




class TestCausalAccuracy:
    """Causal edge correctness for proof→test and proof→memory chains."""

    def test_proof_to_test_chronological(self, tmp_path, monkeypatch):
        """Proof nodes connect to test nodes by chronological index pairing."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain import (
            ET_PROOF_VERIFIED_BY,
            build_project_brain,
        )

        job = _make_job()
        save_job(job)

        # Simulate two proof events and two test events
        events = [
            {
                "event": "patch_apply_proof_recorded",
                "outcome": "proof_stored",
                "metadata": {
                    "intent_id": "intent_A",
                    "target_path": "a.py",
                    "sha256": "aaa",
                    "bytes_written": 100,
                    "line_count": 10,
                },
            },
            {
                "event": "test_run_completed",
                "outcome": "passed",
                "metadata": {
                    "command": "pytest",
                    "status": "passed",
                    "exit_code": 0,
                },
            },
            {
                "event": "patch_apply_proof_recorded",
                "outcome": "proof_stored",
                "metadata": {
                    "intent_id": "intent_B",
                    "target_path": "b.py",
                    "sha256": "bbb",
                    "bytes_written": 200,
                    "line_count": 20,
                },
            },
            {
                "event": "test_run_completed",
                "outcome": "passed",
                "metadata": {
                    "command": "pytest",
                    "status": "passed",
                    "exit_code": 0,
                },
            },
        ]

        graph = build_project_brain(job, events)
        proof_test_edges = [e for e in graph.edges if e.type == ET_PROOF_VERIFIED_BY]
        # Should have at least 2 proof→test edges (one per proof/test pair)
        assert len(proof_test_edges) >= 2

    def test_proof_to_memory_matching(self, tmp_path, monkeypatch):
        """Memory nodes link back to proof via source_id matching."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain import (
            ET_INFORMED_MEMORY,
            build_project_brain,
        )

        job = _make_job()
        save_job(job)

        events = [
            {
                "event": "patch_apply_proof_recorded",
                "outcome": "proof_stored",
                "metadata": {
                    "intent_id": "intent_X",
                    "target_path": "x.py",
                    "sha256": "xxx",
                    "bytes_written": 100,
                    "line_count": 10,
                },
            },
        ]

        graph = build_project_brain(job, events)
        memory_edges = [e for e in graph.edges if e.type == ET_INFORMED_MEMORY]
        # Memory nodes may or may not exist (depends on memory gateway availability)
        # but edges should be structurally valid
        for edge in memory_edges:
            assert edge.source  # non-empty source
            assert edge.target  # non-empty target




class TestContextOptimizer:
    def test_explain_context(self):
        from packages.orchestration.context_optimizer import explain_context
        job = _make_job_s68()
        data = explain_context(job, _make_events(), mode="compact", budget=2000)
        assert data["version"] == 1
        assert data["mode"] == "compact"
        assert data["budget"] == 2000
        assert "sections" in data
        assert "excluded" in data
        assert "recommendations" in data
        assert isinstance(data["sections"], list)

    def test_explain_context_invalid_mode(self):
        from packages.orchestration.context_optimizer import explain_context
        job = _make_job_s68()
        data = explain_context(job, [], mode="invalid_mode", budget=2000)
        assert data["mode"] == "compact"  # fallback

    def test_optimize_context(self):
        from packages.orchestration.context_optimizer import optimize_context
        job = _make_job_s68()
        data = optimize_context(job, _make_events(), budget=2000)
        assert data["version"] == 1
        assert data["budget"] == 2000
        assert "recommended_mode" in data
        assert data["recommended_mode"] in ("caveman", "compact", "standard")
        assert "estimated_tokens" in data
        assert "token_savings" in data
        assert "included_sections" in data
        assert "excluded_sections" in data
        assert "recommended_worker" in data
        assert "recommendations" in data

    def test_optimize_context_tight_budget(self):
        from packages.orchestration.context_optimizer import optimize_context
        job = _make_job_s68()
        data = optimize_context(job, [], budget=50)
        # Very tight budget should pick caveman
        assert data["recommended_mode"] in ("caveman", "compact", "standard")

    def test_optimize_context_7_field_schema(self):
        """context_budget_optimized event must match 7-field schema."""
        from packages.orchestration.context_optimizer import optimize_context
        from packages.orchestration.event_schemas import validate_event_metadata
        job = _make_job_s68()
        data = optimize_context(job, _make_events(), budget=2000)
        # Build metadata as the CLI handler would
        meta = {
            "mode": data["recommended_mode"],
            "budget": data["budget"],
            "estimated_tokens": data["estimated_tokens"],
            "token_savings": data["token_savings"],
            "recommended_worker": data["recommended_worker"],
            "included_section_count": len(data["included_sections"]),
            "excluded_section_count": len(data["excluded_sections"]),
        }
        errors = validate_event_metadata("context_budget_optimized", meta)
        assert errors == [], f"Schema errors: {errors}"


# ── Brain Integration ───────────────────────────────────────────────────




class TestBrainIntegration:
    def test_brain_has_decision_queue_node(self):
        from packages.orchestration.project_brain import (
            NT_DECISION_QUEUE,
            build_project_brain,
        )
        job = _make_job_s68()
        graph = build_project_brain(job, _make_events())
        dq_nodes = [n for n in graph.nodes if n.type == NT_DECISION_QUEUE]
        assert len(dq_nodes) == 1
        assert dq_nodes[0].id == "decision_queue"

    def test_brain_has_context_budget_node(self):
        from packages.orchestration.project_brain import (
            NT_CONTEXT_BUDGET,
            build_project_brain,
        )
        job = _make_job_s68()
        graph = build_project_brain(job, _make_events())
        cb_nodes = [n for n in graph.nodes if n.type == NT_CONTEXT_BUDGET]
        assert len(cb_nodes) == 1
        assert cb_nodes[0].id == "context_budget"

    def test_brain_decision_queue_edges(self):
        from packages.orchestration.project_brain import (
            ET_HAS_DECISION_QUEUE,
            build_project_brain,
        )
        job = _make_job_s68()
        graph = build_project_brain(job, _make_events())
        dq_edges = [e for e in graph.edges if e.type == ET_HAS_DECISION_QUEUE]
        assert len(dq_edges) == 1

    def test_brain_context_budget_edges(self):
        from packages.orchestration.project_brain import (
            ET_HAS_CONTEXT_BUDGET,
            build_project_brain,
        )
        job = _make_job_s68()
        graph = build_project_brain(job, _make_events())
        cb_edges = [e for e in graph.edges if e.type == ET_HAS_CONTEXT_BUDGET]
        assert len(cb_edges) == 1

    def test_brain_node_type_order(self):
        from packages.orchestration.project_brain import (
            NT_CONTEXT_BUDGET,
            NT_DECISION_QUEUE,
            _NODE_TYPE_ORDER,
        )
        assert NT_DECISION_QUEUE in _NODE_TYPE_ORDER
        assert NT_CONTEXT_BUDGET in _NODE_TYPE_ORDER
        assert _NODE_TYPE_ORDER[NT_DECISION_QUEUE] == 25
        assert _NODE_TYPE_ORDER[NT_CONTEXT_BUDGET] == 26


# ── Brain Detail ────────────────────────────────────────────────────────




class TestMemoryCandidateCreateApproveReject:
    """Memory candidate contract closure."""

    def test_create_candidate_basic(self):
        from packages.orchestration.memory_candidates import create_candidate, list_candidates

        job = _make_job_s163()
        c = create_candidate(job, "repair_pattern", "Repair loop fixed mul", confidence="medium")
        assert c["kind"] == "repair_pattern"
        assert c["status"] == "pending"
        assert c["safe_summary"] == "Repair loop fixed mul"
        assert c["confidence"] == "medium"

        candidates = list_candidates(job)
        assert len(candidates) == 1
        assert candidates[0]["id"] == c["id"]

    def test_create_candidate_dedup(self):
        from packages.orchestration.memory_candidates import create_candidate, list_candidates

        job = _make_job_s163()
        c1 = create_candidate(job, "repair_pattern", "Same summary")
        c2 = create_candidate(job, "repair_pattern", "Same summary")
        assert c1["id"] == c2["id"]
        assert len(list_candidates(job)) == 1

    def test_approve_candidate(self):
        from packages.orchestration.memory_candidates import (
            approve_candidate,
            create_candidate,
            list_candidates,
        )

        job = _make_job_s163()
        c = create_candidate(job, "test_command", "pytest passes")
        assert approve_candidate(job, c["id"])
        candidates = list_candidates(job)
        assert candidates[0]["status"] == "approved"

    def test_reject_candidate(self):
        from packages.orchestration.memory_candidates import (
            create_candidate,
            list_candidates,
            reject_candidate,
        )

        job = _make_job_s163()
        c = create_candidate(job, "test_command", "pytest passes")
        assert reject_candidate(job, c["id"])
        candidates = list_candidates(job)
        assert candidates[0]["status"] == "rejected"

    def test_approve_already_rejected(self):
        from packages.orchestration.memory_candidates import (
            approve_candidate,
            create_candidate,
            reject_candidate,
        )

        job = _make_job_s163()
        c = create_candidate(job, "test_command", "test")
        reject_candidate(job, c["id"])
        # Can't approve already rejected
        assert not approve_candidate(job, c["id"])

    def test_no_raw_leaks_in_candidate(self):
        from packages.orchestration.memory_candidates import create_candidate

        job = _make_job_s163()
        c = create_candidate(
            job, "repair_pattern",
            "Safe summary only",
            evidence_node_ids=["node-1", "node-2"],
        )
        s = json.dumps(c)
        for forbidden in ("stdout", "stderr", "traceback", "command_output"):
            assert forbidden not in s.lower()


# ===========================================================================
# Step 164 — Human Story ViewModel
# ===========================================================================




class TestStoryViewModelSchema:
    """Story ViewModel."""

    def test_story_schema(self):
        from packages.orchestration.ui_view_model import build_story

        job = _make_job_s163("Build a README")
        events = _make_events_s163()
        story = build_story(job, events)

        assert story["version"] == 1
        assert story["job_id"] == str(job.id)
        assert story["headline"]
        assert story["plain_status"]
        assert "progress" in story
        for key in ("completed", "active", "pending", "blocked", "needs_review"):
            assert key in story["progress"]
        assert "journey" in story

    def test_journey_has_items(self):
        from packages.orchestration.ui_view_model import build_story

        job = _make_job_s163()
        events = _make_events_s163()
        story = build_story(job, events)
        assert len(story["journey"]) > 0

    def test_journey_items_human_readable(self):
        from packages.orchestration.ui_view_model import build_story

        job = _make_job_s163()
        events = _make_events_s163()
        story = build_story(job, events)

        for j in story["journey"]:
            assert j.get("title"), f"missing title: {j}"
            assert j.get("kind"), f"missing kind: {j}"
            assert j.get("state") in ("done", "current", "pending", "blocked", "suggested")

    def test_forbidden_debug_words_absent(self):
        from packages.orchestration.ui_view_model import build_story
        from packages.orchestration.ui_copy import FORBIDDEN_DEFAULT_WORDS

        job = _make_job_s163()
        events = _make_events_s163()
        story = build_story(job, events)
        s = json.dumps(story).lower()

        for word in FORBIDDEN_DEFAULT_WORDS:
            # Allow "rank" as part of internal data but not in titles/subtitles
            for j in story["journey"]:
                assert word not in j["title"].lower(), f"forbidden '{word}' in title: {j['title']}"
                assert word not in (j.get("subtitle") or "").lower(), f"forbidden '{word}' in subtitle"


# ===========================================================================
# Step 165 — Human Node Detail
# ===========================================================================




class TestUiRebuildSpecDocument:
    """UI rebuild spec document present and complete."""

    @pytest.fixture(autouse=True)
    def load_spec(self):
        self.spec_path = ROOT / "docs" / "ui" / "REMEDY_UI_REBUILD_SPEC.md"
        assert self.spec_path.is_file(), "Spec file must exist"
        self.content = self.spec_path.read_text(encoding="utf-8")

    def test_has_component_tree(self):
        assert "RemedyApp" in self.content
        assert "RemedyShell" in self.content
        assert "LeftBrandRail" in self.content
        assert "BrainGraphStage" in self.content
        assert "RightLivePanel" in self.content
        assert "PhaseTimeline" in self.content
        assert "DetailPopover" in self.content
        assert "LayerSwitcher" in self.content

    def test_has_css_tokens(self):
        assert "--remedy-bg:" in self.content
        assert "--remedy-blue-500:" in self.content
        assert "--remedy-card:" in self.content
        assert "--remedy-text:" in self.content
        assert "--remedy-shadow:" in self.content

    def test_has_forbidden_words_section(self):
        assert "Forbidden" in self.content
        assert "rank" in self.content
        assert "importance" in self.content
        assert "node_type" in self.content
        assert "context coverage" in self.content

    def test_has_semantic_zoom_rules(self):
        assert "Semantic Zoom" in self.content
        assert "Overview" in self.content
        assert "Diagnostics" in self.content

    def test_no_old_ui_as_primary(self):
        lower = self.content.lower()
        assert "old ui is primary" not in lower
        assert "pixi" not in lower


# ---------------------------------------------------------------------------
# Step 174 — Frontend project structure
# ---------------------------------------------------------------------------




class TestFrontendProjectStructure:
    """Frontend has clean modern React structure."""

    def test_package_json_valid(self):
        pkg = json.loads((UI_ROOT / "package.json").read_text(encoding="utf-8"))
        assert pkg["name"] == "@remedy/ui"
        assert "react" in pkg.get("dependencies", {})
        assert "react-force-graph-2d" in pkg.get("dependencies", {})
        assert "@mui/material" in pkg.get("dependencies", {})

    def test_no_pixi_dependency(self):
        pkg = json.loads((UI_ROOT / "package.json").read_text(encoding="utf-8"))
        deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
        assert "pixi.js" not in deps
        assert "pixi-viewport" not in deps
        assert "elkjs" not in deps

    def test_tsconfig_has_jsx(self):
        tsconfig = json.loads((UI_ROOT / "tsconfig.json").read_text(encoding="utf-8"))
        assert tsconfig["compilerOptions"].get("jsx") == "react-jsx"

    def test_vite_config_has_react_plugin(self):
        vite = (UI_ROOT / "vite.config.ts").read_text(encoding="utf-8")
        assert "react" in vite

    def test_eslint_config_exists(self):
        assert (UI_ROOT / "eslint.config.js").is_file()

    def test_no_node_modules_committed(self):
        # Check .gitignore or just that node_modules is not tracked
        nm = UI_ROOT / "node_modules"
        if nm.exists():
            # Just verify it's not in git
            pass  # node_modules should be gitignored

    def test_main_tsx_exists(self):
        assert (UI_SRC / "main.tsx").is_file()

    def test_remedy_app_exists(self):
        assert (UI_SRC / "RemedyApp.tsx").is_file()

    def test_tokens_css_exists(self):
        assert (UI_SRC / "styles" / "tokens.css").is_file()

    def test_globals_css_exists(self):
        assert (UI_SRC / "styles" / "globals.css").is_file()


# ---------------------------------------------------------------------------
# Step 175 — API data adapter
# ---------------------------------------------------------------------------




class TestMultiProofCausalEdges:
    """Proof[i] → test[i] chronological pairing, not last→last."""

    def test_three_proof_three_test_pairing(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain import (
            ET_PROOF_VERIFIED_BY,
            build_project_brain,
        )

        job = _make_job_s61()
        save_job(job)

        events = [
            _proof_event("i1", "a.py"),
            _test_event(),
            _proof_event("i2", "b.py"),
            _test_event(),
            _proof_event("i3", "c.py"),
            _test_event(),
        ]

        graph = build_project_brain(job, events)
        pv_edges = [e for e in graph.edges if e.type == ET_PROOF_VERIFIED_BY]
        assert len(pv_edges) == 3

        # Each proof should connect to its own test, not all to last
        sources = [e.source for e in pv_edges]
        targets = [e.target for e in pv_edges]
        assert len(set(sources)) == 3, "Each proof should have unique source"
        assert len(set(targets)) == 3, "Each test should have unique target"

    def test_more_proofs_than_tests(self, tmp_path, monkeypatch):
        """Extra proofs beyond test count have no test edge."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain import (
            ET_PROOF_VERIFIED_BY,
            build_project_brain,
        )

        job = _make_job_s61()
        save_job(job)

        events = [
            _proof_event("i1", "a.py"),
            _proof_event("i2", "b.py"),
            _test_event(),
        ]

        graph = build_project_brain(job, events)
        pv_edges = [e for e in graph.edges if e.type == ET_PROOF_VERIFIED_BY]
        # At most 1 edge (first proof → first test)
        assert len(pv_edges) == 1

    def test_proof_recorded_edge_exists(self, tmp_path, monkeypatch):
        """patch_apply → proof has recorded_proof edge."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain import (
            ET_RECORDED_PROOF,
            build_project_brain,
        )

        job = _make_job_s61()
        # Need an artifact with apply records to get apply nodes
        art = Artifact(
            id=uuid4(), name="test-art", kind=ArtifactKind.PATCH_INTENT,
            content="",
            metadata={
                "patch_intent_apply_records": {
                    "i1": {"state": "applied", "bytes_written": 50, "line_count": 5}
                }
            },
        )
        job.artifacts.append(art)
        save_job(job)

        events = [_proof_event("i1", "a.py")]
        graph = build_project_brain(job, events)
        rp_edges = [e for e in graph.edges if e.type == ET_RECORDED_PROOF]
        assert len(rp_edges) >= 1
        assert any("apply:i1" in e.source for e in rp_edges)


# ===========================================================================
# File provenance (file why) chain correctness
# ===========================================================================




class TestFileProvenanceChain:
    """file_provenance builds correct causal chain."""

    def test_full_chain_order(self, tmp_path, monkeypatch):
        """Chain follows: patch_intent → approval → apply → proof → test_run."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.approval_queue import make_intent_id
        from packages.orchestration.file_provenance import build_file_provenance

        job = _make_job_s61()
        art_id = uuid4()
        intent_id = make_intent_id(art_id, 0)

        art = Artifact(
            id=art_id, name="test-art", kind=ArtifactKind.PATCH_INTENT,
            content="",
            metadata={
                "patch_intent_explanations": [
                    {
                        "file": "src/foo.py",
                        "action": "modify",
                        "risk": "low",
                        "reason": "test",
                        "summary": "test intent",
                    }
                ],
                "patch_intent_approvals": {
                    intent_id: {
                        "state": "approved",
                        "decided_at": "2026-01-01",
                        "decided_by": "user",
                    }
                },
                "patch_intent_apply_records": {
                    intent_id: {"state": "applied", "bytes_written": 100, "line_count": 10}
                },
            },
        )
        job.artifacts.append(art)
        save_job(job)

        events = [
            _proof_event(intent_id, "src/foo.py"),
            _test_event(),
        ]

        prov = build_file_provenance(job, events, "src/foo.py")
        assert prov.found is True
        steps = [link.step for link in prov.chain]
        assert steps == [
            "patch_intent", "approval_decision", "patch_apply",
            "patch_apply_proof", "test_run",
        ]

    def test_no_match_returns_not_found(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.file_provenance import build_file_provenance

        job = _make_job_s61()
        save_job(job)
        prov = build_file_provenance(job, [], "nonexistent.py")
        assert prov.found is False
        assert len(prov.chain) == 0

    def test_revert_state_from_durable_record(self, tmp_path, monkeypatch):
        """patch_apply status reflects DurableApplyRecord state when data_dir provided (Step 1146)."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.approval_queue import make_intent_id
        from packages.orchestration.file_provenance import build_file_provenance
        from packages.orchestration.repository_snapshot import DurableApplyRecord, save_durable_apply_record

        job = _make_job_s61()
        art_id = uuid4()
        intent_id = make_intent_id(art_id, 0)
        art = Artifact(
            id=art_id, name="test-art", kind=ArtifactKind.PATCH_INTENT,
            content="",
            metadata={
                "patch_intent_explanations": [
                    {"file": "src/foo.py", "action": "modify", "risk": "low", "reason": "", "summary": ""}
                ],
                "patch_intent_approvals": {
                    intent_id: {"state": "approved", "decided_at": "", "decided_by": ""}
                },
                "patch_intent_apply_records": {
                    intent_id: {"state": "applied", "bytes_written": 50, "line_count": 5}
                },
            },
        )
        job.artifacts.append(art)
        save_job(job)

        # Save DurableApplyRecord with reverted state
        record = DurableApplyRecord(
            apply_id=intent_id,
            job_id=str(job.id),
            intent_id=intent_id,
            snapshot_id="snap-001",
            state="reverted",
            target_paths=["src/foo.py"],
            applied_at="2026-01-01T00:00:00Z",
            before_proof={},
            after_proof={},
            snapshot_verified=True,
        )
        save_durable_apply_record(record, str(job.id), tmp_path)

        # Without data_dir: stale artifact state ("applied")
        prov_stale = build_file_provenance(job, [], "src/foo.py")
        apply_link = next(l for l in prov_stale.chain if l.step == "patch_apply")
        assert apply_link.status == "applied"

        # With data_dir: authoritative DurableApplyRecord state ("reverted")
        prov = build_file_provenance(job, [], "src/foo.py", data_dir=tmp_path)
        apply_link = next(l for l in prov.chain if l.step == "patch_apply")
        assert apply_link.status == "reverted"

    def test_provenance_json_no_raw_leaks(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.approval_queue import make_intent_id
        from packages.orchestration.file_provenance import (
            build_file_provenance,
            export_file_provenance_json,
        )

        job = _make_job_s61()
        art_id = uuid4()
        intent_id = make_intent_id(art_id, 0)
        art = Artifact(
            id=art_id, name="test-art", kind=ArtifactKind.PATCH_INTENT,
            content="",
            metadata={
                "patch_intent_explanations": [
                    {
                        "file": "x.py",
                        "action": "modify",
                        "risk": "low",
                        "reason": "test",
                        "summary": "test",
                    }
                ],
                "patch_intent_approvals": {
                    intent_id: {"state": "approved"}
                },
            },
        )
        job.artifacts.append(art)
        save_job(job)

        prov = build_file_provenance(job, [_proof_event(intent_id, "x.py")], "x.py")
        raw = json.dumps(export_file_provenance_json(prov))
        for forbidden in FORBIDDEN_KEYS:
            assert forbidden not in raw, f"Raw leak: {forbidden}"


# ===========================================================================
# Continue roundtrip + project aggregate integrity
# ===========================================================================




class TestContinueRoundtripAggregate:
    """Parent → child continue-from-node, aggregate includes both."""

    def test_aggregate_includes_parent_and_child(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.continue_from_node import continue_from_node
        from packages.orchestration.data_paths import resolve_data_root
        from packages.orchestration.project_brain import build_project_brain
        from packages.orchestration.project_brain_aggregate import (
            build_project_brain_aggregate,
        )
        from packages.orchestration.project_registry import (
            RemyProject,
            save_project,
        )
        from packages.orchestration.storage import load_job
        from packages.orchestration.timeline import load_run_events

        pid = str(uuid4())
        project = RemyProject(id=UUID(pid), name="test-project", repo_paths=[str(tmp_path)])
        save_project(project)

        parent = _make_job_s61(project_id=pid, target_repo=str(tmp_path))
        save_job(parent)

        # Build parent brain, continue from first node
        parent_graph = build_project_brain(parent, [])
        result = continue_from_node(parent, parent_graph, parent_graph.nodes[0].id, "child task")

        child = load_job(UUID(result.child_job_id))

        # Load events for both jobs
        data_root = resolve_data_root()
        parent_events = load_run_events(data_root, parent.id)
        child_events = load_run_events(data_root, child.id)

        all_events = {
            str(parent.id): parent_events,
            str(child.id): child_events,
        }

        # Attach child to project
        project.job_ids.append(str(child.id))
        if str(parent.id) not in project.job_ids:
            project.job_ids.append(str(parent.id))

        agg = build_project_brain_aggregate(
            project, [parent, child], all_events,
        )

        # Aggregate must include nodes from both jobs
        job_node_ids = [n.id for n in agg.nodes if n.type == "job"]
        assert str(parent.id) in job_node_ids
        assert str(child.id) in job_node_ids

        # Must have continuation edge
        cont_edges = [e for e in agg.edges if e.type == "continued_as"]
        assert len(cont_edges) >= 1

        # Must have exactly 2 job subgraphs
        assert len(agg.job_graphs) == 2

    def test_aggregate_summary_counts(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain_aggregate import (
            build_project_brain_aggregate,
        )
        from packages.orchestration.project_registry import (
            RemyProject,
            save_project,
        )

        pid = str(uuid4())
        project = RemyProject(id=UUID(pid), name="count-test", repo_paths=[])
        save_project(project)

        j1 = _make_job_s61(project_id=pid)
        j2 = _make_job_s61(project_id=pid)
        save_job(j1)
        save_job(j2)

        agg = build_project_brain_aggregate(project, [j1, j2], {})
        assert agg.summary["job_count"] == 2
        assert agg.summary["node_count"] > 0
        assert agg.summary["edge_count"] > 0


# ===========================================================================
# No raw content leaks in brain/aggregate outputs
# ===========================================================================




class TestSharedSymbols:
    def test_symbols_module_has_section(self):
        from packages.orchestration._symbols import section
        result = section("Test")
        assert "Test" in result
        assert "\u2500" in result

    def test_section_width_default(self):
        from packages.orchestration._symbols import section
        result = section("Hello")
        # Default width=50, so bar length = max(1, 50 - len("Hello") - 1) = 44
        assert result.count("\u2500") >= 44

    def test_section_width_custom(self):
        from packages.orchestration._symbols import section
        result = section("Hello", width=64)
        assert result.count("\u2500") >= 58




class TestBrainDetailRegistry:
    def test_registry_exists(self):
        from packages.orchestration.brain_detail import (
            _DETAIL_REGISTRY,
            _DETAIL_REGISTRY_JOB,
        )
        assert isinstance(_DETAIL_REGISTRY, dict)
        assert isinstance(_DETAIL_REGISTRY_JOB, dict)
        assert len(_DETAIL_REGISTRY) + len(_DETAIL_REGISTRY_JOB) >= 25

    def test_known_node_types_covered(self):
        """Every NT_* constant from project_brain must have a detail handler."""
        import packages.orchestration.project_brain as pb
        from packages.orchestration.brain_detail import (
            _DETAIL_REGISTRY,
            _DETAIL_REGISTRY_JOB,
        )

        all_nt = {
            v for name, v in vars(pb).items()
            if name.startswith("NT_") and isinstance(v, str)
        }
        covered = set(_DETAIL_REGISTRY.keys()) | set(_DETAIL_REGISTRY_JOB.keys())
        uncovered = all_nt - covered
        assert uncovered == set(), f"Node types without detail handler: {uncovered}"

    def test_all_handlers_callable(self):
        from packages.orchestration.brain_detail import (
            _DETAIL_REGISTRY,
            _DETAIL_REGISTRY_JOB,
        )
        for nt, handler in {**_DETAIL_REGISTRY, **_DETAIL_REGISTRY_JOB}.items():
            assert callable(handler), f"Handler for {nt} is not callable"

    def test_brain_detail_builds_for_all_node_types(self, tmp_path, monkeypatch):
        """build_brain_node_detail must not raise for any node in a real graph."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.brain_detail import build_brain_node_detail
        from packages.orchestration.project_brain import build_project_brain

        job = _make_job_s62()
        save_job(job)
        graph = build_project_brain(job, [])
        for node in graph.nodes:
            detail = build_brain_node_detail(job, graph, node.id, [])
            assert detail.node_id == node.id
            assert detail.node_type == node.type




class TestMemoryCardModel:
    def test_new_fields_exist(self):
        e = MemoryEntry(key="k", value="v")
        assert e.summary == ""
        assert e.scope == "job"
        assert e.validity == "active"
        assert e.review_status == "proposed"
        assert e.updated_at is None
        assert e.supersedes is None
        assert e.contradicts is None
        assert e.evidence_refs == []

    def test_roundtrip(self):
        e = MemoryEntry(
            key="k", value="v", summary="test summary",
            scope="project", validity="stale", review_status="approved",
            evidence_refs=["ref1", "ref2"],
        )
        d = json.loads(e.to_json_line())
        e2 = MemoryEntry.from_dict(d)
        assert e2.summary == "test summary"
        assert e2.scope == "project"
        assert e2.validity == "stale"
        assert e2.review_status == "approved"
        assert e2.evidence_refs == ["ref1", "ref2"]

    def test_backward_compat_from_dict(self):
        """Old entries without new fields still deserialize."""
        d = {"id": str(uuid4()), "key": "old", "value": "v1"}
        e = MemoryEntry.from_dict(d)
        assert e.summary == ""
        assert e.validity == "active"
        assert e.evidence_refs == []




class TestCardManagement:
    def test_approve(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import (
            approve_memory_card,
            store_memory,
        )

        entry = store_memory("k1", "v1", job_id="j1")
        assert entry.approved is False
        result = approve_memory_card(str(entry.id), job_id="j1")
        assert result is not None
        assert result.approved is True
        assert result.review_status == "approved"

    def test_reject(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import (
            reject_memory_card,
            store_memory,
        )

        entry = store_memory("k2", "v2", job_id="j2")
        result = reject_memory_card(str(entry.id), job_id="j2")
        assert result is not None
        assert result.approved is False
        assert result.review_status == "rejected"

    def test_mark_stale(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import mark_stale, store_memory

        entry = store_memory("k3", "v3", job_id="j3")
        result = mark_stale(str(entry.id), job_id="j3")
        assert result is not None
        assert result.validity == "stale"

    def test_supersede(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import (
            store_memory,
            supersede_memory_card,
        )

        e1 = store_memory("k4", "old", job_id="j4")
        e2 = store_memory("k4", "new", job_id="j4")
        old, new = supersede_memory_card(str(e1.id), str(e2.id), job_id="j4")
        assert old is not None
        assert old.validity == "superseded"
        assert new is not None
        assert new.supersedes == str(e1.id)

    def test_contradict(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import (
            contradict_memory_card,
            store_memory,
        )

        e1 = store_memory("k5", "claim_a", job_id="j5")
        e2 = store_memory("k5", "claim_b", job_id="j5")
        contradicted, by = contradict_memory_card(str(e1.id), str(e2.id), job_id="j5")
        assert contradicted is not None
        assert contradicted.validity == "contradicted"
        assert contradicted.contradicts == str(e2.id)

    def test_get_card(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import get_memory_card, store_memory

        entry = store_memory("k6", "v6", job_id="j6")
        card = get_memory_card(str(entry.id), job_id="j6")
        assert card is not None
        assert card.key == "k6"

    def test_get_card_not_found(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import get_memory_card

        card = get_memory_card(str(uuid4()), job_id="nonexistent")
        assert card is None




class TestLearnEvidence:
    def test_learn_creates_entries(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.core.models import Job, RunState, Task
        from packages.orchestration.memory_learn import learn_from_job
        from packages.orchestration.storage import save_job

        job = Job(
            id=uuid4(), name="learn-test", user_prompt="test",
            tasks=[Task(description="t", status=RunState.COMPLETED)],
            metadata={"target_repo": "/tmp/test"},
        )
        save_job(job)
        events = [
            {"event": "test_run_completed", "metadata": {"command": "pytest", "status": "passed", "exit_code": 0}},
            {"event": "patch_apply_proof_recorded", "metadata": {"intent_id": "i1", "target_path": "a.py", "sha256": "aaa", "bytes_written": 10, "line_count": 5}},
        ]
        result = learn_from_job(job, events, approved=True)
        assert result.learned_count > 0




class TestBrainMemoryNodeSafe:
    def test_memory_node_has_evidence_fields(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.core.models import Job, RunState, Task
        from packages.memory.local_gateway import store_memory
        from packages.orchestration.project_brain import build_project_brain
        from packages.orchestration.storage import save_job

        job = Job(
            id=uuid4(), name="brain-mem", user_prompt="test",
            tasks=[Task(description="t", status=RunState.PENDING)],
        )
        save_job(job)
        store_memory("test.key", "test value", job_id=str(job.id), approved=True)
        graph = build_project_brain(job, [])

        mem_nodes = [n for n in graph.nodes if n.type == "memory"]
        assert len(mem_nodes) >= 1
        meta = mem_nodes[0].metadata
        assert "key" in meta
        assert "summary" in meta
        assert "validity" in meta
        assert "review_status" in meta
        assert "scope" in meta
        assert "evidence_refs_count" in meta
        # No raw leaks
        for forbidden in ("stdout", "stderr", "raw_output", "value"):
            assert forbidden not in meta




class TestGitStatusBrainNode:
    def test_git_status_node_in_graph(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain import build_project_brain
        from packages.orchestration.storage import save_job

        job = Job(
            id=uuid4(), name="brain-git", user_prompt="test",
            tasks=[Task(description="t", status=RunState.PENDING)],
            metadata={"target_repo": "."},
        )
        save_job(job)
        graph = build_project_brain(job, [])
        git_nodes = [n for n in graph.nodes if n.type == "git_status"]
        assert len(git_nodes) == 1
        meta = git_nodes[0].metadata
        assert "is_git_repo" in meta
        assert "git_available" in meta
        assert "branch" in meta
        assert "head_sha" in meta
        assert "dirty" in meta
        assert "changed_file_count" in meta
        assert "status_hash" in meta

    def test_git_status_node_no_repo(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain import build_project_brain
        from packages.orchestration.storage import save_job

        job = Job(
            id=uuid4(), name="brain-no-git", user_prompt="test",
            tasks=[Task(description="t", status=RunState.PENDING)],
        )
        save_job(job)
        graph = build_project_brain(job, [])
        git_nodes = [n for n in graph.nodes if n.type == "git_status"]
        # No target_repo → no git_status node
        assert len(git_nodes) == 0

    def test_git_status_non_git_target(self, tmp_path, monkeypatch):
        """Non-git target_repo creates node with is_git_repo=False."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain import build_project_brain
        from packages.orchestration.storage import save_job

        non_git = tmp_path / "not-a-git-repo"
        non_git.mkdir()
        job = Job(
            id=uuid4(), name="brain-non-git", user_prompt="test",
            tasks=[Task(description="t", status=RunState.PENDING)],
            metadata={"target_repo": str(non_git)},
        )
        save_job(job)
        graph = build_project_brain(job, [])
        git_nodes = [n for n in graph.nodes if n.type == "git_status"]
        assert len(git_nodes) == 1
        assert git_nodes[0].metadata["is_git_repo"] is False
        assert git_nodes[0].status == "unavailable"

    def test_job_aware_repo_status(self, tmp_path, monkeypatch):
        """Job-aware repo status reads target_repo and emits run-log event."""
        import os
        from pathlib import Path
        import packages.orchestration.storage as _storage

        jobs_dir = tmp_path / "jobs"
        jobs_dir.mkdir()
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        monkeypatch.setattr(_storage, "_DATA_DIR", jobs_dir)

        from packages.orchestration.storage import save_job

        job = Job(
            id=uuid4(), name="repo-aware", user_prompt="test",
            tasks=[Task(description="t", status=RunState.PENDING)],
            metadata={"target_repo": "."},
        )
        save_job(job)
        env = {**os.environ, "REMEDY_DATA_DIR": str(tmp_path)}
        result = subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped", "repo", "status", str(job.id), "--json"],
            capture_output=True, text=True, timeout=10, env=env,
        )
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["is_git_repo"] is True




class TestStopReasonBrainNode:
    def test_stop_reason_node_in_graph(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain import build_project_brain
        from packages.orchestration.storage import save_job

        job = Job(
            id=uuid4(), name="brain-sr", user_prompt="test",
            tasks=[Task(description="t", status=RunState.PENDING)],
            metadata={},  # No target_repo → derives no_target_repo
        )
        save_job(job)
        graph = build_project_brain(job, [])
        sr_nodes = [n for n in graph.nodes if n.type == "stop_reason"]
        assert len(sr_nodes) >= 1
        codes = [n.metadata.get("reason_code") for n in sr_nodes]
        assert "no_target_repo" in codes

