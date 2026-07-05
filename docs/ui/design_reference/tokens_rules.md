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
- Raw hex/rgba in component CSS or TSX (except inside `tokens.css` and the
  palette bridge). Enforce via stylelint `declaration-property-value-allowed-list`
  (colors must be `var(--remedy-…)`) + an ESLint no-color-literal rule for the
  graph renderer files. CI gate lands in Stage 1.
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
