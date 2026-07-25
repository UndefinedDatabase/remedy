"""Runtime configuration and detection (F007 T002).

The canonical runtime spec for a project lives in ``.remedy/config.toml``:

    [runtime]
    cmd = ["npm", "run", "dev", "--", "--port", "{port}"]
    cwd = "apps/ui"
    port = 5173
    health_path = "/"
    ready_timeout_s = 30

This is deliberately separate from Remedy's general ``remedy.toml`` configuration
system, which is not migrated or replaced here.

When no config exists, the runtime is DETECTED from checked-in project files only —
package.json, pyproject.toml, requirements files. No project module is ever imported
or executed to identify it. Detection that matches more than one runtime is
ambiguous and BLOCKS with a configuration-required message rather than guessing.
Explicit config always wins.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from packages.runtimes.dev_server import (
    RuntimeConfigError,
    RuntimeSpec,
    validate_spec,
)

try:                                   # Python >= 3.11
    import tomllib
except ModuleNotFoundError:            # Python 3.10 with the tomli backport
    import tomli as tomllib  # type: ignore[no-redef]

CONFIG_RELPATH = Path(".remedy") / "config.toml"

DEFAULT_HEALTH_PATH = "/"
DEFAULT_TIMEOUT_S = 30.0


@dataclass(frozen=True)
class DetectedRuntime:
    kind: str                       # "vite" | "next" | "uvicorn"
    spec: RuntimeSpec
    signals: list[str]


# ---------------------------------------------------------------------------
# Explicit configuration
# ---------------------------------------------------------------------------

def _require_int(table: dict[str, Any], key: str, default: int) -> int:
    """A TOML value that must be a real integer. A bool is NOT an integer here."""
    raw = table.get(key, default)
    if isinstance(raw, bool) or not isinstance(raw, int):
        raise RuntimeConfigError(
            f"runtime.{key} must be an integer; got {type(raw).__name__}: {raw!r}")
    return int(raw)


def _require_number(table: dict[str, Any], key: str, default: float) -> float:
    raw = table.get(key, default)
    if isinstance(raw, bool) or not isinstance(raw, (int, float)):
        raise RuntimeConfigError(
            f"runtime.{key} must be a number; got {type(raw).__name__}: {raw!r}")
    return float(raw)


def config_path(project_root: str | Path) -> Path:
    return Path(project_root).resolve() / CONFIG_RELPATH


def load_config_spec(project_root: str | Path) -> RuntimeSpec | None:
    """Read ``[runtime]`` from ``.remedy/config.toml``. None when absent."""
    path = config_path(project_root)
    if not path.is_file():
        return None
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise RuntimeConfigError(f"{CONFIG_RELPATH} is not readable TOML: {exc}") from exc

    table = data.get("runtime")
    if not isinstance(table, dict):
        return None

    cmd = table.get("cmd")
    if isinstance(cmd, str):
        raise RuntimeConfigError(
            "runtime.cmd must be an argv list, not a shell string")
    if not isinstance(cmd, list) or not cmd:
        raise RuntimeConfigError("runtime.cmd must be a non-empty argv list")
    for item in cmd:
        if not isinstance(item, str):
            raise RuntimeConfigError(
                f"runtime.cmd entries must be strings; got {type(item).__name__}: "
                f"{item!r}")

    root = Path(project_root).resolve()
    cwd_raw = table.get("cwd", ".")
    if not isinstance(cwd_raw, str):
        raise RuntimeConfigError(
            f"runtime.cwd must be a string; got {type(cwd_raw).__name__}")
    cwd = (root / cwd_raw) if not Path(cwd_raw).is_absolute() else Path(cwd_raw)

    port = _require_int(table, "port", 5173)
    timeout = _require_number(table, "ready_timeout_s", DEFAULT_TIMEOUT_S)

    health_path = table.get("health_path", DEFAULT_HEALTH_PATH)
    if not isinstance(health_path, str):
        raise RuntimeConfigError(
            f"runtime.health_path must be a string; got {type(health_path).__name__}")

    host = table.get("host", "127.0.0.1")
    if not isinstance(host, str):
        raise RuntimeConfigError(
            f"runtime.host must be a string; got {type(host).__name__}")

    env_raw = table.get("env", {})
    if not isinstance(env_raw, dict):
        raise RuntimeConfigError(
            f"runtime.env must be a table; got {type(env_raw).__name__}")
    env: dict[str, str] = {}
    for key, value in env_raw.items():
        if not isinstance(key, str) or not isinstance(value, str):
            raise RuntimeConfigError(
                f"runtime.env entries must be strings; got {key!r} = {value!r}")
        env[key] = value

    spec = RuntimeSpec(
        cmd=[str(a) for a in cmd],
        cwd=str(cwd),
        port=port,
        health_path=health_path,
        ready_timeout_s=timeout,
        host=host,
        env=env,
        source="config",
    )
    return validate_spec(spec, root)


# ---------------------------------------------------------------------------
# Detection — checked-in files only, never an import of project code
# ---------------------------------------------------------------------------

def _read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def _package_manager(pkg_dir: Path) -> list[str]:
    """The package manager already used by the project, from its lockfile."""
    if (pkg_dir / "pnpm-lock.yaml").is_file():
        return ["pnpm", "run", "dev"]
    if (pkg_dir / "yarn.lock").is_file():
        return ["yarn", "dev"]
    return ["npm", "run", "dev", "--"]


def _node_candidates(root: Path) -> list[Path]:
    """package.json at the root, or one level down (apps/*, packages/*)."""
    found: list[Path] = []
    if (root / "package.json").is_file():
        found.append(root / "package.json")
    for parent in ("apps", "packages", "frontend", "web", "ui", "client"):
        base = root / parent
        if not base.is_dir():
            continue
        if (base / "package.json").is_file():        # e.g. <root>/web/package.json
            found.append(base / "package.json")
            continue
        for child in sorted(p for p in base.iterdir() if p.is_dir()):
            if (child / "package.json").is_file():   # e.g. <root>/apps/ui/package.json
                found.append(child / "package.json")
    return found


def _detect_node(root: Path) -> list[DetectedRuntime]:
    out: list[DetectedRuntime] = []
    for pkg_file in _node_candidates(root):
        pkg = _read_json(pkg_file)
        scripts = pkg.get("scripts") or {}
        deps = {**(pkg.get("dependencies") or {}), **(pkg.get("devDependencies") or {})}
        dev_script = str(scripts.get("dev") or "")
        pkg_dir = pkg_file.parent

        is_next = "next" in deps or "next dev" in dev_script
        is_vite = ("vite" in deps or "vite" in dev_script) and not is_next

        if is_next:
            out.append(DetectedRuntime(
                kind="next",
                spec=RuntimeSpec(
                    cmd=[*_package_manager(pkg_dir), "--port", "{port}"],
                    cwd=str(pkg_dir), port=3000,
                    health_path=DEFAULT_HEALTH_PATH,
                    ready_timeout_s=DEFAULT_TIMEOUT_S,
                    source="detected:next",
                ),
                signals=[f"{pkg_file.name}: next dependency/dev script"],
            ))
        elif is_vite:
            out.append(DetectedRuntime(
                kind="vite",
                spec=RuntimeSpec(
                    cmd=[*_package_manager(pkg_dir), "--port", "{port}",
                         "--host", "127.0.0.1", "--strictPort"],
                    cwd=str(pkg_dir), port=5173,
                    health_path=DEFAULT_HEALTH_PATH,
                    ready_timeout_s=DEFAULT_TIMEOUT_S,
                    source="detected:vite",
                ),
                signals=[f"{pkg_file.name}: vite dependency/dev script"],
            ))
    return out


_UVICORN_HINTS = ("uvicorn", "fastapi")


def _detect_python(root: Path) -> list[DetectedRuntime]:
    text = ""
    signals: list[str] = []
    py = root / "pyproject.toml"
    if py.is_file():
        try:
            text += py.read_text(encoding="utf-8", errors="replace").lower()
            signals.append("pyproject.toml")
        except OSError:
            pass
    for req in ("requirements.txt", "requirements-dev.txt"):
        rp = root / req
        if rp.is_file():
            try:
                text += rp.read_text(encoding="utf-8", errors="replace").lower()
                signals.append(req)
            except OSError:
                pass
    if not any(h in text for h in _UVICORN_HINTS):
        return []

    # Conventional module locations only — the module is never imported.
    module = ""
    for candidate, dotted in (
        ("app/main.py", "app.main:app"),
        ("main.py", "main:app"),
        ("src/main.py", "src.main:app"),
        ("api/main.py", "api.main:app"),
    ):
        if (root / candidate).is_file():
            module = dotted
            signals.append(candidate)
            break
    if not module:
        return []

    return [DetectedRuntime(
        kind="uvicorn",
        spec=RuntimeSpec(
            cmd=["python3", "-m", "uvicorn", module,
                 "--host", "127.0.0.1", "--port", "{port}"],
            cwd=str(root), port=8000,
            health_path=DEFAULT_HEALTH_PATH,
            ready_timeout_s=DEFAULT_TIMEOUT_S,
            source="detected:uvicorn",
        ),
        signals=signals,
    )]


def detect_runtimes(project_root: str | Path) -> list[DetectedRuntime]:
    root = Path(project_root).resolve()
    return _detect_node(root) + _detect_python(root)


def resolve_spec(project_root: str | Path) -> RuntimeSpec:
    """Explicit config, else exactly one detected runtime, else block honestly."""
    root = Path(project_root).resolve()
    if not root.is_dir():
        raise RuntimeConfigError(f"project root {root} is not a directory")

    spec = load_config_spec(root)
    if spec is not None:
        return spec                    # explicit config always wins

    found = detect_runtimes(root)
    if not found:
        raise RuntimeConfigError(
            "no runtime detected and no [runtime] section in "
            f"{CONFIG_RELPATH}: configuration required"
        )
    if len(found) > 1:
        kinds = ", ".join(
            f"{d.kind} ({Path(d.spec.cwd).name})" for d in found)
        raise RuntimeConfigError(
            f"ambiguous runtime: {kinds}. Configuration required — add a [runtime] "
            f"section to {CONFIG_RELPATH}"
        )
    return validate_spec(found[0].spec, root)
