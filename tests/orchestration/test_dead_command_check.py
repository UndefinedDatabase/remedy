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
