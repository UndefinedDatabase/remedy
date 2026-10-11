"""F293 T003 (DECISION F293 D9): each closure's suite transcript records its CPU seconds, and a
closure costing more than 10 percent above the previous feature's says that a finding is owed.

``scripts/closure_suite_cost.py`` reads the test load record ``tests/conftest.py`` writes and the
closure transcripts under ``.agent/authored/``; every test here builds both in ``tmp_path``.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import scripts.closure_suite_cost as cost

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "closure_suite_cost.py"


def _row(command="pytest -n auto -q", cpu=1000.0, utc="2026-10-02T10:00:00Z", **extra):
    return {"command": command, "cpu_seconds": cpu, "utc": utc, "wall_seconds": 400.0,
            "collected": 21000, "exit_status": 0, "workers": 6, **extra}


def _record(tmp_path, *rows, raw=()):
    path = tmp_path / "test_load.jsonl"
    path.write_text("".join(json.dumps(r) + "\n" for r in rows) + "".join(line + "\n" for line in raw),
                    encoding="utf-8")
    return path


def _transcript(authored, feature, cpu, utc):
    authored.mkdir(exist_ok=True)
    line = cost.transcript_line({"cpu_seconds": cpu, "wall_seconds": 300.0, "collected": 20000,
                                 "exit_status": 0, "utc": utc})
    (authored / f"{feature}-closure-suite.txt").write_text(
        f"Command: python3 -m pytest -n auto -q\n{line}\nSome other sentence.\n", encoding="utf-8")


class TestTheRunIsTheNewestFullSuiteLine:
    def test_other_commands_and_lines_that_do_not_parse_are_skipped(self, tmp_path):
        record = _record(
            tmp_path,
            _row(cpu=900.0, utc="2026-10-01T10:00:00Z"),
            _row(cpu=1100.0, utc="2026-10-02T10:00:00Z"),
            _row(command="pytest -n auto -q --durations=0", cpu=5000.0, utc="2026-10-03T10:00:00Z"),
            _row(command="pytest tests/cli -q -n auto", cpu=7.0, utc="2026-10-04T10:00:00Z"),
            _row(cpu=9999.0, utc="yesterday"),
            raw=("not json", json.dumps({"command": "pytest -n auto -q"})))
        run = cost.newest_full_suite_run(record)
        assert run["cpu_seconds"] == 1100.0 and run["utc"] == "2026-10-02T10:00:00Z"

    def test_a_record_without_a_full_suite_line_gives_none(self, tmp_path):
        assert cost.newest_full_suite_run(_record(tmp_path, _row(command="pytest -q"))) is None

    def test_the_printed_line_is_the_line_a_later_closure_reads_back(self):
        run = {"cpu_seconds": 1234.5, "wall_seconds": 448.7, "collected": 21102, "exit_status": 0,
               "utc": "2026-10-02T10:00:00Z"}
        line = cost.transcript_line(run)
        assert line == ("Test load: 1234.50 CPU seconds, 448.70 wall seconds, 21102 tests collected, "
                        "exit status 0, recorded 2026-10-02T10:00:00Z")
        match = cost.LINE.fullmatch(line)
        assert match["cpu"] == "1234.50" and match["utc"] == run["utc"]


class TestThePreviousClosure:
    def test_it_is_the_newest_other_transcript_recorded_before_this_run(self, tmp_path):
        authored = tmp_path / "authored"
        _transcript(authored, "f101", 800.0, "2026-09-01T10:00:00Z")
        _transcript(authored, "f102", 900.0, "2026-09-15T10:00:00Z")
        _transcript(authored, "f103", 950.0, "2026-10-09T10:00:00Z")
        _transcript(authored, "f104", 10.0, "2026-09-20T10:00:00Z")
        (authored / "f105-closure-suite.txt").write_text("no load line\n", encoding="utf-8")
        found = cost.previous_closure(authored, "F104", "2026-10-02T10:00:00Z")
        assert found == {"feature": "F102", "utc": "2026-09-15T10:00:00Z", "cpu_seconds": 900.0}

    def test_none_when_no_transcript_carries_the_line(self, tmp_path):
        authored = tmp_path / "authored"
        authored.mkdir()
        (authored / "f101-closure-suite.txt").write_text("Summary line: 1 passed\n", encoding="utf-8")
        assert cost.previous_closure(authored, "F102", "2026-10-02T10:00:00Z") is None


class TestTheTenPercentLimit:
    PREVIOUS = {"feature": "F102", "utc": "2026-09-15T10:00:00Z", "cpu_seconds": 1000.0}

    def test_more_than_ten_percent_above_owes_a_finding(self):
        sentence, code = cost.compare(1100.01, self.PREVIOUS)
        assert code == 1
        assert sentence == ("This closure's suite used 1100.01 CPU seconds, 10.0 percent more than "
                            "F102's 1000.00; that is above the 10 percent limit, so this closure "
                            "registers a finding owned by the rolling findings paydown.")

    def test_exactly_ten_percent_above_is_within_the_limit(self):
        sentence, code = cost.compare(1100.0, self.PREVIOUS)
        assert code == 0 and sentence.endswith("within the 10 percent limit.")

    def test_a_cheaper_closure_says_less(self):
        sentence, code = cost.compare(800.0, self.PREVIOUS)
        assert code == 0
        assert "20.0 percent less than F102's 1000.00" in sentence

    def test_nothing_earlier_is_not_a_finding(self):
        sentence, code = cost.compare(800.0, None)
        assert code == 0 and "nothing to compare" in sentence


class TestTheModulesThatCarryARise:
    """R-1139: the record's CPU time per test module says where a rise lies."""

    def test_rises_are_largest_first_and_a_new_module_rises_from_nothing(self):
        lines = cost.module_rises({"tests/a.py": 3.0, "tests/b.py": 1.0, "tests/c.py": 2.0},
                                  {"tests/a.py": 1.0, "tests/b.py": 2.0})
        assert lines == ["  +2.00 s  tests/a.py (1.00 -> 3.00)",
                         "  +2.00 s  tests/c.py (0.00 -> 2.00)"]

    def test_only_the_top_modules_are_named(self):
        now = {f"tests/m{n:02d}.py": float(n) for n in range(1, 21)}
        assert len(cost.module_rises(now, {})) == cost.TOP_MODULES

    def test_a_previous_run_without_modules_names_none(self, tmp_path):
        record = _record(tmp_path, _row(cpu=1000.0, utc="2026-09-15T10:00:00Z"))
        run = {"modules": {"tests/a.py": 1.0}}
        previous = {"feature": "F102", "utc": "2026-09-15T10:00:00Z", "cpu_seconds": 1000.0}
        assert cost.module_report(record, run, previous) == [
            "F102's closure run recorded no CPU time per test module, so no module is named."]
        assert cost.module_report(record, run, None) == []


class TestTheCommandLine:
    def _run(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args], cwd=REPO_ROOT,
                              capture_output=True, text=True, timeout=60)

    def test_an_expensive_closure_prints_its_line_and_exits_one(self, tmp_path):
        authored = tmp_path / "authored"
        _transcript(authored, "f102", 1000.0, "2026-09-15T10:00:00Z")
        record = _record(tmp_path, _row(cpu=1250.0))
        done = self._run("--feature", "F103", "--record", str(record), "--authored", str(authored))
        assert done.returncode == 1, done.stdout + done.stderr
        assert done.stdout.splitlines() == [
            "Test load: 1250.00 CPU seconds, 400.00 wall seconds, 21000 tests collected, exit status 0, "
            "recorded 2026-10-02T10:00:00Z",
            "This closure's suite used 1250.00 CPU seconds, 25.0 percent more than F102's 1000.00; that "
            "is above the 10 percent limit, so this closure registers a finding owned by the rolling "
            "findings paydown.",
            "This run recorded no CPU time per test module, so no module is named."]

    def test_the_modules_that_carry_a_rise_are_named_from_the_previous_closure_runs_line(self, tmp_path):
        """R-1139: the previous closure's own full-suite line, found by its time, is the baseline."""
        authored = tmp_path / "authored"
        _transcript(authored, "f102", 1000.0, "2026-09-15T10:00:00Z")
        record = _record(
            tmp_path,
            _row(cpu=1000.0, utc="2026-09-15T10:00:00Z",
                 module_cpu_seconds={"tests/a.py": 10.0, "tests/b.py": 5.0}),
            _row(cpu=1250.0, module_cpu_seconds={"tests/a.py": 12.5, "tests/b.py": 4.0,
                                                 "tests/c.py": 30.0}))
        done = self._run("--feature", "F103", "--record", str(record), "--authored", str(authored))
        assert done.returncode == 1, done.stdout + done.stderr
        assert done.stdout.splitlines()[2:] == [
            "The test modules whose CPU time rose most since F102's closure run:",
            "  +30.00 s  tests/c.py (0.00 -> 30.00)",
            "  +2.50 s  tests/a.py (10.00 -> 12.50)"]

    def test_a_missing_record_exits_two(self, tmp_path):
        done = self._run("--feature", "F103", "--record", str(tmp_path / "absent.jsonl"),
                         "--authored", str(tmp_path))
        assert done.returncode == 2
        assert "cannot be read" in done.stdout
