"""F12 — the writer strictly round-trips and enforces aggregate limits BEFORE publishing."""
from __future__ import annotations

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration import manifest_schema as S
from packages.orchestration.run_manifest import (
    MANIFESTS_SUBDIR,
    ManifestError,
    build_verified_manifest_tree,
    decode_run_manifest_v1,
    write_run_manifest,
)


def _many_calls(n):
    return tuple(T._call(task="T001", seq=i + 1,
                         role="builder" if i % 2 == 0 else "reviewer",
                         rnd=i + 1, kind="attempt", fp=f"p{i}")
                 for i in range(n))


class TestWriterRoundTrip:
    def test_writer_output_always_strict_decodes_and_roundtrips(self, tmp_path):
        ev = tmp_path / "ev"; ev.mkdir()
        path = write_run_manifest(ev, T._mk(episode_id="ep1", calls=_many_calls(6)), root=ev)
        raw = path.read_bytes()
        decoded = decode_run_manifest_v1(raw)               # strict decode of the exact bytes
        from packages.common import secure_fs as _fs
        assert _fs.json_bytes(decoded.to_json(), sort_keys=True) == raw

    def test_a_written_episode_is_always_exportable(self, tmp_path):
        ev = tmp_path / "ev"; ev.mkdir()
        write_run_manifest(ev, T._mk(episode_id="ep1", calls=_many_calls(8)), root=ev)
        files, problems = build_verified_manifest_tree(ev, job_id="j")
        assert problems == [], "the writer published what the exporter refuses"
        assert files


class TestAggregateLimitsBeforeWrite:
    def test_oversized_episode_is_rejected_before_any_write(self, tmp_path, monkeypatch):
        # Shrink the episode ceiling so a legitimately-shaped record exceeds it: the writer must
        # refuse BEFORE creating an immutable episode the canonical reader would reject.
        monkeypatch.setattr(S, "MAX_EPISODE_MANIFEST_BYTES", 2000)
        ev = tmp_path / "ev"; ev.mkdir()
        with pytest.raises(ManifestError, match="canonical limit"):
            write_run_manifest(ev, T._mk(episode_id="ep1", calls=_many_calls(30)), root=ev)
        assert not (ev / MANIFESTS_SUBDIR).exists() or \
            not any((ev / MANIFESTS_SUBDIR).iterdir()), "a partial episode was published"

    def test_oversized_tree_is_rejected_before_publication(self, tmp_path, monkeypatch):
        monkeypatch.setattr(S, "MAX_TREE_BYTES", 3000)
        ev = tmp_path / "ev"; ev.mkdir()
        with pytest.raises(ManifestError, match="manifest tree"):
            write_run_manifest(ev, T._mk(episode_id="ep1", calls=_many_calls(20)), root=ev)

    def test_oversized_single_artifact_is_rejected_before_write(self, tmp_path, monkeypatch):
        monkeypatch.setattr(S, "MAX_CALL_ARTIFACT_BYTES", 200)
        ev = tmp_path / "ev"; ev.mkdir()
        with pytest.raises(ManifestError, match="call artifact"):
            write_run_manifest(ev, T._mk(episode_id="ep1"), root=ev)

    def test_many_individually_valid_calls_still_publish_within_limits(self, tmp_path):
        ev = tmp_path / "ev"; ev.mkdir()
        write_run_manifest(ev, T._mk(episode_id="ep1", calls=_many_calls(40)), root=ev)
        files, problems = build_verified_manifest_tree(ev, job_id="j")
        assert problems == []
        assert len([r for r in files if "/calls/" in r]) == 40
