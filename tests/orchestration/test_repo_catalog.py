"""Tests for packages.orchestration.repo_catalog — the catalog's format, validation and
order (F206 T001)."""

from __future__ import annotations

from packages.orchestration.data_paths import classify_data_child
from packages.orchestration.repo_catalog import (
    RepoCatalogCycleError,
    RepoCatalogEntry,
    RepoCatalogError,
    describe_repo_catalog_edge,
    find_repo_catalog_cycle,
    load_repo_catalog,
    parse_repo_catalog,
    repo_catalog_order,
    repo_catalog_path,
)

DIAMOND = """
[[repo]]
pid = "app"
depends_on = ["lib-a", "lib-b"]

[[repo]]
pid = "lib-a"
depends_on = ["core"]

[[repo]]
pid = "lib-b"
depends_on = ["core"]

[[repo]]
pid = "core"
"""


# ---------------------------------------------------------------------------
# Order and edges
# ---------------------------------------------------------------------------

def test_diamond_orders_core_first_with_its_four_edges():
    catalog = parse_repo_catalog(DIAMOND, "<diamond>")
    order = repo_catalog_order(catalog, ["app", "lib-a", "lib-b", "core"])
    assert order.pids == ("core", "lib-a", "lib-b", "app")
    assert set(order.edges) == {
        ("app", "lib-a", ("app", "lib-a")),
        ("app", "lib-b", ("app", "lib-b")),
        ("lib-a", "core", ("lib-a", "core")),
        ("lib-b", "core", ("lib-b", "core")),
    }
    assert len(order.edges) == 4


def test_two_unrelated_pids_keep_the_given_order():
    catalog = parse_repo_catalog('[[repo]]\npid = "x"\n[[repo]]\npid = "y"\n', "<unrelated>")
    order = repo_catalog_order(catalog, ["y", "x"])
    assert order.pids == ("y", "x")
    assert order.edges == ()


def test_transitive_edge_through_a_pid_not_given_names_the_middle_pid():
    text = (
        '[[repo]]\npid = "app"\ndepends_on = ["brain"]\n'
        '[[repo]]\npid = "brain"\ndepends_on = ["toolbox"]\n'
        '[[repo]]\npid = "toolbox"\n'
    )
    catalog = parse_repo_catalog(text, "<transitive>")
    order = repo_catalog_order(catalog, ["app", "toolbox"])
    assert order.pids == ("toolbox", "app")
    assert len(order.edges) == 1
    edge = order.edges[0]
    assert edge.consumer == "app"
    assert edge.library == "toolbox"
    assert edge.path == ("app", "brain", "toolbox")
    assert describe_repo_catalog_edge(edge) == "app depends on toolbox through brain"


def test_two_pid_path_description_has_no_through_clause():
    catalog = parse_repo_catalog(DIAMOND, "<diamond>")
    order = repo_catalog_order(catalog, ["app", "lib-a"])
    assert len(order.edges) == 1
    assert describe_repo_catalog_edge(order.edges[0]) == "app depends on lib-a"


def test_a_given_pid_the_catalog_lacks_keeps_its_place():
    text = '[[repo]]\npid = "toolbox"\n[[repo]]\npid = "app"\ndepends_on = ["toolbox"]\n'
    catalog = parse_repo_catalog(text, "<ghost>")
    order = repo_catalog_order(catalog, ["toolbox", "ghost", "app"])
    assert order.pids == ("toolbox", "ghost", "app")
    assert all(edge.consumer != "ghost" and edge.library != "ghost" for edge in order.edges)


def test_a_pid_given_twice_raises_value_error():
    catalog = parse_repo_catalog(DIAMOND, "<diamond>")
    try:
        repo_catalog_order(catalog, ["app", "app"])
    except ValueError:
        return
    raise AssertionError("a pid given twice did not raise ValueError")


# ---------------------------------------------------------------------------
# Cycles
# ---------------------------------------------------------------------------

def test_two_pid_cycle_raises_with_exact_cycle_and_message():
    text = '[[repo]]\npid = "a"\ndepends_on = ["b"]\n[[repo]]\npid = "b"\ndepends_on = ["a"]\n'
    try:
        parse_repo_catalog(text, "<c2>")
    except RepoCatalogCycleError as exc:
        assert exc.cycle == ("a", "b", "a")
        assert str(exc) == "<c2>: the repository catalog has a dependency cycle: a -> b -> a"
        return
    raise AssertionError("a two-pid cycle did not raise RepoCatalogCycleError")


def test_three_pid_cycle_raises_with_exact_cycle_and_message():
    text = (
        '[[repo]]\npid = "a"\ndepends_on = ["b"]\n'
        '[[repo]]\npid = "b"\ndepends_on = ["c"]\n'
        '[[repo]]\npid = "c"\ndepends_on = ["a"]\n'
    )
    try:
        parse_repo_catalog(text, "<c3>")
    except RepoCatalogCycleError as exc:
        assert exc.cycle == ("a", "b", "c", "a")
        assert str(exc) == "<c3>: the repository catalog has a dependency cycle: a -> b -> c -> a"
        return
    raise AssertionError("a three-pid cycle did not raise RepoCatalogCycleError")


def test_self_dependency_raises_with_exact_cycle_and_message():
    try:
        parse_repo_catalog('[[repo]]\npid = "a"\ndepends_on = ["a"]\n', "<cself>")
    except RepoCatalogCycleError as exc:
        assert exc.cycle == ("a", "a")
        assert str(exc) == "<cself>: the repository catalog has a dependency cycle: a -> a"
        return
    raise AssertionError("a self-dependency did not raise RepoCatalogCycleError")


def test_find_repo_catalog_cycle_returns_none_when_acyclic():
    assert find_repo_catalog_cycle({"a": ["b"], "b": []}) is None


def test_find_repo_catalog_cycle_ignores_an_unknown_dependency():
    # the function itself is general-purpose; parse_repo_catalog rejects a dangling
    # dependency before this ever runs, so this exercises the guard directly.
    assert find_repo_catalog_cycle({"a": ["ghost"]}) is None


# ---------------------------------------------------------------------------
# Refusals
# ---------------------------------------------------------------------------

def test_invalid_toml_is_refused():
    try:
        parse_repo_catalog("not valid toml {{{", "<bad-toml>")
    except RepoCatalogError as exc:
        assert str(exc).startswith("<bad-toml>: ")
        return
    raise AssertionError("invalid TOML did not raise RepoCatalogError")


def test_unknown_top_level_key_is_refused():
    try:
        parse_repo_catalog('other = 1\n', "<unknown-top>")
    except RepoCatalogError as exc:
        assert str(exc).startswith("<unknown-top>: ")
        assert "'other'" in str(exc)
        return
    raise AssertionError("an unknown top-level key did not raise")


def test_repo_not_an_array_of_tables_is_refused():
    try:
        parse_repo_catalog('repo = "nope"\n', "<not-array>")
    except RepoCatalogError as exc:
        assert str(exc).startswith("<not-array>: ")
        assert "repo" in str(exc)
        return
    raise AssertionError("a non-array 'repo' did not raise")


def test_unknown_key_in_a_table_names_the_key_and_its_position():
    try:
        parse_repo_catalog('[[repo]]\npid = "a"\n[[repo]]\npid = "b"\nbogus = 1\n', "<unknown-key>")
    except RepoCatalogError as exc:
        assert str(exc).startswith("<unknown-key>: ")
        assert "'bogus'" in str(exc)
        assert "repo[2]" in str(exc)
        return
    raise AssertionError("an unknown table key did not raise")


def test_missing_pid_is_refused():
    try:
        parse_repo_catalog('[[repo]]\nname = "x"\n', "<missing-pid>")
    except RepoCatalogError as exc:
        assert str(exc).startswith("<missing-pid>: ")
        assert "pid" in str(exc)
        return
    raise AssertionError("a missing pid did not raise")


def test_empty_string_pid_is_refused():
    try:
        parse_repo_catalog('[[repo]]\npid = ""\n', "<empty-pid>")
    except RepoCatalogError as exc:
        assert str(exc).startswith("<empty-pid>: ")
        return
    raise AssertionError("an empty pid did not raise")


def test_non_string_pid_is_refused():
    try:
        parse_repo_catalog('[[repo]]\npid = 5\n', "<numeric-pid>")
    except RepoCatalogError as exc:
        assert str(exc).startswith("<numeric-pid>: ")
        return
    raise AssertionError("a non-string pid did not raise")


def test_name_root_owner_must_be_strings():
    for key in ("name", "root", "owner"):
        try:
            parse_repo_catalog(f'[[repo]]\npid = "a"\n{key} = 5\n', f"<{key}-type>")
        except RepoCatalogError as exc:
            assert str(exc).startswith(f"<{key}-type>: ")
            assert key in str(exc)
            continue
        raise AssertionError(f"a non-string {key} did not raise")


def test_depends_on_publishes_consumes_must_be_lists_of_non_empty_strings():
    for key in ("depends_on", "publishes", "consumes"):
        try:
            parse_repo_catalog(f'[[repo]]\npid = "a"\n{key} = "nope"\n', f"<{key}-list>")
        except RepoCatalogError as exc:
            assert str(exc).startswith(f"<{key}-list>: ")
            assert key in str(exc)
        else:
            raise AssertionError(f"a non-list {key} did not raise")

        try:
            parse_repo_catalog(f'[[repo]]\npid = "a"\n{key} = [""]\n', f"<{key}-empty>")
        except RepoCatalogError as exc:
            assert str(exc).startswith(f"<{key}-empty>: ")
        else:
            raise AssertionError(f"an empty-string entry in {key} did not raise")


def test_a_name_list_value_named_twice_is_refused():
    for key in ("depends_on", "publishes", "consumes"):
        try:
            parse_repo_catalog(f'[[repo]]\npid = "a"\n{key} = ["x", "x"]\n', f"<{key}-dup>")
        except RepoCatalogError as exc:
            assert str(exc).startswith(f"<{key}-dup>: ")
            assert "'x'" in str(exc)
        else:
            raise AssertionError(f"a doubled value in {key} did not raise")


def test_a_pid_a_second_table_repeats_is_refused():
    try:
        parse_repo_catalog('[[repo]]\npid = "a"\n[[repo]]\npid = "a"\n', "<dup-pid>")
    except RepoCatalogError as exc:
        assert str(exc).startswith("<dup-pid>: ")
        assert "'a'" in str(exc)
        assert "repo[1]" in str(exc) and "repo[2]" in str(exc)
        return
    raise AssertionError("a repeated pid did not raise")


def test_a_depends_on_value_no_table_holds_names_both_pids():
    try:
        parse_repo_catalog('[[repo]]\npid = "a"\ndepends_on = ["ghost"]\n', "<dangling>")
    except RepoCatalogError as exc:
        assert str(exc).startswith("<dangling>: ")
        assert "'a'" in str(exc)
        assert "'ghost'" in str(exc)
        return
    raise AssertionError("a dangling depends_on value did not raise")


def test_an_absent_or_empty_repo_is_a_valid_empty_catalog():
    assert parse_repo_catalog("", "<empty>").entries == ()
    assert parse_repo_catalog("repo = []\n", "<empty-array>").entries == ()


# ---------------------------------------------------------------------------
# Round trip, pids, entry()
# ---------------------------------------------------------------------------

def test_a_full_valid_table_round_trips_every_field():
    text = (
        '[[repo]]\n'
        'pid = "app"\n'
        'name = "App"\n'
        'root = "/repos/app"\n'
        'owner = "team-a"\n'
        'depends_on = ["lib"]\n'
        'publishes = ["app-pkg"]\n'
        'consumes = ["lib-pkg"]\n'
        '\n'
        '[[repo]]\n'
        'pid = "lib"\n'
    )
    catalog = parse_repo_catalog(text, "<full>")
    assert catalog.source == "<full>"
    assert catalog.pids == ("app", "lib")
    assert catalog.entry("app") == RepoCatalogEntry(
        pid="app", name="App", root="/repos/app", owner="team-a",
        depends_on=("lib",), publishes=("app-pkg",), consumes=("lib-pkg",))
    assert catalog.entry("lib") == RepoCatalogEntry(pid="lib")
    assert catalog.entry("missing") is None


# ---------------------------------------------------------------------------
# load_repo_catalog, repo_catalog_path, the data-root class
# ---------------------------------------------------------------------------

def test_load_repo_catalog_reads_none_for_a_missing_file(tmp_path):
    assert load_repo_catalog(tmp_path / "org" / "catalog.toml") is None


def test_load_repo_catalog_reads_a_catalog_for_a_written_file(tmp_path):
    path = tmp_path / "org" / "catalog.toml"
    path.parent.mkdir(parents=True)
    path.write_text('[[repo]]\npid = "app"\n', encoding="utf-8")
    catalog = load_repo_catalog(path)
    assert catalog is not None
    assert catalog.pids == ("app",)
    assert catalog.source == str(path)


def test_repo_catalog_path_under_the_data_root_ends_org_catalog_toml(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    path = repo_catalog_path()
    assert path.as_posix().endswith("org/catalog.toml")
    assert classify_data_child("org") == "durable"
