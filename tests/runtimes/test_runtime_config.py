"""F007 T002 — runtime configuration and detection.

Detection reads checked-in project files only: no project module is ever imported
or executed. Ambiguity blocks; explicit config always wins.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.runtimes.dev_server import RuntimeConfigError, project_digest
from packages.runtimes.runtime_config import (
    CONFIG_RELPATH,
    detect_runtimes,
    load_config_spec,
    resolve_spec,
)


def _write_config(root: Path, body: str) -> None:
    path = root / CONFIG_RELPATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body)


def _pkg(root: Path, rel: str, data: dict) -> None:
    d = root / rel
    d.mkdir(parents=True, exist_ok=True)
    (d / "package.json").write_text(json.dumps(data))


@pytest.fixture
def root(tmp_path) -> Path:
    p = tmp_path / "proj"
    p.mkdir()
    return p


# ---------------------------------------------------------------------------
# Explicit configuration
# ---------------------------------------------------------------------------

class TestExplicitConfig:
    def test_a_runtime_section_is_loaded(self, root):
        (root / "web").mkdir()
        _write_config(root, '''
[runtime]
cmd = ["npm", "run", "dev", "--", "--port", "{port}"]
cwd = "web"
port = 4321
health_path = "/healthz"
ready_timeout_s = 12
''')
        spec = load_config_spec(root)
        assert spec.cmd == ["npm", "run", "dev", "--", "--port", "{port}"]
        assert Path(spec.cwd) == (root / "web").resolve()
        assert spec.port == 4321 and spec.health_path == "/healthz"
        assert spec.ready_timeout_s == 12.0 and spec.source == "config"

    def test_explicit_config_beats_detection(self, root):
        _pkg(root, ".", {"scripts": {"dev": "vite"}, "devDependencies": {"vite": "^5"}})
        _write_config(root, '''
[runtime]
cmd = ["python3", "-m", "http.server", "{port}"]
port = 9000
''')
        spec = resolve_spec(root)
        assert spec.source == "config" and spec.cmd[0] == "python3"

    def test_a_shell_string_command_is_rejected(self, root):
        _write_config(root, '[runtime]\ncmd = "npm run dev"\n')
        with pytest.raises(RuntimeConfigError, match="argv list"):
            load_config_spec(root)

    def test_a_cwd_outside_the_project_is_rejected(self, root, tmp_path):
        _write_config(root, f'[runtime]\ncmd = ["echo"]\ncwd = "{tmp_path}"\n')
        with pytest.raises(RuntimeConfigError, match="outside the project"):
            load_config_spec(root)

    def test_traversal_in_cwd_is_rejected(self, root):
        _write_config(root, '[runtime]\ncmd = ["echo"]\ncwd = "../.."\n')
        with pytest.raises(RuntimeConfigError):
            load_config_spec(root)

    def test_an_invalid_port_is_rejected(self, root):
        _write_config(root, '[runtime]\ncmd = ["echo"]\nport = 99999\n')
        with pytest.raises(RuntimeConfigError, match="port"):
            load_config_spec(root)

    def test_an_invalid_health_path_is_rejected(self, root):
        _write_config(root, '[runtime]\ncmd = ["echo"]\nhealth_path = "healthz"\n')
        with pytest.raises(RuntimeConfigError, match="health_path"):
            load_config_spec(root)

    def test_an_invalid_timeout_is_rejected(self, root):
        _write_config(root, '[runtime]\ncmd = ["echo"]\nready_timeout_s = 0\n')
        with pytest.raises(RuntimeConfigError, match="ready_timeout_s"):
            load_config_spec(root)

    def test_broken_toml_is_reported(self, root):
        _write_config(root, "[runtime\ncmd = ")
        with pytest.raises(RuntimeConfigError, match="TOML"):
            load_config_spec(root)


# ---------------------------------------------------------------------------
# Detection
# ---------------------------------------------------------------------------

class TestDetection:
    def test_vite_is_detected(self, root):
        _pkg(root, "apps/ui", {"scripts": {"dev": "vite --host 127.0.0.1"},
                               "devDependencies": {"vite": "^5.0.0"}})
        found = detect_runtimes(root)
        assert [d.kind for d in found] == ["vite"]
        spec = resolve_spec(root)
        assert spec.source == "detected:vite"
        assert "{port}" in spec.cmd and spec.port == 5173
        assert Path(spec.cwd) == (root / "apps" / "ui").resolve()

    def test_next_is_detected(self, root):
        _pkg(root, "web", {"scripts": {"dev": "next dev"},
                           "dependencies": {"next": "^14"}})
        found = detect_runtimes(root)
        assert [d.kind for d in found] == ["next"]
        assert resolve_spec(root).port == 3000

    def test_the_project_package_manager_is_used(self, root):
        _pkg(root, "apps/ui", {"scripts": {"dev": "vite"},
                               "devDependencies": {"vite": "^5"}})
        (root / "apps" / "ui" / "pnpm-lock.yaml").write_text("lockfile\n")
        assert resolve_spec(root).cmd[0] == "pnpm"

    def test_fastapi_uvicorn_is_detected(self, root):
        (root / "pyproject.toml").write_text(
            '[project]\nname="x"\ndependencies = ["fastapi", "uvicorn"]\n')
        (root / "app").mkdir()
        (root / "app" / "main.py").write_text("app = None\n")
        found = detect_runtimes(root)
        assert [d.kind for d in found] == ["uvicorn"]
        spec = resolve_spec(root)
        assert spec.cmd[:3] == ["python3", "-m", "uvicorn"]
        assert "app.main:app" in spec.cmd and spec.port == 8000

    def test_uvicorn_without_a_conventional_module_is_not_guessed(self, root):
        (root / "requirements.txt").write_text("fastapi\nuvicorn\n")
        assert detect_runtimes(root) == []
        with pytest.raises(RuntimeConfigError, match="no runtime detected"):
            resolve_spec(root)

    def test_detection_never_imports_project_code(self, root):
        (root / "pyproject.toml").write_text('dependencies = ["fastapi"]\n')
        (root / "main.py").write_text("raise SystemExit('project code executed!')\n")
        found = detect_runtimes(root)             # must not execute main.py
        assert [d.kind for d in found] == ["uvicorn"]

    def test_an_ambiguous_project_blocks(self, root):
        _pkg(root, "apps/ui", {"scripts": {"dev": "vite"},
                               "devDependencies": {"vite": "^5"}})
        _pkg(root, "apps/web", {"scripts": {"dev": "next dev"},
                                "dependencies": {"next": "^14"}})
        assert len(detect_runtimes(root)) == 2
        with pytest.raises(RuntimeConfigError, match="ambiguous runtime"):
            resolve_spec(root)

    def test_an_ambiguous_project_can_be_disambiguated_by_config(self, root):
        _pkg(root, "apps/ui", {"scripts": {"dev": "vite"},
                               "devDependencies": {"vite": "^5"}})
        _pkg(root, "apps/web", {"scripts": {"dev": "next dev"},
                                "dependencies": {"next": "^14"}})
        _write_config(root, '[runtime]\ncmd = ["npm", "run", "dev"]\ncwd = "apps/ui"\n')
        assert resolve_spec(root).source == "config"

    def test_a_project_with_no_runtime_blocks(self, root):
        with pytest.raises(RuntimeConfigError, match="configuration required"):
            resolve_spec(root)


class TestProjectSeparation:
    def test_two_repositories_get_different_digests(self, tmp_path):
        a = tmp_path / "a"
        b = tmp_path / "b"
        a.mkdir()
        b.mkdir()
        assert project_digest(a) != project_digest(b)
        assert project_digest(a) == project_digest(a)
