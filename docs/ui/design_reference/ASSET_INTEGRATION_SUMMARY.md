# Asset Integration Summary (2026-07-04, final pass)

## Canonical decisions
| Asset class | Decision | Package / source | License |
|---|---|---|---|
| UI font | **Manrope Variable** (first in stack; deterministic) | `@fontsource-variable/manrope` (self-hosted via npm) | SIL OFL 1.1 |
| Mono font | **JetBrains Mono Variable** | `@fontsource-variable/jetbrains-mono` | SIL OFL 1.1 |
| Generic icons | **lucide-react** (single library) | npm `lucide-react` | ISC |
| Brand + product glyphs | custom set `components/icons/RemedyGlyphs.tsx` / `CodeOrbIcon.tsx` (preserved) | in-repo SVG | project |
| Graph ontology glyphs | dual-render source `graph/renderers/glyphPaths.ts` (canvas Path2D + SVG export) | in-repo | project |
| Logo | `RemedyMark` + "REMEDY" wordmark via `rail/RemedyLogo.tsx` (matches ux_design.png) | in-repo | project |

## Conflicts found & resolved
1. **Nondeterministic fonts:** no `@font-face`/binaries anywhere; stacks began
   with proprietary "Avenir Next"/"SF Mono" → rendering differed per OS and
   would break golden screenshots. Resolved: self-hosted variable fonts first;
   proprietary names removed from active stacks (tokens.css CHANGED note).
2. **Two icon systems:** custom thin-stroke SVG set (matches the screenshot)
   vs. `@mui/icons-material` in `pipeline/StopReasonCard.tsx`,
   `pipeline/PipelineTimeline.tsx`, `layers/LayerSwitcher.tsx` (does not
   match). Resolved: custom set canonical; Material usages get a 1:1 Lucide
   migration table (assets_spec §3); `@mui/icons-material` then removed.
   This also **corrects the earlier audit line** that called MUI unused —
   codebase_audit.md updated honestly.
3. **Two logo marks:** `RemedyMark` (in use, matches screenshot) vs.
   `NetworkLogoIcon` (unused by the rail, hardcoded hex). Resolved:
   RemedyMark canonical; NetworkLogoIcon deprecated.
4. **No air-gap-safe loading rule existed:** resolved — npm self-hosting only,
   remote asset URLs CI-forbidden (assets_spec §8.4, matches roadmap F173).

## Files changed in this pass
- `docs/ui/design_reference/assets_spec.md` — NEW (the asset authority:
  audit, decisions, glyph table, naming rules, CI checks, human checklist,
  agent rules).
- `docs/ui/design_reference/tokens.css` — font stacks CHANGED (deterministic);
  NEW groups: `--remedy-weight-*`, `--remedy-fs-*`, `--remedy-icon-*`,
  `--remedy-glyph-*`.
- `docs/roadmap/ROADMAP.md` Part I — `assets_spec.md` added to the binding
  spec list (one edit; structure untouched).
- All 64 UI-relevant feature files — the existing canonical block now carries
  the **ASSET REFERENCE** clause (fonts/icons/glyphs/logo via assets_spec;
  no new asset source without updating it + assumption_log).
- `acceptance_criteria.md` — §3 extended with asset gates; "do not pass if"
  gains the asset rule. `README.md` package table + `tokens_rules.md`
  cross-pointer + `codebase_audit.md` correction updated.

## Follow-ups for Stage 1 (implementation, not spec)
`npm i @fontsource-variable/manrope @fontsource-variable/jetbrains-mono
lucide-react` in `apps/ui`; import both fonts at the top of
`src/styles/globals.css`; adopt the token additions into
`apps/ui/src/styles/tokens.css`; migrate the three Material-icon files per the
§3 table, then drop `@mui/icons-material`; add the §8 CI gates (stylelint
font allow-list, ESLint restricted imports, binary/remote-URL greps,
fonts.ready golden rule).
