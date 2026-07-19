"""F1 (round 34) — the REAL shell publishes exactly ONCE, private `.part` → status-bearing final path,
with NO public intermediate ZIP. Proven against the real ``make_review_zip.sh`` (not only the
``publish_atomically`` primitive): a foreign file at either possible public path is never deleted or
altered; concurrent shell invocations forced to the same timestamp produce exactly one published ZIP;
the published bytes equal the coordinator's verified SHA-256; and the shell source contains no
``rm``/``mv``/second-publish of a public ZIP output.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import threading
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_review_authoritative_e2e import _build_repo, _git  # noqa: E402

pytestmark = pytest.mark.skipif(shutil.which("git") is None, reason="git required")

_STAMP = "20990101-010101"


def _force_date_bin(tmp_path: Path, stamp: str = _STAMP) -> Path:
    """A PATH-shadowing ``date`` that returns a fixed stamp for the script's timestamp call only."""
    b = tmp_path / "fakebin"
    b.mkdir(exist_ok=True)
    real = shutil.which("date") or "/usr/bin/date"
    (b / "date").write_text(
        "#!/usr/bin/env bash\n"
        f'if [[ "$1" == "+%Y%m%d-%H%M%S" ]]; then echo "{stamp}"; else exec "{real}" "$@"; fi\n')
    (b / "date").chmod(0o755)
    return b


def _make(repo: Path, tmp_path: Path, *, force_stamp: bool = True, extra_env: dict | None = None):
    env = {"PYTHONPATH": str(REPO_ROOT), **(extra_env or {})}
    if force_stamp:
        env["PATH"] = f"{_force_date_bin(tmp_path)}:{os.environ.get('PATH','')}"
    return subprocess.run(["bash", "scripts/make_review_zip.sh"], cwd=repo,
                          capture_output=True, text=True, timeout=180,
                          env={**os.environ, **env})


def _zips(repo: Path):
    return sorted(p.name for p in repo.glob("remedy-review-*.zip"))


class TestSingleShellPublication:
    def test_one_final_zip_no_public_intermediate(self, tmp_path):
        repo, _base, _head = _build_repo(tmp_path)
        proc = _make(repo, tmp_path)
        assert proc.returncode == 0, proc.stdout + proc.stderr
        zips = _zips(repo)
        assert len(zips) == 1, zips
        # The one ZIP is status-bearing; the status-less intermediate name never exists.
        assert zips[0] == f"remedy-review-{_STAMP}-NO_EVIDENCE.zip", zips
        assert not (repo / f"remedy-review-{_STAMP}.zip").exists()
        assert not list(repo.glob(".remedy_zip_*.part"))

    def test_published_sha_equals_coordinator_verified_sha(self, tmp_path):
        repo, _b, _h = _build_repo(tmp_path)
        proc = _make(repo, tmp_path)
        assert proc.returncode == 0, proc.stdout + proc.stderr
        result = json.loads([ln for ln in proc.stdout.splitlines()
                             if ln.strip().startswith("{") and "final_sha256" in ln][0])
        published = repo / result["final_path"]
        assert published.is_file()
        assert hashlib.sha256(published.read_bytes()).hexdigest() == result["final_sha256"]

    def test_foreign_intermediate_path_preserved(self, tmp_path):
        repo, _b, _h = _build_repo(tmp_path)
        foreign = repo / f"remedy-review-{_STAMP}.zip"          # the OLD public-intermediate name
        foreign.write_bytes(b"FOREIGN-INTERMEDIATE-BYTES")
        proc = _make(repo, tmp_path)
        assert proc.returncode == 0, proc.stdout + proc.stderr
        # The foreign file at the (now unused) intermediate path is byte-identical: never rm -f'd.
        assert foreign.read_bytes() == b"FOREIGN-INTERMEDIATE-BYTES"
        # The real publication went to the status-bearing final path.
        assert (repo / f"remedy-review-{_STAMP}-NO_EVIDENCE.zip").is_file()

    def test_foreign_final_path_preserved_and_blocks(self, tmp_path):
        repo, _b, _h = _build_repo(tmp_path)
        final = repo / f"remedy-review-{_STAMP}-NO_EVIDENCE.zip"
        final.write_bytes(b"FOREIGN-FINAL-BYTES")
        proc = _make(repo, tmp_path)
        assert proc.returncode != 0, proc.stdout
        assert final.read_bytes() == b"FOREIGN-FINAL-BYTES"     # never overwritten
        assert not list(repo.glob(".remedy_zip_*.part"))        # private temp cleaned

    def test_symlink_at_final_path_blocks_and_untouched(self, tmp_path):
        repo, _b, _h = _build_repo(tmp_path)
        target = repo / "real_target.bin"
        target.write_bytes(b"TARGET")
        link = repo / f"remedy-review-{_STAMP}-NO_EVIDENCE.zip"
        os.symlink(target, link)
        proc = _make(repo, tmp_path)
        assert proc.returncode != 0, proc.stdout
        assert link.is_symlink() and os.readlink(link) == str(target)
        assert target.read_bytes() == b"TARGET"

    def test_concurrent_same_timestamp_exactly_one_publishes(self, tmp_path):
        repo, _b, _h = _build_repo(tmp_path)
        results: dict[int, subprocess.CompletedProcess] = {}
        barrier = threading.Barrier(2)

        def worker(i):
            barrier.wait()
            results[i] = _make(repo, tmp_path)

        ts = [threading.Thread(target=worker, args=(i,)) for i in range(2)]
        for t in ts:
            t.start()
        for t in ts:
            t.join()
        final = repo / f"remedy-review-{_STAMP}-NO_EVIDENCE.zip"
        assert final.is_file()
        wins = sum(1 for r in results.values() if r.returncode == 0)
        # Exactly one wins the atomic link; the other is a controlled collision. (If they serialize so
        # fully that both see the same status, the loser still cannot overwrite — at most one exit 0.)
        assert wins == 1, {i: r.returncode for i, r in results.items()}
        assert not list(repo.glob(".remedy_zip_*.part"))


class TestShellSourceHasNoPublicIntermediate:
    def test_no_rm_mv_or_second_publish_of_a_public_zip(self):
        src = (REPO_ROOT / "scripts" / "make_review_zip.sh").read_text()
        # No deletion or rename of a ZIP output, and no status-less public intermediate name.
        assert 'rm -f "$OUT"' not in src
        assert 'mv "$OUT"' not in src
        assert 'mv -n' not in src
        assert 'remedy-review-${STAMP}.zip' not in src        # the old public-intermediate name
        # The shell performs no publication itself; the coordinator owns the single publication.
        assert "publish_atomically(" not in src
