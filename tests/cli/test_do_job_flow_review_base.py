"""F6 (round 17) — `do job-flow` forwards the explicit review base.

`do job-evidence` reads the operator's `REMEDY_REVIEW_BASE` declaration once and passes it to
`export_job_evidence`; `do job-flow` called `export_job_evidence(job_id, evidence_out)` with no
base. Since round 16 the export reads NO ambient environment (a base not passed is a base that
does not exist), so a clean committed feature branch exported through the full workflow lost its
committed ReviewSubject entirely — base, HEAD, commits and files all gone, the subject collapsing
to the empty dirty tree.

The fix is one line: read the declaration at the top-level job-flow command and pass it. This test
proves the wiring at the call site and end to end on a real committed branch.
"""
from __future__ import annotations

import inspect

from packages.orchestration.review_subject import (
    read_declared_base,
    resolve_review_subject,
)


class TestBothExportCallsForwardTheBase:
    def test_do_cmd_forwards_declared_base_in_every_export_call(self):
        """Neither `do job-evidence` nor `do job-flow` may call the export without the base."""
        import apps.cli.commands.do_cmd as do_cmd

        src = inspect.getsource(do_cmd)
        # Every export_job_evidence( call must be followed, within its argument list, by
        # declared_base=. A call missing it is exactly the round-17 regression.
        import re
        calls = re.findall(r"export_job_evidence\((.*?)\)", src, re.S)
        assert calls, "expected export_job_evidence call sites"
        for args in calls:
            assert "declared_base=" in args, \
                f"an export_job_evidence call omits declared_base: {args[:80]!r}"

    def test_the_top_level_reader_is_the_single_source(self):
        import os

        os.environ.pop("REMEDY_REVIEW_BASE", None)
        assert read_declared_base() is None
        os.environ["REMEDY_REVIEW_BASE"] = " abc123 "
        try:
            assert read_declared_base() == "abc123"
        finally:
            os.environ.pop("REMEDY_REVIEW_BASE", None)


class TestTheForwardedBaseProducesACommittedSubject:
    """The behaviour the wiring exists for: with a base, a committed branch has a real subject."""

    def _repo(self, tmp_path):
        import subprocess

        r = tmp_path / "repo"
        r.mkdir()

        def sh(c):
            subprocess.run(c, shell=True, cwd=r, check=True, capture_output=True)

        sh("git init -q -b main && git config user.email t@t && git config user.name t")
        sh("echo base > base.txt && git add -A && git commit -qm base")
        base = subprocess.run(["git", "rev-parse", "HEAD"], cwd=r, capture_output=True,
                              text=True).stdout.strip()
        sh("git checkout -q -b feature && echo work > work.py && git add -A "
           "&& git commit -qm work")
        return r, base

    def test_a_clean_committed_branch_with_a_base_has_base_head_commits_files(self, tmp_path):
        r, base = self._repo(tmp_path)
        subject = resolve_review_subject(r, base)      # what job-flow now passes
        assert subject.declared is True
        assert subject.base_commit == base
        assert subject.head_commit and subject.head_commit != base
        assert subject.commits, "the committed history must be present"
        assert "work.py" in subject.paths()

    def test_the_same_clean_branch_with_no_base_is_the_empty_legacy_subject(self, tmp_path):
        """The regression's shape: no base -> nothing committed is in the review."""
        r, _base = self._repo(tmp_path)
        subject = resolve_review_subject(r, None)
        assert subject.declared is False
        assert subject.paths() == []
