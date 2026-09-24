"""Contract tests for the brain graph's birth-motion tokens.

The app stylesheet's `--remedy-dur-birth` / `--remedy-ease-soft` must match
`docs/ui/design_reference/tokens.css` byte-exact in VALUE (graph_spec.md §12;
DECISION F019 D1), and the pure schedule module's `BRAIN_BIRTH_MS` constant
must agree with the token's own millisecond value — both are parsed here,
never hard-coded, so a token or constant drifting out of step is the failure
this guard exists to catch.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
APP_TOKENS = REPO_ROOT / "apps" / "ui" / "src" / "styles" / "tokens.css"
REFERENCE_TOKENS = REPO_ROOT / "docs" / "ui" / "design_reference" / "tokens.css"
BRAIN_MOTION = REPO_ROOT / "apps" / "ui" / "src" / "components" / "graph" / "brainMotion.ts"


def _token_value(css_text: str, name: str) -> str:
    match = re.search(rf"{re.escape(name)}\s*:\s*([^;]+);", css_text)
    assert match, f"{name} is not declared"
    return match.group(1).strip()


def _birth_ms_constant(ts_text: str) -> int:
    match = re.search(r"BRAIN_BIRTH_MS\s*=\s*(\d+)", ts_text)
    assert match, "BRAIN_BIRTH_MS is not declared in brainMotion.ts"
    return int(match.group(1))


class TestBrainBirthTokensMatchDesignReference:
    """Both files exist and declare the two tokens graph_spec §12 names."""

    def test_app_sheet_declares_dur_birth(self):
        _token_value(APP_TOKENS.read_text(), "--remedy-dur-birth")

    def test_app_sheet_declares_ease_soft(self):
        _token_value(APP_TOKENS.read_text(), "--remedy-ease-soft")

    def test_dur_birth_value_matches_the_reference(self):
        app_value = _token_value(APP_TOKENS.read_text(), "--remedy-dur-birth")
        reference_value = _token_value(REFERENCE_TOKENS.read_text(), "--remedy-dur-birth")
        assert app_value == reference_value

    def test_ease_soft_value_matches_the_reference(self):
        app_value = _token_value(APP_TOKENS.read_text(), "--remedy-ease-soft")
        reference_value = _token_value(REFERENCE_TOKENS.read_text(), "--remedy-ease-soft")
        assert app_value == reference_value


class TestBrainMotionAgreesWithTheToken:
    """brainMotion.ts's BRAIN_BIRTH_MS is the token's millisecond value, read
    from the token rather than hard-coded, so the two cannot drift silently."""

    def test_birth_ms_equals_the_app_tokens_millisecond_value(self):
        token_value = _token_value(APP_TOKENS.read_text(), "--remedy-dur-birth")
        match = re.match(r"(\d+)ms$", token_value)
        assert match, f"unexpected --remedy-dur-birth value shape: {token_value!r}"
        token_ms = int(match.group(1))
        assert _birth_ms_constant(BRAIN_MOTION.read_text()) == token_ms
