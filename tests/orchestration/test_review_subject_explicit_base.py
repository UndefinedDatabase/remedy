"""F6 (round 16) — the review base travels EXPLICITLY; the CWD is not a credential.

Round 15's resolver read `REMEDY_REVIEW_BASE` itself and then asked whether the PROCESS CWD's
repository was the one it had been handed. That was aimed at a real bug (an exported base reached
a pytest subprocess and broke an unrelated job's evidence), but it made the CWD an authorization
token — and tokens cut both ways:

    REMEDY_REVIEW_BASE is set
    repo_root is the intended feature repository
    process CWD is elsewhere
    -> the declaration is silently discarded
    -> an EMPTY legacy subject, with no error

An intentional declaration lost, because of where the operator happened to be standing.

The architecture instead: the resolver reads nothing ambient. The top level reads the operator's
declaration exactly once and passes it, with the repository it belongs to. Children never inherit
it, so an unrelated job is not handed a base at all — the round-15 bug is closed structurally
rather than by guessing.
"""
from __future__ import annotations

import subprocess

import pytest

from packages.orchestration.review_subject import (
    REVIEW_BASE_ENV,
    ReviewSubjectError,
    child_env_without_declaration,
    read_declared_base,
    resolve_review_subject,
)


def _sh(repo, cmd):
    subprocess.run(cmd, shell=True, cwd=repo, check=True, capture_output=True)


def _rev(repo, ref="HEAD"):
    return subprocess.run(["git", "rev-parse", ref], cwd=repo, capture_output=True,
                          text=True).stdout.strip()


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "feature"
    r.mkdir()
    _sh(r, "git init -q -b main && git config user.email t@t && git config user.name t")
    _sh(r, "echo base > base.txt && git add -A && git commit -qm base")
    base = _rev(r)
    _sh(r, "git checkout -q -b feature && echo work > work.py && git add -A "
           "&& git commit -qm work")
    return r, base


@pytest.fixture
def other(tmp_path):
    r = tmp_path / "unrelated"
    r.mkdir()
    _sh(r, "git init -q -b main && git config user.email t@t && git config user.name t")
    _sh(r, "echo x > a.txt && git add -A && git commit -qm init")
    (r / "dirty.txt").write_text("d\n")
    return r


# --------------------------------------------------------------------------- the reproduction


class TestAnExplicitBaseWorksFromAnywhere:
    def test_the_reproduced_case(self, repo, tmp_path, monkeypatch):
        """THE finding: standing elsewhere used to silently produce an empty legacy subject."""
        r, base = repo
        elsewhere = tmp_path / "elsewhere"
        elsewhere.mkdir()
        monkeypatch.chdir(elsewhere)
        s = resolve_review_subject(r, base)
        assert s.declared is True
        assert s.base_commit == base
        assert "work.py" in s.paths(), "the committed delta must still be the subject"

    @pytest.mark.parametrize("where", ["repo", "parent", "tmp"])
    def test_the_cwd_never_changes_the_answer(self, repo, tmp_path, monkeypatch, where):
        r, base = repo
        monkeypatch.chdir({"repo": r, "parent": tmp_path, "tmp": tmp_path}[where])
        s = resolve_review_subject(r, base)
        assert s.declared is True and s.base_commit == base

    def test_the_resolver_reads_no_environment(self, repo, monkeypatch):
        r, base = repo
        monkeypatch.setenv(REVIEW_BASE_ENV, base)
        monkeypatch.chdir(r)
        assert resolve_review_subject(r).declared is False


# --------------------------------------------------------------------------- wrong pairing


class TestAWrongRepositoryBasePairingBlocks:
    def test_a_base_from_another_repository_blocks(self, repo, other):
        """Explicit means verified: a base this repo never heard of is an ERROR, not a shrug."""
        _r, base = repo
        with pytest.raises(ReviewSubjectError):
            resolve_review_subject(other, base)

    def test_a_nonexistent_base_blocks(self, other):
        with pytest.raises(ReviewSubjectError):
            resolve_review_subject(other, "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef")

    def test_a_non_ancestor_base_blocks(self, tmp_path):
        r = tmp_path / "branched"
        r.mkdir()
        _sh(r, "git init -q -b main && git config user.email t@t && git config user.name t")
        _sh(r, "echo a > a.txt && git add -A && git commit -qm root")
        root = _rev(r)
        _sh(r, "git checkout -q -b sideline && echo s > s.txt && git add -A && git commit -qm s")
        side = _rev(r)
        _sh(r, f"git checkout -q {root} && git checkout -q -b feature")
        _sh(r, "echo f > f.txt && git add -A && git commit -qm f")
        with pytest.raises(ReviewSubjectError):
            resolve_review_subject(r, side)

    def test_a_declared_base_in_a_non_git_directory_blocks(self, tmp_path):
        d = tmp_path / "plain"
        d.mkdir()
        with pytest.raises(ReviewSubjectError):
            resolve_review_subject(d, "b0ba27a")

    def test_an_unrelated_job_simply_gets_no_base(self, other):
        """Not "a base it must reject" — no declaration at all, so the legacy path applies."""
        s = resolve_review_subject(other)
        assert s.declared is False
        assert s.paths() == ["dirty.txt"]


# --------------------------------------------------------------------------- the transport


class TestTheDeclarationIsReadOnceAndNotInherited:
    def test_the_top_level_reader(self, monkeypatch):
        monkeypatch.setenv(REVIEW_BASE_ENV, " b0ba27a ")
        assert read_declared_base() == "b0ba27a"

    @pytest.mark.parametrize("value", ["", "   "])
    def test_a_blank_declaration_is_no_declaration(self, monkeypatch, value):
        monkeypatch.setenv(REVIEW_BASE_ENV, value)
        assert read_declared_base() is None

    def test_no_declaration_is_none(self, monkeypatch):
        monkeypatch.delenv(REVIEW_BASE_ENV, raising=False)
        assert read_declared_base() is None

    def test_children_never_inherit_the_declaration(self, monkeypatch):
        """The round-15 breakage at its root: a verification subprocess inherited the base and
        an unrelated job lost its content proof entirely."""
        monkeypatch.setenv(REVIEW_BASE_ENV, "b0ba27a")
        monkeypatch.setenv("SOMETHING_ELSE", "kept")
        env = child_env_without_declaration()
        assert REVIEW_BASE_ENV not in env
        assert env.get("SOMETHING_ELSE") == "kept", "only the declaration is stripped"

    def test_the_scrub_does_not_mutate_the_parent_environment(self, monkeypatch):
        import os

        monkeypatch.setenv(REVIEW_BASE_ENV, "b0ba27a")
        child_env_without_declaration()
        assert os.environ.get(REVIEW_BASE_ENV) == "b0ba27a"

    def test_the_verification_runner_scrubs_the_declaration(self, monkeypatch, tmp_path):
        """End to end through the real runner: the child cannot see the base."""
        from packages.orchestration.job_evidence import _default_verification_runner

        monkeypatch.setenv(REVIEW_BASE_ENV, "b0ba27a")
        out = _default_verification_runner(
            f'python3 -c "import os; print(os.environ.get(\'{REVIEW_BASE_ENV}\', \'ABSENT\'))"',
            str(tmp_path))
        assert "ABSENT" in out["stdout_summary"]
        assert "b0ba27a" not in out["stdout_summary"]
