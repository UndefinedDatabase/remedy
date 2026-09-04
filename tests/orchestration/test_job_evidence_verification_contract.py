"""Red proofs for the evidence-packager verification-run contract (F112 R27).

R-0792: ``output_hash`` must always be sha256 of the exact ``stdout_summary``
bytes AS STORED (post scrub, post truncation) — never of raw/pre-truncation
text, and a caller-supplied hash is never trusted. R-0793:
``job_evidence._scrub_paths`` must catch non-repo/non-home absolute paths via
the shared ``packages.common.path_redaction`` scrubber, without regressing
the R-0790 "+/-" non-match guard.

Covers, per the round 27 step block:
    (a) _run_verifications discards a wrong caller-supplied output_hash and
        always recomputes it from the RETURNED (truncated) stdout_summary.
    (b) job_evidence._scrub_paths redacts a third-party absolute path
        (pytest's own platform banner).
    (c) job_evidence._scrub_paths leaves "5 +/- 2" unchanged (R-0790 guard).
    (d) manual_attestation._vt_run_v11 scrubs and rehashes stdout_summary,
        discarding a wrong caller-supplied output_hash.
"""
from __future__ import annotations

import hashlib

from packages.orchestration.job_evidence import _run_verifications, _scrub_paths
from packages.orchestration.manual_attestation import _vt_run_v11

#: A synthetic but realistic multi-line pytest verbose transcript, well over
#: 2000 characters, carrying real absolute-path text (a rootdir banner and a
#: repo-relative-looking node id block) so scrubbing/truncation have real
#: content to act on — not a repeated filler character.
_LONG_PYTEST_TRANSCRIPT = (
    "============================= test session starts ==============================\n"
    "platform linux -- Python 3.10.12, pytest-9.0.3, pluggy-1.6.0 -- /usr/bin/python3\n"
    "cachedir: .pytest_cache\n"
    "rootdir: /home/decodeux/Repos/remedy\n"
    "configfile: pyproject.toml\n"
    "collected 42 items\n\n"
    + "".join(
        f"tests/orchestration/test_class_prompt_budget.py::test_case_{i:03d} PASSED"
        f" [{i % 100:3d}%]\n"
        for i in range(60)
    )
    + "\n============================= 42 passed in 3.14s =============================\n"
)
assert len(_LONG_PYTEST_TRANSCRIPT) > 2000, "fixture must exceed the 2000-char truncation window"


class TestRunVerificationsOutputHashContract:
    """(a) output_hash always matches the RETURNED, truncated stdout_summary."""

    def test_wrong_caller_supplied_hash_is_discarded_and_recomputed(self):
        wrong_hash = "deadbeef" * 8

        def _runner(command):
            return {
                "exit_code": 0,
                "passed": 42,
                "failed": 0,
                "skipped": 0,
                "selected": 42,
                "deselected": 0,
                "node_ids": [],
                "test_files": ["tests/orchestration/test_class_prompt_budget.py"],
                "stdout_summary": _LONG_PYTEST_TRANSCRIPT,
                "output_hash": wrong_hash,
                "head_sha": "",
                "duration_seconds": 1.23,
            }

        vt = _run_verifications(["python3 -m pytest tests/x.py"], repo=".", runner=_runner)
        assert vt is not None
        run = vt["runs"][0]

        # The returned stdout_summary is truncated to the last 2000 chars —
        # the same equality build_review_manifest.py:2267 checks.
        assert run["stdout_summary"] == _LONG_PYTEST_TRANSCRIPT[-2000:]
        assert run["output_hash"] == hashlib.sha256(
            run["stdout_summary"].encode("utf-8", errors="replace")
        ).hexdigest()
        assert run["output_hash"] != wrong_hash


class TestScrubPathsCatchesThirdPartyAbsolutePaths:
    """(b) job_evidence._scrub_paths delegates to the shared scrubber."""

    def test_third_party_absolute_path_is_redacted(self):
        text = ("platform linux -- Python 3.10.12, pytest-9.0.3, "
                "pluggy-1.6.0 -- /usr/bin/python3")
        result = _scrub_paths(text, repo=".")
        assert "/usr/bin/python3" not in result
        assert "python3" in result


class TestScrubPathsDoesNotRegressPlusMinusGuard:
    """(c) R-0790 regression guard: a bare punctuation tail is not a path."""

    def test_plus_minus_text_is_unchanged(self):
        text = "5 +/- 2"
        assert _scrub_paths(text, repo=".") == text


class TestVtRunV11ScrubsAndRehashes:
    """(d) manual_attestation._vt_run_v11 scrubs paths and always rehashes."""

    def test_scrubs_absolute_path_and_recomputes_hash(self):
        banner = ("platform linux -- Python 3.10.12, pytest-9.0.3, "
                  "pluggy-1.6.0 -- /usr/bin/python3")
        long_summary = _LONG_PYTEST_TRANSCRIPT.replace(
            "cachedir: .pytest_cache", f"cachedir: .pytest_cache\n{banner}"
        )
        wrong_hash = "deadbeef" * 8
        run = {
            "run_id": "vr-0001",
            "command": "python3 -m pytest tests/x.py",
            "exit_code": 0,
            "passed": 42,
            "failed": 0,
            "skipped": 0,
            "selected": 42,
            "deselected": 0,
            "node_ids": [],
            "test_files": ["tests/orchestration/test_class_prompt_budget.py"],
            "stdout_summary": long_summary,
            "output_hash": wrong_hash,
            "head_sha": "",
            "duration_seconds": 1.23,
        }

        result = _vt_run_v11(run)

        assert "/usr/bin/python3" not in result["stdout_summary"]
        assert result["output_hash"] == hashlib.sha256(
            result["stdout_summary"].encode("utf-8", errors="replace")
        ).hexdigest()
        assert result["output_hash"] != wrong_hash
