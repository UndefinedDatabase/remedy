"""The server-start wait reddens only for a start that really failed.

Findings R-0734 and R-0708. Each test drives `wait_for_server_info` with a fake
clock and a fake sleep, so the race each finding measured is reproduced on every
run rather than once in twenty, and no test here waits on wall clock.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from tests.ui_server.server_start import (
    SERVER_START_BACKSTOP_S,
    read_server_info,
    wait_for_server_info,
)

INFO = {"version": 1, "host": "127.0.0.1", "port": 43121, "token": "t"}
FULL = json.dumps(INFO, indent=2)


class _Thread:
    def __init__(self, alive: bool) -> None:
        self.alive = alive

    def is_alive(self) -> bool:
        return self.alive


class _Clock:
    """A clock that only moves when the wait sleeps, and a hook that runs then."""

    def __init__(self, on_sleep=None) -> None:
        self.now = 0.0
        self.on_sleep = on_sleep

    def __call__(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.now += seconds
        if self.on_sleep is not None:
            self.on_sleep(self.now)


def _wait(info_file: Path, thread: _Thread, clock: _Clock) -> dict:
    return wait_for_server_info(info_file, thread, clock=clock, sleep=clock.sleep)


class TestAHalfWrittenFileIsNotStartedYet:
    """R-0734: the server creates the file before it writes it."""

    @pytest.mark.parametrize(
        "partial", ["", FULL[:1], FULL[: len(FULL) // 2]], ids=["empty", "one-byte", "half"]
    )
    def test_a_partial_read_is_retried_until_the_file_is_whole(self, tmp_path, partial):
        info_file = tmp_path / "server_info.json"
        info_file.write_text(partial)

        def finish(_now: float) -> None:
            info_file.write_text(FULL)

        assert _wait(info_file, _Thread(alive=True), _Clock(on_sleep=finish)) == INFO

    def test_a_partial_read_is_not_info(self, tmp_path):
        info_file = tmp_path / "server_info.json"
        info_file.write_text("")
        assert read_server_info(info_file) is None


class TestTheWaitLastsAsLongAsTheStart:
    """R-0708: a flat five seconds lost the race to a loaded `-n auto` run."""

    def test_a_slow_but_live_start_is_waited_for_past_the_old_five_seconds(self, tmp_path):
        info_file = tmp_path / "server_info.json"
        arrives_at = 30.0  # six times the flat budget that went red

        def publish(now: float) -> None:
            if now >= arrives_at:
                info_file.write_text(FULL)

        clock = _Clock(on_sleep=publish)
        assert _wait(info_file, _Thread(alive=True), clock) == INFO
        assert clock.now >= arrives_at

    def test_a_dead_server_thread_fails_at_once_rather_than_at_a_budget(self, tmp_path):
        clock = _Clock()
        with pytest.raises(pytest.fail.Exception, match="exited before publishing"):
            _wait(tmp_path / "server_info.json", _Thread(alive=False), clock)
        assert clock.now == 0.0

    def test_a_start_that_never_publishes_still_ends_at_the_backstop(self, tmp_path):
        clock = _Clock()
        with pytest.raises(pytest.fail.Exception, match="still alive but unpublished"):
            _wait(tmp_path / "server_info.json", _Thread(alive=True), clock)
        assert clock.now >= SERVER_START_BACKSTOP_S
