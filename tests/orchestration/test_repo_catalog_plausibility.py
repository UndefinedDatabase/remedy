"""Tests for packages.orchestration.repo_catalog_plausibility — the lockfile plausibility
check (F206 T003, DECISION F206 D3)."""

from __future__ import annotations

import json

from packages.orchestration.project_registry import RemyProject, save_project
from packages.orchestration.repo_catalog import parse_repo_catalog
from packages.orchestration.repo_catalog_plausibility import (
    RepoCatalogSkip,
    RepoCatalogWarning,
    check_repo_catalog_plausibility,
    normalize_package_name,
    read_lockfile_packages,
)


def _mkdirs(tmp_path, *names):
    roots = {}
    for name in names:
        root = tmp_path / name
        root.mkdir()
        roots[name] = root
    return roots


def _package_lock_v2(*names):
    packages = {"": {}}
    for name in names:
        packages[f"node_modules/{name}"] = {"version": "1.0.0"}
    return json.dumps({"name": "x", "lockfileVersion": 3, "packages": packages})


def _toml_packages(*names):
    return "".join(f'[[package]]\nname = "{n}"\nversion = "1.0.0"\n\n' for n in names)


# ---------------------------------------------------------------------------
# normalize_package_name
# ---------------------------------------------------------------------------

def test_normalize_folds_dashes_underscores_and_dots_and_lowercases():
    assert normalize_package_name("Foo_Bar") == "foo-bar"
    assert normalize_package_name("foo-bar") == "foo-bar"
    assert normalize_package_name("Foo.Bar__Baz") == "foo-bar-baz"


# ---------------------------------------------------------------------------
# read_lockfile_packages — one test per lockfile kind, plus the npm shapes
# ---------------------------------------------------------------------------

def test_read_lockfile_packages_reads_each_of_the_four_kinds(tmp_path):
    (tmp_path / "package-lock.json").write_text(_package_lock_v2("pkg-a"), encoding="utf-8")
    (tmp_path / "uv.lock").write_text(_toml_packages("pkg-b"), encoding="utf-8")
    (tmp_path / "poetry.lock").write_text(_toml_packages("pkg-c"), encoding="utf-8")
    (tmp_path / "Cargo.lock").write_text(_toml_packages("pkg-d"), encoding="utf-8")
    packages, errors = read_lockfile_packages(tmp_path)
    assert errors == {}
    assert packages["package-lock.json"] == frozenset({"pkg-a"})
    assert packages["uv.lock"] == frozenset({"pkg-b"})
    assert packages["poetry.lock"] == frozenset({"pkg-c"})
    assert packages["Cargo.lock"] == frozenset({"pkg-d"})


def test_read_lockfile_packages_walks_v1_nested_dependencies(tmp_path):
    data = {
        "name": "x",
        "lockfileVersion": 1,
        "dependencies": {
            "pkg": {"version": "1.0.0", "dependencies": {"nested-pkg": {"version": "2.0.0"}}},
        },
    }
    (tmp_path / "package-lock.json").write_text(json.dumps(data), encoding="utf-8")
    packages, errors = read_lockfile_packages(tmp_path)
    assert errors == {}
    assert packages["package-lock.json"] == frozenset({"pkg", "nested-pkg"})


def test_read_lockfile_packages_reads_a_scoped_npm_name(tmp_path):
    (tmp_path / "package-lock.json").write_text(_package_lock_v2("@scope/pkg"), encoding="utf-8")
    packages, _errors = read_lockfile_packages(tmp_path)
    assert packages["package-lock.json"] == frozenset({"@scope/pkg"})


def test_read_lockfile_packages_only_reads_the_root_not_subdirectories(tmp_path):
    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "package-lock.json").write_text(_package_lock_v2("pkg"), encoding="utf-8")
    packages, errors = read_lockfile_packages(tmp_path)
    assert packages == {}
    assert errors == {}


def test_read_lockfile_packages_reports_a_broken_lockfile(tmp_path):
    (tmp_path / "package-lock.json").write_text("not valid json {{{", encoding="utf-8")
    packages, errors = read_lockfile_packages(tmp_path)
    assert "package-lock.json" not in packages
    assert "package-lock.json" in errors


# ---------------------------------------------------------------------------
# check_repo_catalog_plausibility — the full rule, D3 (5)
# ---------------------------------------------------------------------------

def test_a_lockfile_of_each_kind_yields_a_warning_naming_its_file(tmp_path):
    for filename, make in (
        ("package-lock.json", lambda: _package_lock_v2("pkg")),
        ("uv.lock", lambda: _toml_packages("pkg")),
        ("poetry.lock", lambda: _toml_packages("pkg")),
        ("Cargo.lock", lambda: _toml_packages("pkg")),
    ):
        root = tmp_path / filename.replace(".", "-")
        root.mkdir()
        (root / filename).write_text(make(), encoding="utf-8")
        catalog = parse_repo_catalog(
            '[[repo]]\npid = "app"\n[[repo]]\npid = "lib"\npublishes = ["pkg"]\n', f"<{filename}>")
        result = check_repo_catalog_plausibility(catalog, {"app": root, "lib": tmp_path})
        assert result.skipped == ()
        matching = [w for w in result.warnings if w.proof == filename]
        assert len(matching) == 1
        warning = matching[0]
        assert warning.consumer == "app"
        assert warning.library == "lib"
        assert warning.package == "pkg"
        assert warning.sentence == (
            "app consumes pkg (" + filename + "), which lib publishes, "
            "but the catalog gives app no dependency on lib"
        )


def test_normalization_matches_foo_bar_against_foo_hyphen_bar(tmp_path):
    roots = _mkdirs(tmp_path, "app", "lib")
    (roots["app"] / "package-lock.json").write_text(_package_lock_v2("foo-bar"), encoding="utf-8")
    catalog = parse_repo_catalog(
        '[[repo]]\npid = "app"\n[[repo]]\npid = "lib"\npublishes = ["Foo_Bar"]\n', "<norm>")
    result = check_repo_catalog_plausibility(catalog, roots)
    assert len(result.warnings) == 1
    assert result.warnings[0].package == "Foo_Bar"


def test_a_declared_edge_yields_no_warning(tmp_path):
    roots = _mkdirs(tmp_path, "app", "lib")
    (roots["app"] / "package-lock.json").write_text(_package_lock_v2("pkg"), encoding="utf-8")
    catalog = parse_repo_catalog(
        '[[repo]]\npid = "app"\ndepends_on = ["lib"]\n'
        '[[repo]]\npid = "lib"\npublishes = ["pkg"]\n', "<declared>")
    result = check_repo_catalog_plausibility(catalog, roots)
    assert result.warnings == ()


def test_a_transitive_edge_yields_no_warning(tmp_path):
    roots = _mkdirs(tmp_path, "app", "mid", "lib")
    (roots["app"] / "package-lock.json").write_text(_package_lock_v2("pkg"), encoding="utf-8")
    catalog = parse_repo_catalog(
        '[[repo]]\npid = "app"\ndepends_on = ["mid"]\n'
        '[[repo]]\npid = "mid"\ndepends_on = ["lib"]\n'
        '[[repo]]\npid = "lib"\npublishes = ["pkg"]\n', "<transitive>")
    result = check_repo_catalog_plausibility(catalog, roots)
    assert result.warnings == ()


def test_the_publishers_own_lockfile_naming_itself_yields_no_warning(tmp_path):
    roots = _mkdirs(tmp_path, "lib")
    (roots["lib"] / "package-lock.json").write_text(_package_lock_v2("pkg"), encoding="utf-8")
    catalog = parse_repo_catalog('[[repo]]\npid = "lib"\npublishes = ["pkg"]\n', "<self>")
    result = check_repo_catalog_plausibility(catalog, roots)
    assert result.warnings == ()


def test_consumes_is_accepted_as_proof_with_no_lockfile_at_all(tmp_path):
    roots = _mkdirs(tmp_path, "app", "lib")
    catalog = parse_repo_catalog(
        '[[repo]]\npid = "app"\nconsumes = ["pkg"]\n'
        '[[repo]]\npid = "lib"\npublishes = ["pkg"]\n', "<consumes>")
    result = check_repo_catalog_plausibility(catalog, roots)
    assert len(result.warnings) == 1
    assert result.warnings[0].proof == "consumes"
    assert result.warnings[0].consumer == "app"
    assert result.warnings[0].library == "lib"


def test_a_lockfile_and_consumes_naming_the_same_package_yield_one_warning(tmp_path):
    roots = _mkdirs(tmp_path, "app", "lib")
    (roots["app"] / "package-lock.json").write_text(_package_lock_v2("pkg"), encoding="utf-8")
    catalog = parse_repo_catalog(
        '[[repo]]\npid = "app"\nconsumes = ["pkg"]\n'
        '[[repo]]\npid = "lib"\npublishes = ["pkg"]\n', "<dup-proof>")
    result = check_repo_catalog_plausibility(catalog, roots)
    assert len(result.warnings) == 1
    # the lockfile is read before `consumes` in the evidence order, so it is the proof that wins.
    assert result.warnings[0].proof == "package-lock.json"


def test_a_broken_lockfile_yields_a_warning_naming_the_file_and_reason(tmp_path):
    roots = _mkdirs(tmp_path, "app", "lib")
    (roots["app"] / "package-lock.json").write_text("not valid json {{{", encoding="utf-8")
    catalog = parse_repo_catalog(
        '[[repo]]\npid = "app"\n[[repo]]\npid = "lib"\n', "<broken>")
    result = check_repo_catalog_plausibility(catalog, roots)
    assert len(result.warnings) == 1
    warning = result.warnings[0]
    assert warning.consumer == "app"
    assert warning.library == ""
    assert warning.package == ""
    assert warning.proof == "package-lock.json"
    assert warning.sentence.startswith("app's package-lock.json cannot be read: ")


def test_no_root_and_a_missing_directory_are_both_skipped(tmp_path):
    catalog = parse_repo_catalog(
        '[[repo]]\npid = "no-root"\n[[repo]]\npid = "missing-dir"\n', "<skips>")
    result = check_repo_catalog_plausibility(
        catalog, {"missing-dir": tmp_path / "does-not-exist"})
    assert result.warnings == ()
    assert result.skipped == (
        RepoCatalogSkip(pid="no-root", reason="no-root has no root"),
        RepoCatalogSkip(
            pid="missing-dir",
            reason=f"missing-dir's root {tmp_path / 'does-not-exist'} is not a directory"),
    )


def test_an_entrys_own_root_field_is_used_over_project_roots(tmp_path):
    roots = _mkdirs(tmp_path, "app", "lib", "elsewhere")
    (roots["elsewhere"] / "package-lock.json").write_text(_package_lock_v2("pkg"), encoding="utf-8")
    catalog = parse_repo_catalog(
        f'[[repo]]\npid = "app"\nroot = "{roots["elsewhere"].as_posix()}"\n'
        '[[repo]]\npid = "lib"\npublishes = ["pkg"]\n', "<root-field>")
    # project_roots names a different (empty) directory for "app"; the entry's own `root` wins.
    result = check_repo_catalog_plausibility(catalog, roots)
    assert len(result.warnings) == 1
    assert result.warnings[0].proof == "package-lock.json"


def test_project_roots_none_falls_back_to_the_project_registry(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    repo_root = tmp_path / "app-repo"
    repo_root.mkdir()
    (repo_root / "package-lock.json").write_text(_package_lock_v2("pkg"), encoding="utf-8")
    save_project(RemyProject(name="App", slug="app", canonical_repo_path=str(repo_root)))
    catalog = parse_repo_catalog(
        '[[repo]]\npid = "app"\n[[repo]]\npid = "lib"\npublishes = ["pkg"]\n', "<registry>")
    result = check_repo_catalog_plausibility(catalog)
    assert result.skipped == (RepoCatalogSkip(pid="lib", reason="lib has no root"),)
    assert len(result.warnings) == 1
    assert result.warnings[0].consumer == "app"
    assert result.warnings[0].library == "lib"


def test_the_warnings_order_is_catalog_order_then_evidence_order(tmp_path):
    roots = _mkdirs(tmp_path, "app", "other", "lib-a", "lib-b")
    (roots["app"] / "uv.lock").write_text(_toml_packages("pkg-a"), encoding="utf-8")
    (roots["app"] / "poetry.lock").write_text(_toml_packages("pkg-b"), encoding="utf-8")
    (roots["other"] / "package-lock.json").write_text(_package_lock_v2("pkg-a"), encoding="utf-8")
    catalog = parse_repo_catalog(
        '[[repo]]\npid = "app"\n'
        '[[repo]]\npid = "other"\n'
        '[[repo]]\npid = "lib-a"\npublishes = ["pkg-a"]\n'
        '[[repo]]\npid = "lib-b"\npublishes = ["pkg-b"]\n', "<order>")
    result = check_repo_catalog_plausibility(catalog, roots)
    assert [(w.consumer, w.library, w.package) for w in result.warnings] == [
        ("app", "lib-a", "pkg-a"),
        ("app", "lib-b", "pkg-b"),
        ("other", "lib-a", "pkg-a"),
    ]


def test_check_returns_the_warning_and_skip_named_tuple_shapes():
    assert RepoCatalogWarning._fields == ("consumer", "library", "package", "proof", "sentence")
    assert RepoCatalogSkip._fields == ("pid", "reason")
