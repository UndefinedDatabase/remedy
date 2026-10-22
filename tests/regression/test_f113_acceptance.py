"""F113's Acceptance, held on real runs of the build-and-review loop (DECISIONs F113 D1 to D3).

`docs/roadmap/features/T3_F113.md` names four lines: the summary role served locally on a fixture
with correct evidence and basis; a configuration sending a core role to a local endpoint refused;
an endpoint that is down giving a clean fallback with its classification; and a failing spot check
flipping the role, status showing it, and a passing check flipping it back only through an explicit
re-check after the dwell. Each run below is `run_pingpong` on a demo repository whose oversized
repair diff the summary role must summarize; the endpoint's model answers through a fake `ollama`
client, the role's own model through a fake call_fn, and nothing reaches a real model server.
"""
from __future__ import annotations

import json
import sys
import types
import warnings
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest

from apps.cli.grouped import main as grouped_main
from packages.orchestration import artifact_summary, pingpong_loop
from packages.orchestration.data_paths import run_dir
from packages.orchestration.failure_postmortem import is_provider_unavailable_error
from packages.orchestration.job_evidence import _write_task_run_evidence
from packages.orchestration.local_endpoints import LocalEndpoint, LocalEndpointProbes
from packages.orchestration.pingpong_provider_fake import FakeProvider
from packages.orchestration.side_role_calls import SideRoleCallSummary, query_side_role_calls
from packages.orchestration.side_role_quality import (
    SPOT_CHECK_DWELL_S,
    SUMMARY_SPOT_CHECKS,
    record_spot_check,
    run_spot_check,
    side_role_status_lines,
)
from packages.orchestration.side_role_routing import resolve_side_role_routes
from tests.orchestration.test_local_endpoints import configure_toml

BOX = LocalEndpoint("box", "http://127.0.0.1:9", "muse-glimmer")
ENDPOINT = '[remedy.local_routing.endpoints.box]\nbase_url = "http://127.0.0.1:9"\nmodel = "muse-glimmer"\n'
LOCAL_REPLY = json.dumps({"l1": "summarized on the local endpoint",
                          "l2": [{"section": "big.py", "span_ref": "file:big.py", "summary": "big.py rewritten"}]})
OWN_REPLY = json.dumps({"l1": "summarized on the role's own model", "l2": []})
#: The summaries one run writes: the reviewer's of rounds 1 and 2 and the repair builder's of round 2.
CALLS = ("calls/builder/round-02/tiered_diff.diff.summary.json", "calls/reviewer/round-01/tiered_diff.diff.summary.json",
         "calls/reviewer/round-02/tiered_diff.diff.summary.json")
T0 = datetime(2026, 10, 22, 8, 0, tzinfo=timezone.utc)


@pytest.fixture()
def world(tmp_path, monkeypatch):
    """A data root, the summary role mapped to `box`, a demo repository, and a fake model behind `box`
    that summarizes a spot-check case naming every seeded fact except `world.drop`."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    configure_toml(monkeypatch, tmp_path, ENDPOINT + '[remedy.local_routing.side_roles]\nsummary = "box"\n')
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "README.md").write_text("# Demo\n", encoding="utf-8")
    big = "\n".join(f"# line {i:05d}: " + "x" * 70 for i in range(1000))

    def fake_apply(staging, builder_output, goal):
        for rel_path in builder_output.files_changed:
            (staging / rel_path).write_text(big, encoding="utf-8")

    monkeypatch.setattr(pingpong_loop, "_apply_fake_builder_changes", fake_apply)
    state = SimpleNamespace(repo=repo, tmp=tmp_path, asked=[], own=[], drop="")

    class FakeClient:
        def __init__(self, host=None, timeout=None):
            self.host = host

        def chat(self, **request):
            state.asked.append((self.host, request["model"]))
            prompt = request["messages"][-1]["content"]
            facts = [f for case in SUMMARY_SPOT_CHECKS for f in case.facts if f in prompt]
            if not facts:
                return types.SimpleNamespace(message=types.SimpleNamespace(content=LOCAL_REPLY))
            named = ", ".join(f for f in facts if f != state.drop)
            content = json.dumps({"l1": f"The change touches {named}.", "l2": []})
            return types.SimpleNamespace(message=types.SimpleNamespace(content=content))

    module = types.ModuleType("ollama")
    module.Client = FakeClient
    monkeypatch.setitem(sys.modules, "ollama", module)

    def own_model(model_cls, *, model=None, provider=None):
        return lambda prompt, attempt: state.own.append(prompt) or OWN_REPLY

    monkeypatch.setattr(artifact_summary, "make_structured_call_fn", own_model)
    return state


def endpoint_up(monkeypatch, up: bool) -> None:
    monkeypatch.setattr("packages.orchestration.side_role_routing.LOCAL_ENDPOINT_PROBES",
                        LocalEndpointProbes(list_models=lambda url: ["muse-glimmer:latest"] if up else []))


def run(world) -> tuple[str, dict[str, dict]]:
    """One real run whose repair diff is oversized; answers its id and the routes its summaries recorded."""
    provider = FakeProvider(builder_files=["big.py"], fail_on_round=1, pass_on_round=2)
    result = pingpong_loop.run_pingpong("Fix big file", str(world.repo), builder_provider=provider,
                                        reviewer_provider=provider, max_rounds=2, repair_rounds=2)
    written = sorted(path.relative_to(run_dir(result.run_id)).as_posix()
                     for path in run_dir(result.run_id).glob("calls/*/round-*/*.summary.json"))
    assert written == sorted(CALLS)
    routes = {ref: json.loads((run_dir(result.run_id) / ref).read_text(encoding="utf-8"))["route"] for ref in CALLS}
    return result.run_id, routes


def export(world, run_id: str) -> tuple[list[dict], list[SideRoleCallSummary]]:
    """The job evidence export of the run's task: the rows of its `side_role_calls.json` and the ledger's counts."""
    task = SimpleNamespace(task_id="T001", run_id=run_id, task_class="standard_build", status="passed")
    out = world.tmp / "evidence" / run_id
    written: dict[str, str] = {}
    _write_task_run_evidence(task, str(out), written, ledger_project_id="proj-1", job_id=f"job-{run_id}")
    rows = json.loads((out / "task_runs" / "T001" / "side_role_calls.json").read_text(encoding="utf-8"))["rows"]
    return rows, query_side_role_calls(project_id="proj-1")


def check(world, *, at: datetime, drop: str):
    world.drop = drop
    probes = LocalEndpointProbes(list_models=lambda url: ["muse-glimmer:latest"])
    record = run_spot_check("summary", BOX, probes=probes, now=lambda: at)
    return record, record_spot_check(record)


def test_the_summary_role_is_served_locally_with_correct_evidence_and_basis(world, monkeypatch):
    endpoint_up(monkeypatch, True)
    run_id, routes = run(world)
    assert set(world.asked) == {("http://127.0.0.1:9", "muse-glimmer")} and world.own == []
    for route in routes.values():
        assert (route["route"], route["endpoint"], route["routed_model"], route["cost_basis"]) == (
            "local", "box", "muse-glimmer", "local_zero")
    rows, ledger = export(world, run_id)
    assert sorted(row["call_ref"] for row in rows) == sorted(CALLS)
    assert {(row["cost_basis"], row["tokens_out"]) for row in rows} == {("local_zero", None)}
    assert ledger == [SideRoleCallSummary("summary", "local", "local_zero", len(CALLS))]


def test_a_configuration_sending_a_core_role_to_a_local_endpoint_is_refused(world, monkeypatch, capsys):
    configure_toml(monkeypatch, world.tmp, ENDPOINT + '[remedy.local_routing.side_roles]\nbuilder = "box"\n')
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        grouped_main(["doctor", "side-roles"])
    assert [str(w.message) for w in caught] == [
        "local_routing.side_roles: refused — builder: core_role_on_local_provider; no side role runs locally"]
    assert capsys.readouterr().out.splitlines() == ["Side roles: none is mapped to a local endpoint"]


def test_an_endpoint_that_is_down_falls_back_cleanly_with_its_classification(world, monkeypatch):
    endpoint_up(monkeypatch, False)
    run_id, routes = run(world)
    assert world.asked == [] and len(world.own) == len(CALLS)
    for route in routes.values():
        assert (route["route"], route["endpoint"], route["cost_basis"]) == ("fallback", "box", "unknown")
        assert is_provider_unavailable_error(route["reason"])
    rows, ledger = export(world, run_id)
    assert {row["route"] for row in rows} == {"fallback"}
    assert ledger == [SideRoleCallSummary("summary", "fallback", "unknown", len(CALLS))]


def test_a_failing_spot_check_flips_the_role_and_only_a_re_check_after_the_dwell_flips_it_back(world, monkeypatch):
    endpoint_up(monkeypatch, True)
    failed, entry = check(world, at=T0, drop="retry_limit")
    assert (failed.outcome, failed.reason, entry["state"]) == ("failed", "failed cases: removed-setting", "flipped")
    (line,) = side_role_status_lines(resolve_side_role_routes())
    assert line.startswith("summary on box (muse-glimmer): FLIPPED to its own model") and failed.record_id in line

    world.asked.clear()
    _, routes = run(world)
    assert world.asked == [] and len(world.own) == len(CALLS)
    assert {route["reason"] for route in routes.values()} == {
        f"quality_gate: summary on box (muse-glimmer) failed spot check {failed.record_id} at {T0.isoformat()}"}

    early, entry = check(world, at=T0 + timedelta(seconds=SPOT_CHECK_DWELL_S - 60), drop="")
    assert (early.outcome, entry["state"], entry["record_id"]) == ("passed", "flipped", failed.record_id)
    late, entry = check(world, at=T0 + timedelta(seconds=SPOT_CHECK_DWELL_S), drop="")
    assert (late.outcome, entry["state"], entry["record_id"]) == ("passed", "local", late.record_id)

    world.own.clear()
    _, routes = run(world)
    assert world.own == [] and {route["route"] for route in routes.values()} == {"local"}
