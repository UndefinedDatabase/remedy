"""F7 (round 10) — every Call is BOUND to the embedded JobInput definition.

The embedded definition is the immutable record of which tasks this episode was given. A call
naming a task that is not in it describes work no recorded input ever asked for — and a manifest
that accepts it is no longer a faithful account of its own inputs. Before round 10 a canonical
manifest whose JobInput declared `[T001]` while its call claimed `T999` validated cleanly.

The binding is against the SNAPSHOT's definition, never a later mutable `job.tasks` list: the
JobPlan can be re-planned, and finalizing against whatever it says now would silently record work
the snapshot never described.
"""
from __future__ import annotations

import dataclasses
import hashlib
import subprocess

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration.run_manifest import (
    MODE_PUBLISHED_REFERENCE,
    ManifestError,
    canonical_artifact_ref,
    validate_run_manifest,
    write_run_manifest,
)


def _bind(m):
    bound = []
    for c in m.calls:
        c = dataclasses.replace(c, artifact=canonical_artifact_ref(c.identity))
        bound.append(dataclasses.replace(
            c, artifact_sha256=hashlib.sha256(c.canonical_artifact_bytes()).hexdigest()))
    return dataclasses.replace(m, calls=tuple(bound))


# --------------------------------------------------------------------------- typed manifests


class TestCallsMustNameADeclaredTask:
    def test_a_call_for_an_undeclared_task_is_rejected(self):
        """THE finding: JobInput tasks = [T001], call task_id = T999 — accepted."""
        m = _bind(T._mk(episode_id="ep1", calls=(T._call(task="T999"),)))
        probs = validate_run_manifest(m, mode=MODE_PUBLISHED_REFERENCE)
        assert any("T999" in p and "job_input task list" in p for p in probs), probs

    def test_a_call_for_a_declared_task_is_accepted(self):
        assert validate_run_manifest(_bind(T._mk(episode_id="ep1")),
                                     mode=MODE_PUBLISHED_REFERENCE) == []

    def test_the_writer_refuses_to_publish_an_unbound_call(self, tmp_path):
        ev = tmp_path / "ev"
        ev.mkdir()
        with pytest.raises(ManifestError) as exc:
            write_run_manifest(ev, T._mk(episode_id="ep1", calls=(T._call(task="T999"),)),
                               root=tmp_path)
        assert "T999" in str(exc.value)

    def test_a_task_declared_twice_is_rejected(self):
        """"Exactly once" is the rule: a duplicated declaration makes the call's task ambiguous,
        and an ambiguous binding is not a binding."""
        ji = T._job_input()
        ji = {**ji, "tasks": [ji["tasks"][0], dict(ji["tasks"][0], order=1)]}
        snap = T._snap(job_input=ji)
        m = _bind(T._mk(episode_id="ep1", snap=snap))
        probs = validate_run_manifest(m, mode=MODE_PUBLISHED_REFERENCE)
        assert any("appears 2 times" in p for p in probs), probs

    def test_the_binding_uses_the_embedded_definition_not_live_state(self):
        """The snapshot declares T001; a call for T002 is refused even though a live JobPlan
        might by now list T002."""
        m = _bind(T._mk(episode_id="ep1", calls=(T._call(task="T002"),)))
        probs = validate_run_manifest(m, mode=MODE_PUBLISHED_REFERENCE)
        assert any("T002" in p for p in probs), probs


# --------------------------------------------------------------------------- real persisted runs


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


_JOB = "# Job: bind\n\n## Task 1\nx\n\nAcceptance:\n- y\n"
_TWO = _JOB + "\n## Task 2\nz\n\nAcceptance:\n- w\n"


def _prov():
    from packages.orchestration.pingpong_provider import FakeProvider
    return FakeProvider(pass_on_round=1, fail_on_round=99)


def _real(repo, text=_JOB):
    from packages.orchestration.pingpong_job import load_job_plan, parse_job_file, run_job
    job = parse_job_file(text, str(repo))
    run_job(job.job_id, builder_provider=_prov(), reviewer_provider=_prov(), repair_rounds=0)
    return load_job_plan(job.job_id)


def _finalize(job):
    from packages.orchestration.run_manifest import (
        EpisodeInputSnapshotV1,
        build_input_snapshot,
        build_run_manifest,
    )
    snap = build_input_snapshot(job, inspect_target=False, probe_versions=False)
    wrapper = EpisodeInputSnapshotV1(
        snapshot_v=1, episode_id=job.active_episode_id,
        captured_at="2026-07-16T00:00:00+00:00", capture_phase="episode_start",
        status="ok", problems=(), input=snap)
    return build_run_manifest(job, status="completed", episode_id=job.active_episode_id,
                              created_at="2026-07-16T00:00:00+00:00",
                              episode_snapshot=wrapper,
                              owned_episode_id=job.active_episode_id)


def _capture(job):
    """The episode-start snapshot, taken while the plan still says what it said."""
    from packages.orchestration.run_manifest import EpisodeInputSnapshotV1, build_input_snapshot
    snap = build_input_snapshot(job, inspect_target=False, probe_versions=False)
    return EpisodeInputSnapshotV1(
        snapshot_v=1, episode_id=job.active_episode_id,
        captured_at="2026-07-16T00:00:00+00:00", capture_phase="episode_start",
        status="ok", problems=(), input=snap)


def _finalize_with(job, wrapper):
    from packages.orchestration.run_manifest import build_run_manifest
    return build_run_manifest(job, status="completed", episode_id=job.active_episode_id,
                              created_at="2026-07-16T00:00:00+00:00",
                              episode_snapshot=wrapper,
                              owned_episode_id=job.active_episode_id)


class TestJobPlanMutationAfterCaptureBlocksFinalization:
    """CAPTURE, then mutate the plan, then finalize — the real hazard order."""

    def test_a_clean_run_finalizes(self, data_root, repo):
        job = _real(repo)
        m = _finalize_with(job, _capture(job))
        assert m.coverage.status == "complete", m.coverage.problems

    def test_a_task_removed_after_capture_blocks(self, data_root, repo):
        job = _real(repo, _TWO)
        wrapper = _capture(job)
        job.tasks.pop()                                  # re-planned since capture
        with pytest.raises(ManifestError) as exc:
            _finalize_with(job, wrapper)
        assert "no longer matches" in str(exc.value)

    def test_a_task_added_after_capture_blocks(self, data_root, repo):
        from packages.orchestration.pingpong_job import TaskEntry
        job = _real(repo)
        wrapper = _capture(job)
        job.tasks.append(TaskEntry(task_id="T002", source_heading_number=2, title="new",
                                   body="b", acceptance="a"))
        with pytest.raises(ManifestError) as exc:
            _finalize_with(job, wrapper)
        assert "no longer matches" in str(exc.value)

    def test_tasks_reordered_after_capture_block(self, data_root, repo):
        job = _real(repo, _TWO)
        wrapper = _capture(job)
        job.tasks.reverse()
        with pytest.raises(ManifestError) as exc:
            _finalize_with(job, wrapper)
        assert "no longer matches" in str(exc.value)

    def test_a_task_renamed_after_capture_blocks(self, data_root, repo):
        job = _real(repo)
        wrapper = _capture(job)
        job.tasks[0].task_id = "T042"
        with pytest.raises(ManifestError) as exc:
            _finalize_with(job, wrapper)
        assert "no longer matches" in str(exc.value)
