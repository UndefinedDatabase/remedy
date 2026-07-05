# Remedy Asset Specification — CANONICAL (v1.0 · 2026-07-04)

**This file is the asset authority.** Fonts, icons, graph glyphs, logo and
image assets for the Remedy UI are decided HERE. `ux_design.png` stays the
visual authority; `tokens.css` the token authority. No new font, icon library,
glyph style, logo treatment or asset source may be introduced unless this file
is updated first and the deviation is documented in assumption_log with a
technical reason. Audit basis: review bundle 2026-07-04 (paths verified).

---

## 0. Existing-asset audit (verified)
- **Fonts:** no `@font-face`, no fontsource packages, no font binaries, no
  remote font imports anywhere (`apps/ui/index.html` loads nothing; grep over
  `apps/ui/src` clean). Font stacks in `apps/ui/src/styles/tokens.css` begin
  with **"Avenir Next"** (proprietary, macOS-only) → rendering is currently
  **OS-dependent and nondeterministic** — the single biggest asset conflict
  with golden-screenshot discipline.
- **Icons:** TWO systems coexist. (a) Custom thin-stroke SVG set
  `apps/ui/src/components/icons/RemedyGlyphs.tsx` (strokeWidth 1.4–1.6, round
  caps — matches the screenshot) plus `CodeOrbIcon.tsx`,
  `NetworkLogoIcon.tsx`. (b) **Material icons in active use** at
  `components/pipeline/StopReasonCard.tsx`, `components/pipeline/
  PipelineTimeline.tsx`, `components/layers/LayerSwitcher.tsx`
  (`@mui/icons-material`: WarningAmber, Info, CheckCircle, Error,
  HourglassEmpty, RadioButtonUnchecked, RemoveCircleOutline, AutoAwesome,
  FactCheckOutlined, FolderOutlined…). Material's filled/geometric style does
  NOT match the screenshot's thin rounded line icons — conflict resolved in §3.
- **Logo:** canonical mark in use = `RemedyMark` (dot-ring neuron,
  `icons/RemedyGlyphs.tsx`) composed by `rail/RemedyLogo.tsx` with the
  "REMEDY" wordmark — matches the screenshot. `NetworkLogoIcon.tsx` (triangle
  network, hardcoded `#4c83ff`) is an unused-by-the-rail alternate → deprecated
  (§5).
- **Images:** none in `apps/ui` (no png/svg/woff files, no `public/`);
  the only design image is `docs/ui/design_reference/ux_design.png`.
- **Graphics deps** (`apps/ui/package.json`): `react-force-graph-2d`,
  `d3-force` (graph); `@mui/material` + `@emotion/*` (UI lib, minimal usage);
  no icon-font, no tailwind.

---

## 1. Canonical UI font

- **Canonical decision:** **Manrope (variable)** — self-hosted.
- **Reason:** the exact screenshot font **cannot be proven from pixels** (no
  font metadata exists in the repo; the current first-stack "Avenir Next" is a
  plausible origin of the mock but is proprietary and macOS-bound). Manrope is
  the closest practical open font to the screenshot's geometric-humanist,
  softly rounded, wide-tracked look; it is already second in the existing
  stack and was the roadmap's declared font. Choosing it as FIRST makes
  rendering deterministic on every OS/CI — a hard requirement for golden
  screenshots (acceptance_criteria §1).
- **Source / package:** `@fontsource-variable/manrope` (npm).
- **License:** SIL Open Font License 1.1 (bundling + self-hosting allowed).
- **Install / import:** `npm i @fontsource-variable/manrope` in `apps/ui`;
  first line of `src/styles/globals.css`:
  `@import "@fontsource-variable/manrope";`
  Optional preload of the woff2 in `index.html` for first-paint stability.
- **Token integration:** `--remedy-font-ui` / `--remedy-font-display` updated
  (tokens.css) to `"Manrope Variable", "Manrope", "Inter", -apple-system,
  BlinkMacSystemFont, "Segoe UI", sans-serif`. **"Avenir Next" is removed from
  active stacks** (determinism law).
- **Weights (variable axis 200–800; used):** 500 body/rows · 600 kickers,
  labels, buttons · 700 titles, metric values, wordmark · 800 reserved (never
  without a tokens_rules PR). Tokens: `--remedy-weight-*`.
- **Usage rules by area:** everything human-readable uses `--remedy-font-ui`;
  sizes/hierarchy per `ux_spec.md` §5 (now tokenized as `--remedy-fs-*`);
  uppercase kickers always pair with `--remedy-tracking-label`.
- **Loading strategy:** self-host only (works in air-gap builds, F173 law);
  `font-display: swap` (fontsource default) + test harnesses await
  `document.fonts.ready` before capturing goldens.
- **Fallback behavior:** if the webfont fails, the stack degrades to
  Inter/system sans; UI must remain layout-stable (no metric-dependent
  truncation — verify via the fallback test, §8).
- **Forbidden:** remote font CDNs (Google Fonts links etc.), "Avenir Next" in
  any active stack, committing font binaries to git (they arrive via npm),
  base64 fonts in CSS, any second UI typeface, faux-bold/italic synthesis.

## 2. Canonical monospace font

- **Canonical decision:** **JetBrains Mono (variable)** — self-hosted.
- **Reason:** diffs, prompt traces, task symbols (`collect_file_metadata()`),
  console/log surfaces need a deterministic technical mono; the current
  first-stack "SF Mono" is Apple-proprietary. JetBrains Mono reads
  technically serious, has clear `0O/1lI`, OFL-licensed.
- **Source / package:** `@fontsource-variable/jetbrains-mono` (npm).
- **License:** SIL OFL 1.1.
- **Install / import:** `npm i @fontsource-variable/jetbrains-mono`; import in
  `globals.css` after Manrope.
- **Token integration:** `--remedy-font-mono` → `"JetBrains Mono Variable",
  "JetBrains Mono", ui-monospace, "SF Mono", Menlo, Consolas, monospace`.
- **Usage:** code spans in feed/now-card, diff viewer, prompt-trace previews,
  runtime console (F237), task symbol labels. Size 12–13 per ux_spec.
- **Forbidden:** mono for headings/labels; ligatures ON for diffs (set
  `font-feature-settings:"liga" 0` on diff surfaces — token comment).

## 3. Canonical icon system

- **Canonical decision:** **Two-part system, strictly ruled:**
  (a) **`lucide-react` (ISC license)** is the ONLY generic icon library;
  (b) the **custom Remedy SVG set** (`components/icons/RemedyGlyphs.tsx` +
  `CodeOrbIcon.tsx`) is the ONLY source for brand marks and product-specific
  glyphs (code orb, neuron mark, graph-adjacent chrome).
- **Reason:** the screenshot's icons are thin (≈1.5px) rounded-cap line icons
  — exactly Lucide's design system and exactly the existing RemedyGlyphs
  style; Material's geometry does not match. Lucide: ISC, tree-shakeable,
  React-first, 1500+ icons, stroke-width prop.
- **Migration (existing icons):** custom set = **preserve** (canonical);
  Material usages = **replace** in the three files above (mapping:
  WarningAmber→`TriangleAlert`, Info→`Info`, CheckCircle→`CircleCheck`,
  Error→`CircleX`, HourglassEmpty→`Hourglass`,
  RadioButtonUnchecked→`Circle`, RemoveCircleOutline→`CircleMinus`,
  AutoAwesome→`Sparkles`, FactCheckOutlined→`ListChecks`,
  FolderOutlined→`Folder`); then remove `@mui/icons-material` (and evaluate
  `@mui/material` removal — separate cleanup PR, flagged since the design
  audit).
- **Geometry rules:** stroke `--remedy-icon-stroke` (1.5); linecap/linejoin
  **round**; no filled icons except status tiles (task done/progress tiles are
  drawn shapes, not library icons); corner softness = Lucide default.
- **Sizes:** `--remedy-icon-sm` 16 (inline/status) · `--remedy-icon-md` 20
  (nav, metrics, feed) · `--remedy-icon-lg` 22 (hero metric discs).
- **Color rules:** default `--remedy-icon-color` (ink-soft) · hover
  `--remedy-icon-hover` (ink) · active `--remedy-icon-active` (blue) ·
  disabled `--remedy-icon-disabled` (faint, 45% context opacity). Never status
  colors on non-status icons.
- **Area rules:** *Navigation* (SideIconDock): md size, active slot =
  `--remedy-icon-nav-bg` squircle + glow (ux_spec §7). *Metrics*: lg icon in a
  40px disc `--remedy-icon-metric-bg`. *Right sidebar*: role discs use Remedy
  glyphs (builder `</>` = CodeOrbGlyph), generic actions Lucide md.
  *Activity feed*: 30px role discs; kind→glyph fixed (build=code orb,
  review=user-round, test=flask via graph glyph export, user=initials disc,
  system=dot). *Task status*: drawn tiles per ux_spec §11.4 (NOT library
  checkmarks; the check inside the tile is a 2px path from glyphPaths).
  *Timeline*: phase stops drawn; event chips use the GRAPH glyph exports (§4)
  so canvas and timeline match. *Live badge*: plain dot + text, no icon.
  *Evidence/detail panel*: Lucide md for actions (copy, external-link,
  chevron), Remedy glyphs for kind markers.
- **Accessibility:** icon-only controls MUST have `aria-label`; decorative
  icons `aria-hidden="true"`; labels come from `humanCopy.ts` keys.
- **When library vs custom inline SVG:** library for generic UI verbs/objects;
  custom ONLY for brand, graph ontology glyphs, and status tiles — anything
  that encodes Remedy semantics. New custom icons require an assets_spec PR.
- **Forbidden:** `@mui/icons-material` (after migration), Font Awesome,
  Heroicons/Tabler/Feather mixes, emoji as icons, icon fonts, filled Material
  style, per-feature one-off icon imports from other sets.

## 4. Canonical Growing-Brain glyph system

- **Canonical decision:** ONE dual-render glyph source —
  `apps/ui/src/components/graph/renderers/glyphPaths.ts` — exporting each
  glyph as (a) `Path2D` builders for canvas and (b) SVG path strings for DOM
  (legend, timeline chips, list view). Geometry normalized to a 24×24 box,
  scaled by the renderer. This is the codified form of `graph_spec.md` §5;
  on conflict, graph_spec §5 + this table win over any feature-file prose.
- **Rendering:** canvas = stroke `--remedy-icon-stroke`×scale, round caps;
  glow via pre-rendered gradient sprites (never per-frame shadowBlur —
  graph_spec §13); state colors exclusively from `--remedy-state-*`;
  glow colors from `--remedy-graph-*`.
- **Accessibility fallback:** every glyph has a text name in the shared
  catalog (used by the list view + tooltips); canvas stays `aria-hidden`
  (graph_spec §14).
- **Never generic:** job core, synapse, cluster, decision, vetoed — these
  encode Remedy's ontology and must never be swapped for library icons.

| Glyph | Meaning | Shape (24-box) | Size @zoom 1 | Fill/Stroke | Glow/State |
|---|---|---|---|---|---|
| job_core | the job | `</>` mono glyph inside gradient sphere | r 26 + halo 64 | fill sphere, white glyph | core halo, breath (motion_spec) |
| builder_run | code action | drawn `< />` chevrons path | r 4.5 node; glyph at L1+ | stroke on state sphere | active pulse when running |
| review_run | reviewer | head-and-shoulders outline | r 4.5 | stroke | violet tint when open finding |
| test_run | test | flask (triangle-bottom beaker + neck) | r 4.5 | stroke | state color; fail = blocked red |
| repair_run | retry | `< />` + ¾ circular arrow ring | r 4.5 | stroke | pulse while repairing |
| artifact | document | doc rectangle + folded corner | 7×9 | stroke, corner filled | none (calm) |
| synapse | prompt/tool call | plain dot | r 1.6–2.2 | fill `--remedy-graph-particle` at 70% | particle motion only while active |
| decision | human gate | rounded diamond + dot | r 5 | stroke; dot = state | soft warn glow while open |
| blocked/failed | failure | node + small status dot; edge tint | r as kind | state blocked fill | NO glow (graph_spec §7) |
| vetoed | forbidden | node grayed + 45° strike slash | r as kind | gray stroke | downstream 40% alpha |
| cluster | collapsed n | circle + centered count text | r 9 | ring stroke, count ink | expands on click |
| live activity | now | plain dot | 8px (DOM) | `--remedy-live` | 1.6s pulse; static reduced-motion |
| budget/cost | spend (chips/L2 only) | coin: circle + inner ¢-bar | 16 DOM | stroke | warn tint ≥85% budget |
| checkpoint | resume point | bookmark flag on timeline | 14 DOM | stroke | none |
| branch/dep | dependency | curved edge itself (no icon) | — | edge styles graph_spec §6 | per-branch state |

## 5. Logo & wordmark
- **Canonical:** `RemedyMark` (dot-ring neuron) + wordmark "REMEDY"
  (Manrope 700, tracking `--remedy-tracking-label`+, color ink-strong) as
  composed by `rail/RemedyLogo.tsx` — matches the screenshot; keep.
- Mark colors must move to tokens (currentColor + opacity steps — already
  currentColor ✔); minimum size 20px; clear-space = mark radius.
- **Deprecated:** `NetworkLogoIcon.tsx` (unused by the rail, hardcoded hex) —
  remove or move to an archive folder in the next UI cleanup; never introduce
  raster logos; never restyle the mark per feature.

## 6. Image asset rules
Reference image: `docs/ui/design_reference/ux_design.png` (the only committed
design image). Product screenshots live in evidence folders, never in `src/`.
No stock photos; user avatars = initials discs (README §K2). Any future image
asset requires: purpose, license note, and an entry here. SVG over raster;
raster only for photographic evidence.

## 7. File naming & extension rules
Fonts: via npm only (no font files in git — CI check §8). Icons: Lucide
imports named per icon; custom glyph/SVG components PascalCase in
`components/icons/` (brand/UI) or `graph/renderers/glyphPaths.ts` (ontology).
New assets: kebab-case file names, license header comment. Approval: PR must
touch this file for any new asset class.

## 8. Automated acceptance checks (CI)
1. **No hardcoded font-family** outside `tokens.css` (stylelint
   `font-family` allowed-list = `var(--remedy-font-*)`).
2. **No foreign icon imports**: ESLint `no-restricted-imports` for
   `@mui/icons-material`, `@fortawesome/*`, `react-icons`, `@heroicons/*`,
   `@tabler/icons*` (allow-list: `lucide-react`, local `components/icons`,
   `glyphPaths`).
3. **No font binaries in git**: CI grep for `*.woff|woff2|ttf|otf` in the
   repo tree fails the build (fonts come from node_modules).
4. **No remote asset URLs**: grep for `fonts.googleapis|fonts.gstatic|cdn.` in
   `apps/ui/src` + `index.html` must be empty (air-gap law).
5. **Fallback test**: build with fontsource imports stubbed → app renders,
   layout snapshot within tolerance (no metric-dependent breakage).
6. **Bundle**: fonts ≤ 2 woff2 files loaded (Manrope var + JetBrains var);
   size-limit budget unchanged (+ fonts ≤ ~140 KB combined, estimated).
7. **Goldens await `document.fonts.ready`** (harness rule, asserted).
8. **Icon a11y**: axe rule — no icon-only button without accessible name.
9. **Glyph parity**: legend/timeline SVG paths === canvas Path2D source
   (import-identity test, graph_spec §5).
10. **Reduced motion**: animated glyphs (pulse/particles/breath) produce zero
    animation frames under the media query (existing harness).

## 9. Human visual review checklist
Typography: wordmark tracking matches the screenshot · kickers read as quiet
caps, not shouty · metric values align tabular · no faux bold anywhere · mono
surfaces clearly mono. Icons: one consistent line weight everywhere · nav
active state glows softly, not neon · no filled Material shapes anywhere ·
status tiles match §ux_spec 11.4. Glyphs: core reads as `</>` sphere at a
glance · run-kind glyphs distinguishable at L1 zoom · cluster counts legible ·
vetoed strike unambiguous · timeline chips visibly SAME family as graph glyphs.

## 10. Agent implementation rules (read this first)
Use tokens for every font/icon/glyph property; import icons only from
`lucide-react` or the local canonical files; never introduce an asset source
without editing THIS file; document any visual deviation in assumption_log
with a technical reason; when in doubt, the priority order is
`ux_design.png` → this file + `tokens.css` → `graph_spec.md`/`ux_spec.md` →
feature file prose.
