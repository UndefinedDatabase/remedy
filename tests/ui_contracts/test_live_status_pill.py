"""Contract tests for the LiveStatusPill's transport-status variants.

The pill is the surface this feature's acceptance condition names: the polling
fallback must label itself visibly instead of pretending to be live. There is no
DOM environment here, so the pill is gated as every other component is — by
reading its COMMENT-STRIPPED source, since a guard counting a token inside a
comment is satisfied by the prose describing the code rather than by the code
(R-0584). The stripper is the hook contract's, so the concept is spelled once.
"""
from __future__ import annotations

from pathlib import Path

from .test_brain_stream_hook import strip_ts_comments

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PANELS = REPO_ROOT / "apps" / "ui" / "src" / "components" / "panels"
PILL = PANELS / "LiveStatusPill.tsx"
PANEL = PANELS / "RightLivePanel.tsx"
PANEL_CSS = PANELS / "RightLivePanel.module.css"


class TestLiveStatusPillVariants:
    def test_a_delayed_stream_says_delayed(self):
        code = strip_ts_comments(PILL.read_text())
        assert '"DELAYED"' not in code, "the label is rendered text, not a string prop"
        assert "DELAYED" in code, "the fallback must label itself visibly"
        assert 'streamStatus === "delayed"' in code, "DELAYED is reached by the transport status"

    def test_a_reconnecting_stream_says_so_rather_than_live(self):
        code = strip_ts_comments(PILL.read_text())
        assert "RECONNECTING" in code
        assert 'streamStatus === "reconnecting"' in code

    def test_the_transport_status_is_read_before_the_dashboard_liveness(self):
        code = strip_ts_comments(PILL.read_text())
        delayed = code.index('streamStatus === "delayed"')
        dashboard = code.index("liveDot")
        assert delayed < dashboard, "a delayed client must not fall through to LIVE"

    def test_the_pill_still_reports_the_dashboard_liveness(self):
        code = strip_ts_comments(PILL.read_text())
        assert "LIVE" in code and "IDLE" in code, "the fallback arm must survive"

    def test_each_variant_lights_its_own_dot(self):
        css = PANEL_CSS.read_text()
        assert ".delayedDot" in css, "DELAYED needs a dot rule or it renders unstyled"
        assert ".reconnectingDot" in css


class TestRightLivePanelPassesTheStatusDown:
    def test_the_panel_hands_the_pill_a_stream_status(self):
        code = strip_ts_comments(PANEL.read_text())
        assert "streamStatus={streamStatus}" in code, "or the pill can never see one"

    def test_the_panel_accepts_the_status_from_its_own_caller(self):
        code = strip_ts_comments(PANEL.read_text())
        assert "streamStatus?: BrainStreamStatus | null" in code
