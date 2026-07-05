# Final Design Reference Summary — Pre-Commit State (2026-07-04)

One-page orientation for humans and coding agents. This folder is the design
authority for the Remedy cockpit; `docs/roadmap/` is the behavior authority.

## Authority chain (memorize this)
`ux_design.png` (2174×1206, measured; = the 1678×926 design frame at ≈1.295×)
→ `assets_spec.md` + `tokens.css` → `graph_spec.md` / `ux_spec.md` /
`component_spec.md` / `motion_spec.md` → roadmap feature-file prose.
Feature prose never overrides the design reference on visual matters.
Deviations require an assumption_log entry with a technical reason.

## Canonical decisions (final)
- **UI font:** Manrope Variable, self-hosted (`@fontsource-variable/manrope`,
  OFL 1.1), FIRST in every stack. "Avenir Next" is removed from active stacks
  (deterministic rendering law); it appears in this folder only as audit
  history.
- **Mono font:** JetBrains Mono Variable (`@fontsource-variable/
  jetbrains-mono`, OFL 1.1); "SF Mono" survives only as an OS fallback.
- **Icons:** `lucide-react` (ISC) is the ONLY generic library; the custom
  Remedy SVG set (`RemedyGlyphs.tsx`, `CodeOrbIcon.tsx`) covers brand +
  product glyphs. `@mui/icons-material` is forbidden — the three existing
  usages migrate per `assets_spec.md` §3, then the dependency is removed.
- **Graph glyphs:** one dual-render source (`glyphPaths.ts`: canvas Path2D +
  SVG export); the 15-glyph table in `assets_spec.md` §4 + `graph_spec.md` §5
  win over any feature prose (T5_F020 harmonized accordingly — job core is
  the gradient `</>` sphere, not a hexagon).
- **Logo:** `RemedyMark` + "REMEDY" wordmark via `RemedyLogo.tsx`;
  `NetworkLogoIcon.tsx` deprecated.
- **Tokens:** namespace `--remedy-*`, canonical file `tokens.css` here
  (status palette, graph, icon, glyph, spacing, motion, z, rank groups).
  `--rm-*` exists ONLY as deprecation/migration notes (ROADMAP Part E map).
- **Renderer:** react-force-graph-2d with fully custom painting now; PixiJS v8
  only behind the measured F233 gate (`graph_tech_recommendation.md`).

## Roadmap integration state
- ROADMAP Part I = binding design-authority statement (this folder listed,
  including `assets_spec.md`); Part E = canonical token pointer + migration
  map; A8 points UI prompts here.
- 64 UI-relevant feature files carry BOTH the CANONICAL DESIGN REFERENCE and
  ASSET REFERENCE blocks (record: `feature_reference_block.md`).
- Tier-0 dependency fix applied: STATUS.md and Part F order is
  F146 → F081 → F147 → F148 (init needs project identity; the golden path
  needs init). F147 hard-depends only on F146; F014 (Tier 1) later completes
  full Flight Plan rendering. Dependency metadata across all feature files
  now lists only hard blockers in "Depends on:" — forward references moved to
  Later integrates / Enhanced by / Future UI integration (record:
  `FINAL_CLEANUP_SUMMARY.md`).

## Machine-checked before packaging (all green)
250 feature files, F001–F250 gapless, no duplicates · STATUS.md: 250 unique
entries, matches the file set, A5 points at it · every UI-relevant feature
carries the design + asset reference blocks · remaining `--rm-*` occurrences
are limited to the explicit deprecation/migration notes · zero legacy hex
palette, zero temp paths, zero font binaries · Avenir Next / SF Mono /
Material mentions exist only as historical, fallback or migration notes ·
`ux_design.png` present, all references use the repo path. Fresh results of
the latest pass: `FINAL_CLEANUP_SUMMARY.md`.

## Open follow-ups (implementation, Stage 1 — not spec gaps)
1. `npm i @fontsource-variable/manrope @fontsource-variable/jetbrains-mono
   lucide-react`; import fonts atop `apps/ui/src/styles/globals.css`.
2. Adopt this folder's `tokens.css` additions into
   `apps/ui/src/styles/tokens.css`.
3. Migrate the three Material-icon files per `assets_spec.md` §3; remove
   `@mui/icons-material` (evaluate `@mui/material` in the same PR).
4. Add the CI gates from `assets_spec.md` §8 + `acceptance_criteria.md` §3.
5. Banner/archive the two stale UI docs and the root implementation pack;
   retire the legacy CONVENTIONS `--rm-*` block with the old roadmap
   generation (`feature_reference_block.md`, follow-ups).
