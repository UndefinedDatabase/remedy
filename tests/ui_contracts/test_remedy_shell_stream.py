"""Contract tests for the cockpit's subscription to the brain stream.

RemedyShell is where the two halves of F008 meet: the client the T003 rounds
built is handed the real endpoints T001 and T002 serve, and its status reaches
the badge. This repository has no DOM environment, so the wiring is gated the
way every other component here is gated — by reading its source. Every
assertion runs against COMMENT-STRIPPED source, because a guard that counted a
token inside a comment would be satisfied by the prose describing the code
rather than by the code (finding R-0584).
"""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SHELL = REPO_ROOT / "apps" / "ui" / "src" / "components" / "shell" / "RemedyShell.tsx"
DEPS = REPO_ROOT / "apps" / "ui" / "src" / "api" / "brainStreamDeps.ts"


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
    def test_stripper_removes_a_comment_the_shell_really_carries(self):
        raw = SHELL.read_text()
        assert "// The cockpit subscribes HERE" in raw, "the wiring must keep its WHY comment"
        assert "The cockpit subscribes HERE" not in strip_ts_comments(raw), "stripper must remove it"


class TestShellSubscribesToTheStream:
    def test_shell_subscribes_with_the_dashboard_job_id(self):
        code = strip_ts_comments(SHELL.read_text())
        assert "useBrainStream(dashboard.jobId," in code, (
            "the shell must subscribe with the loaded dashboard's own job id, which "
            "is the reason the call sits here and not in RemedyApp (DECISION F008 D3)"
        )

    def test_shell_builds_its_deps_from_the_real_factory_and_the_browser_env(self):
        code = strip_ts_comments(SHELL.read_text())
        assert "createBrainStreamHostDeps(jobId, browserBrainStreamEnv(window))" in code, (
            "the stream must run against the real endpoints, not a stub"
        )

    def test_shell_passes_the_stream_status_to_the_live_panel(self):
        code = strip_ts_comments(SHELL.read_text())
        assert "streamStatus={stream.status}" in code, (
            "the badge cannot say DELAYED unless the transport status reaches it"
        )

    def test_shell_does_not_compose_the_transport_itself(self):
        code = strip_ts_comments(SHELL.read_text())
        assert "createBrainStreamHost(" not in code, (
            "composition belongs to brainStreamSession.ts, where vitest can test it"
        )


class TestBrowserEnvironmentContract:
    def test_env_is_exported_under_its_own_name(self):
        code = strip_ts_comments(DEPS.read_text())
        assert "export function browserBrainStreamEnv(" in code

    def test_env_degrades_rather_than_claiming_liveness(self):
        code = strip_ts_comments(DEPS.read_text())
        assert "Source === undefined ? null" in code, (
            "a runtime with no EventSource must yield a null source, which is the "
            "unsupported the polling fallback engages on"
        )

    def test_env_reads_its_globals_as_an_argument(self):
        code = strip_ts_comments(DEPS.read_text())
        assert "globalThis" not in code, (
            "reading a global directly would put this module beyond the reach of "
            "the node-environment vitest"
        )
