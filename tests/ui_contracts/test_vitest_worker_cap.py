"""``apps/ui/vitest.config.ts`` keeps the worker cap of operator amendment amend0930-test-load.

Without a limit every vitest run starts one worker per CPU thread. The cap reads the same variable
as ``tests/load_governor.py`` (``REMEDY_TEST_MAX_WORKERS``, unset means 6, 0 means no limit) and is
pinned as source, comment-stripped, so prose above the code cannot satisfy it.
"""
from __future__ import annotations

from pathlib import Path

from tests.ui_contracts.test_brain_stream_ring import strip_ts_comments

CONFIG = Path(__file__).resolve().parent.parent.parent / "apps" / "ui" / "vitest.config.ts"


def _code() -> str:
    return strip_ts_comments(CONFIG.read_text(encoding="utf-8"))


def test_the_config_reads_the_shared_worker_cap_variable():
    assert "process.env.REMEDY_TEST_MAX_WORKERS" in _code()


def test_the_config_limits_workers_with_a_floor_of_one():
    code = _code()
    assert "maxWorkers: workerCap" in code
    assert "minWorkers: 1" in code


def test_the_default_is_six_and_zero_lifts_the_limit():
    code = _code()
    assert "? 6 : asked" in code
    assert "workerCap > 0" in code


def test_the_config_keeps_its_node_environment():
    assert 'environment: "node"' in _code()
    # The include glob holds "/*", which the comment stripper reads as a comment, so it is read raw.
    assert 'include: ["src/**/*.test.ts"]' in CONFIG.read_text(encoding="utf-8")
