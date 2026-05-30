# Plan — Steps 74.1, 75, 76, 77, 78, 79

## Goal
Redaction precision, interactive controls, spatial layout, motion/depth, guidance rail, viewer preview.

## Current Step
All steps complete. Commit + push + PR.

## Steps
- [x] Step 74.1: Redaction gate precision (redaction_patterns.py, precise secret detection)
- [x] Step 75: Interactive brain control surface (search, filter, next-action rail, copy commands, keyboard)
- [x] Step 76: Spatial layout v1 (semantic zones, zone-based radial positioning)
- [x] Step 77: Motion & depth system v1 (mist, scanlines, grid, edge glow, sel-pulse)
- [x] Step 78: Human guidance rail v1 (guidance.py, guide CLI, viewer guidance rail)
- [x] Step 79: Viewer preview & share v1 (brain open/viewer-path/export-viewer, manifest)
- [x] Tests: 2841 passing
- [x] Smoke: PASSED (12aj-12am sections)

## Risks
- Viewer HTML is large — keep JS minimal, no external deps
- No external assets/CDN/fonts
