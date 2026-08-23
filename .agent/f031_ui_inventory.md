# F031 UI Inventory — the ground T002 builds on

Measured by the R9 worker in the primary checkout at `95610316` (C2). Every
value below is one this worker's own command printed; `git diff --name-only
1ec7a330..95610316` names only four paths, all under `.agent/`, so every
reading over `apps/` and `docs/` is identical at the round base `1ec7a330`.

## Q1 — the design authority

Command (Python `os.walk` + `re` over the folder, since the shell guard rejects
the compound `grep`; the pattern is `decision|inbox|queue`, case-insensitive):

    for dirpath, dirs, files in os.walk("docs/ui/design_reference"):
        ... re.compile(r"decision|inbox|queue", re.I).search(line)

The folder holds 17 entries; `ux_design.png` is binary and was skipped, and is
named here rather than silently dropped. Over the 16 text files the pattern hits
22 lines. NONE of them names a decision, inbox or queue COMPONENT:

- `ASSET_INTEGRATION_SUMMARY.md:3,4,33` — "Canonical decisions", an asset table
  column, and a summary sentence. Editorial, not a component.
- `FINAL_CLEANUP_SUMMARY.md:11,15,25` — roadmap redirects; `:15` says
  "F068→F035 (decision-queue data suffices)" and `:25` "F051→F031 (backend queue
  already exists)". Both speak about BACKEND data, not a surface.
- `FINAL_DESIGN_REFERENCE_SUMMARY.md:13` — "Canonical decisions (final)".
- `README.md:31,67` — "every visual decision", "Decision made here".
- `assets_spec.md:44,81,99,149,162,174` — "Canonical decision:" prose, plus the
  glyph table row `| decision | human gate | rounded diamond + dot | r 5 |
  stroke; dot = state | soft warn glow while open |`. This is the ONE piece of
  decision-specific visual authority in the folder, and it is a GRAPH GLYPH, not
  a card.
- `codebase_audit.md:78`, `graph_tech_recommendation.md:47`, `tokens.css:3` —
  renderer/namespace decisions.
- `implementation_plan.md:34` — "queue, `AgentNowCard` crossfade" inside a test
  sentence.
- `ux_spec.md:163` — "lineage): status/digest/inbox surfaces only — out of scope
  here except: do not".

Narrowed to `inbox` alone, the folder has EXACTLY ONE hit: `ux_spec.md:163`,
the out-of-scope line above. Narrowed to `queue`: three hits, all listed above.

`component_spec.md` headings, printed in full (`line.startswith("#")`): `# E —
Component Breakdown`, then `AppShell (RemedyShell)`, `BrandSidebar
(LeftBrandRail)`, `VerticalNavigation (SideIconDock)`, `MetricsBar
(TopMetricsBar)`, `CommandBar`, `GrowingBrainGraph`, `BrainNode / BrainEdge /
BrainCluster / BrainLegend`, `FilterChips (GraphFilterChips)`, `PhaseTimeline +
TimelineScrubber`, `AgentNowCard`, `ActivityFeed (+ chat frame)`,
`SteeringInput / ChatInput`, `TaskList (TaskChecklistCard) / TaskRow /
AddTaskButton`, `DetailPanel / EvidencePanel entry (DetailPopover)`,
`DiffViewer entry point`, `RuntimePreview entry point`, `Shared` — 18 headings,
none a decision, inbox or queue component.

MATCHES the reviewer's reading on both clauses: `component_spec.md` names no
such component, and the only `inbox` string in the folder is the `ux_spec.md`
out-of-scope line. No difference to account for. Added beyond the reviewer's
reading, and relevant to T002: the `assets_spec.md:174` glyph row IS decision
visual authority, for the graph node, not for a card.

## Q2 — the shipped tokens

Command (Python `os.walk` over `apps/ui/src/styles/`, `var(--remedy-…)` usages
stripped from each line BEFORE matching, then the definition pattern
`(--remedy-[A-Za-z0-9_-]+)\s*:`):

    stripped = re.sub(r"var\(\s*--remedy-[A-Za-z0-9_-]+", "", line)
    re.compile(r"(?<!var\()(--remedy-[A-Za-z0-9_-]+)\s*:").finditer(stripped)

The folder holds exactly TWO files: `apps/ui/src/styles/globals.css` and
`apps/ui/src/styles/tokens.css`.

COUNT: 58 distinct `--remedy-*` properties are DEFINED, and every one of them is
defined in `apps/ui/src/styles/tokens.css`. `globals.css` defines ZERO — it only
consumes them. The list, with the defining line:

fonts — `--remedy-font-display` :2, `--remedy-font-ui` :3, `--remedy-font-mono`
:4. ink — `--remedy-ink` :6, `--remedy-ink-strong` :7, `--remedy-ink-soft` :8.
surface — `--remedy-bg` :10, `--remedy-bg-2` :11. blue ramp —
`--remedy-blue-950` :13, `--remedy-blue-900` :14, `--remedy-blue-800` :15,
`--remedy-blue-700` :16, `--remedy-blue-500` :17, `--remedy-blue-300` :18,
`--remedy-blue-100` :19, `--remedy-blue-50` :20, `--remedy-blue` :21,
`--remedy-blue-strong` :22, `--remedy-blue-soft` :23. accents —
`--remedy-cyan-400` :25, `--remedy-green-500` :26, `--remedy-green` :27,
`--remedy-green-50` :28, `--remedy-purple-400` :29, `--remedy-purple` :30,
`--remedy-orange-400` :31, `--remedy-red-500` :32. motion — `--remedy-live` :39,
`--remedy-dur-pulse` :40. lines — `--remedy-line` :42, `--remedy-line-strong`
:43. glass — `--remedy-glass-bg` :45, `--remedy-glass-bg-strong` :46,
`--remedy-glass-border` :47. card — `--remedy-card` :48, `--remedy-card-strong`
:49, `--remedy-card-soft` :50. text — `--remedy-text` :52, `--remedy-muted` :53,
`--remedy-faint` :54. radius — `--remedy-radius-xl` :56, `--remedy-radius-lg`
:57, `--remedy-radius-md` :58, `--remedy-radius-sm` :59, `--remedy-radius-pill`
:63. shadow — `--remedy-shadow-card` :65, `--remedy-shadow-soft` :66,
`--remedy-shadow` :67, `--remedy-glow` :68, `--remedy-glow-strong` :69. layout —
`--remedy-left-width` :71, `--remedy-right-width` :72. state —
`--remedy-state-done` :75, `--remedy-state-current` :76, `--remedy-state-open`
:77, `--remedy-state-planned` :78, `--remedy-state-planned-ring` :79,
`--remedy-state-blocked` :80.

The design reference's own `docs/ui/design_reference/tokens.css` was NOT read
for this answer, as the question directs.

What this means for T002: a decision card needs no new token. The state ramp
already carries `--remedy-state-open` and `--remedy-state-blocked`, which are
exactly the two states a decision card must show, and the card/glass/radius/
shadow families already carry the shell.

## Q3 — the card shell

Read in full: `apps/ui/src/components/panels/NeedsAttentionCard.tsx`, 50 lines by
`wc -l`, 1912 bytes.

CSS module imported: `./RightLivePanel.module.css`, at line 3, as `styles`.

Class names used from it, in source order: `styles.card` (:35),
`styles.cardHeader` (:36), `styles.attentionTitle` (:37), `styles.attentionDesc`
(:38), `styles.attentionAction` (:41) — five.

Root element: `<section>` (:35). Its `data-ui` attribute value is exactly
`needs-attention-card`.

OTHER components importing the SAME module (Python walk over `apps/ui/src` for
the literal `RightLivePanel.module.css`, 7 importers, minus this file = 6):
`ActivityFeedCard.tsx:9`, `AgentNowCard.tsx:8`, `ChatInput.tsx:1`,
`LiveStatusPill.tsx:2`, `RightLivePanel.tsx:11`, `TaskChecklistCard.tsx:4` — all
under `apps/ui/src/components/panels/`.

What this means for T002: `RightLivePanel.module.css` is the shared right-panel
stylesheet, not one card's private sheet, so a decision card joins it rather
than introducing a seventh module.

## Q4 — the test toolchain

VERBATIM from `apps/ui/vitest.config.ts` (8 lines, read in full):

    environment: "node",
    include: ["src/**/*.test.ts"],

The `environment` value is `"node"`. `include` has EXACTLY ONE entry:
`"src/**/*.test.ts"`.

By the config's own glob, run with Python `glob.glob("src/**/*.test.ts",
recursive=True)` from `apps/ui`: 20 files. They are `src/api/actionClass.test.ts`,
`src/api/brainStream.test.ts`, `src/api/brainStreamDeps.test.ts`,
`src/api/brainStreamDriver.test.ts`, `src/api/brainStreamHost.test.ts`,
`src/api/brainStreamRunner.test.ts`, `src/api/brainStreamSession.test.ts`,
`src/api/budgetTick.test.ts`, `src/api/costMetric.test.ts`,
`src/api/costReconciliation.test.ts`, `src/api/costTicker.test.ts`,
`src/api/feedFocus.test.ts`, `src/api/feedRow.test.ts`,
`src/api/feedScroll.test.ts`, `src/api/humanize.test.ts`,
`src/api/recency.test.ts`, `src/api/remedyApi.test.ts`,
`src/cockpitLogic.test.ts`, `src/components/graph/buildForceBrainModel.test.ts`,
`src/components/prompt/promptTraceLens.test.ts`.

`glob.glob("src/**/*.test.tsx", recursive=True)`: 0 files, the empty list.

`apps/ui/package.json` is 34 lines; lines matching `jsdom|happy-dom|
testing-library`: 0.

AGAINST THE REVIEWER'S READING, cell for cell: environment `node` — MATCHES.
One include glob — MATCHES. 20 files matching it — MATCHES. 0 matching the tsx
glob — MATCHES. 0 dependency lines naming a DOM harness — MATCHES (the count is
0 over the WHOLE file, so it is 0 in the dependency blocks a fortiori). There is
no difference to account for.

The gap, stated plainly: nothing in the shipped toolchain can mount a React
component. `environment: "node"` gives no `document`, the include glob collects
no `.tsx`, and no DOM harness is a dependency. A "component test" for T002 is
not a thing this repository can currently run.

## Q5 — what the shipped tests actually test

Three of the 20 files Q4 counted, each read from its imports:

1. `apps/ui/src/api/actionClass.test.ts` (53 lines) — imports `isActionKind` and
   `newestActionRow` from `./actionClass`, plus `STREAM_EVENT_CATALOG` from
   `./humanizeCatalog` and the `FeedRow` TYPE. It asserts on `isActionKind`,
   e.g. `expect(isActionKind("a_kind_no_catalog_has_heard_of")).toBe(true)`.
2. `apps/ui/src/cockpitLogic.test.ts` (110 lines) — imports `deriveAgentStatus`,
   `liveIsActive` and `selectChecklistRows` from `./cockpitLogic`, plus
   `normalizeApiFailure` and `normalizeDashboardPayload` from `./api/remedyApi`.
   It asserts on `deriveAgentStatus`, e.g.
   `expect(deriveAgentStatus(d).status).toBe("Needs your decision")` at :50.
3. `apps/ui/src/components/graph/buildForceBrainModel.test.ts` (46 lines) —
   imports `buildForceBrainModel` from `./buildForceBrainModel` and
   `normalizeDashboardPayload` from `../../api/remedyApi`. It asserts on
   `buildForceBrainModel` under the heading "decorative-dot invariants".

Every import in all three is a PURE FUNCTION or a type; none imports a
component, and none renders anything. THE REPOSITORY'S UI TEST STRATEGY IS
LOGIC-EXTRACTION: behaviour worth testing is pulled out of the component into a
plain module and tested as a function under `node`, which is why the third
example lives beside the graph component it serves yet imports no JSX.

## Q6 — the mount point

The composer is `RightLivePanel`, exported from
`apps/ui/src/components/panels/RightLivePanel.tsx` (53 lines by `wc -l`, read in
full).

Its card children render in this ORDER: `LiveStatusPill` (:18), `AgentNowCard`
(:19), `NeedsAttentionCard` (:20), `ActivityFeedCard` (:21),
`TaskChecklistCard` (:22). After them, outside the card sequence, an advanced
toggle `<button>` (:23) and a conditional `<div data-testid="advanced-details">`
(:32).

The wrapper element is `<aside className={styles.panel}>` at :17, and its
`data-ui` value is exactly `right-live-panel`.

`RightLivePanel` is rendered by `RemedyShell`, in
`apps/ui/src/components/shell/RemedyShell.tsx` — imported at :6 and rendered at
:65 with props `dashboard`, `onSelectNode`, `streamStatus`, `recent`,
`recentDropped`.

## Q7 — the overlap

`Needs your decision` under `apps/ui/src` — 6 occurrences over 4 files:

- `apps/ui/src/cockpitLogic.ts:30` — `return { status: "Needs your decision",
  detail: "A patch is waiting for approval.", isRunning: false };`
- `apps/ui/src/cockpitLogic.test.ts:46` and `:50` — the test name and the
  assertion on `deriveAgentStatus`.
- `apps/ui/src/components/panels/NeedsAttentionCard.tsx:12` — the derived item
  title; `:36` — the rendered `<h2>` heading.
- `apps/ui/src/api/remedyApi.ts:10` — a label map entry, `decision: "Needs your
  decision", blocker: "Blocker",`.

Does anything under `apps/ui/src/api/` reference the T001 route
`/api/jobs/<job_id>/decisions`? NO. That folder holds 37 entries; matching
`decisions|/api/jobs` over all of them returns 12 lines, and every one is either
an events route (`/events/stream`, `/events-since` in `brainStreamDeps.ts` and
its test), a dashboard/brain route (`remedyApi.ts:601`, `:614`), or the English
word inside a comment (`budgetTick.ts:8`). Widening the search to ALL of
`apps/ui/src` for `decisions` leaves exactly ONE hit — that same
`budgetTick.ts:8` comment. There is no client, no URL builder, no type and no
fetch for the decisions route anywhere in the UI source.

IN ONE SENTENCE: a surface already ships under the inbox's own name — a
`NeedsAttentionCard` headed "Needs your decision", mounted third in the right
panel — while the data path T001 built is referenced by nothing in the UI at
all, so T002 is not a greenfield addition but a REPLACEMENT of a heuristic card
whose title the new feature claims.

## Observations

1. The two gaps are independent and both are real. Q1: no visual authority for a
   decision CARD (only a graph GLYPH row in `assets_spec.md:174`). Q4: no
   toolchain that can mount a component at all. A ruling on one does not settle
   the other.
2. The Q4 gap has a cheap shape the logic-extraction strategy of Q5 already
   models: derive the card's rows in a pure module beside the component and test
   THAT under `node`, needing no new dependency. The expensive shape adds a DOM
   harness and a `.tsx` include glob. R10 owns that choice; this file measures
   it, and rules nothing.
3. Q7 is the finding a plan would otherwise miss: `NeedsAttentionCard` already
   occupies the inbox's name and slot. Its title string is also asserted in
   `cockpitLogic.test.ts:50` through `deriveAgentStatus`, so replacing the card
   without touching `cockpitLogic.ts:30` leaves two sources for one phrase, and
   touching it breaks a shipped test. That coupling is a T002 design input.
4. Q2 removes one worry entirely: 58 tokens are shipped, including
   `--remedy-state-open` and `--remedy-state-blocked`, so no new token is owed.
5. Not measured here, and named as absent rather than guessed: whether
   `npx vitest` actually passes at this tree. No suite was run for this file —
   the round's ordered suites are the five Python ones in G9, and no gate of
   this round orders the UI suite.
