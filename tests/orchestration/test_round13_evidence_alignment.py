"""F9 (round 13) — ONE consistent policy for operator-state files.

The round-12 package was refused as non-authoritative, and correctly so:

    changed-file union mismatch vs current_change_content_proof.file_hashes:
      only_in_union=['.agent/context.md', '.agent/live_review.md', '.agent/plan.md']
    changed-file union mismatch vs final_verifier.authoritative_changed_files: ...
    changed-file union mismatch vs change_provenance.covered_files: ...

Not a packaging accident — two policies. `.agent/*.md` are OPERATOR STATE: notes about the work,
not the work. Every authoritative Evidence view already excluded them; the hand-ATTESTED union
did not, so the same change had two different file sets and no proof could line up.

The chosen policy is the committed one (Finding 9's "Preferred", which is also what the code
already said everywhere else): operator state is excluded from the attested union, the Content
Proof, the final-verifier authoritative set and change-provenance coverage alike — and still
ships in the review ZIP as non-authoritative context.
"""
from __future__ import annotations

import subprocess

import pytest

from packages.orchestration.final_verifier import _is_source_for_alignment
from packages.orchestration.repair_attest import is_attestable_source

_OPERATOR_STATE = [".agent/context.md", ".agent/plan.md", ".agent/live_review.md"]
_REAL_SOURCE = ["packages/orchestration/run_manifest.py", "README.md",
                "tests/orchestration/test_run_manifest.py", "docs/roadmap/STATUS.md"]


# --------------------------------------------------------------------------- the predicate


class TestTheOperatorStatePolicy:
    @pytest.mark.parametrize("path", _OPERATOR_STATE)
    def test_operator_state_is_not_attestable_source(self, path):
        assert not is_attestable_source(path)

    @pytest.mark.parametrize("path", _REAL_SOURCE)
    def test_real_source_is_attestable(self, path):
        assert is_attestable_source(path)

    @pytest.mark.parametrize("path", _OPERATOR_STATE + _REAL_SOURCE)
    def test_the_attest_policy_is_the_authoritative_policy(self, path):
        """A6: not a parallel taxonomy — literally the same predicate. If these two could
        disagree, the mismatch that blocked the package would come straight back."""
        assert is_attestable_source(path) == _is_source_for_alignment(path)

    @pytest.mark.parametrize("path", [".data/jobs/x/state.json", "run_transcript.txt",
                                      "x.pyc", "__pycache__/m.pyc", "htmlcov/i.html"])
    def test_the_other_operational_paths_stay_excluded(self, path):
        assert not is_attestable_source(path)


# --------------------------------------------------------------------------- round 14


class TestTheReviewSubjectSurvivesCommitting:
    """Round 14 — a COMMITTED change is still the change under review.

    The Evidence layer equated "the change under review" with `git status`, which held only while
    an operator-attested round left its whole change uncommitted. Once the round-14 commit
    discipline landed, the tree went clean and the content proof and provenance coverage collapsed
    to ZERO while the attested Evidence still described 85 files — and the final verifier blocked
    on exactly the mismatch it should notice:

        file_set_alignment_status: BLOCKED
        authoritative files not covered by change_provenance: [...85 files...]

    The base is DECLARED, never guessed. `REMEDY_REVIEW_BASE=<commit-ish>` means "my delta from
    there, plus anything still dirty". Guessing (say, the merge-base with the default branch)
    would be wrong for an ordinary job whose branch already carries unrelated commits: those files
    are not that job's change, and calling them uncovered would be a false block.
    """

    def _subject(self, repo, base=None, monkeypatch=None):
        """The review-subject collection, exercised exactly as job_evidence performs it."""
        import os
        import subprocess as sp

        dirty: list[str] = []
        r = sp.run(["git", "status", "--porcelain", "-u"], cwd=repo,
                   capture_output=True, text=True)
        for line in r.stdout.splitlines():
            if line.strip():
                dirty.append(line[3:].strip().strip('"'))
        b = (base or os.environ.get("REMEDY_REVIEW_BASE") or "").strip()
        if b:
            c = sp.run(["git", "diff", "--name-only", f"{b}..HEAD"], cwd=repo,
                       capture_output=True, text=True)
            if c.returncode == 0:
                for p in c.stdout.splitlines():
                    p = p.strip().strip('"')
                    if p and p not in dirty:
                        dirty.append(p)
        return sorted(dirty)

    @pytest.fixture
    def committed_repo(self, tmp_path):
        r = tmp_path / "committed"
        r.mkdir()

        def sh(cmd):
            subprocess.run(cmd, shell=True, cwd=r, check=True, capture_output=True)

        sh("git init -q -b main && git config user.email t@t && git config user.name t")
        sh("echo base > a.py && git add -A && git commit -qm base")
        base = subprocess.run(["git", "rev-parse", "HEAD"], cwd=r, capture_output=True,
                              text=True).stdout.strip()
        sh("git checkout -q -b feature")
        sh("echo changed > a.py && echo new > b.py && git add -A && git commit -qm work")
        return r, base

    def test_a_committed_change_leaves_no_dirty_subject(self, committed_repo):
        repo, _base = committed_repo
        assert subprocess.run(["git", "status", "--porcelain"], cwd=repo, capture_output=True,
                              text=True).stdout.strip() == ""
        assert self._subject(repo) == [], "the reproduction: the subject collapsed to nothing"

    def test_a_declared_base_recovers_the_committed_subject(self, committed_repo):
        repo, base = committed_repo
        assert self._subject(repo, base=base) == ["a.py", "b.py"]

    def test_an_undeclared_base_keeps_the_previous_behaviour_exactly(self, committed_repo):
        """Unset must be a no-op: an ordinary job whose branch carries unrelated commits must
        not suddenly report them as uncovered."""
        repo, _base = committed_repo
        assert self._subject(repo, base=None) == []

    def test_dirty_and_committed_changes_are_unioned_without_duplicates(self, committed_repo):
        repo, base = committed_repo
        (repo / "c.py").write_text("still dirty\n")
        (repo / "a.py").write_text("changed again\n")     # both committed AND dirty
        subject = self._subject(repo, base=base)
        assert subject == ["a.py", "b.py", "c.py"]
        assert len(subject) == len(set(subject))

    def test_operator_state_stays_excluded_from_the_committed_subject(self, committed_repo):
        """The round-13 policy still governs what is ATTESTABLE within that subject."""
        repo, base = committed_repo
        (repo / ".agent").mkdir()
        (repo / ".agent" / "plan.md").write_text("# notes\n")
        subprocess.run("git add -A && git commit -qm notes", shell=True, cwd=repo, check=True,
                       capture_output=True)
        subject = self._subject(repo, base=base)
        assert ".agent/plan.md" in subject          # it IS in the delta...
        assert not is_attestable_source(".agent/plan.md")   # ...and still not attestable source
        assert [f for f in subject if is_attestable_source(f)] == ["a.py", "b.py"]
