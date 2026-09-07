"""F272 T004 — no production site reads the RETIRED ``status`` spelling off a JobPlan.

F272 round 9 renamed ``JobPlan.status`` to ``JobPlan.state`` (DECISION F272 D6,
move two). DECISION F272 D7 measured that rename's site set by running the
suites against a raising ``status`` property, which is the only method that can
see a polymorphic attribute — and it is blind to exactly one shape: a read that
NAMES the attribute as a string and supplies a default. ``getattr(job,
"status", "")`` raises nothing when the field is gone; it quietly answers with
the default, so the probe stayed green while two production guards stopped
working.

Both survivors were found at ``67515ab7`` and are fixed in the same commit as
this file:

* ``apps/cli/commands/do_cmd.py`` refused budget flags on a STOPPED job. With
  the dead read the comparison was ``"" == "stopped"``, so the refusal never
  fired and ``remedy do job-run --max-cost-usd`` silently re-ran a stopped job
  under new limits — the exact override F018 put that guard there to prevent.
* ``packages/orchestration/job_evidence.py``'s ``_linked_job_summary`` reported
  ``status: "unknown"`` for every linked job, including jobs that loaded
  perfectly, contradicting its own docstring, which reserves ``unknown`` for a
  job that is UNAVAILABLE.

This test is the standing guard the probe cannot be. It reads every tracked
``.py`` file under ``packages/`` and ``apps/`` with ``ast``, finds the locals
bound from ``load_job_plan(...)`` in each function scope, and fails on any read
of ``status`` off one of them — whether spelled as an attribute or as a
``getattr`` string. A file is enumerated from ``git ls-files`` and never from a
shell glob, per DECISION F272 D2.
"""
from __future__ import annotations

import ast
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

#: The retired spelling. ``state`` is the live one.
RETIRED_FIELD = "status"

#: The loader whose return value is a ``JobPlan``.
JOB_PLAN_LOADER = "load_job_plan"


def _tracked_production_python_files() -> list[Path]:
    """Every tracked ``.py`` under ``packages/`` and ``apps/`` — never a glob."""
    out = subprocess.run(
        ["git", "ls-files", "--", "packages/*.py", "apps/*.py",
         "packages/**/*.py", "apps/**/*.py"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout.split()
    return [REPO_ROOT / rel for rel in sorted(set(out))]


class _RetiredReadFinder(ast.NodeVisitor):
    """Collect reads of the retired field off a local bound from the loader."""

    def __init__(self, rel_path: str) -> None:
        self.rel_path = rel_path
        self.findings: list[str] = []

    def _scope(self, node: ast.AST) -> None:
        # Locals in THIS scope that were bound from the JobPlan loader.
        bound: set[str] = set()
        for sub in ast.walk(node):
            if not isinstance(sub, ast.Assign):
                continue
            call = sub.value
            if not isinstance(call, ast.Call):
                continue
            fn = call.func
            name = fn.attr if isinstance(fn, ast.Attribute) else getattr(fn, "id", "")
            if name != JOB_PLAN_LOADER:
                continue
            for target in sub.targets:
                if isinstance(target, ast.Name):
                    bound.add(target.id)
        if not bound:
            return
        for sub in ast.walk(node):
            # `job.status`
            if (
                isinstance(sub, ast.Attribute)
                and sub.attr == RETIRED_FIELD
                and isinstance(sub.value, ast.Name)
                and sub.value.id in bound
            ):
                self.findings.append(
                    f"{self.rel_path}:{sub.lineno}: {sub.value.id}.{RETIRED_FIELD}"
                )
            # `getattr(job, "status", ...)`
            if (
                isinstance(sub, ast.Call)
                and isinstance(sub.func, ast.Name)
                and sub.func.id == "getattr"
                and len(sub.args) >= 2
                and isinstance(sub.args[0], ast.Name)
                and sub.args[0].id in bound
                and isinstance(sub.args[1], ast.Constant)
                and sub.args[1].value == RETIRED_FIELD
            ):
                self.findings.append(
                    f'{self.rel_path}:{sub.lineno}: '
                    f'getattr({sub.args[0].id}, "{RETIRED_FIELD}", ...)'
                )

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._scope(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._scope(node)
        self.generic_visit(node)


def scan_retired_job_plan_state_reads() -> list[str]:
    """Every production read of the retired field off a loaded JobPlan."""
    findings: list[str] = []
    for path in _tracked_production_python_files():
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (OSError, SyntaxError):
            continue
        finder = _RetiredReadFinder(str(path.relative_to(REPO_ROOT)))
        finder.visit(tree)
        findings.extend(finder.findings)
    return sorted(findings)


class TestNoRetiredJobPlanStateReads:
    def test_the_scan_reaches_a_real_corpus(self) -> None:
        """Anti-blindness: a scan over nothing would pass for the wrong reason."""
        files = _tracked_production_python_files()
        assert len(files) > 300, f"corpus collapsed to {len(files)} files"

    def test_the_scan_sees_a_retired_read_when_one_is_there(self) -> None:
        """The discriminator: the finder is not vacuously empty."""
        source = (
            "def f(jid):\n"
            "    j = load_job_plan(jid)\n"
            "    return getattr(j, 'status', '')\n"
        )
        finder = _RetiredReadFinder("synthetic.py")
        finder.visit(ast.parse(source))
        assert len(finder.findings) == 1, finder.findings

    def test_no_production_site_reads_the_retired_status_off_a_job_plan(self) -> None:
        found = scan_retired_job_plan_state_reads()
        assert found == [], (
            "a production site reads the retired `status` spelling off a JobPlan; "
            "F272 round 9 renamed that field to `state`, and a `getattr` with a "
            "default answers silently instead of raising — read `.state` "
            "instead:\n  " + "\n  ".join(found)
        )
