"""The R-0803 data-root guard reads two levels, and what it sees there (R-1004), and what it
excuses while a supervisor the run did not start serves the root (R-1411)."""
from __future__ import annotations

import os

from tests.conftest import (
    DATA_ROOT_GUARD_DEPTH,
    SUPERVISOR_OWN_CLASSES,
    _data_root_fingerprint,
    _data_root_guard_verdict,
    _foreign_supervisor_answers,
)

PAST_NS = 1_000_000_000_000_000_000


def _record_root(tmp_path):
    root = tmp_path / "data"
    record = root / "jobs" / "job-1"
    record.mkdir(parents=True)
    (record / "job.json").write_text("{}", encoding="utf-8")
    (record / "deep").mkdir()
    (record / "deep" / "leaf.json").write_text("{}", encoding="utf-8")
    for path in (record / "deep", record, root / "jobs"):
        os.utime(path, ns=(PAST_NS, PAST_NS))
    return root, record


def test_it_reads_two_levels_and_no_deeper(tmp_path):
    root, _ = _record_root(tmp_path)
    paths = [entry[0] for entry in _data_root_fingerprint(str(root))]
    assert DATA_ROOT_GUARD_DEPTH == 2
    assert paths == ["jobs", os.path.join("jobs", "job-1")]


def test_a_new_record_changes_the_reading(tmp_path):
    root, _ = _record_root(tmp_path)
    before = _data_root_fingerprint(str(root))
    (root / "jobs" / "job-2").mkdir()
    assert _data_root_fingerprint(str(root)) != before


def test_an_atomic_replace_inside_a_record_changes_the_reading(tmp_path):
    root, record = _record_root(tmp_path)
    before = _data_root_fingerprint(str(root))
    (record / "job.json.tmp").write_text('{"state": "done"}', encoding="utf-8")
    os.replace(record / "job.json.tmp", record / "job.json")
    assert _data_root_fingerprint(str(root)) != before


def test_a_rewrite_in_place_below_the_depth_is_not_seen(tmp_path):
    """The limit the docstring states, pinned so it cannot quietly change."""
    root, record = _record_root(tmp_path)
    before = _data_root_fingerprint(str(root))
    with open(record / "deep" / "leaf.json", "w", encoding="utf-8") as handle:
        handle.write('{"changed": true}')
    assert _data_root_fingerprint(str(root)) == before


def test_an_absent_root_reads_none(tmp_path):
    assert _data_root_fingerprint(str(tmp_path / "absent")) is None


def _readings(tmp_path, *new_dirs: str):
    """Two readings of a root, before and after NEW_DIRS were made in it."""
    root, _ = _record_root(tmp_path)
    before = _data_root_fingerprint(str(root))
    for name in new_dirs:
        (root / name).mkdir(parents=True)
    return before, _data_root_fingerprint(str(root))


def test_a_supervisors_own_folders_are_excused_only_while_a_foreign_one_serves(tmp_path):
    """R-1411: the installed service writes its call ledger while the run lasts."""
    assert SUPERVISOR_OWN_CLASSES == ("api", "serve", "logs", "projects")
    before, after = _readings(tmp_path, "api", os.path.join("serve", "runs"), "logs")
    assert _data_root_guard_verdict(before, after, True) == (
        [], ["api", "logs", "serve", os.path.join("serve", "runs")])
    assert _data_root_guard_verdict(before, after, False) == (
        ["api", "logs", "serve", os.path.join("serve", "runs")], [])


def test_a_record_the_run_wrote_still_fails_beside_a_foreign_supervisor(tmp_path):
    before, after = _readings(tmp_path, "api", os.path.join("jobs", "job-2"))
    counted, excused = _data_root_guard_verdict(before, after, True)
    assert counted == ["jobs", os.path.join("jobs", "job-2")]
    assert excused == ["api"]


def test_a_path_root_reads_two_levels_too(tmp_path):
    """R-1419: the guard's own root is a Path, and it read one level only."""
    root, _ = _record_root(tmp_path)
    assert [entry[0] for entry in _data_root_fingerprint(root)] == ["jobs", os.path.join("jobs", "job-1")]


def test_a_root_no_supervisor_serves_has_no_foreign_supervisor(tmp_path):
    root, _ = _record_root(tmp_path)
    assert _foreign_supervisor_answers(str(root)) is False
