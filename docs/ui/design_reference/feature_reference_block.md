# I — Feature-File Integration (EXECUTED)

The canonical block below has been inserted into the roadmap feature files
listed here (unified English roadmap, `docs/roadmap/features/`). This document
is the record + the template for future UI features.

## Canonical reference block (as inserted)

```markdown
> **CANONICAL DESIGN REFERENCE:** This feature MUST follow the canonical Remedy
> UI design reference in `docs/ui/design_reference/`. `ux_design.png` is the
> visual authority; the written specs, tokens, component rules, graph rules and
> motion rules in that folder are binding for this feature. Builders must not
> invent a new visual language; any visual deviation must be documented in the
> assumption_log with a technical reason. All UI work uses the shared design
> tokens (`--remedy-*`) and component rules from the design reference.
```

## Files carrying the block (64)
- Tier 3: `T3_F084` (demo mode)
- Tier 4: `T4_F119`, `T4_F126`, `T4_F149` (memory-card UI)
- Tier 5 (Operator Cockpit, all): `T5_F008`, `T5_F009`, `T5_F015`,
  `T5_F019`–`T5_F033`, `T5_F035`–`T5_F044`
- Tier 6 (Design-to-Code, all): `T6_F087`–`T6_F102`
- Tier 7: `T7_F136`, `T7_F137`, `T7_F142`
- Tier 12: `T12_F201` (mobile view) · Tier 13: `T13_F210`, `T13_F212`
- Tier 16 (Cockpit v2, all): `T16_F233`–`T16_F242`

Feature-specific pointer notes were added where a spec section is the
authoritative elaboration (F019/F020/F023/F024 → graph_spec/motion_spec;
F044/F098/F233/F242 → acceptance_criteria; F096 → target-project token
namespace clarification; F119/F040 → "CSS below is an excerpt").

## Resolved in the roadmap itself
- `ROADMAP.md` Part I is now the binding design-authority statement.
- `ROADMAP.md` Part E: canonical tokens = this folder's `tokens.css`
  (`--remedy-*`); the former `--rm-*` palette is deprecated with an explicit
  migration map. All `--rm-*` mentions and legacy hex values in roadmap +
  feature files were migrated.
- `ROADMAP.md` A8 now points UI prompts at this folder.

## Remaining repo follow-ups (outside this package's file set)
1. `apps/ui/src/styles/tokens.css`: adopt the additions from this folder's
   `tokens.css` (graph/spacing/motion/z/rank/inset tokens) — Stage 1 task.
2. `remedy_ui_component_implementation_pack.md` (repo root): move to
   `docs/archive/` with a DEPRECATED banner pointing here.
3. DONE (2026-07-05): `docs/ui/REMEDY_UI_REBUILD_SPEC.md` rewritten as v2
   (design-reference banner, updated component tree, v1 token palette and
   five-level zoom table removed) and `RICHTIG_PIXEL_LOCK_SPEC.md` updated to
   v1.1 (density rules harmonized with graph_spec §8–§9; layout tokens
   292/350 now mirror the region table — tokens.css adjusted accordingly).
4. `docs/roadmap/CONVENTIONS.md` (legacy German generation, if kept): its
   `--rm-*` block is superseded by Part E — add the pointer or retire the file
   with the old generation.
