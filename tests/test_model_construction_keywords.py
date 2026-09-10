"""Every keyword passed to a core model is a field that model declares.

pydantic v2 defaults to ``extra="ignore"``, so ``Task(type="write_readme")`` constructs
happily and DROPS the keyword. A test that writes one believes it set something and did
not. F275 round 44 measured forty such keywords across the suite — `Job(permissions=...)`
and `Job(prompt=...)`, `Task(task_type=...)`, `Task(type=...)` and `Task(title=...)`, every
one in a test file and none in production — and four of them also blocked the
classic-to-unified record flip, because `Task(title=..., description=...)` becomes
``TaskEntry(title=..., title=...)`` once `description` maps onto `title`, which does not
compile.

This guard exists so the class cannot come back silently. It is deliberately a SOURCE sweep
rather than a runtime check: the defect is invisible at runtime by construction, which is
what made it survive.
"""
from __future__ import annotations

import ast
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

# The models whose constructions are swept, by the name a caller writes. Each maps to the
# import path that owns it, so the declared-field set is read from the SHIPPED class and
# never from a list kept here — a list would be the second place a field has to be added.
SWEPT_MODELS = {
    "Job": ("packages.core.models", "Job"),
    "Task": ("packages.core.models", "Task"),
}


def _declared_fields(module_path: str, class_name: str) -> set[str]:
    import importlib

    model = getattr(importlib.import_module(module_path), class_name)
    return set(model.model_fields)


def _tracked_python_files() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files", "*.py"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        check=True,
    ).stdout
    return [line for line in out.split() if line]


def _called_name(node: ast.Call) -> str | None:
    func = node.func
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return None


def _undeclared_keyword_sites() -> list[str]:
    declared = {
        name: _declared_fields(*target) for name, target in SWEPT_MODELS.items()
    }
    offenders: list[str] = []
    for rel in _tracked_python_files():
        try:
            source = (REPO_ROOT / rel).read_bytes()
            tree = ast.parse(source, filename=rel)
        except (SyntaxError, OSError):
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            called = _called_name(node)
            if called not in declared:
                continue
            for keyword in node.keywords:
                if keyword.arg and keyword.arg not in declared[called]:
                    offenders.append(
                        f"{rel}:{node.lineno} {called}({keyword.arg}=...) "
                        f"is not a field of {called}"
                    )
    return sorted(offenders)


class TestEveryConstructionKeywordIsADeclaredField:
    def test_no_tracked_file_passes_an_undeclared_keyword(self) -> None:
        offenders = _undeclared_keyword_sites()
        assert offenders == [], (
            "these constructions pass a keyword the model does not declare, so pydantic "
            "drops it silently and the call does not do what it says:\n  "
            + "\n  ".join(offenders)
        )

    @pytest.mark.parametrize("model_name", sorted(SWEPT_MODELS))
    def test_the_sweep_reads_a_nonempty_field_set_for_each_model(
        self, model_name: str
    ) -> None:
        """A guard over an empty field set would pass by looking at nothing."""
        fields = _declared_fields(*SWEPT_MODELS[model_name])
        assert fields, f"{model_name} declares no fields; the sweep above is vacuous"

    def test_the_sweep_actually_reads_files(self) -> None:
        """And a guard over an empty file list would pass the same way."""
        assert len(_tracked_python_files()) > 500

    def test_an_undeclared_keyword_really_is_dropped_rather_than_rejected(self) -> None:
        """The premise, pinned: this is why the defect is invisible at runtime."""
        from packages.core.models import Task

        task = Task(description="d", type="write_readme")
        assert not hasattr(task, "type")
        assert task.model_extra is None
