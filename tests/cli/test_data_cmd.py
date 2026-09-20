"""`remedy data usage` through the grouped CLI (F276 T001)."""
from __future__ import annotations

import json

from apps.cli.commands.data_cmd import format_data_bytes
from apps.cli.grouped import build_parser, main


def _seed(root) -> None:
    (root / "job_workspaces" / "staging_a").mkdir(parents=True)
    (root / "job_workspaces" / "staging_a" / "f.bin").write_bytes(b"x" * 2048)
    (root / "missions").mkdir()
    (root / "missions" / "m.json").write_bytes(b"{}")


def test_usage_json_reports_per_class_bytes_and_totals(tmp_path, monkeypatch, capsys):
    root = tmp_path / "data"
    _seed(root)
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    main(["data", "usage", "--json"])
    body = json.loads(capsys.readouterr().out)
    assert body["version"] == 1
    assert body["root"] == str(root)
    assert body["classes"]["ephemeral"] == {"bytes": 2048, "files": 1}
    assert body["classes"]["durable"] == {"bytes": 2, "files": 1}
    assert body["classes"]["unclassified"] == {"bytes": 0, "files": 0}
    assert body["total"] == {"bytes": 2050, "files": 2}


def test_usage_without_json_prints_one_line_per_class(tmp_path, monkeypatch, capsys):
    root = tmp_path / "data"
    _seed(root)
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    main(["data", "usage"])
    out = capsys.readouterr().out
    assert not out.lstrip().startswith("{")
    lines = [line.split() for line in out.splitlines()]
    assert ["ephemeral", "2.0", "KB", "1", "files"] in lines
    assert ["durable", "2", "B", "1", "files"] in lines
    assert ["unclassified", "0", "B", "0", "files"] in lines
    assert ["total", "2.0", "KB", "2", "files"] in lines


def test_usage_on_a_missing_root_says_so(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "absent"))
    main(["data", "usage", "--json"])
    assert json.loads(capsys.readouterr().out)["exists"] is False


def test_json_is_a_flag_that_parses_false_when_not_typed():
    args, _ = build_parser().parse_known_args(["data", "usage"])
    assert args.json is False
    args, _ = build_parser().parse_known_args(["data", "usage", "--json"])
    assert args.json is True


def test_apply_is_a_flag_that_parses_false_when_not_typed():
    """`--apply` is declared ``is_flag``; only ``--json`` is special-cased by name."""
    args, _ = build_parser().parse_known_args(["data", "reclaim"])
    assert args.apply is False
    args, _ = build_parser().parse_known_args(["data", "reclaim", "--apply"])
    assert args.apply is True


def test_orphans_is_a_flag_that_parses_false_when_not_typed_and_composes():
    """`--orphans` is declared ``is_flag``; `grouped.py` special-cases only `--json`.

    The COMPOSITION is pinned as hard as the parse: the orphan rule widens the plan
    and replaces nothing, so the flag has to survive beside `--apply` and `--json`.
    Not typing it must leave it False — a widening nobody typed is the one outcome
    this flag may never have.
    """
    args, _ = build_parser().parse_known_args(["data", "reclaim"])
    assert args.orphans is False
    args, _ = build_parser().parse_known_args(["data", "reclaim", "--orphans"])
    assert (args.orphans, args.apply, args.json) == (True, False, False)
    args, _ = build_parser().parse_known_args(
        ["data", "reclaim", "--orphans", "--apply", "--json"])
    assert (args.orphans, args.apply, args.json) == (True, True, True)
    args, _ = build_parser().parse_known_args(
        ["data", "reclaim", "--json", "--apply"])
    assert (args.orphans, args.apply, args.json) == (False, True, True)


def test_format_data_bytes():
    assert format_data_bytes(0) == "0 B"
    assert format_data_bytes(1023) == "1023 B"
    assert format_data_bytes(1024) == "1.0 KB"
    assert format_data_bytes(652 * 1024**3) == "652.0 GB"
