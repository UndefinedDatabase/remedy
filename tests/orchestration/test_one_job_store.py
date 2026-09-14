"""F275 T003: the classic job store is gone, and the one store left has no second name.

F260's Acceptance names two absences — the aliased resolver does not exist and nothing
imports it, and the two-stores phrase appears nowhere under ``packages/`` — and T003 deletes
the classic store module and its ``Job`` and ``Task`` models with them. Each absence is read
twice where it can come back two ways: from the imported module, which sees a name revived
by any route, and from the tracked source, which sees a use or a phrase nobody imports.

The deleted names are assembled from fragments on purpose: this file is tracked, so a
literal here would be a hit in every sweep that reads ``tests/``, this one included.
"""
from __future__ import annotations

import ast
import importlib
import importlib.util
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

STORE_MODULE = "packages.orchestration." + "storage"
ALIAS = "resolve_" + "any_job_id"
PHRASE = "two job " + "stores"
CLASSIC_MATCHER = "_classic_" + "job_id_matches"
ADAPTERS = ("_JobPlan" + "Adapter", "_JobPlan" + "TaskAdapter", "_is_" + "job_plan")
CLASSIC_MODELS = ("Job", "Task")


def _tracked(*pathspecs: str) -> list[Path]:
    out = subprocess.run(
        ["git", "ls-files", "--", *pathspecs],
        capture_output=True, text=True, cwd=REPO_ROOT, check=True,
    ).stdout
    return [REPO_ROOT / line for line in out.splitlines() if line]


def _files_containing(token: str, *pathspecs: str, casefold: bool = False) -> list[str]:
    hits = []
    for path in _tracked(*pathspecs):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if (token.lower() in text.lower()) if casefold else (token in text):
            hits.append(str(path.relative_to(REPO_ROOT)))
    return sorted(hits)


def _imports_of_classic_models(source: str) -> list[str]:
    """Every ``from packages.core.models import Job``/``Task`` in one source, by name."""
    found = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.ImportFrom) and node.module == "packages.core.models":
            found.extend(alias.name for alias in node.names if alias.name in CLASSIC_MODELS)
    return found


class TestTheClassicStoreIsGone:
    def test_the_store_module_is_not_on_disk_and_does_not_import(self):
        assert not (REPO_ROOT / Path(*STORE_MODULE.split("."))).with_suffix(".py").exists()
        assert importlib.util.find_spec(STORE_MODULE) is None

    def test_no_tracked_file_imports_the_store_module(self):
        assert _files_containing(STORE_MODULE, "packages", "apps", "tests", "scripts") == []

    def test_the_classic_models_are_not_attributes_of_the_models_module(self):
        models = importlib.import_module("packages.core.models")
        assert [name for name in CLASSIC_MODELS if hasattr(models, name)] == []
        assert hasattr(models, "Artifact"), (
            "hasattr found nothing on packages.core.models; the absence above would "
            "then be measuring an import failure"
        )

    def test_no_python_file_imports_a_classic_model(self):
        offenders = []
        for path in _tracked("*.py"):
            if not path.is_file():
                continue
            try:
                names = _imports_of_classic_models(path.read_text(encoding="utf-8"))
            except SyntaxError:
                continue
            offenders.extend(f"{path.relative_to(REPO_ROOT)}: {name}" for name in names)
        assert offenders == []

    def test_the_import_reading_sees_a_classic_model_import(self):
        """The discriminator: a planted import is found, a sibling import is not."""
        assert _imports_of_classic_models(
            "from packages.core.models import Artifact, " + "Job" + ", RunState\n"
        ) == ["Job"]
        assert _imports_of_classic_models("from packages.core.models import Artifact\n") == []


class TestTheResolverHasOneName:
    def test_the_alias_and_the_classic_matcher_are_not_attributes_of_data_paths(self):
        data_paths = importlib.import_module("packages.orchestration.data_paths")
        assert not hasattr(data_paths, ALIAS)
        assert not hasattr(data_paths, CLASSIC_MATCHER)
        assert hasattr(data_paths, "resolve_job_id"), (
            "hasattr found nothing on data_paths; the absences above would then be "
            "measuring an import failure"
        )

    def test_no_tracked_file_names_the_alias_or_the_classic_matcher(self):
        roots = ("packages", "apps", "tests", "scripts")
        assert _files_containing(ALIAS, *roots) == []
        assert _files_containing(CLASSIC_MATCHER, *roots) == []

    def test_the_sweep_reads_the_files_it_names(self):
        """Non-vacuity: the same sweep finds the live resolver where it is defined."""
        hits = _files_containing("def " + "resolve_job_id(", "packages", "apps", "tests", "scripts")
        assert hits == ["packages/orchestration/data_paths.py"]


class TestNoWhichStoreBranchSurvives:
    def test_the_two_stores_phrase_appears_nowhere_under_packages(self):
        assert _files_containing(PHRASE, "packages", casefold=True) == []

    def test_the_cockpit_adapters_are_gone(self):
        ui_server = importlib.import_module("packages.orchestration.ui_server")
        assert [name for name in ADAPTERS if hasattr(ui_server, name)] == []
        for name in ADAPTERS:
            assert _files_containing(name, "packages", "apps", "tests", "scripts") == [], name
        assert hasattr(ui_server, "_build_dashboard")
