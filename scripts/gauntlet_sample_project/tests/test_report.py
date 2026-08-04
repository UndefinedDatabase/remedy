"""The report over an imported directory."""
from sampleproj.importer import import_records
from sampleproj.report import build_report, report_dir


def test_an_empty_directory_reports_zero(tmp_path):
    assert build_report(tmp_path).startswith("records: 0")


def test_every_imported_record_is_listed(tmp_path):
    import_records(["a=1", "b=2"], tmp_path / "out")
    text = build_report(tmp_path / "out")
    assert "records: 2" in text
    assert "  - a.txt" in text and "  - b.txt" in text


def test_a_missing_directory_reports_zero(tmp_path):
    assert build_report(tmp_path / "absent").startswith("records: 0")


def test_a_relative_directory_is_normalised(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert report_dir("out").is_absolute()
