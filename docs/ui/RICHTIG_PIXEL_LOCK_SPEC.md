# RICHTIG Pixel Lock Specification

Implementation contract for the Remedy UI visual target.

## Design Frame

- Width: 1678px
- Height: 926px
- Background: pale blue/white gradient
- Centered on viewport; scaled down if viewport is smaller
- Never stretches beyond design frame on large screens

## Frame Regions

| Region | x | y | w | h |
|--------|---|---|---|---|
| Left rail | 0 | 0 | 292 | 926 |
| Center stage | 292 | 0 | 976 | 926 |
| Right panel | 1286 | 24 | 350 | 832 |
| Top metrics | 292 | 24 | 976 | 90 |
| Command bar | 292 | 132 | 976 | 56 |
| Graph stage | 292 | 190 | 976 | 552 |
| Filter chips | +150 | +500 (rel graph) | — | — |
| Phase timeline | 150 | 758 | 1116 | 144 |
| Live pill | 1406 | 24 | 106 | 46 |

## Forbidden Default Visual

- Immediate detail popup on load
- Sparse graph with < 60 visual nodes
- Pill boxes dominating the graph
- Raw labels like "Task", "Output", "Memory" repeated
- Plain empty white rectangle
- Large unbalanced whitespace
- Debug words: rank, importance, node_type, metadata, present signals, missing signals, context coverage, connected_to, edge_type, zone

## Visual Density Requirements

- ConstellationBackdrop: >= 140 nodes, >= 180 edges
- Deterministic seeded layout from jobId
- Dense branching from central orb
- Interactive hotspots overlay (small circles, not pills)
- Right panel: >= 12 task rows visible

## CSS Coordinate Contract

These values MUST appear in the built CSS:
- 1678 (frame width)
- 926 (frame height)
- 292px (left rail width)
- 976px (center stage width)
- 1286px (right panel left)
- 350px (right panel width)
- 758px (timeline top)
