# F021 acceptance read — R38

Tree read at `fa3e29f7`, the C3 commit of this round, on branch
`feature/f021-live-activity-feed`. No product file has changed since `24a6b899`.
Source: the `## Goal & Done` and `## Acceptance` sections of
`docs/roadmap/features/T5_F021.md`, split into 18 clauses — 10 from Goal & Done
and 8 from Acceptance.

Node ids for pytest come from `python3 -m pytest --collect-only -q`
(17671 collected), never from a regex over a `-v` run (R-0611). Five clauses are
pinned only by vitest, whose ids cannot come from that command; those ids come
from `npm run test:unit -- --reporter=json` (218 tests, 218 passed, exit 0) and
carry a `vitest:` prefix. That substitution is DECLARED as this round's
deviation 1.

Statuses: SATISFIED 17 · SATISFIED-WITHOUT-A-TEST 1 · UNSATISFIED 0.

## Goal & Done

| # | clause | path + symbol on disk | status | pin |
|---|---|---|---|---|
| GD1 | "a humanization catalog maps event kinds to plain lines" | `apps/ui/src/api/humanizeCatalog.ts` symbol `STREAM_EVENT_CATALOG`; `apps/ui/src/api/humanize.ts` symbol `humanizeStreamEvent` | SATISFIED | `tests/ui_contracts/test_humanize_catalog.py::TestCatalogCoversTheStreamVocabulary::test_catalog_keys_equal_the_static_stream_vocabulary` |
| GD2 | "a NowCard shows the newest action with an activity dot" | `apps/ui/src/components/panels/AgentNowCard.tsx` symbol `AgentNowCard`; `apps/ui/src/api/actionClass.ts` symbol `newestActionRow` | SATISFIED | `tests/ui_contracts/test_brain_stream_ring.py::TestTheNowCardShowsTheNewestAction::test_the_now_card_reads_the_action_class` |
| GD3 | "feed rows carry their seq" | `apps/ui/src/api/feedRow.ts` symbol `FeedRow` field `seq`, written by `feedRowOf`; rendered by `ActivityFeedCard` through `styles.activityTag` | SATISFIED | `vitest: src/api/feedRow.test.ts` — "feedRowOf over a well-formed envelope carries the frame's own seq rather than any envelope field" |
| GD4 | "click-jump to their node in the graph" | `apps/ui/src/api/feedFocus.ts` symbol `nodeIdForFeedRow`; `apps/ui/src/components/panels/ActivityFeedCard.tsx` symbol `ActivityFeedCard` | SATISFIED | `tests/ui_contracts/test_brain_stream_ring.py::TestAFeedRowJumpsToItsNode::test_the_card_resolves_a_row_through_the_rule` |
| GD5 | "the catalog covers every Part E event kind" | `apps/ui/src/api/humanizeCatalog.ts` symbol `STREAM_EVENT_CATALOG`, gated against the `packages/orchestration` emitters by the AST derivation `static_stream_vocabulary` | SATISFIED | `tests/ui_contracts/test_humanize_catalog.py::TestCatalogCoversTheStreamVocabulary::test_catalog_keys_equal_the_static_stream_vocabulary` |
| GD6 | "unknown kinds render an honest generic line, never vanish" | `apps/ui/src/api/humanize.ts` symbol `humanizeStreamEvent`, its `hasOwnProperty` branch returning the kind's own name plus ` event` | SATISFIED | `vitest: src/api/humanize.test.ts` — "humanizeStreamEvent generic path an uncatalogued kind renders the generic line naming itself" |
| GD7 | "the feed renders fixture streams" | `apps/ui/src/components/panels/ActivityFeedCard.tsx` symbol `ActivityFeedCard`, fed the ring projected in `apps/ui/src/api/brainStream.ts` | SATISFIED | `tests/ui_contracts/test_brain_stream_ring.py::TestTheFeedIsFedFromTheStream::test_the_card_renders_the_rows_and_says_when_it_dropped_some` |
| GD8 | "per the binding CSS" | `apps/ui/src/components/panels/RightLivePanel.module.css` selectors `.activityList` and `.activityItem` | SATISFIED-WITHOUT-A-TEST | nothing in this repository renders CSS, so no suite can read a computed value; the declaration-by-declaration reading is below |
| GD9 | "jump-to-node focuses correctly" | `apps/ui/src/components/panels/RightLivePanel.tsx` symbol `RightLivePanel` hands `onSelectNode` to `ActivityFeedCard`; `apps/ui/src/components/shell/RemedyShell.tsx` symbol `RemedyShell` hands the SAME callback to `BrainGraphStage` | SATISFIED | `tests/ui_contracts/test_brain_stream_ring.py::TestAFeedRowJumpsToItsNode::test_the_panel_hands_the_card_what_the_rule_needs` |
| GD10 | "the steering input renders DISABLED with the honest tooltip until its backing feature exists" | `apps/ui/src/components/panels/ChatInput.tsx` symbol `ChatInput`; `ActivityFeedCard.tsx` constant `STEERING_DISABLED_REASON` | SATISFIED | `tests/ui_contracts/test_brain_stream_ring.py::TestTheSteeringInputIsHonestlyDisabled::test_the_input_and_its_button_are_both_disabled` |

## Acceptance

| # | clause | path + symbol on disk | status | pin |
|---|---|---|---|---|
| A1 | "Catalog coverage complete (the failing-on-new-kind test)" | `tests/ui_contracts/test_humanize_catalog.py` symbols `static_stream_vocabulary` and `extract_catalog_keys`, read against `apps/ui/src/api/humanizeCatalog.ts` | SATISFIED | `tests/ui_contracts/test_humanize_catalog.py::TestCatalogCoversTheStreamVocabulary::test_catalog_keys_equal_the_static_stream_vocabulary` |
| A2 | "goldens for the canonical kinds" | `apps/ui/src/api/humanizeCatalog.ts` symbol `STREAM_EVENT_CATALOG` is the checked-in expected-value table; `humanize.ts` symbol `humanizeStreamEvent` is compared against every entry of it | SATISFIED | `vitest: src/api/humanize.test.ts` — "humanizeStreamEvent over the catalog every catalog entry humanizes to its own value" |
| A3 | "unknown-kind generic renders" | `apps/ui/src/api/humanize.ts` symbol `humanizeStreamEvent`; `apps/ui/src/api/feedRow.ts` symbol `feedRowOf`, which keeps the row instead of dropping it | SATISFIED | `vitest: src/api/feedRow.test.ts` — "feedRowOf on envelopes the client does not control an uncatalogued kind still yields a row, on the generic line" |
| A4 | "Scroll never yanks" | `apps/ui/src/api/feedScroll.ts` symbol `shouldFollowNewest`, called by `ActivityFeedCard` as `shouldFollowNewest(distance)` | SATISFIED | `tests/ui_contracts/test_brain_stream_ring.py::TestTheFeedScrollRuleIsWiredToTheCard::test_the_card_never_scrolls_without_asking_the_rule` |
| A5 | "jump focuses the right node (fixture ids)" | `apps/ui/src/api/feedFocus.ts` symbol `nodeIdForFeedRow`, which reads the task's `nodeId` and never assumes it equals the task id | SATISFIED | `vitest: src/api/feedFocus.test.ts` — "nodeIdForFeedRow reads the task's nodeId and never assumes it equals the task id" |
| A6 | "NowCard tracks action events only" | `apps/ui/src/api/actionClass.ts` symbols `isActionKind` and `newestActionRow`, with `BOOKKEEPING_KINDS` and `BOOKKEEPING_SUFFIXES` naming the excluded subset | SATISFIED | `tests/ui_contracts/test_brain_stream_ring.py::TestTheActionClassIsDocumentedAndHeadless::test_the_inspection_suffixes_are_excluded` |
| A7 | "the dot's recency behavior per tokens" | `apps/ui/src/api/recency.ts` symbol `recencyLevel` with `FRESH_WINDOW_MS` and `QUIET_WINDOW_MS`; `AgentNowCard.tsx` renders `styles.activityDot` carrying `data-recency` | SATISFIED | `tests/ui_contracts/test_brain_stream_ring.py::TestTheActivityDotReadsTheRecencyRule::test_the_liveness_tokens_resolve` |
| A8 | "Steering disabled + tooltip asserted" | `apps/ui/src/components/panels/ChatInput.tsx` symbol `ChatInput`, whose reason reaches the reader through `aria-describedby` and not only through `title` | SATISFIED | `tests/ui_contracts/test_brain_stream_ring.py::TestTheSteeringInputIsHonestlyDisabled::test_the_reason_is_the_binding_sentence` |

## GD8 in full, because a status word is not a reading

T5_F021's binding CSS core names two selectors. The shipped sheet is a CSS
module, so the class names differ by construction. Declaration by declaration,
measured at `fa3e29f7`:

- `max-height:52vh` on `.feed` -> `.activityList { max-height: 52vh }` PRESENT,
  and pinned as literal text by
  `tests/ui_contracts/test_brain_stream_ring.py::TestTheFeedScrollRuleIsWiredToTheCard::test_the_feed_box_can_actually_scroll`.
- `overflow:auto` on `.feed` -> `.activityList { overflow: auto }` PRESENT,
  pinned by that same test.
- `display:flex` on `.feed-row` -> `.activityItem { display: flex }` PRESENT,
  unpinned.
- `width:340px`, `border-radius`, `background`, `backdrop-filter` and
  `box-shadow` are NOT on `.activityList`: they sit on the panel card that wraps
  the scroll box rather than on the box.
- `gap:10px` on `.feed-row` -> `.activityItem { gap: 12px }` DIVERGES by 2px.
- `padding:9px 14px` and the `font: 500 13px/1.45 var(--remedy-font-ui)`
  shorthand are NOT on `.activityItem`; the row's typography is set on its child
  selectors instead (`.activityMeta strong`, `.activityItem p`, `.activityTag`).

Those divergences are REPORTED, not minted (block constraint 3), and they did
not stop the round: the clause has a path and a symbol behind it, so it is not
the "nothing on disk satisfies" case constraint 4 halts on. Whether a 2px gap
and a relocated padding are a deviation from a binding spec or the CSS-module
realization of it is a reviewer's call, not a worker's.

## Two further gaps found while reading, reported and not minted

1. `ActivityFeedCard.tsx` renders the seq inside `styles.activityTag`. No suite
   asserts that render site. GD3 is pinned at the DATA level only: `feedRowOf`
   carries the seq, and a card that stopped printing it would leave every suite
   in this repository passing.
2. `RemedyShell.tsx` hands the SAME `onSelectNode` to `BrainGraphStage` and to
   `RightLivePanel`, which is what makes GD9's "focuses correctly" true. `tsc`
   forces the shell to pass SOMETHING, because the prop is required, but no test
   asserts the two callbacks are one. `grep onSelectNode` over
   `tests/ui_contracts/` returns exactly two hits, both inside the
   card-and-panel pair.
