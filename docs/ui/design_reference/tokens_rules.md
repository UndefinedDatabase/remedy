# D — Token Rules

## Where each group is used
- **Status palette** (`--remedy-state-*`): graph node fills/rings, task-tile
  fills, chip dots, timeline event tints, status text. NOTHING else may define
  a status color. Bridge to api types: `suggested`→open, `pending`→planned,
  `current`→in-progress (documented in `forceBrainTypes.ts` comments — keep).
- **Graph tokens** (`--remedy-graph-*`): the ONLY colors a graph renderer may
  paint. Canvas renderers read them once per mount via
  `getComputedStyle(document.documentElement)` into a palette object (pattern
  already used implicitly; make it explicit in `renderers/palette.ts`).
- **Spacing**: all padding/margin/gap use `--remedy-space-*` steps; odd values
  only inside glyph path math.
- **Motion**: every transition/animation duration+easing reads
  `--remedy-dur-*`/`--remedy-ease-*`; canvas animations mirror the same
  numeric constants exported from `renderers/palette.ts` (one source file
  re-exporting the CSS values).
- **Z-index**: no literal z-index anywhere; only the layer tokens.

## Forbidden
- Raw hex/rgb(a)/hsl(a) in component CSS or TSX, except inside `tokens.css`
  and the carve-out below. A `var()` fallback literal counts: it is a second
  copy of a palette value.
  - **Carve-out** (amended F273 T006, R-0755): paint that cannot resolve
    `var()` — the 2D canvas renderer `ForceBrainGraph.tsx`, the SVG
    presentation attributes of `BrainGraphCanvas.tsx`, `CodeOrbIcon.tsx` and
    `NetworkLogoIcon.tsx`, and the MUI theme object in `main.tsx`. These
    migrate to the palette bridge (`renderers/palette.ts`, not built yet) and
    leave the carve-out when it lands.
  - **Enforcement, as built:** no stylelint or ESLint colour gate exists. The
    gate is `tests/ui_contracts/test_raw_colour_ratchet.py`: carved-out files
    are exempt, every other file's pre-existing literals are pinned per file
    and only shrink, and any other file must hold none. A stylelint
    `declaration-property-value-allowed-list` gate remains the target once
    that debt reaches zero.
- New fonts, new radii, new shadows without a token PR.
- Status colors used for non-status meaning (e.g. green as "brand").

## Deviations
Any visual deviation from `ux_design.png` MUST be recorded in
`docs/ui/design_reference/deviations.md` (create on first deviation): what,
where, why, screenshot crop. Reviewers treat undocumented deviations as
findings (mirrors roadmap F101 discipline).

## Asset tokens
Font/icon/glyph tokens are governed by `assets_spec.md` (the asset authority);
this file governs their CSS usage. The two never conflict: assets_spec decides
WHAT the assets are, tokens_rules decides HOW their tokens are consumed.

## Keeping future UI consistent
New components: consume tokens only; propose new tokens via a PR touching
`tokens.css` + this file + one usage. The `--rm-*` block in
`docs/roadmap/CONVENTIONS.md` is superseded by this file — patch note in
`feature_reference_block.md` (do not maintain two palettes).
