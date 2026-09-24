"""Contract tests for T003 part one: the live wiring (DECISION F019 D5).

The stage now draws `rebuildBrainModel(jobId, seeds, rows)` where `rows` is the
ledger's contiguous prefix, merged from `events-since` pages and the live
stream's ring by `useBrainLedger.ts`. Behaviour is pinned by vitest in
brainLedger.test.ts; this suite pins what no vitest run can see because this
repository has no DOM environment: that the SHELL actually hands the stage its
ring and a page reader, that the STAGE actually reads through the ledger hook
rather than seeding once from the dashboard, and that the hook holds its
in-flight guard in a ref rather than in state. Every assertion runs against
COMMENT-STRIPPED source, imported from test_brain_stream_ring.py (this
repository's own precedent — test_lessons_overlay_contract.py and
test_steering_send_contract.py both import it the same way) rather than
copied, so a prose description above a definition cannot satisfy a guard
meant for the code (finding R-0584).
"""
from __future__ import annotations

from pathlib import Path

from tests.ui_contracts.test_brain_stream_ring import strip_ts_comments

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
UI_SRC = REPO_ROOT / "apps" / "ui" / "src"
SHELL = UI_SRC / "components" / "shell" / "RemedyShell.tsx"
STAGE = UI_SRC / "components" / "graph" / "BrainGraphStage.tsx"
DEPS = UI_SRC / "api" / "brainStreamDeps.ts"
HOOK = UI_SRC / "components" / "graph" / "useBrainLedger.ts"


def _source(path: Path) -> str:
    return strip_ts_comments(path.read_text(encoding="utf-8"))


class TestTheShellWiresTheLedgerReader:
    def test_the_stage_line_carries_the_ring_and_the_page_reader(self):
        shell = _source(SHELL)
        element = [line for line in shell.splitlines() if "<BrainGraphStage" in line]
        assert len(element) == 1, "expected exactly one <BrainGraphStage element"
        assert "recent={" in element[0], (
            "the stage cannot fold live rows it is never handed"
        )
        assert "readEventsPage={readEventsPage}" in element[0], (
            "the stage cannot page a hole shut without a reader"
        )
        assert "onSelectNode={onSelectNode}" in element[0], (
            "R-0664's one shared callback must survive this round's edit"
        )

    def test_the_shell_builds_its_page_reader_through_the_one_path_builder(self):
        shell = _source(SHELL)
        assert "eventsSincePath(" in shell, (
            "a page reader that built its own path would disagree with "
            "brainStreamDeps.ts's `since` about escaping the job id"
        )


class TestThePathIsBuiltInOnePlace:
    def test_events_since_path_is_exported(self):
        deps = _source(DEPS)
        assert "export function eventsSincePath(" in deps

    def test_the_streams_own_since_reads_through_it(self):
        deps = _source(DEPS)
        start = deps.index("export function createBrainStreamHostDeps(")
        end = deps.index("\nexport ", start + 1)
        body = deps[start:end]
        assert "eventsSincePath(jobId, cursor)" in body, (
            "the stream's own snapshot/tail must share the graph's path builder"
        )


class TestTheStageReadsThroughTheLedger:
    def test_the_stage_calls_use_brain_ledger(self):
        assert "useBrainLedger(" in _source(STAGE)

    def test_the_stage_calls_brain_ledger_prefix(self):
        assert "brainLedgerPrefix(" in _source(STAGE)

    def test_the_stage_calls_rebuild_brain_model(self):
        assert "rebuildBrainModel(" in _source(STAGE)

    def test_the_stage_no_longer_seeds_once_and_stops(self):
        assert "seedBrainModel(" not in _source(STAGE), (
            "a stage that still calls seedBrainModel( draws the dashboard seed "
            "forever and never folds a stream frame"
        )


class TestTheHookIsThinAndHasNoTransportOfItsOwn:
    def test_the_hook_calls_brain_ledger_request(self):
        assert "brainLedgerRequest(" in _source(HOOK)

    def test_the_hook_calls_brain_ledger_received(self):
        assert "brainLedgerReceived(" in _source(HOOK)

    def test_the_hook_calls_brain_ledger_live(self):
        assert "brainLedgerLive(" in _source(HOOK)

    def test_the_in_flight_cursor_is_held_in_a_ref(self):
        code = _source(HOOK)
        assert "useRef<number | null>(null)" in code, (
            "a state flip here would change the request effect's own key and "
            "cancel the read it exists to guard"
        )

    def test_the_hook_opens_no_transport_of_its_own(self):
        code = _source(HOOK)
        assert "EventSource" not in code, (
            "only brainStreamDeps.ts may construct the transport"
        )
        assert "fetch(" not in code, (
            "the hook reads through the injected `readPage`, never `fetch` directly"
        )
