"""`remedy project catalog-check` / `remedy project catalog-show` through the grouped CLI
(F206 T004, DECISION F206 D4)."""

from __future__ import annotations

import json

import pytest

from apps.cli.grouped import main


def _run_json(monkeypatch, capsys, argv):
    out = main_and_capture(monkeypatch, capsys, argv)
    return json.loads(out)


def main_and_capture(monkeypatch, capsys, argv):
    main(argv)
    return capsys.readouterr().out


# ---------------------------------------------------------------------------
# No catalog at all
# ---------------------------------------------------------------------------

def test_catalog_check_with_no_catalog_is_json_present_false(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    body = _run_json(monkeypatch, capsys, ["project", "catalog-check", "--json"])
    assert body["ok"] is True
    assert body["present"] is False
    assert body["catalog"].endswith("org/catalog.toml")


def test_catalog_show_with_no_catalog_is_json_present_false(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    body = _run_json(monkeypatch, capsys, ["project", "catalog-show", "--json"])
    assert body["present"] is False


def test_catalog_check_with_no_catalog_text_names_the_path(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    out = main_and_capture(monkeypatch, capsys, ["project", "catalog-check"])
    assert out.strip().startswith("No repository catalog at ")
    assert out.strip().endswith("org/catalog.toml.")


def test_catalog_show_with_no_catalog_text_names_the_path(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    out = main_and_capture(monkeypatch, capsys, ["project", "catalog-show"])
    assert out.strip().startswith("No repository catalog at ")


# ---------------------------------------------------------------------------
# A valid catalog, shown with its order and edge sentences; --catalog reads
# another file than the data root's own.
# ---------------------------------------------------------------------------

def _write_diamond(path):
    path.write_text(
        '[[repo]]\npid = "lib"\npublishes = ["pkg"]\n'
        '[[repo]]\npid = "app"\ndepends_on = ["lib"]\n', encoding="utf-8")


def test_catalog_show_json_names_repos_order_and_edges(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    catalog = tmp_path / "custom-catalog.toml"
    _write_diamond(catalog)
    body = _run_json(
        monkeypatch, capsys, ["project", "catalog-show", "--catalog", str(catalog), "--json"])
    assert body["present"] is True
    assert body["catalog"] == str(catalog)
    assert body["repos"] == [
        {"pid": "lib", "name": "", "root": "", "owner": "", "depends_on": [],
         "publishes": ["pkg"], "consumes": []},
        {"pid": "app", "name": "", "root": "", "owner": "", "depends_on": ["lib"],
         "publishes": [], "consumes": []},
    ]
    assert body["order"] == ["lib", "app"]
    assert body["edges"] == [
        {"consumer": "app", "library": "lib", "path": ["app", "lib"],
         "sentence": "app depends on lib"},
    ]


def test_catalog_show_text_names_catalog_order_and_edge_sentence(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    catalog = tmp_path / "custom-catalog.toml"
    _write_diamond(catalog)
    out = main_and_capture(
        monkeypatch, capsys, ["project", "catalog-show", "--catalog", str(catalog)])
    lines = out.splitlines()
    assert lines[0] == f"Catalog: {catalog}"
    assert "lib:" in lines
    assert "  publishes: pkg" in lines
    assert "app:" in lines
    assert "  depends_on: lib" in lines
    assert "Order: lib -> app" in lines
    assert "  app depends on lib" in lines


# ---------------------------------------------------------------------------
# catalog-check: one lockfile warning and one skipped entry
# ---------------------------------------------------------------------------

def _write_warning_catalog(tmp_path):
    app_root = tmp_path / "app-root"
    app_root.mkdir()
    (app_root / "package-lock.json").write_text(
        json.dumps({
            "name": "app", "lockfileVersion": 3,
            "packages": {"": {}, "node_modules/other-pkg": {"version": "1.0.0"}},
        }), encoding="utf-8")
    other_root = tmp_path / "other-root"
    other_root.mkdir()
    catalog = tmp_path / "warn-catalog.toml"
    catalog.write_text(
        f'[[repo]]\npid = "app"\nroot = "{app_root.as_posix()}"\n'
        f'[[repo]]\npid = "other"\nroot = "{other_root.as_posix()}"\npublishes = ["other-pkg"]\n'
        '[[repo]]\npid = "ghost"\n',
        encoding="utf-8",
    )
    return catalog


def test_catalog_check_json_names_one_warning_and_one_skip(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    catalog = _write_warning_catalog(tmp_path)
    body = _run_json(
        monkeypatch, capsys, ["project", "catalog-check", "--catalog", str(catalog), "--json"])
    assert body["present"] is True
    assert body["valid"] is True
    assert body["repositories"] == 3
    assert body["warnings"] == [{
        "consumer": "app", "library": "other", "package": "other-pkg",
        "proof": "package-lock.json",
        "sentence": "app consumes other-pkg (package-lock.json), which other publishes, "
                    "but the catalog gives app no dependency on other",
    }]
    assert body["skipped"] == [{"pid": "ghost", "reason": "ghost has no root"}]


def test_catalog_check_text_names_the_warning_and_the_skip(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    catalog = _write_warning_catalog(tmp_path)
    out = main_and_capture(
        monkeypatch, capsys, ["project", "catalog-check", "--catalog", str(catalog)])
    lines = out.splitlines()
    assert lines[0] == f"Catalog: {catalog}"
    assert "Valid: 3 repositories." in lines
    assert ("Warning: app consumes other-pkg (package-lock.json), which other publishes, "
            "but the catalog gives app no dependency on other") in lines
    assert "Skipped: ghost: ghost has no root" in lines


# ---------------------------------------------------------------------------
# A cycle and an unknown key each exit 1 with repo_catalog_invalid
# ---------------------------------------------------------------------------

def test_catalog_check_on_a_cycle_exits_1_with_its_path(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    catalog = tmp_path / "cycle-catalog.toml"
    catalog.write_text(
        '[[repo]]\npid = "a"\ndepends_on = ["b"]\n[[repo]]\npid = "b"\ndepends_on = ["a"]\n',
        encoding="utf-8")
    with pytest.raises(SystemExit) as exc:
        main(["project", "catalog-check", "--catalog", str(catalog), "--json"])
    assert exc.value.code == 1
    body = json.loads(capsys.readouterr().out)
    assert body["error"] == "repo_catalog_invalid"
    assert body["cycle"] == ["a", "b", "a"]
    assert body["catalog"] == str(catalog)


def test_catalog_show_on_a_cycle_exits_1(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    catalog = tmp_path / "cycle-catalog.toml"
    catalog.write_text(
        '[[repo]]\npid = "a"\ndepends_on = ["b"]\n[[repo]]\npid = "b"\ndepends_on = ["a"]\n',
        encoding="utf-8")
    with pytest.raises(SystemExit) as exc:
        main(["project", "catalog-show", "--catalog", str(catalog), "--json"])
    assert exc.value.code == 1
    body = json.loads(capsys.readouterr().out)
    assert body["error"] == "repo_catalog_invalid"
    assert body["cycle"] == ["a", "b", "a"]


def test_catalog_check_on_an_unknown_key_exits_1_with_no_cycle(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    catalog = tmp_path / "bad-catalog.toml"
    catalog.write_text('[[repo]]\npid = "a"\nbogus = 1\n', encoding="utf-8")
    with pytest.raises(SystemExit) as exc:
        main(["project", "catalog-check", "--catalog", str(catalog), "--json"])
    assert exc.value.code == 1
    body = json.loads(capsys.readouterr().out)
    assert body["error"] == "repo_catalog_invalid"
    assert body["cycle"] is None


def test_catalog_show_on_an_unknown_key_exits_1_with_no_cycle(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    catalog = tmp_path / "bad-catalog.toml"
    catalog.write_text('[[repo]]\npid = "a"\nbogus = 1\n', encoding="utf-8")
    with pytest.raises(SystemExit) as exc:
        main(["project", "catalog-show", "--catalog", str(catalog), "--json"])
    assert exc.value.code == 1
    body = json.loads(capsys.readouterr().out)
    assert body["error"] == "repo_catalog_invalid"
    assert body["cycle"] is None
