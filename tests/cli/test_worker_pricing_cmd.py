"""`remedy worker pricing-update` through the real command line (F158 T003, DECISION F158 D6):
the difference is shown first, nothing is written without `--yes`, and a malformed catalog or an
unraised pricing version is refused."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from packages.orchestration.model_aliases import builtin_model_ids
from packages.orchestration.price_catalog import PRICE_CATALOG_DIR

REPO = Path(__file__).resolve().parents[2]
_CLI = [sys.executable, "-m", "apps.cli.grouped", "worker", "pricing-update"]

IMPORTED = f"""[catalog]
adapter = "claude-cli"
pricing_version = 2

[models."{builtin_model_ids()[0]}"]
input_per_million = 3.0
output_per_million = 15.0
cache_read_per_million = 0.3
cache_write_per_million = 3.75
currency = "usd"
valid_from = 2026-10-01
source = "a maintained catalog the operator imported"
"""


def _run(*args: str) -> subprocess.CompletedProcess:
    env = {**os.environ, "PYTHONPATH": str(REPO)}
    return subprocess.run([*_CLI, *args], capture_output=True, text=True, timeout=60, cwd=REPO, env=env)


@pytest.fixture
def catalogs(tmp_path: Path) -> Path:
    folder = tmp_path / "catalogs"
    folder.mkdir()
    shutil.copyfile(PRICE_CATALOG_DIR / "claude-cli.toml", folder / "claude-cli.toml")
    return folder


@pytest.fixture
def imported(tmp_path: Path) -> Path:
    path = tmp_path / "imported.toml"
    path.write_text(IMPORTED, encoding="utf-8")
    return path


@pytest.mark.subprocess
class TestTheShownDifference:
    def test_without_yes_the_difference_is_shown_and_nothing_is_written(self, catalogs, imported) -> None:
        before = (catalogs / "claude-cli.toml").read_bytes()
        r = _run(str(imported), "--catalog-dir", str(catalogs))
        assert r.returncode == 0, r.stderr
        assert "Price catalog of claude-cli: pricing version 1 to 2" in r.stdout
        assert "--- claude-cli.toml (current)" in r.stdout
        assert "+++ claude-cli.toml (imported)" in r.stdout
        assert "+pricing_version = 2" in r.stdout
        assert "-pricing_version = 1" in r.stdout
        assert r.stdout.rstrip().endswith(
            "Nothing was written. Run the same command again with --yes to write this catalog.")
        assert (catalogs / "claude-cli.toml").read_bytes() == before

    def test_with_yes_the_catalog_is_written_after_its_difference(self, catalogs, imported) -> None:
        r = _run(str(imported), "--catalog-dir", str(catalogs), "--yes")
        assert r.returncode == 0, r.stderr
        assert r.stdout.index("+pricing_version = 2") < r.stdout.index("Wrote ")
        assert (catalogs / "claude-cli.toml").read_text(encoding="utf-8") == IMPORTED

    def test_json_answers_the_difference_and_whether_it_was_written(self, catalogs, imported) -> None:
        body = json.loads(_run(str(imported), "--catalog-dir", str(catalogs), "--json").stdout)
        assert body["ok"] is True
        assert (body["adapter"], body["current_version"], body["new_version"]) == ("claude-cli", 1, 2)
        assert (body["changed"], body["written"]) == (True, False)
        assert "+pricing_version = 2" in body["diff"]
        assert body["warnings"] == []

    def test_an_unchanged_catalog_writes_nothing(self, catalogs) -> None:
        r = _run(str(catalogs / "claude-cli.toml"), "--catalog-dir", str(catalogs), "--yes")
        assert r.returncode == 0, r.stderr
        assert "No change: the imported catalog equals the current one, so nothing is written." in r.stdout

    def test_an_unknown_model_is_warned_about_but_imported(self, catalogs, tmp_path) -> None:
        path = tmp_path / "odd.toml"
        path.write_text(IMPORTED.replace(builtin_model_ids()[0], "a-model-remedy-does-not-ship"),
                        encoding="utf-8")
        r = _run(str(path), "--catalog-dir", str(catalogs), "--yes")
        assert r.returncode == 0, r.stderr
        assert "warning: claude-cli price catalog: model 'a-model-remedy-does-not-ship'" in r.stdout
        assert "Wrote " in r.stdout


@pytest.mark.subprocess
class TestTheRefusals:
    def test_a_change_without_a_raised_version_is_refused_and_nothing_is_written(
            self, catalogs, tmp_path) -> None:
        path = tmp_path / "same-version.toml"
        path.write_text(IMPORTED.replace("pricing_version = 2", "pricing_version = 1"), encoding="utf-8")
        before = (catalogs / "claude-cli.toml").read_bytes()
        r = _run(str(path), "--catalog-dir", str(catalogs), "--yes", "--json")
        assert r.returncode == 1
        body = json.loads(r.stdout)
        assert body["error"] == "invalid_price_catalog"
        assert "pricing_version 1 is not above the current 1" in body["message"]
        assert (catalogs / "claude-cli.toml").read_bytes() == before

    def test_a_malformed_catalog_is_refused(self, catalogs, tmp_path) -> None:
        path = tmp_path / "bad.toml"
        path.write_text(IMPORTED.replace('source = "a maintained catalog the operator imported"\n', ""),
                        encoding="utf-8")
        r = _run(str(path), "--catalog-dir", str(catalogs), "--yes")
        assert r.returncode == 1
        assert "must hold exactly" in r.stdout + r.stderr

    def test_an_unreadable_file_is_a_usage_error(self, catalogs, tmp_path) -> None:
        r = _run(str(tmp_path / "missing.toml"), "--catalog-dir", str(catalogs))
        assert r.returncode == 2
