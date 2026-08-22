"""Contract tests for WHERE the recent-ring append lives.

Behaviour is pinned by vitest in brainStream.test.ts; this suite pins the fact
a behavioural test cannot. The append must sit inside `receiveBrainFrame`
behind the replay guard and appear in neither the driver nor the runner
(DECISION F021 D5): a ring appended in `dispatch` passes every behavioural test
and still duplicates a row on reconnect. Assertions run against
COMMENT-STRIPPED source, or prose above a definition would satisfy a guard
meant for the code (finding R-0584).
"""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
API_DIR = REPO_ROOT / "apps" / "ui" / "src" / "api"
STATE = API_DIR / "brainStream.ts"
DRIVER = API_DIR / "brainStreamDriver.ts"
RUNNER = API_DIR / "brainStreamRunner.ts"


def strip_ts_comments(text: str) -> str:
    """Drop // and /* */ comments. These files hold no string literal carrying
    either marker, which is what lets so plain a scanner be trustworthy here."""
    out: list[str] = []
    i, n = 0, len(text)
    while i < n:
        pair = text[i:i + 2]
        if pair == "//":
            nl = text.find("\n", i)
            i = n if nl == -1 else nl
        elif pair == "/*":
            end = text.find("*/", i + 2)
            i = n if end == -1 else end + 2
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def receive_body(code: str) -> str:
    """`receiveBrainFrame` alone, from its signature to the next top-level
    export. Over the WHOLE file the assertions below would pass on an append
    living anywhere in it, which is the defect they exist to catch."""
    start = code.index("export function receiveBrainFrame(")
    return code[start:code.index("\nexport ", start + 1)]


class TestTheGuardsAreReal:
    def test_stripper_removes_a_comment_the_file_really_carries(self):
        raw = STATE.read_text()
        assert "// Pure, framework-free client state" in raw
        assert "Pure, framework-free client state" not in strip_ts_comments(raw)

    def test_the_body_slice_is_narrower_than_the_whole_file(self):
        code = strip_ts_comments(STATE.read_text())
        assert 0 < len(receive_body(code)) < len(code) / 2


class TestAppendSitsBehindTheReplayGuard:
    def test_the_bound_is_a_named_exported_constant(self):
        code = strip_ts_comments(STATE.read_text())
        assert "export const BRAIN_RECENT_LIMIT = 500;" in code

    def test_state_carries_the_ring_and_the_drop_count(self):
        code = strip_ts_comments(STATE.read_text())
        assert "recent: readonly FeedRow[];" in code, "the ring must be readonly"
        assert "recentDropped: number;" in code, "a silent drop is what D5 forbids"

    def test_the_projection_is_called_inside_receive_brain_frame(self):
        body = receive_body(strip_ts_comments(STATE.read_text()))
        assert "feedRowOf(frame)" in body

    def test_the_replay_guard_returns_before_the_append(self):
        body = receive_body(strip_ts_comments(STATE.read_text()))
        guard = body.index("frame.seq <= state.lastSeq) return state;")
        assert guard < body.index("feedRowOf(frame)"), (
            "an append ahead of the guard duplicates a row on reconnect replay"
        )

    def test_the_bound_is_applied_where_the_append_happens(self):
        body = receive_body(strip_ts_comments(STATE.read_text()))
        assert "BRAIN_RECENT_LIMIT" in body


class TestNoSecondAppendSite:
    def test_the_driver_does_not_project_rows(self):
        code = strip_ts_comments(DRIVER.read_text())
        assert "feedRowOf" not in code, "the driver sees frames before the guard"

    def test_the_runner_does_not_project_rows(self):
        code = strip_ts_comments(RUNNER.read_text())
        assert "feedRowOf" not in code, "dispatch runs for replays too"
