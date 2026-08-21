"""Contract tests for the useBrainStream hook and the session it is thin over.

The hook is the one piece of the SSE client React owns, and this repository has
no DOM environment, so it is gated the way every other component here is gated:
by reading its source. Every assertion runs against COMMENT-STRIPPED source —
these files carry a WHY comment above each definition, and a guard that counted
a token inside a comment would be satisfied by the prose describing the code
rather than by the code (finding R-0584).
"""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
API_DIR = REPO_ROOT / "apps" / "ui" / "src" / "api"
HOOK = API_DIR / "useBrainStream.ts"
SESSION = API_DIR / "brainStreamSession.ts"


def strip_ts_comments(text: str) -> str:
    """Drop // and /* */ comments. These files contain no string literal holding
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


class TestCommentStripping:
    def test_stripper_removes_a_comment_the_file_really_carries(self):
        raw = HOOK.read_text()
        assert "// The React half" in raw, "the hook must keep its WHY comment"
        assert "The React half" not in strip_ts_comments(raw), "stripper must remove it"


class TestBrainStreamHookContract:
    def test_hook_file_exists(self):
        assert HOOK.is_file(), "useBrainStream.ts not found"

    def test_hook_is_exported_under_its_own_name(self):
        code = strip_ts_comments(HOOK.read_text())
        assert "export function useBrainStream(" in code, "the hook must be exported"

    def test_hook_reads_the_runner_as_an_external_store(self):
        code = strip_ts_comments(HOOK.read_text())
        assert "useSyncExternalStore(" in code, (
            "the hook must subscribe to the runner store rather than hold state"
        )

    def test_hook_closes_the_session_on_unmount(self):
        code = strip_ts_comments(HOOK.read_text())
        assert "session.close()" in code, (
            "the hook must close the session, or a remount leaks one EventSource"
        )
        assert "return () => { session.close(); };" in code, (
            "the close must be an effect CLEANUP, which is what unmount runs"
        )

    def test_hook_does_not_compose_the_transport_itself(self):
        code = strip_ts_comments(HOOK.read_text())
        assert "createBrainStreamHost" not in code, (
            "composition belongs to brainStreamSession.ts, where vitest can test it"
        )


class TestBrainStreamSessionContract:
    def test_session_file_exists(self):
        assert SESSION.is_file(), "brainStreamSession.ts not found"

    def test_session_is_exported_under_its_own_name(self):
        code = strip_ts_comments(SESSION.read_text())
        assert "export function createBrainStreamSession(" in code

    def test_session_close_stops_the_runner_and_the_socket(self):
        code = strip_ts_comments(SESSION.read_text())
        assert "runner.stop();" in code, "close must stop the runner"
        assert "host.close();" in code, "close must also close the socket"
