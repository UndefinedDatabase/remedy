"""F305 T002, DECISIONS F305 D1 and D2 — the cockpit's mission card agrees with the server and is
mounted where the decisions say.

`apps/ui/src/api/missionCard.test.ts` pins the client's rules with envelopes typed by hand; this
file closes the other side: every interface the client declares for a mission envelope carries
EXACTLY the keys `packages/orchestration/mission_cockpit.py` answers, read from what the module
really answers for an order over two repositories. The panel has no DOM harness (DECISION F031
D5), so its wiring is pinned here over COMMENT-STRIPPED source (finding R-0584); the behaviour is
proved in a real browser by `tests/ui_server/test_mission_chain_live.py` (T003).
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

from packages.orchestration.mission_cockpit import (
    MISSION_COCKPIT_VERSION,
    mission_orders_view,
    project_missions_view,
)
from packages.orchestration.mission_state import MISSING_JOB_LABEL, UNREADABLE_JOB_LABEL, MissionOrder
from packages.orchestration.pingpong_job import JobPlan, save_job_plan
from packages.orchestration.project_registry import register_project_repo
from packages.orchestration.repo_mission import accept_order_in_each, link_order_job
from tests.ui_contracts.test_brain_stream_ring import strip_ts_comments

REPO_ROOT = Path(__file__).resolve().parents[2]
UI_SRC = REPO_ROOT / "apps" / "ui" / "src"
SEAM = UI_SRC / "api" / "missionCard.ts"
DOOR = UI_SRC / "api" / "missionCardDoor.ts"
PANEL = UI_SRC / "components" / "missions" / "MissionPanel.tsx"
PANEL_CSS = UI_SRC / "components" / "missions" / "MissionPanel.module.css"
SHELL = UI_SRC / "components" / "shell" / "RemedyShell.tsx"
RIGHT_PANEL = UI_SRC / "components" / "panels" / "RightLivePanel.tsx"
PROVIDER = UI_SRC / "components" / "shell" / "ProjectProvider.tsx"
ROUTES = REPO_ROOT / "packages" / "orchestration" / "cockpit_project_routes.py"

_RAW_COLOUR = re.compile(r"#[0-9a-fA-F]{3,8}\b|\b(?:rgba?|hsla?)\(")


def _source(path: Path) -> str:
    return strip_ts_comments(path.read_text(encoding="utf-8"))


def _interfaces() -> dict[str, set[str]]:
    source = SEAM.read_text(encoding="utf-8")
    found = {}
    for name, body in re.findall(r"^export interface (\w+) \{\n(.*?)^\}", source, re.MULTILINE | re.DOTALL):
        found[name] = set(re.findall(r"^\s+(?:readonly\s+)?(\w+)\??:", body, re.MULTILINE))
    return found


def _repo(path: Path) -> Path:
    path.mkdir()
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    subprocess.run(["git", "-C", str(path), "-c", "user.email=a@b", "-c", "user.name=n",
                    "commit", "-q", "--allow-empty", "-m", "x"], check=True)
    return path


@pytest.fixture
def envelopes(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.delenv("REMEDY_PROJECT", raising=False)
    alpha = register_project_repo("alpha", _repo(tmp_path / "alpha"))
    beta = register_project_repo("beta", _repo(tmp_path / "beta"))
    accepted = accept_order_in_each(
        [(alpha, alpha.canonical_repo_path), (beta, beta.canonical_repo_path)],
        MissionOrder(text="Add a health route"))
    for project in (alpha, beta):
        job = JobPlan(job_title=f"{project.slug} job", project_id=str(project.id),
                      repo_path=project.canonical_repo_path)
        save_job_plan(job)
        mission_id, order_id = accepted[str(project.id)]
        link_order_job(str(project.id), mission_id, order_id, str(job.job_id))
    status, orders = mission_orders_view(alpha, accepted[str(alpha.id)][0])
    assert status == 200
    return {"missions": project_missions_view(alpha), "orders": orders}


def test_every_mission_interface_carries_exactly_the_servers_keys(envelopes):
    missions, orders = envelopes["missions"], envelopes["orders"]
    [card] = missions["missions"]
    [order] = orders["orders"]
    assert len(order["chain"]) == 2
    expected = {
        "ProjectMissions": set(missions),
        "MissionCardEntry": set(card),
        "MissionOrders": set(orders),
        "MissionOrderRow": set(order),
        "MissionOrderUsage": set(order["usage"]),
        "MissionTokens": set(order["usage"]["tokens"]),
        "MissionChip": set(order["chain"][0]),
    }
    interfaces = _interfaces()
    assert {name: interfaces.get(name) for name in expected} == expected


def test_the_client_understands_the_servers_version_and_labels():
    source = SEAM.read_text(encoding="utf-8")
    assert f"export const MISSION_COCKPIT_VERSION = {MISSION_COCKPIT_VERSION};" in source
    assert f'export const MISSING_JOB_LABEL = "{MISSING_JOB_LABEL}";' in source
    assert f'export const UNREADABLE_JOB_LABEL = "{UNREADABLE_JOB_LABEL}";' in source


def test_the_client_paths_name_the_routes_the_server_answers():
    seam = _source(SEAM)
    routes = ROUTES.read_text(encoding="utf-8")
    assert "/missions?token=" in seam and 'parts[4] == "missions"' in routes
    assert "/orders?token=" in seam and 'parts[6] == "orders"' in routes


def test_the_seam_is_pure_and_words_no_cost_in_dollars():
    code = _source(SEAM)
    assert "export function decodeMissionOrders" in code
    for forbidden in ("fetch(", "Date", "localStorage", "sessionStorage", "window.", "document.", "usd", "USD"):
        assert forbidden not in code, forbidden


def test_the_door_is_the_one_network_read_and_the_panel_has_none():
    door = _source(DOOR)
    assert door.count("fetch(") == 1
    assert 'method: "GET"' in door and 'credentials: "same-origin"' in door
    assert "fetch(" not in _source(PANEL)


def test_the_panel_is_a_region_portaled_to_the_document_body():
    panel = _source(PANEL)
    assert "createPortal(" in panel and "document.body" in panel
    assert 'role="region"' in panel and 'data-ui="mission-panel"' in panel
    assert 'data-ui="mission-chip"' in panel and "onOpenJob(chip.slug, chip.job_id)" in panel
    assert "disabled={!chipOpenable(chip)}" in panel


def test_the_panel_reads_a_missions_orders_only_once_its_card_is_open():
    panel = _source(PANEL)
    effect = panel[panel.index("loadMissionOrders({"):]
    assert 'if (project === "" || openMissionId === null) return;' in panel
    assert "[project, serverToken, openMissionId]" in effect


def test_the_css_module_names_the_overlay_layer_with_no_raw_colour():
    css = PANEL_CSS.read_text(encoding="utf-8")
    assert "var(--remedy-z-overlay)" in css
    assert not _RAW_COLOUR.search(css)


def test_the_shell_mounts_the_panel_outside_main_and_the_right_panel_opens_it():
    shell = _source(SHELL)
    assert shell.index("</main>") < shell.index("<MissionPanel")
    assert "onOpenMissions={() => setMissionsOpen(true)}" in shell
    assert 'project={projectContext.active?.slug ?? ""}' in shell
    assert "onOpenJob={projectContext.openJob}" in shell
    panel = _source(RIGHT_PANEL)
    assert 'data-ui="missions-button" onClick={onOpenMissions}>Missions</button>' in panel


def test_a_chip_opens_its_job_through_the_one_gate_and_the_one_address_writer():
    provider = _source(PROVIDER)
    body = provider[provider.index("const openJob = useCallback("):provider.index("const value = useMemo")]
    assert "gate.current.begin(slug);" in body
    assert "onSwitched({ slug, jobId, summary: null }, false);" in body
