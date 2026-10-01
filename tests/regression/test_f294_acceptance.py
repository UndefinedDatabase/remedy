"""F294 (Test load diet, part two): its cuts came "without losing a single assertion" (R-1126).

F293's floor in `tests/regression/test_f293_acceptance.py` lists only the test modules F293 changed,
so an assertion deleted from a module F294 changed turned nothing red; the feature's acceptance
audit (operator amendment amend0930b-slow-cap) showed it. This file keeps F293's two checks for
F294's modules, with the same counter and the same reading of a unit.
"""
from __future__ import annotations

import pytest

from tests.regression.test_f293_acceptance import REPO_ROOT, _assertions, _digest, _git, _units

#: Assertions (``assert`` statements, and ``pytest.raises`` / ``pytest.warns`` uses) in every test
#: module F294 changed, counted at `020bc9a16`, where F294 left main. A module never has fewer.
#: A later change that removes one on purpose lowers its number here in the same commit, with the
#: reason.
FLOOR = {
    "tests/cli/test_golden_path.py": (144, 0),
    "tests/cli/test_scoped_listings.py": (69, 0),
    "tests/conftest.py": (0, 0),
    "tests/orchestration/test_run_manifest_integrity.py": (26, 4),
    "tests/test_data_root_isolation.py": (6, 0),
}

#: Where F294 left main, and F294's first commit: while main does not hold that commit, F294 is
#: open and every function, method and assignment that existed where it began in a module of
#: `FLOOR` must still be there word for word, or be a reviewed change.
FORK = "020bc9a168783d5a56f2f5aaa9ece76ff359c7aa"
F294_FIRST_COMMIT = "8cc92d4e3ad33aad972dd0716e2cd8204d167f67"
#: The units F294 changed on purpose: the first 16 hex digits of the sha256 of the text the
#: reviewer read (as `ast.unparse` writes it), and why. A further change needs a new review here.
REVIEWED_CHANGES = {
    "tests/cli/test_golden_path.py": {
        "_init_project": ("cbe56d62d296efd6", "round 4: run in this process (D4)"),
        "_run_do": ("57f26ccb47d54484", "round 4: run in this process (D4)"),
        "_run_status": ("734d06f2a74e4abd", "round 4: run in this process (D4)"),
    },
    "tests/cli/test_scoped_listings.py": {
        "_init_project": ("65d1bcdadb512ead", "round 5: setup run in this process (D5)"),
        "_create_job": ("30b4822c10de8004", "round 5: setup run in this process (D5)"),
        "_get_project_slug": ("e7a65d8276332cf6", "round 5: setup run in this process (D5)"),
    },
    "tests/conftest.py": {
        "_isolated_data_root": ("15c92815491d5d0e", "round 2: the root comes from one parent (D2)"),
    },
}


class TestNoAssertionWasLost:
    """Goal & Done: the cuts came "without losing a single assertion" (R-1126)."""

    def test_no_module_f294_changed_has_fewer_assertions_than_where_f294_began(self):
        short = {}
        for path, floor in FLOOR.items():
            now = _assertions((REPO_ROOT / path).read_text(encoding="utf-8"))
            if now[0] < floor[0] or now[1] < floor[1]:
                short[path] = {"now": now, "floor": floor}
        assert short == {}


class TestNoAssertionWasWeakened:
    """Goal & Done, read for content: no test code that existed where F294 began was changed, so
    no assertion was emptied, weakened or starved of what it checks, except `REVIEWED_CHANGES`
    (R-1126). The claim is about F294's own changes, so the check runs while F294 is open, its
    closure's suite and its pull request included, and says it is skipped once main holds F294
    or the checkout has no history back to where F294 began."""

    def test_every_unit_that_existed_where_f294_began_is_unchanged_or_reviewed(self):
        if _git("cat-file", "-e", FORK + "^{commit}").returncode != 0:
            pytest.skip("this checkout has no history back to where F294 began")
        if _git("merge-base", "--is-ancestor", F294_FIRST_COMMIT, "origin/main").returncode == 0:
            pytest.skip("main holds F294, so its own changes are history")
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
