"""F293 (Test load diet): two acceptance lines that only the repository itself can show.

T001's inventory holds its six readings, drawn from its one full-suite run (R-1121), and the diet
cut CPU "without losing a single assertion" in any test module it changed (R-1122). Both were
found unguarded by the feature's acceptance audit (operator amendment amend0930b-slow-cap).
"""
from __future__ import annotations

import ast
import re
import subprocess
from collections import Counter
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
#: open and every assertion that existed where it began must still be there, word for word (R-1123).
FORK = "8a067a3b93fb3d7080053f9cf742379534bed447"
F293_FIRST_COMMIT = "6d51c38a920dfaa10d9f3ad138e8c9993987e685"
#: The assertions F293 changed on purpose, as `ast.unparse` writes them, with how many times.
ALLOWED_CHANGES = {
    # The five setup checks of `ALLOWED_REMOVALS` (DECISION F293 D11).
    "tests/cli/test_mission_cmd.py": {"assert proc.returncode == 0, proc.stderr": 5},
    # Round 10 added `test_load` to doctor core's exact key list, a stricter check (DECISION F293 D7).
    "tests/cli/test_worker_facade_cmd.py": {
        "assert list(result.keys()) == ['ready', 'checks', 'blockers', 'warnings', 'dead_commands', 'disk']": 1},
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


def _checks(source: str) -> Counter:
    """Every assertion of a module as `ast.unparse` writes it: `assert` statements, and
    `pytest.raises` / `pytest.warns` calls with their arguments."""
    found: Counter = Counter()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Assert) or (
                isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr in ("raises", "warns")):
            found[ast.unparse(node)] += 1
    return found


class TestNoAssertionWasWeakened:
    """Goal & Done, read for content: no assertion that existed where F293 began was changed or
    gutted, except `ALLOWED_CHANGES` (R-1123). The claim is about F293's own changes, so the check
    runs while F293 is open, its closure's suite and its pull request included, and says it is
    skipped once main holds F293 or the checkout has no history back to where F293 began."""

    def test_every_assertion_that_existed_where_f293_began_is_still_there_word_for_word(self):
        if _git("cat-file", "-e", FORK + "^{commit}").returncode != 0:
            pytest.skip("this checkout has no history back to where F293 began")
        if _git("merge-base", "--is-ancestor", F293_FIRST_COMMIT, "origin/main").returncode == 0:
            pytest.skip("main holds F293, so its own changes are history")
        changed = {}
        for path in FLOOR:
            before = _checks(_git("show", f"{FORK}:{path}").stdout)
            now = _checks((REPO_ROOT / path).read_text(encoding="utf-8"))
            gone = (before - now) - Counter(ALLOWED_CHANGES.get(path, {}))
            if gone:
                changed[path] = sorted(gone)
        assert changed == {}

    def test_a_gutted_assertion_is_no_longer_the_same_check(self):
        before = _checks("def test_x():\n    assert value == 3, 'three'\n")
        after = _checks("def test_x():\n    assert True, 'three'\n")
        assert before - after == Counter({"assert value == 3, 'three'": 1})
