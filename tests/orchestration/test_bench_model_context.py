"""F082 T003b — which model served which role, recorded in the run's own evidence.

A NEW file rather than an addition to ``tests/orchestration/test_gauntlet_runner.py``:
that file is one of the gauntlet's seven, which DECISION F082 D7's second condition
freezes UNMODIFIED, so the bench's own pins live in the bench's own file. The
``test_x.py`` <-> ``x.py`` naming convention is deliberately not followed here for
that reason, and the deviation is declared in the round's handback.

What is pinned: an OBSERVED binding reaches ``run.json``, an UNOBSERVED one is
recorded as an absence rather than as a default model name (DECISION F082 D7's
third condition), and the key set of the emitted body is the base set plus
``models`` and nothing else (D7's first condition, additivity).
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pytest

from packages.orchestration.bench_history import (
    BENCH_HISTORY_VERSION,
    append_bench_run,
    load_bench_history,
)
from packages.orchestration.capability_bench import build_bench_record
from packages.orchestration.gauntlet_evidence import RUN_FILENAME
from packages.orchestration.gauntlet_orders import GauntletOrder
from packages.orchestration.gauntlet_runner import (
    TOKENS_UNMEASURED,
    RunnerDeps,
    _evidence_body,
    run_order,
)
from packages.orchestration.orchestrator_loop import TERMINAL_ACHIEVED

#: The base body keys as they exist at BASE b0ea45c9, named one by one so a
#: rename of any of them fails this file rather than passing silently.
BASE_BODY_KEYS = {
    "gauntlet_run_version",
    "order_id",
    "kind",
    "terminal_status",
    "wall_seconds",
    "operator_interventions",
    "data_root_hash_before",
    "postmortems",
    "open_decisions",
    "era_defects",
    "injections",
    "evidence_links",
    "cycles_budget",
    "cycles_resolved",
    "template_digest",
    # Exactly one of ``tokens`` / ``tokens_source`` is added unconditionally;
    # a run with no measured usage carries the source, never a zero (R-0178).
    "tokens_source",
}

#: The three roles a gauntlet run can report on. ``builder`` is never observable
#: from this seam — ``orchestrator_loop.py::execute_dispatched_job`` constructs
#: ``OllamaBuilder()`` itself — so it is recorded as an absence on purpose.
ROLES = ("planner", "orchestrator", "builder")


def an_order(order_id: str = "g01-pure-code-change") -> GauntletOrder:
    return GauntletOrder(
        id=order_id, kind="pure_code_change", title="t", rationale="r",
        risk_probed="risk", goal="do the thing",
        milestones=({"id": "M001", "title": "m", "dod": ["x"]},),
        budget={"max_iterations": 4, "max_tokens": 250_000,
                "max_wall_seconds": 2_400, "max_cycles": 4},
        injections=(), file_name=f"{order_id}.json", sha256="d")


@dataclass
class FakeMission:
    id: str = "m-1"
    job_links: tuple = ()


@dataclass
class FakeResult:
    terminal: str = TERMINAL_ACHIEVED
    entries: list = field(default_factory=list)


def labelled_call_fn(model: str):
    """A call_fn that carries the model its provider instance resolved."""

    def _call(prompt: str, attempt: int) -> str:
        return "{}"

    _call.resolved_model = model
    return _call


def unlabelled_call_fn():
    """A call_fn built by something that never labelled it — an absence."""

    def _call(prompt: str, attempt: int) -> str:
        return "{}"

    return _call


@dataclass
class ModelRecorder:
    """Doubles for the product verbs, with the two call_fn seams under test.

    ``plan_fn`` and ``move_fn`` are whatever the factories would have returned:
    a labelled callable, an unlabelled one, or ``None`` — the last being what
    ``intake.py::make_structured_call_fn`` really returns when Ollama is
    unreachable.
    """

    plan_fn: Any = None
    move_fn: Any = None

    def deps(self) -> RunnerDeps:
        return RunnerDeps(
            make_project=lambda name, slug, repo_path=None: "p-1",
            create_mission=lambda project_id, goal: FakeMission(),
            plan_mission=lambda *a, **k: None,
            run_mission=self._run_mission,
            load_mission=lambda project_id, mission_id: FakeMission(id=mission_id),
            execute_fn=lambda max_cycles, repo_root=None: (lambda job: None),
            materialise=self._materialise,
            plan_call_fn=lambda: self.plan_fn,
            move_call_fn=lambda: self.move_fn,
        )

    def _materialise(self, run_dir: Path) -> Path:
        workspace = run_dir / "workspace"
        workspace.mkdir(parents=True, exist_ok=True)
        return workspace

    def _run_mission(self, mission_id: str, limits, **kwargs) -> FakeResult:
        from packages.orchestration.data_paths import resolve_data_root

        (resolve_data_root() / "missions").mkdir(parents=True, exist_ok=True)
        return FakeResult()


@pytest.fixture()
def real_root(tmp_path: Path) -> Path:
    """A stand-in for the operator's data root, with something in it to lose."""
    root = tmp_path / "real-data"
    (root / "projects").mkdir(parents=True)
    (root / "projects" / "keep.json").write_text('{"id": "keep"}', encoding="utf-8")
    return root


def run_with(plan_fn, move_fn, tmp_path: Path, real_root: Path) -> dict[str, Any]:
    """Drive one order and hand back what its ``run.json`` really says."""
    rec = ModelRecorder(plan_fn=plan_fn, move_fn=move_fn)
    outcome = run_order(an_order(), campaign_root=tmp_path / "campaign",
                        real_data_root=real_root, deps=rec.deps())
    return json.loads((outcome.run_dir / RUN_FILENAME).read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# 1. An observed binding reaches the evidence
# ---------------------------------------------------------------------------

def test_an_observed_model_per_role_is_recorded(tmp_path: Path,
                                                real_root: Path) -> None:
    body = run_with(labelled_call_fn("qwen3:8b"), labelled_call_fn("gpt-oss:20b"),
                    tmp_path, real_root)
    assert body["models"]["planner"] == "qwen3:8b"
    assert body["models"]["orchestrator"] == "gpt-oss:20b"


# ---------------------------------------------------------------------------
# 2. and 3. An unobserved binding is an ABSENCE, never a default name
# ---------------------------------------------------------------------------

def test_an_unlabelled_call_fn_is_recorded_as_absent(tmp_path: Path,
                                                     real_root: Path) -> None:
    body = run_with(unlabelled_call_fn(), unlabelled_call_fn(),
                    tmp_path, real_root)
    assert body["models"] == {"planner": None, "orchestrator": None,
                              "builder": None}


def test_no_call_fn_at_all_is_recorded_as_absent_without_raising(
        tmp_path: Path, real_root: Path) -> None:
    """``make_structured_call_fn`` returns None when Ollama is unreachable."""
    body = run_with(None, None, tmp_path, real_root)
    assert body["models"] == {"planner": None, "orchestrator": None,
                              "builder": None}
    assert body["terminal_status"] == TERMINAL_ACHIEVED


def test_an_absence_never_becomes_a_default_model_name(tmp_path: Path,
                                                       real_root: Path) -> None:
    """The failure D7's third condition exists to prevent, pinned directly."""
    rec = ModelRecorder(plan_fn=None, move_fn=None)
    outcome = run_order(an_order(), campaign_root=tmp_path / "campaign",
                        real_data_root=real_root, deps=rec.deps())
    raw = (outcome.run_dir / RUN_FILENAME).read_text(encoding="utf-8").lower()
    from packages.orchestration.model_aliases import resolve_model_alias

    assert resolve_model_alias("ollama-default").lower() not in raw
    assert all(value is None for value in outcome.body["models"].values())


# ---------------------------------------------------------------------------
# 4. The builder is unobservable from this seam, in every case
# ---------------------------------------------------------------------------

def test_the_builder_is_absent_whatever_the_other_roles_report(
        tmp_path: Path, real_root: Path) -> None:
    for plan_fn, move_fn in ((labelled_call_fn("qwen3:8b"),
                              labelled_call_fn("gpt-oss:20b")),
                             (unlabelled_call_fn(), unlabelled_call_fn()),
                             (None, None)):
        body = run_with(plan_fn, move_fn, tmp_path / str(id(plan_fn)), real_root)
        assert body["models"]["builder"] is None


def test_every_role_the_runner_knows_about_is_present_as_a_key(
        tmp_path: Path, real_root: Path) -> None:
    body = run_with(None, None, tmp_path, real_root)
    assert set(body["models"]) == set(ROLES)


# ---------------------------------------------------------------------------
# 5. Additivity: the exact key set, base plus `models` and nothing else
# ---------------------------------------------------------------------------

def test_the_emitted_body_is_the_base_key_set_plus_models(tmp_path: Path) -> None:
    """D7's first condition, proven as a whole-set equality rather than a
    presence check: an existing key that was renamed or dropped fails here."""
    body = _evidence_body(an_order(), TERMINAL_ACHIEVED, 1.0, [], None, [],
                          "meta-sha256:before", tmp_path,
                          {"planner": None, "orchestrator": None,
                           "builder": None})
    assert set(body) == BASE_BODY_KEYS | {"models"}
    assert body["tokens_source"] == TOKENS_UNMEASURED
    assert "tokens" not in body


def test_the_written_run_json_adds_only_the_after_hash(tmp_path: Path,
                                                       real_root: Path) -> None:
    """``run_order`` adds ``data_root_hash_after`` AFTER the body is built, so
    the file carries exactly one key more than the emitted body."""
    body = run_with(None, None, tmp_path, real_root)
    assert set(body) == BASE_BODY_KEYS | {"models", "data_root_hash_after"}


# ---------------------------------------------------------------------------
# 6. The READ half: the recorded map reaches the bench record, and survives
#    the history file
# ---------------------------------------------------------------------------

def a_recorded_body(tmp_path: Path,
                    models: dict[str, str | None] | None) -> dict[str, Any]:
    """A body from the REAL emitter, never a hand-written dict.

    The read half is only pinned if it is pinned against what the write half
    actually emits; a literal body here would pin this file against itself.
    """
    return _evidence_body(an_order(), TERMINAL_ACHIEVED, 1.0, [], None, [],
                          "meta-sha256:before", tmp_path, models)


def a_record(tmp_path: Path, models: dict[str, str | None] | None):
    """One bench row built from one recorded body, through the real builder."""
    return build_bench_record(
        evidence_body=a_recorded_body(tmp_path, models), series="s1",
        verdict=None)


def test_the_recorded_models_map_reaches_the_bench_record(tmp_path: Path) -> None:
    record = a_record(tmp_path, {"planner": "qwen3:8b",
                                 "orchestrator": "gpt-oss:20b",
                                 "builder": None})
    assert record.models == {"planner": "qwen3:8b",
                             "orchestrator": "gpt-oss:20b",
                             "builder": None}


def test_a_run_that_observed_no_role_reads_back_as_three_absences(
        tmp_path: Path) -> None:
    """One half of the two different absences: the run DID record model
    context, and every role in it was unobservable."""
    assert a_record(tmp_path, None).models == {"planner": None,
                                               "orchestrator": None,
                                               "builder": None}


def test_a_body_with_no_models_key_at_all_reads_back_as_none(
        tmp_path: Path) -> None:
    """The other half: a run from BEFORE the write half landed recorded
    nothing, which is not the same fact as three absences (R-0178)."""
    body = a_recorded_body(tmp_path, None)
    del body["models"]
    record = build_bench_record(evidence_body=body, series="s1", verdict=None)
    assert record.models is None


def test_to_json_carries_models_sorted_and_survives_a_json_round_trip(
        tmp_path: Path) -> None:
    row = a_record(tmp_path, {"planner": "qwen3:8b",
                              "orchestrator": "gpt-oss:20b",
                              "builder": None}).to_json()
    assert row["models"] == {"planner": "qwen3:8b",
                             "orchestrator": "gpt-oss:20b",
                             "builder": None}
    assert list(row) == sorted(row)
    assert json.loads(json.dumps(row)) == row


def test_models_survives_the_real_history_file(tmp_path: Path) -> None:
    """A field that only survives ``to_json`` has not survived the FILE."""
    record = a_record(tmp_path, {"planner": "qwen3:8b",
                                 "orchestrator": "gpt-oss:20b",
                                 "builder": None})
    path = tmp_path / "bench_history.jsonl"
    assert append_bench_run([record], path=path) == 1
    loaded = load_bench_history(path)
    assert len(loaded) == 1
    assert loaded[0].record.models == record.models


def test_a_history_line_written_before_the_read_half_still_loads(
        tmp_path: Path) -> None:
    """Back-compat as a property of the READER, not of a migration: the
    history is append-only, so an old row never gains the new key."""
    path = tmp_path / "bench_history.jsonl"
    path.write_text(json.dumps({
        "bench_history_version": BENCH_HISTORY_VERSION,
        "run_seq": 1,
        "row": {"order_id": "g01-pure-code-change", "series": "s1",
                "passed": True, "cost": {"in": 10, "out": 20},
                "wall_s": 1.5, "repair_rounds": None,
                "postmortem_classes": []},
    }) + "\n", encoding="utf-8")
    loaded = load_bench_history(path)
    assert len(loaded) == 1
    row = loaded[0].record
    assert row.models is None
    assert row.order_id == "g01-pure-code-change"
    assert row.passed is True
    assert row.cost == {"in": 10, "out": 20}
    assert row.wall_s == 1.5
