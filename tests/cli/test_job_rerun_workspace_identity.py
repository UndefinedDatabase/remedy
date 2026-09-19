"""F8 (round 12) — ONE canonical workspace identity format.

The reference recorded a 40-hex git TREE OBJECT in `episode_start_workspace_tree`; the candidate
recorded a 64-hex content DIGEST in the same field; and the logical projection compared the field
directly. So an otherwise identical workspace produced blocking drift and different logical
hashes — two different kinds of thing had been sharing one field name.

Only one of them can be recomputed read-only (computing a git tree WRITES objects — see F11,
round 11), so that is the one the identity uses: the typed `episode_start_workspace_identity`.
`episode_start_workspace_tree` stays as provenance and is never the comparison.
"""
from __future__ import annotations

import subprocess

import pytest

from packages.orchestration.pingpong_job import (
    _persist_job,
    job_evidence_dir,
    load_job_plan,
    parse_job_file,
    run_job,
)
from packages.orchestration.run_manifest import (
    load_latest_manifest_verified,
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


_JOB = "# Job: id\n\n## Task 1\nx\n\nAcceptance:\n- y\n"


@pytest.fixture
def live(data_root, repo):
    """A finished job pointed at a REAL live workspace under the canonical root."""
    job = parse_job_file(_JOB, str(repo))
    run_job(job.job_id, builder_provider=_prov(), reviewer_provider=_prov(), repair_rounds=0)
    j = load_job_plan(job.job_id)
    ref = load_latest_manifest_verified(job_evidence_dir(j.job_id), job_id=j.job_id)
    ws = repo / ".remedy-wt" / "job-live"
    ws.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "worktree", "add", "-q", "--detach", str(ws)], cwd=repo,
                   check=True, capture_output=True)
    j.job_workspace_path = str(ws)
    _persist_job(j)
    return load_job_plan(j.job_id), ref, ws


# --------------------------------------------------------------------------- one format


class TestOneCanonicalIdentityFormat:
    def test_the_logical_projection_carries_the_typed_identity(self, live):
        job, ref, _ws = live
        proj = ref.logical_input_projection()
        assert "episode_start_workspace_identity" in proj
        assert "episode_start_workspace_tree" not in proj
