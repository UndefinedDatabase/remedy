"""F4 (round 14) — the closed canonical call-ref grammar.

`safe_call_ref()` only asked whether a ref was DANGEROUS, so all of these passed:

    calls//builder        calls/./builder        calls/builder/        home/alice        c1

None of them names a call. A call ref is the identity F010's post-mortems, F012's manifests and
F140's replay all use to name the SAME call, so it must be canonical — not merely not-absolute.

The grammar is closed to exactly what production emits. Every source was inspected and RUN first:

    shared_call_id()               -> calls/<role>/round-NN/<kind>        (fallback / fake)
    _allocate_stream_call_dir()    -> streams/<role>/round-NN/<kind>-II   (streamed CLI)
    F010's committed layouts       -> the same two shapes

Both encode role, round and kind — so the ref must AGREE with the CallIdentity it belongs to.
"""
from __future__ import annotations

import subprocess

import pytest

from packages.orchestration.call_identity import CallIdentity
from packages.orchestration.run_manifest import (
    CALL_REF_NAMESPACES,
    parse_call_ref,
    safe_call_ref,
    validate_call_identity,
    validate_call_ref,
)

#: Every shape production actually emits, verified against a live fake-provider run and against
#: `shared_call_id` / `_allocate_stream_call_dir` directly.
REAL_PRODUCTION_REFS = [
    "calls/builder/round-01/attempt",
    "calls/reviewer/round-01/attempt",
    "calls/builder/round-01/parse-retry",
    "calls/reviewer/round-01/parse-retry",
    "calls/builder/round-12/attempt",
    "calls/builder/round-100/attempt",          # a round may exceed 99
    "streams/builder/round-01/attempt-01",
    "streams/reviewer/round-01/attempt-02",
    "streams/reviewer/round-02/parse-retry-03",  # the kind itself contains a dash
]


class TestEveryRealProductionRefPasses:
    @pytest.mark.parametrize("cid", REAL_PRODUCTION_REFS)
    def test_it_passes(self, cid):
        assert safe_call_ref(cid), f"the grammar refuses a ref production emits: {cid}"

    @pytest.mark.parametrize("cid", REAL_PRODUCTION_REFS)
    def test_it_decodes_to_its_fields(self, cid):
        fields, problems = parse_call_ref(cid)
        assert problems == []
        assert fields["namespace"] in CALL_REF_NAMESPACES
        assert fields["role"] in ("builder", "reviewer")
        assert fields["kind"] in ("attempt", "parse-retry")
        assert fields["round"] >= 1

    def test_the_synthesizer_production_uses_agrees_with_the_grammar(self):
        from packages.orchestration.pingpong_loop import shared_call_id

        class NoStream:
            stream_call_id = ""

        for role in ("builder", "reviewer"):
            for kind in ("attempt", "parse-retry"):
                for rnd in (1, 9, 12, 100):
                    cid = shared_call_id(NoStream(), role, rnd, kind)
                    assert safe_call_ref(cid), cid
                    fields, _ = parse_call_ref(cid)
                    assert (fields["role"], fields["kind"], fields["round"]) == (role, kind, rnd)

    def test_a_streamed_provider_ref_passes_through_the_shared_identity(self):
        from packages.orchestration.pingpong_loop import shared_call_id

        class Streamed:
            stream_call_id = "streams/builder/round-03/parse-retry-02"

        cid = shared_call_id(Streamed(), "builder", 3, "parse-retry")
        assert cid == "streams/builder/round-03/parse-retry-02"
        assert validate_call_ref(cid, role="builder", round=3, kind="parse-retry") == []


class TestTheMalformedRefsTheOldRuleAccepted:
    @pytest.mark.parametrize("cid", [
        "calls//builder",          # empty segment
        "calls/./builder",         # `.` segment
        "calls/builder/",          # trailing slash
        "home/alice",              # not a call at all
        "c1",                      # the old synthetic fixture value
    ])
    def test_it_now_blocks(self, cid):
        assert not safe_call_ref(cid), f"{cid!r} still passes"

    @pytest.mark.parametrize("cid", [
        "/home/alice/SUPERSECRET", "~/secrets/x", "calls/../../etc/passwd",
        "calls/builder/../../../etc/shadow", "calls\\builder\\round-01\\attempt",
        "calls/builder/round-01/attempt\x00", "",
        "calls/builder/round-01/attempt/extra",     # too many segments
        "calls/builder/round-01",                    # too few
        "calls/admin/round-01/attempt",              # role not a closed enum
        "calls/builder/round-1/attempt",             # not zero-padded round-NN
        "calls/builder/roundNN/attempt",             # not `round-NN`
        "calls/builder/round-00/attempt",            # not a positive round
        "calls/builder/round-01/invented",           # kind not a closed enum
        "objects/builder/round-01/attempt",          # namespace not a closed enum
        "streams/builder/round-01/attempt",          # streamed refs carry the attempt index
        "calls/builder/round-01/attempt-01",         # non-streamed refs do not
    ])
    def test_the_rest_of_the_grammar_blocks(self, cid):
        assert not safe_call_ref(cid), f"{cid!r} still passes"

    def test_a_secret_canary_blocks(self):
        assert not safe_call_ref("calls/builder/round-01/token=SECRETVALUE123456")

    def test_an_overlong_ref_blocks(self):
        assert not safe_call_ref("calls/builder/round-01/" + "a" * 5000)


class TestTheRefMustAgreeWithItsCallIdentity:
    def test_role_drift_blocks(self):
        assert validate_call_ref("calls/builder/round-01/attempt", role="reviewer", round=1,
                                 kind="attempt")

    def test_round_drift_blocks(self):
        assert validate_call_ref("calls/builder/round-01/attempt", role="builder", round=2,
                                 kind="attempt")

    def test_kind_drift_blocks(self):
        assert validate_call_ref("calls/builder/round-01/attempt", role="builder", round=1,
                                 kind="parse-retry")

    def test_an_agreeing_ref_passes(self):
        assert validate_call_ref("calls/builder/round-01/attempt", role="builder", round=1,
                                 kind="attempt") == []

    def test_a_streamed_ref_agrees_through_its_index(self):
        assert validate_call_ref("streams/reviewer/round-02/parse-retry-03", role="reviewer",
                                 round=2, kind="parse-retry") == []


class TestOneValidatorForIdentityAndLedger:
    def _ident(self, call_id, role="builder", rnd=1, kind="attempt"):
        return CallIdentity(job_id="j", task_id="T001", run_id="r1", sequence=1, role=role,
                            round=rnd, kind=kind, call_id=call_id, episode_id="ep")

    @pytest.mark.parametrize("cid", ["calls//builder", "home/alice", "c1",
                                     "/home/alice/SUPERSECRET"])
    def test_the_call_identity_validator_uses_the_same_grammar(self, cid):
        assert any("call_id" in p for p in validate_call_identity(self._ident(cid)))
        assert not safe_call_ref(cid)

    @pytest.mark.parametrize("cid", REAL_PRODUCTION_REFS)
    def test_the_call_identity_validator_accepts_every_real_ref(self, cid):
        fields, _ = parse_call_ref(cid)
        ident = self._ident(cid, role=fields["role"], rnd=fields["round"], kind=fields["kind"])
        assert validate_call_identity(ident) == []

    def test_the_ledger_entry_uses_the_same_grammar(self):
        import dataclasses

        import tests.orchestration.test_run_manifest as T
        from packages.orchestration.run_manifest import (
            _bind_artifact_refs,
            validate_run_call_ledger,
        )
        base = _bind_artifact_refs(T._mk(calls=(T._call(seq=1),)))
        lg = base.call_ledgers[0]
        for cid in ("calls//builder", "home/alice", "c1"):
            bad = dataclasses.replace(lg, entries=(
                dataclasses.replace(lg.entries[0], call_id=cid),))
            assert any("call_id" in p for p in validate_run_call_ledger(bad)), cid


# --------------------------------------------------------------------------- F010 <-> F012


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


class TestF010AndF012ShareOneCallIdentity:
    def test_there_is_exactly_one_definition(self):
        import inspect

        from packages.orchestration.pingpong_loop import shared_call_id
        src = inspect.getsource(shared_call_id)
        assert "post-mortem writer and F012's manifest both use" in src

    def test_a_real_runs_call_ids_all_satisfy_the_grammar(self, data_root, repo):
        """The manifest's stored ids come from the same seam F010 records, so if the grammar
        refused one of them the two features would be naming different calls."""
        from packages.orchestration.pingpong_job import load_job_plan, parse_job_file, run_job
        from packages.orchestration.pingpong_loop import load_run
        from packages.orchestration.pingpong_provider import FakeProvider

        def prov():
            return FakeProvider(pass_on_round=1, fail_on_round=99)

        job = parse_job_file("# Job: g\n\n## Task 1\nx\n\nAcceptance:\n- y\n", str(repo))
        run_job(job.job_id, builder_provider=prov(), reviewer_provider=prov(), repair_rounds=0)
        j = load_job_plan(job.job_id)
        run = load_run(j.tasks[0].run_id)
        ids = [fc["identity"]["call_id"] for fc in run["finalized_calls"]]
        assert ids, "the run recorded no calls"
        for cid in ids:
            assert safe_call_ref(cid), f"production emitted a ref the grammar refuses: {cid}"
        assert ids == ["calls/builder/round-01/attempt", "calls/reviewer/round-01/attempt"]
