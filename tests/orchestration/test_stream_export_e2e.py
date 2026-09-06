"""F004 Finding 7 — raw stream artifacts survive the whole evidence pipeline.

Internal job storage -> ``do job-evidence`` export -> final review ZIP.

The stream files are copied verbatim (they were redacted at capture time and must
never be redacted twice), every copy is listed with its hash and size, the
artifact contract gate requires them when the run used ``--stream-evidence``, and
``make_review_zip.sh`` ships them under ``evidence/current``.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import zipfile
from pathlib import Path

import pytest

from packages.orchestration.artifact_contract_gate import build_artifact_contract_gate
from packages.orchestration.job_evidence import export_job_evidence
from packages.orchestration.pingpong_job import parse_job_file, run_job
from packages.orchestration.pingpong_provider import FakeProvider

REPO_ROOT = Path(__file__).resolve().parents[2]
MAKE_REVIEW_ZIP = REPO_ROOT / "scripts" / "make_review_zip.sh"

_JOB = """# Job: Stream export

## Task 1
Add a test file.

Acceptance:
- file exists
"""

#: One builder call and one reviewer call, each with its own artifacts.
_CALLS = (
    "streams/builder/round-01/attempt-01",
    "streams/reviewer/round-01/attempt-01",
)

_RAW_LINE = '{"type":"result","usage":{"input_tokens":10,"output_tokens":5}}\n'
_EVENT_LINE = (
    '{"seq":1,"event_type":"result","raw_line_number":1,'
    '"raw_byte_offset":0,"raw_byte_length":63}\n'
)


@pytest.fixture
def isolate_data_root(tmp_path: Path, monkeypatch) -> Path:
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


def _git(repo: Path, *args) -> str:
    return subprocess.run(
        ["git", *args], cwd=repo, check=True, capture_output=True, text=True).stdout.strip()


@pytest.fixture
def demo_repo(tmp_path: Path) -> Path:
    # A REAL git worktree: a committed base, then a HEAD commit whose diff is exactly docs/README.md
    # — the file FakeProvider's builder authoritatively "changes". So the exported bundle is
    # internally consistent: the review subject, the content proof (full 40-hex base/head commits, a
    # requirement the packaging pipeline enforces), final_verifier authoritative_changed_files and the
    # change-provenance covered_files all resolve to the SAME authority set {docs/README.md}.
    repo = tmp_path / "repo"
    (repo / "src").mkdir(parents=True)
    (repo / "README.md").write_text("# Demo\n")
    (repo / "src" / "main.py").write_text("def hello():\n    return 'hello'\n")
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True, capture_output=True)
    _git(repo, "config", "user.email", "demo@example.test")
    _git(repo, "config", "user.name", "Demo")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "base")
    (repo / "docs").mkdir(parents=True)
    (repo / "docs" / "README.md").write_text("# docs\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "change docs/README.md")
    return repo


def _plant_stream_evidence(job) -> tuple[str, list[str]]:
    """Write per-call stream artifacts exactly where a streamed run leaves them.

    Also records the refs in the persisted run result, which is what the export
    reads to build ``provider_evidence.json``.
    """
    from packages.orchestration.data_paths import jobs_dir, pingpong_run_dir

    task = job.tasks[0]
    task_dir = jobs_dir() / job.job_id / "evidence" / "task_runs" / task.task_id

    refs: list[str] = []
    for call in _CALLS:
        call_dir = task_dir / call
        call_dir.mkdir(parents=True, exist_ok=True)
        (call_dir / "raw_stream.jsonl").write_text(_RAW_LINE, encoding="utf-8")
        (call_dir / "run_events.jsonl").write_text(_EVENT_LINE, encoding="utf-8")
        refs += [f"{call}/raw_stream.jsonl", f"{call}/run_events.jsonl"]

    result_file = pingpong_run_dir(task.run_id) / "result.json"
    data = json.loads(result_file.read_text())
    pe = dict(data.get("provider_evidence") or {})
    pe["stream_evidence_present"] = True
    pe["stream_artifact_refs"] = refs
    data["provider_evidence"] = pe
    result_file.write_text(json.dumps(data), encoding="utf-8")

    return task.task_id, refs


def _completed_job(demo_repo: Path):
    job = parse_job_file(_JOB, str(demo_repo))
    return run_job(
        job.job_id,
        builder_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
        reviewer_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
        repair_rounds=0,
    )


class TestStreamArtifactsSurviveExport:
    def test_export_copies_every_stream_artifact_verbatim(
        self, isolate_data_root, demo_repo, tmp_path,
    ):
        job = _completed_job(demo_repo)
        task_id, refs = _plant_stream_evidence(job)

        out = tmp_path / "evidence_out"
        export_job_evidence(job.job_id, str(out))

        for ref in refs:
            copied = out / "task_runs" / task_id / ref
            assert copied.is_file(), f"{ref} missing from exported bundle"

        raw = out / "task_runs" / task_id / _CALLS[0] / "raw_stream.jsonl"
        assert raw.read_text(encoding="utf-8") == _RAW_LINE, "stream bytes were altered"

    def test_builder_and_reviewer_artifacts_stay_distinct(
        self, isolate_data_root, demo_repo, tmp_path,
    ):
        job = _completed_job(demo_repo)
        task_id, _ = _plant_stream_evidence(job)
        out = tmp_path / "evidence_out"
        export_job_evidence(job.job_id, str(out))

        base = out / "task_runs" / task_id
        builder = base / _CALLS[0] / "raw_stream.jsonl"
        reviewer = base / _CALLS[1] / "raw_stream.jsonl"
        assert builder.is_file() and reviewer.is_file()
        assert builder.parent != reviewer.parent

    def test_listing_records_hash_and_size_of_each_artifact(
        self, isolate_data_root, demo_repo, tmp_path,
    ):
        job = _completed_job(demo_repo)
        task_id, refs = _plant_stream_evidence(job)
        out = tmp_path / "evidence_out"
        export_job_evidence(job.job_id, str(out))

        listing = json.loads(
            (out / "task_runs" / task_id / "stream_artifacts.json").read_text()
        )
        artifacts = listing["artifacts"]
        assert len(artifacts) == len(refs)

        for rel, meta in artifacts.items():
            data = (out / rel).read_bytes()
            assert meta["sha256"] == hashlib.sha256(data).hexdigest()
            assert meta["size_bytes"] == len(data)

    def test_symlinked_stream_file_is_not_copied(
        self, isolate_data_root, demo_repo, tmp_path,
    ):
        from packages.orchestration.data_paths import jobs_dir

        job = _completed_job(demo_repo)
        task_id, _ = _plant_stream_evidence(job)

        secret = tmp_path / "outside_secret.jsonl"
        secret.write_text('{"token":"REAL"}\n', encoding="utf-8")
        link_dir = (
            jobs_dir() / job.job_id / "evidence" / "task_runs" / task_id
            / "streams" / "builder" / "round-01" / "attempt-02"
        )
        link_dir.mkdir(parents=True)
        (link_dir / "raw_stream.jsonl").symlink_to(secret)

        out = tmp_path / "evidence_out"
        export_job_evidence(job.job_id, str(out))

        escaped = out / "task_runs" / task_id / "streams/builder/round-01/attempt-02/raw_stream.jsonl"
        assert not escaped.exists(), "a symlinked stream file escaped into the bundle"


class TestArtifactContractOverExportedBundle:
    def test_gate_passes_when_streams_are_exported(
        self, isolate_data_root, demo_repo, tmp_path,
    ):
        job = _completed_job(demo_repo)
        _plant_stream_evidence(job)
        out = tmp_path / "evidence_out"
        export_job_evidence(job.job_id, str(out))

        streams = build_artifact_contract_gate(str(out))["stream_artifacts"]
        assert streams["applicable"] is True
        assert streams["verdict"] == "PASS", streams
        assert streams["artifacts_present"] == len(_CALLS) * 2

    def test_gate_blocks_when_an_exported_stream_is_deleted(
        self, isolate_data_root, demo_repo, tmp_path,
    ):
        job = _completed_job(demo_repo)
        task_id, _ = _plant_stream_evidence(job)
        out = tmp_path / "evidence_out"
        export_job_evidence(job.job_id, str(out))

        (out / "task_runs" / task_id / _CALLS[1] / "raw_stream.jsonl").unlink()

        gate = build_artifact_contract_gate(str(out))
        assert gate["verdict"] == "BLOCKED"
        assert gate["stream_artifacts"]["missing_stream_artifacts"]


@pytest.mark.skipif(
    shutil.which("git") is None or shutil.which("bash") is None or shutil.which("zip") is None,
    reason="git, bash and zip required",
)
class TestStreamArtifactsReachTheReviewZip:
    def test_final_zip_contains_streams_under_evidence_current(
        self, isolate_data_root, demo_repo, tmp_path,
    ):
        job = _completed_job(demo_repo)
        task_id, refs = _plant_stream_evidence(job)

        exported = tmp_path / "evidence_out"
        base = _git(demo_repo, "rev-parse", "HEAD~1")
        export_job_evidence(job.job_id, str(exported), declared_base=base)

        # A minimal repository holding the real script and the exported bundle.
        repo = tmp_path / "ziprepo"
        (repo / "scripts").mkdir(parents=True)
        shutil.copy2(MAKE_REVIEW_ZIP, repo / "scripts" / "make_review_zip.sh")
        # Every helper make_review_zip.sh invokes (transitively) — the pipeline now stages, indexes,
        # builds the manifest, and packages the ZIP across four separate scripts. A missing one aborts
        # the run, so copy the complete set (the packages/ tree resolves via the EXPLICIT PYTHONPATH
        # set on the child below, never inherited outer-shell state).
        for helper in ("select_review_evidence.py", "stage_review_evidence.py",
                       "build_observability_index.py", "build_review_manifest.py",
                       "build_review_zip.py"):
            src = MAKE_REVIEW_ZIP.parent / helper
            assert src.exists(), f"missing pipeline helper in the real repo: {helper}"
            shutil.copy2(src, repo / "scripts" / helper)
        (repo / "README.md").write_text("# tmp\n")
        # The authoritative source file the bundle proves (docs/README.md) is packaged from THIS repo
        # and its bytes are verified against the content-proof hash, so it must be present verbatim.
        (repo / "docs").mkdir(parents=True)
        (repo / "docs" / "README.md").write_text("# docs\n")
        subprocess.run(["git", "init", "-q"], cwd=repo, check=True, capture_output=True)
        subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)

        ev_dir = repo / "remedy-job-evidence-stream"
        shutil.copytree(exported, ev_dir)

        # F5 (round 29): the mini repository deliberately isolates the PACKAGING scripts but not the
        # `packages/` tree, so the copied pipeline imports the Remedy package code from the repository
        # under test through an INTENTIONAL PYTHONPATH — never accidental inherited outer-shell state.
        # Start from a CLEARED path so the child environment is fully explicit and reproducible.
        import os
        env = os.environ.copy()
        env.pop("PYTHONPATH", None)
        env["PYTHONPATH"] = str(REPO_ROOT)

        proc = subprocess.run(
            ["bash", "scripts/make_review_zip.sh", "--evidence-dir", str(ev_dir)],
            cwd=repo, capture_output=True, text=True, timeout=120, env=env,
        )
        assert proc.returncode == 0, proc.stdout + proc.stderr

        zips = sorted(repo.glob("remedy-review-*.zip"))
        assert zips, f"no review zip produced: {proc.stdout}"

        with zipfile.ZipFile(zips[-1]) as zf:
            names = zf.namelist()
            for ref in refs:
                want = f"evidence/current/task_runs/{task_id}/{ref}"
                assert any(n.endswith(want) for n in names), f"{want} missing from {zips[-1].name}"

            raw = next(
                n for n in names
                if n.endswith(f"evidence/current/task_runs/{task_id}/{_CALLS[0]}/raw_stream.jsonl")
            )
            assert zf.read(raw).decode("utf-8") == _RAW_LINE
