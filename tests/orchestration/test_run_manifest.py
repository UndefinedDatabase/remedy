"""F012 (hardened) — the run-input manifest, episode model, snapshot, provider fingerprints.

Exact provider-transport fingerprints, unique per-call identity, start-time input snapshots,
current-state reconstruction, coverage states, and the shared F010/F012 call identity. Every
job here is a real fake-provider ping-pong run in a temporary data root; no provider
generation call is made.
"""
from __future__ import annotations

import json
import subprocess
import unittest.mock as mock
from pathlib import Path

import pytest

from packages.orchestration.call_identity import (
    CallIdentity,
    prepare_call_input,
    sha_text,
)
from packages.orchestration.run_manifest import (
    COVERAGE_COMPLETE,
    COVERAGE_INCOMPLETE,
    MANIFEST_FILENAME,
    REDACTED,
    UNAVAILABLE,
    CallCoverage,
    EpisodeInputSnapshotV1,
    FinalizedCall,
    InputSnapshot,
    ManifestConflictError,
    ManifestError,
    RunManifestV1,
    build_current_candidate,
    build_input_snapshot,
    build_run_manifest,
    diff_manifests,
    is_secret_key,
    probe_provider_version,
    read_run_manifest,
    write_run_manifest,
)


def _git_repo(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    subprocess.run("git init -q && git config user.email t@t && git config user.name t "
                   "&& echo '# demo' > README.md && git add -A && git commit -qm init",
                   shell=True, cwd=path, check=True)
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
    from packages.orchestration.pingpong_provider import FakeProvider
    return FakeProvider(pass_on_round=1, fail_on_round=99)


_JOB = "# Job: F012\n\n## Task 1\nDo a thing.\n\nAcceptance:\n- done\n"
_TWO = _JOB + "\n## Task 2\nDo another.\n\nAcceptance:\n- done\n"


def _run(job_text, repo, **kw):
    from packages.orchestration.pingpong_job import parse_job_file, run_job
    job = parse_job_file(job_text, str(repo))
    res = run_job(job.job_id, builder_provider=_prov(), reviewer_provider=_prov(),
                  repair_rounds=0, **kw)
    return job.job_id, res


def _manifest_of(job_id):
    from packages.orchestration.pingpong_job import job_evidence_dir
    return read_run_manifest(job_evidence_dir(job_id) / MANIFEST_FILENAME)


# ---------------------------------------------------------------------------
# synthetic full manifests
# ---------------------------------------------------------------------------

def _job_input(variant=""):
    """A COMPLETE, valid JobInputDefinitionV1 (F7) built from the real production builder, so the
    fixture can never drift from the exact material field set. ``variant`` changes the
    definition — and therefore its bound hash — the way a real input change would."""
    from packages.orchestration.pingpong_job import ExecutionConfig, TaskEntry
    from packages.orchestration.run_manifest import build_job_input_definition

    class _J:
        job_id = "j"
        job_title = "demo" + variant
        job_file_sha256 = "f" * 64
        isolation_mode = "worktree"
        execution_config = ExecutionConfig()
        tasks = [TaskEntry(task_id="T001", source_heading_number=1, title="t", body="b",
                           acceptance="a")]

    return build_job_input_definition(_J())


def _snap(**over):
    base = dict(
        remedy_git_sha="a" * 40, remedy_dirty=False,
        remedy_worktree={"status": "ok", "head": "a" * 40, "digest": "aa" * 32,
                         "problems": [], "dirty": False},
        target_base_commit="b" * 40,
        target_head="c" * 40, target_tree="d" * 64,
        target_worktree={"status": "ok", "head": "c" * 40, "digest": "dd" * 32,
                         "problems": [], "dirty": False},
        job_initial_tree="e" * 40, episode_start_workspace_tree="e" * 40,
        episode_start_workspace_identity={"status": "ok", "head": "c" * 40,
                                          "digest": "ee" * 32, "problems": [], "dirty": False},
        job_file_sha256="f" * 64, job_input=_job_input(),
        models={"builder": "fake", "reviewer": "fake"},
        provider_versions={"fake": UNAVAILABLE},
        config=[{"key": "ollama.model", "value": "qwen", "source": "default"}],
        environment=[{"key": "REMEDY_DATA_DIR", "value": "[path]"}],
        python_version="3.10", platform="Linux", pythonhashseed="")
    base.update(over)
    return InputSnapshot(**base)


def _wrap(input_snap=None, *, episode_id="ep", phase="episode_start",
          captured_at="2026-07-15T00:00:00+00:00", status="ok", problems=()):
    """Build an EpisodeInputSnapshotV1 wrapper around an InputSnapshot (F4)."""
    return EpisodeInputSnapshotV1(
        snapshot_v=1, episode_id=episode_id, captured_at=captured_at,
        capture_phase=phase, status=status, problems=tuple(problems),
        input=(input_snap if input_snap is not None else _snap()) if status == "ok" else None)


def _call(task="T001", seq=1, role="builder", rnd=1, kind="attempt", fp="fp1",
          episode_id="ep", run=None):
    """F7: the fingerprint is BOUND to the prepared input, so a test call carries a real
    PreparedCallInput. ``fp`` is the prompt seed — a different seed yields a different
    (correctly bound) fingerprint, which is exactly what the drift tests need.

    ``run`` names the owning run. Multi-episode chain fixtures pass a PER-EPISODE run id,
    because that is what production does: a resumed episode re-runs its task under a NEW run.
    (When one run legitimately spans episodes — a pre-work stop carrying prior history — its
    ledger carries the earlier entries too, and F5's continuity rule holds it to that.)
    """
    from packages.orchestration.call_identity import prepare_call_input
    prepared = prepare_call_input(prompt=fp, model="fake", mode="fake", options={})
    return FinalizedCall(
        identity=CallIdentity(job_id="j", task_id=task, run_id=run or ("r" + task), sequence=seq,
                              role=role, round=rnd, kind=kind, call_id=f"c{seq}",
                              episode_id=episode_id),
        fingerprint=prepared.fingerprint, prepared_input=prepared.to_json(),
        fingerprint_source="provider_transport", ok=True)


def _ledgers_for(calls, *, job_id="j"):
    """F1 (round 12): the canonical Run Call LEDGERS production now publishes. The fixture
    derives them from the same facts production does, so it cannot prove something production
    would not."""
    from packages.orchestration.run_manifest import CallLedgerEntryV1, RunCallLedgerV1

    by_run: dict[tuple, list] = {}
    for c in calls:
        by_run.setdefault((c.identity.task_id, c.identity.run_id), []).append(c)
    out = []
    for (tid, rid), cs in sorted(by_run.items()):
        entries = tuple(
            CallLedgerEntryV1(per_run_sequence=i, call_id=c.identity.call_id,
                              episode_id=c.identity.episode_id, role=c.identity.role,
                              round=c.identity.round, kind=c.identity.kind,
                              prepared_input_fingerprint=c.fingerprint, ok=c.ok)
            for i, c in enumerate(cs, start=1))
        out.append(RunCallLedgerV1(job_id=job_id, task_id=tid, run_id=rid,
                                   terminal_state="completed", complete=True, entries=entries))
    return tuple(out)


def _expectation(calls, *, job_input, phase=None, override=None, status="completed",
                 ledgers=()):
    """F6/F9: the self-contained expectation proof production embeds. The fixture DERIVES it from
    the same facts production does — the embedded task list and the calls this episode carries —
    so it cannot drift into proving something production wouldn't."""
    from packages.orchestration.run_manifest import (
        DISPATCH_NEVER, DISPATCH_THIS_EPISODE, EXPECT_EXECUTED, EXPECT_NOT_DISPATCHED,
        EXPECT_SKIPPED, PHASE_WORKED, CallExpectationV1, TaskCallExpectationV1,
    )
    if override is not None:
        return override
    counts: dict[str, int] = {}
    runs: dict[str, str] = {}
    for c in calls:
        counts[c.identity.task_id] = counts.get(c.identity.task_id, 0) + 1
        runs[c.identity.task_id] = c.identity.run_id
    by_task = {lg.task_id: lg for lg in ledgers}
    tasks = []
    for tk in job_input["tasks"]:
        tid = str(tk["task_id"])
        n = counts.get(tid, 0)
        lg = by_task.get(tid)
        if n and lg is not None:
            tasks.append(TaskCallExpectationV1(
                task_id=tid, expectation=EXPECT_EXECUTED, run_id=runs[tid],
                expected_call_count=n, observed_call_count=n,
                finalized_calls_sha256=lg.sha256(), ledger_ref=lg.ref(),
                task_status_at_finalization="applied_to_job_workspace",
                dispatch_state=DISPATCH_THIS_EPISODE))
        else:
            # F7 (round 11): a COMPLETED episode has every task applied or skipped, so a task
            # with no calls in one is `skipped`; only a stopped/planned episode can carry a task
            # that was never dispatched.
            tasks.append(TaskCallExpectationV1(
                task_id=tid,
                expectation=EXPECT_SKIPPED if status == "completed" else EXPECT_NOT_DISPATCHED,
                task_status_at_finalization="skipped" if status == "completed" else "pending",
                dispatch_state=DISPATCH_NEVER))
    return CallExpectationV1(episode_phase=phase or PHASE_WORKED, tasks=tuple(tasks))


def _zero_call_proof(job_input=None):
    """F6 (round 10): the proof a GENUINE zero-call episode carries — every declared task
    explicitly skipped, so "no calls" is a recorded fact rather than an absence of evidence.
    This is the contract's valid zero-call job ("a genuine zero-call (all-skipped) job ...
    stays valid and complete")."""
    from packages.orchestration.run_manifest import (
        EXPECT_SKIPPED, PHASE_WORKED, CallExpectationV1, TaskCallExpectationV1,
    )
    ji = job_input if job_input is not None else _job_input()
    return CallExpectationV1(
        episode_phase=PHASE_WORKED,
        tasks=tuple(TaskCallExpectationV1(task_id=str(tk["task_id"]),
                                          expectation=EXPECT_SKIPPED)
                    for tk in ji["tasks"]))


def _mk(*, episode_id="ep", job_input_variant="", calls=None, status="completed",
        coverage=None, snap=None, expectation=None, phase=None):
    if calls is None:
        calls = (_call(),)
    # re-stamp each call's episode_id to the manifest episode (validation requires agreement)
    calls = tuple(
        FinalizedCall(
            identity=CallIdentity(job_id=c.identity.job_id, task_id=c.identity.task_id,
                                  run_id=c.identity.run_id, sequence=c.identity.sequence,
                                  role=c.identity.role, round=c.identity.round,
                                  kind=c.identity.kind, call_id=c.identity.call_id,
                                  episode_id=episode_id),
            fingerprint=c.fingerprint, prepared_input=c.prepared_input,
            fingerprint_source=c.fingerprint_source, ok=c.ok, artifact=c.artifact,
            artifact_sha256=c.artifact_sha256)
        for c in calls)
    from packages.orchestration.run_manifest import job_input_definition_sha256
    snap = snap or _snap(job_input=_job_input(job_input_variant))
    return RunManifestV1(
        job_id="j", episode_id=episode_id, created_at="2026-07-15T00:00:00+00:00",
        status=status,
        episode_snapshot=_wrap(snap, episode_id=episode_id),
        job_input_sha256=job_input_definition_sha256(snap.job_input),   # F6 bound
        calls=tuple(calls), coverage=coverage or CallCoverage(status=COVERAGE_COMPLETE),
        call_expectation=_expectation(calls, job_input=snap.job_input, phase=phase,
                                      override=expectation, status=status,
                                      ledgers=_ledgers_for(calls)),
        call_ledgers=_ledgers_for(calls))


# ---------------------------------------------------------------------------
# F3 — provider-transport fingerprints via capturing transports
# ---------------------------------------------------------------------------

class TestProviderTransportFingerprints:
    def _fake_api(self, response_text='{"verdict":"pass","findings":[],'
                                      '"confidence":"high","summary":"ok"}'):
        captured: dict = {}

        class _Resp:
            class U:
                output_tokens = 5
            content = [type("B", (), {"text": response_text})()]
            usage = U()

        class _Client:
            class messages:
                @staticmethod
                def create(**kw):
                    captured.update(kw)
                    return _Resp()

        return _Client(), captured

    def test_claude_api_structured_fingerprint_matches_transport(self, monkeypatch):
        monkeypatch.delenv("REMEDY_REVIEWER_FREETEXT", raising=False)
        from packages.orchestration.pingpong_provider import ClaudeProvider

        p = ClaudeProvider(model="claude-x")
        client, captured = self._fake_api()
        p._client = client
        out = p.review("REVIEW", timeout_sec=5, max_output_chars=1000)
        sent = captured["messages"][0]["content"]
        assert out.prepared_input.mode == "api-structured"
        assert out.prepared_input.prompt_sha256 == sha_text(sent)
        assert out.prepared_input.prompt_len_bytes == len(sent.encode('utf-8'))
        assert len(sent) > len("REVIEW")

    def test_claude_api_legacy_fingerprint_matches_transport(self, monkeypatch):
        monkeypatch.setenv("REMEDY_REVIEWER_FREETEXT", "1")
        from packages.orchestration.pingpong_provider import ClaudeProvider

        p = ClaudeProvider(model="claude-x")
        client, captured = self._fake_api()
        p._client = client
        out = p.review("REVIEW", timeout_sec=5, max_output_chars=1000)
        sent = captured["messages"][0]["content"]
        assert out.prepared_input.mode == "api-legacy"
        assert out.prepared_input.prompt_sha256 == sha_text(sent)

    def test_claude_api_builder_fingerprint_matches_transport(self):
        from packages.orchestration.pingpong_provider import ClaudeProvider

        p = ClaudeProvider(model="claude-x")
        client, captured = self._fake_api(response_text="- docs/x.md\nchanged")
        p._client = client
        out = p.build("BUILD", timeout_sec=5, max_output_chars=1000)
        assert out.prepared_input.prompt_sha256 == sha_text(captured["messages"][0]["content"])

    def test_claude_cli_native_schema_fingerprint_includes_schema(self, monkeypatch):
        monkeypatch.delenv("REMEDY_REVIEWER_FREETEXT", raising=False)
        from packages.orchestration import pingpong_provider as PP
        from packages.orchestration.pingpong_provider import ClaudeCliProvider

        p = ClaudeCliProvider(model="claude-cli-x")
        monkeypatch.setattr(p, "_review_impl", lambda *a, **k: PP.ReviewerOutput(
            verdict="pass", provider="claude-cli"))
        out = p.review("REVIEW", timeout_sec=5, max_output_chars=1000)
        assert out.prepared_input.mode == "cli-native"
        assert out.prepared_input.schema_sha256
        assert out.prepared_input.prompt_sha256 == sha_text("REVIEW")

    def test_claude_cli_legacy_fingerprint_matches_sent_prompt(self, monkeypatch):
        monkeypatch.setenv("REMEDY_REVIEWER_FREETEXT", "1")
        from packages.orchestration import pingpong_provider as PP
        from packages.orchestration.pingpong_provider import (
            _REVIEWER_JSON_SCHEMA,
            ClaudeCliProvider,
        )

        p = ClaudeCliProvider(model="claude-cli-x")
        monkeypatch.setattr(p, "_review_impl", lambda *a, **k: PP.ReviewerOutput(
            verdict="pass", provider="claude-cli"))
        out = p.review("REVIEW", timeout_sec=5, max_output_chars=1000)
        assert out.prepared_input.mode == "cli-legacy"
        assert out.prepared_input.prompt_sha256 == sha_text(
            "REVIEW" + "\n\n" + _REVIEWER_JSON_SCHEMA)

    def test_fake_provider_carries_a_fingerprint(self):
        f = _prov()
        assert f.build("HELLO").prepared_input.prompt_sha256 == sha_text("HELLO")
        assert f.review("WORLD").prepared_input.prompt_sha256 == sha_text("WORLD")

    def test_prepare_call_input_covers_model_mode_schema_options(self):
        a = prepare_call_input(prompt="p", model="m", mode="x")
        b = prepare_call_input(prompt="p", model="m2", mode="x")
        c = prepare_call_input(prompt="p", model="m", mode="x", schema="s")
        d = prepare_call_input(prompt="p", model="m", mode="x", options={"k": 1})
        assert len({a.fingerprint, b.fingerprint, c.fingerprint, d.fingerprint}) == 4


# ---------------------------------------------------------------------------
# F5 — unique call identity
# ---------------------------------------------------------------------------

class TestUniqueCallIdentity:
    def test_every_call_in_a_two_task_job_is_unique(self, data_root, repo):
        job_id, _ = _run(_TWO, repo)
        m = _manifest_of(job_id)
        keys = m.call_keys()
        assert len(keys) == len(set(keys))
        assert len({c.identity.task_id for c in m.calls}) == 2

    def test_changing_one_of_two_same_role_calls_is_detected(self):
        ref = _mk(calls=(_call("T001", 1, fp="h1"), _call("T002", 2, fp="h2")))
        cand = _mk(calls=(_call("T001", 1, fp="h1"), _call("T002", 2, fp="CHANGED")))
        diff = diff_manifests(ref, cand)
        assert diff["same_inputs"] is False
        assert any(e["category"] == "prompt" for e in diff["blocking"])

    def test_reordered_calls_are_detected(self):
        a = _call("T001", 1, fp="h1")
        b = _call("T002", 2, role="reviewer", fp="h2")
        ref = _mk(calls=(a, b))
        # swap the sequence numbers so the ORDER differs (same fingerprints)
        a2 = FinalizedCall(identity=CallIdentity(job_id="j", task_id="T001", run_id="rT001",
                           sequence=2, role="builder", round=1, kind="attempt", call_id="c1"),
                           fingerprint="h1", prepared_input={}, fingerprint_source="x", ok=True)
        b2 = FinalizedCall(identity=CallIdentity(job_id="j", task_id="T002", run_id="rT002",
                           sequence=1, role="reviewer", round=1, kind="attempt", call_id="c2"),
                           fingerprint="h2", prepared_input={}, fingerprint_source="x", ok=True)
        cand = _mk(calls=(a2, b2))
        assert diff_manifests(ref, cand)["same_inputs"] is False

    def test_duplicate_call_identity_is_a_manifest_error(self, repo):
        fc = _call()

        class _Job:
            job_id = "j"
            repo_path = str(repo)
            job_file_sha256 = "e" * 64
            worktree_base_commit = worktree_head = job_initial_tree = ""
            tasks: list = []
            execution_config = None

        from packages.orchestration import run_manifest as RM
        # F6 (round 10): collection also returns the episode's expectation proof.
        # F1 (round 12): collection also returns the episode's canonical Run Call ledgers.
        with mock.patch.object(RM, "_collect_calls",
                               return_value=([fc, fc], [], RM.CallExpectationV1(), ())):
            with pytest.raises(ManifestError, match="duplicate"):
                build_run_manifest(_Job(), status="completed", episode_id="ep",
                                   created_at="t",
                                   episode_snapshot=_wrap(episode_id="ep"))

    def test_same_inputs_true_implies_logical_match(self):
        diff = diff_manifests(_mk(), _mk())
        assert diff["same_inputs"] is True and diff["logical_input_match"] is True


# ---------------------------------------------------------------------------
# F6/F10 — coverage
# ---------------------------------------------------------------------------

class TestCoverage:
    def test_check_candidate_is_incomplete_and_never_same(self, data_root, repo):
        job_id, _ = _run(_JOB, repo)
        from packages.orchestration.pingpong_job import load_job_plan
        ref = _manifest_of(job_id)
        cand = build_current_candidate(ref, load_job_plan(job_id))
        diff = diff_manifests(ref, cand)
        assert diff["verification_complete"] is False
        assert diff["same_inputs"] is None
        assert cand.coverage.status == COVERAGE_INCOMPLETE

    def test_two_complete_manifests_verify(self):
        diff = diff_manifests(_mk(), _mk())
        assert diff["verification_complete"] is True and diff["same_inputs"] is True

    def test_a_missing_run_record_is_a_coverage_problem(self, data_root, repo):
        job_id, _ = _run(_JOB, repo)
        from packages.orchestration.pingpong_job import load_job_plan
        job = load_job_plan(job_id)
        job.tasks[0].run_id = "deadbeefdeadbeef"
        # F1/F4: build_run_manifest never re-probes; the caller supplies the episode snapshot
        # WRAPPER, which must be a valid ok snapshot bound to this episode.
        m = build_run_manifest(job, status="completed", episode_id="ep2", created_at="t",
                               episode_snapshot=_wrap(
                                   build_input_snapshot(job, inspect_target=False,
                                                        probe_versions=False),
                                   episode_id="ep2"))
        assert m.coverage.status == COVERAGE_INCOMPLETE
        assert any("missing run record" in p for p in m.coverage.problems)

    def test_a_genuine_zero_call_job_is_complete(self, data_root, repo):
        from packages.orchestration.pingpong_job import (
            TASK_SKIPPED,
            _persist_job,
            parse_job_file,
            run_job,
        )
        job = parse_job_file(_JOB, str(repo))
        job.tasks[0].status = TASK_SKIPPED
        _persist_job(job)
        run_job(job.job_id, builder_provider=_prov(), reviewer_provider=_prov(),
                repair_rounds=0)
        m = _manifest_of(job.job_id)
        assert m.calls == () and m.coverage.status == COVERAGE_COMPLETE


# ---------------------------------------------------------------------------
# F12 — snapshot
# ---------------------------------------------------------------------------

class TestStartSnapshot:
    def test_snapshot_reflects_target_at_start(self, data_root, repo):
        m = _manifest_of(_run(_JOB, repo)[0])
        assert m.snapshot.target_head != UNAVAILABLE
        assert m.snapshot.target_tree != UNAVAILABLE
        assert m.snapshot.remedy_git_sha and m.snapshot.config

    def test_secret_config_and_env_are_redacted(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_ANTHROPIC_API_TOKEN", "CANARY-secret-1")
        monkeypatch.setenv("REMEDY_MY_SECRET_KEY", "CANARY-secret-2")

        class _Job:
            job_id = "j"
            repo_path = str(tmp_path)
            job_file_sha256 = "e" * 64
            worktree_base_commit = worktree_head = job_initial_tree = ""
            tasks: list = []
            execution_config = None

        snap = build_input_snapshot(_Job(), inspect_target=False, probe_versions=False)
        assert "CANARY-secret" not in json.dumps(snap.to_json())
        env = {e["key"]: e["value"] for e in snap.environment}
        assert env["REMEDY_MY_SECRET_KEY"] == REDACTED

    def test_is_secret_key(self):
        assert is_secret_key("api_token") and is_secret_key("db_password")
        assert not is_secret_key("ollama.model")


class TestVersionProbe:
    def test_fake_has_no_version_and_no_subprocess(self, monkeypatch):
        import subprocess as sp
        seen = []
        real = sp.run
        monkeypatch.setattr(sp, "run", lambda *a, **k: (seen.append(a), real(*a, **k))[1])
        assert probe_provider_version("fake") == UNAVAILABLE
        assert seen == []

    def test_path_stripped_probe_is_unavailable(self, monkeypatch):
        monkeypatch.setenv("PATH", "")
        assert probe_provider_version("claude-cli") == UNAVAILABLE


class TestEpisodeWrite:
    def test_completed_writes_episode_manifest_artifacts_and_index(self, data_root, repo):
        job_id, _ = _run(_JOB, repo)
        from packages.orchestration.pingpong_job import job_evidence_dir
        ev = job_evidence_dir(job_id)
        m = _manifest_of(job_id)
        ep = ev / "run_manifests" / m.episode_id
        assert (ep / "run_manifest.json").is_file()
        for c in m.calls:
            assert c.artifact and (ep / c.artifact).is_file()
            assert json.loads((ep / c.artifact).read_text())["fingerprint"] == c.fingerprint
        idx = json.loads((ev / "run_manifest_index.json").read_text())
        assert idx["latest_episode_id"] == m.episode_id

    def test_identical_second_write_is_idempotent(self, tmp_path):
        ev = tmp_path / "evidence"
        ev.mkdir()
        write_run_manifest(ev, _mk(episode_id="epi"), root=ev)
        write_run_manifest(ev, _mk(episode_id="epi"), root=ev)
        assert len(list((ev / "run_manifests").iterdir())) == 1

    def test_conflicting_same_episode_write_raises(self, tmp_path):
        ev = tmp_path / "evidence"
        ev.mkdir()
        write_run_manifest(ev, _mk(episode_id="epi"), root=ev)
        with pytest.raises(ManifestConflictError):
            write_run_manifest(ev, _mk(episode_id="epi", job_input_variant="conflict"), root=ev)

    def test_a_symlinked_root_is_refused(self, tmp_path):
        outside = tmp_path / "outside"
        outside.mkdir()
        (tmp_path / "real").mkdir()
        (tmp_path / "real" / "link").symlink_to(outside)
        with pytest.raises(ManifestError, match="symlink"):
            write_run_manifest(tmp_path / "real" / "link" / "e", _mk(),
                               root=tmp_path / "real" / "link" / "e")
        assert list(outside.iterdir()) == []

    def test_unsupported_version_refused_on_read(self, tmp_path):
        (tmp_path / MANIFEST_FILENAME).write_text(json.dumps({"manifest_v": 99}))
        with pytest.raises(ManifestError, match="unsupported"):
            read_run_manifest(tmp_path / MANIFEST_FILENAME)


# ---------------------------------------------------------------------------
# F11 — F010 and F012 share the call identity
# ---------------------------------------------------------------------------

class TestSharedCallIdentity:
    def test_failed_call_shares_identity_with_postmortem(self, data_root, repo):
        from packages.orchestration.pingpong_job import parse_job_file, run_job
        from packages.orchestration.pingpong_loop import load_run
        from packages.orchestration.pingpong_provider import FakeProvider

        job = parse_job_file(_JOB, str(repo))
        b = FakeProvider(builder_error="provider_unavailable: boom")
        res = run_job(job.job_id, builder_provider=b, reviewer_provider=_prov(),
                      repair_rounds=0)
        run = load_run(res.tasks[0].run_id)
        builder_calls = [c for c in run["finalized_calls"]
                         if c["identity"]["role"] == "builder"]
        assert builder_calls, "the failed builder call was recorded by F012"
        f012_call_id = builder_calls[0]["identity"]["call_id"]
        # F010's post-mortem for the same call used the same call id
        assert any(f012_call_id in p for p in run.get("postmortem_paths", []))


# ---------------------------------------------------------------------------
# Hardening round 2 — content digest, idempotent consistency, artifact/episode integrity
# ---------------------------------------------------------------------------

from packages.orchestration.run_manifest import (              # noqa: E402
    MANIFEST_INDEX_FILENAME,
    MANIFESTS_SUBDIR,
    read_index,
    target_tree,
)


def _g(repo, cmd):
    subprocess.run(cmd, shell=True, cwd=repo, check=True, capture_output=True)


class TestWorkingTreeContentDigest:
    def _repo(self, tmp_path):
        r = tmp_path / "t"
        r.mkdir()
        _g(r, "git init -q && git config user.email t@t && git config user.name t "
              "&& printf one > a.txt && git add -A && git commit -qm i")
        return r

    def test_clean_tree_is_stable(self, tmp_path):
        r = self._repo(tmp_path)
        assert target_tree(str(r)) == target_tree(str(r)) != UNAVAILABLE

    def test_dirty_content_a_to_b_changes_digest_with_same_porcelain(self, tmp_path):
        r = self._repo(tmp_path)
        (r / "a.txt").write_text("two")
        da = target_tree(str(r))
        (r / "a.txt").write_text("three")
        db = target_tree(str(r))
        porcelain = subprocess.run("git status --porcelain", shell=True, cwd=r,
                                   capture_output=True, text=True).stdout
        assert " M a.txt" in porcelain              # porcelain identical for both
        assert da != db                             # ...but content digest differs

    def test_staged_content_changes_digest(self, tmp_path):
        r = self._repo(tmp_path)
        (r / "a.txt").write_text("staged")
        _g(r, "git add a.txt")
        s1 = target_tree(str(r))
        (r / "a.txt").write_text("staged2")
        _g(r, "git add a.txt")
        assert target_tree(str(r)) != s1

    def test_untracked_content_changes_digest(self, tmp_path):
        r = self._repo(tmp_path)
        (r / "u.txt").write_text("u1")
        u1 = target_tree(str(r))
        (r / "u.txt").write_text("u2")
        assert target_tree(str(r)) != u1

    def test_deleted_file_changes_digest(self, tmp_path):
        r = self._repo(tmp_path)
        clean = target_tree(str(r))
        (r / "a.txt").unlink()
        assert target_tree(str(r)) != clean

    def test_filename_with_spaces_is_deterministic(self, tmp_path):
        r = self._repo(tmp_path)
        (r / "w s.txt").write_text("x")
        assert target_tree(str(r)) == target_tree(str(r))

    def test_non_repo_is_unavailable(self, tmp_path):
        assert target_tree(str(tmp_path / "nope")) == UNAVAILABLE


class TestIdempotentEpisodeConsistency:
    def test_refinalize_new_created_at_keeps_episode_root_index_consistent(self, tmp_path):
        import dataclasses
        ev = tmp_path / "ev"
        ev.mkdir()
        m = _mk(episode_id="epi")
        write_run_manifest(ev, m, root=ev)
        write_run_manifest(ev, dataclasses.replace(
            m, created_at="2099-01-01T00:00:00+00:00"), root=ev)
        ep = read_run_manifest(ev / MANIFESTS_SUBDIR / "epi" / MANIFEST_FILENAME)
        root = read_run_manifest(ev / MANIFEST_FILENAME)
        idx = read_index(ev)
        assert ep.created_at == "2026-07-15T00:00:00+00:00"        # original preserved
        assert root.record_sha256() == ep.record_sha256()          # root == episode
        assert idx["episodes"][0]["record_sha256"] == ep.record_sha256()
        assert len(idx["episodes"]) == 1

    def test_stale_root_mirror_is_repaired_from_episode(self, tmp_path):
        ev = tmp_path / "ev"
        ev.mkdir()
        write_run_manifest(ev, _mk(episode_id="epi"), root=ev)
        (ev / MANIFEST_FILENAME).write_text('{"manifest_v": 1, "stale": true}')
        # re-finalizing the same episode repairs the root mirror from the canonical record
        write_run_manifest(ev, _mk(episode_id="epi"), root=ev)
        root = read_run_manifest(ev / MANIFEST_FILENAME)
        ep = read_run_manifest(ev / MANIFESTS_SUBDIR / "epi" / MANIFEST_FILENAME)
        assert root.record_sha256() == ep.record_sha256()

    def test_conflicting_logical_content_still_raises(self, tmp_path):
        ev = tmp_path / "ev"
        ev.mkdir()
        write_run_manifest(ev, _mk(episode_id="epi"), root=ev)
        with pytest.raises(ManifestConflictError):
            write_run_manifest(ev, _mk(episode_id="epi", job_input_variant="conflict"), root=ev)


class TestArtifactAndEpisodeExportIntegrity:
    def _finished(self, data_root, repo):
        from packages.orchestration.pingpong_job import job_evidence_dir
        job_id, _ = _run(_JOB, repo)
        return job_id, job_evidence_dir(job_id)

    def _export(self, job_id, tmp):
        from packages.orchestration.job_evidence import export_job_evidence
        out = export_job_evidence(job_id, str(tmp))
        return json.loads((Path(out["out_dir"]) / "manifest_integrity.json").read_text())

    def test_valid_artifact_passes(self, data_root, repo, tmp_path):
        job_id, _ = self._finished(data_root, repo)
        assert self._export(job_id, tmp_path / "b")["ok"] is True

    def test_prepared_input_tamper_blocks(self, data_root, repo, tmp_path):
        job_id, ev = self._finished(data_root, repo)
        m = _manifest_of(job_id)
        art = ev / MANIFESTS_SUBDIR / m.episode_id / m.calls[0].artifact
        d = json.loads(art.read_text())
        d["prepared_input"] = {"tampered": True}
        art.write_text(json.dumps(d))
        assert self._export(job_id, tmp_path / "b")["ok"] is False

    def test_identity_tamper_blocks(self, data_root, repo, tmp_path):
        job_id, ev = self._finished(data_root, repo)
        m = _manifest_of(job_id)
        art = ev / MANIFESTS_SUBDIR / m.episode_id / m.calls[0].artifact
        d = json.loads(art.read_text())
        d["identity"]["call_id"] = "hacked"
        art.write_text(json.dumps(d))
        assert self._export(job_id, tmp_path / "b")["ok"] is False

    def test_ok_flag_tamper_blocks(self, data_root, repo, tmp_path):
        job_id, ev = self._finished(data_root, repo)
        m = _manifest_of(job_id)
        art = ev / MANIFESTS_SUBDIR / m.episode_id / m.calls[0].artifact
        d = json.loads(art.read_text())
        d["ok"] = not d["ok"]
        art.write_text(json.dumps(d))
        assert self._export(job_id, tmp_path / "b")["ok"] is False

    def test_root_mirror_without_index_blocks(self, data_root, repo, tmp_path):
        job_id, ev = self._finished(data_root, repo)
        (ev / MANIFEST_INDEX_FILENAME).unlink()
        assert self._export(job_id, tmp_path / "b")["ok"] is False

    def test_missing_indexed_episode_blocks(self, data_root, repo, tmp_path):
        import shutil
        job_id, ev = self._finished(data_root, repo)
        m = _manifest_of(job_id)
        shutil.rmtree(ev / MANIFESTS_SUBDIR / m.episode_id)
        assert self._export(job_id, tmp_path / "b")["ok"] is False

    def test_root_mirror_differing_from_episode_blocks(self, data_root, repo, tmp_path):
        job_id, ev = self._finished(data_root, repo)
        (ev / MANIFEST_FILENAME).write_text(
            json.dumps({**json.loads((ev / MANIFEST_FILENAME).read_text()),
                        "job_input_sha256": "0" * 64}))
        assert self._export(job_id, tmp_path / "b")["ok"] is False
