"""F3 (round 14) — Ledger artifact refs are collision-free.

`call_ledgers/{task_id}-{run_id}.json` is ambiguous, because `-` is legal inside both ids:

    (task_id="a-b", run_id="c")  ->  call_ledgers/a-b-c.json
    (task_id="a",   run_id="b-c")  ->  call_ledgers/a-b-c.json

Both ids satisfy the safe-component schema, so both are legal. A crafted canonical tree carrying
both in-Manifest ledgers and ONE physical ledger file was accepted by `validate_index_and_tree`
and `load_latest_manifest_verified`, because `_validate_episode_ledgers_anchored()` built a dict
keyed by filename and silently overwrote one declaration — the second ledger simply stopped
existing as far as verification was concerned.

The ref is now `sha256(unambiguous canonical identity)`. Canonical JSON is length-delimited by
construction, so exactly one (task_id, run_id) pair can produce those bytes. No compatibility
layer: F012 is unmerged, so no accepted record uses the old shape.
"""
from __future__ import annotations

import dataclasses
import hashlib

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration import manifest_schema as _S
from packages.orchestration.run_manifest import (
    LEDGERS_SUBDIR,
    MANIFESTS_SUBDIR,
    MODE_PUBLISHED_REFERENCE,
    RunCallLedgerV1,
    _bind_artifact_refs,
    canonical_ledger_ref,
    ledger_identity_bytes,
    validate_index_and_tree,
    validate_ledger_set,
    validate_run_manifest,
    write_run_manifest,
)

_NAME_MAX = 255


def _lg(task_id, run_id):
    return RunCallLedgerV1(job_id="j", task_id=task_id, run_id=run_id,
                           terminal_state="completed", complete=True, entries=())


# --------------------------------------------------------------------------- the collision


class TestTheReproducedCollision:
    def test_the_dash_pair_produces_distinct_refs(self):
        a = canonical_ledger_ref("a-b", "c")
        b = canonical_ledger_ref("a", "b-c")
        assert a != b, "the reproduced dash collision still maps two identities to one file"

    def test_the_old_concatenation_really_did_collide(self):
        """The defect, stated as the fact it was — so nobody reintroduces the shape."""
        assert f"{'a-b'}-{'c'}" == f"{'a'}-{'b-c'}" == "a-b-c"

    @pytest.mark.parametrize("t1,r1,t2,r2", [
        ("a-b", "c", "a", "b-c"),
        ("x", "y-z", "x-y", "z"),
        ("T001-r", "1", "T001", "r-1"),
        ("a", "b", "a-b", ""),
    ])
    def test_no_dash_split_ambiguity_survives(self, t1, r1, t2, r2):
        assert canonical_ledger_ref(t1, r1) != canonical_ledger_ref(t2, r2)

    def test_the_identity_encoding_is_unambiguous(self):
        assert ledger_identity_bytes("a-b", "c") != ledger_identity_bytes("a", "b-c")


class TestTheRefIsDeterministicAndBounded:
    def test_the_ref_is_deterministic(self):
        assert canonical_ledger_ref("T001", "r1") == canonical_ledger_ref("T001", "r1")

    def test_the_ref_is_recomputable_from_the_ledger_identity(self):
        lg = _lg("T001", "r1")
        assert lg.ref() == canonical_ledger_ref(lg.task_id, lg.run_id)

    def test_maximum_length_ids_still_produce_a_legal_filename(self):
        """A sha256 is fixed-width, so the longest legal ids cannot overflow NAME_MAX."""
        big_t, big_r = "T" * _S.MAX_ID_LEN, "r" * _S.MAX_ID_LEN
        ref = canonical_ledger_ref(big_t, big_r)
        name = ref.split("/", 1)[1]
        assert len(name) == 64 + len(".json")
        assert len(name) < _NAME_MAX
        assert ref == f"{LEDGERS_SUBDIR}/{hashlib.sha256(ledger_identity_bytes(big_t, big_r)).hexdigest()}.json"

    def test_the_ref_is_a_single_safe_component_under_the_ledgers_dir(self):
        name = canonical_ledger_ref("T001", "r1").split("/", 1)[1]
        assert "/" not in name and ".." not in name
        assert all(c in "0123456789abcdef" for c in name[:-len(".json")])


# --------------------------------------------------------------------------- the validators


class TestDuplicateRefsAreRefused:
    def test_distinct_identities_can_never_share_a_ref(self):
        """With the sha256 ref this holds BY CONSTRUCTION, so state it that way rather than
        pretending to catch a collision the encoding cannot produce. The two ways a duplicate ref
        can still reach the validator — the same key twice, or a forged `ref()` — are the two
        tests below."""
        seen: dict[str, tuple] = {}
        pairs = [("a-b", "c"), ("a", "b-c"), ("T001", "r1"), ("T001-r", "1"),
                 ("x", "y-z"), ("x-y", "z"), ("T002", "r1"), ("T001", "r2")]
        for t, r in pairs:
            ref = canonical_ledger_ref(t, r)
            assert ref not in seen, f"({t},{r}) collided with {seen.get(ref)}"
            seen[ref] = (t, r)
        assert len(seen) == len(pairs)

    def test_the_same_ledger_key_twice_blocks(self):
        base = _bind_artifact_refs(T._mk(episode_id="ep1", calls=(T._call(seq=1),)))
        lg = base.call_ledgers[0]
        probs = validate_ledger_set(dataclasses.replace(base, call_ledgers=(lg, lg)))
        assert any("two call ledgers for" in p for p in probs), probs

    def test_a_ledger_not_at_its_recomputed_ref_blocks(self):
        """A ref must be the one its own identity produces — never a pointer at someone else's
        artifact."""
        base = _bind_artifact_refs(T._mk(episode_id="ep1", calls=(T._call(seq=1),)))
        lg = base.call_ledgers[0]

        class Aliased(RunCallLedgerV1):
            def ref(self):                       # type: ignore[override]
                return canonical_ledger_ref("someone", "else")

        bad = Aliased(job_id=lg.job_id, task_id=lg.task_id, run_id=lg.run_id,
                      terminal_state=lg.terminal_state, complete=lg.complete,
                      entries=lg.entries)
        forged = dataclasses.replace(base, call_ledgers=(bad,))
        probs = validate_ledger_set(forged)
        assert any("recomputed from" in p for p in probs), probs


# --------------------------------------------------------------------------- on disk


class TestTheCanonicalTreeRefusesAnAlias:
    @pytest.fixture
    def ev(self, tmp_path):
        d = tmp_path / "ev"
        d.mkdir()
        m = _bind_artifact_refs(T._mk(episode_id="ep1", calls=(T._call(seq=1),)))
        write_run_manifest(d, m, root=tmp_path)
        return d

    def test_the_export_contains_exactly_one_artifact_per_ledger(self, ev):
        from packages.orchestration.run_manifest import load_latest_manifest_verified
        m = load_latest_manifest_verified(ev, job_id="j")
        files = sorted((ev / MANIFESTS_SUBDIR / "ep1" / LEDGERS_SUBDIR).glob("*.json"))
        assert len(files) == len(m.call_ledgers) == 1
        assert files[0].name == m.call_ledgers[0].ref().split("/", 1)[1]

    def test_an_extra_undeclared_ledger_artifact_blocks(self, ev):
        (ev / MANIFESTS_SUBDIR / "ep1" / LEDGERS_SUBDIR / ("f" * 64 + ".json")).write_bytes(b"{}")
        assert any("undeclared call ledgers" in p
                   for p in validate_index_and_tree(ev, job_id="j"))

    def test_a_missing_ledger_artifact_blocks(self, ev):
        f = sorted((ev / MANIFESTS_SUBDIR / "ep1" / LEDGERS_SUBDIR).glob("*.json"))[0]
        f.unlink()
        assert validate_index_and_tree(ev, job_id="j")

    def test_a_clean_tree_validates(self, ev):
        assert validate_index_and_tree(ev, job_id="j") == []


class TestOnePhysicalFileCannotBackTwoLedgers:
    def test_the_loader_refuses_two_declarations_of_one_artifact(self, tmp_path):
        """The exact shape the old dict-by-filename comprehension swallowed."""
        from packages.orchestration.run_manifest import _validate_episode_ledgers_anchored
        import os

        base = _bind_artifact_refs(T._mk(episode_id="ep1", calls=(T._call(seq=1),)))
        lg = base.call_ledgers[0]
        twinned = dataclasses.replace(base, call_ledgers=(lg, lg))
        d = tmp_path / "ep"
        (d / LEDGERS_SUBDIR).mkdir(parents=True)
        (d / LEDGERS_SUBDIR / lg.ref().split("/", 1)[1]).write_bytes(lg.canonical_bytes())
        fd = os.open(str(d), os.O_RDONLY)
        try:
            probs = _validate_episode_ledgers_anchored(fd, "ep1", twinned)
        finally:
            os.close(fd)
        assert any("both claim artifact" in p for p in probs), probs

    def test_the_published_reference_refuses_the_duplicate_too(self):
        base = _bind_artifact_refs(T._mk(episode_id="ep1", calls=(T._call(seq=1),)))
        lg = base.call_ledgers[0]
        assert validate_run_manifest(dataclasses.replace(base, call_ledgers=(lg, lg)),
                                     mode=MODE_PUBLISHED_REFERENCE)
