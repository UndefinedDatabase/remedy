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
UI_SRC = REPO_ROOT / "apps" / "ui" / "src"
STATE = API_DIR / "brainStream.ts"
ROW = API_DIR / "feedRow.ts"
DEPS = API_DIR / "brainStreamDeps.ts"
ACTION = API_DIR / "actionClass.ts"
SCROLL = API_DIR / "feedScroll.ts"
RECENCY = API_DIR / "recency.ts"
CARD = UI_SRC / "components" / "panels" / "ActivityFeedCard.tsx"
CHAT_INPUT = UI_SRC / "components" / "panels" / "ChatInput.tsx"
PANEL = UI_SRC / "components" / "panels" / "RightLivePanel.tsx"
SHELL = UI_SRC / "components" / "shell" / "RemedyShell.tsx"
NOWCARD = UI_SRC / "components" / "panels" / "AgentNowCard.tsx"
DRIVER = API_DIR / "brainStreamDriver.ts"
HOST = API_DIR / "brainStreamHost.ts"
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
        assert "feedRowOf(frame, receivedAtMs)" in body

    def test_the_replay_guard_returns_before_the_append(self):
        body = receive_body(strip_ts_comments(STATE.read_text()))
        guard = body.index("frame.seq <= state.lastSeq) return state;")
        assert guard < body.index("feedRowOf(frame, receivedAtMs)"), (
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


class TestViewPublishesTheRing:
    """The runner half of DECISION F021 D5. These pin the two facts a
    behavioural test states less directly: that the ring reaches the view at
    all, and that its identity is compared by reference rather than rebuilt."""

    def test_the_view_type_carries_the_ring(self):
        code = strip_ts_comments(RUNNER.read_text())
        start = code.index("export interface BrainStreamView {")
        view = code[start:code.index("}", start)]
        assert "recent: readonly FeedRow[];" in view
        assert "recentDropped: number;" in view

    def test_cached_view_is_seeded_from_the_state(self):
        code = strip_ts_comments(RUNNER.read_text())
        init = code[code.index("let cachedView"):code.index("function view()")]
        assert "recent: state.recent," in init, (
            "a fresh [] here is a different array from the initial state's "
            "ring, so the first timer would announce a change nobody made"
        )
        assert "recent: []" not in init

    def test_publish_compares_the_ring_by_reference(self):
        code = strip_ts_comments(RUNNER.read_text())
        body = code[code.index("function publish()"):code.index("function arm(")]
        assert "next.recent === cachedView.recent" in body, (
            "useSyncExternalStore compares with Object.is; a deep compare here "
            "would still hand back a fresh object and re-render forever"
        )
        assert "next.recentDropped === cachedView.recentDropped" in body

    def test_the_runner_still_does_not_project_rows_itself(self):
        code = strip_ts_comments(RUNNER.read_text())
        assert "feedRowOf" not in code, "the projection belongs behind the guard"


class TestTheFeedIsFedFromTheStream:
    """The surface half of DECISION F021 D5. The rows must reach the card by
    being passed DOWN from the one subscription the shell already holds, so
    these pin the path rather than the pixels — this repository has no DOM
    environment and never renders a component in a test."""

    def test_the_shell_hands_the_ring_to_the_panel(self):
        code = strip_ts_comments(SHELL.read_text())
        assert "recent={stream.recent}" in code, (
            "the ring is published on the view but never handed to the panel"
        )
        assert "recentDropped={stream.recentDropped}" in code

    def test_the_panel_hands_the_ring_to_the_card(self):
        code = strip_ts_comments(PANEL.read_text())
        assert "recent={recent}" in code
        assert "recentDropped={recentDropped}" in code

    def test_the_card_renders_the_rows_and_says_when_it_dropped_some(self):
        code = strip_ts_comments(CARD.read_text())
        assert "recent.slice(-LIVE_ROWS_SHOWN).reverse()" in code, (
            "the feed shows the newest rows first"
        )
        assert "recentDropped > 0" in code, (
            "a bounded window that never says it dropped anything is the "
            "silent drop D5 forbids"
        )

    def test_there_is_still_exactly_one_subscription(self):
        calls = 0
        for path in sorted(UI_SRC.rglob("*.ts")) + sorted(UI_SRC.rglob("*.tsx")):
            if path.name.endswith((".test.ts", ".test.tsx")):
                continue
            code = strip_ts_comments(path.read_text())
            calls += code.count("useBrainStream(")
            if path != DEPS:
                assert "EventSource" not in code, (
                    "only brainStreamDeps.ts may construct the transport"
                )
        assert calls == 2, "one definition plus one call, never a second"


class TestTheActionClassIsDocumentedAndHeadless:
    """T5_F021 rules the NowCard over "a documented subset -- heartbeats and
    bookkeeping excluded". Behaviour is pinned by vitest in actionClass.test.ts;
    these pin the facts a behavioural test cannot see, against COMMENT-STRIPPED
    source so that prose above a definition cannot satisfy a guard (R-0584)."""

    def test_the_action_class_stays_headless(self):
        code = strip_ts_comments(ACTION.read_text())
        assert "components/" not in code, (
            "the action class is data the CLI can reuse, not a component import"
        )
        assert "useState" not in code and "useSyncExternalStore" not in code

    def test_the_inspection_suffixes_are_excluded(self):
        code = strip_ts_comments(ACTION.read_text())
        for suffix in ("_inspected", "_read", "_loaded", "_recalled", "_assessed"):
            assert '"' + suffix + '"' in code, (
                suffix + " is bookkeeping the NowCard must stay quiet about"
            )

    def test_an_unknown_kind_stays_in_the_action_class(self):
        code = strip_ts_comments(ACTION.read_text())
        assert "BOOKKEEPING_SUFFIXES.some" in code, (
            "classification is by EXCLUSION: an allow-list would demote every "
            "kind computed at runtime and the NowCard would go quiet"
        )

    def test_the_newest_scan_runs_backwards(self):
        code = strip_ts_comments(ACTION.read_text())
        assert "recent.length - 1" in code, (
            "recent is oldest-first, so the newest action is found from the end"
        )


class TestTheNowCardShowsTheNewestAction:
    """The NowCard half of T5_F021. The card must read the ACTION class rather
    than the raw ring, and the panel must hand it the ring at all -- a card
    wired to nothing renders the pre-stream fallback forever."""

    def test_the_now_card_reads_the_action_class(self):
        code = strip_ts_comments(NOWCARD.read_text())
        assert "newestActionRow" in code, (
            "the NowCard must select through the ACTION class, not the raw ring"
        )
        assert "recent ?? []" in code

    def test_the_panel_hands_the_ring_to_the_now_card(self):
        code = strip_ts_comments(PANEL.read_text())
        assert "<AgentNowCard dashboard={dashboard} recent={recent} />" in code, (
            "the NowCard is wired to nothing and shows the fallback forever"
        )

    def test_the_now_card_falls_back_when_nothing_acted(self):
        code = strip_ts_comments(NOWCARD.read_text())
        assert "liveAction ? liveAction.line : detail" in code, (
            "with no action yet the card still says what the dashboard knows"
        )


class TestTheFeedScrollRuleIsPureAndHeadless:
    """The scroll half of T5_F021. component_spec.md line 86 binds the feed to
    pinned-to-newest-unless-scrolled-up with a new-rows pill, and the rule that
    decides it is a PURE function here because this repository has no DOM in
    which a scroll side effect could be tested at all."""

    def test_the_scroll_rule_is_headless_data(self):
        code = strip_ts_comments(SCROLL.read_text())
        assert "import" not in code, (
            "a rule that imports anything is a component effect in disguise"
        )

    def test_the_rule_never_follows_a_reader_who_scrolled_up(self):
        code = strip_ts_comments(SCROLL.read_text())
        assert "shouldFollowNewest" in code, (
            "the feed must ask before scrolling itself to the newest row"
        )
        assert "isPinnedToNewest" in code

    def test_the_unseen_count_clears_at_the_newest_edge(self):
        code = strip_ts_comments(SCROLL.read_text())
        assert "return FEED_SCROLL_START" in code, (
            "returning to the edge clears the unseen count rather than decrementing it"
        )

    def test_the_unseen_count_accumulates_while_away(self):
        code = strip_ts_comments(SCROLL.read_text())
        assert "prev.unseenRows + arrived" in code, (
            "rows arriving while the reader is away must accumulate unseen"
        )


class TestTheNowCardBadgeTracksTheAgent:
    """R-0652 and DECISION F021 D9. The card's live badge must key on the
    agent's own running flag AND on the recency rule, never on the stream ring
    and never on either source alone: brainStream.ts only appends to `recent`
    and trims it, so a row outlives the job that produced it and a ring-keyed
    badge reads "Live" beside the word "Idle" forever, while recency alone
    reads live for the whole quiet window after a job has ended and renders the
    same words with a fuse instead of a latch."""

    def test_the_badge_is_not_keyed_to_the_ring(self):
        code = strip_ts_comments(NOWCARD.read_text())
        assert "isActive" not in code, (
            "a badge keyed to the ring latches on once any action has arrived"
        )

    def test_the_badge_needs_running_and_recent_together(self):
        code = strip_ts_comments(NOWCARD.read_text())
        assert "isRunning && isLiveByRecency(" in code, (
            "recency alone puts Live beside Idle for the whole quiet window"
        )
        assert "{isLive && <span" in code, (
            "the badge must render the conjunction, not one of its halves"
        )

    def test_the_detail_line_still_prefers_the_newest_action(self):
        code = strip_ts_comments(NOWCARD.read_text())
        assert "liveAction ? liveAction.line : detail" in code, (
            "the R16 wiring stays; only the badge changes"
        )


class TestTheRecencyRuleIsPureAndHeadless:
    """The dot's half of T5_F021 line 63: the activity dot pulses on recency
    and fades to idle after a quiet window. The rule is a PURE function of two
    numbers, so the fade is testable without waiting and without faking time,
    and it never reads a clock of its own."""

    def test_the_recency_rule_is_headless_data(self):
        code = strip_ts_comments(RECENCY.read_text())
        assert "import" not in code, (
            "a rule that imports anything is a component effect in disguise"
        )

    def test_the_rule_reads_no_clock_of_its_own(self):
        code = strip_ts_comments(RECENCY.read_text())
        assert "Date.now" not in code, (
            "now is passed in; a rule reading the clock cannot be tested without one"
        )

    def test_the_pre_stream_state_is_not_idle(self):
        code = strip_ts_comments(RECENCY.read_text())
        assert 'return "none";' in code, (
            "nothing-has-acted-yet is a distinct level from acted-then-went-quiet"
        )

    def test_one_liveness_source_feeds_badge_and_dot(self):
        code = strip_ts_comments(RECENCY.read_text())
        assert "isLiveByRecency" in code, (
            "the badge and the dot must share one rule or they will disagree (R-0652)"
        )


class TestTheTransportClockIsInjected:
    """T5_F021's activity dot needs to know how long ago the agent last acted.
    The envelope's own `timestamp` is a server-clock STRING that ui_server.py
    passes through unparsed, and empty when the run log carries none, so the
    dot is stamped on ARRIVAL instead — both operands on one clock, so a skewed
    server can never read as a dead agent. That stamp is only honest if the
    clock is injected: a module calling Date.now() directly cannot be tested
    without waiting for real time, and this suite pins the seam rather than the
    value."""

    def test_the_host_contract_asks_for_a_clock(self):
        code = strip_ts_comments(HOST.read_text())
        assert "now(): number;" in code, (
            "BrainStreamHostDeps must name the clock it is handed"
        )

    def test_the_environment_carries_the_clock_to_the_deps(self):
        code = strip_ts_comments(DEPS.read_text())
        assert "return env.now();" in code, (
            "createBrainStreamHostDeps forwards the injected clock, never its own"
        )

    def test_the_browser_environment_reads_the_clock_off_its_global(self):
        code = strip_ts_comments(DEPS.read_text())
        assert "return globals.Date.now();" in code, (
            "the one real clock is bound from the injected global, as EventSource is"
        )

    def test_no_module_in_the_transport_chain_calls_the_clock_directly(self):
        for path in (HOST, DEPS, DRIVER, STATE):
            code = strip_ts_comments(path.read_text())
            assert "Date.now()" not in code.replace("globals.Date.now()", ""), (
                f"{path.name} reads a real clock; inject it instead"
            )


class TestEveryFrameIsStampedOnArrival:
    """The dot subtracts two numbers, so a frame must reach the client carrying
    one. The stamp is taken in the HOST — the one place a real clock legitimately
    lives — and travels on the transport event, so the driver stays a pure
    reducer and the ring can read the instant without asking what time it is.
    Pinning the SEAM rather than a value: a behavioural test cannot see which
    clock the number came from."""

    def test_the_transport_event_carries_the_arrival_stamp(self):
        code = strip_ts_comments(DRIVER.read_text())
        assert "receivedAtMs: number" in code, (
            "the frame event must declare the stamp it carries"
        )

    def test_the_host_stamps_from_the_injected_clock(self):
        code = strip_ts_comments(HOST.read_text())
        assert "receivedAtMs: deps.now()" in code, (
            "the stamp comes from the injected clock, never a real one"
        )

    def test_the_driver_does_not_stamp_anything_itself(self):
        code = strip_ts_comments(DRIVER.read_text())
        assert "now()" not in code, (
            "the driver is a pure reducer; only the host reads a clock"
        )

    def test_only_one_module_dispatches_a_stamped_frame(self):
        sites = 0
        for path in (HOST, DRIVER, STATE, DEPS):
            sites += strip_ts_comments(path.read_text()).count('kind: "frame", frame')
        assert sites == 1, (
            f"exactly one dispatch site may stamp a frame, found {sites}"
        )


class TestTheRingCarriesTheArrivalStamp:
    """R23 stamped the transport event; this pins the rest of the path. The ring
    is where the stamp becomes durable, so `feedRowOf` must TAKE it rather than
    read a clock, `receiveBrainFrame` must thread it, and the driver must hand
    over the event's own stamp. A behavioural test sees the number and not its
    provenance, which is why the seam is pinned here."""

    def test_the_projection_takes_the_stamp_rather_than_reading_a_clock(self):
        code = strip_ts_comments(ROW.read_text())
        assert "receivedAtMs: number" in code, (
            "FeedRow must declare the stamp and feedRowOf must take it"
        )
        assert "Date.now()" not in code, (
            "feedRow.ts must never read a real clock; the host stamps"
        )

    def test_the_ring_threads_the_stamp_into_the_row(self):
        code = strip_ts_comments(STATE.read_text())
        assert "feedRowOf(frame, receivedAtMs)" in code, (
            "receiveBrainFrame must pass the arrival instant to the projection"
        )

    def test_the_driver_hands_over_the_events_own_stamp(self):
        code = strip_ts_comments(DRIVER.read_text())
        assert "receiveBrainFrame(state, event.frame, event.receivedAtMs)" in code, (
            "the driver must thread the transport event's stamp, not invent one"
        )


class TestTheActivityDotReadsTheRecencyRule:
    """T5_F021 line 62: the NowCard's activity dot pulses on recency and fades
    to idle after a quiet window. The rule is `recency.ts` and it is pure, so
    what a behavioural test cannot see is WHERE the card gets its two operands.
    Both must sit on ONE clock -- the row's arrival stamp and a `Date.now` the
    card reads itself. The DOT reads the recency level ALONE and answers how
    long since the agent last acted, which stays true after a job ends. The
    BADGE is the conjunction DECISION F021 D9 rules, pinned by
    TestTheNowCardBadgeTracksTheAgent above: recency alone would read live for
    the whole quiet window after a job ends, which is R-0652's rendering with a
    fuse instead of a latch."""

    def test_the_card_reads_the_shared_recency_rule(self):
        code = strip_ts_comments(NOWCARD.read_text())
        assert "recencyLevel(" in code, (
            "the dot must ask recency.ts rather than compare instants itself"
        )

    def test_the_dot_subtracts_the_arrival_stamp(self):
        code = strip_ts_comments(NOWCARD.read_text())
        assert "liveAction.receivedAtMs" in code, (
            "the dot's operand is the arrival stamp, never the server's string"
        )

    def test_the_card_ticks_its_own_clock(self):
        code = strip_ts_comments(NOWCARD.read_text())
        assert "setInterval" in code, (
            "with no tick the dot cannot fade until an unrelated render happens"
        )
        assert "clearInterval" in code, (
            "an interval a component never clears outlives the component"
        )

    def test_the_level_reaches_the_dom_as_data(self):
        code = strip_ts_comments(NOWCARD.read_text())
        assert "data-recency={level}" in code, (
            "the level must reach the markup, or the CSS has nothing to select"
        )

    def test_the_dot_css_covers_every_level(self):
        css = (UI_SRC / "components" / "panels" / "RightLivePanel.module.css").read_text()
        for level in ("none", "fresh", "fading", "idle"):
            assert f'.activityDot[data-recency="{level}"]' in css, (
                f"the {level} level renders unstyled"
            )
        assert "--remedy-dur-pulse" in css, (
            "the pulse must use the motion token, not a literal duration"
        )

    def test_the_liveness_tokens_resolve(self):
        tokens = (UI_SRC / "styles" / "tokens.css").read_text()
        assert "--remedy-live:" in tokens, (
            "assets_spec.md line 178 names a token this file must define"
        )
        assert "--remedy-dur-pulse:" in tokens, (
            "motion_spec.md line 13 gives the LIVE dot a 1600ms pulse token"
        )

class TestTheFeedScrollRuleIsWiredToTheCard:
    """DECISION F021 D10 and T5_F021's scroll clause. feedScroll.ts was pure and
    UNIMPORTED from R17 until R31: every function it exports was covered by
    vitest and reachable from no screen, which is a rule that ships unread. This
    suite pins the wiring a repository with no DOM cannot execute."""

    def test_the_card_imports_the_rule_rather_than_reimplementing_it(self):
        code = strip_ts_comments(CARD.read_text())
        assert 'from "../../api/feedScroll"' in code, (
            "the scroll rule lives in feedScroll.ts; a card that re-derives it "
            "leaves the tested copy unread"
        )

    def test_the_card_never_scrolls_without_asking_the_rule(self):
        code = strip_ts_comments(CARD.read_text())
        assert "shouldFollowNewest(distance)" in code, (
            "the follow branch must be guarded by the rule, or a reader who "
            "scrolled up gets yanked to the newest row"
        )

    def test_the_distance_is_measured_from_the_edge_the_rows_render_at(self):
        code = strip_ts_comments(CARD.read_text())
        assert "recent.slice(-LIVE_ROWS_SHOWN).reverse()" in code
        assert "boxRef.current.scrollTop" in code, (
            "rows render newest FIRST, so the newest edge is scrollTop 0 "
            "(DECISION F021 D10); measuring from the bottom would invert the rule"
        )

    def test_the_unseen_count_comes_from_the_rule(self):
        code = strip_ts_comments(CARD.read_text())
        assert "nextFeedScroll(prev" in code, (
            "the unseen count must come from the pure rule, which clears it at "
            "the edge, rather than from a counter the component increments"
        )

    def test_the_jump_to_live_affordance_is_rendered(self):
        code = strip_ts_comments(CARD.read_text())
        assert "shouldShowNewRowsPill(scrollState)" in code, (
            "the pill appears only when the rule says rows went unseen"
        )
        assert "Jump to live" in code, (
            "T5_F021 binds the wording; an arrow pointing down would point away "
            "from the newest edge under DECISION F021 D10"
        )

    def test_the_feed_box_can_actually_scroll(self):
        css = (UI_SRC / "components" / "panels" / "RightLivePanel.module.css").read_text()
        assert "max-height: 52vh" in css, (
            "T5_F021's binding CSS fixes the feed box at 52vh"
        )
        assert "overflow: auto" in css, (
            "a box that cannot overflow makes every scroll rule unreachable"
        )


class TestAFeedRowJumpsToItsNode:
    """T003's click-jump, gated by source because there is no DOM here.

    The rule itself is `nodeIdForFeedRow` and has its own vitest neighbour.
    What no vitest run can see is whether the COMPONENT calls it, which is the
    half that was missing when `feedScroll.ts` sat pure, tested and imported by
    nothing for fourteen rounds."""

    def test_the_card_resolves_a_row_through_the_rule(self):
        code = strip_ts_comments(CARD.read_text())
        assert "nodeIdForFeedRow(row, tasks)" in code, (
            "the row must be resolved by the shared rule, not by a second "
            "mapping the component invents (DECISION F021 D2)"
        )

    def test_only_a_resolvable_row_becomes_a_button(self):
        code = strip_ts_comments(CARD.read_text())
        assert "onClick={() => onSelectNode(nodeId)}" in code, (
            "a clickable row emits focus for the node it resolved"
        )
        # The conditional is the honesty: a row that cannot jump must not
        # render an affordance that says it can.
        assert "return nodeId ? (" in code, (
            "a row with no linkage stays the article it always was"
        )

    def test_the_panel_hands_the_card_what_the_rule_needs(self):
        # Anchored to the ActivityFeedCard ELEMENT, never to the file: the
        # TaskChecklistCard line beside it has carried both of these props
        # since long before F021, so a file-wide search would pass at a base
        # where the feed gets neither.
        panel = strip_ts_comments(PANEL.read_text())
        element = [l for l in panel.splitlines() if "<ActivityFeedCard" in l]
        assert len(element) == 1, "expected exactly one ActivityFeedCard element"
        assert "tasks={dashboard.tasks}" in element[0], (
            "the resolution reads the task list the dashboard already carries"
        )
        assert "onSelectNode={onSelectNode}" in element[0], (
            "the feed focuses the same graph store the checklist already does"
        )

    def test_the_jump_row_has_its_button_reset(self):
        css = (UI_SRC / "components" / "panels" / "RightLivePanel.module.css").read_text()
        assert ".activityItemJump" in css, (
            "a button carrying a row needs its chrome removed or the feed "
            "renders two visually different kinds of row"
        )


class TestTheSteeringInputIsHonestlyDisabled:
    """The steering input ships VISIBLE and INERT until F030 gives it a back
    end. ux_spec.md §11.3 is binding for this surface and fixes both the
    placement and the sentence; DECISION F021 D11 records why that wording
    rather than the feature file's shorter paraphrase."""

    REASON = "Steering arrives with a later feature — watching only for now."

    def test_the_component_exists_where_the_spec_puts_it(self):
        assert CHAT_INPUT.exists(), (
            "component_spec.md names components/panels/ChatInput.tsx so that "
            "enabling steering later is a change in one file"
        )

    def test_the_input_and_its_button_are_both_disabled(self):
        code = strip_ts_comments(CHAT_INPUT.read_text())
        # Two controls, so two disabled attributes: an enabled send button
        # beside a dead field would still promise something it cannot do.
        assert code.count("disabled={disabled}") == 2, (
            "the field and the send button are both inert until F030"
        )

    def test_the_reason_is_the_binding_sentence(self):
        card = strip_ts_comments(CARD.read_text())
        assert self.REASON in card, (
            "ux_spec.md §11.3 fixes this sentence; a paraphrase would make the "
            "design reference and the shipped surface disagree"
        )

    def test_the_reason_reaches_the_reader_and_not_only_the_tooltip(self):
        code = strip_ts_comments(CHAT_INPUT.read_text())
        # A title attribute alone is invisible to a keyboard or screen-reader
        # user, which is the reader most likely to wonder why nothing happens.
        assert "aria-describedby" in code, (
            "the honest reason is announced, not only hovered"
        )

    def test_the_card_renders_it(self):
        card = strip_ts_comments(CARD.read_text())
        # Both branches: the live feed and the pre-stream fallback. A reader
        # who has not started a job must see the same honest surface.
        assert card.count("<ChatInput disabled") == 2, (
            "the input belongs to the card, not to one of its two branches"
        )
