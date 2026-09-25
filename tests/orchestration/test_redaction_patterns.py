"""R-1060 — the `sk-` alternative of `_SECRET_RE` matches only at a TOKEN START.

Before the repair, `sk-[a-zA-Z0-9_-]{8,}` carried no left boundary, so
`find_forbidden_surface_tokens` flagged any ordinary word ending "...sk-":
this branch's own name (`feature/f026-task-edit-runtime`), `risk-assessment-notes`
and `a desk-organizer here`. The fix adds a negative lookbehind for a letter or a
digit, so those three stay clean while a real key is still found wherever it
plausibly starts: after a space, after `=`, inside double quotes, after `/`,
after `-`, and at the very start of the text.
"""
from __future__ import annotations

import pytest

from packages.orchestration.redaction_patterns import find_forbidden_surface_tokens

_KEY = "sk-A1b2C3d4E5f6G7h8"  # "sk-" plus sixteen letters and digits


class TestNoFalsePositiveOnAnOrdinaryWordEndingSk:

    @pytest.mark.parametrize("text", [
        "feature/f026-task-edit-runtime",
        "risk-assessment-notes",
        "a desk-organizer here",
    ])
    def test_no_finding(self, text):
        assert find_forbidden_surface_tokens(text) == []


class TestKeyStillFoundAtEveryTokenStart:

    @pytest.mark.parametrize("text", [
        f"token {_KEY}",
        f"key={_KEY}",
        f'"{_KEY}"',
        f"path/{_KEY}",
        f"prefix-{_KEY}",
        _KEY,
    ])
    def test_finding(self, text):
        findings = find_forbidden_surface_tokens(text)
        assert len(findings) == 1
        assert _KEY in findings[0]
