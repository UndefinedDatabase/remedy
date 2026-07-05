# RICHTIG Pixel Lock Specification (v1.1 · 2026-07-05)

Layout contract for the Remedy cockpit. This file owns the FRAME GEOMETRY;
all other visual authority lives in `docs/ui/design_reference/`
(`ux_design.png` = the law; the checked-in image is 2174×1206, i.e. this
1678×926 frame at ≈1.295×).

## Design frame
- Width 1678 px · Height 926 px
- Pale blue/white gradient background (recipe: `ux_spec.md` §3)
- Centered on the viewport; scaled down uniformly on smaller viewports;
  never stretched beyond the frame on large screens
- Regions read the CSS vars (`--remedy-left-width` 292, `--remedy-right-width`
  350, `--remedy-frame-w/h`) — no second set of numbers in component CSS

## Frame regions (authoritative)
| Region | x | y | w | h |
|--------|---|---|---|---|
| Left rail | 0 | 0 | 292 | 926 |
| Center stage | 292 | 0 | 976 | 926 |
| Right panel | 1286 | 24 | 350 | 832 |
| Top metrics | 292 | 24 | 976 | 90 |
| Command bar | 292 | 132 | 976 | 56 |
| Graph stage | 292 | 190 | 976 | 552 |
| Filter chips | +150 | +500 (rel. graph) | — | — |
| Phase timeline | 150 | 758 | 1116 | 144 |
| Live pill | 1406 | 24 | 106 | 46 |

## Visual density & depth (harmonized with graph truth rules)
The center must read as a living organism, never as an empty chart — and
never through fake data. Density comes from the layered depth system of
`graph_spec.md` §8–§9, not from invented nodes:
- starfield speckles (~140, seeded, non-semantic, no hit area) + vignette
- capped decorative frontier dots (budget ≤120) on ACTIVE branches only
- beaded, curved edge filaments; branch glow on active branches
- every countable/clickable node maps 1:1 to a real view-model entity
For visual review, the seeded fixture job mirrors the reference density
(≈36 tasks with runs — `acceptance_criteria.md` §1). Right panel: ≥12 task
rows visible at frame height. Interaction affordances are small node
hotspots, not pill boxes.
(The v1 "ConstellationBackdrop ≥140 nodes / ≥180 edges" requirement referred
to a superseded legacy component and is replaced by the rules above.)

## Forbidden default visuals
- Immediate detail popup on load
- A visibly empty/sparse stage (fewer real elements than the fixture shows
  WITHOUT the depth layers compensating) or a plain white rectangle
- Pill boxes dominating the graph; repeated raw labels ("Task", "Output", …)
- Large unbalanced whitespace
- Debug wording — single source: `ux_spec.md` §17

## CSS coordinate contract
These values MUST appear in the built CSS: 1678 (frame width), 926 (frame
height), 292px (left rail), 976px (center stage), 1286px (right panel left),
350px (right panel width), 758px (timeline top). Verified by the
region-geometry test (`acceptance_criteria.md` §3).
