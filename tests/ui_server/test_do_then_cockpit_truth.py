"""amend1015 Part 7.1 — the gate that was missing: one order, then the cockpit, as a person sees it.

Every other test checks one piece of the cockpit alone. This one runs ONE `remedy do` order with
the fake providers on a tiny repository through the real CLI entry, starts the real cockpit
server for the job it made, and reads what the page reads, over plain HTTP: one task, done,
one of one; the recommendation names the apply command; the token line is there and no dollar
figure is; the ledger answers; the live stream answers with the token the client sends.
"""
from __future__ import annotations

import http.client
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import pytest

pytestmark = pytest.mark.integration

REPO = Path(__file__).resolve().parents[2]
UI_DIST = REPO / "apps" / "ui" / "dist" / "assets"
ORDER = "pass die readme an"
#: Wall-clock ceiling for the whole test; a healthy run takes a few seconds.
GATE_SECONDS = 20.0
SERVER_START_SECONDS = 15.0


def _env(data_dir: Path, ceiling: Path) -> dict[str, str]:
    # Built at call time from this process's environment (subprocess env must not escape the
    # scratch data root), with the checkout first on the path for children run from it.
    env = dict(os.environ)
    env.update({"REMEDY_DATA_DIR": str(data_dir), "GIT_CEILING_DIRECTORIES": str(ceiling),
                "PYTHONPATH": str(REPO)})
    return env


def _tiny_repo(root: Path) -> Path:
    repo = root / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    (repo / "README.md").write_text("# tiny\n")
    subprocess.run(["git", "add", "README.md"], cwd=repo, check=True)
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "init"],
                   cwd=repo, check=True)
    return repo


def _wait_for_info(info_file: Path, proc: subprocess.Popen) -> dict:
    deadline = time.monotonic() + SERVER_START_SECONDS
    while time.monotonic() < deadline:
        try:
            return json.loads(info_file.read_text())
        except (OSError, ValueError):
            if proc.poll() is not None:
                pytest.fail(f"the cockpit server exited with {proc.returncode} before publishing")
            time.sleep(0.05)
    pytest.fail("the cockpit server did not publish its info file")


def _get_json(base: str, path: str, token: str) -> dict:
    sep = "&" if "?" in path else "?"
    with urllib.request.urlopen(f"{base}{path}{sep}token={token}", timeout=10) as response:
        return json.loads(response.read())


def test_one_fake_do_run_then_the_cockpit_tells_one_story(tmp_path: Path) -> None:
    started = time.monotonic()
    data_dir = tmp_path / "data"
    env = _env(data_dir, tmp_path)
    repo = _tiny_repo(tmp_path)

    run = subprocess.run(
        [sys.executable, "-m", "apps.cli.grouped", "do", "run", ORDER, "--repo", str(repo),
         "--builder-provider", "fake", "--reviewer-provider", "fake", "--no-ui"],
        cwd=REPO, env=env, capture_output=True, text=True, timeout=GATE_SECONDS)
    assert run.returncode == 0, run.stdout + run.stderr
    # The CLI's own Cost line follows the default: tokens, never dollars (Part 5.2).
    assert "$" not in run.stdout, run.stdout
    [job_id] = set(re.findall(r"remedy job apply ([0-9a-f]{16}) --repo", run.stdout))

    info_file = tmp_path / "ui.json"
    server = subprocess.Popen(
        [sys.executable, "-m", "apps.cli.grouped", "ui", "start", job_id, "--port", "0",
         "--host", "127.0.0.1", "--no-open", "--info-file", str(info_file)],
        cwd=REPO, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        info = _wait_for_info(info_file, server)
        token = info["token"]
        assert f"job={job_id}" in info["url"] and f"token={token}" in info["url"]
        base = f"http://127.0.0.1:{info['port']}/api/jobs/{job_id}"

        dashboard = _get_json(base, "/dashboard", token)
        assert dashboard["metrics"]["done"] == 1
        assert dashboard["metrics"]["progress_percent"] == 100
        assert [t["state"] for t in dashboard["tasks"]] == ["done"]
        assert dashboard["live"]["running"] is False
        assert dashboard["token_usage"]["ledger"]["harness_invocations"] > 0

        digest = _get_json(base, "/digest", token)
        assert digest["primary_action"]["rule_id"] == "apply-pending"
        assert f"remedy job apply {job_id} --repo" in digest["primary_action"]["label"]
        assert digest["tokens"]["line"], digest["tokens"]
        assert "$" not in digest["tokens"]["line"]
        assert digest["tokens"]["show_cost_usd"] is False
        # The command bar and the card name one next command.
        assert dashboard["next_action"]["command"].startswith(f"remedy job apply {job_id}")

        events = _get_json(base, "/events-since?cursor=0", token)
        assert len(events["events"]) >= 1

        conn = http.client.HTTPConnection("127.0.0.1", info["port"], timeout=10)
        try:
            conn.request("GET", f"/api/jobs/{job_id}/events/stream?cursor=0&token={token}")
            response = conn.getresponse()
            assert response.status == 200
            assert response.getheader("Content-Type", "").startswith("text/event-stream")
        finally:
            conn.close()
    finally:
        server.terminate()
        try:
            server.wait(timeout=10)
        except subprocess.TimeoutExpired:
            server.kill()
            server.wait(timeout=10)
    assert time.monotonic() - started < GATE_SECONDS


def test_the_built_client_opens_its_stream_with_the_token() -> None:
    """The bundle the server ships builds the stream URL with `&token=` (Part 2.1)."""
    bundles = sorted(UI_DIST.glob("*.js")) if UI_DIST.is_dir() else []
    if not bundles:
        pytest.skip("apps/ui is not built; npm run build in apps/ui first")
    text = "\n".join(path.read_text(encoding="utf-8", errors="replace") for path in bundles)
    assert "/events/stream?cursor=" in text
    # `withToken` in brainStreamDeps.ts, as the minifier writes it: `${path}&token=${encodeURIComponent(token)}`.
    # The bundle built from main before amend1015 holds no such template (checked 2026-10-15).
    assert re.search(r"\$\{[A-Za-z_$]+\}&token=\$\{encodeURIComponent\([A-Za-z_$]+\)\}", text), (
        "the stream's path builder no longer appends the token")
