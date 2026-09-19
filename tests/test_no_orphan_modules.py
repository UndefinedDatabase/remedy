"""No orphan modules: every production module has a non-test importer or an entry point.

WHAT THIS GUARDS. DECISION amend0905-vocab D11 (c), as T2_F271 Design (c) states
it: `tests/orchestration/test_import_reachability.py` asserts that nothing outside
its allowlist is REACHABLE from the six entry points; it does not assert that
every module IS reached. This file is the mirror. A module under `packages/`,
`apps/` or `scripts/` (other than an `__init__.py`) that nothing outside `tests/`
imports and no entry point names is an orphan — green, counted by coverage, and
serving no product path — and it reds `test_no_module_is_an_orphan`.

WHAT COUNTS AS REACHED. A module is reached when ANY of these names it:
- a static import in a non-test Python file under `packages/`, `apps/`,
  `scripts/` or the repository root — `import a.b`, `from a import b` (which
  reaches the submodule `a.b` through its package), and relative imports
  resolved against the importing file's package. Every import also reaches each
  ancestor package. A `scripts/` file runs with `scripts/` on `sys.path`, so its
  bare `import x` also reaches `scripts.x`;
- `importlib.import_module("<literal>")` or `spec_from_file_location(..., "<x>.py")`
  with a literal argument in such a file;
- the ENTRY-POINT rule: its repository path (`scripts/build_review_zip.py`) or
  its dotted `-m` name appears in `pyproject.toml`, in a `*.sh` at the root or
  under `scripts/`, or in a `.yml` / `.yaml` under `.github/`. `pyproject.toml`
  `[project.scripts]` values name their module as `module:function`.
Imports inside functions and `if TYPE_CHECKING:` count, as they do in the
reachability test: counting a module as reached when it might not be is the
harmless error for a guard whose remedy is deletion.

WHAT IS EXEMPT. Every `__init__.py`, which covers the documented reserved
namespaces of `tests/test_reserved_namespaces.py` — each is a docstring-only
`__init__.py`. `RESERVED_NAMESPACES` are trees that are not product modules at
all (a fixture project). `ALLOWED_UNWIRED` lists each module that
is deliberately without a production importer, with its one-line reason; an
entry whose module no longer exists, or which is no longer an orphan, reds
`test_every_allowed_unwired_entry_is_a_live_orphan`, so the list only shrinks.

WHAT THIS DOES NOT CATCH. An island — two modules importing only each other, or
an orphan's private helper — is reached by an importer that is itself unreached.
Only a closure from entry points measures that, which is the reachability
test's job, not this one's.
"""
from __future__ import annotations

import ast
import functools
import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

#: The trees whose modules must be reached.
SCANNED_ROOTS = ("packages", "apps", "scripts")

#: Directories never walked: caches, vendored or built trees, and worktrees.
SKIPPED_DIRS = frozenset({
    "__pycache__", "node_modules", ".venv", "venv", "dist", "build", ".git",
    ".remedy-wt", ".mypy_cache", ".ruff_cache", ".pytest_cache",
})

#: Trees that are not product modules, as repository-relative path prefixes.
RESERVED_NAMESPACES = (
    # A fixture project the gauntlet copies and runs; its modules are its own.
    "scripts/gauntlet_sample_project/",
)

#: Modules deliberately without a production importer: (repository path, reason).
ALLOWED_UNWIRED: tuple[tuple[str, str], ...] = (
    ("apps/cli/main.py",
     "the documented `python -m apps.cli.main` bridge the runtime process-boundary tests launch"),
    ("packages/contracts/interfaces.py",
     "Protocol contracts satisfied structurally, never imported; the kernel boundary architecture.md names"),
    ("packages/orchestration/autonomy_loop.py",
     "the sole token_policy_applied emitter, kept by DECISION F275 D18 as that event's test vehicle"),
    ("packages/orchestration/bench_run.py",
     "F082's on-demand bench run; never implicit by DECISION F082 D9, the one caller its guard permits"),
    ("packages/orchestration/ci_budgets.py",
     "the ceilings the `budgets` CI stage's tests/orchestration/test_ci_budgets.py compares (DECISION F083 D5)"),
    ("packages/orchestration/event_schemas.py",
     "the event metadata registry DECISION F275 D18 keeps for run logs already on disk"),
    ("packages/orchestration/feature_mission_adapter.py",
     "F080's feature-to-mission adapter; its consumer is the self-build loop F248 registers"),
    ("packages/orchestration/hunk_apply.py",
     "F033's hunk apply seam, unwired by design (F033 D4); forbidden by name in the command-channel guard"),
    ("packages/orchestration/role_conventions.py",
     "finding R-0981: F105 T002's conventions loaders, which no prompt builder registers yet"),
    ("packages/orchestration/self_use_findings.py",
     "run by hand in every closure, STATUS_closure_protocol.md precondition 6 (F258 T003)"),
    ("packages/orchestration/self_use_generator.py",
     "run by hand in every closure, STATUS_closure_protocol.md precondition 6 (F258 T001)"),
    ("packages/orchestration/self_use_runner.py",
     "run by hand in every closure, STATUS_closure_protocol.md precondition 6 (F258 T002); a D11 entry point"),
    ("scripts/remedy_agent_tooling_doctor.py",
     "run by hand after tooling changes, per .claude/skills/remedy-agent-tooling/SKILL.md"),
    ("scripts/rotate_live_review.py",
     "run by hand in every closure sequence, per docs/agents/self_drive_protocol.md"),
    ("scripts/self_run_gauntlet.py",
     "the gauntlet campaign CLI, run by hand (docs/adr/0001, gauntlet_evaluator.py names it)"),
)


def _walk_py(root: Path, rel: str):
    base = root / rel
    for current, dirs, files in os.walk(base):
        dirs[:] = sorted(d for d in dirs if d not in SKIPPED_DIRS)
        for name in sorted(files):
            if name.endswith(".py"):
                yield Path(current, name).relative_to(root).as_posix()


def _dotted(rel_path: str) -> str:
    dotted = rel_path[: -len(".py")].replace("/", ".")
    return dotted[: -len(".__init__")] if dotted.endswith(".__init__") else dotted


def _with_ancestors(dotted: str) -> set[str]:
    parts = dotted.split(".")
    return {".".join(parts[:i]) for i in range(1, len(parts) + 1)}


def _import_names(rel_path: str, tree: ast.AST) -> set[str]:
    """Every dotted name an import statement or a literal dynamic load in this file names."""
    own = _dotted(rel_path)
    package = own if rel_path.endswith("__init__.py") else own.rpartition(".")[0]
    file_dir = rel_path.rpartition("/")[0].replace("/", ".")
    named: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                named.add(alias.name)
                if file_dir:
                    named.add(f"{file_dir}.{alias.name}")
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                parts = package.split(".") if package else []
                parts = parts[: len(parts) - (node.level - 1)] if node.level > 1 else parts
                base = ".".join(parts + ([node.module] if node.module else []))
                bases = [base]
            else:
                bases = [node.module or ""]
                if file_dir and node.module:
                    bases.append(f"{file_dir}.{node.module}")
            for base in bases:
                named.add(base)
                for alias in node.names:
                    named.add(f"{base}.{alias.name}" if base else alias.name)
        elif isinstance(node, ast.Call) and node.args:
            func = node.func
            fname = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")
            first = node.args[0]
            if (fname == "import_module" and isinstance(first, ast.Constant)
                    and isinstance(first.value, str)):
                named.add(first.value)
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            # A SCRIPT launched or loaded by path: "scripts/x.py" names its repository
            # path, a bare "x.py" in a script names its sibling (os.path.join(HERE,
            # "x.py"), spec_from_file_location(..., "x.py")). Only scripts: a package
            # module is imported, and a path string naming one is data about it (a
            # scan table), not a use of it.
            if _PY_PATH.fullmatch(node.value):
                stem = node.value[: -len(".py")]
                dotted = stem.replace("/", ".") if "/" in stem else f"{file_dir}.{stem}"
                if dotted.startswith("scripts."):
                    named.add(dotted)
    return {name for part in named for name in _with_ancestors(part) if name}


_PY_PATH = re.compile(r"[\w/]+\.py")
_SH_SIBLING = re.compile(r"(?<![\w.-])(\w+)\.py\b")


def _entry_point_files(root: Path) -> list[Path]:
    """Every file the ENTRY-POINT rule reads."""
    paths = [root / "pyproject.toml", *sorted(root.glob("*.sh"))]
    for rel, patterns in (("scripts", ("*.sh",)), (".github", ("*.yml", "*.yaml"))):
        for pattern in patterns:
            paths.extend(sorted(
                p for p in (root / rel).rglob(pattern)
                if not SKIPPED_DIRS.intersection(p.relative_to(root).parts)))
    return [p for p in paths if p.is_file()]


def _entry_point_references(root: Path) -> tuple[str, set[str]]:
    """The entry-point files' joined text, and the sibling scripts a shell file launches.

    A shell file launches a sibling by its directory, not by its repository path —
    `"$(dirname "$0")/x.py"`, `"${SCRIPT_DIR}/x.py"` — so a `x.py` token in a
    `.sh` names the `x.py` beside it.
    """
    texts, siblings = [], set()
    for path in _entry_point_files(root):
        text = path.read_text(encoding="utf-8", errors="replace")
        texts.append(text)
        if path.suffix == ".sh":
            here = path.parent.relative_to(root).as_posix()
            for stem in _SH_SIBLING.findall(text):
                siblings.add(f"{here}/{stem}.py" if here != "." else f"{stem}.py")
    return "\n".join(texts), siblings


def find_orphans(root: Path) -> list[str]:
    """Repository paths of scanned modules that nothing outside `tests/` reaches."""
    targets = {}
    for rel in SCANNED_ROOTS:
        for path in _walk_py(root, rel):
            if path.endswith("__init__.py") or path.startswith(RESERVED_NAMESPACES):
                continue
            targets[path] = _dotted(path)
    importers = [p for rel in SCANNED_ROOTS for p in _walk_py(root, rel)]
    importers += sorted(p.name for p in root.glob("*.py"))
    reached: set[str] = set()
    for path in importers:
        source = (root / path).read_text(encoding="utf-8", errors="replace")
        try:
            tree = ast.parse(source, filename=path)
        except SyntaxError:
            continue
        reached |= _import_names(path, tree) - {_dotted(path)}
    entry_text, launched = _entry_point_references(root)
    orphans = []
    for path, dotted in sorted(targets.items()):
        if dotted in reached or path in launched:
            continue
        if path in entry_text or re.search(rf"(?<![\w.]){re.escape(dotted)}(?![\w])", entry_text):
            continue
        orphans.append(path)
    return orphans


def _allowed() -> dict[str, str]:
    return dict(ALLOWED_UNWIRED)


@functools.cache
def _repo_orphans() -> tuple[str, ...]:
    """The live tree's orphans, scanned once for the two tests that read them."""
    return tuple(find_orphans(REPO_ROOT))


def test_no_module_is_an_orphan():
    """D11 (c)'s mirror. A new module nothing imports reds here, naming itself."""
    unlisted = [p for p in _repo_orphans() if p not in _allowed()]
    assert not unlisted, (
        "These modules have no importer outside tests/ and no entry point names "
        "them. Wire each to a real entry point, delete it with its test, or add it "
        "to ALLOWED_UNWIRED with a one-line reason:\n" + "\n".join(unlisted))


def test_every_allowed_unwired_entry_is_a_live_orphan():
    """An entry for a deleted or since-wired module reds here, so the list only shrinks."""
    orphans = set(_repo_orphans())
    stale = [p for p in _allowed() if p not in orphans]
    assert not stale, (
        "These ALLOWED_UNWIRED entries name a module that is missing or now "
        "reached; remove them:\n" + "\n".join(stale))


def test_every_allowed_unwired_entry_carries_a_reason():
    paths = [p for p, _ in ALLOWED_UNWIRED]
    assert len(paths) == len(set(paths)), "duplicate ALLOWED_UNWIRED entry"
    for path, reason in ALLOWED_UNWIRED:
        assert reason.strip() and "\n" not in reason, path


def test_a_planted_orphan_is_reported_and_every_reaching_form_is_not(tmp_path):
    """The scanner's own red proof, standing: a synthetic tree with one orphan."""
    files = {
        "pyproject.toml": '[project.scripts]\ntool = "apps.cli_main:main"\n',
        "scripts/run.sh": (
            "python3 scripts/entry_script.py\n"
            "python3 -m packages.pkg.by_dash_m\n"
            'exec python3 "$(dirname "$0")/sibling_script.py"\n'),
        ".github/workflows/ci.yml": "run: python3 scripts/from_ci.py\n",
        "apps/__init__.py": "",
        "apps/cli_main.py": (
            '"""Prose naming scripts/prose_only.py does not reach it."""\n'
            "import importlib\n"
            "from packages.pkg import via_package\n"
            "from packages.pkg.sub import thing\n"
            "importlib.import_module('packages.pkg.dynamic')\n"
            'RUNNER = "scripts/by_path.py"\n'),
        "packages/__init__.py": "",
        "packages/pkg/__init__.py": "",
        "packages/pkg/via_package.py": "from . import relative\nfrom .inner import deep\n",
        "packages/pkg/relative.py": "",
        "packages/pkg/sub.py": "",
        "packages/pkg/inner/__init__.py": "",
        "packages/pkg/inner/deep.py": "from ..two_up import x\n",
        "packages/pkg/two_up.py": "x = 1\n",
        "packages/pkg/dynamic.py": "",
        "packages/pkg/by_dash_m.py": "",
        "packages/pkg/planted_orphan.py": "X = 1\n",
        "scripts/entry_script.py": "import helper_mod\n",
        "scripts/helper_mod.py": "",
        "scripts/from_ci.py": "",
        "scripts/sibling_script.py": "",
        "scripts/by_path.py": "",
        "scripts/prose_only.py": "",
        "scripts/gauntlet_sample_project/app.py": "",
        "tests/test_planted.py": "from packages.pkg import planted_orphan\n",
    }
    for rel, text in files.items():
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    assert find_orphans(tmp_path) == [
        "packages/pkg/planted_orphan.py", "scripts/prose_only.py"]
