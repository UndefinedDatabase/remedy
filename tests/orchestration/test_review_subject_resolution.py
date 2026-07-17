"""F3/F5 (round 15) — the review subject is typed, verified, and resolved by PRODUCTION.

Round 14 inlined three git commands in `job_evidence` and tested them with a `_subject()` helper
that re-implemented the same commands. That tests the copy, not the product: the helper could stay
green while production drifted, and it did not exercise a single failure path.

These tests call `resolve_review_subject` — the one helper every consumer uses — and cover what
the inline version silently got wrong:

* an invalid base returned exit 128 and was IGNORED, quietly shrinking the review to the dirty
  tree with no error anywhere;
* a non-ancestor base was accepted, dragging another branch's files into the review.

Both are now blocking errors, because a review whose base is unknown or wrong is not a review.
"""
from __future__ import annotations

import subprocess

import pytest

from packages.orchestration.review_subject import (
    REVIEW_BASE_ENV,
    STATUS_ADDED,
    STATUS_DIRTY,
    STATUS_MODIFIED,
    ReviewSubjectError,
    resolve_review_subject,
)


def _sh(repo, cmd):
    subprocess.run(cmd, shell=True, cwd=repo, check=True, capture_output=True)


def _rev(repo, ref="HEAD"):
    return subprocess.run(["git", "rev-parse", ref], cwd=repo, capture_output=True,
                          text=True).stdout.strip()


@pytest.fixture
def repo(tmp_path):
    """A feature branch with a committed change, and an unrelated branch to borrow a base from."""
    r = tmp_path / "repo"
    r.mkdir()
    _sh(r, "git init -q -b main && git config user.email t@t && git config user.name t")
    _sh(r, "echo base > base.txt && git add -A && git commit -qm base")
    base = _rev(r)
    _sh(r, "git checkout -q -b other && echo unrelated > other.txt "
           "&& git add -A && git commit -qm other")
    foreign = _rev(r)
    _sh(r, f"git checkout -q {base} && git checkout -q -b feature")
    _sh(r, "echo changed > base.txt && echo new > feature.txt "
           "&& git add -A && git commit -qm work")
    return r, base, foreign


# --------------------------------------------------------------------------- the reproductions


class TestAnInvalidBaseIsBlocking:
    def test_the_reproduced_case(self, repo):
        """`git diff NO_SUCH_BASE..HEAD` exits 128; the inline version ignored it."""
        r, _base, _foreign = repo
        with pytest.raises(ReviewSubjectError) as exc:
            resolve_review_subject(r, "NO_SUCH_BASE")
        assert "does not resolve to a commit" in str(exc.value)

    def test_an_invalid_base_never_degrades_to_the_dirty_tree(self, repo):
        """The dangerous half: a typo'd base must not quietly produce a SMALLER review."""
        r, _base, _foreign = repo
        (r / "dirty.txt").write_text("x\n")
        with pytest.raises(ReviewSubjectError):
            resolve_review_subject(r, "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef")

    @pytest.mark.parametrize("bad", ["NO_SUCH_BASE", "refs/heads/nope", "zzzz", "HEAD~99"])
    def test_every_unresolvable_base_blocks(self, repo, bad):
        r, _base, _foreign = repo
        with pytest.raises(ReviewSubjectError):
            resolve_review_subject(r, bad)


class TestANonAncestorBaseIsBlocking:
    def test_the_reproduced_case(self, repo):
        """`git diff foreign..HEAD` succeeds and lists another branch's files."""
        r, _base, foreign = repo
        raw = subprocess.run(["git", "diff", "--name-only", f"{foreign}..HEAD"], cwd=r,
                             capture_output=True, text=True)
        assert raw.returncode == 0 and "other.txt" in raw.stdout, "the repro must be real"
        with pytest.raises(ReviewSubjectError) as exc:
            resolve_review_subject(r, foreign)
        assert "not an ancestor" in str(exc.value)

    def test_the_error_says_why_it_matters(self, repo):
        r, _base, foreign = repo
        with pytest.raises(ReviewSubjectError) as exc:
            resolve_review_subject(r, foreign)
        assert "not on this branch" in str(exc.value)


# --------------------------------------------------------------------------- the typed facts


class TestTheResolvedSubjectIsATypedFact:
    def test_base_and_head_are_full_shas(self, repo):
        r, base, _foreign = repo
        s = resolve_review_subject(r, base)
        assert len(s.base_commit) == 40 and len(s.head_commit) == 40
        assert s.base_commit == base and s.head_commit == _rev(r)
        assert s.base_is_ancestor is True
        assert s.subject_v == 1

    def test_a_short_base_resolves_to_the_full_sha(self, repo):
        """The environment may SUPPLY an abbreviation; the fact is the full commit."""
        r, base, _foreign = repo
        s = resolve_review_subject(r, base[:8])
        assert s.base_commit == base

    def test_the_committed_change_is_the_subject(self, repo):
        r, base, _foreign = repo
        s = resolve_review_subject(r, base)
        assert s.paths() == ["base.txt", "feature.txt"]
        by = {f.path: f for f in s.files}
        assert by["base.txt"].status == STATUS_MODIFIED
        assert by["feature.txt"].status == STATUS_ADDED
        assert by["feature.txt"].base_sha256 is None
        assert by["feature.txt"].current_sha256

    def test_dirty_changes_union_with_committed_changes(self, repo):
        r, base, _foreign = repo
        (r / "dirty.txt").write_text("uncommitted\n")
        s = resolve_review_subject(r, base)
        assert s.paths() == ["base.txt", "dirty.txt", "feature.txt"]
        assert {f.path: f.status for f in s.files}["dirty.txt"] == STATUS_DIRTY

    def test_a_path_that_is_both_committed_and_dirty_appears_once(self, repo):
        r, base, _foreign = repo
        (r / "base.txt").write_text("changed again\n")
        s = resolve_review_subject(r, base)
        assert s.paths().count("base.txt") == 1
        by = {f.path: f for f in s.files}
        # the working tree is the later truth, but the file's history is not erased
        assert by["base.txt"].status == STATUS_DIRTY
        assert by["base.txt"].base_sha256 is not None

    def test_the_subject_serializes_to_the_documented_schema(self, repo):
        r, base, _foreign = repo
        d = resolve_review_subject(r, base).to_json()
        assert set(d) == {"subject_v", "base_commit", "head_commit", "base_is_ancestor",
                          "commits", "files"}
        assert all(set(f) >= {"path", "status", "base_sha256", "current_sha256"}
                   for f in d["files"])


# --------------------------------------------------------------------------- the legacy path


class TestTheUndeclaredBaseKeepsTheLegacyBehaviour:
    def test_no_declared_base_means_the_dirty_tree_only(self, repo):
        """Unset must be a no-op: an ordinary job whose branch carries unrelated commits must not
        suddenly report them as uncovered."""
        r, _base, _foreign = repo
        (r / "dirty.txt").write_text("x\n")
        s = resolve_review_subject(r, "")
        assert s.paths() == ["dirty.txt"]
        assert s.declared is False
        assert s.base_commit == "" and s.head_commit == ""

    def test_a_clean_tree_with_no_base_is_an_empty_subject(self, repo):
        r, _base, _foreign = repo
        assert resolve_review_subject(r, "").files == ()

    def test_the_top_level_supplies_the_base_explicitly(self, repo, monkeypatch):
        """F6 (round 16): the resolver takes the base as an ARGUMENT and reads no environment.

        It used to read `REMEDY_REVIEW_BASE` itself and then decide, from the process CWD,
        whether the declaration was about the repository it had been handed — which made the CWD
        an authorization token and silently dropped an intentional declaration made from
        elsewhere. The top level reads the operator's declaration exactly once and passes it.
        """
        r, base, _foreign = repo
        monkeypatch.setenv(REVIEW_BASE_ENV, base)
        assert resolve_review_subject(r).declared is False, "the env must not reach the resolver"
        assert resolve_review_subject(r, base).base_commit == base

    def test_a_non_git_directory_with_no_base_is_empty_not_an_error(self, tmp_path):
        d = tmp_path / "plain"
        d.mkdir()
        assert resolve_review_subject(d, "").files == ()

    def test_a_non_git_directory_with_a_declared_base_blocks(self, tmp_path):
        d = tmp_path / "plain2"
        d.mkdir()
        with pytest.raises(ReviewSubjectError):
            resolve_review_subject(d, "abc123")


# --------------------------------------------------------------------------- one implementation


class TestProductionIsTheOnlyImplementation:
    def test_every_consumer_calls_the_shared_resolver(self):
        """F5: no module may re-derive the subject with its own git commands."""
        import inspect

        from packages.orchestration import job_evidence
        src = inspect.getsource(job_evidence)
        assert "resolve_review_subject" in src
        # the round-14 inline reconstruction is gone
        assert 'git", "diff", "--name-only", f"{_base}..HEAD"' not in src
        assert "REMEDY_REVIEW_BASE" not in src, (
            "job_evidence must not read the base itself — the resolver owns that")

    def test_the_env_var_is_read_in_exactly_one_module(self):
        import pathlib
        root = pathlib.Path(__file__).resolve().parents[2]
        hits = []
        for p in list((root / "packages").rglob("*.py")) + list((root / "apps").rglob("*.py")):
            if REVIEW_BASE_ENV in p.read_text(encoding="utf-8", errors="replace"):
                hits.append(p.name)
        assert hits == ["review_subject.py"], hits


class TestAnAmbientDeclarationBelongsToOneRepository:
    """An env var is inherited by every child process; a review base is about ONE repository.

    Observed during round 15: `REMEDY_REVIEW_BASE` was exported for the Remedy repo, a
    verification command ran pytest as a subprocess, a test in it exported evidence for its own
    temporary repo, and `resolve_review_subject` raised because that repo has never heard of
    `b0ba27a`. The export lost its content proof entirely — an unrelated declaration breaking an
    unrelated job.

    Round 15 fixed that by asking whether the process CWD's repository was the one being
    exported. Round 16 (F6) removes the question: the CWD is not a credential, and using it as one
    ALSO discarded an intentional declaration whenever the operator ran from elsewhere — the
    export silently produced an empty legacy subject.

    The resolver now reads no environment at all. A base is passed EXPLICITLY by the top level or
    it is not declared; there is no ambient third state whose applicability must be guessed. An
    unrelated job simply is not handed a base, and children never inherit one
    (`child_env_without_declaration`).
    """

    @pytest.fixture
    def foreign(self, tmp_path):
        r = tmp_path / "foreign"
        r.mkdir()
        _sh(r, "git init -q -b main && git config user.email t@t && git config user.name t")
        _sh(r, "echo x > a.txt && git add -A && git commit -qm init")
        (r / "dirty.txt").write_text("d\n")
        return r

    def test_the_reproduced_case(self, foreign, monkeypatch):
        """A base exported for another repository must not reach this one's evidence at all."""
        monkeypatch.setenv(REVIEW_BASE_ENV, "b0ba27ac40c1d8e92316f09dd54162ec780d7cb5")
        s = resolve_review_subject(foreign)          # no base passed -> none used
        assert s.declared is False
        assert s.paths() == ["dirty.txt"], "the legacy path must still describe the dirty tree"

    def test_the_resolver_never_reads_the_environment(self, foreign, monkeypatch):
        """F6: the environment cannot reach the resolver, from any directory."""
        monkeypatch.setenv(REVIEW_BASE_ENV, "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef")
        monkeypatch.chdir(foreign)
        assert resolve_review_subject(foreign).declared is False

    def test_children_do_not_inherit_the_declaration(self, monkeypatch):
        """The round-15 breakage at its root: a verification subprocess inherited the base."""
        from packages.orchestration.review_subject import child_env_without_declaration

        monkeypatch.setenv(REVIEW_BASE_ENV, "b0ba27a")
        assert REVIEW_BASE_ENV not in child_env_without_declaration()

    def test_the_top_level_reads_the_declaration_exactly_once(self, monkeypatch):
        from packages.orchestration.review_subject import read_declared_base

        monkeypatch.setenv(REVIEW_BASE_ENV, "  b0ba27a  ")
        assert read_declared_base() == "b0ba27a"
        monkeypatch.setenv(REVIEW_BASE_ENV, "   ")
        assert read_declared_base() is None
        monkeypatch.delenv(REVIEW_BASE_ENV)
        assert read_declared_base() is None

    def test_an_explicit_base_is_still_strictly_verified(self, foreign):
        """The finding stays closed: an operator naming a base for THIS repo gets it checked."""
        with pytest.raises(ReviewSubjectError):
            resolve_review_subject(foreign, "b0ba27ac40c1d8e92316f09dd54162ec780d7cb5")

    def test_an_explicit_base_works_from_any_process_cwd(self, repo, monkeypatch, tmp_path):
        """F6's other half: round 15 DISCARDED an intentional declaration when the CWD moved.
        An explicitly passed base is about the repository it is passed with — full stop."""
        r, base, _foreign = repo
        elsewhere = tmp_path / "somewhere-else"
        elsewhere.mkdir()
        monkeypatch.chdir(elsewhere)
        s = resolve_review_subject(r, base)
        assert s.declared is True and s.base_commit == base
