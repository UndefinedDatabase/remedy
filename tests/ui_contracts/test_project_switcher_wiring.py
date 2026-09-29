"""F042 T002, DECISION F042 D3 — the project seam is mounted where the decision says.

Written by the reviewer. The cockpit has no DOM test harness, so the wiring a render proves is
pinned here over the sources, with their comments removed, at the places no vitest file
reaches: the app's one provider, the shell keyed by project and job, the address changed only
by a switch or a Back step, and the switcher in the brand rail's kicker. The behaviour itself is
proved in a real browser by the round's render harness.
"""

from __future__ import annotations

import re
from pathlib import Path

UI_SRC = Path(__file__).resolve().parents[2] / "apps" / "ui" / "src"
APP = UI_SRC / "RemedyApp.tsx"
PROVIDER = UI_SRC / "components" / "shell" / "ProjectProvider.tsx"
SWITCHER = UI_SRC / "components" / "shell" / "ProjectSwitcher.tsx"
RAIL = UI_SRC / "components" / "rail" / "LeftBrandRail.tsx"


def _code(path: Path) -> str:
    source = path.read_text(encoding="utf-8")
    return re.sub(r"//[^\n]*", "", re.sub(r"/\*.*?\*/", "", source, flags=re.DOTALL))


def test_the_app_mounts_one_provider_around_every_face():
    code = _code(APP)
    assert code.count("<ProjectProvider ") == 1
    assert "onSwitched={onSwitched}" in code
    assert code.index("<ProjectProvider ") < code.index("{body}") < code.index("</ProjectProvider>")


def test_a_new_project_or_job_is_a_new_shell():
    code = _code(APP)
    assert "<RemedyShell key={shellKeyOf(address)}" in code


def test_only_a_switch_or_a_back_step_changes_the_address():
    code = _code(APP)
    assert code.count("window.history.pushState(") == 1
    assert "searchForProjectSwitch(window.location.search, target.slug, target.jobId)" in code
    assert 'window.addEventListener("popstate", onPopState)' in code
    assert 'window.removeEventListener("popstate", onPopState)' in code
    assert "replaceState" not in code


def test_the_provider_switches_through_the_one_gate():
    code = _code(PROVIDER)
    assert code.count("createSwitchGate(") == 1
    assert "switchProject(slug, gate.current," in code
    assert "loadProjectsView(" in code and "loadJobProject(" in code and "loadProjectSummary(" in code


def test_the_switcher_is_a_native_select_in_the_rails_kicker():
    switcher = _code(SWITCHER)
    assert "switcherVisible(view)" in switcher
    assert "<select" in switcher and "aria-label={PROJECT_SWITCHER_LABEL}" in switcher
    assert "@mui" not in switcher
    rail = _code(RAIL)
    assert "<ProjectSwitcher fallback={<div className={styles.concept}>CONCEPT 01 OF 10</div>} />" in rail
