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
from packages.orchestration.repair_attest import (
    _collect_workspace_diff,
    build_safe_diff_text,
    is_attestable_source,
    parse_safe_diff_paths,
)

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


# --------------------------------------------------------------------------- the real diff


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "repo"
    (r / ".agent").mkdir(parents=True)
    (r / "packages").mkdir()
    subprocess.run("git init -q && git config user.email t@t && git config user.name t",
                   shell=True, cwd=r, check=True)
    (r / "packages" / "mod.py").write_text("original = 1\n")
    (r / ".agent" / "plan.md").write_text("# Plan — step 1\n")
    subprocess.run("git add -A && git commit -qm init", shell=True, cwd=r, check=True)
    # the operator edits BOTH real source and their own state notes
    (r / "packages" / "mod.py").write_text("original = 2\n")
    (r / ".agent" / "plan.md").write_text("# Plan — step 2\n")
    (r / ".agent" / "live_review.md").write_text("# Live Review\n")     # untracked state
    (r / "packages" / "new.py").write_text("fresh = True\n")            # untracked source
    return r


class TestTheAttestedDiffCarriesOnlySource:
    def test_the_reproduced_case(self, repo):
        """The attested union no longer contains the three operator-state files."""
        ws = _collect_workspace_diff(str(repo))
        assert ".agent/plan.md" not in ws.changed_files
        assert ".agent/live_review.md" not in ws.changed_files
        assert set(ws.changed_files) == {"packages/mod.py", "packages/new.py"}

    def test_tracked_and_untracked_state_are_both_excluded(self, repo):
        ws = _collect_workspace_diff(str(repo))
        assert not any(f.startswith(".agent/") for f in ws.changed_files)
        assert not any(str(u["path"]).startswith(".agent/")
                       for u in ws.untracked_file_hashes)

    def test_real_source_is_still_fully_attested(self, repo):
        ws = _collect_workspace_diff(str(repo))
        assert "packages/mod.py" in ws.changed_files          # tracked edit
        assert "packages/new.py" in ws.changed_files          # untracked addition
        assert "original = 2" in ws.tracked_diff

    def test_the_safe_diff_and_the_file_list_are_one_account(self, repo):
        """The packager demands EXACT equality. Filtering only the list would have moved the
        mismatch into the diff: "only_in_diff=['.agent/plan.md']"."""
        ws = _collect_workspace_diff(str(repo))
        safe = build_safe_diff_text(ws.tracked_diff, ws.untracked_file_hashes)
        assert set(parse_safe_diff_paths(safe)) == set(ws.changed_files)

    def test_no_operator_state_hunk_survives_in_the_safe_diff(self, repo):
        ws = _collect_workspace_diff(str(repo))
        safe = build_safe_diff_text(ws.tracked_diff, ws.untracked_file_hashes)
        assert ".agent/plan.md" not in safe
        assert "step 2" not in safe

    def test_a_change_that_is_only_operator_state_attests_nothing(self, tmp_path):
        """Honest edge: if the whole diff is state, there is no source change to attest — an
        empty account, not a fabricated one."""
        r = tmp_path / "only_state"
        (r / ".agent").mkdir(parents=True)
        subprocess.run("git init -q && git config user.email t@t && git config user.name t "
                       "&& echo x > f.txt && git add -A && git commit -qm i",
                       shell=True, cwd=r, check=True)
        (r / ".agent" / "plan.md").write_text("# only notes\n")
        ws = _collect_workspace_diff(str(r))
        assert ws.changed_files == []
        assert build_safe_diff_text(ws.tracked_diff, ws.untracked_file_hashes) == ""

    def test_a_clean_worktree_stays_empty(self, tmp_path):
        r = tmp_path / "clean"
        r.mkdir()
        subprocess.run("git init -q && git config user.email t@t && git config user.name t "
                       "&& echo x > f.txt && git add -A && git commit -qm i",
                       shell=True, cwd=r, check=True)
        ws = _collect_workspace_diff(str(r))
        assert ws.changed_files == []


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
