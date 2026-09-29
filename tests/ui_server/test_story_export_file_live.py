"""F039 T003, DECISIONS F039 D7, D8 and D9 — the zero-network proof.

Remedy deliberately proves the export in a real browser rather than by reading the file: the
exported page's own content security policy, its embedded player and its embedded data are
each things a browser enforces or executes, not things a text reader can check. This test runs
the demo job on the fake providers exactly as
``tests/ui_server/test_brain_demo_recording_live.py`` does, exports its story around a player
built into its own temporary folder, and drives headless Chrome over
``--remote-debugging-pipe`` — Chrome's own file-descriptor transport, driven with nothing but
the standard library, because Node 20 (CI's pinned runtime) carries no WebSocket client and a
pinned WebSocket dependency would exist for this one test alone.
"""
from __future__ import annotations

import json
import os
import select
import shutil
import subprocess
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

from packages.orchestration.config import get_key_spec
from packages.orchestration.story_export import export_story_html
from tests.ui_server.test_brain_demo_recording_live import CLI, ORDER, _env, _git_repo, _run

REPO_ROOT = Path(__file__).resolve().parents[2]
VITE_BIN = REPO_ROOT / "apps" / "ui" / "node_modules" / ".bin" / "vite"
CHROME_BIN = shutil.which("google-chrome") or shutil.which("chromium")

STORY_EXPORT_MAX_BYTES = get_key_spec("story.export_max_bytes").default

# R-1103: `ChromePipe.send` only files a message as an event while a command reply is
# outstanding, and the test's last check answers well under a second after the page loads, so a
# request the page makes once idle — after every check has already passed — was never collected.
# Draining for this long with nothing outstanding, directly after the last check, closes the gap.
IDLE_DRAIN_SECONDS = 2.0

CHAPTERS_EXPR = (
    'Array.from(document.querySelectorAll(\'[data-ui="story-chapters"] button\'))'
    ".map((b) => b.textContent)"
)
POSITION_EXPR = 'document.querySelector(\'[data-ui="story-position"]\').textContent'
SLIDER_VALUE_EXPR = (
    'Number(document.querySelector(\'[role="slider"]\').getAttribute("aria-valuenow"))'
)
PLAY_PAUSE_EXPR = (
    "(() => { const b = Array.from(document.querySelectorAll("
    "'[data-ui=\"story-panel\"] button')).find("
    "(el) => el.textContent === 'Play' || el.textContent === 'Pause'); "
    "return b ? b.textContent : null; })()"
)
CLOSE_BUTTON_PRESENT_EXPR = (
    "Array.from(document.querySelectorAll('[data-ui=\"story-panel\"] button'))"
    ".some((b) => b.textContent === 'Close story')"
)


class ChromePipe:
    """Drives headless Chrome over ``--remote-debugging-pipe``: Chrome reads commands on file
    descriptor 3 and writes replies on file descriptor 4, each message one JSON object ended
    by one NUL byte. No websocket-client, no Node driver — the two pipes this class opens are
    the whole transport.
    """

    def __init__(self, chrome: str, profile_dir: Path) -> None:
        cmd_r, cmd_w = os.pipe()
        reply_r, reply_w = os.pipe()
        script = f'exec "$0" "$@" 3<&{cmd_r} 4>&{reply_w}'
        args = [
            "--headless=new",
            "--remote-debugging-pipe",
            f"--user-data-dir={profile_dir}",
            "--no-first-run",
            "--no-default-browser-check",
            "--window-size=1280,800",
            "about:blank",
        ]
        self._proc = subprocess.Popen(
            ["bash", "-c", script, chrome, *args],
            pass_fds=(cmd_r, reply_w),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        os.close(cmd_r)
        os.close(reply_w)
        self._cmd_w = cmd_w
        self._reply_r = reply_r
        self._buffer = b""
        self._next_id = 1
        self.session_id: str | None = None
        self.events: list[dict[str, Any]] = []

    def _read_message(self, deadline: float) -> dict[str, Any]:
        while b"\0" not in self._buffer:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError("timed out waiting for a reply from Chrome's pipe")
            ready, _, _ = select.select([self._reply_r], [], [], remaining)
            if not ready:
                continue
            chunk = os.read(self._reply_r, 1 << 16)
            if not chunk:
                raise EOFError("Chrome's reply pipe closed before answering")
            self._buffer += chunk
        raw, _, self._buffer = self._buffer.partition(b"\0")
        return json.loads(raw.decode("utf-8"))

    def send(self, method: str, params: dict[str, Any] | None = None, *, timeout: float = 15.0) -> dict[str, Any]:
        message_id = self._next_id
        self._next_id += 1
        payload: dict[str, Any] = {"id": message_id, "method": method, "params": params or {}}
        if self.session_id is not None:
            payload["sessionId"] = self.session_id
        os.write(self._cmd_w, json.dumps(payload).encode("utf-8") + b"\0")
        deadline = time.monotonic() + timeout
        while True:
            message = self._read_message(deadline)
            if message.get("id") == message_id:
                if "error" in message:
                    raise RuntimeError(f"{method} failed: {message['error']}")
                return message.get("result", {})
            self.events.append(message)

    def drain(self, seconds: float) -> None:
        """Keeps every message Chrome sends as an event until ``seconds`` pass with no command
        outstanding — nothing here is a reply to wait for, so anything that arrives is an event."""
        deadline = time.monotonic() + seconds
        while True:
            try:
                message = self._read_message(deadline)
            except TimeoutError:
                return
            self.events.append(message)

    def close(self) -> None:
        self._proc.terminate()
        try:
            self._proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self._proc.kill()
            self._proc.wait(timeout=10)
        os.close(self._cmd_w)
        os.close(self._reply_r)


def _poll(pipe: ChromePipe, expression: str, predicate: Callable[[Any], bool], *, timeout: float = 15.0) -> Any:
    deadline = time.monotonic() + timeout
    last: Any = None
    while time.monotonic() < deadline:
        result = pipe.send("Runtime.evaluate", {"expression": expression, "returnByValue": True})
        last = result.get("result", {}).get("value")
        if predicate(last):
            return last
        time.sleep(0.2)
    raise AssertionError(f"timed out polling {expression!r}; last value was {last!r}")


def _dispatch_key(pipe: ChromePipe, *, key: str, code: str, virtual_key_code: int, text: str | None = None) -> None:
    down: dict[str, Any] = {
        "type": "keyDown", "key": key, "code": code,
        "windowsVirtualKeyCode": virtual_key_code, "nativeVirtualKeyCode": virtual_key_code,
    }
    if text is not None:
        down["text"] = text
    up = {k: v for k, v in down.items() if k != "text"}
    up["type"] = "keyUp"
    pipe.send("Input.dispatchKeyEvent", down)
    pipe.send("Input.dispatchKeyEvent", up)


@pytest.fixture(scope="module")
def story_player_dir(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Once per module: the story player's second build into ITS OWN temporary folder — never
    the shared ``apps/ui/dist``, which a parallel worker's own cockpit build could empty out
    from under a test reading it (DECISION F039 D9)."""
    if not VITE_BIN.is_file():
        pytest.skip(f"{VITE_BIN} is not built; run `cd apps/ui && npm install`")
    out_dir = tmp_path_factory.mktemp("story-player-build") / "dist"
    proc = subprocess.run(
        [str(VITE_BIN), "build", "--outDir", str(out_dir), "--emptyOutDir"],
        cwd=str(REPO_ROOT / "apps" / "ui"), capture_output=True, text=True, timeout=300,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    player_dir = out_dir / "story"
    assert sorted(p.name for p in player_dir.iterdir()) == ["story-player.css", "story-player.js"]
    return player_dir


def test_the_exported_demo_story_plays_from_file_with_no_request(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, story_player_dir: Path,
) -> None:
    if CHROME_BIN is None:
        pytest.skip("neither google-chrome nor chromium is on the path")

    data_dir = tmp_path / "data"
    env = _env(data_dir)
    repo = _git_repo(tmp_path)

    init_result = _run([*CLI, "init"], cwd=repo, env=env)
    assert init_result.returncode == 0, init_result.stderr

    plan_result = _run([*CLI, "do", ORDER, "--no-llm", "--plan-only", "--json"], cwd=repo, env=env)
    assert plan_result.returncode == 0, plan_result.stderr
    job_id = json.loads(plan_result.stdout)["job_ids"][0]

    run_result = _run(
        [*CLI, "job", "run", job_id, "--builder-provider", "fake", "--reviewer-provider", "fake", "--json"],
        cwd=repo, env=env,
    )
    assert run_result.returncode == 0, run_result.stderr

    # In-process read needs REMEDY_DATA_DIR in THIS process's environment (the CLI subprocess
    # env above does not reach `load_job_plan` here) — scoped to this test via monkeypatch,
    # exactly as test_brain_demo_recording_live.py does.
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    from packages.orchestration.pingpong_job import load_job_plan

    job = load_job_plan(job_id)
    assert job is not None

    data = export_story_html(job, max_bytes=STORY_EXPORT_MAX_BYTES, player_dir=story_player_dir)
    story_path = tmp_path / "story.html"
    story_path.write_bytes(data)
    file_url = story_path.resolve().as_uri()

    pipe = ChromePipe(CHROME_BIN, tmp_path / "profile")
    events: list[dict[str, Any]] = []
    try:
        target = pipe.send("Target.createTarget", {"url": "about:blank"})
        attach = pipe.send("Target.attachToTarget", {"targetId": target["targetId"], "flatten": True})
        pipe.session_id = attach["sessionId"]
        pipe.send("Network.enable")
        pipe.send("Page.enable")
        pipe.send("Runtime.enable")
        pipe.send("Log.enable")
        pipe.send("Page.navigate", {"url": file_url})

        chapters = _poll(pipe, CHAPTERS_EXPR, lambda v: v == ["The build", "The review", "The finish"])
        assert chapters == ["The build", "The review", "The finish"]

        position = _poll(pipe, POSITION_EXPR, lambda v: v == "Chapter 3 of 3: The finish")
        assert position == "Chapter 3 of 3: The finish"

        value = _poll(pipe, SLIDER_VALUE_EXPR, lambda v: v == 9)
        assert value == 9

        pipe.send("Runtime.evaluate", {"expression": 'document.querySelector(\'[role="slider"]\').focus()'})
        _dispatch_key(pipe, key="ArrowLeft", code="ArrowLeft", virtual_key_code=37)
        value = _poll(pipe, SLIDER_VALUE_EXPR, lambda v: v == 8)
        assert value == 8

        pipe.send(
            "Runtime.evaluate",
            {"expression": 'document.querySelectorAll(\'[data-ui="story-chapters"] button\')[1].click()'},
        )
        position = _poll(pipe, POSITION_EXPR, lambda v: v == "Chapter 2 of 3: The review")
        assert position == "Chapter 2 of 3: The review"

        pipe.send(
            "Runtime.evaluate",
            {"expression": "document.activeElement && document.activeElement.blur()"},
        )
        _dispatch_key(pipe, key=" ", code="Space", virtual_key_code=32, text=" ")
        label = _poll(pipe, PLAY_PAUSE_EXPR, lambda v: v == "Pause")
        assert label == "Pause"

        _dispatch_key(pipe, key=" ", code="Space", virtual_key_code=32, text=" ")
        label = _poll(pipe, PLAY_PAUSE_EXPR, lambda v: v == "Play")
        assert label == "Play"

        close_present = pipe.send(
            "Runtime.evaluate", {"expression": CLOSE_BUTTON_PRESENT_EXPR, "returnByValue": True},
        )["result"]["value"]
        assert close_present is False

        pipe.drain(IDLE_DRAIN_SECONDS)
    finally:
        events = list(pipe.events)
        pipe.close()

    request_urls = [
        e["params"]["request"]["url"] for e in events if e.get("method") == "Network.requestWillBeSent"
    ]
    assert request_urls == [file_url]

    exceptions = [e for e in events if e.get("method") == "Runtime.exceptionThrown"]
    assert exceptions == []

    log_errors = [
        e for e in events
        if e.get("method") == "Log.entryAdded" and e.get("params", {}).get("entry", {}).get("level") == "error"
    ]
    assert log_errors == []

    assert story_path.stat().st_size <= STORY_EXPORT_MAX_BYTES
