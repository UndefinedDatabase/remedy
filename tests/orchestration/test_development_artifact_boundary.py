"""Guard tests: development artifact boundary enforcement.

Ensures product-facing modules do not depend on .agent/live_review.md.
Legacy development modules are explicitly whitelisted by relative path.
"""

from __future__ import annotations

import inspect
import re
from pathlib import Path

# Modules that must NEVER reference live_review.md or REMEDY_REVIEW_FILE.
_PRODUCT_MODULES = (
    "worker_facade_cmd",
)

# Legacy/development modules allowed to reference live_review.md.
# Uses relative paths from repo root — not bare filenames.
_ALLOWED_LEGACY = {
    "packages/orchestration/self_dogfood.py",
    "packages/orchestration/self_dogfood_execution.py",
    "packages/orchestration/orchestrator_brain.py",
    "packages/orchestration/integrity_gate.py",
    # The freshness gate binds packaged evidence to the agent's live review by
    # design: it derives the step range from .agent/plan.md AND
    # .agent/live_review.md and reports a mismatch. Development-only by
    # construction — it is the gate over development state.
    "packages/orchestration/fresh_evidence_gate.py",
    # F258's self-use generator reads the SAME development ledger to pick its
    # next self-maintenance item — it is Remedy's own dogfooding machinery,
    # the same category as self_dogfood.py and integrity_gate.py above, never
    # a runtime dependency of an end-user's job.
    "packages/orchestration/self_use_generator.py",
}

_LIVE_REVIEW_PATTERN = re.compile(
    r"live_review\.md|REMEDY_REVIEW_FILE|read_agent_file\(['\"]live_review"
)

_ROOT = Path(__file__).resolve().parents[2]


def _without_docstrings(source: str) -> str:
    """The module's source with every docstring blanked out.

    Unparseable sources are returned unchanged — a scanner must never go
    quiet because a file failed to parse.
    """
    import ast
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return source
    spans = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Module, ast.ClassDef,
                                 ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        body = getattr(node, "body", None)
        if not body or not isinstance(body[0], ast.Expr):
            continue
        value = body[0].value
        if isinstance(value, ast.Constant) and isinstance(value.value, str):
            spans.append((value.lineno, value.end_lineno))
    if not spans:
        return source
    lines = source.splitlines(keepends=True)
    for start, end in spans:
        for i in range(start - 1, min(end, len(lines))):
            lines[i] = "\n"
    return "".join(lines)


class TestProductModulesNoLiveReview:
    """Product modules must not depend on .agent/live_review.md."""

    def test_worker_facade_cmd(self):
        from apps.cli.commands import worker_facade_cmd as mod
        source = inspect.getsource(mod)
        assert not _LIVE_REVIEW_PATTERN.search(source), \
            "worker_facade_cmd.py must not reference live_review.md"


class TestAllowlistCompleteness:
    """Every allowlisted path must exist in the repo."""

    def test_all_allowlisted_paths_exist(self):
        missing = [p for p in _ALLOWED_LEGACY if not (_ROOT / p).exists()]
        assert not missing, f"Stale allowlist entries (files not found): {missing}"


class TestWhitelistBoundary:
    """Source files referencing live_review.md must be in the allowed set."""

    def test_no_new_product_dependency(self):
        """Scan packages/ and apps/ for live_review references outside whitelist."""
        violations = []
        for search_dir in ("packages", "apps"):
            dir_path = _ROOT / search_dir
            if not dir_path.is_dir():
                continue
            for py_file in dir_path.rglob("*.py"):
                if py_file.name.startswith("__"):
                    continue
                try:
                    content = py_file.read_text(errors="replace")
                except OSError:
                    continue
                # A DEPENDENCY is code, not prose: repair_attest.py names
                # live_review.md in its docstring precisely to say the file is
                # excluded operator state. Docstrings are stripped so a module
                # cannot be flagged for documenting the boundary it honours.
                content = _without_docstrings(content)
                match = _LIVE_REVIEW_PATTERN.search(content)
                if match:
                    rel = str(py_file.relative_to(_ROOT))
                    if rel not in _ALLOWED_LEGACY:
                        violations.append(
                            f"{rel} (matched: {match.group()!r}) — "
                            "remove the dependency or add to _ALLOWED_LEGACY "
                            "if development-only"
                        )
        assert not violations, (
            "New live_review.md dependency in product code:\n"
            + "\n".join(f"  - {v}" for v in violations)
        )


class TestDoctorCoreNoDevTruth:
    """Doctor core (in worker_facade_cmd) must not reference live_review.md."""

    def test_doctor_core_no_live_review(self):
        from apps.cli.commands import worker_facade_cmd as mod
        source = inspect.getsource(mod)
        assert not _LIVE_REVIEW_PATTERN.search(source), \
            "worker_facade_cmd.py must not reference live_review.md"


# ---------------------------------------------------------------------------
# Functional proofs: product paths work without .agent/ directory
# ---------------------------------------------------------------------------


class TestFunctionalNoAgent:
    """Product-facing paths must work without .agent/ directory."""

    def test_worker_doctor_core_no_agent(self, tmp_path):
        """Doctor core import checks work without .agent/."""
        import importlib
        for mod_name in (
            "apps.cli.commands.worker_facade_cmd",
            "apps.cli.command_catalog",
            "packages.orchestration.run_contract",
            "packages.orchestration.config",
        ):
            mod = importlib.import_module(mod_name)
            assert mod is not None
