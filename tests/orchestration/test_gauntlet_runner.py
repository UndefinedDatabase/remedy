"""F075 T003a — the live runner, driven with doubles instead of a provider.

No test here calls a model. What is proven is everything around the provider:
that a run happens inside its OWN data root, that the operator's real root is
hashed before and after and comes out byte-identical, that the order's budget
reaches the product through the existing config keys, that the evidence lands
in the recorded schema and is judged by the REAL evaluator, and that a run
which dies takes only itself down.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pytest

from packages.orchestration.gauntlet_evaluator import (
    CRITERION_DATA_ROOT_UNTOUCHED,
    evaluate_evidence_dir,
)
from packages.orchestration.gauntlet_evidence import RUN_FILENAME, load_run
from packages.orchestration.gauntlet_injection import MissingSeamError
from packages.orchestration.gauntlet_orders import GauntletOrder
from packages.orchestration.gauntlet_runner import (
    ABSENT_ROOT_DIGEST,
    ENV_DATA_ROOT,
    ENV_MAX_TOKENS,
    ENV_MAX_WALL_MINUTES,
    ISOLATED_ROOT_DIRNAME,
    TOKENS_UNMEASURED,
    RunnerDeps,
    data_root_digest,
    isolated_environment,
    measure_tokens,
    run_campaign,
    run_order,
)
from packages.orchestration.orchestrator_loop import TERMINAL_ACHIEVED


def an_order(order_id: str = "g01-pure-code-change", *, injections=(),
             max_iterations: int = 4, max_tokens: int = 250_000,
             max_wall_seconds: int = 2_400) -> GauntletOrder:
    return GauntletOrder(
        id=order_id, kind="pure_code_change", title="t", rationale="r",
        risk_probed="risk", goal="do the thing",
        milestones=({"id": "M001", "title": "m", "dod": ["x"]},),
        budget={"max_iterations": max_iterations, "max_tokens": max_tokens,
                "max_wall_seconds": max_wall_seconds},
        injections=tuple(injections), file_name=f"{order_id}.json", sha256="d")


@dataclass
class FakeMission:
    id: str = "m-1"
    job_links: tuple = ()


@dataclass
class FakeResult:
    terminal: str = TERMINAL_ACHIEVED
    entries: list = field(default_factory=list)


def ledger_entry(prompt: int = 0, completion: int = 0, detail: str = "",
                 measured: bool = True) -> dict[str, Any]:
    return {"iteration": 1, "outcome": {"status": "dispatched", "detail": detail},
            "cost": {"calls": 1,
                     "usage": ({"prompt_tokens": prompt,
                                "completion_tokens": completion}
                               if measured else None)}}


@dataclass
class Recorder:
    """Doubles for the three product verbs, remembering what they were handed."""

    terminal: str = TERMINAL_ACHIEVED
    entries: list = field(default_factory=list)
    raise_in_run: Exception | None = None
    seen_limits: Any = None
    seen_env: dict[str, str] = field(default_factory=dict)
    wrote_into: Path | None = None

    def deps(self) -> RunnerDeps:
        return RunnerDeps(
            make_project=self._make_project,
            create_mission=self._create_mission,
            plan_mission=self._plan_mission,
            run_mission=self._run_mission,
            load_mission=lambda project_id, mission_id: FakeMission(id=mission_id),
            plan_call_fn=lambda: (lambda p, a: "{}"),
            move_call_fn=lambda: (lambda p, a: "{}"),
        )

    def _make_project(self, name: str, slug: str) -> str:
        return "p-1"

    def _create_mission(self, project_id: str, goal: str) -> FakeMission:
        return FakeMission()

    def _plan_mission(self, project_id: str, mission_id: str, call_fn) -> Any:
        return None

    def _run_mission(self, mission_id: str, limits, **kwargs) -> FakeResult:
        self.seen_limits = limits
        self.seen_env = {k: os.environ.get(k, "")
                         for k in (ENV_DATA_ROOT, ENV_MAX_TOKENS, ENV_MAX_WALL_MINUTES)}
        # Write through the product's own resolution, so "the isolated root was
        # actually used" is proven by where the bytes land, not by a mock call.
        from packages.orchestration.data_paths import resolve_data_root

        self.wrote_into = resolve_data_root()
        (self.wrote_into / "missions").mkdir(parents=True, exist_ok=True)
        (self.wrote_into / "missions" / "ledger.jsonl").write_text("{}\n",
                                                                   encoding="utf-8")
        if self.raise_in_run is not None:
            raise self.raise_in_run
        return FakeResult(terminal=self.terminal, entries=list(self.entries))


@pytest.fixture()
def real_root(tmp_path: Path) -> Path:
    """A stand-in for the operator's data root, with something in it to lose."""
    root = tmp_path / "real-data"
    (root / "projects").mkdir(parents=True)
    (root / "projects" / "keep.json").write_text('{"id": "keep"}', encoding="utf-8")
    return root


# ---------------------------------------------------------------------------
# Hashing a data root
# ---------------------------------------------------------------------------

def test_an_absent_root_hashes_to_a_named_answer(tmp_path: Path) -> None:
    assert data_root_digest(tmp_path / "nowhere") == ABSENT_ROOT_DIGEST


def test_the_digest_is_stable_across_calls(real_root: Path) -> None:
    assert data_root_digest(real_root) == data_root_digest(real_root)


def test_a_new_file_changes_the_digest(real_root: Path) -> None:
    before = data_root_digest(real_root)
    (real_root / "projects" / "stray.json").write_text("{}", encoding="utf-8")
    assert data_root_digest(real_root) != before


def test_a_moved_file_changes_the_digest(real_root: Path) -> None:
    """Byte-untouched has to mean the tree, not a bag of contents."""
    before = data_root_digest(real_root)
    (real_root / "projects" / "keep.json").rename(real_root / "keep.json")
    assert data_root_digest(real_root) != before


# ---------------------------------------------------------------------------
# Isolation
# ---------------------------------------------------------------------------

def test_isolation_sets_and_restores_every_key(tmp_path: Path) -> None:
    order = an_order(max_tokens=123_456, max_wall_seconds=90)
    before = {k: os.environ.get(k) for k in
              (ENV_DATA_ROOT, ENV_MAX_TOKENS, ENV_MAX_WALL_MINUTES)}
    with isolated_environment(tmp_path / "iso", order):
        assert os.environ[ENV_DATA_ROOT] == str(tmp_path / "iso")
        assert os.environ[ENV_MAX_TOKENS] == "123456"
        assert os.environ[ENV_MAX_WALL_MINUTES] == "2"  # 90s rounds up to 2 minutes
    assert {k: os.environ.get(k) for k in before} == before


def test_isolation_restores_even_when_the_body_raises(tmp_path: Path) -> None:
    before = os.environ.get(ENV_DATA_ROOT)
    with pytest.raises(RuntimeError):
        with isolated_environment(tmp_path / "iso", an_order()):
            raise RuntimeError("boom")
    assert os.environ.get(ENV_DATA_ROOT) == before


def test_a_sub_minute_budget_never_becomes_zero_minutes(tmp_path: Path) -> None:
    with isolated_environment(tmp_path / "iso", an_order(max_wall_seconds=5)):
        assert os.environ[ENV_MAX_WALL_MINUTES] == "1"


# ---------------------------------------------------------------------------
# One order
# ---------------------------------------------------------------------------

def test_the_run_happens_inside_its_own_data_root(tmp_path: Path,
                                                  real_root: Path) -> None:
    rec = Recorder()
    outcome = run_order(an_order(), campaign_root=tmp_path / "campaign",
                        real_data_root=real_root, deps=rec.deps())
    assert rec.wrote_into == outcome.run_dir / ISOLATED_ROOT_DIRNAME
    assert (outcome.run_dir / ISOLATED_ROOT_DIRNAME / "missions").is_dir()


def test_the_real_root_is_hashed_before_and_after_and_is_untouched(
        tmp_path: Path, real_root: Path) -> None:
    expected = data_root_digest(real_root)
    rec = Recorder()
    outcome = run_order(an_order(), campaign_root=tmp_path / "campaign",
                        real_data_root=real_root, deps=rec.deps())
    body = outcome.body
    assert body["data_root_hash_before"] == body["data_root_hash_after"] == expected
    assert data_root_digest(real_root) == expected


def test_the_orders_budget_reaches_the_product(tmp_path: Path,
                                               real_root: Path) -> None:
    rec = Recorder()
    order = an_order(max_iterations=7, max_tokens=99_000, max_wall_seconds=600)
    run_order(order, campaign_root=tmp_path / "campaign",
              real_data_root=real_root, deps=rec.deps())
    assert rec.seen_limits.max_iterations == 7
    assert rec.seen_env[ENV_MAX_TOKENS] == "99000"
    assert rec.seen_env[ENV_MAX_WALL_MINUTES] == "10"


def test_the_evidence_is_in_the_recorded_schema(tmp_path: Path,
                                                real_root: Path) -> None:
    rec = Recorder(entries=[ledger_entry(prompt=1_000, completion=200)])
    outcome = run_order(an_order(), campaign_root=tmp_path / "campaign",
                        real_data_root=real_root, deps=rec.deps())
    ev = load_run(outcome.run_dir)
    assert ev.load_error == ""
    assert ev.order_id == "g01-pure-code-change"
    assert ev.terminal_status == TERMINAL_ACHIEVED
    assert (ev.tokens_in, ev.tokens_out) == (1_000, 200)
    assert ev.operator_interventions == ()


def test_unmeasured_tokens_are_absent_rather_than_zero(tmp_path: Path,
                                                       real_root: Path) -> None:
    """R-0178's lesson applied at the source: a zero would be a claim."""
    rec = Recorder(entries=[ledger_entry(measured=False)])
    outcome = run_order(an_order(), campaign_root=tmp_path / "campaign",
                        real_data_root=real_root, deps=rec.deps())
    body = json.loads((outcome.run_dir / RUN_FILENAME).read_text(encoding="utf-8"))
    assert "tokens" not in body
    assert body["tokens_source"] == TOKENS_UNMEASURED
    assert load_run(outcome.run_dir).load_error == ""


def test_measure_tokens_returns_none_when_nothing_was_measured() -> None:
    assert measure_tokens([ledger_entry(measured=False)]) is None
    assert measure_tokens([]) is None
    assert measure_tokens([ledger_entry(prompt=5, completion=6)]) == {"in": 5, "out": 6}


def test_an_era_defect_refusal_is_carried_into_the_evidence(
        tmp_path: Path, real_root: Path) -> None:
    rec = Recorder(entries=[ledger_entry(
        detail="refused: self_authored_verdict in the handback")])
    outcome = run_order(an_order(), campaign_root=tmp_path / "campaign",
                        real_data_root=real_root, deps=rec.deps())
    defects = outcome.body["era_defects"]
    assert [d["kind"] for d in defects] == ["self_authored_verdict"]
    assert defects[0]["finding_class"] == "R-0144"


def test_a_declared_injection_is_recorded(tmp_path: Path, real_root: Path) -> None:
    rec = Recorder()
    outcome = run_order(an_order(injections=["truncated_model_response"]),
                        campaign_root=tmp_path / "campaign",
                        real_data_root=real_root, deps=rec.deps())
    assert [i["class"] for i in outcome.body["injections"]] == \
        ["truncated_model_response"]
    assert outcome.body["injections"][0]["disposition"]


def test_an_order_with_a_blocked_injection_fails_rather_than_running_uninjected(
        tmp_path: Path, real_root: Path) -> None:
    """Evidence that omits a declared injection would be a lie by omission."""
    rec = Recorder()
    outcome = run_order(an_order(injections=["harness_death_mid_write"]),
                        campaign_root=tmp_path / "campaign",
                        real_data_root=real_root, deps=rec.deps())
    assert MissingSeamError.__name__ in outcome.crashed
    assert outcome.terminal_status == "runner_crashed"
    assert (outcome.run_dir / RUN_FILENAME).is_file()


# ---------------------------------------------------------------------------
# A crash is a failed run, not a missing one
# ---------------------------------------------------------------------------

def test_a_crashed_run_still_writes_evidence_and_both_hashes(
        tmp_path: Path, real_root: Path) -> None:
    rec = Recorder(raise_in_run=RuntimeError("provider exploded"))
    outcome = run_order(an_order(), campaign_root=tmp_path / "campaign",
                        real_data_root=real_root, deps=rec.deps())
    assert outcome.crashed.startswith("RuntimeError")
    body = outcome.body
    assert body["data_root_hash_before"] == body["data_root_hash_after"]
    assert any("raised out of the harness" in p["detail"]
               for p in body["postmortems"])
    assert load_run(outcome.run_dir).load_error == ""


def test_a_crashed_run_is_not_flawless(tmp_path: Path, real_root: Path) -> None:
    rec = Recorder(raise_in_run=RuntimeError("provider exploded"))
    run_order(an_order(), campaign_root=tmp_path / "campaign",
              real_data_root=real_root, deps=rec.deps())
    verdict = evaluate_evidence_dir(tmp_path / "campaign")
    assert verdict.passed is False
    assert verdict.runs[0].flawless is False


def test_a_crash_does_not_scan_the_operators_root_for_postmortems(
        tmp_path: Path, real_root: Path) -> None:
    """The crash path re-enters isolation; a postmortem in the REAL root must
    not be collected into the run's evidence."""
    (real_root / "runs").mkdir(parents=True, exist_ok=True)
    (real_root / "runs" / "postmortem.json").write_text(
        json.dumps({"scope": "task", "failure_class": "unknown",
                    "raw_reason": "belongs to the operator"}), encoding="utf-8")
    rec = Recorder(raise_in_run=RuntimeError("boom"))
    outcome = run_order(an_order(), campaign_root=tmp_path / "campaign",
                        real_data_root=real_root, deps=rec.deps())
    assert not any("belongs to the operator" in p["detail"]
                   for p in outcome.body["postmortems"])


# ---------------------------------------------------------------------------
# The campaign
# ---------------------------------------------------------------------------

def test_the_campaign_runs_every_order_in_manifest_order(
        tmp_path: Path, real_root: Path) -> None:
    rec = Recorder()
    orders = tuple(an_order(f"g{i:02d}-order") for i in range(1, 4))
    outcomes = run_campaign(orders, tmp_path / "campaign", deps=rec.deps(),
                            real_data_root=real_root)
    assert [o.order_id for o in outcomes] == ["g01-order", "g02-order", "g03-order"]
    assert [o.run_dir.name for o in outcomes] == [
        "run-01-g01-order", "run-02-g02-order", "run-03-g03-order"]


def test_a_dying_run_takes_only_itself_down(tmp_path: Path, real_root: Path) -> None:
    """A missing run is worse than a failed one — the matrix is the deliverable."""

    class Flaky(Recorder):
        seen = 0

        def _run_mission(self, mission_id: str, limits, **kwargs):
            Flaky.seen += 1
            if Flaky.seen == 2:
                raise RuntimeError("second order died")
            return super()._run_mission(mission_id, limits, **kwargs)

    rec = Flaky()
    orders = tuple(an_order(f"g{i:02d}-order") for i in range(1, 4))
    outcomes = run_campaign(orders, tmp_path / "campaign", deps=rec.deps(),
                            real_data_root=real_root)
    assert [bool(o.crashed) for o in outcomes] == [False, True, False]
    verdict = evaluate_evidence_dir(tmp_path / "campaign")
    assert len(verdict.runs) == 3
    assert verdict.runs[1].flawless is False


def test_the_campaign_leaves_the_real_root_byte_identical(
        tmp_path: Path, real_root: Path) -> None:
    expected = data_root_digest(real_root)
    rec = Recorder()
    orders = tuple(an_order(f"g{i:02d}-order") for i in range(1, 4))
    run_campaign(orders, tmp_path / "campaign", deps=rec.deps(),
                 real_data_root=real_root)
    assert data_root_digest(real_root) == expected
    verdict = evaluate_evidence_dir(tmp_path / "campaign")
    assert all(r.criteria[CRITERION_DATA_ROOT_UNTOUCHED] for r in verdict.runs)


def test_each_run_gets_its_own_root_not_the_previous_ones(
        tmp_path: Path, real_root: Path) -> None:
    roots: list[Path] = []

    class Watching(Recorder):
        def _run_mission(self, mission_id: str, limits, **kwargs):
            result = super()._run_mission(mission_id, limits, **kwargs)
            roots.append(self.wrote_into)
            return result

    orders = tuple(an_order(f"g{i:02d}-order") for i in range(1, 4))
    run_campaign(orders, tmp_path / "campaign", deps=Watching().deps(),
                 real_data_root=real_root)
    assert len(set(roots)) == 3


def test_the_defaults_are_the_production_verbs() -> None:
    """The doubles above are a test convenience; nobody ships them."""
    from packages.orchestration.mission_compiler import plan_mission
    from packages.orchestration.mission_state import create_mission, load_mission
    from packages.orchestration.orchestrator_loop import run_mission

    deps = RunnerDeps()
    assert deps.create_mission is create_mission
    assert deps.plan_mission is plan_mission
    assert deps.run_mission is run_mission
    assert deps.load_mission is load_mission


# ---------------------------------------------------------------------------
# R-0180: the crash path can itself fail, and the campaign still finishes
# ---------------------------------------------------------------------------

def test_a_crash_path_that_also_raises_still_leaves_judgeable_evidence(
        tmp_path: Path, real_root: Path, monkeypatch) -> None:
    """Collecting a dead run's evidence can fail too. The fallback keeps the run
    in the matrix instead of losing it behind a NameError."""
    import packages.orchestration.gauntlet_runner as runner_mod

    def collector_explodes(_data_root):
        raise OSError("the isolated root went away mid-collection")

    monkeypatch.setattr(runner_mod, "collect_postmortems", collector_explodes)
    rec = Recorder(raise_in_run=RuntimeError("the run died"))
    outcome = run_order(an_order(), campaign_root=tmp_path / "campaign",
                        real_data_root=real_root, deps=rec.deps())

    assert outcome.crashed.startswith("RuntimeError")
    assert outcome.terminal_status == runner_mod.TERMINAL_RUNNER_CRASHED
    details = " ".join(p["detail"] for p in outcome.body["postmortems"])
    assert "collecting this run's evidence also failed" in details
    assert "the run raised out of the harness" in details
    # Still real, readable evidence with both hashes.
    ev = load_run(outcome.run_dir)
    assert ev.load_error == ""
    assert outcome.body["data_root_hash_before"] == outcome.body["data_root_hash_after"]
    assert evaluate_evidence_dir(tmp_path / "campaign").runs[0].flawless is False


def test_a_raise_from_run_order_itself_does_not_kill_the_campaign(
        tmp_path: Path, real_root: Path, monkeypatch) -> None:
    """run_campaign's promise, enforced: only the dying order dies."""
    import packages.orchestration.gauntlet_runner as runner_mod

    real_run_order = runner_mod.run_order
    calls = {"n": 0}

    def flaky_run_order(order, **kwargs):
        calls["n"] += 1
        if calls["n"] == 2:
            raise OSError("could not write this run's evidence")
        return real_run_order(order, **kwargs)

    monkeypatch.setattr(runner_mod, "run_order", flaky_run_order)
    orders = tuple(an_order(f"g{i:02d}-order") for i in range(1, 4))
    outcomes = run_campaign(orders, tmp_path / "campaign", deps=Recorder().deps(),
                            real_data_root=real_root)

    assert [bool(o.crashed) for o in outcomes] == [False, True, False]
    assert outcomes[1].terminal_status == runner_mod.TERMINAL_RUNNER_CRASHED
    assert "could not write this run's evidence" in outcomes[1].crashed
    # The survivors' evidence is intact and judgeable.
    verdict = evaluate_evidence_dir(tmp_path / "campaign")
    assert [r.run_dir for r in verdict.runs] == [
        "run-01-g01-order", "run-03-g03-order"]
