"""F1/F2/F16 — corrupt disk state becomes a typed CLI integrity Exit 1, never a traceback."""
from __future__ import annotations

import contextlib
import io
import json
import os
import subprocess

import pytest

from apps.cli.commands import job_rerun_cmd as CMD
from packages.orchestration.pingpong_job import (
    job_evidence_dir,
    parse_job_file,
    run_job,
)
from packages.orchestration.run_manifest import (
    MANIFEST_INDEX_FILENAME,
    load_latest_manifest_for_cli,
)


@pytest.fixture
def data_root(tmp_path, monkeypatch):
    root = tmp_path / "remedy_data"; root.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    return root


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "repo"; r.mkdir()
    subprocess.run("git init -q && git config user.email t@t && git config user.name t "
                   "&& echo '# demo' > README.md && git add -A && git commit -qm init",
                   shell=True, cwd=r, check=True)
    return r


def _prov():
    from packages.orchestration.pingpong_provider import FakeProvider
    return FakeProvider(pass_on_round=1, fail_on_round=99)


@pytest.fixture
def finished(data_root, repo):
    job = parse_job_file("# Job: c\n\n## Task 1\nx\n\nAcceptance:\n- y\n", str(repo))
    run_job(job.job_id, builder_provider=_prov(), reviewer_provider=_prov(), repair_rounds=0)
    return job.job_id


def _run_cli(job_id, json_output=True):
    buf = io.StringIO()
    with pytest.raises(SystemExit) as exc:
        with contextlib.redirect_stdout(buf):
            CMD._cmd_job_rerun(job_id, check_manifest=True, json_output=json_output)
    return exc.value.code, buf.getvalue()


class TestTypedLoaderNeverThrows:
    def test_malformed_index_is_a_typed_integrity_error(self, finished):
        (job_evidence_dir(finished) / MANIFEST_INDEX_FILENAME).write_text("{bad")
        res = load_latest_manifest_for_cli(job_evidence_dir(finished), job_id=finished)
        assert res.kind == "integrity_error" and res.detail

    def test_unsupported_index_version_is_typed(self, finished):
        p = job_evidence_dir(finished) / MANIFEST_INDEX_FILENAME
        d = json.loads(p.read_text()); d["index_v"] = 99
        p.write_text(json.dumps(d))
        assert load_latest_manifest_for_cli(job_evidence_dir(finished),
                                            job_id=finished).kind == "integrity_error"

    def test_oversized_index_is_typed(self, finished):
        from packages.orchestration import manifest_schema as S
        p = job_evidence_dir(finished) / MANIFEST_INDEX_FILENAME
        p.write_text("x" * (S.MAX_INDEX_BYTES + 10))
        assert load_latest_manifest_for_cli(job_evidence_dir(finished),
                                            job_id=finished).kind == "integrity_error"

    def test_symlinked_index_is_typed(self, finished, tmp_path):
        p = job_evidence_dir(finished) / MANIFEST_INDEX_FILENAME
        elsewhere = tmp_path / "idx.json"; elsewhere.write_text("{}")
        p.unlink(); os.symlink(str(elsewhere), str(p))
        assert load_latest_manifest_for_cli(job_evidence_dir(finished),
                                            job_id=finished).kind == "integrity_error"

    def test_no_artifacts_at_all_is_legacy_no_manifest(self, data_root, repo):
        job = parse_job_file("# Job: n\n\n## Task 1\nx\n\nAcceptance:\n- y\n", str(repo))
        res = load_latest_manifest_for_cli(job_evidence_dir(job.job_id), job_id=job.job_id)
        assert res.kind == "no_manifest"


class TestPublicCliExitsOne:
    def test_malformed_index_exits_1_json_without_traceback(self, finished):
        (job_evidence_dir(finished) / MANIFEST_INDEX_FILENAME).write_text("{bad")
        code, out = _run_cli(finished, json_output=True)
        assert code == 1
        assert "Traceback" not in out
        assert json.loads(out)["error"] == "manifest_integrity"

    def test_malformed_index_exits_1_human_without_traceback(self, finished, capsys):
        (job_evidence_dir(finished) / MANIFEST_INDEX_FILENAME).write_text("{bad")
        code, out = _run_cli(finished, json_output=False)
        assert code == 1 and "Traceback" not in out

    def test_partial_chain_is_integrity_not_no_manifest(self, finished):
        # mirror present, index removed → partial chain → integrity error, NOT no_manifest
        (job_evidence_dir(finished) / MANIFEST_INDEX_FILENAME).unlink()
        code, out = _run_cli(finished, json_output=True)
        assert code == 1
        assert json.loads(out)["error"] == "manifest_integrity"
