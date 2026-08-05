"""Importing records, and planning an import without doing it."""
from sampleproj.importer import import_records, plan_import


def test_each_record_becomes_a_file(tmp_path):
    written = import_records(["a=1", "b=2"], tmp_path / "out")
    assert [p.name for p in written] == ["a.txt", "b.txt"]
    assert (tmp_path / "out" / "a.txt").read_text(encoding="utf-8") == "1\n"


def test_malformed_records_are_not_written(tmp_path):
    written = import_records(["a=1", "junk"], tmp_path / "out")
    assert [p.name for p in written] == ["a.txt"]


def test_the_target_directory_is_created(tmp_path):
    import_records(["a=1"], tmp_path / "deep" / "nested")
    assert (tmp_path / "deep" / "nested" / "a.txt").is_file()


def test_planning_writes_nothing(tmp_path):
    target = tmp_path / "out"
    planned = plan_import(["a=1", "b=2"], target)
    assert len(planned) == 2
    assert not target.exists()
