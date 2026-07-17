"""F5 — the Evidence export validates FIRST and copies only the allowlisted verified bytes.

An undeclared call file, an unindexed episode directory, a secret canary in an extra file, or an
oversized extra file must never enter the exported bundle, and a valid tree must export
identically.
"""
from __future__ import annotations

import os
import subprocess

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration.run_manifest import (
    CALLS_SUBDIR,
    MANIFESTS_SUBDIR,
    MANIFEST_FILENAME,
    build_verified_manifest_tree,
    write_run_manifest,
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


def _episode(ev):
    ev.mkdir()
    write_run_manifest(ev, T._mk(episode_id="ep1"), root=ev)


class TestAllowlist:
    def test_valid_tree_exports_the_declared_set(self, tmp_path):
        ev = tmp_path / "ev"
        _episode(ev)
        files, problems = build_verified_manifest_tree(ev, job_id="j")
        assert problems == []
        assert MANIFEST_FILENAME in files
        assert any(r.endswith(f"/{MANIFEST_FILENAME}") and r.startswith(MANIFESTS_SUBDIR)
                   for r in files)

    def test_undeclared_call_file_is_not_copied(self, tmp_path):
        ev = tmp_path / "ev"
        _episode(ev)
        calls = ev / MANIFESTS_SUBDIR / "ep1" / CALLS_SUBDIR
        (calls / "SECRET_CANARY.txt").write_text("CANARY-SECRET-XYZ")
        files, problems = build_verified_manifest_tree(ev, job_id="j")
        assert not any("SECRET_CANARY" in r for r in files)
        assert not any(b"CANARY-SECRET-XYZ" in v for v in files.values())
        assert any("undeclared call artifacts" in p for p in problems)

    def test_unindexed_episode_dir_is_not_copied(self, tmp_path):
        ev = tmp_path / "ev"
        _episode(ev)
        rogue = ev / MANIFESTS_SUBDIR / "rogue_ep"
        rogue.mkdir()
        (rogue / MANIFEST_FILENAME).write_text('{"secret":"leak"}')
        files, problems = build_verified_manifest_tree(ev, job_id="j")
        assert not any("rogue_ep" in r for r in files)
        assert not any(b"leak" in v for v in files.values())
        assert any("unindexed episode" in p for p in problems)

    def test_oversized_extra_file_is_not_read(self, tmp_path):
        ev = tmp_path / "ev"
        _episode(ev)
        big = ev / MANIFESTS_SUBDIR / "ep1" / CALLS_SUBDIR / "HUGE.bin"
        big.write_bytes(b"\0" * (9 * 1024 * 1024))       # > the 8 MiB per-file ceiling
        files, problems = build_verified_manifest_tree(ev, job_id="j")
        # the allowlist reads only DECLARED artifacts, so the huge extra is never read/copied
        assert not any("HUGE.bin" in r for r in files)
        assert any("undeclared call artifacts" in p for p in problems)


class TestFullExportCopiesNothingWhenDirty:
    def test_canary_never_enters_the_bundle(self, tmp_path, data_root, repo):
        from packages.orchestration.job_evidence import export_job_evidence
        from packages.orchestration.pingpong_job import (
            job_evidence_dir,
            parse_job_file,
            run_job,
        )
        from packages.orchestration.pingpong_provider import FakeProvider

        job = parse_job_file("# Job: e\n\n## Task 1\nx\n\nAcceptance:\n- y\n", str(repo))
        run_job(job.job_id, builder_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
                reviewer_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
                repair_rounds=0)
        ev = job_evidence_dir(job.job_id)
        eid = next((ev / MANIFESTS_SUBDIR).iterdir()).name
        (ev / MANIFESTS_SUBDIR / eid / CALLS_SUBDIR / "EXTRA_SECRET.txt").write_text("CANARY99")

        out = tmp_path / "bundle"
        out.mkdir()
        export_job_evidence(job.job_id, str(out))

        leaked = []
        for root, _dirs, fnames in os.walk(out):
            for fn in fnames:
                p = os.path.join(root, fn)
                if fn == "EXTRA_SECRET.txt":
                    leaked.append(p)
                    continue
                try:
                    if b"CANARY99" in open(p, "rb").read():
                        leaked.append(p)
                except OSError:
                    pass
        assert leaked == [], f"canary leaked into bundle: {leaked}"
