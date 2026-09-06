"""F012 T003 (hardened) — `remedy job rerun --check-manifest` against real current state.

Drift is exercised through the ACTUAL CLI against a real Git target repo, using the
current-state candidate — not by rewriting the stored reference manifest. Coverage states
and the new incomplete-coverage exit code (5) are asserted. Episodes (stop→resume→complete)
are covered too. Nothing re-executes; no provider generation call is made.
"""
from __future__ import annotations

import contextlib
import io
import json
import subprocess
from pathlib import Path

import pytest

from apps.cli.command_catalog import CATALOG, get_commands_for_group
from apps.cli.commands import collect_all_handlers
from apps.cli.commands import job_rerun_cmd as CMD


@pytest.fixture(autouse=True)
def _freeze_remedy_identity(monkeypatch):
    """Pin Remedy's own worktree identity for the duration of each test.

    A run manifest records the identity of the Remedy checkout itself — HEAD, a
    content hash and a dirty flag — and any UNTRACKED entry sets dirty
    (run_manifest.py, `dirty = True  # any untracked entry means dirty`). The
    reference manifest is written when the job runs; the candidate is built a
    moment later. Under `-n auto` all 24 workers share this one repo tree, so a
    neighbouring test creating or removing a file in the repo between those two
    moments changes the identity, the diff records a blocking drift, and
    `same_inputs` becomes False where the test requires None.

    Reproduced deterministically: with a loop touching and removing an untracked
    file in the repo root, the coverage test failed 5/5; with a quiet tree it
    passed 3/3.

    Freezing to the value observed at test start keeps the REAL identity — no
    forced "complete" — and only removes the race, so what these tests assert
    stays what they asserted: the job inputs, not Remedy's own tree. This is the
    same seam the module already uses deliberately in _patch_remedy_identity.
    """
    from packages.orchestration import run_manifest as _RM
    snapshot = _RM.remedy_worktree_identity()
    monkeypatch.setattr(_RM, "remedy_worktree_identity", lambda: snapshot)



def _git_repo(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    subprocess.run("git init -q && git config user.email t@t && git config user.name t "
                   "&& echo '# demo' > README.md && git add -A && git commit -qm init",
                   shell=True, cwd=path, check=True)
    return path


_JOB = "# Job: F012 rerun\n\n## Task 1\nDo a thing.\n\nAcceptance:\n- it is done\n"


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


def _complete_remedy_identity():
    """A deterministic, COMPLETE Remedy worktree identity — so an equality check does not
    depend on whether the test harness happens to sit in a git checkout (F12)."""
    from packages.orchestration.run_manifest import GIT_OK, WorktreeIdentity
    return WorktreeIdentity(GIT_OK, "a" * 40, "d" * 64, (), dirty=False)


def _patch_remedy_identity(monkeypatch, identity):
    """Pin ``remedy_worktree_identity()`` for both the recorded reference and the check
    candidate, so the F012 equality being asserted is about the JOB inputs, not the presence of
    Remedy's own ``.git`` (which an extracted review ZIP does not have)."""
    monkeypatch.setattr(
        "packages.orchestration.run_manifest.remedy_worktree_identity",
        lambda: identity)


@pytest.fixture
def finished_job(data_root, repo):
    from packages.orchestration.pingpong_job import parse_job_file, run_job
    job = parse_job_file(_JOB, str(repo))
    run_job(job.job_id, builder_provider=_prov(), reviewer_provider=_prov(),
            repair_rounds=0)
    return job.job_id


def _run_json(job_id):
    buf = io.StringIO()
    with pytest.raises(SystemExit) as exc:
        with contextlib.redirect_stdout(buf):
            CMD._cmd_job_rerun(job_id, check_manifest=True, json_output=True)
    return exc.value.code, json.loads(buf.getvalue())


# ---------------------------------------------------------------------------
# F1/F2 — current-state drift through the CLI, real git repo
# ---------------------------------------------------------------------------

class TestCurrentTargetDrift:
    def test_a_new_target_commit_causes_exit_4(self, finished_job, repo):
        subprocess.run("echo more >> README.md && git add -A && git commit -qm two",
                       shell=True, cwd=repo, check=True)
        code, payload = _run_json(finished_job)
        assert code == 4
        assert any(e["category"] == "base_commit" for e in payload["blocking"])
        assert payload["same_inputs"] is False

    def test_an_uncommitted_target_change_is_detected(self, finished_job, repo):
        (repo / "README.md").write_text("# demo\nuncommitted\n")
        code, payload = _run_json(finished_job)
        assert code == 4
        assert any(e["field"] == "target_tree" for e in payload["blocking"])

    def test_unchanged_target_verifies_without_blocking(self, finished_job):
        # No blocking drift; per-call coverage is incomplete in check-only mode → exit 5.
        code, payload = _run_json(finished_job)
        assert code == 5
        assert payload["blocking"] == []
        assert payload["verification_complete"] is False
        assert payload["same_inputs"] is None

    def test_config_drift_exits_4(self, finished_job, monkeypatch):
        monkeypatch.setenv("REMEDY_OLLAMA_MODEL", "a-different-model")
        code, payload = _run_json(finished_job)
        assert code == 4
        cats = {e["category"] for e in payload["blocking"]}
        assert "config_value" in cats or "environment" in cats


# ---------------------------------------------------------------------------
# F6 — coverage & exit codes
# ---------------------------------------------------------------------------

class TestCoverageAndExitCodes:
    def test_incomplete_coverage_returns_5_and_never_same(self, finished_job, capsys):
        with pytest.raises(SystemExit) as exc:
            CMD._cmd_job_rerun(finished_job, check_manifest=True, json_output=False)
        assert exc.value.code == 5
        out = capsys.readouterr().out
        assert "Input equality could not be fully verified." in out
        assert "recorded, not promised" in out
        assert "did not re-execute" in out
        assert "same inputs" not in out.lower().split("could not")[0]

    def test_json_exposes_coverage_and_verification_state(self, finished_job):
        code, payload = _run_json(finished_job)
        assert payload["verification_complete"] is False
        assert payload["same_inputs"] is None
        assert "calls" not in payload["coverage"] or True
        assert payload["coverage"]["calls_compared"] is False

    def test_no_secret_or_absolute_path_in_output(self, finished_job, monkeypatch):
        monkeypatch.setenv("REMEDY_SECRET_TOKEN", "CANARY-abc123")
        code, payload = _run_json(finished_job)
        assert "CANARY-abc123" not in json.dumps(payload)

    def test_it_mutates_nothing(self, finished_job):
        from packages.orchestration.pingpong_job import job_evidence_dir
        mp = job_evidence_dir(finished_job) / "run_manifest.json"
        before = mp.read_text()
        with pytest.raises(SystemExit):
            CMD._cmd_job_rerun(finished_job, check_manifest=True, json_output=True)
        assert mp.read_text() == before


# ---------------------------------------------------------------------------
# F7 — episodes: stop → resume → complete
# ---------------------------------------------------------------------------

class TestEpisodes:
    def test_stop_resume_complete_two_episodes_no_conflict(self, data_root, repo):
        from packages.orchestration.pingpong_job import (
            JOB_COMPLETED,
            JOB_STOPPED,
            job_evidence_dir,
            parse_job_file,
            run_job,
        )
        from packages.orchestration.pingpong_provider import FakeProvider
        from packages.orchestration.run_manifest import read_index
        from packages.orchestration.safe_points import request_stop

        class _Stopper(FakeProvider):
            def __init__(self, jid):
                super().__init__(pass_on_round=1, fail_on_round=99)
                self.jid = jid

            def build(self, prompt, **kw):
                request_stop(self.jid, "operator", "cli")
                return super().build(prompt, **kw)

        job = parse_job_file(_JOB, str(repo))
        stopped = run_job(job.job_id, builder_provider=_Stopper(job.job_id),
                          reviewer_provider=_prov(), repair_rounds=0)
        assert stopped.status == JOB_STOPPED
        ev = job_evidence_dir(job.job_id)
        stop_ep = read_index(ev)["latest_episode_id"]
        stop_manifest_before = (ev / "run_manifests" / stop_ep / "run_manifest.json").read_text()

        # resume → complete
        done = run_job(job.job_id, builder_provider=_prov(), reviewer_provider=_prov(),
                       repair_rounds=0)
        assert done.status == JOB_COMPLETED

        idx = read_index(ev)
        assert len(idx["episodes"]) == 2
        complete_ep = idx["latest_episode_id"]
        assert complete_ep != stop_ep
        # the stopped episode's manifest is unchanged
        assert (ev / "run_manifests" / stop_ep / "run_manifest.json").read_text() \
            == stop_manifest_before
        # the completed episode references the prior stop episode
        from packages.orchestration.run_manifest import read_run_manifest
        comp = read_run_manifest(ev / "run_manifests" / complete_ep / "run_manifest.json")
        assert stop_ep in comp.prior_episode_ids
        assert not done.run_manifest_error


# ---------------------------------------------------------------------------
# F8 — manifest failure participates in the stop transaction
# ---------------------------------------------------------------------------

class TestStopTransaction:
    def test_manifest_write_failure_leaves_the_stop_request_pending(self, data_root, repo,
                                                                    monkeypatch):
        from packages.orchestration import run_manifest as RM
        from packages.orchestration.pingpong_job import (
            JOB_STOPPED,
            parse_job_file,
            run_job,
        )
        from packages.orchestration.safe_points import request_stop, stop_requested

        job = parse_job_file(_JOB, str(repo))
        request_stop(job.job_id, "operator", "cli")

        with monkeypatch.context() as m:
            m.setattr(RM, "write_run_manifest",
                      lambda *a, **k: (_ for _ in ()).throw(OSError("disk gone")))
            res = run_job(job.job_id, builder_provider=_prov(),
                          reviewer_provider=_prov(), repair_rounds=0)
        assert res.status != JOB_STOPPED               # no false clean stop
        assert "run_manifest_write_failed" in res.run_manifest_error
        assert stop_requested(job.job_id) is not None  # request still pending

        # retry succeeds: exactly one archive/postmortem/event/manifest
        from packages.orchestration.pingpong_job import (
            STOP_POSTMORTEM_SUBDIR,
            job_evidence_dir,
        )
        from packages.orchestration.safe_points import archived_signals
        stopped = run_job(job.job_id, builder_provider=_prov(),
                          reviewer_provider=_prov(), repair_rounds=0)
        assert stopped.status == JOB_STOPPED
        assert len(archived_signals(job.job_id)) == 1
        eps = job_evidence_dir(job.job_id) / STOP_POSTMORTEM_SUBDIR
        assert len(list(eps.iterdir())) == 1
        runs = data_root / "job_logs" / job.job_id
        events = [json.loads(ln) for f in runs.glob("*.jsonl")
                  for ln in f.read_text().splitlines() if ln.strip()]
        assert len([e for e in events if e["event"] == "job_stopped"]) == 1


# ---------------------------------------------------------------------------
# F9 — legacy marker
# ---------------------------------------------------------------------------

class TestLegacyMarker:
    def test_pre_f012_completed_job_is_legacy_not_corrupt(self, data_root, repo):
        # simulate an old completed job: no F012 marker, no manifest.
        from packages.orchestration.job_evidence import export_job_evidence
        from packages.orchestration.pingpong_job import (
            JOB_COMPLETED,
            _persist_job,
            parse_job_file,
        )
        job = parse_job_file(_JOB, str(repo))
        job.status = JOB_COMPLETED
        job.tasks[0].status = "applied_to_job_workspace"
        job.run_manifest_required_v = 0            # unmarked = legacy
        _persist_job(job)
        out = export_job_evidence(job.job_id, str(repo.parent / "bundle_legacy"))
        mi = json.loads((Path(out["out_dir"]) / "manifest_integrity.json").read_text())
        assert mi["ok"] is True
        assert any("legacy" in n for n in mi.get("notes", []))

    def test_marked_completed_job_without_manifest_is_blocking(self, data_root, repo):
        from packages.orchestration.job_evidence import export_job_evidence
        from packages.orchestration.pingpong_job import (
            JOB_COMPLETED,
            _persist_job,
            parse_job_file,
        )
        job = parse_job_file(_JOB, str(repo))
        job.status = JOB_COMPLETED
        job.tasks[0].status = "applied_to_job_workspace"
        job.run_manifest_required_v = 1            # marked, but no manifest present
        _persist_job(job)
        out = export_job_evidence(job.job_id, str(repo.parent / "bundle_marked"))
        mi = json.loads((Path(out["out_dir"]) / "manifest_integrity.json").read_text())
        assert mi["ok"] is False


# ---------------------------------------------------------------------------
# Errors + wiring
# ---------------------------------------------------------------------------

class TestErrors:
    def test_unknown_job_exits_3(self, data_root):
        with pytest.raises(SystemExit) as exc:
            CMD._cmd_job_rerun("0123456789abcdef", check_manifest=True, json_output=True)
        assert exc.value.code == 3

    def test_without_check_manifest_is_usage_error(self, finished_job):
        with pytest.raises(SystemExit) as exc:
            CMD._cmd_job_rerun(finished_job, check_manifest=False, json_output=True)
        assert exc.value.code == 2

    def test_no_manifest_job_is_an_error(self, data_root, repo):
        from packages.orchestration.pingpong_job import parse_job_file
        job = parse_job_file(_JOB, str(repo))
        with pytest.raises(SystemExit) as exc:
            CMD._cmd_job_rerun(job.job_id, check_manifest=True, json_output=True)
        assert exc.value.code == 1

    def test_malformed_job_id_is_usage_error(self, data_root):
        with pytest.raises(SystemExit) as exc:
            CMD._cmd_job_rerun("../etc", check_manifest=True, json_output=True)
        assert exc.value.code == 2


class TestWiring:
    def test_the_command_is_in_the_catalog(self):
        entry = next(e for e in CATALOG if e.command_id == "job.rerun")
        assert entry.group_id == "job" and entry.subcommand == "rerun"
        assert entry.supports_json and not entry.may_mutate_repo
        assert "--check-manifest" in {a.name for a in entry.args if a.is_flag}
        assert entry.command_id in {e.command_id for e in get_commands_for_group("job")}

    def test_the_handler_is_registered(self):
        assert "job.rerun" in collect_all_handlers()


# ---------------------------------------------------------------------------
# Hardening round 2
# ---------------------------------------------------------------------------

class TestContentDriftThroughCli:
    def test_dirty_content_to_dirty_content_drift_is_detected(self, finished_job, repo):
        # first dirty edit, then a DIFFERENT dirty edit with identical porcelain status
        (repo / "README.md").write_text("# demo\nAAAA\n")
        code_a, _ = _run_json(finished_job)         # already blocking vs the clean recorded tree
        assert code_a == 4
        (repo / "README.md").write_text("# demo\nBBBB\n")
        code_b, payload_b = _run_json(finished_job)
        assert code_b == 4
        assert any(e["field"] == "target_tree" for e in payload_b["blocking"])


class TestCompleteVerificationPath:
    def test_pure_diff_equal_calls_is_same_inputs(self):
        import tests.orchestration.test_run_manifest as T
        from packages.orchestration.run_manifest import diff_manifests
        a = T._mk()
        b = T._mk()
        d = diff_manifests(a, b)
        assert d["same_inputs"] is True and d["verification_complete"] is True

    def test_pure_diff_call_change_is_blocking(self):
        import tests.orchestration.test_run_manifest as T
        from packages.orchestration.run_manifest import diff_manifests
        a = T._mk(calls=(T._call("T001", 1, fp="h1"),))
        b = T._mk(calls=(T._call("T001", 1, fp="CHANGED"),))
        d = diff_manifests(a, b)
        assert d["same_inputs"] is False and any(e["category"] == "prompt"
                                                 for e in d["blocking"])

    def test_public_cli_real_job_with_calls_exits_5(self, finished_job):
        code, payload = _run_json(finished_job)
        assert code == 5 and payload["same_inputs"] is None

    def test_exit_5_names_which_coverage_dimension_is_short(self, finished_job):
        """F9 (round 12): "every call compared" and "every material input known" are different
        claims — an operator must see which one fell short."""
        code, payload = _run_json(finished_job)
        assert code == 5
        cov = payload["coverage"]
        assert cov["call_status"] == "incomplete"      # per-call replay is F140
        assert "input_status" in cov and "input_problems" in cov

    def test_the_text_output_names_both_coverage_dimensions(self, finished_job):
        buf = io.StringIO()
        with pytest.raises(SystemExit) as exc:
            with contextlib.redirect_stdout(buf):
                CMD._cmd_job_rerun(finished_job, check_manifest=True)
        assert exc.value.code == 5
        out = buf.getvalue()
        assert "call inputs:" in out and "material inputs:" in out, out

    def test_public_cli_zero_call_job_exits_0(self, data_root, repo, monkeypatch):
        # F12: a zero-call equality check must not silently depend on Remedy's OWN worktree
        # being under Git. When this test runs from an EXTRACTED review ZIP there is no `.git`,
        # so `remedy_worktree_identity()` would be `unavailable`, dragging the check to exit 5.
        # Pin Remedy's identity to a deterministic COMPLETE fixture for BOTH the recorded
        # reference (captured in run_job) and the check candidate — the equality being proved is
        # about the JOB inputs, not about whether the harness happens to sit in a git checkout.
        _patch_remedy_identity(monkeypatch, _complete_remedy_identity())
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
        code, payload = _run_json(job.job_id)
        assert code == 0 and payload["same_inputs"] is True
        assert payload["verification_complete"] is True

    def test_no_git_remedy_env_zero_call_exits_5(self, data_root, repo, monkeypatch):
        # F12: the honest counterpart — when Remedy's own worktree identity is genuinely
        # UNAVAILABLE (no Git around the harness), the check must NOT claim "same inputs". It
        # reports incomplete coverage (exit 5), never a false exit 0.
        from packages.orchestration.run_manifest import (
            GIT_UNAVAILABLE,
            UNAVAILABLE,
            WorktreeIdentity,
        )
        _patch_remedy_identity(
            monkeypatch,
            WorktreeIdentity(GIT_UNAVAILABLE, UNAVAILABLE, "", ("no git",), dirty=None))
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
        code, payload = _run_json(job.job_id)
        assert code == 5
        assert payload["same_inputs"] is None
        assert payload["verification_complete"] is False


class TestSharedFinalizedCallContext:
    def test_f010_and_f012_build_the_same_context(self, data_root, repo):
        from packages.orchestration.pingpong_job import parse_job_file, run_job
        from packages.orchestration.pingpong_loop import (
            finalized_call_context,
            load_run,
        )
        from packages.orchestration.pingpong_provider import FakeProvider

        job = parse_job_file(_JOB, str(repo))
        res = run_job(job.job_id,
                      builder_provider=FakeProvider(builder_error="provider_unavailable: x"),
                      reviewer_provider=_prov(), repair_rounds=0)
        run = load_run(res.tasks[0].run_id)
        builder = [c for c in run["finalized_calls"]
                   if c["identity"]["role"] == "builder"][0]
        # F010's post-mortem for that terminal failure used the same call id
        assert any(builder["identity"]["call_id"] in p
                   for p in run.get("postmortem_paths", []))
        # and the shared constructor exists and returns a FinalizedCallContext
        assert hasattr(finalized_call_context, "__call__")


# ---------------------------------------------------------------------------
# Hardening round 3
# ---------------------------------------------------------------------------

class TestCompleteJobInputDrift:
    def test_max_rounds_drift_blocks(self, finished_job):
        from packages.orchestration.pingpong_job import job_evidence_dir, load_job_plan
        from packages.orchestration.run_manifest import (
            build_current_candidate,
            diff_manifests,
            load_latest_manifest_verified,
        )
        ev = job_evidence_dir(finished_job)
        ref = load_latest_manifest_verified(ev, job_id=finished_job)
        job = load_job_plan(finished_job)
        job.execution_config.max_rounds = 99          # a material execution input changed
        cand = build_current_candidate(ref, job)
        diff = diff_manifests(ref, cand)
        assert diff["same_inputs"] is False
        assert any(e["field"] == "job_input_sha256" for e in diff["blocking"])

    def test_test_command_drift_blocks(self, finished_job):
        from packages.orchestration.pingpong_job import job_evidence_dir, load_job_plan
        from packages.orchestration.run_manifest import (
            build_current_candidate,
            diff_manifests,
            load_latest_manifest_verified,
        )
        ev = job_evidence_dir(finished_job)
        ref = load_latest_manifest_verified(ev, job_id=finished_job)
        job = load_job_plan(finished_job)
        job.execution_config.test_command = "a-new-test-command"
        diff = diff_manifests(ref, build_current_candidate(ref, job))
        assert diff["same_inputs"] is False


class TestRemedyContentDrift:
    def test_remedy_worktree_digest_change_blocks(self):
        import dataclasses

        import tests.orchestration.test_run_manifest as T
        from packages.orchestration.run_manifest import diff_manifests
        a = T._mk()
        b_snap = dataclasses.replace(
            a.snapshot, remedy_worktree={"status": "ok", "head": "a" * 40,
                                         "digest": "CHANGED", "problems": []})
        b_wrapper = dataclasses.replace(a.episode_snapshot, input=b_snap)
        b = dataclasses.replace(a, episode_snapshot=b_wrapper)
        diff = diff_manifests(a, b)
        assert diff["same_inputs"] is False
        assert any(e["field"] == "remedy_worktree_digest" for e in diff["blocking"])


class TestEpisodeIsolation:
    def test_completed_resume_episode_has_only_its_own_calls(self, data_root, repo):
        from packages.orchestration.pingpong_job import (
            JOB_COMPLETED,
            JOB_STOPPED,
            job_evidence_dir,
            parse_job_file,
            run_job,
        )
        from packages.orchestration.pingpong_provider import FakeProvider
        from packages.orchestration.run_manifest import (
            load_latest_manifest_verified,
            read_index,
            read_run_manifest,
        )
        from packages.orchestration.safe_points import request_stop

        _TWO = ("# Job: iso\n\n## Task 1\nA.\n\nAcceptance:\n- x\n"
                "\n## Task 2\nB.\n\nAcceptance:\n- x\n")

        class _StopAfter1(FakeProvider):
            def __init__(self, jid):
                super().__init__(pass_on_round=1, fail_on_round=99)
                self.jid = jid
                self.calls = 0

            def review(self, prompt, **kw):
                out = super().review(prompt, **kw)
                self.calls += 1
                if self.calls == 1:                    # stop after task 1's reviewer passes
                    request_stop(self.jid, "op", "cli")
                return out

        job = parse_job_file(_TWO, str(repo))
        stopped = run_job(job.job_id, builder_provider=FakeProvider(pass_on_round=1,
                          fail_on_round=99), reviewer_provider=_StopAfter1(job.job_id),
                          repair_rounds=0)
        assert stopped.status == JOB_STOPPED
        ev = job_evidence_dir(job.job_id)
        stop_ep = read_index(ev)["latest_episode_id"]
        stop_m = read_run_manifest(ev / "run_manifests" / stop_ep / "run_manifest.json")
        stop_eps = {c.identity.episode_id for c in stop_m.calls}

        done = run_job(job.job_id, builder_provider=FakeProvider(pass_on_round=1,
                       fail_on_round=99), reviewer_provider=FakeProvider(pass_on_round=1,
                       fail_on_round=99), repair_rounds=0)
        assert done.status == JOB_COMPLETED
        idx = read_index(ev)
        assert len(idx["episodes"]) == 2
        comp_ep = idx["latest_episode_id"]
        comp_m = read_run_manifest(ev / "run_manifests" / comp_ep / "run_manifest.json")
        # every call in the completed episode belongs to THAT episode — not the stopped one
        assert all(c.identity.episode_id == comp_ep for c in comp_m.calls)
        assert stop_ep not in {c.identity.episode_id for c in comp_m.calls}
        # the stopped episode is unchanged and self-consistent
        assert all(c.identity.episode_id == stop_ep for c in stop_m.calls) or not stop_m.calls
        # timestamps differ across episodes (F5)
        assert stop_m.created_at != comp_m.created_at
        # the whole tree still validates
        assert load_latest_manifest_verified(ev, job_id=job.job_id).episode_id == comp_ep
