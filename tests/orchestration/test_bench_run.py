"""F082 — the bench run end to end, driven with doubles instead of a provider.

No test here calls a model, shells out to ``git`` or writes a project registry.
The whole product path from the FROZEN order set to the history file is
exercised, and every seam that would leave this machine is substituted at the
call site through :class:`RunnerDeps`.

NINE seams are doubled, counted: ``make_project``, ``create_mission``,
``plan_mission``, ``run_mission``, ``load_mission``, ``execute_fn``,
``materialise``, ``plan_call_fn`` and ``move_call_fn``. The F082 inventory's Q6
named three of them; the other six are the ones a run discovers it also needs —
``make_project`` writes the project registry by default, ``materialise`` shells
out to ``git``, and the four mission verbs are the product path itself.

The REAL frozen set under ``scripts/bench_orders`` is used, not a fixture copy,
so these properties exercise the freeze that actually ships. Every path the run
touches is under ``tmp_path``, including the data root: nothing here may reach
the operator's real one.

The doubles below follow the SHAPE of ``tests/orchestration/test_gauntlet_runner``'s
``Recorder``, authored locally rather than imported — a test module is not an
API, and sharing its privates would make either file unable to move.
"""
from __future__ import annotations

import json
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pytest

from packages.orchestration import bench_dry_run
from packages.orchestration.bench_history import load_bench_history
from packages.orchestration.bench_orders import (
    BenchOrderSetError,
    default_bench_orders_dir,
    load_bench_order_set,
)
from packages.orchestration.bench_run import run_bench_campaign
from packages.orchestration.gauntlet_runner import RunnerDeps

SERIES = "bench-run-test"


@dataclass
class FakeMission:
    id: str = "m-1"
    job_links: tuple = ()


@dataclass
class FakeExecution:
    """What the loop's execute seam hands back."""

    terminal_status: str = "all_green"
    job_status: str = "completed"
    stop_reason: str = ""
    resolved_cycles: dict = field(default_factory=dict)


@dataclass
class FakeResult:
    terminal: str = "achieved"
    entries: list = field(default_factory=list)


@dataclass
class NoNetworkRun:
    """Doubles for all NINE product seams a bench run drives.

    ``_run_mission`` writes through the product's OWN path resolution, so "the
    run stayed inside its isolated root" is proven by where bytes land rather
    than by a recorded call.
    """

    roots_written: list[Path] = field(default_factory=list)

    def deps(self) -> RunnerDeps:
        return RunnerDeps(
            make_project=self._make_project,
            create_mission=self._create_mission,
            plan_mission=self._plan_mission,
            run_mission=self._run_mission,
            load_mission=lambda project_id, mission_id: FakeMission(id=mission_id),
            execute_fn=self._execute_fn,
            materialise=self._materialise,
            plan_call_fn=lambda: (lambda prompt, attempt: "{}"),
            move_call_fn=lambda: (lambda prompt, attempt: "{}"),
        )

    def _materialise(self, run_dir: Path) -> Path:
        """A workspace without ``git``: the real one is proven in its own test."""
        workspace = run_dir / "workspace"
        workspace.mkdir(parents=True, exist_ok=True)
        return workspace

    def _execute_fn(self, max_cycles: int, repo_root: Path | None = None):
        def _execute(job: Any) -> FakeExecution:
            return FakeExecution(resolved_cycles={"max_cycles": max_cycles,
                                                  "source": "experiment",
                                                  "over_cap": False})

        return _execute

    def _make_project(self, name: str, slug: str, repo_path: Path | None = None) -> str:
        return "p-1"

    def _create_mission(self, project_id: str, goal: str) -> FakeMission:
        return FakeMission()

    def _plan_mission(self, project_id: str, mission_id: str, call_fn, **kwargs) -> None:
        return None

    def _run_mission(self, mission_id: str, limits, **kwargs) -> FakeResult:
        from packages.orchestration.data_paths import resolve_data_root

        root = resolve_data_root()
        self.roots_written.append(root)
        (root / "missions").mkdir(parents=True, exist_ok=True)
        (root / "missions" / "ledger.jsonl").write_text("{}\n", encoding="utf-8")
        return FakeResult()


@pytest.fixture()
def data_root(tmp_path: Path) -> Path:
    """A stand-in for the operator's data root, with something in it to lose."""
    root = tmp_path / "real-data"
    (root / "projects").mkdir(parents=True)
    (root / "projects" / "keep.json").write_text('{"id": "keep"}', encoding="utf-8")
    return root


def _run(tmp_path: Path, data_root: Path, *, campaign: str = "campaign",
         orders_dir: Path | None = None):
    return run_bench_campaign(
        campaign_root=tmp_path / campaign,
        data_root=data_root,
        history_path=tmp_path / "history" / "bench_history.jsonl",
        series=SERIES,
        orders_dir=orders_dir,
        deps=NoNetworkRun().deps(),
    )


# ---------------------------------------------------------------------------
# 1. ONE ROW PER FROZEN ORDER, IN THE ORDER SET'S OWN ORDER
# ---------------------------------------------------------------------------

def test_the_run_produces_one_row_per_frozen_order_in_set_order(
        tmp_path: Path, data_root: Path) -> None:
    """A SEQUENCE comparison, never a set: a history that silently re-sorted
    itself would not be comparable across runs."""
    expected = [order.id for order in load_bench_order_set()]
    result = _run(tmp_path, data_root)
    assert [row.order_id for row in result.rows] == expected, (
        f"Bench rows {[r.order_id for r in result.rows]} do not match the frozen "
        f"order ids {expected} as a sequence")
    assert [outcome.order_id for outcome in result.outcomes] == expected


# ---------------------------------------------------------------------------
# 2. THE HISTORY IS WRITTEN AND SURVIVES A SECOND RUN
# ---------------------------------------------------------------------------

def test_the_history_survives_a_second_run(tmp_path: Path, data_root: Path) -> None:
    """Append-only: the second run ADDS rows and never rewrites the first's."""
    first = _run(tmp_path, data_root, campaign="campaign-1")
    second = _run(tmp_path, data_root, campaign="campaign-2")
    assert second.run_seq == first.run_seq + 1, (
        f"Second run_seq {second.run_seq} is not one past the first "
        f"{first.run_seq} — the history was rewritten, not appended")

    entries = load_bench_history(tmp_path / "history" / "bench_history.jsonl")
    seqs = sorted({entry.run_seq for entry in entries})
    assert seqs == [first.run_seq, second.run_seq], (
        f"History holds runs {seqs}, expected both {first.run_seq} and "
        f"{second.run_seq}")
    assert len(entries) == len(first.rows) + len(second.rows)


# ---------------------------------------------------------------------------
# 3. NO ROW IS AN evidence_missing ROW
# ---------------------------------------------------------------------------

def test_no_row_is_an_evidence_missing_row(tmp_path: Path, data_root: Path) -> None:
    """Without this, properties 1 and 2 both pass over three MISSING rows — a
    dry run against an empty directory looks identical from the outside."""
    result = _run(tmp_path, data_root)
    missing = [row.order_id for row in result.rows
               if bench_dry_run.EVIDENCE_MISSING_CLASS in row.postmortem_classes]
    assert not missing, (
        f"Orders {missing} produced {bench_dry_run.EVIDENCE_MISSING_CLASS} rows — "
        "the campaign left no evidence the join could read, so this was a dry "
        "run over an empty directory, not an end-to-end run")


# ---------------------------------------------------------------------------
# 4. NOTHING IS WRITTEN OUTSIDE tmp_path
# ---------------------------------------------------------------------------

def test_the_run_writes_nothing_outside_tmp_path(tmp_path: Path, data_root: Path) -> None:
    """``resolve_data_root()`` is deliberately never called here: reading the
    operator's real root is the thing this property refuses to do."""
    runner = NoNetworkRun()
    campaign_root = tmp_path / "campaign"
    history_path = tmp_path / "history" / "bench_history.jsonl"
    run_bench_campaign(campaign_root=campaign_root, data_root=data_root,
                       history_path=history_path, series=SERIES,
                       deps=runner.deps())

    assert campaign_root.is_relative_to(tmp_path)
    assert history_path.is_relative_to(tmp_path)
    assert history_path.is_file()
    assert len(runner.roots_written) == len(load_bench_order_set()), (
        "The mission double never ran, so the check below would pass vacuously")
    stray = [root for root in runner.roots_written if not root.is_relative_to(tmp_path)]
    assert not stray, f"The run resolved a data root outside tmp_path: {stray}"


# ---------------------------------------------------------------------------
# 5. THE SIGNATURE REFUSES A MISSING ROOT
# ---------------------------------------------------------------------------

def test_a_missing_data_root_is_a_type_error(tmp_path: Path) -> None:
    """No default may reach the operator's real data root (F082 inventory Q6)."""
    with pytest.raises(TypeError):
        run_bench_campaign(campaign_root=tmp_path / "campaign",
                           history_path=tmp_path / "h.jsonl", series=SERIES)


def test_a_missing_history_path_is_a_type_error(tmp_path: Path, data_root: Path) -> None:
    """The history must not resolve through ``data_paths.projects_dir`` here."""
    with pytest.raises(TypeError):
        run_bench_campaign(campaign_root=tmp_path / "campaign",
                           data_root=data_root, series=SERIES)


# ---------------------------------------------------------------------------
# 6. THE FREEZE RUNS BEFORE THE CAMPAIGN
# ---------------------------------------------------------------------------

def test_a_tampered_order_set_refuses_before_anything_runs(
        tmp_path: Path, data_root: Path) -> None:
    """The refusal has to come BEFORE the campaign, or a tampered set costs a
    whole run before anyone finds out."""
    orders_dir = tmp_path / "bench_orders"
    shutil.copytree(default_bench_orders_dir(), orders_dir)
    tampered = orders_dir / "b01-cli-report-width.json"
    body = json.loads(tampered.read_text(encoding="utf-8"))
    body["goal"] = body["goal"] + " Also rename the module."
    tampered.write_text(json.dumps(body, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8")

    campaign_root = tmp_path / "campaign"
    with pytest.raises(BenchOrderSetError):
        _run(tmp_path, data_root, orders_dir=orders_dir)

    run_dirs = sorted(p.name for p in campaign_root.glob("*")) if campaign_root.is_dir() else []
    assert run_dirs == [], (
        f"The campaign root holds {run_dirs} after a refused set — the freeze "
        "ran AFTER the campaign, not before it")
    assert not (tmp_path / "history" / "bench_history.jsonl").exists()
