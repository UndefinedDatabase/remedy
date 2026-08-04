"""F075 T001 — the gauntlet CLI: thin, honest, and non-zero when it should be.

Three things are worth testing about a thin CLI: that the flags reach the
evaluator, that a failed campaign exits non-zero (a gate that always exits 0 is
not a gate), and that the round's absence of live execution is SAID rather than
faked.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from packages.orchestration.gauntlet_matrix import (
    MATRIX_JSON_FILENAME,
    MATRIX_MARKDOWN_FILENAME,
)
from tests.orchestration.test_gauntlet_evidence import (
    FLAWLESS_BODY,
    RECORDED_DIR,
    RELEASED_GATE,
    write_run,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "self_run_gauntlet.py"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
import self_run_gauntlet as cli  # noqa: E402


def flawless_evidence(root: Path, count: int = 2) -> Path:
    evidence = root / "recorded"
    for index in range(1, count + 1):
        write_run(evidence, f"run-{index:02d}",
                  dict(FLAWLESS_BODY, order_id=f"g{index:02d}"), RELEASED_GATE)
    return evidence


def test_a_flawless_campaign_exits_zero(tmp_path: Path, capsys) -> None:
    code = cli.main(["--dry-run", str(flawless_evidence(tmp_path))])
    assert code == cli.EXIT_PASS
    assert "2/2 runs flawless · **PASS**" in capsys.readouterr().out


def test_the_recorded_fixture_campaign_exits_non_zero(capsys) -> None:
    code = cli.main(["--dry-run", str(RECORDED_DIR)])
    assert code == cli.EXIT_NOT_A_PASS
    assert "5/9 runs flawless · **NOT A PASS**" in capsys.readouterr().out


def test_an_empty_evidence_dir_is_not_a_pass(tmp_path: Path) -> None:
    (tmp_path / "empty").mkdir()
    assert cli.main(["--dry-run", str(tmp_path / "empty")]) == cli.EXIT_NOT_A_PASS


def test_only_selects_one_run(tmp_path: Path, capsys) -> None:
    evidence = flawless_evidence(tmp_path, count=3)
    assert cli.main(["--dry-run", str(evidence), "--only", "2"]) == cli.EXIT_PASS
    out = capsys.readouterr().out
    assert "1/1 runs flawless" in out
    assert "run-02" in out and "run-03" not in out


def test_only_outside_the_range_is_a_usage_error(tmp_path: Path, capsys) -> None:
    evidence = flawless_evidence(tmp_path)
    assert cli.main(["--dry-run", str(evidence), "--only", "9"]) == cli.EXIT_USAGE
    assert "outside 1..2" in capsys.readouterr().err


def test_a_missing_evidence_dir_is_a_usage_error(tmp_path: Path, capsys) -> None:
    assert cli.main(["--dry-run", str(tmp_path / "nowhere")]) == cli.EXIT_USAGE
    assert "no such evidence directory" in capsys.readouterr().err


@pytest.mark.parametrize("fmt,needle", [
    ("md", "# Gauntlet matrix"),
    ("json", '"matrix_version": 1'),
])
def test_format_selects_what_reaches_stdout(tmp_path: Path, capsys,
                                            fmt: str, needle: str) -> None:
    cli.main(["--dry-run", str(flawless_evidence(tmp_path)), "--format", fmt])
    out = capsys.readouterr().out
    assert needle in out


def test_format_both_prints_both(tmp_path: Path, capsys) -> None:
    cli.main(["--dry-run", str(flawless_evidence(tmp_path)), "--format", "both"])
    out = capsys.readouterr().out
    assert "# Gauntlet matrix" in out and '"matrix_version": 1' in out


def test_out_writes_both_reports(tmp_path: Path, capsys) -> None:
    out_dir = tmp_path / "report"
    cli.main(["--dry-run", str(flawless_evidence(tmp_path)), "--out", str(out_dir)])
    capsys.readouterr()
    body = json.loads((out_dir / MATRIX_JSON_FILENAME).read_text(encoding="utf-8"))
    assert body["runs_recorded"] == 2
    assert (out_dir / MATRIX_MARKDOWN_FILENAME).read_text(
        encoding="utf-8").startswith("# Gauntlet matrix")


def test_label_reaches_both_renderers(tmp_path: Path, capsys) -> None:
    cli.main(["--dry-run", str(flawless_evidence(tmp_path)),
              "--format", "both", "--label", "set-v1"])
    out = capsys.readouterr().out
    assert "# Gauntlet matrix — set-v1" in out
    assert '"evidence_label": "set-v1"' in out


def test_a_dry_run_writes_nothing_into_the_evidence_it_reads(tmp_path: Path,
                                                             capsys) -> None:
    evidence = flawless_evidence(tmp_path)
    before = {p.relative_to(evidence): p.read_bytes()
              for p in sorted(evidence.rglob("*")) if p.is_file()}
    cli.main(["--dry-run", str(evidence)])
    capsys.readouterr()
    after = {p.relative_to(evidence): p.read_bytes()
             for p in sorted(evidence.rglob("*")) if p.is_file()}
    assert after == before


def test_without_a_mode_the_cli_names_both_modes() -> None:
    """A run with no mode is a usage error, said out loud."""
    proc = subprocess.run([sys.executable, str(SCRIPT)],
                          capture_output=True, text=True, cwd=str(REPO_ROOT))
    assert proc.returncode == cli.EXIT_USAGE
    assert "--dry-run <evidence-dir>" in proc.stderr
    assert "--live <campaign-root>" in proc.stderr


def test_both_modes_at_once_is_a_usage_error(tmp_path: Path) -> None:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--dry-run", str(RECORDED_DIR),
         "--live", str(tmp_path / "campaign")],
        capture_output=True, text=True, cwd=str(REPO_ROOT))
    assert proc.returncode == cli.EXIT_USAGE
    assert "not both" in proc.stderr
    assert not (tmp_path / "campaign").exists()


# ---------------------------------------------------------------------------
# --live, and the campaign it refuses to start
# ---------------------------------------------------------------------------

def test_the_frozen_set_passes_preflight_now_that_every_class_is_driveable() -> None:
    """Since the R3 boundary landed, nothing in the set is blocked.

    Checked through the preflight rather than by starting a campaign: no test
    in this file may take the production path, because that spends real tokens
    on ten real missions.
    """
    from packages.orchestration.gauntlet_orders import load_order_set

    assert cli.preflight_injections(load_order_set()) == []


def test_the_preflight_still_refuses_an_order_declaring_an_unknown_class() -> None:
    """The guard that stopped R2's campaign is intact for any future class."""
    from packages.orchestration.gauntlet_orders import GauntletOrder

    order = GauntletOrder(
        id="gxx", kind="pure_code_change", title="t", rationale="r",
        risk_probed="risk", goal="g", milestones=({"id": "M001"},),
        budget={"max_iterations": 1, "max_tokens": 1, "max_wall_seconds": 1},
        injections=("cosmic_ray",), file_name="gxx.json", sha256="d")
    blocked = cli.preflight_injections((order,))
    assert len(blocked) == 1
    assert "unknown injection class" in blocked[0]


def test_a_live_campaign_stops_when_an_order_is_blocked(tmp_path: Path,
                                                        monkeypatch, capsys) -> None:
    """Refused before the first provider call, so a set nobody can judge costs
    nothing to discover."""
    from packages.orchestration import gauntlet_orders as orders_mod
    from packages.orchestration.gauntlet_orders import GauntletOrder

    order = GauntletOrder(
        id="gxx-unknown", kind="pure_code_change", title="t", rationale="r",
        risk_probed="risk", goal="g", milestones=({"id": "M001"},),
        budget={"max_iterations": 1, "max_tokens": 1, "max_wall_seconds": 1},
        injections=("cosmic_ray",), file_name="gxx.json", sha256="d")
    monkeypatch.setattr(orders_mod, "load_order_set", lambda *a, **k: (order,))

    assert cli.main(["--live", str(tmp_path / "campaign")]) == cli.EXIT_USAGE
    err = capsys.readouterr().err
    assert "refusing to start a live campaign" in err
    assert "gxx-unknown" in err
    assert not (tmp_path / "campaign").exists()


def test_a_live_campaign_with_runnable_orders_produces_a_judged_matrix(
        tmp_path: Path, monkeypatch, capsys) -> None:
    """The only orders that can run today do run, and the SAME evaluator judges."""
    from packages.orchestration import gauntlet_orders as orders_mod
    from packages.orchestration import gauntlet_runner as runner_mod
    from tests.orchestration.test_gauntlet_runner import Recorder, an_order

    runnable = (an_order("g01-pure-code-change"), an_order("g02-test-add"))
    monkeypatch.setattr(orders_mod, "load_order_set", lambda *a, **k: runnable)
    real_root = tmp_path / "real"
    real_root.mkdir()
    deps = Recorder().deps()
    original = runner_mod.run_campaign
    monkeypatch.setattr(
        runner_mod, "run_campaign",
        lambda o, root, **kw: original(o, root, deps=deps,
                                       real_data_root=real_root,
                                       on_order=kw.get("on_order")))

    code = cli.main(["--live", str(tmp_path / "campaign"), "--format", "json"])
    body = json.loads(capsys.readouterr().out)
    assert body["runs_recorded"] == 2
    assert code in (cli.EXIT_PASS, cli.EXIT_NOT_A_PASS)
    assert (tmp_path / "campaign" / "run-01-g01-pure-code-change").is_dir()


def test_a_broken_frozen_set_stops_the_campaign(tmp_path: Path, monkeypatch,
                                                capsys) -> None:
    from packages.orchestration import gauntlet_orders as orders_mod

    def boom(*a, **k):
        raise orders_mod.OrderSetError("sha256 does not match the manifest")

    monkeypatch.setattr(orders_mod, "load_order_set", boom)
    assert cli.main(["--live", str(tmp_path / "campaign")]) == cli.EXIT_USAGE
    assert "the frozen order set is not intact" in capsys.readouterr().err


def test_the_script_runs_as_a_subprocess_from_any_cwd(tmp_path: Path) -> None:
    """The repo-root sys.path insert is load-bearing — a fresh interpreter proves it."""
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--dry-run", str(RECORDED_DIR), "--format", "json"],
        capture_output=True, text=True, cwd=str(tmp_path))
    assert proc.returncode == cli.EXIT_NOT_A_PASS
    assert json.loads(proc.stdout)["runs_flawless"] == 5
