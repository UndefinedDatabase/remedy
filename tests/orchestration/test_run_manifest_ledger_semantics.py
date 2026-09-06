"""F1/F2/F3 (round 13) — what a Run Call Ledger MEANS.

Round 12 made the ledger real bytes. This round makes those bytes say something true:

* `complete` was written and never read, so a partial account of a run could be sealed into a
  published terminal reference as the whole story;
* `terminal_state` was derived from the surrounding TASK's status, which is a different fact that
  moves for its own reasons — and an unrecognised status quietly became `"stopped"`;
* the Manifest/Ledger bijection compared role/round/kind/fingerprint/episode but NOT `ok`, so the
  two accounts of one call could disagree about whether it succeeded, both sealed, both valid.
"""
from __future__ import annotations

import dataclasses
import json
import subprocess

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration.run_manifest import (
    LEDGER_CALL_BIJECTION_FIELDS,
    MODE_CURRENT_CANDIDATE,
    MODE_PUBLISHED_REFERENCE,
    RUN_FINAL_STATUS_TO_LEDGER_STATE,
    _bind_artifact_refs,
    _ledger_state_for_run,
    validate_run_call_ledger,
    validate_run_manifest,
)


def _published(m):
    return validate_run_manifest(m, mode=MODE_PUBLISHED_REFERENCE)


def _reseal(base, lg):
    """Re-seal the expectation over the forged ledger — the tamper must not be caught merely
    because a hash no longer matches. The forger would update the hash; so do we."""
    te = base.call_expectation.tasks[0]
    return dataclasses.replace(base, call_ledgers=(lg,), call_expectation=dataclasses.replace(
        base.call_expectation, tasks=(dataclasses.replace(
            te, finalized_calls_sha256=lg.sha256(), ledger_ref=lg.ref()),)))


@pytest.fixture
def base():
    return _bind_artifact_refs(T._mk(calls=(T._call(seq=1),)))


# --------------------------------------------------------------------------- F1 completeness


class TestAPublishedLedgerMustBeComplete:
    def test_the_reproduced_case(self, base):
        """`complete=false` + a correctly updated hash validated as a published reference."""
        forged = _reseal(base, dataclasses.replace(base.call_ledgers[0], complete=False))
        probs = _published(forged)
        assert any("incomplete" in p for p in probs), probs

    def test_a_complete_ledger_passes(self, base):
        assert base.call_ledgers[0].complete is True
        assert _published(base) == []

    def test_an_incomplete_ledger_is_allowed_where_the_contract_says_so(self, base):
        """A candidate that has not finished is not a lie — it is unfinished. It says so."""
        lg = dataclasses.replace(base.call_ledgers[0], complete=False)
        assert validate_run_call_ledger(lg, mode=MODE_CURRENT_CANDIDATE) == []
        assert any("incomplete" in p
                   for p in validate_run_call_ledger(lg, mode=MODE_PUBLISHED_REFERENCE))

    def test_complete_must_be_a_real_boolean(self, base):
        lg = dataclasses.replace(base.call_ledgers[0], complete="yes")
        assert any("not a boolean" in p for p in validate_run_call_ledger(lg))


# --------------------------------------------------------------------------- F2 terminal state


class TestTheTerminalStateComesFromTheRunRecord:
    @pytest.mark.parametrize("final_status,expected", sorted(
        RUN_FINAL_STATUS_TO_LEDGER_STATE.items()))
    def test_the_matrix_is_exactly_the_runs_own_vocabulary(self, final_status, expected):
        state, probs = _ledger_state_for_run({"final_status": final_status}, where="w")
        assert (state, probs) == (expected, [])

    def test_the_matrix_is_closed(self):
        """An unknown outcome is reported, never defaulted into a plausible one."""
        state, probs = _ledger_state_for_run({"final_status": "something_new"}, where="w")
        assert state == ""
        assert any("not a recognised terminal status" in p for p in probs)

    def test_a_run_record_is_strictly_decoded(self):
        for run, expect in (({}, "no final_status"),
                            ({"final_status": 7}, "not a string"),
                            ({"final_status": ""}, "has not reached a terminal state")):
            state, probs = _ledger_state_for_run(run, where="w")
            assert state == ""
            assert any(expect in p for p in probs), (run, probs)

    def test_a_ledger_state_contradicting_the_task_lifecycle_blocks(self, base):
        """THE finding: task/manifest describe a successful execution, the ledger says failed."""
        te = base.call_expectation.tasks[0]
        assert te.task_status_at_finalization == "applied_to_job_workspace"
        forged = _reseal(base, dataclasses.replace(base.call_ledgers[0],
                                                   terminal_state="failed"))
        probs = _published(forged)
        assert any("only reachable after a successful run" in p for p in probs), probs

    @pytest.mark.parametrize("state", ["stopped", "blocked", "skipped"])
    def test_no_non_completed_state_survives_an_applied_task(self, base, state):
        forged = _reseal(base, dataclasses.replace(base.call_ledgers[0], terminal_state=state))
        assert _published(forged) != []

    def test_an_unsupported_terminal_state_blocks(self, base):
        forged = _reseal(base, dataclasses.replace(base.call_ledgers[0],
                                                   terminal_state="invented"))
        assert any("unsupported" in p for p in _published(forged))


# --------------------------------------------------------------------------- F3 the result


class TestTheLedgerEntryResultMatchesTheCall:
    def test_the_reproduced_case(self, base):
        """Manifest call ok=true, ledger entry ok=false, hash resealed — it validated."""
        assert base.calls[0].ok is True
        lg = base.call_ledgers[0]
        forged = _reseal(base, dataclasses.replace(
            lg, entries=(dataclasses.replace(lg.entries[0], ok=False),)))
        probs = _published(forged)
        assert any("ok" in p and "!=" in p for p in probs), probs

    def test_ok_is_part_of_the_named_bijection(self):
        assert "ok" in LEDGER_CALL_BIJECTION_FIELDS

    def test_the_bijection_names_every_replay_material_field(self):
        """F140 replays on these; a field that drifts out of this tuple stops being checked."""
        assert set(LEDGER_CALL_BIJECTION_FIELDS) == {
            "call_id", "episode_id", "role", "round", "kind",
            "prepared_input_fingerprint", "ok"}

    @pytest.mark.parametrize("field,value", [
        ("role", "reviewer"), ("round", 9), ("kind", "parse-retry"),
        ("prepared_input_fingerprint", "d" * 64), ("call_id", "calls/other/round-01/attempt"),
    ])
    def test_every_bijection_field_is_compared(self, base, field, value):
        lg = base.call_ledgers[0]
        forged = _reseal(base, dataclasses.replace(
            lg, entries=(dataclasses.replace(lg.entries[0], **{field: value}),)))
        assert _published(forged) != [], f"{field} drifted without being caught"

    def test_ok_is_a_real_boolean(self, base):
        lg = base.call_ledgers[0]
        bad = dataclasses.replace(lg, entries=(dataclasses.replace(lg.entries[0], ok="true"),))
        assert any("'ok' is not a boolean" in p for p in validate_run_call_ledger(bad))


# --------------------------------------------------------------------------- production


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "repo"
    r.mkdir()
    subprocess.run("git init -q && git config user.email t@t && git config user.name t "
                   "&& echo '# demo' > README.md && git add -A && git commit -qm init",
                   shell=True, cwd=r, check=True)
    return r


@pytest.fixture
def data_root(tmp_path, monkeypatch):
    root = tmp_path / "remedy_data"
    root.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    return root


class TestProductionBuildsTheStateFromTheRun:
    def test_a_real_run_ledger_takes_its_state_from_its_run_record(self, data_root, repo):
        from packages.orchestration.pingpong_job import (
            load_job_plan,
            parse_job_file,
            run_job,
        )
        from packages.orchestration.pingpong_loop import load_run
        from packages.orchestration.pingpong_provider import FakeProvider
        from packages.orchestration.run_manifest import (
            EpisodeInputSnapshotV1,
            build_input_snapshot,
            build_run_manifest,
        )

        def prov():
            return FakeProvider(pass_on_round=1, fail_on_round=99)

        job = parse_job_file("# Job: ls\n\n## Task 1\nx\n\nAcceptance:\n- y\n", str(repo))
        run_job(job.job_id, builder_provider=prov(), reviewer_provider=prov(), repair_rounds=0)
        j = load_job_plan(job.job_id)
        run = load_run(j.tasks[0].run_id)
        assert run["final_status"] == "staged_review_passed"

        snap = build_input_snapshot(j, inspect_target=False, probe_versions=False)
        w = EpisodeInputSnapshotV1(snapshot_v=1, episode_id=j.active_episode_id,
                                   captured_at="2026-07-16T00:00:00+00:00",
                                   capture_phase="episode_start", status="ok", problems=(),
                                   input=snap)
        m = build_run_manifest(j, status="completed", episode_id=j.active_episode_id,
                               created_at="2026-07-16T00:00:00+00:00", episode_snapshot=w,
                               owned_episode_id=j.active_episode_id)
        lg = m.call_ledgers[0]
        assert lg.terminal_state == RUN_FINAL_STATUS_TO_LEDGER_STATE["staged_review_passed"]
        assert lg.complete is True

    def test_an_unreadable_run_outcome_is_incomplete_never_a_default(self, data_root, repo):
        """The old code defaulted an unknown status to "stopped" and sealed it as complete."""
        from packages.orchestration.data_paths import pingpong_run_dir
        from packages.orchestration.pingpong_job import (
            load_job_plan,
            parse_job_file,
            run_job,
        )
        from packages.orchestration.pingpong_provider import FakeProvider
        from packages.orchestration.run_manifest import (
            EpisodeInputSnapshotV1,
            build_input_snapshot,
            build_run_manifest,
        )

        def prov():
            return FakeProvider(pass_on_round=1, fail_on_round=99)

        job = parse_job_file("# Job: ls\n\n## Task 1\nx\n\nAcceptance:\n- y\n", str(repo))
        run_job(job.job_id, builder_provider=prov(), reviewer_provider=prov(), repair_rounds=0)
        j = load_job_plan(job.job_id)
        p = pingpong_run_dir(j.tasks[0].run_id) / "result.json"
        d = json.loads(p.read_text())
        d["final_status"] = "a_status_from_the_future"
        p.write_text(json.dumps(d))

        snap = build_input_snapshot(j, inspect_target=False, probe_versions=False)
        w = EpisodeInputSnapshotV1(snapshot_v=1, episode_id=j.active_episode_id,
                                   captured_at="2026-07-16T00:00:00+00:00",
                                   capture_phase="episode_start", status="ok", problems=(),
                                   input=snap)
        m = build_run_manifest(j, status="completed", episode_id=j.active_episode_id,
                               created_at="2026-07-16T00:00:00+00:00", episode_snapshot=w,
                               owned_episode_id=j.active_episode_id)
        assert m.call_ledgers[0].complete is False
        assert m.coverage.status == "incomplete"
        assert any("not a recognised terminal status" in p for p in m.coverage.problems)
        # And such a record can never be published as a terminal reference.
        assert _published(m) != []
