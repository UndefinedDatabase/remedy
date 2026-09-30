"""F293 (Test load diet): two acceptance lines that only the repository itself can show.

T001's inventory holds its six readings, drawn from its one full-suite run (R-1121), and the diet
cut CPU "without losing a single assertion" in any test module it changed (R-1122). Both were
found unguarded by the feature's acceptance audit (operator amendment amend0930b-slow-cap).
"""
from __future__ import annotations

import ast
import hashlib
import re
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
INVENTORY = REPO_ROOT / ".agent" / "f293_inventory.md"
DURATIONS = REPO_ROOT / ".agent" / "authored" / "f293-r1-durations.txt"
READINGS = ("## 1. Cost of collection", "## 2. CPU share per test file", "## 3. The 100 slowest tests",
            "## 4. Tests that start a child process", "## 5. UI builds and Chrome starts",
            "## 6. Processes alive after the run")
ROW = re.compile(r"^\| (\d+) \| (\d+\.\d\d) \| (setup|call|teardown) \| `([^`]+)` \|$", re.MULTILINE)

#: Assertions (``assert`` statements, and ``pytest.raises`` / ``pytest.warns`` uses) in every test
#: module F293 changed, counted at `8a067a3b9`, where F293 left main. A module never has fewer.
#: A later change that removes one on purpose lowers its number here in the same commit, with the
#: reason, as `ALLOWED_REMOVALS` does.
FLOOR = {
    "tests/cli/test_mission_cmd.py": (271, 0),
    "tests/cli/test_worker_facade_cmd.py": (148, 4),
    "tests/orchestration/test_dead_command_check.py": (3, 0),
    "tests/orchestration/test_job_budgets.py": (225, 43),
    "tests/orchestration/test_job_task_runner.py": (525, 2),
    "tests/orchestration/test_review_gate_sensitive_metadata.py": (8, 0),
    "tests/orchestration/test_run_manifest_security.py": (13, 3),
    "tests/regression/test_test_load_governor.py": (47, 0),
    "tests/runtimes/test_dev_server.py": (64, 6),
    "tests/test_no_orphan_modules.py": (8, 0),
}
#: F293 round 6 wrote five setup helpers' records in-process; each had asserted only that the
#: child process writing the record exited 0 (`assert proc.returncode == 0, proc.stderr`). The
#: in-process call raises when the write fails, so the check is in the call (DECISION F293 D11).
ALLOWED_REMOVALS = {"tests/cli/test_mission_cmd.py": (5, 0)}

#: Where F293 left main, and F293's first commit: while main does not hold that commit, F293 is
#: open and every function, method and assignment that existed where it began in a module of
#: `FLOOR` must still be there word for word, or be a reviewed change (R-1123).
FORK = "8a067a3b93fb3d7080053f9cf742379534bed447"
F293_FIRST_COMMIT = "6d51c38a920dfaa10d9f3ad138e8c9993987e685"
#: The units F293 changed on purpose: the first 16 hex digits of the sha256 of the text the
#: reviewer read (as `ast.unparse` writes it), and why. A further change needs a new review here.
REVIEWED_CHANGES = {
    "tests/cli/test_mission_cmd.py": {
        "_make_project": ("853ad7df90af628b", "round 6: setup written in-process (D11)"),
        "_start": ("856d4264c8563d9a", "round 13: setup mission created in-process (D10)"),
        "_link_job": ("19624b4d69e31fde", "round 6: setup written in-process (D11)"),
        "_pending_plan_job": ("dbe51ae27a9c932d", "round 6: setup written in-process (D11)"),
        "TestContinue._green_job": ("0bbfa02ede11e1f4", "round 6: setup written in-process (D11)"),
        "_append_trip_entry": ("0b74219dc57308a1", "round 6: setup written in-process (D11)"),
    },
    "tests/cli/test_worker_facade_cmd.py": {
        "TestDoctorCoreReportFunction.test_report_as_json_matches_the_commands_own_json_output_in_the_same_run": (
            "30582ae1b10f778a", "round 10: the exact key list gained `test_load` (D7)"),
        "TestDoctorCoreReportFunction.test_as_json_key_order": (
            "ec1b11fc4040cb39", "round 10: the exact key list gained `test_load` (D7)"),
    },
    "tests/orchestration/test_job_budgets.py": {
        "TestOnProviderAttemptCallback.test_callback_fires_on_retry": (
            "e9c90e73771838c7", "round 4: the real 30-second retry wait is patched out"),
    },
    "tests/orchestration/test_job_task_runner.py": {
        "TestProviderOverrideToFake.test_cli_handler_provider_override": (
            "9378594c041b797e", "round 3: the paid claude-cli call is faked (R-1119)"),
        "TestCommandPathExplicitOverrides.test_provider_override_to_fake": (
            "6a06a59c67bba9d4", "round 3: the paid claude-cli call is faked (R-1119)"),
    },
    "tests/runtimes/test_dev_server.py": {
        "TestReadiness.test_readiness_timeout_stops_the_tree_and_leaves_no_state": (
            "877302d122811168", "round 11: a failed setup still stops the helper (D8)"),
    },
    "tests/test_no_orphan_modules.py": {
        "ALLOWED_UNWIRED": ("47c40138ffbb1633", "round 12: `scripts/closure_suite_cost.py` joins (D9)"),
    },
}


def _section(text: str, heading: str) -> str:
    start = text.index(heading)
    following = [text.find(h, start + 1) for h in READINGS if text.find(h, start + 1) > start]
    return text[start:min(following, default=len(text))]


def _assertions(source: str) -> tuple[int, int]:
    tree = ast.parse(source)
    asserts = sum(isinstance(node, ast.Assert) for node in ast.walk(tree))
    raises = sum(isinstance(node, ast.Attribute) and node.attr in ("raises", "warns")
                 for node in ast.walk(tree))
    return asserts, raises


class TestTheInventoryHoldsItsSixReadings:
    """T001: `.agent/f293_inventory.md` exists and holds the six readings from one run (R-1121)."""

    def test_the_six_readings_are_there_in_order(self):
        text = INVENTORY.read_text(encoding="utf-8")
        positions = [text.find(heading) for heading in READINGS]
        assert -1 not in positions, [h for h, p in zip(READINGS, positions) if p == -1]
        assert positions == sorted(positions)

    def test_the_slowest_tests_are_a_hundred_rows_of_the_one_run(self):
        text = INVENTORY.read_text(encoding="utf-8")
        rows = ROW.findall(_section(text, READINGS[2]))
        assert [int(rank) for rank, *_ in rows] == list(range(1, 101))
        run = DURATIONS.read_text(encoding="utf-8")
        missing = [node for _rank, seconds, phase, node in rows
                   if not re.search(rf"^{re.escape(seconds)}s {phase} +{re.escape(node)}$", run, re.MULTILINE)]
        assert missing == []

    def test_the_totals_are_the_record_of_that_run(self):
        text = " ".join(INVENTORY.read_text(encoding="utf-8").split())
        assert "`collected` 21102, `wall_seconds` 355.02, `cpu_seconds` 1246.09" in text
        summary = DURATIONS.read_text(encoding="utf-8").strip().splitlines()[-1]
        passed, skipped = (int(n) for n in re.match(r"(\d+) passed, (\d+) skipped", summary).groups())
        assert passed + skipped == 21102


class TestNoAssertionWasLost:
    """Goal & Done: the cut came "without losing a single assertion" (R-1122)."""

    def test_no_module_f293_changed_has_fewer_assertions_than_where_f293_began(self):
        short = {}
        for path, (asserts, raises) in FLOOR.items():
            allowed = ALLOWED_REMOVALS.get(path, (0, 0))
            now = _assertions((REPO_ROOT / path).read_text(encoding="utf-8"))
            if now[0] < asserts - allowed[0] or now[1] < raises - allowed[1]:
                short[path] = {"now": now, "floor": (asserts - allowed[0], raises - allowed[1])}
        assert short == {}

    def test_the_counter_sees_both_kinds(self):
        source = "import pytest\n\ndef test_x():\n    assert 1\n    with pytest.raises(ValueError):\n        int('x')\n"
        assert _assertions(source) == (1, 1)


def _git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(REPO_ROOT), *args], capture_output=True, text=True, timeout=60)


def _units(source: str) -> dict[str, str]:
    """Each function and method by its qualified name, each assignment by its targets, and each
    other statement outside a function by its own text, mapped to its text as `ast.unparse`
    writes it. Imports and docstrings are left out; so are comments, which `ast` does not keep."""
    found: dict[str, str] = {}

    def walk(body, prefix):
        for node in body:
            if isinstance(node, (ast.Import, ast.ImportFrom)) or (
                    isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant)
                    and isinstance(node.value.value, str)):
                continue
            text = ast.unparse(node)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                found[prefix + node.name] = text
            elif isinstance(node, ast.ClassDef):
                walk(node.body, prefix + node.name + ".")
            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                found[prefix + ", ".join(ast.unparse(t) for t in targets)] = text
            else:
                found[prefix + text] = text

    walk(ast.parse(source).body, "")
    return found


def _digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


class TestNoAssertionWasWeakened:
    """Goal & Done, read for content: no test code that existed where F293 began was changed, so
    no assertion was emptied, weakened or starved of what it checks, except `REVIEWED_CHANGES`
    (R-1123). The claim is about F293's own changes, so the check runs while F293 is open, its
    closure's suite and its pull request included, and says it is skipped once main holds F293
    or the checkout has no history back to where F293 began."""

    def test_every_unit_that_existed_where_f293_began_is_unchanged_or_reviewed(self):
        if _git("cat-file", "-e", FORK + "^{commit}").returncode != 0:
            pytest.skip("this checkout has no history back to where F293 began")
        if _git("merge-base", "--is-ancestor", F293_FIRST_COMMIT, "origin/main").returncode == 0:
            pytest.skip("main holds F293, so its own changes are history")
        changed = {}
        for path in FLOOR:
            before = _units(_git("show", f"{FORK}:{path}").stdout)
            now = _units((REPO_ROOT / path).read_text(encoding="utf-8"))
            reviewed = REVIEWED_CHANGES.get(path, {})
            unreviewed = [key for key, text in before.items() if now.get(key) != text
                          and not (key in now and key in reviewed and _digest(now[key]) == reviewed[key][0])]
            if unreviewed:
                changed[path] = unreviewed
        assert changed == {}

    def test_a_statement_that_feeds_an_unchanged_assertion_changes_its_function(self):
        before = _units("def test_x():\n    listing = run()\n    assert 'a' in listing\n")
        after = _units("def test_x():\n    listing = run()\n    listing += 'a'\n    assert 'a' in listing\n")
        assert set(before) == set(after) == {"test_x"}
        assert before["test_x"] != after["test_x"]
