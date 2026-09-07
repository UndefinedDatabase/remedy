"""F5 (round 9) — a persisted Call's sequence and ownership are VERIFIED, never NORMALIZED.

A finalized-call record on disk is untrusted state. The manifest checks each call's identity
AGAINST its real containers — job, task, run, episode — and refuses what disagrees. What it must
never do is rewrite a wrong record until it looks right: renumbering a tampered sequence into a
contiguous 1..N order produces a manifest that reports COMPLETE coverage over data it just
invented. The tamper must survive as a coverage PROBLEM.

The stored sequence is the call's position within its OWN RUN (each task's run numbers its calls
from 1 — that is the recorded fact). The manifest's job-wide contiguous order is DERIVED, and
only a call whose stored per-run sequence verifies is ever given a derived position.
"""
from __future__ import annotations

import json
import subprocess

import pytest

from packages.orchestration.pingpong_job import load_job_plan, parse_job_file, run_job
from packages.orchestration.run_manifest import (
    COVERAGE_COMPLETE,
    COVERAGE_INCOMPLETE,
    build_input_snapshot,
    build_run_manifest,
)


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


def _prov():
    from packages.orchestration.pingpong_provider import FakeProvider
    return FakeProvider(pass_on_round=1, fail_on_round=99)


def _run(repo, text="# Job: own\n\n## Task 1\nx\n\nAcceptance:\n- y\n"):
    job = parse_job_file(text, str(repo))
    run_job(job.job_id, builder_provider=_prov(), reviewer_provider=_prov(), repair_rounds=0)
    return load_job_plan(job.job_id)


def _run_json_path(job, task_ix=0):
    from packages.orchestration.data_paths import run_dir
    return run_dir(job.tasks[task_ix].run_id) / "result.json"


def _tamper(job, mutate, *, task_ix=0, call_ix=0):
    p = _run_json_path(job, task_ix)
    d = json.loads(p.read_text())
    mutate(d["finalized_calls"][call_ix])
    p.write_text(json.dumps(d))


def _collect(job, **chain):
    from packages.orchestration.run_manifest import EpisodeInputSnapshotV1
    snap = build_input_snapshot(job, inspect_target=False, probe_versions=False)
    wrapper = EpisodeInputSnapshotV1(
        snapshot_v=1, episode_id=job.active_episode_id,
        captured_at="2026-07-16T00:00:00+00:00", capture_phase="episode_start",
        status="ok", problems=(), input=snap)
    return build_run_manifest(job, status="completed", episode_id=job.active_episode_id,
                              created_at="2026-07-16T00:00:00+00:00",
                              episode_snapshot=wrapper,
                              owned_episode_id=job.active_episode_id, **chain)


def _problems(job):
    return "; ".join(_collect(job).coverage.problems)


# --------------------------------------------------------------------------- the baseline


class TestCleanRunIsComplete:
    def test_an_untampered_run_has_complete_coverage_and_a_contiguous_order(
            self, data_root, repo):
        job = _run(repo)
        m = _collect(job)
        assert m.coverage.status == COVERAGE_COMPLETE, m.coverage.problems
        assert [c.identity.sequence for c in m.calls] == list(range(1, len(m.calls) + 1))

    def test_two_tasks_each_number_their_own_run_from_one(self, data_root, repo):
        """The REAL data model: per-run numbering on disk, job-wide order in the manifest."""
        job = _run(repo, "# Job: own\n\n## Task 1\nx\n\nAcceptance:\n- y\n"
                         "\n## Task 2\nz\n\nAcceptance:\n- w\n")
        stored = []
        for ix in range(len(job.tasks)):
            d = json.loads(_run_json_path(job, ix).read_text())
            stored.append([c["identity"]["sequence"] for c in d["finalized_calls"]])
        assert all(s == list(range(1, len(s) + 1)) for s in stored), stored
        m = _collect(job)
        assert m.coverage.status == COVERAGE_COMPLETE, m.coverage.problems
        assert [c.identity.sequence for c in m.calls] == list(range(1, len(m.calls) + 1))


# --------------------------------------------------------------------------- sequence


class TestSequenceIsVerifiedNotRenumbered:
    def test_a_tampered_sequence_is_reported_not_silently_fixed(self, data_root, repo):
        """The defect this closes: sequence 999 was renumbered to 1 and coverage still said
        COMPLETE."""
        job = _run(repo)
        _tamper(job, lambda c: c["identity"].update(sequence=999))
        m = _collect(job)
        assert m.coverage.status == COVERAGE_INCOMPLETE
        assert "stored sequence 999" in "; ".join(m.coverage.problems)
        assert all(c.identity.sequence != 999 for c in m.calls)   # never published either

    @pytest.mark.parametrize("bad", [0, -1])
    def test_a_non_positive_sequence_is_rejected(self, data_root, repo, bad):
        job = _run(repo)
        _tamper(job, lambda c: c["identity"].update(sequence=bad))
        assert _collect(job).coverage.status == COVERAGE_INCOMPLETE

    def test_a_non_integer_sequence_is_rejected(self, data_root, repo):
        job = _run(repo)
        _tamper(job, lambda c: c["identity"].update(sequence="1"))
        assert _collect(job).coverage.status == COVERAGE_INCOMPLETE

    def test_a_duplicate_sequence_is_blocking(self, data_root, repo):
        job = _run(repo)
        d = json.loads(_run_json_path(job).read_text())
        assert len(d["finalized_calls"]) >= 2, "need two calls to duplicate a sequence"
        d["finalized_calls"][1]["identity"]["sequence"] = \
            d["finalized_calls"][0]["identity"]["sequence"]
        _run_json_path(job).write_text(json.dumps(d))
        assert _collect(job).coverage.status == COVERAGE_INCOMPLETE

    def test_a_duplicate_logical_slot_is_blocking(self, data_root, repo):
        """Two records claiming the same (task, role, round, kind) cannot both be real."""
        job = _run(repo)
        d = json.loads(_run_json_path(job).read_text())
        assert len(d["finalized_calls"]) >= 2
        for f in ("role", "round", "kind"):
            d["finalized_calls"][1]["identity"][f] = d["finalized_calls"][0]["identity"][f]
        _run_json_path(job).write_text(json.dumps(d))
        assert _collect(job).coverage.status == COVERAGE_INCOMPLETE


# --------------------------------------------------------------------------- ownership


class TestOwnershipIsVerified:
    def test_a_foreign_job_id_is_rejected(self, data_root, repo):
        job = _run(repo)
        _tamper(job, lambda c: c["identity"].update(job_id="someone-elses-job"))
        assert "job_id" in _problems(job)

    def test_a_foreign_task_id_is_rejected(self, data_root, repo):
        job = _run(repo)
        _tamper(job, lambda c: c["identity"].update(task_id="T999"))
        assert "task_id" in _problems(job)

    def test_a_foreign_run_id_is_rejected(self, data_root, repo):
        job = _run(repo)
        _tamper(job, lambda c: c["identity"].update(run_id="not-this-run"))
        assert "run_id" in _problems(job)

    def test_an_empty_episode_id_is_rejected_never_adopted(self, data_root, repo):
        """An unowned call is NOT quietly adopted into the current episode."""
        job = _run(repo)
        _tamper(job, lambda c: c["identity"].update(episode_id=""))
        m = _collect(job)
        assert m.coverage.status == COVERAGE_INCOMPLETE
        assert "empty episode_id" in "; ".join(m.coverage.problems)

    def test_a_foreign_episode_with_broken_lineage_is_reported(self, data_root, repo):
        """Foreign episode AND foreign task: not a prior-episode exclusion — a real problem."""
        job = _run(repo)

        def _mutate(c):
            c["identity"].update(episode_id="ep-somewhere-else", task_id="T999")
        _tamper(job, _mutate)
        probs = _problems(job)
        assert "T999" in probs or "ep-somewhere-else" in probs, probs


class TestPriorEpisodeCallsAreExcludedNotRestamped:
    def test_a_valid_KNOWN_prior_episode_call_is_excluded_without_restamping(
            self, data_root, repo):
        """A resume must not re-collect an earlier episode's calls — and must not relabel them
        into the new episode either. It simply does not own them.

        F5 (round 10): "earlier" is not a claim the call gets to make about itself. The episode
        must be a KNOWN member of the canonical chain with a lower ordinal, listed among THIS
        episode's priors — that is what makes the exclusion provable rather than polite.
        """
        job = _run(repo)
        d = json.loads(_run_json_path(job).read_text())
        first = d["finalized_calls"][0]["identity"]["call_id"]
        d["finalized_calls"][0]["identity"]["episode_id"] = "ep-earlier"   # lineage otherwise ok
        _run_json_path(job).write_text(json.dumps(d))

        # ep-earlier is a REAL prior episode of this job's chain (ordinal 1; we are ordinal 2).
        m = _collect(job, prior_episode_ordinals={"ep-earlier": 1},
                     prior_episode_ids=("ep-earlier",), episode_ordinal=2)
        assert all(c.identity.call_id != first for c in m.calls)        # excluded
        assert all(c.identity.episode_id == job.active_episode_id for c in m.calls)
        # never restamped: no CALL was relabelled into this episode. (The id itself DOES appear
        # in prior_episode_ids — that is the chain honestly naming its own history.)
        assert "ep-earlier" not in json.dumps([c.to_json() for c in m.calls])
        assert "ep-earlier" in m.prior_episode_ids
        assert m.coverage.status == COVERAGE_COMPLETE, m.coverage.problems

    def test_an_UNKNOWN_episode_call_is_reported_not_excluded(self, data_root, repo):
        """THE finding: an episode nobody has heard of is not history — it is unattributable
        evidence, and silently dropping it produced a manifest claiming complete coverage."""
        job = _run(repo)
        d = json.loads(_run_json_path(job).read_text())
        d["finalized_calls"][-1]["identity"]["episode_id"] = "UNKNOWN-FUTURE-EPISODE"
        _run_json_path(job).write_text(json.dumps(d))
        m = _collect(job)
        assert m.coverage.status == COVERAGE_INCOMPLETE
        assert "not a known episode" in "; ".join(m.coverage.problems)

    def test_a_future_ordinal_episode_call_is_reported(self, data_root, repo):
        """A call from an episode that comes AFTER this one cannot be this one's history."""
        job = _run(repo)
        d = json.loads(_run_json_path(job).read_text())
        d["finalized_calls"][-1]["identity"]["episode_id"] = "ep-later"
        _run_json_path(job).write_text(json.dumps(d))
        m = _collect(job, prior_episode_ordinals={"ep-later": 5}, prior_episode_ids=("ep-later",),
                     episode_ordinal=2)
        assert m.coverage.status == COVERAGE_INCOMPLETE
        assert "not strictly earlier" in "; ".join(m.coverage.problems)

    def test_a_known_episode_that_is_not_listed_as_a_prior_is_reported(self, data_root, repo):
        """Known and earlier is still not enough: it must be in THIS episode's exact priors."""
        job = _run(repo)
        d = json.loads(_run_json_path(job).read_text())
        d["finalized_calls"][-1]["identity"]["episode_id"] = "ep-unlisted"
        _run_json_path(job).write_text(json.dumps(d))
        m = _collect(job, prior_episode_ordinals={"ep-unlisted": 1}, prior_episode_ids=(),
                     episode_ordinal=2)
        assert m.coverage.status == COVERAGE_INCOMPLETE
        assert "does not list among its priors" in "; ".join(m.coverage.problems)

    def test_an_excluded_prior_call_still_counts_toward_its_run_sequence(
            self, data_root, repo):
        """The stored sequence is per-RUN and counts every call the run made — including the
        ones an earlier episode owns. If exclusion silently rewound the counter, the surviving
        calls would look mis-sequenced."""
        job = _run(repo)
        d = json.loads(_run_json_path(job).read_text())
        assert len(d["finalized_calls"]) >= 2
        d["finalized_calls"][0]["identity"]["episode_id"] = "ep-earlier"   # run position 1
        _run_json_path(job).write_text(json.dumps(d))
        m = _collect(job, prior_episode_ordinals={"ep-earlier": 1},
                     prior_episode_ids=("ep-earlier",), episode_ordinal=2)
        # the SECOND call still verifies at its stored in-run position 2 and is published
        assert m.coverage.status == COVERAGE_COMPLETE, m.coverage.problems
        assert len(m.calls) == len(d["finalized_calls"]) - 1


# --------------------------------------------------------------------------- field vocabulary


class TestCallFieldsAreValidated:
    @pytest.mark.parametrize("field,value", [
        ("role", "wizard"),
        ("kind", "vibes"),
        ("round", 0),
        ("round", -3),
        ("call_id", "../escape"),
    ])
    def test_an_invalid_identity_field_is_rejected(self, data_root, repo, field, value):
        job = _run(repo)
        _tamper(job, lambda c: c["identity"].update({field: value}))
        assert _collect(job).coverage.status == COVERAGE_INCOMPLETE

    def test_a_malformed_prepared_input_is_rejected(self, data_root, repo):
        job = _run(repo)
        _tamper(job, lambda c: c["prepared_input"].update(prompt_sha256="nope"))
        assert _collect(job).coverage.status == COVERAGE_INCOMPLETE

    def test_an_empty_fingerprint_is_rejected(self, data_root, repo):
        job = _run(repo)
        _tamper(job, lambda c: c.update(fingerprint=""))
        assert _collect(job).coverage.status == COVERAGE_INCOMPLETE
