# Plan — Steps 83-90

## Goal
Replace current viewer UX with real zoomable semantic brain UI using PixiJS + pixi-viewport + d3-force.

## Current Step
All steps complete. Self-review, commit + push.

## Steps
- [x] Step 83: Primary UI reset — legacy viewer quarantine, docstrings updated
- [x] Step 84: PixiJS Brain Canvas — `apps/ui/` with Vite/TS, pixi.js 8 + pixi-viewport 6 + d3-force
- [x] Step 85: Semantic Zoom Layering — ui_view_model.py, brain-view-model API, 6 layers
- [x] Step 86: Minimal Node Detail — floating compact card, detail API
- [x] Step 87: UI Command Flow — ui.latest, ui.status, ui.stop, ui.open, session registry
- [x] Step 88: UX Quality Gate v2 — 32 anti-regression tests
- [x] Step 89: Legacy Viewer Cleanup — docstrings mark legacy, new primary documented
- [x] Step 90: First Satisfaction Cut — all 2938 tests pass

## Risks
- PixiJS bundle ~327KB gzipped — acceptable for localhost-only
- pixi-viewport 6 requires pixi.js >=8 (addressed)
