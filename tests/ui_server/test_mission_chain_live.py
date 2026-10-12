"""F305 T003, DECISIONS F305 D1 to D3; R-1248 — the missions panel and its chain band, end to end
through the cockpit in a real browser.

Two projects are registered over two real git folders, and one order over both is accepted the
way `remedy do` accepts an order over several repositories: one batch in each repository's own
mission, the batches sharing a correlation id. The order holds three jobs, two in alpha and one in
beta, and alpha's ledger holds two model calls of its jobs. The REAL UI server is started for
alpha's first job in this process, serving a cockpit built into this module's own temporary
folder (never the shared `apps/ui/dist`, DECISION F039 D9), and headless Chrome is driven over
`--remote-debugging-pipe` with the story test's `ChromePipe`.

What it proves, as a person meets it: the right panel's Missions button opens one card for alpha's
mission; its orders are read only when the card is opened; the order shows its calls and tokens and
three chips naming two projects; a click on beta's chip opens beta's cockpit on beta's job, whose
own missions panel shows beta's mission with the same three chips and beta's job marked current;
and the browser's Back step returns to alpha's job.
"""
from __future__ import annotations

import base64
import subprocess
import threading
from pathlib import Path
from typing import Any

import pytest

from packages.orchestration.mission_state import MissionOrder
from packages.orchestration.pingpong_job import JobPlan, save_job_plan
from packages.orchestration.project_registry import register_project_repo
from packages.orchestration.repo_mission import accept_order_in_each, link_order_job
from tests.ui_server.test_story_export_file_live import (
    CHROME_BIN,
    CHROME_STARTUP_TIMEOUT,
    IDLE_DRAIN_SECONDS,
    VITE_BIN,
    ChromePipe,
    _poll,
)

REPO_ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def cockpit_dist(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Once per module: the cockpit built into ITS OWN temporary folder."""
    if not VITE_BIN.is_file():
        pytest.skip(f"{VITE_BIN} is not built; run `cd apps/ui && npm install`")
    out_dir = tmp_path_factory.mktemp("cockpit-build") / "dist"
    proc = subprocess.run(
        [str(VITE_BIN), "build", "--outDir", str(out_dir), "--emptyOutDir"],
        cwd=str(REPO_ROOT / "apps" / "ui"), capture_output=True, text=True, timeout=300,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert (out_dir / "index.html").is_file()
    return out_dir


def _repo(path: Path) -> Path:
    path.mkdir()
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    subprocess.run(["git", "-C", str(path), "-c", "user.email=a@b", "-c", "user.name=n",
                    "commit", "-q", "--allow-empty", "-m", "x"], check=True)
    return path


def _order_over_two_repositories(tmp_path: Path) -> dict[str, str]:
    """The acceptance fixture of `docs/roadmap/features/T13_F305.md`: three jobs in two repositories."""
    from packages.orchestration.token_ledger import CallRecord, record_call

    alpha = register_project_repo("alpha", _repo(tmp_path / "alpha"))
    beta = register_project_repo("beta", _repo(tmp_path / "beta"))
    accepted = accept_order_in_each(
        [(alpha, alpha.canonical_repo_path), (beta, beta.canonical_repo_path)],
        MissionOrder(text="Add a health route to both services"))
    ids = {}
    for key, project, title in (("a1", alpha, "Add the route to alpha"), ("b1", beta, "Add the route to beta"),
                                ("a2", alpha, "Document alpha's route")):
        job = JobPlan(job_title=title, project_id=str(project.id), repo_path=project.canonical_repo_path)
        save_job_plan(job)
        mission_id, order_id = accepted[str(project.id)]
        link_order_job(str(project.id), mission_id, order_id, str(job.job_id))
        ids[key] = str(job.job_id)
    for call_id, key, tokens_in, tokens_out in (("c1", "a1", 100, 20), ("c2", "a2", 50, 5)):
        assert record_call(CallRecord(call_id=call_id, job_id=ids[key], ts_utc="2026-10-12T09:00:00+00:00",
                                      tokens_in=tokens_in, tokens_out=tokens_out), project_id=alpha.id)
    return ids


def _start_server(job_id: str, tmp_path: Path) -> dict[str, Any]:
    """The REAL UI server for ``job_id`` in a daemon thread; its published info."""
    import secrets

    from packages.orchestration.ui_server import start_ui_server
    from tests.ui_server.server_start import wait_for_server_info

    info_file = str(tmp_path / "server_info.json")

    def run() -> None:
        try:
            start_ui_server(job_id, host="127.0.0.1", port=0, token=secrets.token_hex(16),
                            open_browser=False, info_file=info_file)
        except (SystemExit, KeyboardInterrupt):
            pass

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    return wait_for_server_info(info_file, thread)


def _click(selector: str) -> str:
    return (f"(() => {{ const el = document.querySelector('{selector}'); if (el) el.click(); "
            "return !!el; })()")


COCKPIT = "document.querySelector('[data-ui=\"remedy-visual-v2\"]') !== null"
CARDS = ("Array.from(document.querySelectorAll('[data-ui=\"mission-card\"] button[aria-expanded]'))"
         ".map((b) => b.textContent)")
CHIPS = ("Array.from(document.querySelectorAll('[data-ui=\"mission-chip\"]'))"
         ".map((c) => [c.getAttribute('data-project'), c.getAttribute('data-job'), c.getAttribute('aria-current')])")
USAGE = "(document.querySelector('[data-ui=\"mission-order-usage\"]') || {}).textContent || null"
ORDERS_SHOWN = "document.querySelector('[data-ui=\"mission-orders\"]') !== null"
# The computed box of the rules `MissionPanel.module.css` adds that a text check cannot see: the
# panel floats over the page, the band wraps its chips, and the current job's chip is outlined.
STYLES = (
    "(() => { const s = (q) => getComputedStyle(document.querySelector(q));"
    " return [s('[data-ui=\"mission-panel\"]').position, s('[data-ui=\"mission-chain\"]').flexWrap,"
    " s('[data-ui=\"mission-chip\"][aria-current=\"true\"]').borderTopColor"
    " !== s('[data-ui=\"mission-chip\"]:not([aria-current])').borderTopColor]; })()"
)


def _orders_requests(events: list[dict[str, Any]]) -> list[str]:
    return [e["params"]["request"]["url"] for e in events
            if e.get("method") == "Network.requestWillBeSent" and "/orders?" in e["params"]["request"]["url"]]


def _open_missions_and_card(pipe: ChromePipe) -> None:
    assert _poll(pipe, _click('[data-ui="missions-button"]'), lambda v: v is True, timeout=20.0)
    assert _poll(pipe, CARDS, lambda v: isinstance(v, list) and len(v) == 1, timeout=20.0)


def test_the_missions_panel_shows_an_orders_chain_and_a_chip_opens_the_other_projects_cockpit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, cockpit_dist: Path,
) -> None:
    if CHROME_BIN is None:
        pytest.skip("neither google-chrome nor chromium is on the path")
    from packages.orchestration import ui_server

    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.delenv("REMEDY_PROJECT", raising=False)
    monkeypatch.setattr(ui_server, "_get_frontend_dist", lambda: cockpit_dist)
    monkeypatch.setattr(ui_server, "_frontend_is_stale", lambda: False)
    ids = _order_over_two_repositories(tmp_path)
    info = _start_server(ids["a1"], tmp_path)
    expected_chain = [["alpha", ids["a1"]], ["beta", ids["b1"]], ["alpha", ids["a2"]]]

    pipe = ChromePipe(CHROME_BIN, tmp_path / "profile", log_path=tmp_path / "chrome.log")
    events: list[dict[str, Any]] = []
    try:
        target = pipe.send("Target.createTarget", {"url": "about:blank"}, timeout=CHROME_STARTUP_TIMEOUT)
        attach = pipe.send("Target.attachToTarget", {"targetId": target["targetId"], "flatten": True})
        pipe.session_id = attach["sessionId"]
        for domain in ("Page.enable", "Runtime.enable", "Log.enable", "Network.enable"):
            pipe.send(domain)
        pipe.send("Page.addScriptToEvaluateOnNewDocument", {
            "source": "window.localStorage.setItem('remedy:first-run-tour', 'seen');"})
        pipe.send("Page.navigate", {"url": info["url"]})
        assert _poll(pipe, COCKPIT, lambda v: v is True, timeout=30.0)

        # ONE CARD for alpha's mission, its orders not read until the card is opened.
        _open_missions_and_card(pipe)
        assert _poll(pipe, CARDS, lambda v: v is not None) == ["Maintain alpha1 order · 2 jobs"]
        pipe.drain(IDLE_DRAIN_SECONDS)
        assert _poll(pipe, ORDERS_SHOWN, lambda v: v is False) is False
        assert _orders_requests(list(pipe.events)) == []

        # OPENED, the order shows its calls and tokens and three chips naming two projects.
        assert _poll(pipe, _click('[data-ui="mission-card"] button[aria-expanded]'), lambda v: v is True)
        chips = _poll(pipe, CHIPS, lambda v: isinstance(v, list) and len(v) == 3, timeout=20.0)
        assert [chip[:2] for chip in chips] == expected_chain
        assert [chip[2] for chip in chips] == ["true", None, None]
        assert _poll(pipe, USAGE, lambda v: v is not None) == "2 model calls · 150 tokens in, 25 out"
        assert len(_orders_requests(list(pipe.events))) == 1
        assert _poll(pipe, STYLES, lambda v: v is not None) == ["fixed", "wrap", True]
        shot = pipe.send("Page.captureScreenshot", {"format": "png"})
        (tmp_path / "missions-panel.png").write_bytes(base64.b64decode(shot["data"]))

        # A CLICK on beta's chip opens beta's cockpit on beta's job.
        chip = f'[data-ui="mission-chip"][data-job="{ids["b1"]}"]'
        assert _poll(pipe, _click(chip), lambda v: v is True)
        search = _poll(pipe, "window.location.search",
                       lambda v: isinstance(v, str) and f"job={ids['b1']}" in v, timeout=20.0)
        assert "project=beta" in search and "token=" in search
        assert _poll(pipe, COCKPIT, lambda v: v is True, timeout=30.0)
        assert _poll(pipe, "document.querySelector('[data-ui=\"mission-panel\"]') === null", lambda v: v is True)

        # BETA'S OWN PANEL shows beta's mission, the same three chips, and beta's job as current.
        _open_missions_and_card(pipe)
        assert _poll(pipe, CARDS, lambda v: v is not None) == ["Maintain beta1 order · 1 job"]
        assert _poll(pipe, _click('[data-ui="mission-card"] button[aria-expanded]'), lambda v: v is True)
        chips = _poll(pipe, CHIPS, lambda v: isinstance(v, list) and len(v) == 3, timeout=20.0)
        assert [chip[:2] for chip in chips] == expected_chain
        assert [chip[2] for chip in chips] == [None, "true", None]
        assert _poll(pipe, USAGE, lambda v: v is not None) == "No model calls"

        # BACK returns to alpha's job: the chip pushed the address rather than replacing it.
        pipe.send("Runtime.evaluate", {"expression": "window.history.back()"})
        assert _poll(pipe, "window.location.search",
                     lambda v: isinstance(v, str) and f"job={ids['a1']}" in v, timeout=20.0)
        assert _poll(pipe, COCKPIT, lambda v: v is True, timeout=30.0)
        pipe.drain(IDLE_DRAIN_SECONDS)
    finally:
        events = list(pipe.events)
        pipe.close()

    dashboards = [e["params"]["request"]["url"] for e in events
                  if e.get("method") == "Network.requestWillBeSent" and "/dashboard?" in e["params"]["request"]["url"]]
    assert any(f"/api/jobs/{ids['b1']}/dashboard?" in url for url in dashboards)
    exceptions = [e for e in events if e.get("method") == "Runtime.exceptionThrown"]
    assert exceptions == []
    log_errors = [
        e for e in events
        if e.get("method") == "Log.entryAdded"
        and e["params"]["entry"].get("level") == "error"
        and e["params"]["entry"].get("source") != "network"
    ]
    assert log_errors == []
