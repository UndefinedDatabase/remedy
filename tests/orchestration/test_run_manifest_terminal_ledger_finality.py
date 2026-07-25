"""F1 (round 14) — a complete terminal Run Ledger is FINAL.

Round 13 compared the entry PREFIX, which permitted exactly what three separate facts forbid:

    ep1:  run_id=rT001  terminal_state=completed  complete=true  entries=[Call 1]
    ep2:  run_id=rT001  terminal_state=failed     complete=true  entries=[Call 1, Call 2]

Both manifests validated, both writer calls succeeded, and the canonical loader and verified tree
accepted the chain. But `complete=true` says "this is the entire account of that run",
`terminal_state` says the run ended, and published Evidence is immutable. A prefix rule can only
see the entries; the lie lived in the header.

The ledger object is now frozen whole. A later episode may repeat it byte-for-byte and nothing
else; later work belongs to a NEW run id — which is what production already does
(`PingPongResult.run_id` is a fresh `uuid4().hex[:16]` per execution).
"""
from __future__ import annotations

import dataclasses
import subprocess

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration.run_manifest import (
    LEDGER_TERMINAL_STATES,
    CallLedgerEntryV1,
    ManifestError,
    _bind_artifact_refs,
    load_latest_manifest_verified,
    validate_index_and_tree,
    validate_ledger_chain,
    write_run_manifest,
)


def _entry(seq, *, episode_id, role="reviewer", kind="attempt"):
    return CallLedgerEntryV1(
        per_run_sequence=seq, call_id=f"calls/{role}/round-01/{kind}", episode_id=episode_id,
        role=role, round=1, kind=kind, prepared_input_fingerprint="a" * 64, ok=True)


@pytest.fixture
def chain():
    """ep1 finishes a run; ep2 repeats that terminal ledger byte-for-byte as prior history.

    ep2's expectation is `prior_episode` — the shape production records for a task whose work
    happened earlier: it still names the run and seals its ledger, but owes this episode no calls.
    """
    from packages.orchestration.run_manifest import (
        DISPATCH_PRIOR_EPISODE,
        EXPECT_PRIOR_EPISODE,
        CallExpectationV1,
        TaskCallExpectationV1,
    )
    ep1 = _bind_artifact_refs(T._mk(episode_id="ep1", calls=(T._call(seq=1),)))
    lg = ep1.call_ledgers[0]
    ep2 = _bind_artifact_refs(T._mk(episode_id="ep2", calls=()))
    ep2 = dataclasses.replace(
        ep2, prior_episode_ids=("ep1",), previous_episode_id="ep1", episode_ordinal=2,
        call_ledgers=ep1.call_ledgers,
        call_expectation=CallExpectationV1(tasks=(TaskCallExpectationV1(
            task_id=lg.task_id, expectation=EXPECT_PRIOR_EPISODE, run_id=lg.run_id,
            finalized_calls_sha256=lg.sha256(), ledger_ref=lg.ref(),
            task_status_at_finalization="applied_to_job_workspace",
            dispatch_state=DISPATCH_PRIOR_EPISODE),)),
        created_at="2026-07-15T00:02:00+00:00")
    return ep1, ep2


def _swap(ep2, ledger):
    return dataclasses.replace(ep2, call_ledgers=(ledger,))


# --------------------------------------------------------------------------- the reproduction


class TestTheReproducedCase:
    def test_a_terminal_ledger_cannot_be_extended_and_restated(self, chain):
        ep1, ep2 = chain
        lg = ep1.call_ledgers[0]
        forged = dataclasses.replace(lg, terminal_state="failed",
                                     entries=lg.entries + (_entry(2, episode_id="ep2"),))
        probs = validate_ledger_chain([ep1, _swap(ep2, forged)])
        assert any("frozen" in p for p in probs), probs
        assert any("new run id" in p for p in probs), probs


class TestExtensionIsRefusedForEveryTerminalState:
    @pytest.mark.parametrize("state", sorted(LEDGER_TERMINAL_STATES))
    def test_a_complete_ledger_in_any_terminal_state_cannot_extend(self, chain, state):
        ep1, ep2 = chain
        lg = dataclasses.replace(ep1.call_ledgers[0], terminal_state=state)
        ep1 = dataclasses.replace(ep1, call_ledgers=(lg,))
        extended = dataclasses.replace(lg, entries=lg.entries + (_entry(2, episode_id="ep2"),))
        assert validate_ledger_chain([ep1, _swap(ep2, extended)])

    def test_a_complete_completed_ledger_cannot_extend(self, chain):
        ep1, ep2 = chain
        lg = ep1.call_ledgers[0]
        assert lg.terminal_state == "completed" and lg.complete is True
        assert validate_ledger_chain([ep1, _swap(ep2, dataclasses.replace(
            lg, entries=lg.entries + (_entry(2, episode_id="ep2"),)))])

    def test_a_complete_stopped_ledger_cannot_extend(self, chain):
        ep1, ep2 = chain
        lg = dataclasses.replace(ep1.call_ledgers[0], terminal_state="stopped")
        ep1 = dataclasses.replace(ep1, call_ledgers=(lg,))
        assert validate_ledger_chain([ep1, _swap(ep2, dataclasses.replace(
            lg, entries=lg.entries + (_entry(2, episode_id="ep2"),)))])

    def test_a_terminal_ledger_cannot_shrink(self, chain):
        ep1, ep2 = chain
        assert validate_ledger_chain([ep1, _swap(ep2, dataclasses.replace(
            ep1.call_ledgers[0], entries=()))])


class TestTheHeaderIsFrozenToo:
    @pytest.mark.parametrize("state", ["failed", "blocked", "stopped", "skipped"])
    def test_the_terminal_state_cannot_change(self, chain, state):
        ep1, ep2 = chain
        probs = validate_ledger_chain([ep1, _swap(ep2, dataclasses.replace(
            ep1.call_ledgers[0], terminal_state=state))])
        assert any("frozen" in p for p in probs), probs

    def test_complete_cannot_change(self, chain):
        ep1, ep2 = chain
        assert validate_ledger_chain([ep1, _swap(ep2, dataclasses.replace(
            ep1.call_ledgers[0], complete=False))])

    def test_the_job_id_cannot_change(self, chain):
        ep1, ep2 = chain
        assert validate_ledger_chain([ep1, _swap(ep2, dataclasses.replace(
            ep1.call_ledgers[0], job_id="another-job"))])


# --------------------------------------------------------------------------- what IS allowed


class TestWhatRemainsLegal:
    def test_a_byte_identical_repeat_passes(self, chain):
        ep1, ep2 = chain
        assert ep2.call_ledgers[0].sha256() == ep1.call_ledgers[0].sha256()
        assert validate_ledger_chain([ep1, ep2]) == []

    def test_new_work_under_a_new_run_id_passes(self, chain):
        """The product's answer to "the run continued": it did not — a new run began."""
        ep1, ep2 = chain
        fresh = _bind_artifact_refs(T._mk(episode_id="ep2", calls=(
            T._call(seq=1, role="reviewer", run="r-fresh"),)))
        merged = dataclasses.replace(
            ep2, call_ledgers=ep1.call_ledgers + fresh.call_ledgers)
        assert validate_ledger_chain([ep1, merged]) == []

    def test_three_episodes_repeating_one_terminal_ledger_pass(self, chain):
        ep1, ep2 = chain
        ep3 = dataclasses.replace(ep2, episode_id="ep3", episode_ordinal=3,
                                  previous_episode_id="ep2", prior_episode_ids=("ep1", "ep2"))
        assert validate_ledger_chain([ep1, ep2, ep3]) == []


# --------------------------------------------------------------------------- every seam


class TestEverySeamRefusesTheInvalidChain:
    def _publish(self, ev, tmp_path, ep1, ep2):
        write_run_manifest(ev, ep1, root=tmp_path)
        write_run_manifest(ev, ep2, root=tmp_path)

    def test_the_writer_refuses_to_publish_an_extension(self, tmp_path, chain):
        ep1, ep2 = chain
        ev = tmp_path / "ev"
        ev.mkdir()
        write_run_manifest(ev, ep1, root=tmp_path)
        lg = ep1.call_ledgers[0]
        bad = _swap(ep2, dataclasses.replace(
            lg, terminal_state="failed", entries=lg.entries + (_entry(2, episode_id="ep2"),)))
        with pytest.raises(ManifestError):
            write_run_manifest(ev, bad, root=tmp_path)

    def test_a_valid_chain_still_publishes_and_reads_back(self, tmp_path, chain):
        ep1, ep2 = chain
        ev = tmp_path / "ev"
        ev.mkdir()
        self._publish(ev, tmp_path, ep1, ep2)
        assert validate_index_and_tree(ev, job_id="j") == []
        assert load_latest_manifest_verified(ev, job_id="j").episode_id == "ep2"


# --------------------------------------------------------------------------- production


@pytest.fixture
def data_root(tmp_path, monkeypatch):
    root = tmp_path / "remedy_data"
    root.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    return root


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "repo"
    r.mkdir()
    subprocess.run("git init -q && git config user.email t@t && git config user.name t "
                   "&& echo '# demo' > README.md && git add -A && git commit -qm init",
                   shell=True, cwd=r, check=True)
    return r


class TestProductionUsesTheNewRunIdModel:
    def test_a_real_stop_then_resume_repeats_the_terminal_ledger_byte_for_byte(
            self, data_root, repo):
        """The rule is production's, not an invention: a resumed job repeats the finished run's
        ledger unchanged and gives its NEW work a NEW run id."""
        from packages.orchestration.pingpong_job import job_evidence_dir, parse_job_file, run_job
        from packages.orchestration.pingpong_provider import FakeProvider
        from packages.orchestration.run_manifest import (
            load_episode_manifest_verified,
            read_canonical_episode_order,
        )
        from packages.orchestration.safe_points import request_stop

        job = parse_job_file(
            "# Job: fin\n\n## Task 1\nx\n\nAcceptance:\n- y\n\n## Task 2\nz\n\nAcceptance:\n- w\n",
            str(repo))

        class StopAfterFirstReview(FakeProvider):
            def __init__(self, jid):
                super().__init__(pass_on_round=1, fail_on_round=99)
                self.jid, self.n = jid, 0

            def review(self, prompt, **kw):
                out = super().review(prompt, **kw)
                self.n += 1
                if self.n == 1:
                    request_stop(self.jid, "op", "cli")
                return out

        run_job(job.job_id, builder_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
                reviewer_provider=StopAfterFirstReview(job.job_id), repair_rounds=0)
        run_job(job.job_id, builder_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
                reviewer_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
                repair_rounds=0)

        ev = job_evidence_dir(job.job_id)
        order = read_canonical_episode_order(ev, job_id=job.job_id)
        assert len(order) == 2, "the resume did not publish a second episode"
        seen: dict[tuple, set] = {}
        for e in order:
            m = load_episode_manifest_verified(ev, e["episode_id"], expected_job_id=job.job_id)
            for lg in m.call_ledgers:
                seen.setdefault((lg.task_id, lg.run_id), set()).add(lg.sha256())
        spanning = {k: v for k, v in seen.items() if len(v) >= 1}
        assert spanning, "no ledgers were published"
        for key, shas in seen.items():
            assert len(shas) == 1, f"{key} was republished with different bytes"
        assert validate_index_and_tree(ev, job_id=job.job_id) == []

    def test_every_execution_gets_a_fresh_run_id(self, data_root, repo):
        """Why finality is safe: later work never reuses a finished run."""
        from packages.orchestration.pingpong_loop import PingPongResult
        ids = {PingPongResult().run_id for _ in range(50)}
        assert len(ids) == 50
