"""F012 hardening round 3 — the integrity matrix.

The strict validators, the index trust chain, anchored evidence traversal, immutable-artifact
conflict, complete job-input identity, Remedy/target worktree content identity and the strict
Git collector — each in its own readable class. Fixtures live only in temporary directories.
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

from packages.orchestration.call_identity import CallIdentity
from packages.orchestration.job_evidence import export_job_evidence
from packages.orchestration.pingpong_job import (
    job_evidence_dir,
    parse_job_file,
    run_job,
)
from packages.orchestration.pingpong_provider import FakeProvider
from packages.orchestration.run_manifest import (
    GIT_INCOMPLETE,
    GIT_OK,
    MANIFEST_FILENAME,
    MANIFEST_INDEX_FILENAME,
    MANIFESTS_SUBDIR,
    FinalizedCall,
    ManifestConflictError,
    ManifestError,
    build_job_input_definition,
    build_run_manifest,
    load_latest_manifest_verified,
    read_run_manifest,
    validate_index_and_tree,
    validate_run_manifest,
    worktree_identity,
    write_run_manifest,
)


def _git(repo, cmd):
    subprocess.run(cmd, shell=True, cwd=repo, check=True, capture_output=True)


def _git_repo(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    _git(path, "git init -q && git config user.email t@t && git config user.name t "
               "&& printf one > a.txt && git add -A && git commit -qm init")
    return path


@pytest.fixture
def data_root(tmp_path, monkeypatch):
    root = tmp_path / "remedy_data"
    root.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    return root


@pytest.fixture
def repo(tmp_path):
    return _git_repo(tmp_path / "repo")


def _prov():
    return FakeProvider(pass_on_round=1, fail_on_round=99)


_JOB = "# Job: F012\n\n## Task 1\nDo a thing.\n\nAcceptance:\n- done\n"


def _finished(repo):
    job = parse_job_file(_JOB, str(repo))
    run_job(job.job_id, builder_provider=_prov(), reviewer_provider=_prov(), repair_rounds=0)
    return job.job_id, job_evidence_dir(job.job_id)


def _export_ok(job_id, tmp):
    out = export_job_evidence(job_id, str(tmp))
    return json.loads((Path(out["out_dir"]) / "manifest_integrity.json").read_text())["ok"]


# ---------------------------------------------------------------------------
# F3 — strict Git worktree content collector
# ---------------------------------------------------------------------------

class TestStrictGitCollector:
    def test_git_diff_failure_never_equals_clean(self, repo, monkeypatch):
        import packages.orchestration.run_manifest as RM
        clean = worktree_identity(str(repo))
        real = RM._git_bytes
        monkeypatch.setattr(RM, "_git_bytes", lambda rp, args, timeout=15:
                            (False, b"", "forced") if args[0] == "diff"
                            else real(rp, args, timeout=timeout))
        wf = worktree_identity(str(repo))
        assert wf.status == GIT_INCOMPLETE and wf.digest != clean.digest

    def test_git_timeout_never_equals_clean(self, repo, monkeypatch):
        import packages.orchestration.run_manifest as RM
        clean = worktree_identity(str(repo))
        real = RM._git_bytes
        monkeypatch.setattr(RM, "_git_bytes", lambda rp, args, timeout=15:
                            (False, b"", "git diff timed out") if args[0] == "diff"
                            else real(rp, args, timeout=timeout))
        wt = worktree_identity(str(repo))
        assert wt.status == GIT_INCOMPLETE and wt.digest != clean.digest

    def test_untracked_symlink_hashes_link_text_not_target(self, repo, tmp_path):
        secret = tmp_path / "secret"
        secret.write_text("SECRET-A")
        os.symlink(str(secret), str(repo / "link"))
        d1 = worktree_identity(str(repo)).digest
        secret.write_text("SECRET-B")                 # external target content change
        assert worktree_identity(str(repo)).digest == d1      # identity unchanged

    def test_changing_symlink_text_changes_identity(self, repo, tmp_path):
        os.symlink(str(tmp_path / "one"), str(repo / "link"))
        d1 = worktree_identity(str(repo)).digest
        (repo / "link").unlink()
        os.symlink(str(tmp_path / "two"), str(repo / "link"))
        assert worktree_identity(str(repo)).digest != d1

    def test_fifo_does_not_hang(self, repo):
        os.mkfifo(str(repo / "fifo"))
        wt = worktree_identity(str(repo))              # must return, not hang
        assert wt.status in (GIT_OK, GIT_INCOMPLETE)

    def test_no_absolute_path_in_identity(self, repo, tmp_path):
        os.symlink(str(tmp_path / "x"), str(repo / "link"))
        wt = worktree_identity(str(repo))
        assert str(tmp_path) not in json.dumps(wt.to_json())


# ---------------------------------------------------------------------------
# F1 — complete job-input definition
# ---------------------------------------------------------------------------

class TestCompleteJobInput:
    def _defn(self, job):
        return build_job_input_definition(job)

    def test_max_rounds_change_moves_the_definition(self, data_root, repo):
        job = parse_job_file(_JOB, str(repo))
        run_job(job.job_id, builder_provider=_prov(), reviewer_provider=_prov(),
                repair_rounds=0, max_rounds=3)
        from packages.orchestration.pingpong_job import load_job_plan
        m = read_run_manifest(job_evidence_dir(job.job_id) / MANIFEST_FILENAME)
        base = m.job_input_sha256
        j2 = load_job_plan(job.job_id)
        j2.execution_config.max_rounds = 99
        from packages.orchestration.run_manifest import job_input_sha256
        assert job_input_sha256(j2) != base

    def test_test_command_secret_is_hashed_not_serialized(self, repo):
        job = parse_job_file(_JOB, str(repo))
        from packages.orchestration.pingpong_job import ExecutionConfig
        job.execution_config = ExecutionConfig(test_command="pytest --token=SECRETXYZ")
        defn = build_job_input_definition(job)
        blob = json.dumps(defn)
        assert "SECRETXYZ" not in blob
        assert defn["execution"]["test_command"]["sha256"]     # still identity-bearing


# ---------------------------------------------------------------------------
# F7 — strict manifest validation
# ---------------------------------------------------------------------------

def _valid_manifest_bits():
    import tests.orchestration.test_run_manifest as T
    return T


class TestManifestValidation:
    def test_duplicate_call_identity_is_refused_by_writer(self, tmp_path):
        T = _valid_manifest_bits()
        dup = T._call(seq=1)
        m = T._mk(calls=(dup, dup))
        ev = tmp_path / "ev"
        ev.mkdir()
        with pytest.raises(ManifestError):
            write_run_manifest(ev, m, root=ev)

    def test_duplicate_call_identity_is_refused_by_reader(self, tmp_path):
        T = _valid_manifest_bits()
        m = T._mk()
        d = m.to_json()
        d["calls"] = d["calls"] + d["calls"]          # duplicate
        (tmp_path / MANIFEST_FILENAME).write_text(json.dumps(d))
        with pytest.raises(ManifestError):
            read_run_manifest(tmp_path / MANIFEST_FILENAME)

    def test_noncontiguous_sequence_is_invalid(self):
        T = _valid_manifest_bits()
        m = T._mk(calls=(T._call(seq=5),))
        assert any("contiguous" in p for p in validate_run_manifest(m))

    def test_complete_coverage_with_problems_is_invalid(self):
        from packages.orchestration.run_manifest import COVERAGE_COMPLETE, CallCoverage
        T = _valid_manifest_bits()
        m = T._mk(coverage=CallCoverage(status=COVERAGE_COMPLETE, problems=("x",)))
        assert any("coverage is complete yet declares problems" in p
                   for p in validate_run_manifest(m))

    def test_self_referential_prior_episode_is_invalid(self):
        T = _valid_manifest_bits()
        import dataclasses
        m = T._mk(episode_id="ep")
        m = dataclasses.replace(m, prior_episode_ids=("ep",))
        assert any("self reference" in p for p in validate_run_manifest(m))


# ---------------------------------------------------------------------------
# F8 — index trust chain
# ---------------------------------------------------------------------------

class TestIndexTrustChain:
    def test_tampered_index_hash_blocks(self, data_root, repo, tmp_path):
        job_id, ev = _finished(repo)
        idx = json.loads((ev / MANIFEST_INDEX_FILENAME).read_text())
        idx["episodes"][0]["record_sha256"] = "0" * 64
        (ev / MANIFEST_INDEX_FILENAME).write_text(json.dumps(idx))
        assert validate_index_and_tree(ev, job_id=job_id)
        assert _export_ok(job_id, tmp_path / "b") is False

    def test_index_status_mismatch_blocks(self, data_root, repo, tmp_path):
        job_id, ev = _finished(repo)
        idx = json.loads((ev / MANIFEST_INDEX_FILENAME).read_text())
        idx["episodes"][0]["status"] = "stopped"      # manifest says completed
        (ev / MANIFEST_INDEX_FILENAME).write_text(json.dumps(idx))
        assert validate_index_and_tree(ev, job_id=job_id)

    def test_extra_unindexed_episode_blocks(self, data_root, repo, tmp_path):
        import shutil
        job_id, ev = _finished(repo)
        m = read_run_manifest(ev / MANIFEST_FILENAME)
        shutil.copytree(ev / MANIFESTS_SUBDIR / m.episode_id,
                        ev / MANIFESTS_SUBDIR / "extra1234")
        assert any("unindexed" in p for p in validate_index_and_tree(ev, job_id=job_id))

    def test_missing_indexed_episode_blocks(self, data_root, repo, tmp_path):
        import shutil
        job_id, ev = _finished(repo)
        m = read_run_manifest(ev / MANIFEST_FILENAME)
        shutil.rmtree(ev / MANIFESTS_SUBDIR / m.episode_id)
        assert validate_index_and_tree(ev, job_id=job_id)

    def test_valid_tree_has_no_problems(self, data_root, repo):
        job_id, ev = _finished(repo)
        assert validate_index_and_tree(ev, job_id=job_id) == []


# ---------------------------------------------------------------------------
# F9 — anchored, symlink-refusing evidence reads
# ---------------------------------------------------------------------------

class TestAnchoredReads:
    def test_symlinked_run_manifests_blocks_without_outside_read(self, data_root, repo,
                                                                 tmp_path):
        import shutil
        job_id, ev = _finished(repo)
        outside = tmp_path / "outside"
        shutil.move(str(ev / MANIFESTS_SUBDIR), str(outside))
        os.symlink(str(outside), str(ev / MANIFESTS_SUBDIR))
        probs = validate_index_and_tree(ev, job_id=job_id)
        assert any("symlink" in p.lower() for p in probs)

    def test_symlinked_episode_dir_blocks(self, data_root, repo, tmp_path):
        import shutil
        job_id, ev = _finished(repo)
        m = read_run_manifest(ev / MANIFEST_FILENAME)
        real = ev / MANIFESTS_SUBDIR / m.episode_id
        outside = tmp_path / "ep_outside"
        shutil.move(str(real), str(outside))
        os.symlink(str(outside), str(real))
        assert validate_index_and_tree(ev, job_id=job_id)

    def test_no_fd_leak_on_repeated_validation(self, data_root, repo):
        job_id, ev = _finished(repo)
        before = len(os.listdir("/proc/self/fd"))
        for _ in range(30):
            validate_index_and_tree(ev, job_id=job_id)
        assert len(os.listdir("/proc/self/fd")) <= before + 1


# ---------------------------------------------------------------------------
# F10 — immutable artifact conflict
# ---------------------------------------------------------------------------

class TestImmutableArtifact:
    def test_tampered_existing_artifact_blocks_an_idempotent_write(self, tmp_path):
        T = _valid_manifest_bits()
        ev = tmp_path / "ev"
        ev.mkdir()
        m = T._mk(episode_id="epi",
                  calls=(T._call(seq=1, fp="fp1"),))
        write_run_manifest(ev, m, root=ev)
        # tamper the on-disk artifact, then re-issue the same episode
        art_dir = ev / MANIFESTS_SUBDIR / "epi" / "calls"
        art = next(art_dir.iterdir())
        art.write_text('{"tampered": true}')
        with pytest.raises(ManifestError):
            write_run_manifest(ev, m, root=ev)


# ---------------------------------------------------------------------------
# F11 — canonical loader + CLI integrity exit
# ---------------------------------------------------------------------------

class TestCanonicalLoader:
    def test_valid_latest_loads(self, data_root, repo):
        job_id, ev = _finished(repo)
        m = load_latest_manifest_verified(ev, job_id=job_id)
        assert m.status == "completed"

    def test_inconsistent_tree_raises(self, data_root, repo):
        job_id, ev = _finished(repo)
        idx = json.loads((ev / MANIFEST_INDEX_FILENAME).read_text())
        idx["episodes"][0]["record_sha256"] = "0" * 64
        (ev / MANIFEST_INDEX_FILENAME).write_text(json.dumps(idx))
        with pytest.raises(ManifestError):
            load_latest_manifest_verified(ev, job_id=job_id)

    def test_cli_refuses_inconsistent_tree_with_exit_1(self, data_root, repo):
        from apps.cli.commands import job_rerun_cmd as CMD
        job_id, ev = _finished(repo)
        (ev / MANIFEST_FILENAME).write_text(json.dumps(
            {**json.loads((ev / MANIFEST_FILENAME).read_text()),
             "job_input_sha256": "0" * 64}))
        with pytest.raises(SystemExit) as exc:
            CMD._cmd_job_rerun(job_id, check_manifest=True, json_output=True)
        assert exc.value.code == 1


# ---------------------------------------------------------------------------
# F6 — F010 and F012 consume the exact same finalized-call context (no re-sequence)
# ---------------------------------------------------------------------------

class TestSharedContextNoResequence:
    def test_f010_and_f012_same_identity_and_sequence(self, data_root, repo):
        from packages.orchestration.pingpong_job import parse_job_file, run_job
        from packages.orchestration.pingpong_loop import load_run
        from packages.orchestration.pingpong_provider import FakeProvider

        job = parse_job_file(_JOB, str(repo))
        res = run_job(job.job_id,
                      builder_provider=FakeProvider(builder_error="provider_unavailable: x"),
                      reviewer_provider=_prov(), repair_rounds=0)
        run = load_run(res.tasks[0].run_id)
        fc = [c for c in run["finalized_calls"] if c["identity"]["role"] == "builder"]
        assert len(fc) == 1
        seq = fc[0]["identity"]["sequence"]
        call_id = fc[0]["identity"]["call_id"]
        assert seq == 1                                # F010 did not advance the sequence
        # F010's post-mortem references the very same call id
        assert any(call_id in p for p in run.get("postmortem_paths", []))
        # no duplicate sequence in the run's finalized calls
        seqs = [c["identity"]["sequence"] for c in run["finalized_calls"]]
        assert len(seqs) == len(set(seqs))
