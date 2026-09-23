"""`remedy doctor toolchain`: each pinned tool's installed, pinned and newest version (T2_F279 T004).

T002 pins the toolchain CI installs in `constraints.txt`. Pinning freezes versions; this report
is how an operator sees them drift: the version this interpreter has installed, the version
`constraints.txt` pins, and the newest version the package index knows. The newest version
needs the network, so it reads "unknown" whenever it cannot be fetched and never a made-up
number such as "0" — an honest gap, not a false reading (DECISION F279 D6).

The tools reported are the ones `pyproject.toml` declares as Remedy's own dependencies and in
its `dev` extra, which is the set T004's refresh order raises.
"""
from __future__ import annotations

import json
import re
import sys
from collections.abc import Callable
from dataclasses import dataclass
from importlib import metadata
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:  # pragma: no cover - the 3.10 floor reads pyproject.toml through the backport
    import tomli as tomllib

REPO_ROOT = Path(__file__).resolve().parents[2]
CONSTRAINTS_PATH = "constraints.txt"
PYPROJECT_PATH = "pyproject.toml"
UNKNOWN = "unknown"
NOT_INSTALLED = "not installed"
NOT_PINNED = "not pinned"
PYPI_JSON_URL = "https://pypi.org/pypi/{name}/json"
FETCH_TIMEOUT_SECONDS = 5.0

_PIN = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*)==([^\s;\\]+)", re.M)
_REQUIREMENT_NAME = re.compile(r"^\s*([A-Za-z0-9][A-Za-z0-9._-]*)")


def canonical_name(name: str) -> str:
    """PEP 503 normalization: case and runs of `-`, `_` and `.` never make two names differ."""
    return re.sub(r"[-_.]+", "-", name).lower()


@dataclass(frozen=True)
class ToolRow:
    name: str
    installed: str
    pinned: str
    newest: str

    def as_dict(self) -> dict[str, str]:
        return {"name": self.name, "installed": self.installed, "pinned": self.pinned,
                "newest": self.newest}


def pinned_versions(constraints_text: str) -> dict[str, str]:
    return {canonical_name(name): version for name, version in _PIN.findall(constraints_text)}


def pinned_tools(pyproject_text: str) -> list[str]:
    """Remedy's own dependencies and its `dev` extra, canonical names, in declaration order."""
    project = tomllib.loads(pyproject_text)["project"]
    declared = [*project["dependencies"], *project["optional-dependencies"]["dev"]]
    names: list[str] = []
    for requirement in declared:
        match = _REQUIREMENT_NAME.match(requirement)
        if match and canonical_name(match.group(1)) not in names:
            names.append(canonical_name(match.group(1)))
    return names


def installed_version(name: str) -> str:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return NOT_INSTALLED


def pypi_newest(name: str, timeout: float = FETCH_TIMEOUT_SECONDS) -> str:
    """The newest version the package index names, or "unknown" when it cannot be fetched."""
    import urllib.error
    import urllib.request

    try:
        with urllib.request.urlopen(PYPI_JSON_URL.format(name=name), timeout=timeout) as response:  # noqa: S310
            version = json.loads(response.read().decode("utf-8"))["info"]["version"]
    except (OSError, urllib.error.URLError, ValueError, KeyError, TypeError):
        return UNKNOWN
    return version if isinstance(version, str) and version else UNKNOWN


def offline(_name: str) -> str:
    return UNKNOWN


def toolchain_rows(
    fetch_newest: Callable[[str], str] = pypi_newest,
    installed: Callable[[str], str] = installed_version,
    repo_root: Path = REPO_ROOT,
) -> list[ToolRow]:
    pins = pinned_versions((repo_root / CONSTRAINTS_PATH).read_text(encoding="utf-8"))
    rows = []
    for name in pinned_tools((repo_root / PYPROJECT_PATH).read_text(encoding="utf-8")):
        newest = fetch_newest(name) or UNKNOWN
        rows.append(ToolRow(name, installed(name), pins.get(name, NOT_PINNED), newest))
    return rows
