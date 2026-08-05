"""The command line: progress on stdout, errors on stderr."""
from sampleproj.cli import main


def test_import_prints_progress_to_stdout(tmp_path, capsys):
    source = tmp_path / "in.txt"
    source.write_text("a=1\nb=2\n", encoding="utf-8")
    assert main(["import", str(source), str(tmp_path / "out")]) == 0
    out = capsys.readouterr().out
    assert "importing from" in out
    assert "imported 2 record(s)" in out


def test_a_missing_input_file_is_an_error_on_stderr(tmp_path, capsys):
    assert main(["import", str(tmp_path / "absent.txt"), str(tmp_path)]) == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "error: no such input file" in captured.err


def test_report_writes_the_listing_to_stdout(tmp_path, capsys):
    source = tmp_path / "in.txt"
    source.write_text("a=1\n", encoding="utf-8")
    main(["import", str(source), str(tmp_path / "out")])
    capsys.readouterr()
    assert main(["report", str(tmp_path / "out")]) == 0
    assert "records: 1" in capsys.readouterr().out
