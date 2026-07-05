# C — Canonical Design Specification (the screenshot is law)

Values measured from `ux_design.png` at the 1678×926 design frame
(screenshot ≈1.295× of frame; all px below are FRAME px). Where a value cannot
be read exactly it is marked **(estimated)**.

## 1. Visual direction
Bright, airy "ice + indigo" glass cockpit. One luminous organism at center on a
soft periwinkle field with faint starfield depth; everything else is quiet
white glass. Nothing saturated except semantic status color and the indigo
accent. No dark mode in this reference. No cartoon, no cyberpunk, no noise.

## 2. Layout structure & page grid
Fixed design frame 1678×926 centered in the viewport (contract:
`docs/ui/RICHTIG_PIXEL_LOCK_SPEC.md` — unchanged, authoritative):

| Region | x | y | w | h | Component |
|---|---|---|---|---|---|
| Left rail | 0 | 0 | 292 | 926 | LeftBrandRail |
| Center stage | 292 | 0 | 976 | 926 | MetricsBar/CommandBar/Graph/Timeline |
| Right panel | 1286 | 24 | 350 | 832 | RightLivePanel |
| Top metrics | 292+24 | 24 | ~928 | 90 | TopMetricsBar |

Inside the stage: metrics card (y 24, h 90) → command bar (y ~138, h 56)
→ graph canvas (fills middle; filter chips docked bottom-left of it, y ~830)
→ phase timeline card (y ~≥856 to 926−24, h ~96). Global outer gutter 24;
inter-card gap 20 **(estimated ±4)**.

## 3. Background treatment
Body: layered gradients (keep `globals.css` recipe, recalibrated):
white bloom ellipse behind the graph core (`rgba(255,255,255,.95)` → transparent
70%), soft blue tint ellipse (`rgba(140,180,255,.22)`), base linear
150° `#f7faff → #ecf2fb → #e4edf8`. The graph canvas adds its OWN depth layer
(starfield + vignette, see graph_spec §9) — never on body, so panels stay clean.

## 4. Glass card rules
- Surface `var(--remedy-glass-bg-strong)` (white .78), border 1px
  `var(--remedy-glass-border)`, radius `--remedy-radius-lg` (20) for panel
  cards, `--remedy-radius-xl` (26) for the hero metrics card **(estimated)**.
- backdrop-filter blur(14px); inner top highlight `--remedy-shadow-inset-like`
  via 1px white top border is NOT in the reference — omit.
- Shadow: `--remedy-shadow-soft` default; hover lifts to `--remedy-shadow-card`.
- Nesting rule: glass on glass max depth 2; inner tiles use
  `--remedy-card-soft` without blur.

## 5. Typography
- Family: `--remedy-font-ui` stack — **Manrope Variable first** (self-hosted,
  deterministic on every OS; assets_spec.md §1 is the authority), falling back
  to Manrope/Inter/system sans. "Avenir Next" is removed from active stacks
  and may not be reintroduced.
- Hierarchy (frame px / weight / tracking):
  - Kicker/labels: 11 / 600 / +0.12em, uppercase, `--remedy-ink-soft`
    ("OPEN", "PLANNED", "AGENT IS DOING NOW", "CHAT / ACTIVITY", "TASKS").
  - Page title (rail): 26 / 700 / +0.01em, `--remedy-ink-strong`, 1.15 line
    ("GROWING BRAIN OVERVIEW" slot) **(estimated 24–28)**.
  - Rail body: 14 / 500 / 0 / `--remedy-ink-soft`, 1.5.
  - Metric value: 30 / 700 / tabular-nums / `--remedy-ink-strong`.
  - Card titles ("Builder is implementing…"): 14 / 600.
  - Body/feed: 13 / 500 / 1.45; timestamps 11 / 500 `--remedy-faint`.
  - Task rows: 12.5 / 500; status text 11.5 / 600.
  - Mono (`collect_file_metadata()`): `--remedy-font-mono` 13.

## 6. Iconography
Thin-line 1.5px rounded-cap icons, 20–22px box, ink-soft color; active nav icon
sits in a 44px glass squircle with accent tint + soft glow. Sources: `lucide-react`
(the only generic library) plus the `icons/RemedyGlyphs.tsx` custom set —
assets_spec.md §3 is the authority. Material icons are forbidden in the
canonical UI (existing `@mui/icons-material` usages migrate per the §3 table).
The sparkle icon in
the command bar and `</>` orb reuse `CodeOrbIcon`/glyph paths.

## 7. Navigation (SideIconDock)
Vertical glass pill (radius 22) hugging the rail, ~56px wide, 7 icon slots at
44px pitch; active = accent icon + `rgba(76,131,255,.12)` fill + 1px accent
border at 25% + outer glow `--remedy-glow` at 20% **(estimated)**. Hover =
ink; focus = 2px `--remedy-focus` ring. Tooltips right side, 11px labels.

## 8. Buttons
- Primary pill (e.g. "All" chip, send arrow): fill `--remedy-blue`, text white,
  radius 999, h 32 (chips) / 36 (send), shadow `0 6px 16px rgba(76,131,255,.35)`
  **(estimated)**; hover `--remedy-blue-strong`; active translateY(1px).
- Ghost: ink-soft text, transparent, hover `rgba(76,131,255,.08)`.
- "+ Add Task": full-width ghost row inside the tasks card, 13/600 ink-soft,
  leading plus glyph; hover accent text.
- Disabled: 45% opacity + not-allowed cursor + honest tooltip.

## 9. Command bar (Ask/jump)
Glass pill h 56, radius 999… actually radius 18 **(estimated 16–20)**; left
sparkle icon in a 36px accent-tinted disc; placeholder "Ask your agent or jump
to anything (e.g., "improve error handling")" ink-faint 14/500; right circular
36px glass button with return-arrow glyph. Focus: 2px focus ring + slight
brighten; typing shows live jump matches (existing `handleJump` logic) in a
dropdown glass sheet (radius 14, items 13px, ↑↓+Enter navigable).

## 10. Metrics bar
One hero glass card; 4 segments divided by 1px `--remedy-line` verticals.
Segment: icon disc 40px (accent-tinted line icon), kicker label, value 30/700.
PROGRESS segment: value "68%" + 6px track (radius 3, `--remedy-blue-100`) with
accent fill and 350ms width transition; percent uses tabular-nums. Tooltips
(existing metric.tooltip) on hover as glass tip. Unknown values render "—"
with an honest tooltip (never fake zeros; keep `unknown` semantics).

## 11. Right panel
350px column of stacked glass cards, 16px gaps:
1. Header row: "AGENT IS DOING NOW" kicker + LIVE pill (green dot pulse).
2. AgentNowCard: 40px role disc (`</>` builder blue), title 14/600 two-line,
   right-aligned "Just now" 11 faint.
3. CHAT / ACTIVITY card: kicker; feed rows (role disc 30px, name 12.5/700 +
   time 11 faint, message 13/500 ink, 1.45); user rows use initial-letter disc.
   Bottom: input "Ask something…" (h 40, radius 12, `--remedy-bg-2` fill, 1px
   line border) + 36px primary send button. Input DISABLED until steering
   exists (tooltip: "Steering arrives with a later feature — watching only for
   now."). Feed max-height ~38vh, thin scrollbar.
4. TASKS card: kicker + right-aligned "24 of 36 completed" 11 faint; rows h 30:
   leading 16px state tile (done: green rounded square + white check;
   in-progress: blue square outline… reference shows filled blue square with
   check for the first in-progress and doc glyph for later ones — canonical
   rule: done=green filled check tile, in_progress=blue filled check tile only
   when partially applied else doc glyph + "• In Progress" right text,
   planned=doc glyph + "Planned") — right status text 11.5/600 colored
   (done green, in-progress blue with leading dot, planned ink-faint).
   Mono-ish task labels stay 12.5 sans (reference shows sans with underscores).
   Row hover: `rgba(76,131,255,.06)` + focus ring; click = select node (exists).
5. "+ Add Task" ghost row (opens inject flow when available; else disabled).
NeedsAttentionCard: only renders when attention exists; style as warn-tinted
glass card at slot 2.5 (kicker "NEEDS ATTENTION", `--remedy-red-500` accents).

## 12. Timeline (bottom)
Glass card h ~96. Track: 6 phase stops (Job, Planning, Build, Test, Review,
Finalized): done = 22px white disc, 2px accent ring, accent check; current =
22px accent-filled disc with white ring + glow pulse; future = 18px
`--remedy-line-strong` ring disc. Connectors 4px: done segments solid accent,
current segment accent→track gradient, future `--remedy-blue-100`. Below:
event chips (26px glass discs) grouped under their phase — `</>` LLM action
(blue tint), flask test (ink), person review (ink); plus the small tick marks
row. Legend row bottom-center: three glyph+label pairs 11px. Scrubber: the
current-phase disc doubles as the drag handle (grab cursor); dragging enters
replay (LIVE pill switches to "REPLAY", accent→violet) — wire in Stage 4.

## 13. Filter chips (graph dock)
Glass pill dock bottom-left inside the stage, radius 999, padding 6; chips:
"All" solid primary; others ghost with 8px status dot (Open violet, Planned
white+ring, Done green) + 12.5/600 label. Selected ghost chip: accent text +
`rgba(76,131,255,.10)` fill. Keyboard: arrow keys cycle; chips are buttons
with aria-pressed.

## 14. States (global rules)
- **Empty:** stage shows core + message "No visible tasks" (existing
  FILTER_EMPTY_MESSAGES copy) in a small glass tip; panels show quiet
  one-line empties, never illustrations.
- **Loading:** skeleton shimmer ONLY inside cards (1.2s ease-in-out,
  `--remedy-blue-50` base); the graph shows the core breathing at 50% glow.
- **Error/degraded:** existing `DegradedBanner` (top, warn tint) is canonical;
  cards show "—" + tooltip; never fake data (P6).
- **Disabled:** 45% opacity + honest tooltip; **Focus:** 2px
  `--remedy-focus` outer ring, radius follows control; **Hover:** lift/ tint
  as per component; никогда color-only state changes (add icon/ring).

## 15. Responsive behavior
The pixel-lock frame scales down uniformly ≥1280 viewport width; below 1280:
right panel becomes an overlay sheet (toggle in nav), rail collapses to the
icon dock (brand block hides), stage keeps min 720px. ≤430px (PWA later, F201
lineage): status/digest/inbox surfaces only — out of scope here except: do not
hard-code the frame; all regions read the CSS vars `--remedy-left-width`/
`--remedy-right-width`.

## 16. Reduced motion
`prefers-reduced-motion` (already global-killed in globals.css + Provider):
graph birth = fade-in (no spring), no particles, pulse → static 70% glow,
progress bar jumps, LIVE dot static. Everything remains state-readable
without motion (motion is garnish, never information — a11y rule).

## 17. Copy rules (absorbed from the rebuild pack — still binding)
Default UI never shows: rank, importance, node_type, metadata, present/missing
signals, context coverage, zone, edge_type, connected_to, raw UUIDs, raw JSON,
raw stdout/stderr, tracebacks. Human phrasing via `src/copy/humanCopy.ts` only.
