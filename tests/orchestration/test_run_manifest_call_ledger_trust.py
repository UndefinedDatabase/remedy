"""F1 (round 12) — the finalized-call ledger is a VERIFIED CANONICAL ARTIFACT.

`CallExpectationV1` used to carry `expected_call_count`, `observed_call_count` and a
`finalized_calls_sha256` taken over the mutable Run JSON. None of those bytes were in the
canonical tree — the loader verified the Index, the Root Mirror, the Episode Manifest and the
per-Call artifacts, and nothing else. So a stored reference could drop a call, restate both
counts, put any formally-valid 64-hex string in the hash field, and validate. Reproduced exactly.

A number that only ever agrees with itself is not evidence. The ledger is therefore an artifact
like any other: canonical bytes at `run_manifests/<episode>/call_ledgers/<task>-<run>.json`, in
the episode's exact allowlist, hash-bound from the manifest, verified by the canonical loader,
recovery and the Evidence export — and a strict bijection with the manifest's calls.

It is also the per-run sequence F140's replay needs ("serves stream N for call N", keyed by call
sequence), which is why the run's own order is recorded rather than derived.
"""
from __future__ import annotations

import dataclasses
import hashlib
import json

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration import manifest_schema as _S
from packages.orchestration.run_manifest import (
    LEDGERS_SUBDIR,
    MANIFESTS_SUBDIR,
    MODE_PUBLISHED_REFERENCE,
    CallExpectationV1,
    CallLedgerEntryV1,
    ManifestError,
    RunCallLedgerV1,
    TaskCallExpectationV1,
    canonical_artifact_ref,
    decode_run_call_ledger_v1,
    load_latest_manifest_verified,
    validate_index_and_tree,
    validate_run_manifest,
    write_run_manifest,
)


def _bind(m):
    bound = []
    for c in m.calls:
        c = dataclasses.replace(c, artifact=canonical_artifact_ref(c.identity))
        bound.append(dataclasses.replace(
            c, artifact_sha256=hashlib.sha256(c.canonical_artifact_bytes()).hexdigest()))
    return dataclasses.replace(m, calls=tuple(bound))


_TWO = (T._call(seq=1), T._call(seq=2, role="reviewer", rnd=1, fp="r"))


def _two_call_manifest():
    return _bind(T._mk(episode_id="ep1", calls=_TWO))


def _probs(m):
    return validate_run_manifest(m, mode=MODE_PUBLISHED_REFERENCE)


# --------------------------------------------------------------------------- the finding


class TestAStoredReferenceCannotSelfAssertAShorterLedger:
    def test_the_reproduced_case(self):
        """Drop call 2, restate both counts to 1, invent a 64-hex ledger hash."""
        m = _two_call_manifest()
        assert _probs(m) == []
        lg = m.call_ledgers[0]
        shrunk = dataclasses.replace(
            m, calls=(m.calls[0],),
            call_expectation=CallExpectationV1(tasks=(TaskCallExpectationV1(
                task_id="T001", expectation="executed", run_id="rT001",
                expected_call_count=1, observed_call_count=1,
                finalized_calls_sha256="b" * 64, ledger_ref=lg.ref(),
                task_status_at_finalization="applied_to_job_workspace",
                dispatch_state="dispatched_this_episode"),)))
        problems = _probs(shrunk)
        assert problems, "a stored reference self-asserted a shorter complete ledger"
        assert any("not its ledger's canonical bytes" in p for p in problems), problems

    def test_an_arbitrary_ledger_hash_never_validates(self):
        m = _two_call_manifest()
        te = m.call_expectation.tasks[0]
        tampered = dataclasses.replace(
            m, call_expectation=CallExpectationV1(tasks=(
                dataclasses.replace(te, finalized_calls_sha256="c" * 64),)))
        assert any("not its ledger's canonical bytes" in p for p in _probs(tampered))

    def test_a_ledger_ref_that_names_nothing_blocks(self):
        m = _two_call_manifest()
        te = m.call_expectation.tasks[0]
        broken = dataclasses.replace(
            m, call_ledgers=(),
            call_expectation=CallExpectationV1(tasks=(te,)))
        assert any("no such ledger" in p for p in _probs(broken))


# --------------------------------------------------------------------------- the bijection


class TestLedgerManifestBijection:
    def test_every_manifest_call_maps_to_exactly_one_ledger_entry(self):
        m = _two_call_manifest()
        assert _probs(m) == []
        ids = [e.call_id for e in m.call_ledgers[0].entries]
        assert sorted(ids) == sorted(c.identity.call_id for c in m.calls)

    def test_an_extra_ledger_entry_blocks(self):
        m = _two_call_manifest()
        lg = m.call_ledgers[0]
        ghost = CallLedgerEntryV1(per_run_sequence=3, call_id="c-ghost", episode_id="ep1",
                                  role="builder", round=2, kind="attempt",
                                  prepared_input_fingerprint="d" * 64, ok=True)
        bad = dataclasses.replace(m, call_ledgers=(
            dataclasses.replace(lg, entries=lg.entries + (ghost,)),))
        assert any("does not publish it" in p for p in _probs(bad))

    def test_a_missing_ledger_entry_blocks(self):
        m = _two_call_manifest()
        lg = m.call_ledgers[0]
        bad = dataclasses.replace(m, call_ledgers=(
            dataclasses.replace(lg, entries=lg.entries[:1]),))
        assert any("has no ledger" in p or "ledger entries" in p for p in _probs(bad))

    def test_a_ledger_sequence_gap_blocks(self):
        m = _two_call_manifest()
        lg = m.call_ledgers[0]
        broken = dataclasses.replace(lg, entries=(
            lg.entries[0], dataclasses.replace(lg.entries[1], per_run_sequence=7)))
        assert any("not contiguous" in p for p in _probs(
            dataclasses.replace(m, call_ledgers=(broken,))))

    def test_a_ledger_fingerprint_mismatch_blocks(self):
        m = _two_call_manifest()
        lg = m.call_ledgers[0]
        broken = dataclasses.replace(lg, entries=(
            dataclasses.replace(lg.entries[0], prepared_input_fingerprint="e" * 64),
            lg.entries[1]))
        assert any("fingerprint" in p for p in _probs(
            dataclasses.replace(m, call_ledgers=(broken,))))

    def test_a_ledger_entry_for_an_unrelated_episode_blocks(self):
        m = _two_call_manifest()
        lg = m.call_ledgers[0]
        broken = dataclasses.replace(lg, entries=(
            dataclasses.replace(lg.entries[0], episode_id="ep-nowhere"), lg.entries[1]))
        probs = _probs(dataclasses.replace(m, call_ledgers=(broken,)))
        # Round 13: the field-by-field bijection names the disagreeing field itself; the
        # membership rule still fires too. Either way the record cannot be published.
        assert any("neither this episode nor one of its priors" in p or "names episode" in p
                   or "episode_id" in p for p in probs), probs

    def test_a_ledger_for_another_job_blocks(self):
        m = _two_call_manifest()
        bad = dataclasses.replace(m, call_ledgers=(
            dataclasses.replace(m.call_ledgers[0], job_id="another-job"),))
        assert any("belongs to job" in p for p in _probs(bad))

    def test_the_counts_must_be_the_ledgers_own_truth(self):
        m = _two_call_manifest()
        te = m.call_expectation.tasks[0]
        bad = dataclasses.replace(m, call_expectation=CallExpectationV1(tasks=(
            dataclasses.replace(te, expected_call_count=5),)))
        assert any("its ledger records" in p or "expected exactly" in p for p in _probs(bad))


# --------------------------------------------------------------------------- on disk


class TestTheLedgerIsACanonicalArtifact:
    @pytest.fixture
    def ev(self, tmp_path):
        d = tmp_path / "ev"
        d.mkdir()
        m = dataclasses.replace(_two_call_manifest(), episode_ordinal=1)
        write_run_manifest(d, m, root=tmp_path)
        return d

    def _ledger_file(self, ev):
        return sorted((ev / MANIFESTS_SUBDIR / "ep1" / LEDGERS_SUBDIR).glob("*.json"))[0]

    def test_the_writer_publishes_the_ledger(self, ev):
        f = self._ledger_file(ev)
        assert f.exists()
        stored = decode_run_call_ledger_v1(f.read_bytes())
        # Round 14: the fixture emits the REAL canonical refs production emits.
        assert [e.call_id for e in stored.entries] == [
            "calls/builder/round-01/attempt", "calls/reviewer/round-01/attempt"]
        assert validate_index_and_tree(ev, job_id="j") == []

    def test_a_tampered_ledger_artifact_blocks(self, ev):
        f = self._ledger_file(ev)
        raw = json.loads(f.read_text())
        raw["entries"] = raw["entries"][:1]
        f.write_bytes((json.dumps(raw, indent=2, sort_keys=True) + "\n").encode())
        problems = validate_index_and_tree(ev, job_id="j")
        assert any("ledger" in p for p in problems), problems
        with pytest.raises(ManifestError):
            load_latest_manifest_verified(ev, job_id="j")

    def test_a_missing_ledger_artifact_blocks(self, ev):
        self._ledger_file(ev).unlink()
        problems = validate_index_and_tree(ev, job_id="j")
        assert any("missing call ledger" in p for p in problems), problems

    def test_an_undeclared_ledger_artifact_blocks(self, ev):
        (self._ledger_file(ev).parent / "T999-rogue.json").write_bytes(b"{}")
        problems = validate_index_and_tree(ev, job_id="j")
        assert any("undeclared call ledgers" in p for p in problems), problems

    def test_a_noncanonical_ledger_artifact_blocks(self, ev):
        f = self._ledger_file(ev)
        f.write_bytes(json.dumps(json.loads(f.read_text()), indent=4).encode())
        assert validate_index_and_tree(ev, job_id="j") != []

    def test_the_ledger_is_exported_as_a_verified_member(self, ev, tmp_path):
        from packages.orchestration.run_manifest import build_verified_manifest_tree
        files, problems = build_verified_manifest_tree(ev, job_id="j")
        assert problems == []
        assert any(LEDGERS_SUBDIR in k for k in files), sorted(files)


# --------------------------------------------------------------------------- the schema


class TestTheLedgerSchemaIsExact:
    def _raw(self):
        return RunCallLedgerV1(job_id="j", task_id="T001", run_id="r1",
                               terminal_state="completed", complete=True,
                               entries=(CallLedgerEntryV1(
                                   per_run_sequence=1, call_id="c1", episode_id="ep1",
                                   role="builder", round=1, kind="attempt",
                                   prepared_input_fingerprint="a" * 64, ok=True),)).to_json()

    def test_a_clean_ledger_round_trips(self):
        raw = self._raw()
        assert decode_run_call_ledger_v1(raw).to_json() == raw

    def test_an_unknown_field_is_refused(self):
        with pytest.raises(_S.SchemaError):
            decode_run_call_ledger_v1({**self._raw(), "SMUGGLED": 1})

    def test_an_unsupported_version_is_refused(self):
        with pytest.raises(_S.SchemaError):
            decode_run_call_ledger_v1({**self._raw(), "ledger_v": 2})

    def test_an_unsupported_terminal_state_is_refused(self):
        with pytest.raises(_S.SchemaError):
            decode_run_call_ledger_v1({**self._raw(), "terminal_state": "vibes"})

    def test_a_wrong_type_is_refused(self):
        with pytest.raises(_S.SchemaError):
            decode_run_call_ledger_v1({**self._raw(), "complete": "true"})


# --------------------------------------------------------------------------- production


class TestProductionPublishesRealLedgers:
    def test_a_real_run(self, data_root, repo):
        from packages.orchestration.pingpong_job import job_evidence_dir

        job_id, _res = T._run(T._JOB, repo)
        ev = job_evidence_dir(job_id)
        ref = load_latest_manifest_verified(ev, job_id=job_id)
        assert ref.call_ledgers, "production published no ledger"
        lg = ref.call_ledgers[0]
        assert [e.per_run_sequence for e in lg.entries] == list(range(1, len(lg.entries) + 1))
        assert {e.call_id for e in lg.entries} == {c.identity.call_id for c in ref.calls}
        te = ref.call_expectation.tasks[0]
        assert te.ledger_ref == lg.ref()
        assert te.finalized_calls_sha256 == lg.sha256()
        assert validate_run_manifest(ref, mode=MODE_PUBLISHED_REFERENCE) == []
        assert validate_index_and_tree(ev, job_id=job_id) == []


data_root = T.data_root
repo = T.repo
