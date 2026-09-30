"""Tests for packages.orchestration.dead_command_check.dead_command_ids.

Pure in-process: every test builds its own tmp_path search root with a
synthetic tests/ and scripts/ directory, except the one integration test that
proves the real catalog and the real repo's tests/ + scripts/ read empty.
"""
from __future__ import annotations

from packages.orchestration.dead_command_check import dead_command_ids


def _fn(name):
    ns: dict = {}
    exec(f"def {name}(args):\n    pass\n", ns)
    return ns[name]


class TestDeadCommandIds:
    def test_a_command_referenced_nowhere_is_dead(self, tmp_path):
        (tmp_path / "tests").mkdir()
        (tmp_path / "scripts").mkdir()
        (tmp_path / "tests" / "test_x.py").write_text("live_handler()\n", encoding="utf-8")
        catalog = [("do.run", "do", "run"), ("ghost.vanish", "ghost", "vanish")]
        handlers = {"do.run": _fn("live_handler"), "ghost.vanish": _fn("dead_handler")}
        assert dead_command_ids(catalog, handlers, root=tmp_path) == ["ghost.vanish"]

    def test_an_argv_list_pair_counts_as_a_reference(self, tmp_path):
        (tmp_path / "tests").mkdir()
        (tmp_path / "scripts").mkdir()
        (tmp_path / "tests" / "test_x.py").write_text(
            'subprocess.run([*_CLI, "job", "run-next", short_id])\n', encoding="utf-8",
        )
        catalog = [("job.run-next", "job", "run-next")]
        handlers = {"job.run-next": _fn("unrelated_name")}
        assert dead_command_ids(catalog, handlers, root=tmp_path) == []

    def test_the_real_catalog_has_no_dead_commands(self):
        from apps.cli.command_catalog import CATALOG
        from apps.cli.commands import collect_all_handlers

        triples = [(e.command_id, e.group_id, e.subcommand) for e in CATALOG]
        assert dead_command_ids(triples, collect_all_handlers()) == []

    def test_the_file_scan_is_not_repeated_for_the_same_root(self, tmp_path, monkeypatch):
        (tmp_path / "tests").mkdir()
        (tmp_path / "scripts").mkdir()
        (tmp_path / "tests" / "test_x.py").write_text("live_handler()\n", encoding="utf-8")
        catalog = [("do.run", "do", "run")]
        handlers = {"do.run": _fn("live_handler")}

        import packages.orchestration.dead_command_check as mod
        calls = {"n": 0}
        real_iter = mod._iter_search_files

        def counting_iter(root):
            calls["n"] += 1
            yield from real_iter(root)

        monkeypatch.setattr(mod, "_iter_search_files", counting_iter)
        dead_command_ids(catalog, handlers, root=tmp_path)
        dead_command_ids(catalog, handlers, root=tmp_path)
        assert calls["n"] == 1

    def test_two_different_roots_never_share_a_cache_entry(self, tmp_path):
        root_a = tmp_path / "a"
        root_b = tmp_path / "b"
        for root in (root_a, root_b):
            (root / "tests").mkdir(parents=True)
            (root / "scripts").mkdir()
        # root_a: "ghost.vanish" is referenced nowhere -> dead.
        (root_a / "tests" / "test_x.py").write_text("nothing_relevant()\n", encoding="utf-8")
        # root_b: the SAME command_id IS referenced -> not dead.
        (root_b / "tests" / "test_x.py").write_text("dead_handler()\n", encoding="utf-8")
        catalog = [("ghost.vanish", "ghost", "vanish")]
        handlers = {"ghost.vanish": _fn("dead_handler")}
        assert dead_command_ids(catalog, handlers, root=root_a) == ["ghost.vanish"]
        assert dead_command_ids(catalog, handlers, root=root_b) == []

    def test_a_repeated_question_reads_no_search_text_again(self, tmp_path):
        # DECISION F293 D4: the answer for one command depends on the root's files and the words
        # searched for, so asking again about the same root reads none of its texts.
        import packages.orchestration.dead_command_check as mod

        (tmp_path / "tests").mkdir()
        (tmp_path / "scripts").mkdir()
        (tmp_path / "tests" / "test_x.py").write_text("live_handler()\n", encoding="utf-8")
        catalog = [("do.run", "do", "run"), ("ghost.vanish", "ghost", "vanish")]
        handlers = {"do.run": _fn("live_handler"), "ghost.vanish": _fn("dead_handler")}
        assert dead_command_ids(catalog, handlers, root=tmp_path) == ["ghost.vanish"]

        class _Unreadable(list):
            def __iter__(self):
                raise AssertionError("the search texts were read again")

        texts, pairs = mod._SCAN_CACHE[tmp_path]
        mod._SCAN_CACHE[tmp_path] = (_Unreadable(texts), pairs)
        assert dead_command_ids(catalog, handlers, root=tmp_path) == ["ghost.vanish"]
